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

### Financial Analysis Suite
- **Intelligence Workbook** - Comprehensive FP&A analysis with auto-insights (NEW!)
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

### Financial Analysis Agents
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-intelligence` | **Most powerful** - FP&A intelligence workbook with auto-insights | 10-sheet Excel |
| `/dr-anomalies-report` | Data quality assessment with anomaly detection | Excel report |
| `/dr-insights` | Trend analysis and executive insights | PowerPoint + Excel |
| `/dr-reconcile` | P&L vs KPI consistency validation | Excel report |
| `/dr-dashboard` | Executive KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Budget vs actual variance analysis | Excel + PowerPoint |
| `/dr-audit` | SOX compliance audit reporting | PDF + Excel |
| `/dr-departments` | Department P&L analysis | Excel + PowerPoint |

### /dr-intelligence (NEW - Most Powerful!)

Generate comprehensive FP&A intelligence workbooks with auto-detected insights.

```
/dr-intelligence --year 2025                    # Full intelligence workbook
/dr-intelligence --year 2025 --env app          # From production
/dr-intelligence --year 2025 --output report.xlsx
```

**What makes it different:**
| Traditional Report | Intelligence Workbook |
|-------------------|----------------------|
| Shows data | Answers questions |
| Lists numbers | Explains "why" |
| Static tables | Highlights anomalies |
| Manual analysis | Insights auto-surfaced |
| Data dump | Recommendations included |

**10 Sheets Generated:**
1. Insights Dashboard - Top 5 findings with severity
2. Expense Deep Dive - Top 20 accounts, % of total
3. Variance Waterfall - What changed and why
4. Trend Analysis - 12-month trends
5. Anomaly Report - Auto-detected outliers
6. Vendor Analysis - Top vendors, concentration risk
7. SaaS Metrics - ARR, LTV, CAC, Efficiency
8. Sales Performance - Rep leaderboard
9. Cost Center P&L - Department detail
10. Raw Data - Pivot-ready for analysis

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

Discover table structure and create a client profile. Run this once per environment to enable `/dr-extract` and `/dr-intelligence`.

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

A complete suite of specialized financial analysis agents for executive reporting, compliance, and business intelligence.

### Quick Examples

**Generate comprehensive intelligence workbook** (NEW!):
```
/dr-intelligence --year 2025 --env app
```
Generates 10-sheet Excel with auto-detected insights, recommendations, and professional formatting.

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
│   └── skills/                  # Skill definitions
│       ├── dr-auth/
│       ├── dr-intelligence/     # NEW - FP&A Intelligence Workbook
│       ├── dr-extract/
│       └── ...
├── mcp-server/                  # Bundled MCP server
│   ├── src/datarails_mcp/
│   │   ├── client.py            # API client
│   │   ├── auth.py              # Authentication
│   │   ├── report_utils.py      # Report formatting
│   │   ├── excel_builder.py     # Excel generation
│   │   ├── pptx_builder.py      # PowerPoint generation
│   │   └── ...
│   ├── scripts/
│   │   ├── intelligence_workbook.py  # NEW - Intelligence generator
│   │   ├── api_diagnostic.py         # NEW - API testing tool
│   │   ├── extract_financials.py
│   │   └── ...
│   └── pyproject.toml
├── config/
│   ├── environments.json        # Configurable environments
│   ├── profile-schema.json      # Client profile schema
│   └── client-profiles/         # Client-specific configs (not committed)
├── docs/
│   ├── analysis/
│   │   ├── FINANCE_OS_API_ISSUES_REPORT.md  # NEW - API issues documentation
│   │   └── ...
│   └── guides/
├── tmp/                         # Output files location (not committed)
├── CLAUDE.md                    # Claude Code instructions
├── SETUP.md                     # Detailed setup guide
└── README.md                    # This file
```

## Known API Limitations

The Finance OS API has documented limitations (see `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md`):

| Issue | Impact | Workaround |
|-------|--------|------------|
| Aggregation API fails | Returns 500/502/202 | Client-side aggregation |
| JWT expires in 5 min | Long operations fail | Auto-refresh every 20K rows |
| 500 record page limit | Slow extraction | Pagination implemented |
| Distinct values fails | Returns 409 | Sample data extraction |

**Performance:** Extracting 54K records takes ~10 minutes due to these limitations.

## Data Limits

The plugin enforces sensible limits to prevent data overload:

| Operation | Max Rows |
|-----------|----------|
| Sample records | 20 |
| Filtered query | 500 |
| Custom query | 1,000 |
| Paginated extraction | 100,000 |

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
| Slow extraction | Normal - API requires pagination (~90 rec/sec) |
| "No profile found" | Run `/dr-learn --env <env>` first |

## Diagnostic Tools

Test API connectivity and performance:

```bash
# Run API diagnostic
uv --directory mcp-server run python scripts/api_diagnostic.py --env app
```

Generates report at `tmp/API_Diagnostic_Report_*.txt` with:
- Endpoint test results
- Response times
- Error analysis
- Recommendations

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins/issues
- Datarails Support: support@datarails.com
