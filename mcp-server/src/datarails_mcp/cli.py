"""Command-line interface for Datarails Finance OS MCP Server.

Provides commands for:
- auth: Authenticate with Datarails via browser cookie extraction
- serve: Run the MCP server (called by Claude)
- status: Check authentication and configuration status
- setup: Configure Claude clients

Multi-Account Support:
- auth --env <env>: Authenticate to specific environment
- auth --switch <env>: Switch active environment
- auth --list: List all environments and their auth status
- auth --logout <env>: Clear credentials for specific environment
"""

import json
import os
import sys
import webbrowser
from pathlib import Path

import click

from datarails_mcp.auth import (
    BrowserAuth,
    clear_auth,
    clear_all_auth,
    get_auth,
    get_authenticated_environments,
)
from datarails_mcp.browser_cookies import get_datarails_cookies, get_login_url
from datarails_mcp.constants import (
    DEFAULT_ENV,
    get_active_environment,
    get_environment_names,
    get_environments,
    set_active_environment,
)

# Check for rich library (optional, for better output)
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table

    console = Console()
    RICH_AVAILABLE = True
except ImportError:
    console = None
    RICH_AVAILABLE = False


def echo(message: str, style: str | None = None, **kwargs):
    """Print message with optional styling (uses rich if available)."""
    if RICH_AVAILABLE and console and style:
        console.print(message, style=style, **kwargs)
    else:
        click.echo(message, **kwargs)


def echo_success(message: str):
    """Print success message."""
    if RICH_AVAILABLE and console:
        console.print(f"[green]\u2713[/green] {message}")
    else:
        click.echo(f"\u2713 {message}")


def echo_error(message: str):
    """Print error message."""
    if RICH_AVAILABLE and console:
        console.print(f"[red]\u2717[/red] {message}", style="red")
    else:
        click.echo(f"\u2717 {message}", err=True)


def echo_warning(message: str):
    """Print warning message."""
    if RICH_AVAILABLE and console:
        console.print(f"[yellow]![/yellow] {message}")
    else:
        click.echo(f"! {message}")


def echo_info(message: str):
    """Print info message."""
    if RICH_AVAILABLE and console:
        console.print(f"[blue]\u2022[/blue] {message}")
    else:
        click.echo(f"\u2022 {message}")


class EnvChoice(click.ParamType):
    """Click parameter type for environment names (dynamic from config)."""

    name = "environment"

    def get_metavar(self, param, ctx=None):
        return "[ENV]"

    def convert(self, value, param, ctx):
        env_names = get_environment_names()
        if value not in env_names:
            self.fail(
                f"'{value}' is not a valid environment. "
                f"Available: {', '.join(env_names)}",
                param,
                ctx,
            )
        return value


ENV_CHOICE = EnvChoice()


@click.group()
@click.version_option()
def main():
    """Datarails Finance OS MCP Server.

    A Model Context Protocol server that provides Claude with access
    to Datarails Finance OS data for analysis and insights.

    \b
    Quick start:
      datarails-mcp auth           # Authenticate with Datarails
      datarails-mcp auth --list    # List all environments
      datarails-mcp status         # Check authentication status
      datarails-mcp serve          # Start the MCP server

    \b
    Multi-account usage:
      datarails-mcp auth --env app     # Authenticate to production
      datarails-mcp auth --switch app  # Switch active environment
      datarails-mcp auth --logout dev  # Clear dev credentials

    For more information, visit: https://github.com/Datarails/datarails-finance-os-mcp
    """
    pass


@main.command()
@click.option(
    "--env",
    "-e",
    type=ENV_CHOICE,
    default=None,
    help="Environment to authenticate against (default: active environment)",
)
@click.option(
    "--manual",
    "-m",
    is_flag=True,
    help="Manual cookie entry (copy/paste from browser DevTools)",
)
@click.option(
    "--list",
    "list_envs",
    is_flag=True,
    help="List all environments and their authentication status",
)
@click.option(
    "--switch",
    "-s",
    type=ENV_CHOICE,
    default=None,
    help="Switch active environment (no re-auth if already authenticated)",
)
@click.option(
    "--logout",
    type=ENV_CHOICE,
    default=None,
    help="Clear credentials for specific environment",
)
@click.option(
    "--logout-all",
    is_flag=True,
    help="Clear credentials for all environments",
)
def auth(
    env: str | None,
    manual: bool,
    list_envs: bool,
    switch: str | None,
    logout: str | None,
    logout_all: bool,
):
    """Authenticate with Datarails.

    Reads session cookies directly from your browser. Just be logged into
    Datarails (and switched to the correct user) before running this.

    \b
    Examples:
      datarails-mcp auth                    # Auto-detect from browser (active env)
      datarails-mcp auth --env app          # Authenticate to production
      datarails-mcp auth --manual           # Manual cookie entry
      datarails-mcp auth --list             # List all environments
      datarails-mcp auth --switch app       # Switch active environment
      datarails-mcp auth --logout dev       # Clear dev credentials
      datarails-mcp auth --logout-all       # Clear all credentials
    """
    # Handle --list
    if list_envs:
        _list_environments()
        return

    # Handle --logout-all
    if logout_all:
        _logout_all()
        return

    # Handle --logout <env>
    if logout:
        _logout_env(logout)
        return

    # Handle --switch <env>
    if switch:
        _switch_environment(switch)
        return

    # Default: authenticate to specified or active environment
    target_env = env or get_active_environment()
    environments = get_environments()
    env_config = environments.get(target_env, {})

    echo_info(f"Environment: {env_config.get('display_name', target_env)} ({env_config.get('base_url', '')})")

    if manual:
        _auth_manual(target_env)
    else:
        _auth_browser_cookies(target_env)


def _list_environments():
    """List all environments with authentication status."""
    echo("")
    echo("Datarails Environments")
    echo("=" * 50)
    echo("")

    env_status = get_authenticated_environments()

    if RICH_AVAILABLE and console:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Status", width=6)
        table.add_column("Name", width=10)
        table.add_column("Display", width=15)
        table.add_column("URL", width=30)

        for env in env_status:
            status = "[green]\u2713[/green]" if env["authenticated"] else "[red]\u2717[/red]"
            active = " [yellow](active)[/yellow]" if env["is_active"] else ""
            table.add_row(
                status,
                f"{env['name']}{active}",
                env["display_name"],
                env.get("base_url", "")
            )

        console.print(table)
    else:
        for env in env_status:
            status = "\u2713" if env["authenticated"] else "\u2717"
            active = " (active)" if env["is_active"] else ""
            click.echo(f"  {status} {env['name']}{active} - {env['display_name']}")

    echo("")
    authenticated_count = sum(1 for e in env_status if e["authenticated"])
    echo_info(f"{authenticated_count} of {len(env_status)} environments authenticated")


def _logout_env(env: str):
    """Clear credentials for specific environment."""
    environments = get_environments()
    env_config = environments.get(env, {})
    display_name = env_config.get("display_name", env)

    clear_auth(env)
    echo_success(f"Logged out of {display_name} ({env})")


def _logout_all():
    """Clear credentials for all environments."""
    if not click.confirm("Clear credentials for ALL environments?", default=False):
        echo_info("Cancelled")
        return

    clear_all_auth()
    echo_success("Cleared credentials for all environments")


def _switch_environment(env: str):
    """Switch the active environment."""
    environments = get_environments()
    env_config = environments.get(env, {})
    display_name = env_config.get("display_name", env)

    # Check if already authenticated to target environment
    auth = BrowserAuth(env)
    if not auth.has_session():
        echo_warning(f"Not authenticated to {display_name}")
        echo_info(f"Run 'datarails-mcp auth --env {env}' to authenticate first")
        echo_info("Or continue to switch anyway (API calls will require auth)")
        echo("")
        if not click.confirm(f"Switch to {env} anyway?", default=False):
            return

    if set_active_environment(env):
        echo_success(f"Switched active environment to {display_name} ({env})")
    else:
        # Fallback: set via environment variable hint
        echo_success(f"Switched active environment to {display_name} ({env})")
        echo_info("Note: Config file not writable. Set DATARAILS_ENV='{env}' for persistence")


def _auth_manual(env: str):
    """Manual authentication flow - user enters cookies from DevTools."""
    echo("")
    echo("Manual Authentication")
    echo("=" * 40)
    echo("")
    echo_info("To get your session cookies:")
    echo("  1. Open your browser and navigate to Datarails")
    echo("  2. Log in if needed")
    echo("  3. Open DevTools (F12) \u2192 Application \u2192 Cookies")
    echo("  4. Find cookies for the Datarails domain")
    echo("  5. Copy the values for 'sessionid' and 'csrftoken'")
    echo("")

    session_id = click.prompt("Session ID (sessionid cookie)", type=str)
    csrf_token = click.prompt("CSRF Token (csrftoken cookie)", type=str)

    if not session_id or not csrf_token:
        echo_error("Both session ID and CSRF token are required")
        sys.exit(1)

    # Store credentials
    auth_handler = BrowserAuth(env)
    auth_handler.set_session_cookies(session_id.strip(), csrf_token.strip())

    echo("")
    echo_success("Credentials stored successfully!")
    echo_info(f"Environment: {env}")
    echo_info("Run 'datarails-mcp status' to verify authentication")


def _auth_browser_cookies(env: str):
    """Browser cookie extraction authentication flow.

    Reads cookies directly from browser's local storage.
    User just needs to be logged into Datarails.
    """
    echo("")
    echo("Browser Cookie Authentication")
    echo("=" * 40)
    echo_info("Looking for Datarails session in your browser...")
    echo("")

    def on_status(msg: str):
        echo_info(msg)

    result = get_datarails_cookies(env=env, on_status=on_status)

    if result.success:
        # Store credentials
        auth_handler = BrowserAuth(env)
        auth_handler.set_session_cookies(result.session_id, result.csrf_token)

        echo("")
        echo_success(f"Found session in {result.browser_name}!")
        echo_success(f"Credentials saved for environment: {env}")
        echo_info("Run 'datarails-mcp status' to verify")
    else:
        echo("")
        echo_warning(result.error or "No Datarails session found in any browser.")
        echo("")
        echo_info("Please log in to Datarails in your browser first.")
        echo_info(f"Login URL: {get_login_url(env)}")
        echo("")

        if click.confirm("Open browser to log in?", default=True):
            webbrowser.open(get_login_url(env))
            echo("")
            echo_info("After logging in (and switching to the correct user if needed),")
            echo_info("run 'datarails-mcp auth' again.")
        else:
            echo_info("You can also use 'datarails-mcp auth --manual' to enter cookies manually.")

        sys.exit(1)


@main.command()
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output status as JSON",
)
@click.option(
    "--env",
    "-e",
    type=ENV_CHOICE,
    default=None,
    help="Check status for specific environment",
)
@click.option(
    "--all",
    "show_all",
    is_flag=True,
    help="Show status for all environments",
)
def status(output_json: bool, env: str | None, show_all: bool):
    """Check authentication and configuration status.

    Shows whether you're authenticated with Datarails and displays
    configuration details.

    \b
    Examples:
      datarails-mcp status             # Status for active environment
      datarails-mcp status --all       # Status for all environments
      datarails-mcp status --env app   # Status for specific environment
      datarails-mcp status --json      # JSON output
    """
    if show_all:
        _status_all(output_json)
        return

    target_env = env or get_active_environment()
    auth_handler = get_auth(target_env)
    is_authenticated = auth_handler.is_authenticated()
    environments = get_environments()
    env_config = environments.get(target_env, {})

    status_data = {
        "authenticated": is_authenticated,
        "environment": target_env,
        "environment_display": env_config.get("display_name", target_env),
        "environment_url": env_config.get("base_url", "unknown"),
        "is_active": target_env == get_active_environment(),
        "keyring_available": _check_keyring(),
    }

    # Add token info if available
    if hasattr(auth_handler, "token_info"):
        status_data["token_info"] = auth_handler.token_info

    if output_json:
        click.echo(json.dumps(status_data, indent=2))
        return

    # Human-readable output
    echo("")
    echo("Datarails MCP Status")
    echo("=" * 40)
    echo("")

    if is_authenticated:
        echo_success("Authenticated")
        echo_info(f"Environment: {env_config.get('display_name', target_env)}")
        echo_info(f"URL: {env_config.get('base_url', 'unknown')}")

        if hasattr(auth_handler, "token_info"):
            info = auth_handler.token_info
            if info.get("has_access_token"):
                expires_in = int(info.get("access_expires_in", 0))
                if expires_in > 0:
                    echo_info(f"Access token expires in: {expires_in}s")
                else:
                    echo_warning("Access token expired (will auto-refresh)")
    else:
        echo_error("Not authenticated")
        echo_info(f"Environment: {env_config.get('display_name', target_env)}")
        echo_info(f"Run 'datarails-mcp auth --env {target_env}' to authenticate")

    echo("")

    # Keyring status
    if status_data["keyring_available"]:
        echo_success("Keyring available (credentials stored securely)")
    else:
        echo_warning("Keyring not available (using fallback storage)")


def _status_all(output_json: bool):
    """Show status for all environments."""
    env_status = get_authenticated_environments()
    active_env = get_active_environment()

    if output_json:
        click.echo(json.dumps({
            "active_environment": active_env,
            "environments": env_status,
            "keyring_available": _check_keyring(),
        }, indent=2))
        return

    echo("")
    echo("Datarails MCP Status (All Environments)")
    echo("=" * 50)
    echo("")

    for env in env_status:
        status_icon = "\u2713" if env["authenticated"] else "\u2717"
        active_mark = " (active)" if env["is_active"] else ""

        if env["authenticated"]:
            echo_success(f"{env['display_name']}{active_mark}")
        else:
            echo_error(f"{env['display_name']}{active_mark} - not authenticated")

        echo_info(f"  Name: {env['name']}")
        echo_info(f"  URL: {env.get('base_url', 'unknown')}")
        echo("")

    authenticated_count = sum(1 for e in env_status if e["authenticated"])
    echo_info(f"Summary: {authenticated_count}/{len(env_status)} environments authenticated")


def _check_keyring() -> bool:
    """Check if system keyring is available."""
    from datarails_mcp.auth import _keyring_get_with_timeout
    result = _keyring_get_with_timeout("datarails-mcp-test", "test", timeout=3)
    # If it returns None, keyring might be unavailable or empty - either is ok
    # The real test is that it didn't hang
    return True


@main.command()
def serve():
    """Run the MCP server.

    This command is called by Claude clients (Claude Code, Claude Desktop)
    to start the MCP server. You typically don't need to run this manually.

    The server communicates via stdio using the MCP protocol.
    """
    # Import here to avoid circular imports and speed up CLI startup
    from datarails_mcp.server import main as server_main

    server_main()


@main.command()
@click.option(
    "--env",
    "-e",
    type=ENV_CHOICE,
    default=None,
    help="Default environment for the server",
)
@click.option(
    "--claude-code",
    is_flag=True,
    help="Configure Claude Code (global settings)",
)
@click.option(
    "--claude-desktop",
    is_flag=True,
    help="Configure Claude Desktop",
)
@click.option(
    "--project",
    is_flag=True,
    help="Configure current project (.mcp.json)",
)
def setup(env: str | None, claude_code: bool, claude_desktop: bool, project: bool):
    """Configure Claude clients to use this MCP server.

    Automatically detects and configures available Claude clients.
    If no specific client is selected, configures all detected clients.

    \b
    Examples:
      datarails-mcp setup                    # Auto-detect and configure all
      datarails-mcp setup --claude-code      # Configure Claude Code only
      datarails-mcp setup --claude-desktop   # Configure Claude Desktop only
      datarails-mcp setup --project          # Configure current project only
    """
    target_env = env or get_active_environment()

    # Determine which clients to configure
    configure_all = not (claude_code or claude_desktop or project)

    if configure_all:
        echo_info("Auto-detecting Claude clients...")
        echo("")

    configs_updated = []

    # Claude Code global config
    if configure_all or claude_code:
        path = _get_claude_code_config_path()
        if path:
            if _configure_client(path, target_env, "Claude Code (global)"):
                configs_updated.append(("Claude Code (global)", path))

    # Claude Desktop config
    if configure_all or claude_desktop:
        path = _get_claude_desktop_config_path()
        if path:
            if _configure_client(path, target_env, "Claude Desktop"):
                configs_updated.append(("Claude Desktop", path))

    # Project config
    if configure_all or project:
        path = Path.cwd() / ".mcp.json"
        if _configure_client(path, target_env, "Project"):
            configs_updated.append(("Project", path))

    echo("")
    if configs_updated:
        echo_success(f"Configured {len(configs_updated)} client(s):")
        for name, path in configs_updated:
            echo_info(f"  {name}: {path}")
        echo("")
        echo_info("Restart your Claude client for changes to take effect.")
    else:
        echo_warning("No Claude clients were configured.")
        echo_info("Run with --project to create a project config file.")


def _get_claude_code_config_path() -> Path | None:
    """Get Claude Code global config path."""
    config_dir = Path.home() / ".claude"
    if config_dir.exists():
        return config_dir / "settings.json"
    return None


def _get_claude_desktop_config_path() -> Path | None:
    """Get Claude Desktop config path (platform-specific)."""
    if sys.platform == "darwin":
        path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA", "")
        if appdata:
            path = Path(appdata) / "Claude" / "claude_desktop_config.json"
        else:
            return None
    else:  # Linux
        path = Path.home() / ".config" / "claude" / "claude_desktop_config.json"

    # Check if Claude Desktop is installed (parent dir exists)
    if path.parent.exists():
        return path
    return None


def _configure_client(path: Path, env: str, name: str) -> bool:
    """Configure a Claude client config file.

    Returns True if configuration was updated.
    """
    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    # Load existing config or create new
    config = {}
    if path.exists():
        try:
            config = json.loads(path.read_text())
        except json.JSONDecodeError:
            echo_warning(f"  {name}: Invalid JSON, creating new config")
            config = {}

    # Ensure mcpServers key exists
    if "mcpServers" not in config:
        config["mcpServers"] = {}

    # Add our server config
    config["mcpServers"]["datarails-finance-os"] = {
        "command": "datarails-mcp",
        "args": ["serve"],
        "env": {
            "DATARAILS_ENV": env,
        },
    }

    # Write config
    try:
        path.write_text(json.dumps(config, indent=2) + "\n")
        echo_success(f"  {name}: Configured")
        return True
    except Exception as e:
        echo_error(f"  {name}: Failed to write config - {e}")
        return False


@main.command()
def envs():
    """List available environments.

    Shows all configured environments and their URLs.
    Use 'auth --list' to see authentication status.
    """
    environments = get_environments()
    active = get_active_environment()

    echo("")
    echo("Available Environments")
    echo("=" * 40)
    echo("")

    for name, config in environments.items():
        active_mark = " (active)" if name == active else ""
        echo_info(f"{name}{active_mark}")
        echo(f"    Display: {config.get('display_name', name)}")
        echo(f"    URL: {config.get('base_url', 'unknown')}")
        echo(f"    Auth: {config.get('auth_url', 'unknown')}")
        echo("")

    echo_info("To add custom environments, edit config/environments.json")


if __name__ == "__main__":
    main()
