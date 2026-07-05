---
name: dr-revenue-trends
description: Revenue trends, growth rates, and composition from real aggregated monthly data. Self-contained — discovers the client's financials table and fields itself, no profile or setup step required.
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
  - Read
  - Write
argument-hint: "[--scenario <name>] [--year <YYYY>] [--breakdown <l1|l2>]"
---

# Revenue Trends

Analyze revenue patterns over time using real aggregated monthly data —
growth rates, peak/trough months, composition by sub-category, and
overall direction. Built on `get_aggregated_data_by_alias` (or its by-id
twin) — no row cap, real totals, not samples.

This skill is **self-contained**: it discovers the client's financials
table and field names itself (Step 2). It does not depend on
a saved profile, a learn step, or any prior setup — every Datarails
environment names its table and fields differently, so discovery
happens inline, once per conversation.

## Workflow

### Step 1: Verify Authentication

If a tool call fails with an auth or connection error, tell the user
to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect), then stop.

### Step 2: Discover the financials table and its fields

**If you already discovered these earlier in THIS conversation, reuse
them — skip to the next step.** Discovery is cheap but not free; do it
once per conversation, then carry the values forward.

1. `list_data_models`. Pick the financials table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Note **both** its numeric `id` and its `alias`
   (the alias may be empty). **Prefer the alias path when an alias
   exists** — friendlier field names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each
   field's numeric `id` — the by-id tools address fields by id). Bind
   these by case-insensitive match on the field alias/name (respecting
   the noted type):
   - `<amount_field>`       — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`     — categorical: `^scenario$` → `^version$`
   - `<date_field>`         — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_field>`   — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>`   — `dr_acc_l2` → `account_l2` (optional, for `--breakdown`)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

3. Resolve the P&L grain, then the revenue category value:
   `get_distinct_values_by_alias(<alias>, <account_l1_field>)` (or
   `get_distinct_values_by_id(<id>, <account_l1_field_id>)`). If the
   distinct call errors, fall back to `get_data_by_alias(<alias>,
   select=[<account_l1_field>], limit=500)` (or the by-id twin) and
   collect the distinct values.

   **Check the grain before matching** (data-scope preamble below,
   item 2): on many orgs the top account level is the balance-sheet
   equation (asset/liability/equity/income-style values), where an
   income-like bucket is the *entire* income statement — not revenue.
   If the distinct values look like the balance-sheet equation rather
   than revenue/COGS/opex-like P&L buckets, pull distinct values one
   level deeper and rebind: `<account_l1_field>` := the level whose
   values partition P&L flows, `<account_l2_field>` := the level below
   it. Every filter and breakdown below uses the rebound fields.

   Match `<revenue_value>` ← `/revenue|sales|income/i` **at the P&L
   grain** — accept an income-like value only when its siblings at the
   same level are COGS/opex-like line buckets, never when they are
   asset/liability/equity-like. If several candidates match, pick the
   broadest one at that grain; if genuinely ambiguous, ask the user
   once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`get_distinct_values_by_alias`/`_by_id`) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

### Step 3: Pull monthly revenue totals

Alias path (preferred):

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<date_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <account_l1_field>, "values": [<revenue_value>], "is_excluded": false},
    {"name": <scenario_field>, "values": [<scenario_value>], "is_excluded": false}
  ]
)
```

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>,
dimensions=[<date_field_id>], metrics=[{"field_id": <amount_field_id>,
"agg": "SUM"}], filters=[{"field_id": <account_l1_field_id>, "values":
[<revenue_value>]}, {"field_id": <scenario_field_id>, "values": [...]}])`.

Filter rules:
- **Scenario value:** `<scenario_value>` = `--scenario` when given
  (verify it exists in the discovered scenario domain — preamble
  item 1), else the actuals-like value from that domain. Never assume a
  scenario name exists.
- **Default period scope:** with no `--year`, do not pull all-time —
  scope to the latest complete fiscal year (or trailing 12 closed
  months) from the discovered date range (preamble item 3), using the
  same advanced `total_range` shape as below. Financials tables are
  multi-year cumulative; an unscoped total misleads.
- **Scoping by year:** if the user passed `--year`, you can either add
  `<date_field>` to `dimensions` and filter the result client-side, or
  pass an advanced date filter directly:
  `{"name": <date_field>, "values": {"type": "advanced", "val":
  [{"condition": "total_range", "value": ["<year_start_epoch>",
  "<year_end_epoch>"]}]}}` (epoch seconds as strings; use the org's
  fiscal-year boundaries — don't assume Jan–Dec). Both work — date
  filtering is no longer rejected.
- Value-list filters take `values: [...]` (set `is_excluded: true` for
  NOT-IN). The account category and the scenario field are the right
  shape.

### Step 4: Pull revenue composition (optional, if `--breakdown` or
data permits)

For a breakdown of revenue one level below the P&L grain (e.g. Product
vs Services), apply the **same period scope and scenario as Step 3** so
the composition matches the trend:

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<account_l2_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <account_l1_field>, "values": [<revenue_value>], "is_excluded": false},
    {"name": <scenario_field>, "values": [<scenario_value>], "is_excluded": false},
    <same period filter as Step 3>
  ]
)
```

By-id twin when there's no alias: `get_aggregated_data_by_id(...,
dimensions=[<account_l2_field_id>], metrics=[{"field_id":
<amount_field_id>, "agg": "SUM"}], filters=[...])`.

If `<account_l2_field>` is rejected (500), retry with a sibling
account-level field from the discovered schema (orgs often carry
in-between levels), fall back from the alias path to the by-id twin, or
skip this step and present top-level only. Note the limitation in the
output.

### Step 5: Pull KPI context (optional)

`list_business_metrics` to see whether the org publishes named revenue
KPIs (ARR / MRR / Net New ARR / Churn). It returns a flat list — each
entry has `id`, `name`, `description`, `category`, `kind`, `dimensions[]`,
and `status_info{}`. Filter that list client-side for revenue-related
metrics by name/category.

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

This is **discovery only** — `list_business_metrics` names the KPIs but
the metric-value tools aren't available here. P&L-derivable KPIs
(revenue, expense buckets, margins) can be numbered by aggregating the
financials table at the discovered P&L grain, using the same
`get_aggregated_data_by_alias` / `get_aggregated_data_by_id` shape as
above (the metric's `dimensions[]` and name tell you which category /
field to sum). SaaS/unit-economics KPIs cannot — if the catalog reports
one as populated, note it by name without a value (you can't fetch it
here); otherwise leave it out of the output entirely. KPI structures
vary heavily across orgs — read field names from the schema discovered in
Step 2, don't hardcode them.

### Step 6: Compute and present

First, clean the series: every aggregation response appends a trailing
**keyless grand-total row** — drop it from the monthly series and from
the composition rows before any math (left in, it becomes a phantom
month that corrupts MoM, growth, and shares; use it only as a checksum
against your client-side total). A `[null]` date bucket is unattributed
revenue — report it separately, never as a month in the trend.

Calculate from the monthly series (client-side):
- Total revenue across the period
- Average monthly revenue
- Peak and trough months
- Growth (first month → last month)
- MoM changes per month
- Direction label: growing / stable / declining

```
## Your Revenue Trends

Overview:
  Total Revenue: $[total]
  Scenario:      [scenario]
  Period:        [start] to [end]   ([N] months)

Monthly Trend:
| Month     | Revenue    | MoM Δ% |
|-----------|------------|--------|
| [month 1] | $[amount]  |    —   |
| [month 2] | $[amount]  |   +X%  |
| ...

Analysis:
  Direction:  [growing / stable / declining]
  Avg/month:  $[mean]
  Peak:       [month] at $[amount]
  Growth:     [first → last] = [X]%

[If --breakdown given and L2 succeeded:]
Composition:
| Source        | Amount     | Share |
|---------------|------------|-------|
| [source 1]    | $[amount]  | [X]%  |
| ...

[KPI Context — apply the "Render only KPIs you can source" rule
(Step 5). One line per KPI actually sourced; populated catalog metrics
whose values can't be fetched here appear by name only. Omit the whole
section if nothing was sourced — never print placeholder ARR/MRR/churn
figures:]
KPI Context:
  [KPI name]:    $[sourced amount]
  [KPI name]:    (populated metric — value not fetchable here)

Insights:
  - [Notable pattern or change]
  - [Recommendation based on the data]
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `--scenario <name>` | Scenario to analyze | The actuals-like value from the discovered scenario domain |
| `--year <YYYY>` | Restrict to one fiscal year (client-side filter on the date dimension) | Latest complete fiscal year (or trailing 12 closed months) |
| `--breakdown <l1\|l2>` | Composition breakdown depth | None (top-level only) |

## Data layers used

- Alias-first: aggregate via `get_aggregated_data_by_alias` when the
  table has an alias, falling back to `get_aggregated_data_by_id`.
- Date ranges filter directly via an advanced `total_range` filter
  (epoch-second strings); adding the date as a dimension and filtering
  client-side still works and is optional.
- Comparison / range filtering is available through advanced filters when
  you need it.

## Handling failures

**Aggregation field rejected (500):** retry with a sibling
account-level field from the discovered schema (orgs often carry
in-between levels), or fall back from the alias path to the by-id twin;
if none works, tell the user which field failed.

**No revenue category identifiable:** ask the user which category
represents revenue, given the discovered L1 values.

**Single period of data:** show the snapshot for that period instead
of a trend; note that trend analysis needs ≥2 periods.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-expense-analysis` — flip side
- `/dr-forecast-variance` — actuals vs budget vs forecast
- `/dr-intelligence` — full FP&A workbook
