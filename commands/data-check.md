---
description: Check your financial data for quality issues - missing values, anomalies, and inconsistencies
---

# Data Quality Check

Run automated checks on your financial data to identify potential issues before they cause problems.

## Step 1: Verify Connection

Start by calling `list_data_models` to verify the connection is active.

**If the tool call fails:** The Datarails connector isn't connected. Tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

## Step 2: Find Tables to Check

```
Use: mcp__datarails-finance-os__list_data_models
```

Identify all relevant tables (financials, KPIs, etc.). Each entry carries both a numeric `id` (for the by-id tools) and an `alias` (empty when the table has no alias).

## Step 3: Profile Numeric Fields

The MCP server has no server-side anomaly tool — findings (outliers, missing-value rates, duplicate counts, severity) are computed **client-side** from baseline aggregates. Start by pulling the numeric baseline for each important table:

```
Use: mcp__datarails-finance-os__profile_numeric_fields
Parameters:
  table_id: <table_id>
```

Returns `SUM, AVG, MIN, MAX, COUNT` per numeric field. From these, derive client-side:
- Min/max values (potential errors)
- Statistical range outliers (flag values outside a band around AVG; true z-scores aren't available because std dev isn't returned)
- Unexpected nulls (compare COUNT to total row count)

## Step 4: Profile Categorical Fields

```
Use: mcp__datarails-finance-os__profile_categorical_fields
Parameters:
  table_id: <table_id>
```

Returns distinct-count + sample values per field. From these, derive client-side:
- Unexpected values
- High cardinality issues
- Inconsistent naming

## Step 5: Compute Findings (per-value frequencies, duplicates, nulls)

For per-value counts, duplicate detection, and exact null rates, group the data yourself:

```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias   (preferred, if the table has an alias)
Parameters:
  alias: <table_alias>
  dimensions: [<field_alias>]
  metrics: [{"field": <field_alias>, "agg": "COUNT"}]

# or, for tables without an alias:
Use: mcp__datarails-finance-os__get_aggregated_data_by_id
Parameters:
  table_id: <table_id>
  dimensions: [<field_id>]
  metrics: [{"field_id": <field_id>, "agg": "COUNT"}]
```

From the grouped result, compute findings:
- **Duplicates** — group by a candidate key, flag groups where `COUNT > 1`.
- **Missing values** — the null/blank group appears as an unnamed bucket; divide its COUNT by total rows for the null rate.
- **Rare categorical values** — flag values whose COUNT is below a small threshold.

To surface specific offending rows, fetch them directly with advanced filters:

```
Use: mcp__datarails-finance-os__get_data_by_alias   (or get_data_by_id)
Parameters:
  alias: <table_alias>
  select: [<field_alias>, ...]
  filters: [{"name": <amount_alias>, "values": {"type": "advanced", "val": [{"condition": "gt", "value": "<upper_band>"}]}}]
```

(By-id twin uses `{"field_id": <id>, "values": {...}}`.) Advanced conditions include `gt`, `gte`, `lt`, `lte`, `range`, `total_range`, `is null`, `contains` — comparisons, ranges, text matching, and null checks are all supported.

## Step 6: Present Results

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
