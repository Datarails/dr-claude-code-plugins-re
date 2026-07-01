---
description: Get a quick summary of your financial data - revenue, expenses, and key metrics using real aggregated totals
---

# Financial Summary

Generate a quick overview of the user's financial data with real aggregated totals. Perfect for a morning check-in or preparing for a meeting.

## Step 1: Verify Connection

Start by calling `list_data_models` to verify the connection is active.

**If the tool call fails:** The Datarails connector isn't connected. Tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

## Step 2: Discover Available Data

```
Use: mcp__datarails-finance-os__list_data_models
```

Each entry carries both a numeric `id` (for the by-id tools) and an `alias` (for the by-alias tools; empty when the table has no alias). **Prefer the alias path when an alias exists** — friendlier field names, far fewer tokens.

Look for tables that contain:
- Financial/P&L data (usually named "Financials", "P&L", "Income Statement")
- KPI metrics (usually named "KPIs", "Metrics", "Dashboard")

## Step 3: Understand the Structure

Discover the field names. If the financials table has an alias, list its
business-friendly fields:

```
Use: mcp__datarails-finance-os__list_aliased_fields
Parameters:
  alias: <financials_alias>
```

If the table has no alias, fall back to by-id (capture each field's numeric
`id` — the by-id tools address fields by id):

```
Use: mcp__datarails-finance-os__get_fields_by_id
Parameters:
  table_id: <financials_table_id>
```

Identify key fields:
- **Amount field** (e.g., "Amount")
- **Account hierarchy field** (e.g., "DR_ACC_L0", "DR_ACC_L1" or similar)
- **Scenario field** (e.g., "Scenario")
- **Date field** (e.g., "Reporting Date")

## Step 4: Get Real Financial Totals via Aggregation

Use the aggregation API to get complete, accurate totals (not estimates from samples):

**Aggregation rules:**
- Text fields (`Scenario`, `Account Group L0`, etc.) go in `filters` as value-lists.
- Date ranges now filter directly via an **advanced** filter — to scope to a period, pass `{"name": "<date_field>", "values": {"type": "advanced", "val": [{"condition": "total_range", "value": ["<start_epoch>", "<end_epoch>"]}]}}` (epoch seconds as strings). Putting the date in `dimensions` and filtering client-side still works and is optional.

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

This returns real totals grouped by account category in ~5 seconds.

## Step 5: Get Monthly Trend Data

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
  dimensions: ["<date_field>", "<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

(By-id fallback: `get_aggregated_data_by_id` with `dimensions=[<date_field_id>, <account_l1_field_id>]` and `metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]`.)

## Step 6: Get Key KPI Metrics (if available)

For named KPIs, discover what's defined for this org:

```
Use: mcp__datarails-finance-os__list_business_metrics
```

This returns a flat list — each entry has `id`, `name`, `description`,
`category`, `kind`, `dimensions[]`, and `status_info{}`. Use it to identify the
relevant KPIs, then compute their values from the aggregated totals above (or
via a targeted `get_aggregated_data_by_alias` / `get_aggregated_data_by_id`
call on the metric's source table). If a KPI table exists and you want a quick
look at its rows:

```
Use: mcp__datarails-finance-os__get_data_by_alias
Parameters:
  alias: <kpi_alias>
  limit: 20
```

(By-id fallback: `get_data_by_id` with `table_id=<kpi_table_id>` and `limit=20`.)

## Step 7: Present Summary

Create a friendly summary with real numbers:

> ## Your Financial Snapshot
>
> **Real Totals (Actuals):**
> - Revenue: $[real_total]
> - Cost of Goods Sold: $[real_total]
> - Operating Expenses: $[real_total]
> - Gross Profit: $[calculated]
> - Gross Margin: [calculated]%
>
> **Monthly Trend:**
> - [X] months of data available
> - Most recent month: [month] - Revenue $[amount]
> - Revenue direction: [Growing/Stable/Declining]
>
> **Data Quality:**
> - Data quality: [Good/Fair/Needs attention]
>
> **Want to dig deeper?**
> - `/datarails-finance-os:expense-analysis` - Detailed expense breakdown
> - `/datarails-finance-os:revenue-trends` - Revenue trends over time
> - `/datarails-finance-os:budget-comparison` - Compare to budget
> - `/datarails-finance-os:data-check` - Full data quality report

## Handling Aggregation Failures

If the aggregation call returns an error for a specific field:
1. Try using a different account hierarchy field (e.g., "DR_ACC_L1.5" instead of "DR_ACC_L1")
2. If an alias call errors, retry the by-id twin (`get_aggregated_data_by_id`)
3. If all aggregation fails, fall back to a small row pull via `get_data_by_alias` / `get_data_by_id` (small `limit`) and note that totals are estimated:

> **Note:** These are estimates based on a data sample. For complete totals, the aggregation API needs to be tested with `/datarails-finance-os:test-api`.

## Handling Missing Data

If no financials table found:
> I couldn't find a financials table in your Datarails account. This might mean:
> - The data hasn't been loaded yet
> - You might need different access permissions
>
> Would you like me to show you all available tables so we can find your data?

## Tips for Users

- This command shows real aggregated totals, not estimates from samples
- Data refreshes when you run the command - always shows current state
- Results typically arrive in about 5 seconds
- If something looks wrong, try `/datarails-finance-os:data-check` to investigate
