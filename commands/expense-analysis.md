---
description: Analyze your expenses - find top spending categories, trends, and potential issues using complete aggregated data
---

# Expense Analysis

Help the user understand where their money is going. Uses aggregation for complete, accurate expense totals instead of limited samples.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Financial Data

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify the main financials/P&L table.

## Step 3: Understand the Structure

```
Use: mcp__datarails-finance-os__get_table_schema
Parameters:
  table_id: <financials_table_id>
```

Look for:
- Amount/Value fields
- Account hierarchy fields (L0, L1, L2 categories)
- Date fields
- Scenario field (Actuals vs Budget)

## Step 4: Get Complete Expense Totals by Category

Use aggregation to get real totals (not estimates from 500-row samples):

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<account_l1_field>", "<account_l2_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false},
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": true}
  ]
```

This excludes revenue and gives complete expense breakdown in ~5 seconds.

**If a field fails (500 error):** Try a different account hierarchy field. For example, if "DR_ACC_L2" fails, try "DR_ACC_L1.5" or just use "DR_ACC_L1" for a higher-level breakdown.

## Step 5: Get Monthly Expense Trend

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id>
  dimensions: ["<date_field>", "<account_l1_field>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false},
    {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": true}
  ]
```

## Step 6: Analyze and Present

Create a user-friendly expense breakdown with real totals:

> ## Your Expense Analysis
>
> ### Total Expenses: $[real_total]
>
> ### Top Expense Categories (Complete Totals)
> | Category | Amount | % of Total |
> |----------|--------|-----------|
> | [Category 1] | $XX,XXX | XX% |
> | [Category 2] | $XX,XXX | XX% |
> | [Category 3] | $XX,XXX | XX% |
>
> ### Key Findings
> - **Largest expense area:** [Category] at $[amount] ([X]% of total)
> - **Number of expense categories:** [X]
> - **Data covers:** [date range]
>
> ### Monthly Trend
> - [Direction: Growing/Stable/Declining]
> - Highest month: [month] at $[amount]
> - Lowest month: [month] at $[amount]
>
> ### Things to Watch
> - [Any unusual patterns noticed]
> - [Categories with high concentration]
> - [Significant month-over-month changes]
>
> ### Recommended Actions
> 1. [Specific recommendation based on data]
> 2. [Another recommendation]
>
> **Want more detail?**
> - Ask me about a specific category: "Tell me more about [category] expenses"
> - `/datarails-finance-os:budget-comparison` - Compare to budget
> - `/datarails-finance-os:data-check` - Check for data anomalies

## Handling Different Data Structures

Different organizations structure their data differently. Adapt based on what you find:

**If account hierarchy uses different names:**
- Look for fields containing "Account", "Category", "Cost Center", "Department"
- Use `get_table_schema` to discover available fields

**If aggregation fails for a field:**
- Try a different hierarchy level (L1 instead of L2, or L1.5)
- If all aggregation fails, fall back to `get_records_by_filter` with limit 500 and note the totals are partial

## Follow-up Questions to Offer

After presenting the analysis, offer:
- "Would you like me to compare this to your budget?"
- "Should I look at how these expenses have changed over time?"
- "Want me to break this down by department or cost center?"
