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

## API Capabilities & Best Practices

The Finance OS API has a two-tier data access model. **Read `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` for full details.**

### Known Issues

| Issue | Status | Impact |
|-------|--------|--------|
| **Aggregation API** | ✅ WORKING (async polling) | ~5 seconds per query, 120x faster than pagination |
| **JWT Token Expiry** | ⚠️ 5 minutes | Must refresh every 20K rows (pagination only) |
| **Distinct Values** | 🔴 BROKEN | Returns 409 - use sample data |
| **Page Size Limit** | ⚠️ 500 max | Requires pagination for raw data |
| **Some Fields Fail** | ⚠️ Per-client | Some fields cause 500 in aggregation - tracked in client profile |

### PREFERRED: Aggregation API (Tier 1 - Fast)

**Use aggregation for summaries, totals, and grouped data (~5 seconds).**

The aggregation API uses async polling (POST 202 + Location header). The `client.aggregate()` method handles this automatically. Most fields work (212/220 tested), but some fields fail per-client. The client profile tracks which fields work and provides alternatives.

```python
# Use aggregate_table_data MCP tool or client.aggregate()
# The profile's aggregation.field_alternatives maps failed fields to working ones
profile = load_profile(env)
agg_hints = profile.get("aggregation", {})

# Check if a field has a known alternative
account_field = fields["account_l1"]
if account_field in agg_hints.get("failed_fields", []):
    # Use the alternative field from the profile
    alt = agg_hints.get("field_alternatives", {}).get("account_l1", account_field)
    account_field = fields.get(alt, account_field)

result = await client.aggregate(
    table_id=financials_table,
    dimensions=["Reporting Date", account_field],
    metrics=[{"field": "Amount", "agg": "SUM"}],
    filters=[{"name": "Scenario", "values": ["Actuals"], "is_excluded": False}]
)
```

### FALLBACK: Pagination (Tier 2 - Slow)

**Use pagination only for raw data extraction or when aggregation fails.**

```python
async def fetch_all_data(table_id, filters, max_rows=100000):
    """Fetch ALL data using pagination with token refresh."""
    all_data = []
    offset = 0

    async with httpx.AsyncClient(timeout=60.0) as client:
        while len(all_data) < max_rows:
            if offset > 0 and offset % 20000 == 0:
                await auth.ensure_valid_token()

            resp = await client.post(url, headers=auth.get_headers(), json={
                'filters': filters,
                'limit': 500,
                'offset': offset
            })

            if resp.status_code == 401:
                await auth.ensure_valid_token()
                continue
            if resp.status_code >= 500:
                await asyncio.sleep(1)
                continue

            page = resp.json().get('data', [])
            if not page:
                break

            all_data.extend(page)
            offset += 500

    return all_data
```

### Profile-Based Aggregation Hints

The client profile (`config/client-profiles/<env>.json`) tracks which fields work with aggregation:

```json
"aggregation": {
  "supported": true,
  "failed_fields": ["DR_ACC_L1", "DR_ACC_L2"],
  "field_alternatives": {
    "account_l1": "account_l1_5",
    "account_l2": "account_l1_5"
  },
  "tested_at": "2026-02-08T..."
}
```

Run `/dr-test` to discover field compatibility and update the profile automatically.

### Performance Expectations

| Approach | Expected Time | Use Case |
|----------|---------------|----------|
| Aggregation (Tier 1) | ~5 seconds | Summaries, totals, grouped data |
| Pagination (Tier 2) | ~10 minutes (50K+ rows) | Raw data extraction, full exports |

**Decision matrix:**
- Need totals/summaries? → Use aggregation
- Need raw records for Excel pivot? → Use pagination
- Field fails in aggregation? → Check `aggregation.field_alternatives` in profile, or fall back to pagination

---

## Project Structure

```
datarails-plugin/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest (required)
│
├── commands/                    # Cowork-friendly commands (no CLI)
│   ├── login.md                 # Browser-based authentication
│   ├── financial-summary.md     # Quick financial overview (aggregation)
│   ├── expense-analysis.md      # Expense breakdown (aggregation)
│   ├── revenue-trends.md        # Revenue patterns (aggregation)
│   ├── budget-comparison.md     # Actual vs budget (aggregation)
│   ├── test-api.md              # API field compatibility test
│   ├── data-check.md            # Data quality check
│   └── explore-tables.md        # Discover data
│
├── skills/                      # Full-featured skills (Claude Code)
│   ├── auth/SKILL.md
│   ├── intelligence/SKILL.md    # Most powerful skill
│   ├── extract/SKILL.md
│   └── ... (15 skills total)
│
├── .claude/
│   └── skills/                  # Symlinks for standalone mode
│       ├── dr-auth -> ../../skills/auth
│       └── ...
│
├── mcp-server/                  # Bundled MCP server
│   ├── src/datarails_mcp/       # Core MCP implementation
│   ├── scripts/
│   │   ├── intelligence_workbook.py  # FP&A intelligence generator
│   │   ├── api_diagnostic.py         # API testing tool
│   │   ├── extract_financials.py     # Data extraction
│   │   └── ...
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
│   │   ├── FINANCE_OS_API_ISSUES_REPORT.md  # API limitations doc
│   │   ├── TABLE_STRUCTURE_ANALYSIS.md
│   │   └── DATA_EXTRACTION_STRATEGY.md
│   ├── guides/                  # Operational documentation
│   └── notebooks/               # Jupyter notebooks
│
├── tmp/                         # Generated outputs (not committed)
│
├── CLAUDE.md                    # This file
├── README.md                    # Project overview
├── SETUP.md                     # Setup instructions
└── .gitignore                   # Excludes client profiles & tmp/
```

---

## Available Skills

### Core Skills
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-auth` | Authenticate with Datarails | Session stored in keyring |
| `/dr-learn` | Discover table structure + aggregation compatibility | Creates client profile |
| `/dr-test` | Test API field compatibility and performance | Diagnostic report + profile update |
| `/dr-tables` | List and explore tables | Table metadata |
| `/dr-profile` | Profile table statistics | Data quality metrics |
| `/dr-anomalies` | Detect data anomalies | Quality findings |
| `/dr-query` | Query table data | Sample records |
| `/dr-extract` | Extract to Excel | Financial reports |

### Financial Analysis Skills
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-intelligence` | **Most powerful** - FP&A intelligence with auto-insights | 10-sheet Excel |
| `/dr-anomalies-report` | Data quality assessment | Excel report |
| `/dr-insights` | Executive insights | PowerPoint + Excel |
| `/dr-reconcile` | P&L vs KPI validation | Excel report |
| `/dr-dashboard` | KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Variance analysis | Excel + PowerPoint |
| `/dr-audit` | SOX compliance | PDF + Excel |
| `/dr-departments` | Department analytics | Excel + PowerPoint |

### Cowork Commands (No CLI Required)

Simple commands for non-technical users in Claude Cowork:

| Command | Description |
|---------|-------------|
| `/datarails-finance-os:login` | Browser-based authentication |
| `/datarails-finance-os:financial-summary` | Quick financial overview (real aggregated totals) |
| `/datarails-finance-os:expense-analysis` | Expense breakdown with complete totals |
| `/datarails-finance-os:revenue-trends` | Revenue patterns over time |
| `/datarails-finance-os:budget-comparison` | Actual vs budget variance analysis |
| `/datarails-finance-os:test-api` | Test API field compatibility and performance |
| `/datarails-finance-os:data-check` | Data quality assessment |
| `/datarails-finance-os:explore-tables` | Discover available data |

These commands use only MCP tools (no Bash) and provide guided workflows suitable for finance teams.

---

## Documentation Organization

### System Analysis & Strategy (Versioned)
**Location:** `docs/analysis/`

These files document how systems work and are versioned with the project:
- `*_ANALYSIS.md` - Technical analysis and findings
- `*_STRATEGY.md` - Implementation strategies and architectures
- `*_REPORT.md` - Investigation reports and discoveries
- `FINANCE_OS_API_ISSUES_REPORT.md` - **Critical API limitations**

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
- PowerPoint presentations (`.pptx`)
- CSV extracts (`.csv`)
- Diagnostic reports (`.txt`)
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
    },
    "kpis": {
      "id": "67890",
      "name": "KPI Metrics"
    }
  },

  "field_mappings": {
    "amount": "Amount",
    "date": "Reporting Date",
    "account_l0": "DR_ACC_L0",
    "account_l1": "DR_ACC_L1",
    "account_l2": "DR_ACC_L2",
    "scenario": "Scenario",
    "year": "System_Year"
  },

  "account_hierarchy": {
    "pnl_filter": "P&L",
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

## Output Files

Generated output files should be saved to `tmp/`:

```bash
# Example output locations
tmp/FPA_Intelligence_Workbook_2025_20260205.xlsx
tmp/Financial_Extract_2025.xlsx
tmp/API_Diagnostic_Report_20260205.txt
tmp/Insights_2025_Q4.pptx
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
/dr-intelligence --year 2025 --env app  # Intelligence workbook
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

### Diagnostic Tool

Test API connectivity and identify issues:

```bash
# Run comprehensive API diagnostic
uv --directory mcp-server run python scripts/api_diagnostic.py --env app
```

Generates report with:
- Endpoint test results
- Response times
- Error analysis
- Recommendations

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

### Slow extraction (normal for raw data)
For raw data extraction via pagination:
- ~90 records/second
- 54K records = ~10 minutes
- This is expected for `/dr-extract` raw exports

For summaries/totals, use aggregation instead (~5 seconds).

### API returns 500 errors on aggregation
Some fields fail in aggregation on a per-client basis:
1. Run `/dr-test` to discover which fields work
2. Check `aggregation.field_alternatives` in the client profile
3. See `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` for details

---

## For Developers

### Adding New Skills

Create a new skill in `skills/<skill-name>/SKILL.md` (official plugin location):
```
skills/
└── new-skill/
    └── SKILL.md
```

Then create a symlink in `.claude/skills/` for standalone mode:
```bash
cd .claude/skills && ln -sf ../../skills/new-skill dr-new-skill
```

**Required SKILL.md sections:**
- Frontmatter (name, description, allowed-tools, argument-hint)
- Client Profile System section (if using profiles)
- Workflow section with phases
- Execution Instructions
- Troubleshooting

See `skills/intelligence/SKILL.md` as reference.

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
- **Read `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` before building new features**
