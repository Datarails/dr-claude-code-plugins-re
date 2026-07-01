---
description: See your revenue trends over time - growth rates, patterns, and insights using complete aggregated data
---

# Revenue Trends

Analyze revenue patterns over time using real aggregated data. Shows growth trends, seasonal patterns, and revenue composition.

## Step 1: Verify Connection

Start by calling `list_data_models` to verify the connection is active.

**If the tool call fails:** The Datarails connector isn't connected. Tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_data_models
```

Identify:
- Main financials/P&L table — note **both** its numeric `id` and its `alias` (the alias may be empty). **Prefer the alias path when an alias exists.**
- KPI table (often contains ARR, MRR metrics)

## Step 3: Understand Revenue Structure

```
# If the table has an alias (preferred):
Use: mcp__datarails-finance-os__list_aliased_fields
Parameters:
  alias: <financials_alias>

# Otherwise, by id (capture each field's numeric id — the by-id tools need ids):
Use: mcp__datarails-finance-os__get_fields_by_id
Parameters:
  table_id: <financials_table_id>
```

Look for:
- Revenue account categories
- Date/Period fields
- Scenario field (Actuals)

## Step 4: Get Monthly Revenue Totals via Aggregation

Use aggregation for complete monthly revenue data:

**Aggregation rules:**
- Put the date field (`Reporting Date`, `Reporting Month`, etc.) in `dimensions` to get a row per month.
- To scope to a specific period you can either add the date as a dimension and filter client-side, or pass an **advanced** date filter directly (epoch seconds as strings): `{"name": "<date_field>", "values": {"type": "advanced", "val": [{"condition": "total_range", "value": ["<start_epoch>", "<end_epoch>"]}]}}`.
- Text fields (`Scenario`, `Account Group L0`, etc.) go in `filters` as value lists.

```
# Alias path (preferred):
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
  dimensions: ["<date_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": false},
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]

# By-id fallback (no alias):
Use: mcp__datarails-finance-os__get_aggregated_data_by_id
Parameters:
  table_id: <financials_table_id>
  dimensions: [<date_field_id>]
  metrics: [{"field_id": <amount_field_id>, "agg": "SUM"}]
  filters: [
    {"field_id": <account_l1_field_id>, "values": ["<revenue_category>"]},
    {"field_id": <scenario_field_id>, "values": ["Actuals"]}
  ]
```

This returns real monthly revenue totals in ~5 seconds.

## Step 5: Get Revenue by Sub-Category (if available)

For revenue composition breakdown:

```
# Alias path (preferred):
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
  dimensions: ["<account_l2_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": false},
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]

# By-id fallback (no alias):
Use: mcp__datarails-finance-os__get_aggregated_data_by_id
Parameters:
  table_id: <financials_table_id>
  dimensions: [<account_l2_field_id>]
  metrics: [{"field_id": <amount_field_id>, "agg": "SUM"}]
  filters: [
    {"field_id": <account_l1_field_id>, "values": ["<revenue_category>"]},
    {"field_id": <scenario_field_id>, "values": ["Actuals"]}
  ]
```

**If the L2 field fails:** Try a different field level (a sibling from the Step 3 schema), or skip this step and show only top-level revenue.

## Step 6: Check KPI Metrics (if available)

For named KPIs, start with the business-metrics catalog:

```
Use: mcp__datarails-finance-os__list_business_metrics
```

Scan the returned flat list for ARR, MRR, Net New ARR, Churn metrics. If you need the underlying values, aggregate them from the KPI table via the aliased/by-id tools (discover the table the same way as Step 2):

```
# Small sample to inspect the KPI table's structure (alias path preferred):
Use: mcp__datarails-finance-os__get_data_by_alias
Parameters:
  alias: <kpi_alias>
  limit: 20

# By-id fallback (no alias):
Use: mcp__datarails-finance-os__get_data_by_id
Parameters:
  table_id: <kpi_table_id>
  limit: 20
```

## Step 7: Analyze and Present

Create a compelling revenue story with real numbers:

> ## Your Revenue Trends
>
> ### Revenue Overview
> - **Total Revenue (Actuals):** $[real_total]
> - **Data period:** [start] to [end]
> - **Months of data:** [count]
>
> ### Monthly Trend
> | Month | Revenue | MoM Change |
> |-------|---------|------------|
> | [Month 1] | $XX,XXX | — |
> | [Month 2] | $XX,XXX | +X% |
> | ... | ... | ... |
>
> ### Trend Analysis
> - **Overall direction:** [Growing/Stable/Declining]
> - **Average monthly revenue:** $[calculated]
> - **Peak month:** [month] at $[amount]
> - **Growth (first to last):** [X]%
>
> ### Revenue Composition (if L2 data available)
> | Source | Amount | Share |
> |--------|--------|-------|
> | [Source 1] | $XX,XXX | XX% |
> | [Source 2] | $XX,XXX | XX% |
> | [Other] | $XX,XXX | XX% |
>
> ### Key Metrics (if KPI data available)
> - ARR: $[amount]
> - Net New ARR: $[amount]
> - Churn Rate: [X]%
>
> ### Insights
> - [Key insight about the trends]
> - [Notable pattern or change]
> - [Recommendation based on data]
>
> **Questions to explore:**
> - "How does this compare to budget?"
> - "What's driving the growth/decline?"
> - "Show me revenue by department"

## Handling Limited Data

**If only one period of data:**
> I can see your revenue data, but I only have [one period]. For trend analysis, I'd need multiple months. Would you like me to show you the breakdown for this period instead?

**If no revenue category found:**
> I'm having trouble identifying revenue in your data. The account categories I found are: [list them]. Which of these represents your revenue?

## Handling Aggregation Failures

If aggregation fails for a specific field:
1. Try using a broader field (L1 instead of L2), or a sibling field from the Step 3 schema
2. If an alias call errors, retry the by-id twin (`get_aggregated_data_by_id`)
3. If all aggregation fails, fall back to `get_data_by_alias` / `get_data_by_id` and note the data is partial

## Follow-up Options

After analysis, offer:
- "Compare revenue to expenses?"
- "Look at revenue by department or product?"
- "Compare to budget or forecast?"
