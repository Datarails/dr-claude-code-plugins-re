---
description: See your revenue trends over time - growth rates, patterns, and insights using complete aggregated data
---

# Revenue Trends

Analyze revenue patterns over time using real aggregated data. Shows growth trends, seasonal patterns, and revenue composition.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify:
- Main financials/P&L table
- KPI table (often contains ARR, MRR metrics)

## Step 3: Understand Revenue Structure

```
Use: mcp__datarails-finance-os__get_table_schema
Parameters:
  table_id: <financials_table_id>
```

Look for:
- Revenue account categories
- Date/Period fields
- Scenario field (Actuals)

## Step 4: Get Monthly Revenue Totals via Aggregation

Use aggregation for complete monthly revenue data:

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<date_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": false},
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

This returns real monthly revenue totals in ~5 seconds.

## Step 5: Get Revenue by Sub-Category (if available)

For revenue composition breakdown:

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<account_l2_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": false},
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
  ]
```

**If the L2 field fails:** Try a different field level, or skip this step and show only top-level revenue.

## Step 6: Check KPI Metrics (if available)

If a KPI table exists:

```
Use: mcp__datarails-finance-os__get_sample_records
Parameters:
  table_id: <kpi_table_id>
  n: 20
```

Look for ARR, MRR, Net New ARR, Churn metrics.

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
1. Try using a broader field (L1 instead of L2)
2. If all aggregation fails, fall back to `get_records_by_filter` and note the data is partial

## Follow-up Options

After analysis, offer:
- "Compare revenue to expenses?"
- "Look at revenue by department or product?"
- "Compare to budget or forecast?"
