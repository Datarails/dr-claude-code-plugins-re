---
description: Test API field compatibility and performance - discover which fields work with aggregation and update your profile
---

# API Diagnostic Test

Run a quick diagnostic to test which fields work with the aggregation API in your environment. Results are used to optimize all other commands for speed.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify the main financials table.

## Step 3: Get Table Schema

```
Use: mcp__datarails-finance-os__get_table_schema
Parameters:
  table_id: <financials_table_id>
```

Identify key fields to test:
- Account hierarchy fields (L0, L1, L1.5, L2, etc.)
- Date field
- Scenario field
- Department/Cost Center fields
- Any other categorical fields

## Step 4: Test Each Field with Aggregation

For each key field, run a simple aggregation test:

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<field_to_test>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

**For each field, record:**
- PASS: Returns data successfully (note group count and timing)
- FAIL: Returns error (500, timeout, etc.)

Test these fields in order:
1. Scenario field
2. Date field
3. Account L0 field
4. Account L1 field
5. Account L2 field
6. Any L1.5 or alternative account fields
7. Department/Cost Center fields
8. Other categorical fields

## Step 5: Present Results

Show a clear diagnostic report:

> ## API Diagnostic Results
>
> **Environment:** [name]
> **Table:** [name] (ID: [id])
>
> ### Aggregation Field Tests
> | Field | Status | Groups | Notes |
> |-------|--------|--------|-------|
> | Scenario | PASS | 4 | Works |
> | Reporting Date | PASS | 101 | Works |
> | DR_ACC_L0 | PASS | 5 | Works |
> | DR_ACC_L1 | FAIL | - | 500 error |
> | DR_ACC_L2 | FAIL | - | 500 error |
> | DR_ACC_L1.5 | PASS | 18 | Alternative for L1/L2 |
> | Department L1 | PASS | 3 | Works |
> | Cost Center | PASS | 24 | Works |
>
> ### Summary
> - **[X]/[Y] fields work** ([Z]%)
> - **Recommended alternatives:**
>   - Use [field A] instead of [field B]
>
> ### What This Means
> - Commands like `/datarails-finance-os:financial-summary` will use working fields for fast (~5s) results
> - Fields that fail will use alternative fields or fall back to slower pagination
>
> ### Next Steps
> - These results should be saved to your client profile
> - Run `/dr-learn` to auto-save these results
> - Re-run this test any time after Datarails platform updates

## Tips

- Each test takes about 5 seconds
- Testing 8 fields takes about 40 seconds total
- If ALL fields fail, the aggregation API may not work in your environment
- Results help optimize all financial commands and skills
