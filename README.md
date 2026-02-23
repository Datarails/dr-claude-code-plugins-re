# Datarails Finance OS Plugin for Claude Code & Cowork

Analyze financial data, detect anomalies, and query Finance OS tables directly from Claude Code or Claude Cowork.

## For Cowork Users (Finance Team)

**No terminal or coding experience required.**

### Install

1. Download the installer for your OS:
   - **Mac:** [`install-datarails-plugin.command`](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest/download/install-datarails-plugin.command)
   - **Windows:** [`install-datarails-plugin.bat`](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest/download/install-datarails-plugin.bat)
2. Double-click the downloaded file
3. Restart Claude Desktop

That's it! Open a Cowork conversation and ask: **"What can you do with Datarails?"**

### Update

Double-click the same installer file again. It downloads the latest version automatically.

### Prerequisites

- [Claude Desktop](https://claude.ai/desktop) with Cowork enabled
- [uv](https://astral.sh/uv) (Python package manager - the installer will warn you if it's missing)
- A Datarails account (be logged in via your browser)

---

## For Claude Code Users (Developers)

### Quick Start

```bash
# 1. Clone the plugin
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re

# 2. Run the setup wizard
python setup.py
```

Or manually:

```bash
# 2. Authenticate (be logged into Datarails in browser first)
uvx datarails-finance-os-mcp auth

# 3. Start Claude Code
claude

# 4. Test
/dr-tables
```

New here? Follow the **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** for a hands-on walkthrough (~15 minutes).

---

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
- **Intelligence Workbook** - Comprehensive FP&A analysis with auto-insights
- **Anomaly Detection** - Data quality monitoring with severity scoring
- **Trend Analysis** - P&L trends, KPI analysis, growth metrics
- **Executive Insights** - Professional PowerPoint presentations with visualizations
- **Data Reconciliation** - P&L vs KPI consistency validation
- **Executive Dashboard** - Real-time KPI monitoring
- **Forecast Analysis** - Multi-scenario (Actuals/Budget/Forecast) variance analysis
- **Compliance Auditing** - SOX compliance control testing and audit reports
- **Department Analytics** - Departmental P&L and performance analysis

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

### Financial Analysis
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
| `/dr-get-formula` | Generate Excel with DR.GET formulas | Excel workbook |

### /dr-intelligence (Most Powerful)

Generate comprehensive FP&A intelligence workbooks with auto-detected insights.

```
/dr-intelligence --year 2025                    # Full intelligence workbook
/dr-intelligence --year 2025 --env app          # From production
```

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

## Multi-Environment Support

| Environment | URL | Description |
|-------------|-----|-------------|
| `dev` | dev.datarails.com | Development |
| `demo` | demo.datarails.com | Demo |
| `testapp` | testapp.datarails.com | Test App |
| `app` | app.datarails.com | Production |

All skills support the `--env` flag:

```
/dr-tables --env app               # Production tables
/dr-intelligence --year 2025 --env app  # Intelligence from production
```

## Publishing Updates (for maintainers)

```bash
# 1. Make changes, commit
git add . && git commit -m "feat: your changes"

# 2. Tag and push
git tag v1.3.0
git push origin main --tags

# 3. GitHub Actions auto-builds the release
# Colleagues double-click their installer to get the update
```

## Troubleshooting

See [SETUP.md](SETUP.md#troubleshooting-authentication) for detailed troubleshooting.

| Problem | Solution |
|---------|----------|
| Skills not showing | Restart Claude Code; skills are in `skills/` directory |
| "Not authenticated" | Run `uvx datarails-finance-os-mcp auth` |
| Wrong environment | Use `--env` flag or `datarails-mcp auth --switch <env>` |
| Slow extraction | Normal - API requires pagination (~90 rec/sec) |
| "No profile found" | Run `/dr-learn --env <env>` first |
| Installer can't find Cowork dir | Open Claude Desktop with Cowork first, then re-run |

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
