# Datarails Finance OS Plugin - Setup Guide

This guide will help you set up and test the Datarails Finance OS plugin for Claude Code.

## Quick Setup (Recommended)

Run the interactive setup wizard:

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
python setup.py
```

The wizard will:
1. Check prerequisites (Python, uv, Claude Code)
2. Verify skills are configured
3. Guide you through authentication
4. Test the connection with data access skills
5. Test Financial Agents (anomaly detection, insights, dashboards)
6. Show next steps

---

## Manual Setup

If you prefer manual setup, follow the steps below.

## Prerequisites

Before starting, ensure you have:

- [ ] **Claude Code** installed ([install guide](https://docs.anthropic.com/claude-code))
- [ ] **Python 3.10+** installed
- [ ] **uv** package manager installed
- [ ] **Datarails account** with access to Finance OS

### Install uv (if not installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

---

## Step 1: Clone the Plugin

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
```

Skills are pre-configured in `skills/` directory - no additional setup needed.

---

## Step 2: Authenticate with Datarails

### 2.1 Log into Datarails in Your Browser

Open your browser and log into Datarails:
- **Development**: https://dev.datarails.com
- **Production**: https://app.datarails.com

Make sure you're logged in and can see the Datarails dashboard.

### 2.2 Run Authentication

```bash
uvx datarails-finance-os-mcp auth
```

The CLI will extract cookies from your browser automatically.

**Expected output:**
```
• Environment: Development (https://dev.datarails.com)

Browser Cookie Authentication
========================================
• Looking for Datarails session in your browser...
• Checking Chrome...
• Found cookies in Chrome
✓ Found session in Chrome!
✓ Credentials saved for environment: dev
• Run 'datarails-mcp status' to verify
```

### 2.3 Verify Authentication

```bash
uv run datarails-mcp status
```

**Expected output:**
```
Datarails MCP Status
========================================

✓ Authenticated
• Environment: Development
• URL: https://dev.datarails.com
✓ Keyring available (credentials stored securely)
```

### Troubleshooting Authentication

| Problem | Solution |
|---------|----------|
| "No Datarails session found" | Make sure you're logged into Datarails in your browser |
| "Browser may be locked" | Close your browser and try again |
| "Cookie decryption failed" | Grant keychain access when prompted (macOS) |
| Wrong environment | Use `--env` flag: `uv run datarails-mcp auth --env app` |

**Manual authentication (if automatic fails):**
```bash
uv run datarails-mcp auth --manual
```
Then copy cookies from browser DevTools (F12 → Application → Cookies).

---

## Step 3: Create Client Profile

Before using extraction skills, create a client profile:

```bash
# Start Claude Code
claude

# In Claude Code, run:
/dr-learn --env app
```

This discovers your table structure and creates `config/client-profiles/app.json`.

---

## Step 4: Start Claude Code

```bash
# Make sure you're in the plugin directory
cd /path/to/dr-claude-code-plugins-re

# Start Claude Code
claude
```

---

## Step 5: Test the Plugin

### Test 1: Check Authentication

Type in Claude Code:
```
Check if I'm authenticated with Datarails
```

**Expected:** Claude confirms you're authenticated to the dev environment.

### Test 2: List Tables

```
/dr-tables
```

**Expected:** A list of Finance OS tables with IDs and names.

### Test 3: View Table Schema

```
/dr-tables 11442
```

(Replace `11442` with an actual table ID from the list)

**Expected:** Table schema with columns, types, and metadata.

### Test 4: Profile a Table

```
/dr-profile 11442
```

**Expected:** Statistics for numeric and categorical fields.

### Test 5: Query Data

```
/dr-query 11442 --sample
```

**Expected:** Sample records from the table (up to 20 rows).

### Test 6: Generate Intelligence Workbook (NEW!)

```
/dr-intelligence --year 2025 --env app
```

**Expected:** 10-sheet Excel workbook with auto-generated insights.
**Note:** This takes ~10 minutes due to API limitations (see below).

---

## Step 6: Test Financial Agents

After authentication, test the Financial Agents Suite:

```bash
cd /path/to/dr-claude-code-plugins-re
claude

# In Claude Code, try:
/dr-anomalies-report --env app
/dr-insights --year 2025 --quarter Q4
/dr-dashboard --env app
/dr-intelligence --year 2025 --env app
```

These agents provide professional financial analysis with Excel and PowerPoint outputs.

---

## Available Commands

| Command | Description |
|---------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-auth --list` | List all environments and auth status |
| `/dr-auth --env app` | Authenticate to production |
| `/dr-auth --switch app` | Switch active environment |
| `/dr-tables` | List all Finance OS tables |
| `/dr-tables <id>` | View schema for a specific table |
| `/dr-profile <id>` | Profile table statistics |
| `/dr-anomalies <id>` | Detect data anomalies |
| `/dr-query <id> --sample` | Get sample records |
| `/dr-query <id> <filter>` | Query with filters |
| `/dr-learn --env app` | Create client profile |
| `/dr-extract --year 2025` | Extract financial data |
| `/dr-intelligence --year 2025` | **Generate FP&A intelligence workbook** |

---

## Multi-Environment Testing

The plugin supports multiple Datarails environments:

| Environment | URL | Use Case |
|-------------|-----|----------|
| `dev` | dev.datarails.com | Development (default) |
| `demo` | demo.datarails.com | Demo |
| `testapp` | testapp.datarails.com | Test App |
| `app` | app.datarails.com | Production |

### Authenticate to Multiple Environments

```bash
# Auth to dev (default)
uvx datarails-finance-os-mcp auth

# Auth to production
uvx datarails-finance-os-mcp auth --env app

# List all authenticated environments
uvx datarails-finance-os-mcp auth --list
```

### Query Different Environments

In Claude Code:
```
/dr-tables --env app
/dr-profile 11442 --env dev
/dr-intelligence --year 2025 --env app
```

---

## Known API Limitations

The Finance OS API has documented limitations that affect performance:

| Issue | Impact | What You'll See |
|-------|--------|-----------------|
| Aggregation API broken | Must fetch all raw data | Longer extraction times |
| JWT expires in 5 min | Token refresh required | "Refreshing token..." messages |
| 500 record page limit | Many API calls needed | ~90 records/second |

**Expected times:**
- Small datasets (< 10K): ~2 minutes
- Medium datasets (10-50K): ~5 minutes
- Large datasets (50K+): ~10 minutes

This is normal behavior, not a bug. See `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` for details.

---

## Diagnostic Tools

If you encounter issues, run the API diagnostic:

```bash
uvx datarails-finance-os-mcp status --all
```

Or use the `/dr-test` skill for a comprehensive API diagnostic.

---

## Reporting Issues

If you encounter problems:

1. **Check authentication status:**
   ```bash
   uvx datarails-finance-os-mcp status --all
   ```

2. **Run API diagnostic:**
   Use the `/dr-test` skill in Claude Code.

3. **Common issues:**
   - Skills not showing: Restart Claude Code
   - Auth fails: Make sure you're logged into Datarails in browser
   - Tools not working: Check MCP server is running
   - Slow extraction: Normal due to API limitations

4. **Report the issue** with:
   - Error message
   - Output of `datarails-mcp status`
   - Output of API diagnostic
   - Steps to reproduce

---

## Quick Reference

```bash
# Setup (one-time)
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
uvx datarails-finance-os-mcp auth

# Daily use
cd dr-claude-code-plugins-re
claude

# In Claude Code
/dr-tables                           # List tables
/dr-learn --env app                  # Create profile (first time)
/dr-intelligence --year 2025         # Generate intelligence workbook
/dr-extract --year 2025              # Extract financial data
```

---

## Best Practices

1. **Always authenticate first** - Run `/dr-auth` or check status
2. **Create profile before extraction** - Run `/dr-learn --env app` once
3. **Use `/dr-intelligence` for comprehensive analysis** - Most powerful skill
4. **Expect longer times for large datasets** - API limitations
5. **Check `docs/analysis/` for system documentation** - Understand limitations
6. **Output goes to `tmp/`** - Check there for generated files
