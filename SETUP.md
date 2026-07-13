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
/datarails-financeos:tables                             # List tables
/datarails-financeos:financial-summary                  # Quick revenue/expense/margin snapshot
/datarails-financeos:intelligence --year 2026           # Generate intelligence workbook
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
| `/datarails-financeos:test` | Test API field compatibility |
| `/datarails-financeos:tables` | List all Finance OS tables |
| `/datarails-financeos:tables <id>` | View schema for a specific table |
| `/datarails-financeos:profile <id>` | Profile table statistics |
| `/datarails-financeos:anomalies <id>` | Detect data anomalies |
| `/datarails-financeos:query <id> --sample` | Get sample records |
| `/datarails-financeos:financial-summary` | Revenue/expense/margin snapshot |
| `/datarails-financeos:revenue-trends` | Revenue trends and growth rates |
| `/datarails-financeos:expense-analysis` | Top expense categories and trends |
| `/datarails-financeos:extract --year 2026` | Extract financial data to Excel |
| `/datarails-financeos:intelligence --year 2026` | Generate FP&A intelligence workbook |
| `/datarails-financeos:insights --year 2026` | Executive insights with PowerPoint |
| `/datarails-financeos:reconciliation --year 2026` | Independent-source pipeline-consistency checks |
| `/datarails-financeos:dashboard` | Executive KPI dashboard |
| `/datarails-financeos:forecast-variance --year 2026` | Scenario/plan-vs-actual variance |
| `/datarails-financeos:audit --year 2026` | Audit-support evidence package (not a SOX certification) |
| `/datarails-financeos:departments --year 2026` | Department P&L analysis |
| `/datarails-financeos:get-formula` | Generate Excel with DR.GET formulas |
| `/datarails-financeos:drilldown` | Drill down on DR.GET formula cells |
| `/datarails-financeos:anomalies-report` | Comprehensive anomaly detection report |

---

## API Performance

| Approach | Speed | Use Case |
|----------|-------|----------|
| Aggregation API | Fast — returns in seconds, no row limit | Summaries, totals, grouped data |
| Pagination | Much slower — capped at 500 rows per page | Raw data extraction, full exports |

Most skills use the aggregation API for fast results. Only `/datarails-financeos:extract` with raw data needs pagination.

---

## Reporting Issues

1. Run `/datarails-financeos:test` in Claude Code for a comprehensive API diagnostic
2. Verify the Datarails connector is connected
3. Report with error message and steps to reproduce

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
