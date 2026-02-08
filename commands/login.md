---
description: Connect to Datarails - simple browser-based login (no terminal required)
---

# Connect to Datarails

Help the user connect to their Datarails account using browser-based authentication.

## What To Do Now

Call the `check_auth_status` tool to see if the user is already connected:

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If authenticated:** Tell the user they're already connected, show the environment name, and suggest these commands:
- `/datarails-finance-os:financial-summary` - Quick overview of your finances
- `/datarails-finance-os:expense-analysis` - Analyze your expenses
- `/datarails-finance-os:revenue-trends` - See revenue trends
- `/datarails-finance-os:data-check` - Check data quality

Then STOP. Do not call any other tools.

**If not authenticated:** Show the user these instructions and then STOP. Do NOT call any other tools after this - wait for the user to reply.

Tell the user:

> You're not connected to Datarails yet. Here's how to connect:
>
> **1. Log into Datarails** in a new browser tab at https://app.datarails.com
>
> **2. Extract your session cookies** - once logged in, press F12 to open Developer Tools, click the Console tab, and paste this code:
>
> ```javascript
> (function() {
>   const cookies = document.cookie.split(';').reduce((acc, c) => {
>     const [key, val] = c.trim().split('=');
>     acc[key] = val;
>     return acc;
>   }, {});
>   console.log('Session ID:', cookies.sessionid);
>   console.log('CSRF Token:', cookies.csrftoken);
> })();
> ```
>
> **3. Copy and paste both values here** (the Session ID and CSRF Token that appear in the console).

IMPORTANT: After showing these instructions, STOP and wait for the user to reply with their cookie values. Do NOT call any more tools until the user provides their session_id and csrf_token.

## When The User Provides Cookie Values

When the user replies with their session_id and csrf_token values, store them:

```
Use: mcp__datarails-finance-os__set_auth_cookies
Parameters:
  session_id: <the sessionid value>
  csrf_token: <the csrftoken value>
```

Then verify the connection:

```
Use: mcp__datarails-finance-os__check_auth_status
```

If successful, tell the user they're connected and suggest the commands listed above.

If failed, ask the user to double-check they copied the correct values and try again.

## Troubleshooting

If the user says "sessionid is undefined": they may not be fully logged in. Ask them to refresh the Datarails page and try the JavaScript again.

If the user says "cookies.sessionid is empty": browser may be blocking cookies. Ask them to check they're on app.datarails.com (not a different subdomain).
