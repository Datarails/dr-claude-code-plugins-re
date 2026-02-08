"""Authentication for Datarails Finance OS API.

Supports multiple authentication methods:
1. BrowserAuth (primary) - Session cookies extracted from browser, with automatic JWT refresh
2. EnvAuth (fallback) - Environment variables for CI/testing

Multi-Account Support:
- Credentials are stored per-environment (e.g., session_dev, session_app)
- Users can authenticate to multiple environments simultaneously
- Switch between environments without re-authentication

Datarails Auth Flow:
- Session cookies (sessionid, csrftoken) are long-lived (days/weeks)
- JWT access tokens expire in ~5 minutes
- JWT refresh tokens expire in ~3 days
- This module automatically manages token lifecycle using session cookies
"""

import base64
import json
import os
import threading
import time
from pathlib import Path
from typing import Any

import httpx

from datarails_mcp.constants import (
    DEFAULT_ENV,
    KEYRING_SERVICE,
    get_active_environment,
    get_environments,
    get_keyring_account,
)

# Fallback file location (used by Chrome extension native host)
FALLBACK_AUTH_FILE = Path.home() / ".datarails-auth.json"

# Keyring timeout (seconds) - prevents hanging in environments without a keyring backend
KEYRING_TIMEOUT = 5

# Lazy keyring import with availability check
_keyring_available: bool | None = None
_keyring_module = None


def _get_keyring():
    """Get keyring module with lazy import and availability check."""
    global _keyring_available, _keyring_module
    if _keyring_available is not None:
        return _keyring_module if _keyring_available else None
    try:
        import keyring
        _keyring_module = keyring
        _keyring_available = True
        return keyring
    except ImportError:
        _keyring_available = False
        return None


def _keyring_get_with_timeout(service: str, account: str, timeout: float = KEYRING_TIMEOUT) -> str | None:
    """Call keyring.get_password with a timeout to prevent hanging.

    On some platforms (containers, locked keychains), keyring can block
    indefinitely. This wraps it with a thread-based timeout.
    """
    kr = _get_keyring()
    if kr is None:
        return None

    result = [None]
    error = [None]

    def _get():
        try:
            result[0] = kr.get_password(service, account)
        except Exception as e:
            error[0] = e

    thread = threading.Thread(target=_get, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if thread.is_alive():
        # Keyring is hanging - give up
        return None

    return result[0]


def _keyring_set_with_timeout(service: str, account: str, value: str, timeout: float = KEYRING_TIMEOUT) -> bool:
    """Call keyring.set_password with a timeout."""
    kr = _get_keyring()
    if kr is None:
        return False

    success = [False]

    def _set():
        try:
            kr.set_password(service, account, value)
            success[0] = True
        except Exception:
            pass

    thread = threading.Thread(target=_set, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    return success[0] and not thread.is_alive()


def _keyring_delete_with_timeout(service: str, account: str, timeout: float = KEYRING_TIMEOUT) -> bool:
    """Call keyring.delete_password with a timeout."""
    kr = _get_keyring()
    if kr is None:
        return False

    success = [False]

    def _delete():
        try:
            kr.delete_password(service, account)
            success[0] = True
        except Exception:
            pass

    thread = threading.Thread(target=_delete, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    return success[0] and not thread.is_alive()


class BrowserAuth:
    """Session cookie-based authentication with automatic JWT token management.

    After user authenticates via Microsoft SSO in browser, Claude extracts
    the session cookies (sessionid, csrftoken). These are used to automatically
    fetch and refresh JWT tokens as needed.

    Multi-Account Support:
    - Pass env parameter to authenticate to specific environment
    - Credentials stored separately per environment in keyring
    - Can maintain sessions for multiple environments simultaneously

    Token lifecycle:
    1. Session cookies (persistent) -> fetch new token pair from /jwt/api/token/
    2. Access token (5 min) -> use for API calls
    3. When access expires -> refresh via /jwt/api/token/refresh/
    4. When refresh expires -> re-fetch using session cookies
    """

    SERVICE_NAME = KEYRING_SERVICE

    # Token refresh buffer - refresh 30 seconds before expiry
    REFRESH_BUFFER_SECONDS = 30

    def __init__(self, env: str | None = None):
        self.env = env or os.environ.get("DATARAILS_ENV") or get_active_environment()
        self.base_url = self._get_base_url()
        self.auth_url = self._get_auth_url()

        # Session cookies (persistent)
        self._session_id: str | None = None
        self._csrf_token: str | None = None

        # JWT tokens (short-lived, auto-refreshed)
        self._access_token: str | None = None
        self._refresh_token: str | None = None
        self._access_exp: float = 0
        self._refresh_exp: float = 0

        self._load_session()

    @property
    def keyring_account(self) -> str:
        """Get keyring account for this environment."""
        return get_keyring_account(self.env)

    def _get_base_url(self) -> str:
        """Get the base URL for the Datarails API based on environment."""
        environments = get_environments()
        env_config = environments.get(self.env, environments.get(DEFAULT_ENV, {}))
        return env_config.get("base_url", f"https://{self.env}.datarails.com")

    def _get_auth_url(self) -> str:
        """Get the auth URL for browser login."""
        environments = get_environments()
        env_config = environments.get(self.env, environments.get(DEFAULT_ENV, {}))
        return env_config.get("auth_url", f"https://{self.env}-auth.datarails.com")

    def _load_session(self) -> None:
        """Load session cookies from system keychain or fallback file."""
        # Try keyring first (uses per-environment account, with timeout)
        stored = _keyring_get_with_timeout(self.SERVICE_NAME, self.keyring_account)
        if stored:
            try:
                data = json.loads(stored)
                self._session_id = data.get("session_id")
                self._csrf_token = data.get("csrf_token")
                if self._session_id and self._csrf_token:
                    return  # Successfully loaded from keyring
            except (json.JSONDecodeError, TypeError):
                pass

        # Fallback: check file (written by Chrome extension native host)
        try:
            if FALLBACK_AUTH_FILE.exists():
                data = json.loads(FALLBACK_AUTH_FILE.read_text())
                # Check if file has credentials for this environment
                env_data = data.get(self.env, data)
                self._session_id = env_data.get("session_id")
                self._csrf_token = env_data.get("csrf_token")
        except Exception:
            pass

    def _save_session(self) -> None:
        """Save session cookies to system keychain and fallback file."""
        value = json.dumps({
            "session_id": self._session_id,
            "csrf_token": self._csrf_token,
            "env": self.env,
            "saved_at": time.time(),
        })
        saved = _keyring_set_with_timeout(self.SERVICE_NAME, self.keyring_account, value)

        # Always also save to fallback file for environments without keyring
        if not saved:
            self._save_to_fallback_file()

    def _save_to_fallback_file(self) -> None:
        """Save session to fallback file."""
        try:
            existing = {}
            if FALLBACK_AUTH_FILE.exists():
                existing = json.loads(FALLBACK_AUTH_FILE.read_text())
            existing[self.env] = {
                "session_id": self._session_id,
                "csrf_token": self._csrf_token,
                "saved_at": time.time(),
            }
            FALLBACK_AUTH_FILE.write_text(json.dumps(existing, indent=2))
        except Exception:
            pass

    def set_session_cookies(self, session_id: str, csrf_token: str) -> None:
        """Set session cookies (called by Claude after browser extraction)."""
        self._session_id = session_id
        self._csrf_token = csrf_token
        # Clear any cached JWT tokens to force refresh
        self._access_token = None
        self._refresh_token = None
        self._save_session()

    def clear_session(self) -> None:
        """Clear stored session and tokens (for logout)."""
        _keyring_delete_with_timeout(self.SERVICE_NAME, self.keyring_account)
        # Also clear fallback file
        try:
            if FALLBACK_AUTH_FILE.exists():
                data = json.loads(FALLBACK_AUTH_FILE.read_text())
                data.pop(self.env, None)
                FALLBACK_AUTH_FILE.write_text(json.dumps(data, indent=2))
        except Exception:
            pass
        self._session_id = None
        self._csrf_token = None
        self._access_token = None
        self._refresh_token = None

    # Aliases for backward compatibility
    def clear_tokens(self) -> None:
        self.clear_session()

    def clear_cookies(self) -> None:
        self.clear_session()

    def _decode_jwt_exp(self, token: str) -> float:
        """Extract expiration timestamp from JWT without verification."""
        parts = token.split('.')
        if len(parts) != 3:
            return 0

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        try:
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            return float(data.get('exp', 0))
        except Exception:
            return 0

    def _needs_refresh(self) -> bool:
        """Check if access token needs refresh."""
        if not self._access_token:
            return True
        return time.time() > (self._access_exp - self.REFRESH_BUFFER_SECONDS)

    def _refresh_token_valid(self) -> bool:
        """Check if refresh token is still valid."""
        if not self._refresh_token:
            return False
        return time.time() < (self._refresh_exp - self.REFRESH_BUFFER_SECONDS)

    async def _fetch_token_pair(self) -> bool:
        """Fetch new token pair using session cookies."""
        if not self._session_id or not self._csrf_token:
            return False

        url = f"{self.base_url}/jwt/api/token/"
        headers = {
            "Cookie": f"csrftoken={self._csrf_token}; sessionid={self._session_id}",
            "X-CSRFToken": self._csrf_token,
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    self._access_token = data['access']
                    self._refresh_token = data['refresh']
                    self._access_exp = self._decode_jwt_exp(self._access_token)
                    self._refresh_exp = self._decode_jwt_exp(self._refresh_token)
                    return True
        except Exception:
            pass

        return False

    async def _refresh_access_token(self) -> bool:
        """Refresh access token using refresh token."""
        if not self._refresh_token:
            return False

        url = f"{self.base_url}/jwt/api/token/refresh/"
        headers = {
            "Cookie": f"csrftoken={self._csrf_token}; sessionid={self._session_id}",
            "X-CSRFToken": self._csrf_token,
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    url,
                    headers=headers,
                    json={"refresh": self._refresh_token}
                )
                if response.status_code == 200:
                    data = response.json()
                    self._access_token = data['access']
                    self._access_exp = self._decode_jwt_exp(self._access_token)
                    return True
        except Exception:
            pass

        return False

    async def ensure_valid_token(self) -> bool:
        """Ensure we have a valid access token, refreshing if needed."""
        if not self._needs_refresh():
            return True

        # Try refresh first if we have a valid refresh token
        if self._refresh_token_valid():
            if await self._refresh_access_token():
                return True

        # Fetch new token pair using session cookies
        return await self._fetch_token_pair()

    def get_headers(self) -> dict[str, str]:
        """Return headers for API requests (uses cached token)."""
        headers = {"Content-Type": "application/json"}

        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"

        if self._csrf_token:
            headers["X-CSRFToken"] = self._csrf_token

        return headers

    def has_session(self) -> bool:
        """Check if we have session cookies."""
        return bool(self._session_id and self._csrf_token)

    def is_authenticated(self) -> bool:
        """Check if we have session cookies (tokens will be auto-fetched)."""
        return self.has_session()

    def get_login_url(self) -> str:
        """Get the URL where user should authenticate."""
        return self.auth_url

    def get_session_extraction_js(self) -> str:
        """Return JavaScript code to extract session cookies from the browser."""
        return """
(function() {
    const result = {
        session_id: null,
        csrf_token: null
    };

    document.cookie.split(';').forEach(function(cookie) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'sessionid') {
            result.session_id = value;
        } else if (name === 'csrftoken') {
            result.csrf_token = value;
        }
    });

    return JSON.stringify(result);
})();
"""

    # Alias for backward compatibility
    def get_token_extraction_js(self) -> str:
        return self.get_session_extraction_js()

    def get_cookie_extraction_js(self) -> str:
        return self.get_session_extraction_js()

    def needs_auth_response(self) -> dict[str, Any]:
        """Return a structured response indicating auth is needed."""
        environments = get_environments()
        env_config = environments.get(self.env, {})
        display_name = env_config.get("display_name", self.env)

        return {
            "error": "authentication_required",
            "message": f"Please authenticate with Datarails ({display_name}) to continue.",
            "environment": self.env,
            "login_url": self.get_login_url(),
            "instructions": [
                f"1. Open {self.get_login_url()} in browser",
                "2. Sign in with Microsoft SSO",
                "3. After login, you'll be redirected to the Datarails app",
                "4. I'll extract the session cookies (sessionid, csrftoken) automatically",
                "5. These cookies are persistent - you won't need to re-authenticate frequently",
            ],
            "extraction_js": self.get_session_extraction_js(),
        }

    @property
    def token_info(self) -> dict[str, Any]:
        """Get info about current tokens (for debugging)."""
        now = time.time()
        return {
            "environment": self.env,
            "has_session": self.has_session(),
            "has_access_token": bool(self._access_token),
            "access_expires_in": max(0, self._access_exp - now) if self._access_token else 0,
            "refresh_expires_in": max(0, self._refresh_exp - now) if self._refresh_token else 0,
            "needs_refresh": self._needs_refresh(),
        }


class EnvAuth:
    """Environment variable-based authentication for CI/testing.

    Set these environment variables:
    - DATARAILS_SESSION_ID: The sessionid cookie value
    - DATARAILS_CSRF_TOKEN: The csrftoken cookie value
    - DATARAILS_ENV: Environment name (default: "dev")

    For direct JWT token (skips auto-refresh):
    - DATARAILS_JWT_TOKEN: A pre-fetched JWT access token
    """

    # Token refresh buffer
    REFRESH_BUFFER_SECONDS = 30

    def __init__(self, env: str | None = None):
        self.env = env or os.environ.get("DATARAILS_ENV", DEFAULT_ENV)
        self.base_url = self._get_base_url()

        # Session cookies
        self._session_id = os.environ.get("DATARAILS_SESSION_ID")
        self._csrf_token = os.environ.get("DATARAILS_CSRF_TOKEN")

        # Direct JWT token (optional, skips token fetch)
        self._jwt_token = os.environ.get("DATARAILS_JWT_TOKEN")

        # Cached tokens
        self._access_token: str | None = self._jwt_token
        self._refresh_token: str | None = None
        self._access_exp: float = 0
        self._refresh_exp: float = 0

    def _get_base_url(self) -> str:
        """Get the base URL for the Datarails API based on environment."""
        environments = get_environments()
        env_config = environments.get(self.env, environments.get(DEFAULT_ENV, {}))
        return env_config.get("base_url", f"https://{self.env}.datarails.com")

    def _decode_jwt_exp(self, token: str) -> float:
        """Extract expiration timestamp from JWT."""
        parts = token.split('.')
        if len(parts) != 3:
            return 0

        payload = parts[1]
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += '=' * padding

        try:
            decoded = base64.urlsafe_b64decode(payload)
            data = json.loads(decoded)
            return float(data.get('exp', 0))
        except Exception:
            return 0

    def _needs_refresh(self) -> bool:
        """Check if access token needs refresh."""
        if not self._access_token:
            return True
        if self._access_exp == 0:
            # If we have a token but no exp, decode it
            self._access_exp = self._decode_jwt_exp(self._access_token)
        return time.time() > (self._access_exp - self.REFRESH_BUFFER_SECONDS)

    async def _fetch_token_pair(self) -> bool:
        """Fetch new token pair using session cookies."""
        if not self._session_id or not self._csrf_token:
            return False

        url = f"{self.base_url}/jwt/api/token/"
        headers = {
            "Cookie": f"csrftoken={self._csrf_token}; sessionid={self._session_id}",
            "X-CSRFToken": self._csrf_token,
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    self._access_token = data['access']
                    self._refresh_token = data['refresh']
                    self._access_exp = self._decode_jwt_exp(self._access_token)
                    self._refresh_exp = self._decode_jwt_exp(self._refresh_token)
                    return True
        except Exception:
            pass

        return False

    async def ensure_valid_token(self) -> bool:
        """Ensure we have a valid access token."""
        if not self._needs_refresh():
            return True

        # If we have session cookies, fetch new tokens
        if self._session_id and self._csrf_token:
            return await self._fetch_token_pair()

        return False

    def get_headers(self) -> dict[str, str]:
        """Return headers for API requests."""
        headers = {"Content-Type": "application/json"}

        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"

        if self._csrf_token:
            headers["X-CSRFToken"] = self._csrf_token

        return headers

    def is_configured(self) -> bool:
        """Check if environment auth is configured."""
        # Either have session cookies OR a direct JWT token
        return bool(self._session_id and self._csrf_token) or bool(self._jwt_token)

    def is_authenticated(self) -> bool:
        """Alias for is_configured."""
        return self.is_configured()


def get_auth(env: str | None = None) -> BrowserAuth | EnvAuth:
    """Get the appropriate auth handler based on configuration.

    Args:
        env: Optional environment name. If not specified, uses active environment.

    Priority:
    1. Environment variables (if DATARAILS_SESSION_ID or DATARAILS_JWT_TOKEN is set)
    2. Browser-extracted session cookies (stored in keyring per environment)
    """
    # Determine environment
    target_env = env or os.environ.get("DATARAILS_ENV") or get_active_environment()

    # Check for env var auth first
    env_auth = EnvAuth(target_env)
    if env_auth.is_configured():
        return env_auth

    return BrowserAuth(target_env)


def get_authenticated_environments() -> list[dict[str, Any]]:
    """Get list of all environments with their authentication status.

    Returns list of dicts with:
    - name: Environment name
    - display_name: Human-readable name
    - authenticated: Whether credentials are stored
    - is_active: Whether this is the active environment
    """
    environments = get_environments()
    active_env = get_active_environment()
    result = []

    for env_name, env_config in environments.items():
        # Check if we have stored credentials for this environment
        auth = BrowserAuth(env_name)
        authenticated = auth.has_session()

        result.append({
            "name": env_name,
            "display_name": env_config.get("display_name", env_name),
            "base_url": env_config.get("base_url"),
            "authenticated": authenticated,
            "is_active": env_name == active_env,
        })

    return result


def set_session_cookies(session_id: str, csrf_token: str, env: str | None = None) -> None:
    """Convenience function to set session cookies.

    Called by Claude after extracting cookies from browser.

    Args:
        session_id: The sessionid cookie value
        csrf_token: The csrftoken cookie value
        env: Optional environment name (defaults to active environment)
    """
    target_env = env or get_active_environment()
    auth = BrowserAuth(target_env)
    auth.set_session_cookies(session_id, csrf_token)


def clear_auth(env: str | None = None) -> None:
    """Clear authentication for an environment.

    Args:
        env: Environment to clear. If None, clears active environment.
    """
    target_env = env or get_active_environment()
    auth = BrowserAuth(target_env)
    auth.clear_session()


def clear_all_auth() -> None:
    """Clear authentication for all environments."""
    environments = get_environments()
    for env_name in environments:
        auth = BrowserAuth(env_name)
        auth.clear_session()


# Aliases for backward compatibility
def set_browser_tokens(jwt_token: str, csrf_token: str | None = None) -> None:
    """Legacy function - session cookies are now preferred."""
    # If only JWT provided, we can't do much without session cookies
    pass


def set_browser_cookies(
    access_token: str,
    refresh_token: str | None = None,
    csrf_token: str | None = None,
    session_id: str | None = None,
) -> None:
    """Legacy function - use set_session_cookies instead."""
    if session_id and csrf_token:
        set_session_cookies(session_id, csrf_token)
