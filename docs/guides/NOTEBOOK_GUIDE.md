# Jupyter Notebook Guide: Datarails API Explorer

## Quick Start

### 1. Open the Notebook
```bash
jupyter notebook DATARAILS_API_EXPLORER.ipynb
```

### 2. Run Cells in Order
- Start with **Setup** cell to install dependencies
- Then **Authentication Configuration** (credentials are pre-populated)
- Then **Utility Functions**
- Finally, run individual tests as needed

---

## What Each Test Does

### ✅ Test 1: Simple Single Request
- Fetches 100 records from offset 0
- Shows response time and throughput
- Useful for: Quick verification that API is working

### ✅ Test 2: Batch Size Performance
- Tests batch sizes: 50, 100, 250, 500
- Compares throughput for each
- **Finding**: 500-record batches are optimal (184.8 rec/sec)

### ✅ Test 3: Full Pagination with Progress
- Fetches all records using optimal batch size
- Shows real-time progress updates
- Calculates ETA for remaining records
- **Change `max_records=3000`** to fetch more (or all 54,390)

### ✅ Test 4: Concurrent Async Requests
- Demonstrates async/concurrent request handling
- Fetches 5 different offsets in parallel
- Shows speedup vs sequential
- **Important**: Shows Datarails API is sync, async just speeds up fetching

### ✅ Test 5: Month Distribution Analysis
- Analyzes the 3000 records from Test 3
- Shows records and amounts by month
- Shows accounts (L1 hierarchy)
- Reveals data distribution problems

### ✅ Test 6: Binary Search for Total Count
- Finds the exact last record offset
- Confirms extraction script's 54,390 count
- Takes ~17 requests (log₂ 100,000)
- **Result**: Last record confirmed at offset 54,389

### ✅ Test 7: Anomalies Detection
- Searches records 40K-40.5K for negative values
- Shows top 5 negative entries
- **Finding**: Found -$173K (data quality issue)

### ✅ Test 8: Month Coverage Check
- Samples 10 batches to find which months have data
- Shows missing months
- **Finding**: July, October, December missing

### ✅ Test 9: Summary Report
- Exports all findings
- Creates text report
- Saves curl commands for reference

---

## Key Features

### ✨ Pre-Populated Credentials
```python
CONFIG = {
    "base_url": "https://app.datarails.com",
    "jwt_token": "eyJ0eXAi...",  # Valid ~5 minutes
    "csrf_token": "REDACTED...",
    "table_id": "TABLE_ID"
}
```

### ⏱️ Timing Information Included
Every request shows:
- Response time (seconds)
- Throughput (records/sec)
- Timestamps
- ETAs for full data fetch

### 🔄 Async Handling
```python
# The API client automatically handles:
records, metadata = await api.fetch_data(limit=500, offset=0)
# Returns immediately with:
# - records: list of data
# - metadata: timing, status, throughput info
```

### 📊 Progress Tracking
```python
def progress_printer(progress):
    print(f"Batch {progress['batch']} | {progress['batch_size']} records | "
          f"{progress['throughput']:.1f} rec/sec | ETA: {eta_seconds}s")

records = await api.fetch_paginated(
    batch_size=500,
    max_records=3000,
    progress_callback=progress_printer
)
```

---

## Important Notes

### Token Expiration
- Credentials expire in ~5 minutes
- If you get 401 errors: Generate new credentials by running the cell again
- Or use: `await api.fetch_data()` which will auto-handle expiration

### Data Issues Found
1. **Uneven distribution**: September has 904 records out of first 1000
2. **Missing months**: July, October, December have 0 records
3. **Negative values**: Found in June 2025 (records 40K-40.5K)
4. **Wrong ordering**: Data not sorted by date

### Async Behavior
- The Datarails API itself is **synchronous** (returns immediately)
- Async is used for **concurrent requests** (multiple batches in parallel)
- `await` syntax simply waits for network response
- No polling loops needed

---

## Customization Examples

### Fetch Different Time Period
```python
# Change to 2024 Actuals
custom_filters = [
    {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
    {"name": "System_Year", "values": ["2024"], "is_excluded": False},
    {"name": "DR_ACC_L0", "values": ["P&L"], "is_excluded": False},
]

records, metadata = await api.fetch_data(
    limit=100,
    filters=custom_filters
)
```

### Fetch All Records (Not Just Sample)
```python
# Change max_records parameter
records, metadata = await api.fetch_paginated(
    batch_size=500,
    max_records=None,  # Fetch ALL 54,390
    progress_callback=progress_printer
)
# This will take ~5 minutes
```

### Real-Time Data Analysis
```python
# After fetching records, analyze in real-time:
df = pd.DataFrame(records)

# By month
df['Month'] = pd.to_datetime(df['Reporting Date'], unit='s').dt.to_period('M')
print(df.groupby('Month')['Amount'].sum())

# By account
print(df.groupby('DR_ACC_L1')['Amount'].sum())

# Negative values
print(df[df['Amount'] < 0])
```

---

## Output Files

The notebook creates these files:
- `/tmp/datarails_api_test_summary.txt` - Summary report
- `/tmp/datarails_curl_commands.sh` - Curl commands for manual testing

---

## Troubleshooting

### Getting 401 Unauthorized
```
Solution: Run the Authentication Configuration cell again to get fresh token
```

### Timeout errors
```
Solution: Increase timeout in fetch_data() or check network
```

### No data returned
```
Solution: Check filters are correct, try 2024 data instead
```

### Want to use curl directly?
```
# Find the commands at the bottom of the notebook
# Or check: /tmp/datarails_curl_commands.sh
```

---

## Next Steps

1. **Review the findings** from each test
2. **Compare with** the diagnostic report (DATARAILS_API_DIAGNOSTIC_REPORT.md)
3. **Present to platform team** with specific evidence:
   - Binary search proof of 54,390 records
   - Sample negative values
   - Missing month statistics
4. **Ask them** to investigate the data quality issues

---

**Status**: ✅ Ready to use
**Credentials**: ✅ Pre-populated
**Async handling**: ✅ Fully supported
**Timing info**: ✅ Included in all tests
