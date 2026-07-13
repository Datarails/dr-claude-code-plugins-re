---
name: dr-financial-summary
description: Quick snapshot of revenue, expenses, gross profit, and margin from real aggregated totals. Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
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
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__list_business_metrics
argument-hint: "[--scenario <name>] [--year <YYYY>]"
---

# Financial Summary

## What this skill does

A quick overview of the user's financial data — revenue, key expense
categories, gross profit, gross margin, monthly trend direction. Built for a
morning check-in or 30-second meeting prep. Uses the aggregation start→poll
tools (`start_aggregation_by_alias` → `get_aggregation_result_by_alias`, or
their by-id twins) for real totals — no row caps, no estimation from samples.
Totals default to the latest complete fiscal year (or trailing 12 closed
months), never an unscoped all-time figure, and every snapshot is labeled with
the period and scenario it covers.

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
   - `<account_level_fields>` — categorical: **every** account-hierarchy level
     field (alias/name matching an account word with a level-like suffix, e.g.
     `/acc(ount)?.*l\d/i`). Keep all levels as candidates — `<account_field>`
     (the P&L grain) is chosen in item 3, not here.

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

3. Apply the data-scope preamble above to bind the query scope:

   - **Scenario** (preamble item 1): from the discovered scenario domain, bind
     `<scenario_value>` ← the value matching `--scenario` case-insensitively
     when given, else the actuals-like value (`/actual/i`). If `--scenario`
     matches nothing in the domain, list the scenarios that do exist and ask.
   - **P&L grain** (preamble item 2): pull distinct values of each
     `<account_level_fields>` candidate —
     `start_distinct_values_by_alias(<alias>, <field>)` (or
     `start_distinct_values_by_id(<id>, <field_id>)`) → poll the matching
     `get_distinct_values_result_by_*(handle)` until ready (async-fetch
     pattern); if a distinct call errors,
     fall back to `get_data_by_alias(<alias>, select=[<field>], limit=500)` (or
     the by-id twin) and collect the distinct values. Bind `<account_field>` to
     the level whose values partition P&L flows into revenue/COGS/opex-like
     buckets — do **not** assume the top level does. Then match within the
     chosen level's values:
     - `<revenue_value>` ← `/revenue|sales|income/i`
     - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
     - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

     Every total in this skill is scoped to those P&L flows — balance-sheet
     buckets stay out of the snapshot. If a category has several candidates at
     the chosen level, pick the broadest one; if genuinely ambiguous, ask the
     user once.
   - **Period** (preamble item 3): discover the date field's range, then bind
     `<period_start_epoch>` / `<period_end_epoch>` to the default scope — the
     latest complete fiscal year, or the trailing 12 closed months when the
     fiscal-year boundary is unclear — unless `--year` overrides the bounds.
     Keep a human-readable `<period_label>` (e.g. `FY2025 (Jan–Dec 2025)`) for
     the output.

### Step 3: Aggregate totals by account category

Alias path (preferred):

```
start_aggregation_by_alias(
  alias=<financials_alias>,
  dimensions=[<account_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <scenario_field>, "values": [<scenario_value>], "is_excluded": false},
    {"name": <date_field>, "values": {"type": "advanced", "val": [{"condition":
      "total_range", "value": ["<period_start_epoch>", "<period_end_epoch>"]}]}}
  ]
)
```

→ poll `get_aggregation_result_by_alias(handle)` until ready (async-fetch
pattern).

By-id fallback (no alias): `start_aggregation_by_id(table_id=<id>,
dimensions=[<account_field_id>], metrics=[{"field_id": <amount_field_id>, "agg":
"SUM"}], filters=[...])` → poll `get_aggregation_result_by_id(handle)` until
ready — same scenario + date filters, keyed by `field_id`.

Filter rules:
- **The period filter is always on:** the advanced `total_range` date filter
  above (epoch seconds as strings) carries the Step 2 default — latest complete
  fiscal year / trailing 12 closed months — or the `--year` bounds when given.
  Never run this aggregate unscoped: the table is multi-year cumulative, and an
  all-time total misreads stock as flow.
- Value-list filters take `values: [...]` (set `is_excluded: true` for NOT-IN).

**Reading the response (preamble item 4):** drop the trailing **keyless
grand-total row** before summing or computing shares — at most use it as a
checksum against the bucket sum — and read null groups only from the explicit
`[null]` bucket.

**If the call fails on `<account_field>` with a 500:** that field isn't usable
as a dimension for this client. Re-inspect the Step 2 schema for a sibling
hierarchy level (e.g. a half-level or account-group variant adjacent to the
chosen level), re-check that its values still partition P&L flows (preamble
item 2), and retry. If the alias call errors, retry the by-id twin. If no
sibling works, tell the user which field failed.

### Step 4: Pull the monthly trend

Same call shape — same scenario + period filters — with the date added as a
dimension:

```
start_aggregation_by_alias(
  alias=<financials_alias>,
  dimensions=[<date_field>, <account_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <scenario_field>, "values": [<scenario_value>], "is_excluded": false},
    {"name": <date_field>, "values": {"type": "advanced", "val": [{"condition":
      "total_range", "value": ["<period_start_epoch>", "<period_end_epoch>"]}]}}
  ]
)
```

→ poll `get_aggregation_result_by_alias(handle)` until ready (async-fetch
pattern).

Drop the keyless grand-total row first (preamble item 4) — it is not a month —
then compute direction (growing / stable / declining), peak month, and most
recent value client-side from the time series.

### Step 5: Present the snapshot

Filter the Step 3 aggregate to the revenue / COGS / opex categories using the
values discovered in Step 2:

```
## Your Financial Snapshot

Period: <period_label> · Scenario: <scenario_value>

Real Totals:
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
| `--scenario <name>` | Scenario to summarize (must exist in the discovered scenario domain) | The discovered actuals-like scenario |
| `--year <YYYY>` | Scope to one fiscal year via the advanced date-range filter | Latest complete fiscal year (trailing 12 closed months when the fiscal-year boundary is unclear) |

## Handling failures

**Connection / auth error on any call:** surface the reconnect message from
Step 1 and STOP.

**No table matches the financials pattern in Step 2:** list the tables you
found and ask the user which one holds their P&L / financial data, then
continue.

**Aggregation rejected on `<account_field>` (500) at Step 3:** swap to a
sibling field from the Step 2 schema, or fall back from the alias path to the
by-id twin, and retry (see Step 3). Discover lazily, fall back reactively.

**`--scenario` (or the actuals-like default) isn't in the discovered scenario
domain:** list the scenarios that do exist and ask which to use — never filter
on an assumed scenario name.

**No hierarchy level partitions P&L flows, or a category value isn't found at
the chosen grain (Step 2.3):** present what you have, note which category
(revenue/COGS/opex) couldn't be resolved, and never substitute a balance-sheet
bucket for it.

## Related skills

- `/dr-revenue-trends` — deeper revenue narrative with composition
- `/dr-expense-analysis` — top expense categories and concentration
- `/dr-intelligence` — full FP&A workbook
