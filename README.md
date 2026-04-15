# Datarails Finance OS Plugin for Claude

Analyze financial data, detect anomalies, and generate insights directly from Claude.

## Install

### Cowork (Claude Desktop)

1. Open Claude Desktop → Browse plugins → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `Datarails/dr-claude-code-plugins-re`
4. Install the **Datarails FinanceOS** plugin

> **Fallback:** If marketplace install fails due to a [known SSH issue](https://github.com/anthropics/claude-code/issues/26588), download the ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest) and upload via **+** → **Upload plugin**.

### Claude Code (Terminal)

**Option A: Install from GitHub (Recommended)**

Open Claude Code in any project and run:
```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install datarails-financeos@datarails-marketplace
```

> **Important:** Use the full HTTPS URL (not `Datarails/dr-claude-code-plugins-re`). The shorthand format triggers SSH cloning which may fail without SSH keys configured.

This installs the plugin globally — skills are available from any project.

**Option B: Load from local directory (Development)**

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
claude --plugin-dir ./dr-claude-code-plugins-re
```

This loads the plugin for the current session only — useful for development and testing.

**Option C: Run from the plugin directory**

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
claude
```

Skills are auto-discovered from the `skills/` directory when running inside the repo.

**Managing the plugin:**
```
/plugin                    # View installed plugins, enable/disable
/plugin update             # Update to latest version
/plugin uninstall          # Remove the plugin
```

---

## Getting Started

Once the Datarails connector is connected, explore your data:

```
/dr-tables                             # List available tables
/dr-learn                              # Create client profile (first time)
/dr-intelligence --year 2025           # Generate FP&A intelligence workbook
```

**Connecting:** In Claude Desktop, click "+" > Connectors > Datarails > Connect. In Claude Code terminal, run `claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp`.

New here? Follow the **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** for a hands-on walkthrough (~15 minutes).

---

## Skills

### Data Access & Setup
| Skill | Description |
|-------|-------------|
| `/dr-learn` | Discover table structure and create client profile |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile field statistics |
| `/dr-query` | Query and filter records |
| `/dr-extract` | Extract financial data to Excel |
| `/dr-test` | Test API field compatibility and update profile |
| `/dr-anomalies` | Detect anomalies in a specific table |
| `/dr-drilldown` | Drill down on DR.GET formula cells to see underlying detail |

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

### Cowork Commands (Claude Desktop)
| Command | Description |
|---------|-------------|
| `/explore-tables` | Browse available tables |
| `/financial-summary` | Quick financial overview |
| `/revenue-trends` | Revenue trends and growth |
| `/expense-analysis` | Expense breakdown and analysis |
| `/budget-comparison` | Actual vs budget comparison |
| `/data-check` | Data quality checks |
| `/test-api` | Test API field compatibility |
| `/drilldown` | Drill down on DR.GET values |

### /dr-intelligence (Most Powerful)

```
/dr-intelligence --year 2025                    # Full intelligence workbook
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

---

## Authentication

Authentication is handled automatically via **OAuth 2.0 + PKCE** when you connect the Datarails connector. A browser window opens for login — no manual steps needed.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tools not available | Connect via Connectors UI ("+" > Connectors > Datarails > Connect) |
| "Not authenticated" | Disconnect and reconnect via Connectors UI |
| "No profile found" | Run `/dr-learn` first |
| Skills not showing | Restart Claude Desktop / Claude Code |
| Slow extraction | Normal for raw data (~90 rec/sec). Summaries use aggregation (~5s) |

See [SETUP.md](SETUP.md) for detailed setup and troubleshooting.

---

## For Maintainers

### Publishing Updates

```bash
# Bump version in .claude-plugin/plugin.json first
git tag v2.5.0
git push origin main --tags
# GitHub Actions builds the release ZIP automatically
```

---

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
