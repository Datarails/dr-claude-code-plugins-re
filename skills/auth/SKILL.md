---
name: dr-auth
description: Authenticate with Datarails Finance OS using OAuth 2.0. Opens your browser for secure login.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__authenticate
  - mcp__datarails-finance-os__auth_status
  - mcp__datarails-finance-os__disable
argument-hint: "[--env prod|dev|test] [--disable]"
---

# Datarails Authentication

Help the user authenticate with Datarails Finance OS using OAuth 2.0 + PKCE.

## IMPORTANT: If Datarails Tools Are Not Available

If the MCP tools (`auth_status`, `authenticate`, etc.) are not available, fail, or are not found, the Datarails connector is not connected yet. **Do NOT try bash commands, `which` commands, or any workarounds.**

Instead, check if there is a way to suggest the Datarails connector to the user (e.g., via the MCP registry or connector suggestions). If the platform supports showing "Suggested connectors", use that to let the user click **Connect** directly.

If connector suggestions are not available, tell the user:

> The Datarails connector isn't connected yet. To connect:
>
> - **Claude Desktop:** Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Alternatively, go to **Settings > Connectors** to manage connectors.
> - **Claude Code (Terminal):** Run: `claude mcp add --transport http datarails-mcp https://mcp.datarails.com/mcp`
>
> After connecting, come back here and try again.

Then STOP. Do not attempt any other tools or commands until the user has connected.

## How It Works

Authentication uses **OAuth 2.0 Authorization Code + PKCE**:
1. A browser window opens automatically for you to log in
2. After login, tokens are securely stored and auto-refreshed
3. No manual cookie extraction or copy/paste needed

## Workflow

### Step 1: Check Current Status

Call the MCP tool to check if already authenticated:

```
Use: mcp__datarails-finance-os__auth_status
```

### Step 2: If Not Authenticated

Call the authenticate tool to start the OAuth flow:

```
Use: mcp__datarails-finance-os__authenticate
Parameters:
  env: <parsed env, default "prod">
```

This opens the user's browser automatically. The user logs in via the Datarails login page, and tokens are returned to the MCP server via a local callback.

Then verify authentication succeeded:

```
Use: mcp__datarails-finance-os__auth_status
```

### Step 3: If Already Authenticated

Confirm the connection is active and show the environment, organization, and token status.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--env <env>` | Auth server: `prod`, `dev`, `test` | `prod` |
| `--disable` | Revoke tokens and disconnect | — |

## Disconnecting / Switching Environments

To disconnect or switch to a different environment:

1. Run `/dr-auth --disable` (or call `mcp__datarails-finance-os__disable`)
2. Then authenticate to the new environment: `/dr-auth --env <env>`

## Example Interactions

**User: "/dr-auth"**
1. Call `auth_status`
2. If authenticated: "You're connected to Datarails (organization: Acme Corp, environment: prod)"
3. If not: Call `authenticate` → browser opens → verify with `auth_status`

**User: "/dr-auth --env dev"**
1. Call `authenticate` with `env: "dev"`
2. Browser opens for dev login
3. Verify with `auth_status`

**User: "/dr-auth --disable"**
1. Call `disable` to revoke tokens and clear credentials
2. Confirm: "Disconnected from Datarails"

## Auth Status Response

The `auth_status` tool returns:
- `authenticated` — whether connected
- `organization` — the org name
- `environment` — which environment (prod/dev/test)
- `api_url` — the API base URL
- `jwt_expires_in_seconds` — time until JWT expires
- `jwt_expired` — whether the JWT has expired (auto-refreshes)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Browser doesn't open | Check default browser settings; try opening the URL manually |
| "Authentication failed" | Verify your Datarails credentials and try again |
| "Token expired" | Tokens auto-refresh; if persistent, run `/dr-auth` again |
| Need different environment | Run `/dr-auth --disable` then `/dr-auth --env <env>` |
| Callback timeout | Ensure no firewall blocking localhost; try again |
