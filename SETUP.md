# Datarails Finance OS Plugin - Setup Guide

## Cowork Setup (Claude Desktop)

### Option 1: Marketplace (Recommended)

1. Open Claude Desktop → Browse plugins → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `Datarails/dr-claude-code-plugins-re`
4. Install the **Datarails Finance OS** plugin
5. Restart Claude Desktop

### Option 2: Upload ZIP

1. Download the plugin ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest)
2. Open Claude Desktop → Browse plugins → **Personal** tab
3. Click **+** → **Upload plugin**
4. Select the downloaded ZIP
5. Restart Claude Desktop

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

### Step 3: Authenticate

In Claude Code:

```
/dr-auth --env app
```

Make sure you're logged into Datarails in your browser first. The CLI extracts cookies automatically.

### Step 4: Create Client Profile (First Time)

```
/dr-learn --env app
```

This discovers your table structure and creates `config/client-profiles/app.json`.

### Step 5: Test

```
/dr-tables                             # List tables
/dr-query <table_id> --sample          # Get sample data
/dr-intelligence --year 2025 --env app # Generate intelligence workbook
```

---

## Authentication

### How It Works

1. **Log into Datarails** in your browser (Chrome, Firefox, Safari, Edge, Brave)
2. **Run `/dr-auth`** - extracts session cookies from your browser automatically
3. **Credentials stored** securely in your system keyring (per environment)
4. **JWT auto-refresh** - tokens refresh automatically (5-min expiry handled transparently)

### Multi-Environment

```
/dr-auth --env app          # Authenticate to production
/dr-auth --env dev          # Authenticate to development
/dr-auth --list             # See all connections
/dr-auth --switch app       # Switch active environment
```

### Troubleshooting Authentication

| Problem | Solution |
|---------|----------|
| "No Datarails session found" | Log into Datarails in your browser first |
| "Browser may be locked" | Close the browser and retry |
| "Cookie decryption failed" | Grant keychain access when prompted (macOS) |
| Wrong environment | Use `--env` flag: `/dr-auth --env app` |
| Manual auth needed | Run `/dr-auth --manual` and paste cookies from DevTools |

---

## Available Skills

| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-auth --list` | List all environments and auth status |
| `/dr-learn --env app` | Create client profile |
| `/dr-test --env app` | Test API field compatibility |
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
2. Check authentication: `/dr-auth --list`
3. Report with error message and steps to reproduce

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
