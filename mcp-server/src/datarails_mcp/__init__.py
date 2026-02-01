"""Datarails Finance OS MCP Server for Claude.

A Model Context Protocol (MCP) server that provides Claude with access
to Datarails Finance OS data for analysis and insights.

Installation (for plugin development):
    cd mcp-server && pip install -e ".[dev]"

Quick Start:
    datarails-mcp auth           # Authenticate with Datarails
    datarails-mcp auth --list    # List all environments
    datarails-mcp status         # Check authentication status
    datarails-mcp serve          # Run the MCP server

Multi-Account Support:
    datarails-mcp auth --env app      # Authenticate to production
    datarails-mcp auth --switch app   # Switch active environment
    datarails-mcp auth --logout dev   # Clear dev credentials

For more information, see: https://github.com/Datarails/dr-claude-code-plugins
"""

__version__ = "0.2.0"

from datarails_mcp.auth import (
    BrowserAuth,
    EnvAuth,
    clear_all_auth,
    clear_auth,
    get_auth,
    get_authenticated_environments,
    set_session_cookies,
)
from datarails_mcp.client import DatarailsClient
from datarails_mcp.constants import (
    get_active_environment,
    get_environment_names,
    get_environments,
    set_active_environment,
)

__all__ = [
    # Auth
    "BrowserAuth",
    "EnvAuth",
    "DatarailsClient",
    "get_auth",
    "set_session_cookies",
    "clear_auth",
    "clear_all_auth",
    "get_authenticated_environments",
    # Environments
    "get_environments",
    "get_environment_names",
    "get_active_environment",
    "set_active_environment",
]
