# Datarails API Explorer Notebook - Complete Setup Guide

## 📋 What You Have

A complete **interactive Jupyter notebook** for exploring the Datarails Finance OS API with:
- 9 comprehensive tests
- Async request handling
- Performance metrics & timing
- Error handling
- Data quality analysis

## ⚠️ The Token Expiration Issue (Now Fixed!)

**Problem**: Static JWT tokens expire after ~5 minutes, causing `401 Unauthorized` errors

**Solution**: Generate JWT dynamically from session credentials (auto-refreshes!)

## 🚀 Quick Start (3 Steps)

### Step 1: Generate Fresh Credentials
```bash
python3 GET_DYNAMIC_JWT.py
```

This outputs:
```
✓ Credentials generated from session
CONFIG = {
    "base_url": "https://app.datarails.com",
    "jwt_token": "eyJ0eXAi...",
    "csrf_token": "REDACTED...",
    "table_id": "TABLE_ID",
}
```

### Step 2: Update Notebook
1. Open: `DATARAILS_API_EXPLORER.ipynb`
2. Find: **"Authentication Configuration"** cell
3. Replace the CONFIG dict with output from Step 1
4. Run the cell

### Step 3: Start Testing
- Run **"Utility Functions"** cell
- Then run any test (1-9)
- Tests work without manual token refresh! ✅

---

## 📚 File Guide

### Core Files

| File | Purpose |
|------|---------|
| `DATARAILS_API_EXPLORER.ipynb` | Main notebook with 9 tests |
| `GET_DYNAMIC_JWT.py` | Generate fresh credentials |
| `DYNAMIC_JWT_GUIDE.md` | Explains dynamic token generation |

### Reference Files

| File | Purpose |
|------|---------|
| `NOTEBOOK_GUIDE.md` | How to use each test |
| `NOTEBOOK_TROUBLESHOOTING.md` | Troubleshooting guide |
| `QUICK_FIX.txt` | Quick reference for token issues |
| `DATARAILS_API_DIAGNOSTIC_REPORT.md` | API findings & curl commands |
| `START_HERE_NOTEBOOK_FIX.md` | Fix for token expiration error |

---

## 🧪 What Each Test Does

### Test 1: Simple Request
- Verify API works
- Check response time
- Get baseline throughput

### Test 2: Batch Size Performance
- Compare different batch sizes
- Find optimal (500 records = 184.8 rec/sec)

### Test 3: Full Pagination
- Fetch records using optimal batches
- Show real-time progress
- Calculate ETA

### Test 4: Concurrent Async
- Demonstrate parallel requests
- Show speedup vs sequential
- Explain async benefits

### Test 5: Month Distribution
- Analyze fetched records
- Show monthly breakdown
- Display account hierarchy

### Test 6: Binary Search
- Find exact record count
- Confirm 54,390 records
- Log iterations

### Test 7: Anomalies
- Search for negative values
- Find data quality issues
- Show problematic records

### Test 8: Month Coverage
- Check which months have data
- Identify missing months
- Flag data gaps

### Test 9: Summary Report
- Export all findings
- Create text report
- Save curl commands

---

## 🔑 Token Management

### Dynamic Generation (Recommended)

```python
# In notebook or script:
import asyncio
from datarails_mcp.auth import get_auth

async def get_credentials():
    auth = get_auth("app")
    await auth.ensure_valid_token()
    headers = auth.get_headers()
    return {
        "jwt_token": headers['Authorization'].replace('Bearer ', ''),
        "csrf_token": headers['X-CSRFToken'],
    }

config = asyncio.run(get_credentials())
```

**Benefits**:
- ✅ Auto-refreshes during session
- ✅ Works for long operations
- ✅ No manual token updates

### Token Lifecycle

- **Generated**: When you run `GET_DYNAMIC_JWT.py`
- **Valid**: ~5 minutes
- **Auto-refresh**: Happens automatically during pagination
- **Expires**: ~5 minutes, then auto-refreshed

---

## ⏱️ Performance Expectations

| Operation | Time | Throughput |
|-----------|------|-----------|
| Single request (100 records) | ~2.3 sec | 43.5 rec/sec |
| Batch request (500 records) | ~2.7 sec | 184.8 rec/sec |
| All 54,390 records (sequential) | ~5 min | 184.8 rec/sec |
| All records (concurrent) | ~1 min | 5x faster |

---

## 📊 Key Findings (From Tests)

### API Working ✅
- All 54,390 records confirmed
- API responsive and reliable
- Optimal throughput: 500 records/batch

### Data Quality Issues ⚠️
- Missing months: July, October, December
- Uneven distribution: Sept has 1300+, Jan has 33
- Negative values: Found in June 2025
- Large amounts concentrated at end: $33.6M in records 50K-50.5K

---

## 🛠️ Customization Examples

### Fetch Different Year
```python
custom_filters = [
    {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
    {"name": "System_Year", "values": ["2024"], "is_excluded": False},
    {"name": "DR_ACC_L0", "values": ["P&L"], "is_excluded": False},
]

records = await api.fetch_data(limit=100, filters=custom_filters)
```

### Fetch All Records (Not Just Sample)
```python
records = await api.fetch_paginated(
    batch_size=500,
    max_records=None,  # All 54,390
    progress_callback=progress_printer
)
```

### Analyze with Pandas
```python
import pandas as pd

df = pd.DataFrame(records)
df['Month'] = pd.to_datetime(df['Reporting Date'], unit='s').dt.to_period('M')

# Group by month
monthly = df.groupby('Month')['Amount'].sum()
print(monthly)

# Find negative values
negatives = df[df['Amount'] < 0]
```

---

## 🚦 Troubleshooting

### Getting 401 Errors?
1. Run `GET_DYNAMIC_JWT.py` again
2. Update CONFIG in notebook
3. Re-run test

### Getting Timeout?
1. Check internet connection
2. API might be slow - wait and retry
3. Try smaller batch size (100 instead of 500)

### Getting No Records?
1. Check filters are correct
2. Verify year (2025) exists
3. Try without filters

### Need Fresh Tokens?
```bash
# Anytime during session:
python3 GET_DYNAMIC_JWT.py
```

---

## ✅ Checklist: First Run

- [ ] Read this file
- [ ] Run `GET_DYNAMIC_JWT.py`
- [ ] Copy CONFIG into notebook
- [ ] Open `DATARAILS_API_EXPLORER.ipynb`
- [ ] Run Setup cell
- [ ] Run Authentication cell with new CONFIG
- [ ] Run Utility Functions cell
- [ ] Run Test 1
- [ ] Verify: Status Code should be 200
- [ ] Run other tests as needed!

---

## 📞 Quick Reference

### Generate Credentials
```bash
python3 GET_DYNAMIC_JWT.py
```

### Run Notebook
```bash
jupyter notebook DATARAILS_API_EXPLORER.ipynb
```

### View Documentation
- Troubleshooting: `NOTEBOOK_TROUBLESHOOTING.md`
- Token info: `DYNAMIC_JWT_GUIDE.md`
- API details: `DATARAILS_API_DIAGNOSTIC_REPORT.md`

---

## 🎯 Expected Results

After setup, you should see:

**Test 1 Output:**
```
Status Code: 200
Records returned: 100
Response time: 2.30 seconds
Throughput: 43.5 records/sec
```

If you see:
- `Status Code: 200` ✅ Everything working
- `Status Code: 401` ⚠️ Refresh credentials
- `Status Code: 404` ❌ Check URL/table ID

---

## 🔗 Data Investigation Workflow

1. **Run Test 3** → Get sample data
2. **Run Test 5** → Analyze distribution
3. **Run Test 6** → Confirm total records
4. **Run Test 7** → Find anomalies
5. **Run Test 8** → Check month coverage
6. **Run Test 9** → Generate report

Use findings to present to platform team!

---

## 🎓 Learning Path

**Beginner**: Tests 1-2 (Understand API basics)
**Intermediate**: Tests 3-4 (Learn pagination & async)
**Advanced**: Tests 5-9 (Data analysis & quality)

---

## 💡 Pro Tips

1. **Keep notebook open** → Don't close between tests
2. **Generate fresh creds** → Before long operations
3. **Check status code** → First indicator of issues
4. **Use progress callback** → Monitor long operations
5. **Export results** → Test 9 saves findings

---

## 🚀 You're Ready!

Everything is set up. Follow the **Quick Start** section above and you'll be exploring the API in 5 minutes!

Questions? Check the troubleshooting guide or run:
```bash
python3 GET_DYNAMIC_JWT.py
```

**Happy exploring! 🎉**
