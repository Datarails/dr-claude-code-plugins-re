---
description: Get a quick summary of your financial data - revenue, expenses, and key metrics
---

# Financial Summary

Generate a quick overview of the user's financial data. Perfect for a morning check-in or preparing for a meeting.

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

## Step 3: Get Table Overview

For the main financials table found:

```
Use: mcp__datarails-finance-os__profile_table_summary
Parameters:
  table_id: <financials_table_id>
```

This gives row counts, column info, and data quality metrics.

## Step 4: Fetch Sample Data

Get a sample to understand the data structure:

```
Use: mcp__datarails-finance-os__get_sample_records
Parameters:
  table_id: <financials_table_id>
  n: 20
```

## Step 5: Get Key Metrics

If a KPI table exists, fetch sample KPI data:

```
Use: mcp__datarails-finance-os__get_sample_records
Parameters:
  table_id: <kpi_table_id>
  n: 20
```

## Step 6: Present Summary

Create a friendly summary for the user:

> ## Your Financial Snapshot
>
> **Data Available:**
> - [X] records in your financials table
> - Covering dates from [earliest] to [latest]
> - [Y] different accounts tracked
>
> **At a Glance:**
> Based on your recent data:
> - Revenue categories: [list top 3]
> - Expense categories: [list top 3]
> - Data quality: [Good/Fair/Needs attention]
>
> **Want to dig deeper?**
> - `/datarails-finance-os:expense-analysis` - Detailed expense breakdown
> - `/datarails-finance-os:revenue-trends` - Revenue trends over time
> - `/datarails-finance-os:data-check` - Full data quality report

## Handling Missing Data

If no financials table found:
> I couldn't find a financials table in your Datarails account. This might mean:
> - The data hasn't been loaded yet
> - You might need different access permissions
>
> Would you like me to show you all available tables so we can find your data?

## Tips for Users

- This command gives a quick overview - for detailed analysis, use the specific commands
- Data refreshes when you run the command - always shows current state
- If something looks wrong, try `/datarails-finance-os:data-check` to investigate
