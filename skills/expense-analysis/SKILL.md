---
name: dr-expense-analysis
description: Top expense categories, monthly expense trends, and concentration analysis from real aggregated data. Self-contained — discovers the client's financials table and fields itself, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__get_records_by_filter
  - Read
  - Write
argument-hint: "[--scenario <name>] [--year <YYYY>] [--breakdown <l1|l2>]"
---

# Expense Analysis

Where the money is going — top expense categories with complete
totals (not sample estimates), monthly trend, and concentration
analysis. Built on `aggregate_table_data` (no row cap).

This skill is **self-contained**: it discovers the client's financials
table and field names itself (Step 2). It does not depend on
a saved profile, a learn step, or any prior setup — every Datarails
environment names its table and fields differently, so discovery
happens inline, once per conversation.

## Workflow

### Step 1: Verify Authentication

If a tool call fails with auth or connection error, tell the user to
connect via Connectors UI ("+" → Connectors → Datarails → Connect),
then stop.

### Step 2: Discover the financials table and its fields

**If you already discovered these earlier in THIS conversation, reuse
them — skip to the next step.** Discovery is cheap but not free; do it
once per conversation, then carry the values forward.

1. `list_finance_tables`. Pick the financials table: the one whose name
   matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Call it `<financials_table_id>`.

2. `get_table_schema(<financials_table_id>)`. Bind these by
   case-insensitive name match (respecting the noted type):
   - `<amount_field>`       — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`     — categorical: `^scenario$` → `^version$`
   - `<date_field>`         — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_field>`   — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>`   — `dr_acc_l2` → `account_l2` (for breakdown depth)

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

3. Find the account-category values. The distinct-values API often
   returns 409, so call `get_sample_records(<financials_table_id>,
   limit=500)` and collect the distinct `<account_l1_field>` values.
   Match:
   - `<revenue_value>` ← `/revenue|sales|income/i` (excluded from expenses)
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest top-level
   one; if genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

### Step 3: Pull totals by expense category

Default breakdown is L1 × L2 if available, otherwise L1 only.

```
table_id: <financials_table_id>
dimensions: ["<account_l1_field>", "<account_l2_field>"]
metrics: [{"field": "<amount_field>", "agg": "SUM"}]
filters: [
  {"name": "<scenario_field>", "values": ["<scenario or Actuals>"], "is_excluded": false},
  {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": true}
]
```

Filter rules:
- **Date fields go in `dimensions`, never `filters`.** Filter API
  silently returns empty for date columns.
- **Only text fields go in filters.** Equality, value-list, or
  exclusion list — comparison operators are rejected by the backend.

If the L2 field is rejected: retry without it (group by L1 only) and
note the limitation in the output.

### Step 4: Pull monthly expense trend

```
dimensions: ["<date_field>", "<account_l1_field>"]
metrics: [{"field": "<amount_field>", "agg": "SUM"}]
filters: [
  {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false},
  {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": true}
]
```

### Step 5: Compute concentration and present

Calculate client-side from the L1×L2 result:
- Total expenses
- Top N categories by absolute amount
- Each category's share of total (concentration)
- Categories above 20% of total → concentration flag
- From the monthly series: direction, highest/lowest month, MoM
  changes

```
## Your Expense Analysis

Total Expenses: $[real_total]

Top Expense Categories:
| Category               | Amount      | % of Total |
|------------------------|-------------|------------|
| [category 1]           | $[amount]   | [X]%       |
| [category 2]           | $[amount]   | [X]%       |
| ...                    |             |            |

Concentration:
  - Largest category: [category] at [X]% of total
  - Top 3 share:       [X]%
  - [Concentration flag if top 1 > 20% or top 3 > 60%]

Monthly Trend:
  Direction:    [growing / stable / declining]
  Highest:      [month] at $[amount]
  Lowest:       [month] at $[amount]

Things to Watch:
  - [Concentration risk on a single category, if any]
  - [Unusually large MoM jump, if any]
  - [Categories with sparse coverage, if any]

Recommended Actions:
  1. [Specific suggestion grounded in the numbers]
  2. ...
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `--scenario <name>` | Scenario to analyze | `Actuals` |
| `--year <YYYY>` | Restrict to one fiscal year (client-side filter on the date dimension) | All available |
| `--breakdown <l1\|l2>` | Hierarchy depth for the category table | `l2` if available, else `l1` |

## Backward compatibility

- Uses only raw-tables MCP tools (always available).
- Date filtering is client-side (API rejects date filters).
- Comparison / range filter operators are not used (rejected by
  backend).

## Handling failures

**L2 field rejected (500):** retry grouping by L1 only (or a sibling
account field from the discovered schema, e.g. `DR_ACC_L1.5`); note the
reduced depth in the output. If no field works, tell the user which
field failed.

**Revenue category ambiguous:** ask the user which L1 value
represents revenue so it can be properly excluded from "expenses".

**All aggregation fails:** fall back to `get_records_by_filter`
with the scenario as an equality filter (500-row cap). Note that
totals are partial.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-revenue-trends` — revenue counterpart
- `/dr-departments` — by department/cost-center
- `/dr-intelligence` — full FP&A workbook
- `/dr-anomalies` — data quality check
