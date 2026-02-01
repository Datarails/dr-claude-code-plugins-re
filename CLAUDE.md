# CLAUDE.md - Datarails Finance OS Plugin

## Overview

This Claude Code plugin provides integration with Datarails Finance OS for financial data analysis, anomaly detection, and table querying. It includes a bundled MCP server and supports multi-account authentication.

## Quick Start

### 1. Authenticate

```bash
# Be logged into Datarails in your browser first, then:
/dr-auth

# Or authenticate to specific environment
/dr-auth --env app
```

### 2. Explore Data

```
/dr-tables                    # List all tables
/dr-tables 11442              # View table schema
/dr-profile 11442             # Profile table statistics
/dr-anomalies 11442           # Detect data quality issues
/dr-query 11442 --sample      # Get sample records
```

## Multi-Account Support

This plugin supports simultaneous authentication to multiple Datarails environments.

### Available Environments

| Name | Display | URL |
|------|---------|-----|
| `dev` | Development | dev.datarails.com |
| `demo` | Demo | demo.datarails.com |
| `testapp` | Test App | testapp.datarails.com |
| `app` | Production | app.datarails.com |

### Managing Accounts

```bash
# List all environments and their auth status
/dr-auth --list

# Authenticate to specific environment
/dr-auth --env app
/dr-auth --env dev

# Switch active environment (uses stored credentials)
/dr-auth --switch app

# Logout from specific environment
/dr-auth --logout dev

# Logout from all environments
/dr-auth --logout-all
```

### Using --env Flag

All skills support the `--env` flag to query a specific environment:

```
/dr-tables --env app               # List tables in production
/dr-profile 11442 --env dev        # Profile in development
/dr-query 11442 --sample --env app # Sample from production
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile table statistics |
| `/dr-anomalies` | Detect data anomalies |
| `/dr-query` | Query table data |

## Adding Custom Environments

Edit `config/environments.json` to add custom environments:

```json
{
  "environments": {
    "custom-client": {
      "base_url": "https://custom-client.datarails.com",
      "auth_url": "https://custom-client-auth.datarails.com",
      "display_name": "Custom Client"
    }
  }
}
```

## MCP Server

The MCP server is bundled in `mcp-server/` and runs automatically. For development:

```bash
# Install for development
cd mcp-server && pip install -e ".[dev]"

# Run server directly
datarails-mcp serve

# Check status
datarails-mcp status --all
```

## Authentication Flow

1. **Browser Cookie Extraction**: The CLI reads cookies directly from your browser's local storage
2. **Keyring Storage**: Credentials are securely stored in your system keyring (per environment)
3. **JWT Auto-refresh**: Session cookies are used to automatically fetch/refresh JWT tokens

Supported browsers: Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium

## Troubleshooting

### "Not authenticated" error
1. Make sure you're logged into Datarails in your browser
2. Run `/dr-auth` to extract cookies
3. Check status with `datarails-mcp status`

### Browser cookie extraction fails
1. Try closing the browser first (some browsers lock the cookie database)
2. Use manual entry: `/dr-auth --manual`
3. Grant keychain access if prompted (macOS)

### Wrong environment
1. Check active environment: `/dr-auth --list`
2. Switch with: `/dr-auth --switch <env>`
3. Or specify explicitly: `/dr-tables --env app`

## Plugin Structure

```
dr-claude-code-plugins/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   ├── auth/SKILL.md        # /dr-auth
│   ├── tables/SKILL.md      # /dr-tables
│   ├── profile/SKILL.md     # /dr-profile
│   ├── anomalies/SKILL.md   # /dr-anomalies
│   └── query/SKILL.md       # /dr-query
├── mcp-server/              # Bundled MCP server
│   ├── src/datarails_mcp/
│   └── pyproject.toml
├── config/
│   └── environments.json    # Configurable environments
├── agents/
│   └── finance-analyst.md
└── CLAUDE.md                # This file
```
