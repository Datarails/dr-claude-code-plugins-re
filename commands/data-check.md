---
description: Check your financial data for quality issues - missing values, anomalies, and inconsistencies
---

# Data Quality Check

Run automated checks on your financial data to identify potential issues before they cause problems.

## Step 1: Verify Connection

```
Use: mcp__datarails-finance-os__check_auth_status
```

**If not authenticated:** Guide user to run `/datarails-finance-os:login` first.

## Step 2: Find Tables to Check

```
Use: mcp__datarails-finance-os__list_finance_tables
```

Identify all relevant tables (financials, KPIs, etc.)

## Step 3: Run Anomaly Detection

For each important table:

```
Use: mcp__datarails-finance-os__detect_anomalies
Parameters:
  table_id: <table_id>
```

This automatically checks for:
- Outliers (unusual values)
- Missing data patterns
- Duplicate records
- Date/time anomalies
- Referential integrity issues

## Step 4: Profile Data Quality

```
Use: mcp__datarails-finance-os__profile_table_summary
Parameters:
  table_id: <table_id>
```

Gets comprehensive stats including:
- Row counts
- Missing value percentages
- Data quality score

## Step 5: Check Numeric Fields

```
Use: mcp__datarails-finance-os__profile_numeric_fields
Parameters:
  table_id: <table_id>
```

Identifies:
- Min/max values (potential errors)
- Statistical outliers
- Unexpected nulls

## Step 6: Check Categorical Fields

```
Use: mcp__datarails-finance-os__profile_categorical_fields
Parameters:
  table_id: <table_id>
```

Identifies:
- Unexpected values
- High cardinality issues
- Inconsistent naming

## Step 7: Present Results

Create a clear, actionable report:

> ## Data Quality Report
>
> ### Overall Health: [Score]/100
> [Health indicator: Excellent/Good/Fair/Needs Attention/Critical]
>
> ### Summary
> - **Tables checked:** [count]
> - **Total records:** [count]
> - **Issues found:** [count]
>
> ### Issues by Severity
>
> #### Critical (Fix Immediately)
> - [Issue description and location]
> - [Impact explanation]
>
> #### High Priority (Fix This Week)
> - [Issue description]
>
> #### Medium Priority (Review Soon)
> - [Issue description]
>
> #### Low Priority (Monitor)
> - [Issue description]
>
> ### Detailed Findings
>
> **Missing Data:**
> - [Field X]: [Y]% missing
> - [Field Z]: [W]% missing
>
> **Outliers Detected:**
> - [Description of unusual values]
>
> **Potential Duplicates:**
> - [If any found]
>
> ### Recommended Actions
> 1. [Most important action]
> 2. [Second priority]
> 3. [Third priority]
>
> ### What's Working Well
> - [Positive findings]
> - [Areas with good data quality]

## Severity Definitions

Help users understand priority:

| Severity | Meaning | Action |
|----------|---------|--------|
| Critical | Data is incorrect or missing in ways that affect reports | Fix before using data |
| High | Significant issues that could cause errors | Fix within a week |
| Medium | Minor issues or potential problems | Review when convenient |
| Low | Cosmetic or very minor issues | Monitor over time |

## Common Issues and Explanations

**"Outliers detected in Amount field"**
> Some values are statistically unusual - they're much higher or lower than typical. This could be:
> - Legitimate large transactions
> - Data entry errors
> - One-time adjustments
>
> Would you like me to show you the specific records?

**"Missing values in date field"**
> Some records don't have dates, which could affect time-based reporting.
>
> This typically happens when:
> - Data wasn't fully loaded
> - Records are pending completion
>
> [X] records affected.

**"High cardinality in category field"**
> There are many unique values where we'd expect fewer. This might indicate:
> - Inconsistent naming (e.g., "Marketing" vs "marketing" vs "Mktg")
> - Data needs cleanup
>
> Want me to show the variations?

## Follow-up Actions

After the report, offer:
- "Show me the specific records with issues"
- "Which issue should I investigate first?"
- "Run the check again after fixes"
