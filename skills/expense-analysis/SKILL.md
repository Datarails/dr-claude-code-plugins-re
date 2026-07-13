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
  - mcp__datarails-finance-os__start_aggregation_by_alias
  - mcp__datarails-finance-os__get_aggregation_result_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__start_aggregation_by_id
  - mcp__datarails-finance-os__get_aggregation_result_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__start_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_result_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__start_distinct_values_by_id
  - mcp__datarails-finance-os__get_distinct_values_result_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__list_business_metrics
  - Read
  - Write
argument-hint: "[--scenario <name>] [--year <YYYY>] [--breakdown <l1|l2>]"
---

# Expense Analysis

Where the money is going — top expense categories with complete
totals (not sample estimates), monthly trend, and concentration
analysis. Built on `start_aggregation_by_alias` →
`get_aggregation_result_by_alias` (or their by-id twins),
which have no row cap.

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
   - `<account_level_fields>` — categorical, one per hierarchy level:
     `dr_acc_l\d` → `account_l\d` → `account_group_l\d` (collect every
     level you find — L0/L1/L2-like; the working grain among them is
     picked in item 3, and the next level down serves as breakdown
     depth)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

3. Find the expense-side account values — **at the right grain** (see
   the data-scope preamble below, item 2). Pull distinct values of each
   account-hierarchy level field:
   `start_distinct_values_by_alias(<alias>, <account_field>)` (or
   `start_distinct_values_by_id(<id>, <account_field_id>)`) → poll the
   matching `get_distinct_values_result_by_*(handle)` until ready
   (async-fetch pattern). If a
   distinct call errors, fall back to `get_data_by_alias(<alias>,
   select=[<account_field>], limit=500)` (or the by-id twin) and
   collect the distinct values. Pick the level whose values partition
   P&L flows into revenue/COGS/opex-like buckets — on many orgs the
   top level is the balance-sheet equation and the P&L line items live
   one level deeper. Call the chosen level `<expense_grain_field>` and
   the next level down (if any) `<expense_detail_field>`. At that
   grain, bind over the DISCOVERED values:
   - `<expense_values>` ← every P&L bucket matching
     `/cogs|cost|expense|opex|sg&a/i` — this **include-list** is what
     "expenses" means below. Never define expenses as "everything
     except revenue": on real orgs that sweeps balance-sheet buckets
     into the ranking.
   - `<revenue_value>`  ← `/revenue|sales|income/i` (kept out of the
     expense list; useful for context ratios)
   - Balance-sheet buckets (`/asset|liabilit|equity/i`) are excluded
     entirely — never report them as expenses.

   If a bucket has several candidates, pick the broadest top-level
   one; if genuinely ambiguous (or nothing expense-like matches at any
   level), ask the user once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

### Step 3: Pull totals by expense category

Scope first (data-scope preamble, items 1 and 3): scenario =
`--scenario` if given, else the actuals-like value (`/actual/i`) from
the discovered scenario domain; period = the latest complete fiscal
year (or trailing 12 closed months) unless `--year` narrows it —
never an unscoped all-time total. Default breakdown is
`<expense_grain_field>` × `<expense_detail_field>` if a deeper level
exists, otherwise the grain field alone.

Alias path (preferred):

```
start_aggregation_by_alias(
  alias=<financials_alias>,
  dimensions=["<expense_grain_field>", "<expense_detail_field>"],
  metrics=[{"field": "<amount_field>", "agg": "SUM"}],
  filters=[
    {"name": "<scenario_field>", "values": ["<discovered actuals-like scenario>"], "is_excluded": false},
    {"name": "<expense_grain_field>", "values": [<expense_values>], "is_excluded": false},
    <period filter on <date_field> — see Date scoping below>
  ]
)
```

→ poll `get_aggregation_result_by_alias(handle)` until ready
(async-fetch pattern).

By-id fallback (no alias): `start_aggregation_by_id(table_id=<id>,
dimensions=[<expense_grain_field_id>, <expense_detail_field_id>],
metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}],
filters=[{"field_id": <scenario_field_id>, "values": [...]},
{"field_id": <expense_grain_field_id>, "values": [<expense_values>],
"is_excluded": false}, <period filter>])` → poll
`get_aggregation_result_by_id(handle)` until ready.

Filter rules:
- **Value-list filters** match any of the listed values — expenses are
  an *include-list* of the discovered `<expense_values>`, never a
  NOT-IN of revenue (that would sweep balance-sheet buckets into the
  ranking). `is_excluded: true` turns a list into NOT-IN when you
  genuinely need one.
- **Date scoping** can go in `filters` directly via an advanced
  `total_range` condition (epoch-second strings), or you can add
  `<date_field>` to `dimensions` and filter client-side — both work;
  apply the default period scope one of these two ways.
- **Comparisons, ranges, text matching, and null checks** are all
  supported via advanced filters (see the `--year` note below).

If the detail-level field is rejected: retry without it (group by
`<expense_grain_field>` only) and note the limitation in the output.

### Step 4: Pull monthly expense trend

Same scenario and period scope as Step 3.

```
start_aggregation_by_alias(
  alias=<financials_alias>,
  dimensions=["<date_field>", "<expense_grain_field>"],
  metrics=[{"field": "<amount_field>", "agg": "SUM"}],
  filters=[
    {"name": "<scenario_field>", "values": ["<discovered actuals-like scenario>"], "is_excluded": false},
    {"name": "<expense_grain_field>", "values": [<expense_values>], "is_excluded": false}
  ]
)
```

→ poll `get_aggregation_result_by_alias(handle)` until ready
(async-fetch pattern).

(By-id twin: `start_aggregation_by_id` with field ids and
`metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]` → poll
`get_aggregation_result_by_id(handle)`.)

### Step 5: Compute concentration and present

Before computing anything, apply the aggregate-reading rule
(data-scope preamble, item 4): drop the trailing **keyless
grand-total row** from every aggregation response — it is not a
category; exclude it from totals, shares, rankings, and bucket counts
(at most use it as a checksum against your own sum). Null groups
arrive as an explicit `[null]` bucket — surface them as "(unmapped)"
rather than silently merging or dropping them.

Calculate client-side from the grain × detail result:
- Total expenses
- Top N categories by absolute amount
- Each category's share of total (concentration)
- Categories above 20% of total → concentration flag
- From the monthly series: direction, highest/lowest month, MoM
  changes

```
## Your Expense Analysis
Scenario: [scenario] · Period: [period covered]

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
| `--scenario <name>` | Scenario to analyze | Actuals-like value from the discovered scenario domain |
| `--year <YYYY>` | Restrict to one fiscal year (advanced `total_range` date filter, or a date dimension + client-side filter) | Latest complete fiscal year (or trailing 12 closed months) |
| `--breakdown <l1\|l2>` | Hierarchy depth for the category table (grain only vs grain + one level deeper) | `l2` if a deeper level exists, else `l1` |

## Backward compatibility

- Alias-first: uses the by-alias data tools when the table has an alias,
  and falls back to the by-id twins otherwise (both always available).
- Date ranges filter directly via an advanced `total_range` filter, or
  by adding the date as a dimension and filtering client-side.
- Comparison, range, text-matching, and null filter operators are
  available via advanced filters if a narrower scope is needed.

## Handling failures

**Detail-level field rejected (500):** retry grouping by
`<expense_grain_field>` only (or a sibling account-level field from
the discovered schema); note the reduced depth in the output. If no
field works, tell the user which field failed. If an alias call
errors, retry the by-id twin.

**Expense buckets ambiguous:** ask the user which account values at
the chosen grain represent expenses (COGS/OpEx-like) — never fall
back to "everything except revenue", which mislabels balance-sheet
buckets as expenses.

**All aggregation fails:** fall back to `get_data_by_alias` (or
`get_data_by_id`) with the scenario as a value-list filter (500-row
cap). Note that totals are partial.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-revenue-trends` — revenue counterpart
- `/dr-departments` — by department/cost-center
- `/dr-intelligence` — full FP&A workbook
- `/dr-anomalies` — data quality check
