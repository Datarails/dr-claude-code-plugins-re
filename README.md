# Datarails Finance OS Plugin for Claude Code

Analyze financial data, detect anomalies, and query Finance OS tables directly from Claude Code.

## Features

- **Multi-Account Support** - Connect to dev, demo, testapp, and production environments
- **Easy Authentication** - Browser cookie extraction for seamless login
- **Table Discovery** - List and explore all Finance OS tables
- **Data Profiling** - Numeric and categorical field analysis
- **Anomaly Detection** - Automated data quality checks
- **Data Queries** - Filter, sample, and query records

## Quick Start

**Option 1: Setup Wizard (Recommended)**

```bash
# 1. Clone the plugin
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re

# 2. Run the setup wizard
python setup.py
```

The wizard will guide you through prerequisites, authentication, and testing.

**Option 2: Manual Setup**

```bash
# 1. Clone the plugin
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re

# 2. Authenticate (be logged into Datarails in browser first)
cd mcp-server && uv run datarails-mcp auth && cd ..

# 3. Start Claude Code
claude

# 4. Test
/dr-tables
```

Skills are pre-configured - no additional setup needed!

## Skills

| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-learn` | Discover table structure and create client profile |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile field statistics |
| `/dr-anomalies` | Detect data quality issues |
| `/dr-query` | Query and filter records |
| `/dr-extract` | Extract financial data to Excel |

### /dr-auth

Authenticate with Datarails Finance OS. Supports multiple environments.

```
/dr-auth                    # Authenticate to active environment
/dr-auth --env app          # Authenticate to production
/dr-auth --list             # List all environments & auth status
/dr-auth --switch app       # Switch active environment
/dr-auth --logout dev       # Clear credentials for dev
```

### /dr-tables

Discover and explore Finance OS tables.

```
/dr-tables                          # List all tables
/dr-tables 11442                    # Show table schema
/dr-tables 11442 --field account    # Show distinct values
/dr-tables --env app                # List tables in production
```

### /dr-profile

Profile table fields for statistics and patterns.

```
/dr-profile 11442                   # Full profile
/dr-profile 11442 --numeric         # Numeric fields only
/dr-profile 11442 --categorical     # Categorical fields only
/dr-profile 11442 --field amount    # Specific field
```

### /dr-anomalies

Automated anomaly detection.

```
/dr-anomalies 11442                      # Full scan
/dr-anomalies 11442 --severity critical  # Critical only
/dr-anomalies 11442 --type outliers      # Specific type
```

### /dr-query

Query table records with filters.

```
/dr-query 11442 --sample                          # Random sample
/dr-query 11442 amount > 100000                   # Filter records
/dr-query 11442 department = "Sales" --limit 50   # With limit
```

### /dr-learn

Discover table structure and create a client profile. Run this once per environment to enable `/dr-extract`.

```
/dr-learn                   # Discover tables in active environment
/dr-learn --env app         # Discover in production
/dr-learn --force           # Overwrite existing profile
```

Creates a profile at `config/client-profiles/<env>.json` with:
- Table IDs and field mappings
- Account hierarchy names
- KPI definitions
- Any discovered business rules or data notes

### /dr-extract

Extract validated financial data to Excel workbooks.

```
/dr-extract --year 2025                    # Extract current year
/dr-extract --year 2025 --env app          # From production
/dr-extract --year 2025 --scenario Budget  # Budget data
/dr-extract --year 2025 --output report.xlsx
```

Requires a client profile (run `/dr-learn` first). Generates Excel with:
- P&L by month
- KPIs by quarter
- Validation checks

## Multi-Environment Support

The plugin supports simultaneous authentication to multiple Datarails environments:

| Environment | URL | Description |
|-------------|-----|-------------|
| `dev` | dev.datarails.com | Development (default) |
| `demo` | demo.datarails.com | Demo |
| `testapp` | testapp.datarails.com | Test App |
| `app` | app.datarails.com | Production |

### Authenticate to Multiple Environments

```bash
cd mcp-server
uv run datarails-mcp auth --env dev
uv run datarails-mcp auth --env app
uv run datarails-mcp auth --list
```

### Query Different Environments

```
/dr-tables --env app               # Production tables
/dr-profile 11442 --env dev        # Profile in dev
/dr-query 11442 --sample --env app # Sample from production
```

### Add Custom Environments

Edit `config/environments.json`:

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

## Plugin Structure

```
dr-claude-code-plugins/
├── .claude/
│   └── skills/                  # Skill symlinks
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── skills/
│   ├── auth/SKILL.md            # /dr-auth
│   ├── learn/SKILL.md           # /dr-learn
│   ├── tables/SKILL.md          # /dr-tables
│   ├── profile/SKILL.md         # /dr-profile
│   ├── anomalies/SKILL.md       # /dr-anomalies
│   ├── query/SKILL.md           # /dr-query
│   └── extract/SKILL.md         # /dr-extract
├── mcp-server/                  # Bundled MCP server
│   ├── src/datarails_mcp/
│   ├── scripts/                 # Extraction scripts
│   └── pyproject.toml
├── config/
│   ├── environments.json        # Configurable environments
│   ├── profile-schema.json      # Client profile schema
│   └── client-profiles/         # Client-specific configs (not committed)
├── .mcp.json                    # MCP server config
├── CLAUDE.md                    # Claude Code instructions
├── SETUP.md                     # Detailed setup guide
└── README.md                    # This file
```

## Data Limits

The plugin enforces sensible limits to prevent data overload:

| Operation | Max Rows |
|-----------|----------|
| Sample records | 20 |
| Filtered query | 500 |
| Custom query | 1,000 |

For larger datasets, use the profiling tools which work via aggregation.

## Troubleshooting

See [SETUP.md](SETUP.md#troubleshooting-authentication) for detailed troubleshooting.

### Quick Fixes

| Problem | Solution |
|---------|----------|
| Skills not showing | Run `mkdir -p .claude && ln -s ../skills .claude/skills` |
| "Not authenticated" | Run `cd mcp-server && uv run datarails-mcp auth` |
| "Session expired" | Re-authenticate with `datarails-mcp auth` |
| Wrong environment | Use `--env` flag or `datarails-mcp auth --switch <env>` |

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins/issues
- Datarails Support: support@datarails.com
