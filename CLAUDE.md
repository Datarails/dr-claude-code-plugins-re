# CLAUDE.md - Datarails Finance OS Plugin

## Output Files

Generated output files (Excel exports, reports, documentation, etc.) should be saved to the `tmp/` folder in the project root. This keeps generated artifacts separate from code and configuration files.

```bash
# Example output locations
tmp/Financial_Extract_20260203.xlsx
tmp/budget_report.xlsx
tmp/analysis_output.csv
```

## Git Commit Guidelines

**DO commit** (general plugin changes):
- Skill definitions (`skills/*/SKILL.md`)
- MCP server code (`mcp-server/src/`, `mcp-server/scripts/`)
- Plugin configuration (`.claude-plugin/plugin.json`)
- Schema files (`config/profile-schema.json`, `config/environments.json`)
- Documentation (`CLAUDE.md`, `README.md`)

**DO NOT commit** (client-specific data):
- Client profiles (`config/client-profiles/*.json`) - contain client-specific table IDs, field mappings, and discovered knowledge
- Output files (`tmp/`) - extraction results
- Authentication credentials (stored in system keyring, not in files)

## Client Knowledge Base

Client profiles (`config/client-profiles/<env>.json`) serve as a **knowledge base** for each Datarails environment. They store not just table mappings, but any client-specific information discovered during agent work.

### What to Store in Client Profiles

- **Table mappings** - discovered by `/dr-learn`
- **Field mappings** - column names, data types, relationships
- **Business logic** - how the client calculates certain metrics, fiscal year definitions
- **Data quirks** - known issues, missing data periods, naming inconsistencies
- **Custom KPIs** - client-specific metric definitions
- **Preferred formats** - report layouts, naming conventions
- **Notes** - anything useful for future analysis

### Adding Knowledge During Agent Work

When you discover new information about a client's data during analysis, **add it to the client profile**. Use the `notes` section for freeform knowledge:

```json
{
  "tables": { ... },
  "field_mappings": { ... },
  "notes": {
    "fiscal_year": "Starts in February, not January",
    "revenue_recognition": "Q4 includes annual true-ups that inflate numbers",
    "data_gaps": "Missing March 2024 data due to system migration",
    "naming": "Department 'R&D' is sometimes labeled 'Product' in older data"
  }
}
```

This knowledge persists across sessions and helps the agent provide better, more context-aware analysis.

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

### 2. Learn Your Data Structure (First Time)

```bash
# Discover tables and create a client profile
/dr-learn

# Or for a specific environment
/dr-learn --env app
```

This creates a profile at `config/client-profiles/<env>.json` that maps your specific table IDs and field names.

### 3. Explore Data

```
/dr-tables                    # List all tables
/dr-tables 11442              # View table schema
/dr-profile 11442             # Profile table statistics
/dr-anomalies 11442           # Detect data quality issues
/dr-query 11442 --sample      # Get sample records
```

### 4. Extract Financial Data

```bash
# Extract data using your client profile
/dr-extract --year 2025

# Specify environment
/dr-extract --year 2025 --env app
```

## Client Profile System

Different clients have different table structures, field names, and account hierarchies. The plugin uses **client profiles** to adapt to each environment.

### How It Works

1. **First-time setup**: Run `/dr-learn` to discover your table structure
2. **Profile saved**: Creates `config/client-profiles/<env>.json`
3. **Subsequent extractions**: `/dr-extract` reads the profile automatically

### Profile Location

```
config/client-profiles/
├── app.json      # Production profile
├── dev.json      # Development profile
└── demo.json     # Demo profile
```

### Profile Contents

Each profile contains:
- **Table IDs**: Which tables contain financials and KPIs
- **Field mappings**: Amount, Date, Account, Scenario field names
- **Account hierarchy**: Revenue, COGS, OpEx category names
- **KPI definitions**: KPI name mappings

### Manual Profile Editing

You can edit profiles directly:

```json
{
  "tables": {
    "financials": { "id": "TABLE_ID", "name": "Financials Cube" },
    "kpis": { "id": "34298", "name": "KPI Metrics" }
  },
  "field_mappings": {
    "amount": "Amount",
    "account_l1": "DR_ACC_L1"
  },
  "account_hierarchy": {
    "revenue": "REVENUE",
    "cogs": "Cost of Good sold"
  }
}
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
/dr-learn --env app                # Create profile for production
/dr-extract --year 2025 --env app  # Extract from production
```

## Available Skills

| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-learn` | Discover table structure and create client profile |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile table statistics |
| `/dr-anomalies` | Detect data anomalies |
| `/dr-query` | Query table data |
| `/dr-extract` | Extract validated financial data to Excel |

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

After adding a custom environment:
1. `/dr-auth --env custom-client` to authenticate
2. `/dr-learn --env custom-client` to discover tables
3. `/dr-extract --env custom-client --year 2025` to extract

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

### "No profile found" error
1. Run `/dr-learn --env <env>` to create a profile
2. Or copy an existing profile and modify it

### Extraction returns wrong data
1. Check profile at `config/client-profiles/<env>.json`
2. Verify table IDs match your environment
3. Re-run `/dr-learn` to rediscover structure

## Plugin Structure

```
dr-claude-code-plugins/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   ├── auth/SKILL.md        # /dr-auth
│   ├── learn/SKILL.md       # /dr-learn (NEW)
│   ├── tables/SKILL.md      # /dr-tables
│   ├── profile/SKILL.md     # /dr-profile
│   ├── anomalies/SKILL.md   # /dr-anomalies
│   ├── query/SKILL.md       # /dr-query
│   └── extract/SKILL.md     # /dr-extract
├── mcp-server/              # Bundled MCP server
│   ├── src/datarails_mcp/
│   ├── scripts/
│   │   └── extract_financials.py  # Profile-aware extraction
│   └── pyproject.toml
├── config/
│   ├── environments.json    # Configurable environments
│   ├── profile-schema.json  # JSON schema for profiles
│   └── client-profiles/     # Client-specific configs
│       └── app.json         # Default production profile
├── agents/
│   └── finance-analyst.md
└── CLAUDE.md                # This file
```
