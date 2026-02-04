# CLAUDE.md - Datarails Finance OS Plugin
**Guidelines for agents and developers working with this plugin.**

---

## 🚨 CRITICAL PRINCIPLE: ALWAYS USE FRESH REAL DATA

**NEVER generate reports, Excel files, or any artifacts without first fetching fresh data from the live Datarails API.**

### Why This Matters
Reports with fake/placeholder data have ZERO value and mislead stakeholders. Every agent must:
1. Connect to the live environment (verify authentication)
2. Fetch fresh data from Datarails tables
3. Analyze the real data
4. Generate reports based on that analysis

### How to Verify
Before creating any artifact:
```python
# Always start with fresh API calls
records = await client.get_sample(table_id, n=50)
print(f"✓ Got {len(records)} real records")

# Never use placeholder data
assert len(records) > 0, "No data to analyze!"

# Generate report from actual analysis
total = sum([r.get("Amount", 0) for r in records])
excel.add_data([["Total", total]])  # Real number, not made up
```

---

## Project Structure

```
datarails-plugin/
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
├── SETUP.md                     # Setup instructions
│
├── skills/                      # Skill definitions
│   ├── dr-auth/
│   ├── dr-learn/
│   ├── dr-extract/
│   └── ... (other skills)
│
├── mcp-server/                  # Bundled MCP server
│   ├── src/datarails_mcp/       # Core MCP implementation
│   ├── scripts/                 # Utility scripts
│   └── pyproject.toml
│
├── config/
│   ├── environments.json        # Available Datarails environments
│   ├── profile-schema.json      # Client profile JSON schema
│   └── client-profiles/         # 🔒 CLIENT-SPECIFIC DATA (not committed)
│       ├── app.json             # Production profile
│       ├── dev.json             # Development profile
│       └── .gitkeep
│
├── docs/
│   ├── analysis/                # System analysis & strategy
│   │   ├── TABLE_STRUCTURE_ANALYSIS.md
│   │   ├── DATA_EXTRACTION_STRATEGY.md
│   │   └── API_DIAGNOSTIC_REPORT.md
│   ├── guides/                  # Operational documentation
│   │   ├── NOTEBOOK_GUIDE.md
│   │   ├── DYNAMIC_JWT_GUIDE.md
│   │   └── ...
│   └── notebooks/               # Jupyter notebooks
│       └── DATARAILS_API_EXPLORER.ipynb
│
├── tmp/                         # Generated outputs (not committed)
│   └── .gitkeep
│
└── .gitignore                   # Excludes client profiles & tmp/
```

---

## Documentation Organization

### System Analysis & Strategy (Versioned)
**Location:** `docs/analysis/`

These files document how systems work and are versioned with the project:
- `*_ANALYSIS.md` - Technical analysis and findings
- `*_STRATEGY.md` - Implementation strategies and architectures
- `*_REPORT.md` - Investigation reports and discoveries

**Purpose:** Help future agents understand system architecture and optimization opportunities.

### Operational Guides (Versioned)
**Location:** `docs/guides/`

How-to documents and tutorials:
- `*_GUIDE.md` - Step-by-step operational guides
- `README_*.md` - Setup and tutorial documentation

**Purpose:** Train agents on how to use features and workflows.

### Notebooks & Tools (Versioned)
**Location:** `docs/notebooks/`

Interactive Jupyter notebooks for testing and exploration.

### Generated Outputs (Not Versioned)
**Location:** `tmp/`

Generated reports, exports, and temporary files:
- Excel exports (`.xlsx`)
- CSV extracts (`.csv`)
- Temporary logs and debugging output

**Not committed to git** - Use `.gitignore`

---

## 🔒 Client-Specific Information

### Where Client Data Goes
**NEVER put client-specific information in CLAUDE.md or root documentation.**

All client-specific data belongs in `config/client-profiles/<env>.json`:
- Table IDs
- Field mappings
- Account hierarchies
- Data quirks and special handling
- Business rules and calculations

### What Goes in Client Profiles

```json
{
  "version": "1.0",
  "environment": "app",

  "tables": {
    "financials": {
      "id": "12345",
      "name": "Financial Records"
    }
  },

  "field_mappings": {
    "amount": "Amount",
    "date": "Reporting Date",
    "account": "DR_ACC_L1"
  },

  "account_hierarchy": {
    "revenue": "REVENUE",
    "cogs": "Cost of Goods Sold",
    "opex": "Operating Expense"
  },

  "data_quality": {
    "known_issues": ["Missing July data"],
    "missing_periods": ["2025-07", "2025-10"],
    "negative_values_valid": true
  },

  "notes": {
    "data_organization": "Records randomly distributed, sort client-side",
    "optimization": "Use 500-record batches for optimal throughput",
    "special_handling": "14.9% negative values are legitimate reversals"
  }
}
```

### Updating Client Profiles

When agents discover new system information during analysis:

1. **Document in docs/analysis/**: Create analysis markdown files
2. **Update client profile**: Add findings to `config/client-profiles/<env>.json`
3. **Git commit**: Only commit the analysis files, NOT the profile
   ```bash
   git add docs/analysis/TABLE_STRUCTURE_ANALYSIS.md
   git commit -m "docs: Add table structure analysis"
   # Client profile stays local (protected by .gitignore)
   ```

### What NOT to Include in CLAUDE.md

❌ **DON'T document here:**
- Table IDs (e.g., "TABLE_ID")
- Field names (e.g., "DR_ACC_L1")
- Business logic specifics
- Account hierarchies
- Data anomalies or quirks
- Client-specific workflows

✅ **DO document client data in:** `config/client-profiles/<env>.json`

---

## System-Specific Documentation

When agents discover how the system works, document it in `docs/analysis/`:

### Example: Table Structure Discovery

If you discover how a table is organized:

1. **Create analysis file:**
   ```bash
   docs/analysis/TABLE_STRUCTURE_ANALYSIS.md
   ```
   Document what you discovered (publicly shareable)

2. **Update client profile:**
   ```bash
   config/client-profiles/app.json
   ```
   Add client-specific details (stay local)

3. **Commit analysis, not profile:**
   ```bash
   git add docs/analysis/TABLE_STRUCTURE_ANALYSIS.md
   git commit -m "docs: Add table structure analysis"
   ```
   Profile changes don't get committed

---

## Output Files

Generated output files should be saved to `tmp/`:

```bash
# Example output locations
tmp/Financial_Extract_20260203.xlsx
tmp/budget_report_2025_Q1.xlsx
tmp/anomaly_detection_results.csv
```

Files in `tmp/` are **not committed** (protected by `.gitignore`).

---

## Git Commit Guidelines

### ✅ DO COMMIT (Plugin changes)
- Skill definitions (`skills/*/SKILL.md`)
- MCP server code (`mcp-server/src/`, `mcp-server/scripts/`)
- Plugin configuration (`.claude-plugin/plugin.json`)
- Schema files (`config/profile-schema.json`, `config/environments.json`)
- Documentation (`CLAUDE.md`, `README.md`, `SETUP.md`)
- **Analysis & findings** (`docs/analysis/*.md`)
- **Operational guides** (`docs/guides/*.md`)
- **Jupyter notebooks** (`docs/notebooks/*.ipynb`)

### ❌ DO NOT COMMIT (Protected by .gitignore)
- **Client profiles** (`config/client-profiles/*.json`) - Use these for data that varies per environment
- **Output files** (`tmp/`) - Generated reports and exports
- **Authentication credentials** - Stored in system keyring, not files
- **Environment variables** (`.env.local`)

---

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

# Switch active environment
/dr-auth --switch app

# Logout from specific environment
/dr-auth --logout dev

# Logout from all
/dr-auth --logout-all
```

### Using --env Flag

All skills support the `--env` flag:

```bash
/dr-tables --env app               # List tables in production
/dr-profile TABLE_ID --env dev     # Profile in development
/dr-learn --env app                # Create profile for production
/dr-extract --env app --year 2025  # Extract from production
```

---

## Adding Custom Environments

Edit `config/environments.json` to add custom environments:

```json
{
  "environments": {
    "custom-instance": {
      "base_url": "https://custom.datarails.com",
      "auth_url": "https://custom-auth.datarails.com",
      "display_name": "Custom Instance"
    }
  }
}
```

After adding a custom environment:
1. `/dr-auth --env custom-instance` to authenticate
2. `/dr-learn --env custom-instance` to discover tables
3. `/dr-extract --env custom-instance --year 2025` to extract

---

## Available Skills

| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-auth` | Authenticate with Datarails | Session stored in keyring |
| `/dr-learn` | Discover table structure | Creates client profile |
| `/dr-tables` | List and explore tables | Table metadata |
| `/dr-profile` | Profile table statistics | Data quality metrics |
| `/dr-anomalies` | Detect data anomalies | Quality findings |
| `/dr-query` | Query table data | Sample records |
| `/dr-extract` | Extract to Excel | Financial reports |

---

## MCP Server

The MCP server is bundled in `mcp-server/` and runs automatically.

### For Development

```bash
# Install for development
cd mcp-server && pip install -e ".[dev]"

# Run server directly
datarails-mcp serve

# Check status
datarails-mcp status --all

# Check specific environment
datarails-mcp status --env app
```

---

## Authentication Flow

1. **Browser Cookie Extraction**: CLI reads cookies from your browser's local storage
2. **Keyring Storage**: Credentials are securely stored in your system keyring (per environment)
3. **JWT Auto-refresh**: Session cookies are used to automatically fetch/refresh JWT tokens (5-min expiry)

**Supported browsers:** Chrome, Firefox, Safari, Edge, Brave, Opera, Chromium

---

## Troubleshooting

### "Not authenticated" error
1. Make sure you're logged into Datarails in your browser
2. Run `/dr-auth` to extract cookies
3. Check status: `datarails-mcp status`

### Browser cookie extraction fails
1. Try closing the browser first (some browsers lock the cookie database)
2. Use manual entry: `/dr-auth --manual`
3. Grant keychain access if prompted (macOS)

### Wrong environment
1. Check active environment: `/dr-auth --list`
2. Switch: `/dr-auth --switch <env>`
3. Or specify explicitly: `/dr-tables --env app`

### "No profile found" error
1. Run `/dr-learn --env <env>` to create a profile
2. Or copy an existing profile and modify it locally

### Extraction returns unexpected data
1. Check profile at `config/client-profiles/<env>.json`
2. Verify all field mappings are correct
3. Re-run `/dr-learn --env <env>` to rediscover structure

---

## For Developers

### Adding New Skills

Create a new skill in `skills/<skill-name>/SKILL.md`:
```
skills/
└── new-skill/
    └── SKILL.md
```

### Adding System Analysis

Document discoveries in `docs/analysis/`:
```
docs/analysis/
└── NEW_SYSTEM_ANALYSIS.md
```

### Adding Guides

Document procedures in `docs/guides/`:
```
docs/guides/
└── HOW_TO_*.md
```

All new files should be committed to git when they're ready for team use.

---

## Notes

- All client-specific data stays in `config/client-profiles/` (not committed)
- All system documentation goes in `docs/` (committed)
- All generated outputs go in `tmp/` (not committed)
- Keep CLAUDE.md free of specific table IDs, field names, and client business logic
- Use markdown files in `docs/analysis/` for system documentation
- Use client profiles for environment-specific configuration
