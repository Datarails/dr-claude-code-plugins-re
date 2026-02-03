# Development Guidelines - DataRails Financial Agents

## 🚨 CRITICAL PRINCIPLE: ALWAYS USE FRESH REAL DATA

**RULE #1: NEVER generate reports or artifacts without first fetching fresh data from the live Datarails API.**

### ❌ WHAT NOT TO DO:
```python
# WRONG: Creating placeholder/fake data
excel.add_data([
    ["ARR", "$2.3M"],
    ["Churn", "3.2%"],
    ["Runway", "11.2 months"],
])

# WRONG: Using hardcoded test data
insights = {
    "revenue": 2300000,
    "growth": "23%",
}
```

### ✅ WHAT TO DO:
```python
# CORRECT: Always fetch fresh data first
records = await client.get_sample(table_id, n=50)
data = json.loads(records)

# CORRECT: Analyze the actual data
total_revenue = sum([r.get("Amount", 0) for r in data])
accounts = list(set([r.get("Account") for r in data]))

# CORRECT: Generate reports from analyzed real data
excel.add_data([["Account", "Amount"]])
for account, amount in account_totals.items():
    excel.add_data([[account, amount]])
```

## Workflow for All Agents

### Step 1: Fetch Fresh Data
```python
# Always start with API calls
sample_data = await client.get_sample(table_id, n=50)
records = json.loads(sample_data)

# Or use aggregation for large datasets (NO ROW LIMIT)
agg_data = await client.aggregate(
    table_id=table_id,
    dimensions=["Account_L1", "Department"],
    metrics=[{"field": "Amount", "agg": "SUM"}]
)
```

### Step 2: Analyze Real Data
```python
# Work with what you got
by_account = {}
for record in records:
    account = record.get("Account")
    amount = record.get("Amount") or 0
    by_account[account] = by_account.get(account, 0) + amount
```

### Step 3: Generate Report from Analysis
```python
# Report is based on actual analysis
excel.add_data([["Account", "Total"]])
for account, total in by_account.items():
    excel.add_data([[account, total]])
```

## Key Data Sources

### Financials Table (ID: TABLE_ID)
- Contains: GL transactions, forecast data, actual amounts
- Key fields: `Amount`, `DR_ACC_L1`, `DR_ACC_L2`, `Scenario`, `Cost Center`
- Use for: P&L analysis, account breakdowns, department analysis

### KPI Table (ID: 34298)
- Contains: Key performance metrics
- Key fields: `metric`, `value`, `period`
- Use for: Dashboard data, trend analysis

### Other Tables
- SF_Opps (19792): Sales opportunities
- HeadCount (21649): Employee data
- Invoices (29964): Invoice records

## Authentication Verification

Before generating ANY report, verify connection:
```python
auth = get_auth()
client = DatarailsClient(auth)

# Verify tables exist
tables = json.loads(await client.list_tables())
# Should return 27+ tables

# Verify data access
sample = json.loads(await client.get_sample(table_id, n=1))
# Should return actual records, not empty
```

## Report Generation Checklist

- [ ] Verified authentication to correct environment (app, dev, etc.)
- [ ] Fetched fresh data from API (within last execution)
- [ ] Analyzed actual data (not hardcoded values)
- [ ] Generated report from analysis results
- [ ] Verified file created successfully
- [ ] Tested report can be opened

## Common Mistakes to Avoid

### ❌ Mistake 1: Using cached/old data
```python
# Don't reuse data from previous runs
data_cache = {"revenue": 2300000}  # WRONG
```

### ❌ Mistake 2: Placeholder values
```python
# Don't create fake data
metrics = {
    "arr": "$2.3M",  # Made up
    "churn": "3.2%",  # Guessed
}
```

### ❌ Mistake 3: Hardcoding business logic
```python
# Don't assume data structure
revenue = records[0]["revenue"]  # What if field name is different?
```

### ✅ Correct Approach:
```python
# Always defensive, always real
revenue = sum([r.get("Amount", 0) for r in records if r])
if not revenue:
    print("No data found")
    return
```

## Testing Reports

Every report must pass this test:

```python
def verify_report_has_real_data(excel_path):
    wb = load_workbook(excel_path)
    ws = wb.active

    # Check for actual numbers (not placeholders)
    has_numbers = False
    for row in ws.iter_rows(values_only=True):
        for cell in row:
            if isinstance(cell, (int, float)) and cell != 0:
                has_numbers = True
                break

    assert has_numbers, "Report has no real data!"
    return True
```

## Project Memory

**CRITICAL PRINCIPLE FOR ALL AGENTS:**
- Every artifact (Excel, PowerPoint, PDF) MUST be based on fresh API calls
- Never use placeholder data or hardcoded values
- Always verify data exists before creating reports
- If no data: return error message, don't create fake report
- Data freshness is more important than speed

---

**Added:** 2026-02-03
**Reason:** Prevent inaccurate reports that have no real value
**Priority:** CRITICAL - Apply to all future work
