---
name: dr-financial-summary
description: Quick snapshot of revenue, expenses, gross profit, and margin from real aggregated totals. Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__list_business_metrics
argument-hint: "[--scenario <name>] [--year <YYYY>]"
---

# Financial Summary

## What this skill does

A quick overview of the user's financial data — revenue, key expense
categories, gross profit, gross margin, monthly trend direction. Built for a
morning check-in or 30-second meeting prep. Uses `get_aggregated_data_by_alias`
(or its by-id twin) for real totals — no row caps, no estimation from samples.

This skill is **self-contained**: it discovers the client's financials table
and field names itself (Step 2). It does not depend on a
saved profile, a learn step, or any prior setup — every Datarails environment names its
table and fields differently, so discovery happens inline, once per
conversation.

## Workflow

### Step 1: Verify the connection

If any Datarails tool call fails with an authentication or connection error,
tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to
> the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user reconnects.

### Step 2: Discover the financials table and its fields

**If you already identified the financials table, its field names, and the
account categories earlier in THIS conversation, reuse them — skip to Step 3.**
Discovery is cheap but not free; do it once per conversation, then carry the
values forward.

1. `list_data_models`. Pick the financials table: the one whose name (or alias)
   matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest by
   row count. Note **both** its numeric `id` and its `alias` (the alias may be
   empty). **Prefer the alias path when an alias exists** — friendlier field
   names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<alias>)`; otherwise
   `get_fields_by_id(<financials_table_id>)` (capture each field's numeric `id`
   — the by-id tools address fields by id). Bind these by case-insensitive
   match on the field alias/name (respecting the noted type):
   - `<amount_field>`   — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>` — categorical: `^scenario$` → `^version$`
   - `<date_field>`     — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_field>`  — `dr_acc_l1` → `account_l1` → `account_group_l1`

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue.

3. Find the revenue / COGS / opex category values:
   `get_distinct_values_by_alias(<alias>, <account_field>)` (or
   `get_distinct_values_by_id(<id>, <account_field_id>)`). If the distinct call
   errors, fall back to `get_data_by_alias(<alias>, select=[<account_field>],
   limit=500)` (or the by-id twin) and collect the distinct values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once.

### Step 3: Aggregate totals by account category

Alias path (preferred):

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<account_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <scenario_field>, "values": [<--scenario> or "Actuals"], "is_excluded": false}
  ]
)
```

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>,
dimensions=[<account_field_id>], metrics=[{"field_id": <amount_field_id>, "agg":
"SUM"}], filters=[{"field_id": <scenario_field_id>, "values": [...]}])`.

Filter rules:
- **Scoping by year:** if the user passed `--year`, you can either add
  `<date_field>` to `dimensions` and filter the result client-side, or pass an
  advanced date filter directly:
  `{"name": <date_field>, "values": {"type": "advanced", "val": [{"condition":
  "total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}` (epoch seconds
  as strings). Both work — date filtering is no longer rejected.
- Value-list filters take `values: [...]` (set `is_excluded: true` for NOT-IN).

**If the call fails on `<account_field>` with a 500:** that field isn't usable
as a dimension for this client. Re-inspect the Step 2 schema for a sibling
(e.g. `DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`) and retry.
If the alias call errors, retry the by-id twin. If no sibling works, tell the
user which field failed.

### Step 4: Pull the monthly trend

Same call shape with the date added as a dimension:

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<date_field>, <account_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[{"name": <scenario_field>, "values": ["Actuals"], "is_excluded": false}]
)
```

Compute direction (growing / stable / declining), peak month, and most recent
value client-side from the time series.

### Step 5: Present the snapshot

Filter the Step 3 aggregate to the revenue / COGS / opex categories using the
values discovered in Step 2:

```
## Your Financial Snapshot

Real Totals (<scenario>):
- Revenue:                 $[sum of rows where account == <revenue_value>]
- Cost of Goods Sold:      $[sum of rows where account == <cogs_value>]
- Operating Expenses:      $[sum of rows where account == <opex_value>]
- Gross Profit:            $[Revenue - COGS]
- Gross Margin:            [Gross Profit / Revenue]%

Monthly Trend:
- [N] months of data
- Most recent month: [month] — Revenue $[amount]
- Direction: [Growing / Stable / Declining]

Want to dig deeper?
- /dr-revenue-trends     — revenue trends over time
- /dr-expense-analysis   — detailed expense breakdown
- /dr-forecast-variance  — actuals vs budget vs forecast
- /dr-anomalies          — data quality check
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `--scenario <name>` | Scenario to summarize | `Actuals` |
| `--year <YYYY>` | Filter to one fiscal year (date dimension + client-side filter, or an advanced date-range filter) | All available |

## Handling failures

**Connection / auth error on any call:** surface the reconnect message from
Step 1 and STOP.

**No table matches the financials pattern in Step 2:** list the tables you
found and ask the user which one holds their P&L / financial data, then
continue.

**Aggregation rejected on `<account_field>` (500) at Step 3:** swap to a
sibling field from the Step 2 schema, or fall back from the alias path to the
by-id twin, and retry (see Step 3). Discover lazily, fall back reactively.

**A category value isn't found in Step 2.3:** present what you have and note
which category (revenue/COGS/opex) couldn't be resolved, rather than guessing.

## Related skills

- `/dr-revenue-trends` — deeper revenue narrative with composition
- `/dr-expense-analysis` — top expense categories and concentration
- `/dr-intelligence` — full FP&A workbook
