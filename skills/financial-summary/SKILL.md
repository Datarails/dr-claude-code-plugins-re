---
name: dr-financial-summary
description: Quick snapshot of revenue, expenses, gross profit, and margin from real aggregated totals. Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
argument-hint: "[--scenario <name>] [--year <YYYY>]"
---

# Financial Summary

## What this skill does

A quick overview of the user's financial data — revenue, key expense
categories, gross profit, gross margin, monthly trend direction. Built for a
morning check-in or 30-second meeting prep. Uses `aggregate_table_data` for
real totals (no row caps, no estimation from samples).

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

1. `list_finance_tables`. Pick the financials table: the one whose name
   matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest by
   row count. Call it `<financials_table_id>`.

2. `get_table_schema(<financials_table_id>)`. From the fields, bind these by
   case-insensitive name match (respecting the noted type):
   - `<amount_field>`   — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>` — categorical: `^scenario$` → `^version$`
   - `<date_field>`     — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_field>`  — `dr_acc_l1` → `account_l1` → `account_group_l1`

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue.

3. Find the revenue / COGS / opex category values. The distinct-values API
   often returns 409, so call `get_sample_records(<financials_table_id>,
   limit=500)` and collect the distinct `<account_field>` values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once.

### Step 3: Aggregate totals by account category

```
aggregate_table_data(
  table_id=<financials_table_id>,
  dimensions=[<account_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <scenario_field>, "values": [<--scenario> or "Actuals"], "is_excluded": false}
  ]
)
```

Filter rules:
- **Date fields must be dimensions, never filters.** Stored as epoch ints —
  date filters silently return empty. If the user passed `--year`, include
  `<date_field>` in `dimensions` and filter client-side.
- **Only text fields in filters.**

**If the call fails on `<account_field>` with a 500:** that field isn't
usable as a dimension for this client. Re-inspect the Step 2 schema for a
sibling (e.g. `DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`)
and retry with it. If no sibling works, tell the user which field failed.

### Step 4: Pull the monthly trend

Same call shape with the date added as a dimension:

```
aggregate_table_data(
  table_id=<financials_table_id>,
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
| `--year <YYYY>` | Filter to one fiscal year (applied client-side after the date dimension is pulled) | All available |

## Handling failures

**Connection / auth error on any call:** surface the reconnect message from
Step 1 and STOP.

**No table matches the financials pattern in Step 2:** list the tables you
found and ask the user which one holds their P&L / financial data, then
continue.

**Aggregation rejected on `<account_field>` (500) at Step 3:** swap to a
sibling field from the Step 2 schema and retry (see Step 3). This replaces
the old pre-probe approach — discover lazily, fall back reactively.

**A category value isn't found in Step 2.3:** present what you have and note
which category (revenue/COGS/opex) couldn't be resolved, rather than guessing.

## Related skills

- `/dr-revenue-trends` — deeper revenue narrative with composition
- `/dr-expense-analysis` — top expense categories and concentration
- `/dr-intelligence` — full FP&A workbook
