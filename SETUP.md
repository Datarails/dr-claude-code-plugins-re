# Datarails Finance OS Plugin - Setup Guide

## Cowork Setup (Claude Desktop)

### Option 1: Upload ZIP (Recommended)

1. Download the plugin ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest)
2. Open Claude Desktop → Cowork → Browse plugins → **Personal** tab
3. Click **+** → **Upload plugin**
4. Select the downloaded ZIP
5. Restart Claude Desktop

### Option 2: Marketplace (GitHub)

1. Open Claude Desktop → Browse plugins → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `https://github.com/Datarails/dr-claude-code-plugins-re.git`
4. Install the **Datarails FinanceOS** plugin
5. Restart Claude Desktop

> **Known issue:** The marketplace install may fail with "Host key verification failed" due to a [known Claude Desktop bug](https://github.com/anthropics/claude-code/issues/26588) where the VM uses SSH instead of HTTPS. Use Option 1 (ZIP upload) if this happens.

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

### Step 1: Clone the Plugin

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
```

### Step 2: Start Claude Code

```bash
claude
```

Skills are automatically available from the `skills/` directory.

### Step 3: Connect to Datarails

Add the Datarails connector:

```
claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp
```

A browser window will open for OAuth login when you first use a Datarails tool.

### Step 4: Create Client Profile (First Time)

```
/dr-learn
```

This discovers your table structure and creates `config/client-profiles/app.json`.

### Step 5: Test

```
/dr-tables                             # List tables
/dr-query <table_id> --sample          # Get sample data
/dr-intelligence --year 2025           # Generate intelligence workbook
```

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
| `/dr-learn` | Create client profile |
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
