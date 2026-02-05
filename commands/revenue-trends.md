---
description: See your revenue trends over time - growth rates, patterns, and insights
---

# Revenue Trends

Analyze revenue patterns over time. Shows growth trends, seasonal patterns, and revenue composition.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
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

## Step 4: Profile Revenue Categories

```
Use: mcp__datarails-finance-os__get_field_distinct_values
Parameters:
  table_id: <financials_table_id>
  field_name: <account_l1_field>
  limit: 50
```

Identify revenue-related categories (REVENUE, Sales, Income, etc.)

## Step 5: Fetch Revenue Data

```
Use: mcp__datarails-finance-os__get_records_by_filter
Parameters:
  table_id: <financials_table_id>
  filters: {
    "<account_l1_field>": {"in": ["REVENUE", "Revenue", "Sales", "Income"]},
    "<scenario_field>": "Actuals"
  }
  limit: 500
```

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

Create a compelling revenue story:

> ## Your Revenue Trends
>
> ### Revenue Overview
> - **Latest period revenue:** $[amount]
> - **Data period:** [start] to [end]
> - **Revenue sources:** [count] different categories
>
> ### Trend Analysis
> Based on your data:
> - **Overall direction:** [Growing/Stable/Declining]
> - **Key revenue drivers:** [top categories]
>
> ### Revenue Composition
> | Source | Share |
> |--------|-------|
> | [Source 1] | XX% |
> | [Source 2] | XX% |
> | [Other] | XX% |
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
> - "How does this compare to last year?"
> - "What's driving the growth/decline?"
> - "Show me revenue by customer segment"

## Handling Limited Data

**If only one period of data:**
> I can see your revenue data, but I only have [one period]. For trend analysis, I'd need multiple months or quarters. Would you like me to show you the breakdown for this period instead?

**If no revenue category found:**
> I'm having trouble identifying revenue in your data. The account categories I found are: [list them]. Which of these represents your revenue?

## Visualization Suggestions

Since Cowork can't generate charts, suggest:

> **Tip:** For visual charts, you can:
> 1. Export this data to Excel using `/datarails-finance-os:export-data`
> 2. Or paste these numbers into your favorite charting tool

## Follow-up Options

After analysis, offer:
- "Compare revenue to expenses?"
- "Look at revenue by department or product?"
- "Check for seasonality patterns?"
