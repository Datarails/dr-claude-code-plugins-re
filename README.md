# Datarails Finance OS Plugin for Claude Code

Analyze financial data, detect anomalies, and query Finance OS tables directly from Claude Code.

## Features

### Data Access & Exploration
- **Multi-Account Support** - Connect to dev, demo, testapp, and production environments
- **Easy Authentication** - Browser cookie extraction for seamless login
- **Table Discovery** - List and explore all Finance OS tables
- **Data Profiling** - Numeric and categorical field analysis
- **Anomaly Detection** - Automated data quality checks
- **Data Queries** - Filter, sample, and query records
- **Data Extraction** - Export validated financial data to Excel

### Financial Analysis Suite (NEW! 🎯)
- **Anomaly Detection** - Data quality monitoring with severity scoring
- **Trend Analysis** - P&L trends, KPI analysis, growth metrics
- **Executive Insights** - Professional PowerPoint presentations with visualizations
- **Data Reconciliation** - P&L vs KPI consistency validation
- **Executive Dashboard** - Real-time KPI monitoring
- **Forecast Analysis** - Multi-scenario (Actuals/Budget/Forecast) variance analysis
- **Compliance Auditing** - SOX compliance control testing and audit reports
- **Department Analytics** - Departmental P&L and performance analysis

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

### Data Access & Setup
| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-learn` | Discover table structure and create client profile |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile field statistics |
| `/dr-query` | Query and filter records |
| `/dr-extract` | Extract financial data to Excel |

### Financial Analysis Agents (NEW! 🚀)
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-anomalies-report` | Data quality assessment with anomaly detection | Excel report |
| `/dr-insights` | Trend analysis and executive insights | PowerPoint + Excel |
| `/dr-reconcile` | P&L vs KPI consistency validation | Excel report |
| `/dr-dashboard` | Executive KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Budget vs actual variance analysis | Excel + PowerPoint |
| `/dr-audit` | SOX compliance audit reporting | PDF + Excel |
| `/dr-departments` | Department P&L analysis | Excel + PowerPoint |

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

## Financial Agents Suite

A complete suite of 7 specialized financial analysis agents for executive reporting, compliance, and business intelligence.

### Quick Examples

**Check data quality**:
```
/dr-anomalies-report --env app
```
Generates Excel report with critical, high, medium, and low priority findings.

**Generate quarterly insights**:
```
/dr-insights --year 2025 --quarter Q4
```
Generates professional PowerPoint presentation (7 slides) + Excel data book with trends, KPIs, and recommendations.

**Validate P&L vs KPI consistency**:
```
/dr-reconcile --year 2025
```
Validates consistency between P&L and KPI tables, identifies variance exceptions.

**Executive KPI dashboard**:
```
/dr-dashboard --env app
```
Real-time executive dashboard in Excel and one-page PowerPoint summary.

**Budget vs actual variance analysis**:
```
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget,Forecast
```
Multi-scenario variance analysis comparing actual, budget, and forecast.

**SOX compliance audit**:
```
/dr-audit --year 2025 --quarter Q4
```
Generates professional PDF audit report + Excel evidence package.

**Department performance analysis**:
```
/dr-departments --year 2025
```
Department P&L analysis with Excel + PowerPoint outputs.

### Financial Agents Documentation

See individual skill documentation for complete details:
- `/dr-anomalies-report` - Data quality assessment
- `/dr-insights` - Trend analysis & visualizations
- `/dr-reconcile` - Consistency validation
- `/dr-dashboard` - Executive KPI monitoring
- `/dr-forecast-variance` - Variance analysis
- `/dr-audit` - Compliance auditing
- `/dr-departments` - Department analytics

For comprehensive implementation details, see [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md).

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
│   ├── extract/SKILL.md         # /dr-extract
│   ├── anomalies-report/SKILL.md        # /dr-anomalies-report (NEW!)
│   ├── insights/SKILL.md                # /dr-insights (NEW!)
│   ├── reconciliation/SKILL.md          # /dr-reconcile (NEW!)
│   ├── dashboard/SKILL.md               # /dr-dashboard (NEW!)
│   ├── forecast-variance/SKILL.md       # /dr-forecast-variance (NEW!)
│   ├── audit/SKILL.md                   # /dr-audit (NEW!)
│   └── departments/SKILL.md             # /dr-departments (NEW!)
├── agents/                      # Agent definitions
│   ├── anomaly-detector.md
│   ├── insights.md
│   ├── reconciliation.md
│   ├── dashboard.md
│   ├── forecast.md
│   ├── audit.md
│   └── departments.md
├── mcp-server/                  # Bundled MCP server
│   ├── src/datarails_mcp/
│   │   ├── report_utils.py              # Report formatting utilities (NEW!)
│   │   ├── chart_builder.py             # Chart generation (NEW!)
│   │   ├── excel_builder.py             # Excel generation (NEW!)
│   │   ├── pptx_builder.py              # PowerPoint generation (NEW!)
│   │   ├── pdf_builder.py               # PDF generation (NEW!)
│   │   └── ... (existing modules)
│   ├── scripts/
│   │   ├── extract_financials.py
│   │   ├── anomaly_detector.py          # (NEW!)
│   │   ├── insights_generator.py        # (NEW!)
│   │   ├── reconciliation_engine.py     # (NEW!)
│   │   ├── executive_dashboard.py       # (NEW!)
│   │   ├── forecast_analyzer.py         # (NEW!)
│   │   ├── compliance_auditor.py        # (NEW!)
│   │   └── department_analytics.py      # (NEW!)
│   ├── templates/               # Report styling (NEW!)
│   ├── tests/
│   └── pyproject.toml
├── config/
│   ├── environments.json        # Configurable environments
│   ├── profile-schema.json      # Client profile schema
│   └── client-profiles/         # Client-specific configs (not committed)
├── tmp/                         # Output files location
├── .mcp.json                    # MCP server config
├── CLAUDE.md                    # Claude Code instructions
├── SETUP.md                     # Detailed setup guide
├── README.md                    # This file
├── IMPLEMENTATION_COMPLETE.md   # Full implementation details (NEW!)
└── PHASE_1_2_SUMMARY.md         # Phase summary (NEW!)
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
