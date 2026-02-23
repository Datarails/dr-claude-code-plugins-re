# Jupyter Notebook Troubleshooting Guide

## Error: `KeyError: 'records_returned'`

This error occurs when the API request fails, typically because the **authentication token has expired**.

### Root Cause
- JWT tokens are valid for ~5 minutes
- CSRF tokens may also expire
- If either expires, API returns **401 Unauthorized**
- The error handling wasn't catching this properly

### Solution: Refresh Credentials

#### Option 1: Quick Fix in Notebook (Easiest)

1. Open terminal
2. Run this Python command:
   ```bash
   python3 << 'EOF'
   import sys
   sys.path.insert(0, "/Users/stasg/DataRails-dev/dr-claude-code-plugins-re/src (in dr-datarails-mcp-re repo)")
   import asyncio
   from datarails_mcp.auth import get_auth

   async def refresh():
       auth = get_auth("app")
       await auth.ensure_valid_token()
       headers = auth.get_headers()
       jwt = headers.get('Authorization', '').replace('Bearer ', '')
       csrf = headers.get('X-CSRFToken', '')
       print(f"JWT_TOKEN = '{jwt}'")
       print(f"CSRF_TOKEN = '{csrf}'")

   asyncio.run(refresh())
   EOF
   ```

3. Copy the output `JWT_TOKEN` and `CSRF_TOKEN`

4. In the notebook, go to **Authentication Configuration** cell

5. Replace the values:
   ```python
   CONFIG = {
       "base_url": "https://app.datarails.com",
       "jwt_token": "PASTE_NEW_JWT_HERE",      # ← Replace
       "csrf_token": "PASTE_NEW_CSRF_HERE",    # ← Replace
       "table_id": "16528",
   }
   ```

6. Re-run the **Utility Functions** cell to reinitialize the API client:
   ```python
   api = DatarailsAPI(CONFIG)
   print("✓ DatarailsAPI client reinitialized")
   ```

7. Now run your test cell again - it should work!

#### Option 2: Run Python Script
```bash
cd /Users/stasg/DataRails-dev/dr-claude-code-plugins-re
python3 REFRESH_CREDENTIALS.py
```

This will print new credentials to use.

---

## How to Avoid Token Expiration

### Don't Close Jupyter for Long Periods
- Keep the notebook running
- Run tests within ~5 minutes of starting
- If you take a break, refresh credentials when you return

### Before Long Operations
If you're about to run a long test (like fetching all 54,390 records):
1. Refresh credentials first
2. Tokens refresh automatically as you go, so long operations usually work fine

### After 5-10 Minutes
If tests start failing with 401 errors:
1. Immediately refresh credentials
2. Reinitialize the API client
3. Continue testing

---

## Better Error Handling (Updated Notebook)

The updated Test 1 cell now includes error handling:

```python
if metadata['status_code'] != 200:
    print(f"❌ ERROR: HTTP {metadata['status_code']}")
    if metadata['status_code'] == 401:
        print("Token expired - run the REFRESH CREDENTIALS cell above")
else:
    # Success - show results
    print(f"Records: {metadata['records_returned']}")
```

This prevents the `KeyError` and shows helpful error messages instead.

---

## Token Expiration Timeline

| Time | Status | Action |
|------|--------|--------|
| 0-5 min | ✅ Valid | Use normally |
| 5+ min | ⚠️ Expired | Refresh credentials |
| After refresh | ✅ Valid | Ready to use (~5 min) |

---

## Verification: Did It Work?

After refreshing credentials, run this simple test:

```python
records, metadata = await api.fetch_data(limit=10, offset=0)

if metadata['status_code'] == 200:
    print(f"✓ SUCCESS! Got {len(records)} records")
else:
    print(f"✗ Still failing with status {metadata['status_code']}")
```

If you see `✓ SUCCESS`, you're ready to run all the other tests!

---

## Common Issues

### Issue: Still getting 401 after refresh
**Solution:**
- Make sure you updated CONFIG dict correctly
- Make sure you ran the API reinitialize cell
- Try refreshing credentials again

### Issue: API works then suddenly fails
**Solution:**
- Token expired during test
- Refresh credentials
- Resume testing

### Issue: "Module not found" error
**Solution:**
- Missing dependencies
- Run the Setup cell at the top of the notebook
- Install httpx if needed: `pip install httpx`

---

## Quick Checklist

- [ ] Open Jupyter notebook
- [ ] Run Setup cell
- [ ] Run Authentication Configuration cell
- [ ] Run Utility Functions cell
- [ ] Try Test 1
- [ ] If 401 error → Follow "Option 1: Quick Fix" above
- [ ] Verify with the test at bottom of this guide
- [ ] Run other tests!

---

**You're now ready to explore the Datarails API!** 🚀
