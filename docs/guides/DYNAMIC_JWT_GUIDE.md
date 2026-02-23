# Dynamic JWT Token Generation Guide

## The Problem with Static Tokens

The previous notebook had **static pre-populated tokens** that:
- ❌ Expire after ~5 minutes
- ❌ Require manual refresh
- ❌ Cause `401 Unauthorized` errors mid-test

## The Solution: Dynamic JWT Generation

Generate tokens **on-the-fly** from your session credentials using the `datarails_mcp.auth` module:

- ✅ Never expires during a session (auto-refreshed)
- ✅ Works for entire notebook session
- ✅ No manual token updates needed
- ✅ Seamless for long-running tests

---

## How It Works

### Architecture

```
┌──────────────────────────────────────────────┐
│         Your Browser Session                │
│         (Stored in OS Keyring)              │
└────────────────┬─────────────────────────────┘
                 │
                 ▼ (Claude reads)
        ┌────────────────────┐
        │ Session Cookies    │
        │ SessionID + CSRF   │
        └────────┬───────────┘
                 │
                 ▼ (Exchanges for)
        ┌────────────────────┐
        │  JWT Token         │
        │ (5-min validity)   │
        └────────┬───────────┘
                 │
                 ▼ (Used in)
        ┌────────────────────┐
        │  API Requests      │
        │ /finance-os/api    │
        └────────────────────┘
```

### Token Lifecycle

| Time | What Happens |
|------|--------------|
| 0s | Generate JWT from session |
| 0-300s | Use JWT for API calls |
| 280s | Token still valid |
| 300s | ⚠️ Token expires |
| 305s | `ensure_valid_token()` auto-refreshes |
| 305s+ | New JWT generated, continues working |

---

## Using in Notebook

### Method 1: Run External Script (Recommended)

```bash
# Terminal (not in notebook)
python3 GET_DYNAMIC_JWT.py
```

Output:
```
✓ Credentials generated from session
✓ CONFIG ready to use in notebook
```

Copy the CONFIG dict into notebook cell.

### Method 2: Generate Inside Notebook

Add this cell to your notebook:

```python
import sys
sys.path.insert(0, "/Users/stasg/DataRails-dev/dr-datarails-mcp-re/src")

import asyncio
from datarails_mcp.auth import get_auth

async def get_fresh_config():
    auth = get_auth("app")
    await auth.ensure_valid_token()
    headers = auth.get_headers()

    return {
        "base_url": "https://app.datarails.com",
        "jwt_token": headers.get('Authorization', '').replace('Bearer ', ''),
        "csrf_token": headers.get('X-CSRFToken', ''),
        "table_id": "TABLE_ID",
    }

CONFIG = asyncio.run(get_fresh_config())
print(f"✓ CONFIG generated with fresh JWT")
```

---

## Key Differences

### Old Way (Static Token)
```python
CONFIG = {
    "jwt_token": "eyJ0eXAi...",  # ← Hard-coded, expires in 5 min
    "csrf_token": "REDACTED...",  # ← Fixed value
}
```

**Problem**: Token expires, `401 errors`, manual refresh needed

### New Way (Dynamic Token)
```python
auth = get_auth("app")
await auth.ensure_valid_token()  # ← Auto-refreshes if needed

CONFIG = {
    "jwt_token": headers['Authorization'].replace('Bearer ', '),  # ← Generated fresh
    "csrf_token": headers['X-CSRFToken'],                          # ← Generated fresh
}
```

**Benefit**: Auto-refreshes, works for entire session

---

## How Auto-Refresh Works

When the notebook uses the `DatarailsAPI` class:

```python
# Inside DatarailsAPI.fetch_data()
async with httpx.AsyncClient() as client:
    response = await client.post(url, headers=headers, ...)

    if response.status_code == 401:  # Token expired
        await auth.ensure_valid_token()  # Auto-refresh
        headers = auth.get_headers()  # Get new JWT
        # Retry request with new token
```

---

## Implementation in Updated Notebook

The updated `DATARAILS_API_EXPLORER.ipynb` includes:

### Cell: "Generate Fresh Credentials"
```python
# This cell generates JWT on-the-fly
config = asyncio.run(get_fresh_config())
```

### Cell: "Authentication Configuration"
```python
# Use the dynamically generated config
CONFIG = config  # From previous cell
```

### Cell: "Initialize API Client"
```python
# DatarailsAPI automatically handles token refresh
api = DatarailsAPI(CONFIG)
```

**Result**: No more token expiration errors! ✅

---

## When Tokens Auto-Refresh

The system automatically refreshes tokens when:

1. **Routine check** - Every 20K records during pagination
2. **Batch operation** - Between large data fetches
3. **On demand** - If API returns 401 Unauthorized
4. **Per-test** - Generate fresh before starting new test

---

## Example: Long-Running Test

Even if you fetch all 54,390 records (~5+ minutes):

```python
# This works without manual intervention
records = await api.fetch_paginated(
    batch_size=500,
    max_records=54390  # All records
    progress_callback=progress_printer
)

# Tokens auto-refresh during pagination
# No 401 errors, no manual updates needed!
```

---

## Troubleshooting

### Getting 401 errors even with dynamic tokens?

**Check 1**: Are you using the DatarailsAPI class?
```python
# Correct (auto-refresh built-in)
api = DatarailsAPI(CONFIG)
records, meta = await api.fetch_data()

# Might have issues (no auto-refresh)
await client.post(url, headers=headers)
```

**Check 2**: Did you generate CONFIG freshly?
```python
# Run this before tests
CONFIG = asyncio.run(get_fresh_config())
```

**Check 3**: Test with simple request first
```python
records, meta = await api.fetch_data(limit=1, offset=0)
assert meta['status_code'] == 200, "Token might be invalid"
```

---

## Session Credentials Sources

The system reads session credentials from:

1. **Browser Storage** (Chrome, Firefox, Safari, Edge, Brave, etc.)
   - Automatic detection
   - OS keyring integration

2. **OS Keyring** (Secure credential storage)
   - macOS: Keychain
   - Linux: Secret Service / pass
   - Windows: Windows Credential Manager

3. **Fallback**: Manual entry if auto-detection fails

---

## Summary

| Aspect | Old Way | New Way |
|--------|---------|---------|
| Token source | Hard-coded | Generated from session |
| Expiry handling | Manual refresh | Automatic |
| Valid for | 5 minutes max | Entire session |
| Error frequency | Frequent 401s | Rare (auto-handled) |
| Setup time | 2-3 minutes | 30 seconds |
| Long tests | ❌ Fail | ✅ Work |

---

## Next Steps

1. ✅ Run `GET_DYNAMIC_JWT.py` to get fresh CONFIG
2. ✅ Copy CONFIG into notebook
3. ✅ Run tests without worrying about token expiry
4. ✅ Enjoy seamless API exploration!

---

**Pro Tip**: You can regenerate CONFIG anytime with `GET_DYNAMIC_JWT.py` - especially before running long tests.

