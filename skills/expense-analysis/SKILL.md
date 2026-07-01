---
name: dr-expense-analysis
description: Top expense categories, monthly expense trends, and concentration analysis from real aggregated data. Self-contained — discovers the client's financials table and fields itself, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__list_business_metrics
  - Read
  - Write
argument-hint: "[--scenario <name>] [--year <YYYY>] [--breakdown <l1|l2>]"
---

# Expense Analysis

Where the money is going — top expense categories with complete
totals (not sample estimates), monthly trend, and concentration
analysis. Built on `get_aggregated_data_by_alias` (or its by-id twin),
which has no row cap.

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

1. `list_data_models`. Pick the financials table: the one whose name
   (or alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match,
   the largest by row count. Note **both** its numeric `id` and its
   `alias` (the alias may be empty). **Prefer the alias path when an
   alias exists** — friendlier field names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each
   field's numeric `id` — the by-id tools address fields by id). Bind
   these by case-insensitive match on the field alias/name (respecting
   the noted type):
   - `<amount_field>`       — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`     — categorical: `^scenario$` → `^version$`
   - `<date_field>`         — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_field>`   — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>`   — `dr_acc_l2` → `account_l2` (for breakdown depth)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

3. Find the account-category values:
   `get_distinct_values_by_alias(<alias>, <account_l1_field>)` (or
   `get_distinct_values_by_id(<id>, <account_l1_field_id>)`). If the
   distinct call errors, fall back to `get_data_by_alias(<alias>,
   select=[<account_l1_field>], limit=500)` (or the by-id twin) and
   collect the distinct values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i` (excluded from expenses)
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest top-level
   one; if genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

### Step 3: Pull totals by expense category

Default breakdown is L1 × L2 if available, otherwise L1 only.

Alias path (preferred):

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=["<account_l1_field>", "<account_l2_field>"],
  metrics=[{"field": "<amount_field>", "agg": "SUM"}],
  filters=[
    {"name": "<scenario_field>", "values": ["<scenario or Actuals>"], "is_excluded": false},
    {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": true}
  ]
)
```

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>,
dimensions=[<account_l1_field_id>, <account_l2_field_id>],
metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}],
filters=[{"field_id": <scenario_field_id>, "values": [...]},
{"field_id": <account_l1_field_id>, "values": [<revenue_value>], "is_excluded": true}])`.

Filter rules:
- **Value-list / exclusion filters** match any of the listed values; set
  `is_excluded: true` to turn the list into NOT-IN (that's how revenue is
  dropped above).
- **Date scoping** can go in `filters` directly via an advanced
  `total_range` condition (epoch-second strings), or you can add
  `<date_field>` to `dimensions` and filter client-side — both work.
- **Comparisons, ranges, text matching, and null checks** are all
  supported via advanced filters (see the `--year` note below).

If the L2 field is rejected: retry without it (group by L1 only) and
note the limitation in the output.

### Step 4: Pull monthly expense trend

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=["<date_field>", "<account_l1_field>"],
  metrics=[{"field": "<amount_field>", "agg": "SUM"}],
  filters=[
    {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false},
    {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": true}
  ]
)
```

(By-id twin: `get_aggregated_data_by_id` with field ids and
`metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]`.)

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
| `--year <YYYY>` | Restrict to one fiscal year (advanced `total_range` date filter, or a date dimension + client-side filter) | All available |
| `--breakdown <l1\|l2>` | Hierarchy depth for the category table | `l2` if available, else `l1` |

## Backward compatibility

- Alias-first: uses the by-alias data tools when the table has an alias,
  and falls back to the by-id twins otherwise (both always available).
- Date ranges filter directly via an advanced `total_range` filter, or
  by adding the date as a dimension and filtering client-side.
- Comparison, range, text-matching, and null filter operators are
  available via advanced filters if a narrower scope is needed.

## Handling failures

**L2 field rejected (500):** retry grouping by L1 only (or a sibling
account field from the discovered schema, e.g. `DR_ACC_L1.5`); note the
reduced depth in the output. If no field works, tell the user which
field failed. If an alias call errors, retry the by-id twin.

**Revenue category ambiguous:** ask the user which L1 value
represents revenue so it can be properly excluded from "expenses".

**All aggregation fails:** fall back to `get_data_by_alias` (or
`get_data_by_id`) with the scenario as a value-list filter (500-row
cap). Note that totals are partial.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-revenue-trends` — revenue counterpart
- `/dr-departments` — by department/cost-center
- `/dr-intelligence` — full FP&A workbook
- `/dr-anomalies` — data quality check
