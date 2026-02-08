---
description: Get a quick summary of your financial data - revenue, expenses, and key metrics using real aggregated totals
---

# Financial Summary

Generate a quick overview of the user's financial data with real aggregated totals. Perfect for a morning check-in or preparing for a meeting.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Discover Available Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Look for tables that contain:
- Financial/P&L data (usually named "Financials", "P&L", "Income Statement")
- KPI metrics (usually named "KPIs", "Metrics", "Dashboard")

## Step 3: Understand the Structure

Get the table schema to discover field names:

```
Use: mcp__datarails-finance-os__get_table_schema
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

This returns real totals grouped by account category in ~5 seconds.

## Step 5: Get Monthly Trend Data

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<date_field>", "<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

## Step 6: Get Key KPI Metrics (if available)

If a KPI table exists:

```
Use: mcp__datarails-finance-os__get_sample_records
Parameters:
  table_id: <kpi_table_id>
  n: 20
```

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
2. If all aggregation fails, fall back to `get_sample_records` and note that totals are estimated:

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
