---
description: Connect to Datarails - secure OAuth login (opens your browser automatically)
---

# Connect to Datarails

Help the user connect to their Datarails account using OAuth 2.0 authentication.

## What To Do Now

Call the `auth_status` tool to see if the user is already connected:

```
Use: mcp__datarails-finance-os__auth_status
```

**If authenticated:** Tell the user they're already connected, show the organization and environment, and suggest these commands:
- `/datarails-finance-os:financial-summary` - Quick overview of your finances
- `/datarails-finance-os:expense-analysis` - Analyze your expenses
- `/datarails-finance-os:revenue-trends` - See revenue trends
- `/datarails-finance-os:data-check` - Check data quality

Then STOP. Do not call any other tools.

**If not authenticated:** Call the authenticate tool to start the OAuth flow:

```
Use: mcp__datarails-finance-os__authenticate
Parameters:
  env: "prod"
```

Tell the user:

> Connecting to Datarails... A browser window will open for you to log in.
>
> Once you've logged in, you'll be automatically connected.

IMPORTANT: After calling authenticate, verify the connection:

```
Use: mcp__datarails-finance-os__auth_status
```

If successful, tell the user they're connected and suggest the commands listed above.

If failed, ask the user to try again or check their Datarails credentials.

## Troubleshooting

If the browser doesn't open: Ask the user to check their default browser settings.

If authentication times out: Ask the user to try running the login command again.

If the user needs a different environment: Guide them to specify the environment (e.g., "Connect to Datarails dev environment").
