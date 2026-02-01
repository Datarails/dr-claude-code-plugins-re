"""Read Datarails cookies directly from user's browser.

Uses browser_cookie3 to read cookies from browser's local storage (SQLite/binary).
This provides zero-interaction authentication - user just needs to be logged in.

Supported browsers: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium
"""

from dataclasses import dataclass
from typing import Callable

from datarails_mcp.constants import DEFAULT_ENV, get_environments


@dataclass
class BrowserCookieResult:
    """Result of browser cookie extraction."""

    success: bool
    session_id: str | None = None
    csrf_token: str | None = None
    browser_name: str | None = None
    error: str | None = None


def get_datarails_cookies(
    env: str = DEFAULT_ENV,
    on_status: Callable[[str], None] | None = None,
) -> BrowserCookieResult:
    """Extract sessionid and csrftoken from browser.

    Tries browsers in order: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium.
    Returns BrowserCookieResult with session cookies if found.

    Args:
        env: Environment to get cookies for ("dev" or "prod")
        on_status: Optional callback for status updates

    Returns:
        BrowserCookieResult with success status and cookies (or error)
    """
    try:
        import browser_cookie3
    except ImportError:
        return BrowserCookieResult(
            success=False,
            error="browser-cookie3 not installed. Run: pip install browser-cookie3",
        )

    status_fn = on_status or (lambda msg: None)

    # Get domain based on environment
    environments = get_environments()
    env_config = environments.get(env, environments.get(DEFAULT_ENV, {}))
    base_url = env_config.get("base_url", f"https://{env}.datarails.com")
    # Extract domain from URL (e.g., "https://dev.datarails.com" -> "dev.datarails.com")
    domain = base_url.replace("https://", "").replace("http://", "").rstrip("/")

    # List of browsers to try, in order of preference
    browsers = [
        ("Chrome", browser_cookie3.chrome),
        ("Firefox", browser_cookie3.firefox),
        ("Safari", browser_cookie3.safari),
        ("Edge", browser_cookie3.edge),
        ("Brave", browser_cookie3.brave),
        ("Opera", browser_cookie3.opera),
        ("Chromium", browser_cookie3.chromium),
    ]

    errors = []

    for name, loader in browsers:
        try:
            status_fn(f"Checking {name}...")

            # Load cookies for the domain
            # Note: Some browsers may require the browser to be closed
            cj = loader(domain_name=domain)

            session_id = None
            csrf_token = None

            for cookie in cj:
                if cookie.name == "sessionid":
                    session_id = cookie.value
                elif cookie.name == "csrftoken":
                    csrf_token = cookie.value

            if session_id and csrf_token:
                status_fn(f"Found cookies in {name}")
                return BrowserCookieResult(
                    success=True,
                    session_id=session_id,
                    csrf_token=csrf_token,
                    browser_name=name,
                )

        except PermissionError as e:
            # Browser is likely running and has locked the cookie database
            errors.append(f"{name}: Browser may be locked - try closing it ({e})")
        except FileNotFoundError:
            # Browser not installed or profile not found
            pass
        except Exception as e:
            # Other errors (e.g., decryption issues on some platforms)
            error_msg = str(e)
            if "decrypt" in error_msg.lower():
                errors.append(f"{name}: Cookie decryption failed - may need keychain access")
            elif len(error_msg) < 100:  # Only include short errors
                errors.append(f"{name}: {error_msg}")

    # No cookies found in any browser
    if errors:
        error_detail = "; ".join(errors[:3])  # Limit to first 3 errors
        return BrowserCookieResult(
            success=False,
            error=f"No Datarails session found. Issues: {error_detail}",
        )

    return BrowserCookieResult(
        success=False,
        error=f"No Datarails session found for {domain}. Please log in first.",
    )


def get_login_url(env: str = DEFAULT_ENV) -> str:
    """Get the login URL for the given environment."""
    environments = get_environments()
    env_config = environments.get(env, environments.get(DEFAULT_ENV, {}))
    return env_config.get("auth_url", f"https://{env}-auth.datarails.com")
