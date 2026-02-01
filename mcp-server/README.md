# Datarails Finance OS MCP Server

MCP (Model Context Protocol) server for Datarails Finance OS integration with Claude. This is the bundled server included in the `dr-claude-code-plugins` plugin.

## Installation

For development:

```bash
cd mcp-server
pip install -e ".[dev]"
```

The plugin runs the server automatically via `uv`.

## CLI Commands

```bash
# Authenticate (extracts cookies from browser)
datarails-mcp auth

# Authenticate to specific environment
datarails-mcp auth --env app

# List all environments
datarails-mcp auth --list

# Switch active environment
datarails-mcp auth --switch app

# Logout
datarails-mcp auth --logout dev

# Check status
datarails-mcp status
datarails-mcp status --all

# Run server (called by Claude)
datarails-mcp serve

# Show available environments
datarails-mcp envs
```

## Multi-Account Support

Credentials are stored per-environment in the system keyring:
- `session_dev` - Development credentials
- `session_app` - Production credentials
- `session_demo` - Demo credentials
- `session_testapp` - Test App credentials

You can authenticate to multiple environments simultaneously and switch between them without re-authenticating.

## Environment Configuration

Environments are configured in `../config/environments.json`. The server loads this automatically.

Default environments:
- `dev` - Development (dev.datarails.com)
- `demo` - Demo (demo.datarails.com)
- `testapp` - Test App (testapp.datarails.com)
- `app` - Production (app.datarails.com)

## MCP Tools

| Tool | Description |
|------|-------------|
| `check_auth_status` | Check authentication status |
| `set_auth_cookies` | Store session cookies |
| `clear_auth_cookies` | Clear authentication |
| `get_cookie_extraction_script` | Get JS for manual cookie extraction |
| `list_finance_tables` | List available tables |
| `get_table_schema` | Get table columns and types |
| `get_field_distinct_values` | Get unique values for a field |
| `profile_table_summary` | Comprehensive table overview |
| `profile_numeric_fields` | Statistics for numeric fields |
| `profile_categorical_fields` | Cardinality for categorical fields |
| `detect_anomalies` | Automated anomaly detection |
| `get_records_by_filter` | Fetch filtered records (max 500) |
| `get_sample_records` | Get random sample (max 20) |
| `execute_query` | Custom query (max 1000) |

## Development

```bash
# Run tests
pytest

# Run with verbose output
pytest -v

# Type checking
mypy src/
```
