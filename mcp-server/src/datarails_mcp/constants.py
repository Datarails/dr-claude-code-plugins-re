"""Constants for Datarails Finance OS MCP Server.

Centralized configuration for URLs, paths, and defaults.
Supports loading custom environments from config file.
"""

import json
import os
from pathlib import Path
from typing import Any


# Default environment configurations (fallback if no config file)
DEFAULT_ENVIRONMENTS = {
    "dev": {
        "base_url": "https://dev.datarails.com",
        "auth_url": "https://dev-auth.datarails.com",
        "display_name": "Development",
    },
    "demo": {
        "base_url": "https://demo.datarails.com",
        "auth_url": "https://demo-auth.datarails.com",
        "display_name": "Demo",
    },
    "testapp": {
        "base_url": "https://testapp.datarails.com",
        "auth_url": "https://testapp-auth.datarails.com",
        "display_name": "Test App",
    },
    "app": {
        "base_url": "https://app.datarails.com",
        "auth_url": "https://auth.datarails.com",
        "display_name": "Production",
    },
}

DEFAULT_ENV = "dev"


def _find_config_dir() -> Path | None:
    """Find the config directory.

    Checks in order:
    1. DATARAILS_CONFIG_DIR environment variable
    2. Plugin config directory (relative to this file)
    3. Current working directory /config
    """
    # Check environment variable first
    env_dir = os.environ.get("DATARAILS_CONFIG_DIR")
    if env_dir:
        config_path = Path(env_dir)
        if config_path.exists():
            return config_path

    # Check relative to this file (for bundled plugin)
    # This file is at mcp-server/src/datarails_mcp/constants.py
    # Config is at config/
    this_file = Path(__file__).resolve()
    plugin_root = this_file.parent.parent.parent.parent  # Go up 4 levels
    plugin_config = plugin_root / "config"
    if plugin_config.exists():
        return plugin_config

    # Check current working directory
    cwd_config = Path.cwd() / "config"
    if cwd_config.exists():
        return cwd_config

    return None


def _load_environments_config() -> dict[str, Any]:
    """Load environments from config file if available."""
    config_dir = _find_config_dir()
    if not config_dir:
        return {}

    config_file = config_dir / "environments.json"
    if not config_file.exists():
        return {}

    try:
        with open(config_file) as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def _save_environments_config(config: dict[str, Any]) -> bool:
    """Save environments config to file."""
    config_dir = _find_config_dir()
    if not config_dir:
        return False

    config_file = config_dir / "environments.json"
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
            f.write("\n")
        return True
    except IOError:
        return False


def get_environments() -> dict[str, dict[str, str]]:
    """Get all configured environments."""
    config = _load_environments_config()
    environments = config.get("environments", {})

    # Merge with defaults (config takes precedence)
    result = DEFAULT_ENVIRONMENTS.copy()
    result.update(environments)
    return result


def get_active_environment() -> str:
    """Get the currently active environment."""
    # Check environment variable first
    env_var = os.environ.get("DATARAILS_ENV")
    if env_var:
        return env_var

    # Check config file
    config = _load_environments_config()
    return config.get("active_environment", DEFAULT_ENV)


def set_active_environment(env: str) -> bool:
    """Set the active environment in config file."""
    config = _load_environments_config()
    if not config:
        config = {
            "environments": get_environments(),
            "default_environment": DEFAULT_ENV,
        }

    config["active_environment"] = env
    return _save_environments_config(config)


def get_environment_names() -> list[str]:
    """Get list of all environment names."""
    return list(get_environments().keys())


# Legacy compatibility: ENVIRONMENTS dict
# This is a dynamic property that loads from config
class _EnvironmentsProxy:
    """Proxy to provide dict-like access to environments with config loading."""

    def __getitem__(self, key: str) -> dict[str, str]:
        envs = get_environments()
        if key in envs:
            return envs[key]
        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in get_environments()

    def get(self, key: str, default: dict | None = None) -> dict[str, str] | None:
        return get_environments().get(key, default)

    def keys(self):
        return get_environments().keys()

    def values(self):
        return get_environments().values()

    def items(self):
        return get_environments().items()

    def __iter__(self):
        return iter(get_environments())


ENVIRONMENTS = _EnvironmentsProxy()

# Auth constants
AUTH_TIMEOUT_SECONDS = 300  # 5 minutes to complete login
AUTH_CALLBACK_PATH = "/callback"
LOCAL_AUTH_HOST = "127.0.0.1"

# Keyring service name
KEYRING_SERVICE = "datarails-mcp"


def get_keyring_account(env: str) -> str:
    """Get keyring account name for an environment.

    Enables per-environment credential storage.
    """
    return f"session_{env}"


# Legacy compatibility
KEYRING_ACCOUNT = get_keyring_account(DEFAULT_ENV)

# CLI colors (for rich output)
COLORS = {
    "success": "green",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "dim": "dim",
}
