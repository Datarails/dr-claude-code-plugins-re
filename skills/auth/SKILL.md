---
name: dr-auth
description: Authenticate with Datarails Finance OS. Supports multi-account authentication to dev, demo, testapp, and app environments.
user-invocable: true
allowed-tools:
  - Bash
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__set_auth_cookies
  - mcp__datarails-finance-os__get_cookie_extraction_script
  - mcp__datarails-finance-os__clear_auth_cookies
argument-hint: "[--env dev|demo|testapp|app] [--list] [--switch <env>] [--logout <env>] [--manual]"
---

# Datarails Authentication

Help the user authenticate with Datarails Finance OS. Supports multi-account authentication to multiple environments.

## Available Environments

| Environment | URL | Description |
|-------------|-----|-------------|
| `dev` | dev.datarails.com | Development (default) |
| `demo` | demo.datarails.com | Demo |
| `testapp` | testapp.datarails.com | Test App |
| `app` | app.datarails.com | Production |

## Workflow

### Step 1: Check Current Status

First, check the current authentication status using `mcp__datarails-finance-os__check_auth_status`.

### Step 2: Handle Based on Request

**List all environments (--list):**
```bash
datarails-mcp auth --list
```
Shows all environments with their authentication status.

**Switch active environment (--switch):**
```bash
datarails-mcp auth --switch app
```
Changes the active environment (no re-auth if already authenticated).

**Logout from environment (--logout):**
```bash
datarails-mcp auth --logout dev
```
Clears credentials for specific environment.

**Authenticate to environment:**
```bash
datarails-mcp auth                    # Active environment (default: dev)
datarails-mcp auth --env app          # Production
datarails-mcp auth --env demo         # Demo
datarails-mcp auth --manual           # Manual cookie entry
```

### Step 3: Authentication Flow

1. Ask the user to log into Datarails in their browser
2. Run `datarails-mcp auth --env <env>`
3. If CLI doesn't work, offer manual cookie extraction:
   - Get the extraction script with `mcp__datarails-finance-os__get_cookie_extraction_script`
   - Guide user to paste cookies
   - Use `mcp__datarails-finance-os__set_auth_cookies` to store them
4. Verify authentication succeeded

## Arguments

| Argument | Description |
|----------|-------------|
| `--env <env>` | Authenticate to specific environment (dev, demo, testapp, app) |
| `--list` | List all environments and their auth status |
| `--switch <env>` | Switch active environment |
| `--logout <env>` | Clear credentials for specific environment |
| `--logout-all` | Clear credentials for all environments |
| `--manual` | Skip automatic extraction, use manual cookie entry |

## Example Interactions

**User: "/dr-auth"**
1. Check status -> Show active environment status
2. If not authenticated, guide through auth flow

**User: "/dr-auth --list"**
```
Datarails Environments
==================================================

| Status | Name   | Display     | URL                           |
|--------|--------|-------------|-------------------------------|
| ✓      | dev    | Development | https://dev.datarails.com     |
| ✓      | app    | Production  | https://app.datarails.com     |
| ✗      | demo   | Demo        | https://demo.datarails.com    |
| ✗      | testapp| Test App    | https://testapp.datarails.com |

2 of 4 environments authenticated
```

**User: "/dr-auth --env app"**
1. Check current status for app environment
2. Run `datarails-mcp auth --env app`
3. Verify -> "Successfully connected to Datarails (Production)"

**User: "/dr-auth --switch app"**
1. Run `datarails-mcp auth --switch app`
2. Confirm -> "Switched active environment to Production (app)"

**User: "/dr-auth --logout dev"**
1. Run `datarails-mcp auth --logout dev`
2. Confirm -> "Logged out of Development (dev)"

## Commands Summary

```bash
# List all environments
datarails-mcp auth --list

# Authenticate to environment
datarails-mcp auth --env dev
datarails-mcp auth --env app
datarails-mcp auth --env demo
datarails-mcp auth --env testapp

# Switch active environment
datarails-mcp auth --switch app

# Logout
datarails-mcp auth --logout dev
datarails-mcp auth --logout-all

# Manual authentication
datarails-mcp auth --manual

# Check status
datarails-mcp status
datarails-mcp status --all
datarails-mcp status --env app
```

## Troubleshooting

If automatic auth fails:
1. Ensure user is logged into Datarails in browser (correct environment!)
2. Try `datarails-mcp auth --manual`
3. If still failing, guide through DevTools cookie extraction:
   - Open Datarails in browser
   - Open DevTools (F12) -> Application -> Cookies
   - Copy `sessionid` and `csrftoken` values
   - Use `set_auth_cookies` MCP tool

## Error Messages

| Error | Solution |
|-------|----------|
| "No browser cookies found" | User needs to log into Datarails in browser first |
| "Session expired" | Re-run authentication for that environment |
| "Invalid credentials" | Clear cookies with --logout and re-authenticate |
| "Not authenticated to <env>" | Run auth with --env flag for that environment |
