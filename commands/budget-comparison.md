---
description: Compare actual results to budget - see where you're over or under plan
---

# Budget vs Actual Comparison

Compare your actual financial results against budget to identify variances and understand performance.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify the financials table that contains both Actuals and Budget scenarios.

## Step 3: Check Available Scenarios

```
Use: mcp__datarails-finance-os__get_field_distinct_values
Parameters:
  table_id: <financials_table_id>
  field_name: "Scenario"
  limit: 20
```

Look for: Actuals, Budget, Forecast, Plan, etc.

## Step 4: Fetch Actuals Data

```
Use: mcp__datarails-finance-os__get_records_by_filter
Parameters:
  table_id: <financials_table_id>
  filters: {"Scenario": "Actuals"}
  limit: 500
```

## Step 5: Fetch Budget Data

```
Use: mcp__datarails-finance-os__get_records_by_filter
Parameters:
  table_id: <financials_table_id>
  filters: {"Scenario": "Budget"}
  limit: 500
```

## Step 6: Analyze Variances

Compare actuals to budget by:
- Account category
- Department/Cost Center (if available)
- Time period

Calculate:
- Dollar variance (Actual - Budget)
- Percentage variance ((Actual - Budget) / Budget * 100)

## Step 7: Present Comparison

Create a clear variance report:

> ## Budget vs Actual Analysis
>
> ### Summary
> - **Period:** [time range]
> - **Overall status:** [Over/Under/On budget]
>
> ### High-Level Comparison
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
> Budget data exists but doesn't cover all periods/accounts that Actuals covers.
>
> I can:
> - Compare only the overlapping data
> - Show you where budget data is missing

## Department-Level Analysis

If cost center/department data is available, offer:

> I can also break this down by department. Would you like to see:
> - Which departments are over/under budget?
> - A specific department's performance?

## Follow-up Questions

After the analysis, offer:
- "Why is [category] over budget?"
- "Show me the details for [specific line item]"
- "How does this compare to last month/quarter?"
- "Which department is driving the variance?"
