---
description: Compare actual results to budget - see where you're over or under plan using complete aggregated data
---

# Budget vs Actual Comparison

Compare your actual financial results against budget using real aggregated totals to identify variances and understand performance.

## Step 1: Verify Connection

Start by calling `list_data_models` to verify the connection is active.

**If the tool call fails:** The Datarails connector isn't connected. Tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_data_models
```

Identify the financials table that contains both Actuals and Budget scenarios. Note **both** its numeric `id` and its `alias` (the alias may be empty). **Prefer the alias path when an alias exists** — friendlier field names, far fewer tokens.

## Step 3: Understand the Structure

```
# If the table has an alias:
Use: mcp__datarails-finance-os__list_aliased_fields
Parameters:
  alias: <financials_alias>

# Otherwise (no alias), use the by-id schema (capture each field's numeric id):
Use: mcp__datarails-finance-os__get_fields_by_id
Parameters:
  table_id: <financials_table_id>
```

Identify key fields: Scenario, Amount, Account hierarchy, Date.

## Step 4: Get Actuals Totals via Aggregation

**Aggregation rules:**
- Text fields (`Scenario`, `Account Group L0`, etc.) go in `filters` as value lists.
- To limit to a specific period, pass an **advanced** date filter directly (`total_range` with epoch-second strings), or add the date as a dimension and filter the results client-side. Both work — date filtering is no longer rejected.

Alias path (preferred):

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
  dimensions: ["<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

By-id fallback (no alias):

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_id
Parameters:
  table_id: <financials_table_id>
  dimensions: [<account_l1_field_id>]
  metrics: [{"field_id": <amount_field_id>, "agg": "SUM"}]
  filters: [
    {"field_id": <scenario_field_id>, "values": ["Actuals"]}
  ]
```

## Step 5: Get Budget Totals via Aggregation

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
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
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
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
1. Try a different account hierarchy field (re-inspect the Step 3 schema for a sibling)
2. If the alias call errors, retry the by-id twin (`get_aggregated_data_by_id`)
3. If all aggregation fails, fall back to `get_data_by_alias` / `get_data_by_id` (500-row limit per scenario) and note the comparison is based on partial data

## Department-Level Analysis

If the user wants department-level variances, run additional aggregation:

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
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
