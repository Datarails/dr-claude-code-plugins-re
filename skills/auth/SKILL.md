---
name: dr-auth
description: Authenticate with Datarails Finance OS. Supports multi-account authentication to dev, demo, testapp, and app environments.
user-invocable: true
allowed-tools:
  - Bash
  - mcp__datarails-finance-os__check_auth_status
argument-hint: "[--env dev|demo|testapp|app] [--list] [--switch <env>] [--logout <env>]"
---

# Datarails Authentication

Help the user authenticate with Datarails Finance OS using the CLI.

## IMPORTANT: Use the CLI for Authentication

**ALWAYS use the `datarails-mcp` CLI command for authentication.** The CLI automatically extracts cookies from the user's browser - no manual JavaScript or copy/paste needed.

## Workflow

### Step 1: Check Current Status

Run this Bash command to check authentication status:

```bash
uvx datarails-finance-os-mcp status
```

Or use the MCP tool: `mcp__datarails-finance-os__check_auth_status`

### Step 2: If Not Authenticated

1. **Ask the user to log into Datarails in their browser first** (e.g., https://dev.datarails.com)

2. **Run the CLI auth command** - it will automatically extract cookies from the browser:

```bash
uvx datarails-finance-os-mcp auth
```

For a specific environment:
```bash
uvx datarails-finance-os-mcp auth --env app
```

3. **Verify it worked:**
```bash
uvx datarails-finance-os-mcp status
```

### Step 3: If Already Authenticated

Confirm the connection is active and show which environment is connected.

## Available Environments

| Environment | URL | Description |
|-------------|-----|-------------|
| `dev` | dev.datarails.com | Development (default) |
| `demo` | demo.datarails.com | Demo |
| `testapp` | testapp.datarails.com | Test App |
| `app` | app.datarails.com | Production |

## CLI Commands

```bash
# Check status
uvx datarails-finance-os-mcp status

# Authenticate (auto-extracts from browser)
uvx datarails-finance-os-mcp auth

# Authenticate to specific environment
uvx datarails-finance-os-mcp auth --env app
uvx datarails-finance-os-mcp auth --env dev
uvx datarails-finance-os-mcp auth --env demo

# List all environments and auth status
uvx datarails-finance-os-mcp auth --list

# Switch active environment
uvx datarails-finance-os-mcp auth --switch app

# Logout from environment
uvx datarails-finance-os-mcp auth --logout dev

# Logout from all
uvx datarails-finance-os-mcp auth --logout-all

# Manual entry (only if automatic fails)
uvx datarails-finance-os-mcp auth --manual
```

## Example Interactions

**User: "/dr-auth"**
1. Run `uvx datarails-finance-os-mcp status`
2. If authenticated: "You're connected to Datarails (dev)"
3. If not: Ask user to log into Datarails in browser, then run `uvx datarails-finance-os-mcp auth`

**User: "/dr-auth --list"**
Run: `uvx datarails-finance-os-mcp auth --list`

**User: "/dr-auth --env app"**
1. Ask user to log into https://app.datarails.com in browser
2. Run: `uvx datarails-finance-os-mcp auth --env app`
3. Verify: `uvx datarails-finance-os-mcp status`

**User: "/dr-auth --switch app"**
Run: `uvx datarails-finance-os-mcp auth --switch app`

**User: "/dr-auth --logout dev"**
Run: `uvx datarails-finance-os-mcp auth --logout dev`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No browser cookies found" | User must log into Datarails in browser first |
| "Browser may be locked" | Close the browser and try again |
| "Cookie decryption failed" | Grant keychain access (macOS) or try `--manual` |
| Wrong environment | Specify with `--env` flag |

**If automatic extraction fails**, use manual mode:
```bash
uvx datarails-finance-os-mcp auth --manual
```
Then user copies cookies from DevTools (F12 > Application > Cookies).
