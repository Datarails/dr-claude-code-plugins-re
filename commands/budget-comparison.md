---
description: Compare actual results to budget - see where you're over or under plan using complete aggregated data
---

# Budget vs Actual Comparison

Compare your actual financial results against budget using real aggregated totals to identify variances and understand performance.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify the financials table that contains both Actuals and Budget scenarios.

## Step 3: Understand the Structure

```
Use: mcp__datarails-finance-os__get_table_schema
Parameters:
  table_id: <financials_table_id>
```

Identify key fields: Scenario, Amount, Account hierarchy, Date.

## Step 4: Get Actuals Totals via Aggregation

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

## Step 5: Get Budget Totals via Aggregation

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Budget"], "is_excluded": false}
  ]
```

Both calls complete in ~5 seconds each, giving complete totals for both scenarios.

## Step 6: Get Monthly Breakdown (Optional Detail)

For a month-by-month comparison:

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<date_field>", "<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals", "Budget"], "is_excluded": false}
  ]
```

Note: You may need to split this into two calls (one for Actuals, one for Budget) and merge the results.

## Step 7: Analyze Variances

Compare actuals to budget by:
- Account category
- Calculate dollar variance (Actual - Budget)
- Calculate percentage variance ((Actual - Budget) / Budget * 100)

## Step 8: Present Comparison

Create a clear variance report with real totals:

> ## Budget vs Actual Analysis
>
> ### Summary
> - **Period:** [time range covered]
> - **Overall status:** [Over/Under/On budget]
>
> ### High-Level Comparison (Complete Totals)
>
> | Category | Actual | Budget | Variance | % Var |
> |----------|--------|--------|----------|-------|
> | Revenue | $X | $Y | $Z | +/-W% |
> | COGS | $X | $Y | $Z | +/-W% |
> | Gross Profit | $X | $Y | $Z | +/-W% |
> | Operating Expenses | $X | $Y | $Z | +/-W% |
> | Net Income | $X | $Y | $Z | +/-W% |
>
> ### Favorable Variances (Good News)
> Areas performing better than planned:
> - [Category]: $[amount] under budget ([X]%)
> - [Category]: $[amount] above plan ([X]%)
>
> ### Unfavorable Variances (Needs Attention)
> Areas not meeting plan:
> - [Category]: $[amount] over budget ([X]%)
> - [Category]: $[amount] below plan ([X]%)
>
> ### Key Insights
> 1. **Biggest positive:** [description]
> 2. **Biggest concern:** [description]
> 3. **Trend observation:** [description]
>
> ### Recommended Actions
> - [Action based on largest unfavorable variance]
> - [Action based on positive variance opportunity]

## Variance Thresholds

Flag variances that matter:

| Variance % | Flag | Meaning |
|------------|------|---------|
| > 20% | Critical | Significant deviation, investigate immediately |
| 10-20% | Warning | Notable variance, review soon |
| 5-10% | Watch | Minor variance, monitor |
| < 5% | Normal | Within acceptable range |

## Handling Missing Budget Data

**If no Budget scenario exists:**
> I found Actuals data but couldn't locate Budget data in your financials table.
>
> The available scenarios are: [list them]
>
> Options:
> - Would you like me to compare against a different scenario (like Forecast)?
> - Or should I just show you the Actuals breakdown?

**If Budget data is incomplete:**
> Budget data exists but doesn't cover all categories that Actuals covers.
>
> I can:
> - Compare only the overlapping categories
> - Show you where budget data is missing

## Handling Aggregation Failures

If aggregation fails for a specific field:
1. Try a different account hierarchy field
2. If all aggregation fails, fall back to `get_records_by_filter` (500-row limit per scenario) and note the comparison is based on partial data

## Department-Level Analysis

If the user wants department-level variances, run additional aggregation:

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<department_field>", "<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

## Follow-up Questions

After the analysis, offer:
- "Why is [category] over budget?"
- "Show me the monthly trend for the largest variance"
- "Which department is driving the variance?"
- "Compare against Forecast instead of Budget?"
