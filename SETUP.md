# Datarails Finance OS Plugin - Setup Guide

## Cowork Setup (Claude Desktop)

1. Open Claude Desktop → Browse plugins → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `Datarails/dr-claude-code-plugins-re`
4. Install the **Datarails FinanceOS** plugin
5. Restart Claude Desktop

> **Fallback:** If marketplace install fails due to a [known SSH issue](https://github.com/anthropics/claude-code/issues/26588), download the ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest) and upload via **+** → **Upload plugin**.

### After Installation

Open a Cowork conversation and try:

```
What can you do with Datarails?
```

Or jump straight in:

```
Show me a financial summary for 2025
```

---

## Claude Code Setup

### Prerequisites

- [Claude Code](https://docs.anthropic.com/claude-code) installed
- A Datarails account with access to Finance OS

### Step 1: Install the Plugin

Open Claude Code in any project and run:

```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install datarails-financeos@datarails-marketplace
```

Skills are installed globally and available from any project.

### Step 2: Connect to Datarails

The connector is **bundled with the plugin** — the server `datarails-finance-os`
(`https://mcp.datarails.com/mcp`) is registered automatically on install. No
`claude mcp add` step is needed. A browser window opens for OAuth login the
first time a Datarails tool is used.

### Step 3: Try a skill

```
/dr-tables                             # List tables
/dr-financial-summary                  # Quick revenue/expense/margin snapshot
/dr-intelligence --year 2025           # Generate intelligence workbook
```

No setup or profile step is needed — every skill discovers your financials table and field names on its own, each session.

---

## Authentication

Authentication is handled automatically via **OAuth 2.0 + PKCE** when you connect the Datarails connector.

### Connecting

- **Claude Desktop / Cowork:** Click "+" > Connectors > Datarails > Connect
- **Claude Code (terminal):** the connector is bundled with the plugin — a browser window opens for OAuth on first tool use.

A browser window opens for login. Tokens are managed and refreshed automatically.

### Troubleshooting Connection

| Problem | Solution |
|---------|----------|
| Tools not available | Verify the plugin is installed and enabled (`/plugin`); reconnect the Datarails connector if prompted |
| "Not authenticated" | Disconnect and reconnect via Connectors UI |
| Browser doesn't open | Check default browser settings |
| Need different environment | Disconnect and reconnect |

---

## Available Skills

| Skill | Description |
|-------|-------------|
| `/dr-test` | Test API field compatibility |
| `/dr-tables` | List all Finance OS tables |
| `/dr-tables <id>` | View schema for a specific table |
| `/dr-profile <id>` | Profile table statistics |
| `/dr-anomalies <id>` | Detect data anomalies |
| `/dr-query <id> --sample` | Get sample records |
| `/dr-financial-summary` | Revenue/expense/margin snapshot |
| `/dr-revenue-trends` | Revenue trends and growth rates |
| `/dr-expense-analysis` | Top expense categories and trends |
| `/dr-extract --year 2025` | Extract financial data to Excel |
| `/dr-intelligence --year 2025` | Generate FP&A intelligence workbook |
| `/dr-insights --year 2025` | Executive insights with PowerPoint |
| `/dr-reconcile --year 2025` | Independent-source pipeline-consistency checks |
| `/dr-dashboard` | Executive KPI dashboard |
| `/dr-forecast-variance --year 2025` | Scenario/plan-vs-actual variance |
| `/dr-audit --year 2025` | Audit-support evidence package (SOX-oriented reports) |
| `/dr-departments --year 2025` | Department P&L analysis |
| `/dr-get-formula` | Generate Excel with DR.GET formulas |
| `/dr-drilldown` | Drill down on DR.GET formula cells |
| `/dr-anomalies-report` | Comprehensive anomaly detection report |

---

## API Performance

| Approach | Speed | Use Case |
|----------|-------|----------|
| Aggregation API | Fast — returns in seconds, no row limit | Summaries, totals, grouped data |
| Pagination | Much slower — capped at 500 rows per page | Raw data extraction, full exports |

Most skills use the aggregation API for fast results. Only `/dr-extract` with raw data needs pagination.

---

## Reporting Issues

1. Run `/dr-test` in Claude Code for a comprehensive API diagnostic
2. Verify the Datarails connector is connected
3. Report with error message and steps to reproduce

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
