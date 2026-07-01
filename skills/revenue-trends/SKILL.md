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

3. Find the revenue category value:
   `get_distinct_values_by_alias(<alias>, <account_l1_field>)` (or
   `get_distinct_values_by_id(<id>, <account_l1_field_id>)`). If the
   distinct call errors, fall back to `get_data_by_alias(<alias>,
   select=[<account_l1_field>], limit=500)` (or the by-id twin) and
   collect the distinct values. Match `<revenue_value>` ←
   `/revenue|sales|income/i`. If several candidates match, pick the
   broadest top-level one; if genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

### Step 3: Pull monthly revenue totals

Alias path (preferred):

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<date_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <account_l1_field>, "values": [<revenue_value>], "is_excluded": false},
    {"name": <scenario_field>, "values": [<--scenario> or "Actuals"], "is_excluded": false}
  ]
)
```

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>,
dimensions=[<date_field_id>], metrics=[{"field_id": <amount_field_id>,
"agg": "SUM"}], filters=[{"field_id": <account_l1_field_id>, "values":
[<revenue_value>]}, {"field_id": <scenario_field_id>, "values": [...]}])`.

Filter rules:
- **Scoping by year:** if the user passed `--year`, you can either add
  `<date_field>` to `dimensions` and filter the result client-side, or
  pass an advanced date filter directly:
  `{"name": <date_field>, "values": {"type": "advanced", "val":
  [{"condition": "total_range", "value": ["<jan1_epoch>",
  "<dec31_epoch>"]}]}}` (epoch seconds as strings). Both work — date
  filtering is no longer rejected.
- Value-list filters take `values: [...]` (set `is_excluded: true` for
  NOT-IN). The account category and the scenario field are the right
  shape.

### Step 4: Pull revenue composition (optional, if `--breakdown` or
data permits)

For L1 breakdown of revenue (e.g. Product vs Services):

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<account_l2_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <account_l1_field>, "values": [<revenue_value>], "is_excluded": false},
    {"name": <scenario_field>, "values": ["Actuals"], "is_excluded": false}
  ]
)
```

By-id twin when there's no alias: `get_aggregated_data_by_id(...,
dimensions=[<account_l2_field_id>], metrics=[{"field_id":
<amount_field_id>, "agg": "SUM"}], filters=[...])`.

If `<account_l2_field>` is rejected (500), retry with a sibling account
field from the discovered schema (e.g. `DR_ACC_L1.5`), fall back from the
alias path to the by-id twin, or skip this step and present top-level
only. Note the limitation in the output.

### Step 5: Pull KPI context (optional)

`list_business_metrics` to see whether the org publishes named revenue
KPIs (ARR / MRR / Net New ARR / Churn). It returns a flat list — each
entry has `id`, `name`, `description`, `category`, `kind`, `dimensions[]`,
and `status_info{}`. Filter that list client-side for revenue-related
metrics by name/category.

This is **discovery only** — `list_business_metrics` names the KPIs but
the metric-value tools aren't available here. To put a number against a
KPI, aggregate it from the financials table using the same
`get_aggregated_data_by_alias` / `get_aggregated_data_by_id` shape as
above (the metric's `dimensions[]` and name tell you which category /
field to sum), or note the KPI by name without a value. KPI structures
vary heavily across orgs — read field names from the schema discovered in
Step 2, don't hardcode them.

### Step 6: Compute and present

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
  Total Revenue (Actuals): $[total]
  Period: [start] to [end]   ([N] months)

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

[If KPI table available:]
KPI Context:
  ARR:           $[amount]
  Net New ARR:   $[amount]
  Churn rate:    [X]%

Insights:
  - [Notable pattern or change]
  - [Recommendation based on the data]
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `--scenario <name>` | Scenario to analyze | `Actuals` |
| `--year <YYYY>` | Restrict to one fiscal year (client-side filter on the date dimension) | All available |
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

**Aggregation field rejected (500):** retry with a sibling account
field from the discovered schema (e.g. `DR_ACC_L1.5`), or fall back from
the alias path to the by-id twin; if none works, tell the user which
field failed.

**No revenue category identifiable:** ask the user which category
represents revenue, given the discovered L1 values.

**Single period of data:** show the snapshot for that period instead
of a trend; note that trend analysis needs ≥2 periods.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-expense-analysis` — flip side
- `/dr-forecast-variance` — actuals vs budget vs forecast
- `/dr-intelligence` — full FP&A workbook
