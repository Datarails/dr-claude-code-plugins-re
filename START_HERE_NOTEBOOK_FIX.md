# Notebook Fix: Token Expiration Error

## What Went Wrong
You got a `KeyError: 'records_returned'` error because the authentication token **expired** (valid only ~5 minutes).

## How to Fix It (Quick)

### Step 1: Get Fresh Credentials
Copy and paste this into your terminal:

```bash
python3 << 'EOF'
import sys
sys.path.insert(0, "/Users/stasg/DataRails-dev/dr-claude-code-plugins-re/mcp-server/src")
import asyncio
from datarails_mcp.auth import get_auth

async def refresh():
    auth = get_auth("app")
    await auth.ensure_valid_token()
    headers = auth.get_headers()
    jwt = headers.get('Authorization', '').replace('Bearer ', '')
    csrf = headers.get('X-CSRFToken', '')
    print("Copy these values:")
    print(f"\nJWT_TOKEN:\n{jwt}")
    print(f"\nCSRF_TOKEN:\n{csrf}")

asyncio.run(refresh())
EOF
```

### Step 2: Update Notebook
1. Open `DATARAILS_API_EXPLORER.ipynb`
2. Find the **"Authentication Configuration"** cell
3. Replace:
   - `jwt_token` with the JWT_TOKEN from above
   - `csrf_token` with the CSRF_TOKEN from above
4. Run the cell (Shift+Enter)

### Step 3: Reinitialize API Client
Run this cell:
```python
api = DatarailsAPI(CONFIG)
print("✓ API client reinitialized")
```

### Step 4: Test It
Run Test 1 again - should work now!

---

## Files Created

| File | Purpose |
|------|---------|
| `DATARAILS_API_EXPLORER.ipynb` | Main interactive notebook with 9 tests |
| `NOTEBOOK_TROUBLESHOOTING.md` | Detailed troubleshooting guide |
| `NOTEBOOK_GUIDE.md` | How to use each test |
| `QUICK_FIX.txt` | This quick fix guide |
| `REFRESH_CREDENTIALS.py` | Python script to get new credentials |

---

## Understanding the Issue

### Token Lifecycle
- **Generated**: When you authenticate
- **Valid for**: ~5 minutes
- **After expiry**: API returns 401 Unauthorized
- **Fix**: Get new token, update config, continue

### This is Normal!
- Tokens are designed to expire for security
- Refreshing is quick (1-2 minutes)
- After refresh, token is valid for another ~5 minutes

---

## Best Practices

1. **Keep notebook open** - Don't close and reopen frequently
2. **Run tests within 5 minutes** - Avoid token expiry
3. **Before long operations** - Refresh credentials first
4. **If tests fail** - Check error message, refresh if 401

---

## What's Next

After fixing the token issue:

1. ✅ Run Test 1 (Simple request)
2. ✅ Run Test 2 (Batch size comparison)
3. ✅ Run Test 3 (Full pagination)
4. ✅ Run Test 4 (Concurrent requests)
5. ✅ Run Test 5 (Data analysis)
6. ✅ Run Test 6 (Binary search)
7. ✅ Run Test 7 (Anomalies)
8. ✅ Run Test 8 (Month coverage)
9. ✅ Run Test 9 (Summary report)

Each test shows different aspects of the Datarails API and data quality.

---

## Need More Help?

See: `NOTEBOOK_TROUBLESHOOTING.md` - Comprehensive guide for all issues

---

**Ready to explore?** 🚀 Follow the steps above and you'll be back on track in 2 minutes!
