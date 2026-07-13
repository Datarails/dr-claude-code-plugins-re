# Datarails Finance OS Plugin for Claude

Analyze financial data, detect anomalies, and build FP&A reports directly in Claude — connected live to your Datarails Finance OS.

## Install

### Claude Desktop (Cowork)

1. Open Claude Desktop → **Browse plugins** → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter `Datarails/dr-claude-code-plugins-re`
4. Install **Datarails FinanceOS**

> **If marketplace install fails** (a [known SSH issue](https://github.com/anthropics/claude-code/issues/26588)): download the ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest) and add it via **+** → **Upload plugin**.

### Claude Code (Terminal)

```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install datarails-financeos@datarails-marketplace
```

> Use the full HTTPS URL (not the `owner/repo` shorthand) — the shorthand triggers SSH cloning, which fails without SSH keys configured.

Manage it anytime: `/plugin` (view, enable/disable), `/plugin update`, `/plugin uninstall`. For local development, load a clone directly with `claude --plugin-dir ./dr-claude-code-plugins-re` (that session only).

## Connect to Datarails

The Datarails connector is **bundled with the plugin** — there's no separate setup or `claude mcp add` step. The first time a skill needs data, a browser window opens for **OAuth login**; sign in once and you're connected. (In Claude Desktop you can also connect from **+** → **Connectors** → **Datarails**.)

## Using the plugin

**Just ask.** Describe what you want in plain language and Claude picks the right skill or agent automatically:

> "Give me a financial summary for 2026."
> "What are our top expenses this year — flag anything unusual."
> "Build an FP&A intelligence workbook."

**Or invoke a skill explicitly.** In Claude Code, type `/datarails-financeos:` and press **Tab** to autocomplete every command:

```
/datarails-financeos:tables                      # list & explore tables
/datarails-financeos:financial-summary            # revenue / expense / margin snapshot
/datarails-financeos:intelligence --year 2026     # full FP&A workbook
```

> The `datarails-financeos:` prefix is **required** — Claude Code namespaces every plugin skill to prevent collisions, so a bare `/tables` won't resolve.

## Skills

Invoke any of these as **`/datarails-financeos:<name>`**, or just describe the task and let Claude choose. Every skill discovers your org's tables, fields, scenarios, and account structure at runtime — nothing is hardcoded.

### Explore & query
| Skill | What it does |
|-------|--------------|
| `tables` | List tables, view schemas, inspect a field's values |
| `profile` | Field statistics — null rates, cardinality, range outliers |
| `query` | Fetch and filter records; value-list **and** advanced filters (ranges, comparisons, text, null checks, date ranges) |
| `test` | Check which fields work as aggregation dimensions in your environment |

### Snapshots & trends
| Skill | What it does |
|-------|--------------|
| `financial-summary` | Period-scoped snapshot: revenue, expenses, gross profit & margin |
| `revenue-trends` | Revenue growth rates, seasonality, composition over time |
| `expense-analysis` | Top expense categories, concentration, monthly trend |

### Reports & workbooks
| Skill | What it does | Output |
|-------|--------------|--------|
| `intelligence` | **Most powerful** — FP&A workbook with auto-detected insights | Excel (up to 10 sheets) |
| `insights` | Executive trend analysis and narrative | PowerPoint + Excel |
| `dashboard` | Executive KPI dashboard | Excel + PowerPoint |
| `departments` | Departmental P&L and comparison | Excel + PowerPoint |
| `forecast-variance` | Multi-scenario variance — scenarios discovered at runtime (no fixed "Budget" assumed) | Excel + PowerPoint |
| `extract` | Extract validated financial data (P&L, Balance Sheet, sourceable KPIs) | Excel |

### Assurance & data quality
| Skill | What it does | Output |
|-------|--------------|--------|
| `anomalies` | Detect data-quality anomalies in a table | inline |
| `anomalies-report` | Full data-quality assessment with a quality score | Excel |
| `reconciliation` | Independent-source consistency checks — cross-endpoint agreement, balance-sheet identity, roll-ups, scenario/period integrity. Validates the **data pipeline**, not source systems | Excel |
| `audit` | Audit-support evidence package (completeness, reconciliation, mapping integrity, sampling). **Not** a SOX certification — access-control / change-management / ITGC evidence is out of scope | PDF + Excel |

### Excel & drill-down
| Skill | What it does |
|-------|--------------|
| `get-formula` | Generate Excel workbooks with live `DR.GET` formulas |
| `drilldown` | Break a Datarails number into its line items — from a workbook cell, a pasted `DR.GET` formula, or a plain-language description (no file needed) |

> A few short **command aliases** also resolve under the same namespace for common tasks — `/datarails-financeos:explore-tables`, `:data-check`, `:budget-comparison`, `:test-api` — each launches the matching skill above.

## Agents

Beyond the skills, the plugin ships **autonomous agents** — `finance-analyst`, `anomaly-detector`, and others — that Claude engages on its own for open-ended, multi-step work (e.g. "profile this table and write up the data-quality risks"). You don't invoke them by name; just describe the task and Claude delegates.

## The intelligence workbook

The flagship report. Run it for a full FP&A book:

```
/datarails-financeos:intelligence --year 2026
```

It generates **up to 10 sheets** — conditional sheets are included only when your data sources them, and omitted (never fabricated) otherwise:

1. **Insights Dashboard** — top findings with severity
2. **Expense Deep Dive** — top accounts, % of total
3. **Variance Waterfall** — what changed and why
4. **Trend Analysis** — 12-month trends
5. **Anomaly Report** — auto-detected outliers
6. **Vendor Analysis** — top vendors, concentration *(when vendor data exists)*
7. **SaaS Metrics** — ARR, NRR, CAC, LTV *(when your data sources them)*
8. **Sales Performance** — rep leaderboard *(when rep/bookings data exists)*
9. **Cost Center P&L** — department detail
10. **Raw Data** — pivot-ready

## Authentication

Handled automatically via **OAuth 2.0 + PKCE** when the connector is first used — a browser window opens for login, tokens refresh on their own, and there are no manual steps.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| A command isn't found | Type `/datarails-financeos:` and press **Tab** — every command is under that prefix; a bare name won't resolve |
| Tools not available | Connect the Datarails connector: **+** → **Connectors** → **Datarails** → **Connect** |
| "Not authenticated" | Disconnect and reconnect the Datarails connector |
| Skill picked the wrong table/field | Skills discover your financials table and fields automatically; if it guesses wrong, tell it which to use and it continues — there's no profile to configure |
| Commands not showing | Restart Claude Desktop / Claude Code, and check the plugin is enabled (`/plugin`) |
| Slow extraction | Row-by-row extraction pages 500 rows at a time and can take minutes on large tables; summary skills use aggregation, which returns in seconds |

See [SETUP.md](SETUP.md) for detailed setup and troubleshooting, or the [Getting Started Guide](docs/guides/GETTING_STARTED.md) for a ~15-minute hands-on walkthrough.

## License

MIT License — see LICENSE file.

## Privacy

This plugin connects to the Datarails Finance OS service to analyze your financial data. See the [Datarails Privacy Policy](https://www.datarails.com/privacy-policy/) for how your data is collected, used, and protected.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
