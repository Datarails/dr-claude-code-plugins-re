# Datarails Finance OS Plugin - Setup Guide

This guide will help you set up and test the Datarails Finance OS plugin for Claude Code.

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

Skills are pre-configured in `.claude/skills/` - no additional setup needed.

---

## Step 2: Authenticate with Datarails

### 2.1 Log into Datarails in Your Browser

Open your browser and log into Datarails:
- **Development**: https://dev.datarails.com
- **Production**: https://app.datarails.com

Make sure you're logged in and can see the Datarails dashboard.

### 2.2 Run Authentication

```bash
cd mcp-server
uv run datarails-mcp auth
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

## Step 3: Start Claude Code

```bash
# Make sure you're in the plugin directory
cd /path/to/dr-claude-code-plugins-re

# Start Claude Code
claude
```

---

## Step 4: Test the Plugin

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
cd mcp-server

# Auth to dev (default)
uv run datarails-mcp auth

# Auth to production
uv run datarails-mcp auth --env app

# List all authenticated environments
uv run datarails-mcp auth --list
```

### Query Different Environments

In Claude Code:
```
/dr-tables --env app
/dr-profile 11442 --env dev
```

---

## Reporting Issues

If you encounter problems:

1. **Check authentication status:**
   ```bash
   cd mcp-server && uv run datarails-mcp status --all
   ```

2. **Common issues:**
   - Skills not showing: Restart Claude Code
   - Auth fails: Make sure you're logged into Datarails in browser
   - Tools not working: Check MCP server is running

3. **Report the issue** with:
   - Error message
   - Output of `datarails-mcp status`
   - Steps to reproduce

---

## Quick Reference

```bash
# Setup (one-time)
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
cd mcp-server && uv run datarails-mcp auth && cd ..

# Daily use
cd dr-claude-code-plugins-re
claude

# In Claude Code
/dr-tables
/dr-profile <table_id>
/dr-query <table_id> --sample
```
