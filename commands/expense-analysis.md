---
description: Analyze your expenses - find top spending categories, trends, and potential issues
---

# Expense Analysis

Help the user understand where their money is going. Identifies top expense categories, unusual spending, and trends.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
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
- Account hierarchy fields (L1, L2, L3 categories)
- Date fields
- Scenario field (Actuals vs Budget)

## Step 4: Profile Expense Categories

```
Use: mcp__datarails-finance-os__profile_categorical_fields
Parameters:
  table_id: <financials_table_id>
  fields: ["<account_l1_field>", "<account_l2_field>"]
```

This shows the expense categories and their frequency.

## Step 5: Get Expense Data Sample

```
Use: mcp__datarails-finance-os__get_records_by_filter
Parameters:
  table_id: <financials_table_id>
  filters: {"<account_l1_field>": {"in": ["Operating Expense", "Cost of Good sold", "COGS", "OpEx"]}}
  limit: 500
```

Note: Adjust filter values based on what you found in the categorical profile.

## Step 6: Analyze and Present

Create a user-friendly expense breakdown:

> ## Your Expense Analysis
>
> ### Top Expense Categories
> | Category | Estimated % of Total |
> |----------|---------------------|
> | [Category 1] | XX% |
> | [Category 2] | XX% |
> | [Category 3] | XX% |
>
> ### Key Findings
> - **Largest expense area:** [Category]
> - **Number of expense accounts:** [X]
> - **Data covers:** [date range]
>
> ### Things to Watch
> - [Any unusual patterns noticed]
> - [Categories with high variability]
> - [Potential data quality issues]
>
> ### Recommended Actions
> 1. [Specific recommendation based on data]
> 2. [Another recommendation]
>
> **Want more detail?**
> - Ask me about a specific category: "Tell me more about [category] expenses"
> - `/datarails-finance-os:data-check` - Check for data anomalies

## Handling Different Data Structures

Different organizations structure their data differently. Adapt based on what you find:

**If account hierarchy uses different names:**
- Look for fields containing "Account", "Category", "Cost Center", "Department"
- Use `get_field_distinct_values` to understand the values

**If no clear expense indicator:**
- Look for Amount fields with negative values (often expenses)
- Or filter by Account Type if available

## Follow-up Questions to Offer

After presenting the analysis, offer:
- "Would you like me to compare this to your budget?"
- "Should I look at how these expenses have changed over time?"
- "Want me to identify any unusual transactions?"
