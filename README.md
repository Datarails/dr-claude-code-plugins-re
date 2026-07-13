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
/dr-financial-summary                  # Quick revenue/expense/margin snapshot
/dr-intelligence --year 2026           # Generate FP&A intelligence workbook
```

**Connecting:** In Claude Desktop, click "+" > Connectors > Datarails > Connect. In Claude Code, the connector is bundled with the plugin — a browser OAuth window opens the first time a skill uses it; no manual `claude mcp add` step is needed.

New here? Follow the **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** for a hands-on walkthrough (~15 minutes).

---

## Skills

### Data Access & Exploration
| Skill | Description |
|-------|-------------|
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile field statistics |
| `/dr-query` | Query and filter records — value-list and advanced filters (comparisons, ranges, text matching, null checks, date ranges) |
| `/dr-extract` | Extract financial data to Excel |
| `/dr-test` | Test API field compatibility and report which fields work as dimensions |
| `/dr-anomalies` | Detect anomalies in a specific table |
| `/dr-drilldown` | Drill down on a DR.GET value — from a workbook cell, a pasted formula, or a plain-language description (no file needed) |

### Quick Views
| Skill | Description |
|-------|-------------|
| `/dr-financial-summary` | Morning-check snapshot: revenue, expenses, gross margin |
| `/dr-revenue-trends` | Revenue trends, growth rates, and composition |
| `/dr-expense-analysis` | Top expense categories, concentration, and monthly trend |

### Financial Analysis
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-intelligence` | **Most powerful** - FP&A intelligence workbook with auto-insights | up to 10-sheet Excel |
| `/dr-anomalies-report` | Data quality assessment with anomaly detection | Excel report |
| `/dr-insights` | Trend analysis and executive insights | PowerPoint + Excel |
| `/dr-reconcile` | Independent-source pipeline-consistency checks (cross-endpoint agreement, balance-sheet identity, roll-ups, scenario/period integrity) — validates the pipeline, not source systems | Excel report |
| `/dr-dashboard` | Executive KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Scenario/plan-vs-actual variance analysis (scenarios discovered at runtime) | Excel + PowerPoint |
| `/dr-audit` | Audit-support evidence package (completeness, reconciliation, mapping-integrity, substantive samples) — not a SOX certification; ITGC/access-control evidence out of scope | PDF + Excel |
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

### Specialized Agents

Beyond the slash-command skills, the plugin bundles autonomous agents (e.g. `finance-analyst`, `anomaly-detector`) that Claude invokes on its own for open-ended, multi-step analysis — just describe the task in natural language; no manual invocation needed.

### /dr-intelligence (Most Powerful)

```
/dr-intelligence --year 2026                    # Full intelligence workbook
```

**Sheets Generated** (up to 10 — conditional sheets are included only when the org's data sources them, and omitted rather than fabricated):
1. Insights Dashboard - Top 5 findings with severity
2. Expense Deep Dive - Top 20 accounts, % of total
3. Variance Waterfall - What changed and why
4. Trend Analysis - 12-month trends
5. Anomaly Report - Auto-detected outliers
6. Vendor Analysis - Top vendors, concentration risk *(only when vendor-level data exists)*
7. SaaS Metrics - ARR, NRR, CAC, LTV *(only when the org's data sources these metrics; omitted otherwise)*
8. Sales Performance - Rep leaderboard *(only when rep/bookings data exists; omitted otherwise)*
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
| Skill picked the wrong table/fields | Skills discover your financials table and fields automatically; if it guesses wrong, tell it which table/field to use and it will continue |
| Skills not showing | Restart Claude Desktop / Claude Code |
| Slow extraction | Raw row extraction pages 500 rows at a time and can take minutes on large tables; summary skills use aggregation, which returns in seconds |

See [SETUP.md](SETUP.md) for detailed setup and troubleshooting.

---

## License

MIT License - see LICENSE file.

## Privacy

This plugin connects to the Datarails Finance OS service to analyze your financial data. See the [Datarails Privacy Policy](https://www.datarails.com/privacy-policy/) for details on how your data is collected, used, and protected.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
