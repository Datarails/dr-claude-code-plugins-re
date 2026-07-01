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

Add the Datarails connector:

```
claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp
```

A browser window will open for OAuth login when you first use a Datarails tool.

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
- **Claude Code (terminal):** `claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp`

A browser window opens for login. Tokens are managed and refreshed automatically.

### Troubleshooting Connection

| Problem | Solution |
|---------|----------|
| Tools not available | Connect via Connectors UI or `claude mcp add` command |
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
| `/dr-extract --year 2025` | Extract financial data to Excel |
| `/dr-intelligence --year 2025` | Generate FP&A intelligence workbook |
| `/dr-insights --year 2025` | Executive insights with PowerPoint |
| `/dr-reconcile --year 2025` | P&L vs KPI validation |
| `/dr-dashboard` | Executive KPI dashboard |
| `/dr-forecast-variance --year 2025` | Budget vs actual variance |
| `/dr-audit --year 2025` | SOX compliance audit |
| `/dr-departments --year 2025` | Department P&L analysis |
| `/dr-get-formula` | Generate Excel with DR.GET formulas |
| `/dr-drilldown` | Drill down on DR.GET formula cells |
| `/dr-anomalies-report` | Comprehensive anomaly detection report |

---

## API Performance

| Approach | Speed | Use Case |
|----------|-------|----------|
| Aggregation API | ~5 seconds | Summaries, totals, grouped data |
| Pagination | ~10 minutes (50K+ rows) | Raw data extraction, full exports |

Most skills use the aggregation API for fast results. Only `/dr-extract` with raw data needs pagination.

---

## Reporting Issues

1. Run `/dr-test` in Claude Code for a comprehensive API diagnostic
2. Verify the Datarails connector is connected
3. Report with error message and steps to reproduce

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
