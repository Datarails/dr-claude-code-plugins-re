---
description: Explore what data is available in your Datarails account
---

# Explore Your Data

Discover what tables and data are available in your Datarails Finance OS account.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: List All Tables

```
Use: mcp__datarails-finance-os__list_finance_tables
```

## Step 3: Present Available Data

Create a friendly overview:

> ## Your Datarails Data
>
> I found [X] tables in your account:
>
> ### Financial Data
> | Table | Records | Description |
> |-------|---------|-------------|
> | [Table Name] (ID: XXXX) | ~[count] | [inferred purpose] |
>
> ### KPI/Metrics Data
> | Table | Records | Description |
> |-------|---------|-------------|
> | [Table Name] (ID: XXXX) | ~[count] | [inferred purpose] |
>
> ### Other Tables
> | Table | Records | Description |
> |-------|---------|-------------|
> | [Table Name] (ID: XXXX) | ~[count] | [inferred purpose] |
>
> **Want to explore a specific table?** Just ask:
> - "Show me the columns in [table name]"
> - "What kind of data is in [table name]?"
> - "Show me a sample from [table name]"

## Step 4: Explore Specific Table (on request)

When user asks about a specific table:

### Get Schema
```
Use: mcp__datarails-finance-os__get_table_schema
Parameters:
  table_id: <requested_table_id>
```

### Get Sample Data
```
Use: mcp__datarails-finance-os__get_sample_records
Parameters:
  table_id: <requested_table_id>
  n: 10
```

### Present Table Details

> ## Table: [Table Name]
>
> ### Columns Available
> | Column | Type | Description |
> |--------|------|-------------|
> | [Column 1] | [type] | [inferred meaning] |
> | [Column 2] | [type] | [inferred meaning] |
> | ... | ... | ... |
>
> ### Sample Data
> Here's what the data looks like:
>
> [Show 3-5 sample records in a readable format]
>
> ### Quick Stats
> - **Total records:** ~[count]
> - **Date range:** [if date field exists]
> - **Key categories:** [if categorical fields exist]
>
> **What would you like to do with this data?**
> - Analyze it (expenses, revenue, etc.)
> - Check data quality
> - Compare to budget

## Inferring Table Purpose

Help users understand their tables based on column names:

**Likely Financial/P&L Table if contains:**
- Amount, Value, Sum columns
- Account hierarchy (L1, L2, L3)
- Scenario (Actuals, Budget)
- Date/Period fields

**Likely KPI Table if contains:**
- Metric names (ARR, MRR, Churn, etc.)
- Quarter/Period identifiers
- Calculated ratios

**Likely Master Data if contains:**
- Names, Codes, IDs
- No amount fields
- Lookup/reference structure

## Common Questions

**"What's the difference between these tables?"**
> [Table A] appears to contain [type of data] while [Table B] contains [different type]. They're likely used for different purposes in your reporting.

**"Which table should I use for [X]?"**
> For [X analysis], you'd typically want [Table Name] because it contains [relevant fields].

**"How often is this updated?"**
> I can see data through [latest date]. The refresh schedule depends on your Datarails setup - typically daily or when data is loaded.

## Follow-up Options

After exploration, offer relevant next steps:
- "Want me to analyze this data?"
- "Should I check for data quality issues?"
- "Ready to compare actuals to budget?"
