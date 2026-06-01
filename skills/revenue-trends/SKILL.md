---
name: dr-revenue-trends
description: Revenue trends, growth rates, and composition from real aggregated monthly data. Self-contained — discovers the client's financials table and fields itself, no profile or setup step required.
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

# Revenue Trends

Analyze revenue patterns over time using real aggregated monthly data —
growth rates, peak/trough months, composition by sub-category, and
overall direction. Built on `aggregate_table_data` (no row cap, real
totals), not on samples.

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

1. `list_finance_tables`. Pick the financials table: the one whose name
   matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Call it `<financials_table_id>`.

2. `get_table_schema(<financials_table_id>)`. Bind these by
   case-insensitive name match (respecting the noted type):
   - `<amount_field>`       — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`     — categorical: `^scenario$` → `^version$`
   - `<date_field>`         — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_field>`   — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>`   — `dr_acc_l2` → `account_l2` (optional, for `--breakdown`)

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

3. Find the revenue category value. The distinct-values API often
   returns 409, so call `get_sample_records(<financials_table_id>,
   limit=500)` and collect the distinct `<account_l1_field>` values.
   Match `<revenue_value>` ← `/revenue|sales|income/i`. If several
   candidates match, pick the broadest top-level one; if genuinely
   ambiguous, ask the user once.

Aggregation-field failures are handled reactively (see below), not
pre-probed.

### Step 3: Pull monthly revenue totals

```
table_id: <financials_table_id>
dimensions: ["<date_field>"]
metrics: [{"field": "<amount_field>", "agg": "SUM"}]
filters: [
  {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": false},
  {"name": "<scenario_field>", "values": ["<scenario or Actuals>"], "is_excluded": false}
]
```

Filter rules:
- **Date fields go in `dimensions`, never `filters`.** The filter API
  silently returns empty for date columns.
- **Only text fields go in filters.** The account category and the
  scenario field are the right shape.
- For range filtering (e.g. specific year), include the date as a
  dimension and filter client-side. The backend rejects comparison
  operators with `unsupported_filter_operators`.

### Step 4: Pull revenue composition (optional, if `--breakdown` or
data permits)

For L1 breakdown of revenue (e.g. Product vs Services):

```
dimensions: ["<account_l2_field>"]
metrics: [{"field": "<amount_field>", "agg": "SUM"}]
filters: [
  {"name": "<account_l1_field>", "values": ["<revenue_value>"], "is_excluded": false},
  {"name": "<scenario_field>", "values": ["Actuals"], "is_excluded": false}
]
```

If `<account_l2_field>` is rejected (500), retry with a sibling account
field from the discovered schema (e.g. `DR_ACC_L1.5`) or skip this step
and present top-level only. Note the limitation in the output.

### Step 5: Pull KPI context (optional, if a KPI/metrics table was found)

If you found a KPI/metrics table in the discovery step, fetch sample
records or aggregate ARR / MRR / Net New ARR / Churn for the same
period. KPI tables vary heavily across orgs — discover the field names
from the schema, don't hardcode them.

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

## Backward compatibility

- Uses only raw-tables MCP tools (always available).
- Date filtering is client-side (API rejects date filters).
- Range / comparison filtering is not used — comparisons are rejected
  by the backend filter API.

## Handling failures

**Aggregation field rejected (500):** retry with a sibling account
field from the discovered schema (e.g. `DR_ACC_L1.5`); if none works,
tell the user which field failed.

**No revenue category identifiable:** ask the user which category
represents revenue, given the discovered L1 values.

**Single period of data:** show the snapshot for that period instead
of a trend; note that trend analysis needs ≥2 periods.

## Related skills

- `/dr-financial-summary` — top-level snapshot
- `/dr-expense-analysis` — flip side
- `/dr-forecast-variance` — actuals vs budget vs forecast
- `/dr-intelligence` — full FP&A workbook
