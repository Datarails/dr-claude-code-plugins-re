---
description: Connect to Datarails - simple browser-based login (no terminal required)
---

# Connect to Datarails

Help the user connect to their Datarails account using browser-based authentication. This is the Cowork-friendly login flow - no terminal or CLI required.

## Step 1: Check Current Status

First, check if already connected:

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If authenticated:** Tell the user they're already connected and ask what they'd like to do.

**If not authenticated:** Continue to Step 2.

## Step 2: Guide Browser Login

Tell the user:

> To connect your Datarails account, I need you to:
>
> 1. **Open Datarails** in a new browser tab: https://app.datarails.com
> 2. **Log in** with your credentials
> 3. **Stay on that page** after logging in
>
> Let me know when you're logged in and I'll help you complete the connection.

## Step 3: Get Cookie Extraction Script

When user confirms they're logged in:

```
Use: mcp__datarails-finance-os__get_cookie_extraction_script
```

This returns JavaScript code and instructions.

## Step 4: Guide Cookie Extraction

Tell the user:

> Great! Now I need to securely connect to your session. Here's how:
>
> 1. On the Datarails page, **press F12** (or right-click → Inspect) to open Developer Tools
> 2. Click the **Console** tab
> 3. **Paste this code** and press Enter:
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
>   return { sessionid: cookies.sessionid, csrftoken: cookies.csrftoken };
> })();
> ```
>
> 4. **Copy the two values** that appear (Session ID and CSRF Token)
> 5. **Paste them here** and I'll complete the connection

## Step 5: Store Credentials

When user provides the session_id and csrf_token values:

```
Use: mcp__datarails-finance-os__set_auth_cookies
Parameters:
  session_id: <the sessionid value user provided>
  csrf_token: <the csrftoken value user provided>
```

## Step 6: Verify Connection

After storing cookies:

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If successful:**

> You're now connected to Datarails! Your session will stay active for several days.
>
> Here's what you can do:
> - `/datarails-finance-os:financial-summary` - Get a quick overview of your finances
> - `/datarails-finance-os:expense-analysis` - Analyze your expenses
> - `/datarails-finance-os:revenue-trends` - See revenue trends
> - `/datarails-finance-os:data-check` - Check data quality
>
> What would you like to explore?

**If failed:** Ask user to try again, making sure they copied the correct values.

## Troubleshooting

**"sessionid is undefined"**
- User may not be fully logged in
- Ask them to refresh the Datarails page and try again

**"cookies.sessionid is empty"**
- Browser may be blocking cookies
- Ask user to check they're on the correct domain (app.datarails.com)

**Connection expires**
- Session cookies last days/weeks
- If expired, just run `/datarails-finance-os:login` again
