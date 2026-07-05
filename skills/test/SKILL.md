---
name: dr-test
description: Test API field compatibility and performance. Discovers which fields work with aggregation and suggests sibling alternatives for failed fields, then reports the results. Self-contained — discovers the client's financials table and candidate fields on its own, no profile or setup step required.
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
  - Write
  - Read
  - Bash
argument-hint: ""
---

# API Diagnostic & Field Compatibility Test

Test which fields work with the aggregation API for a specific environment.
Discovers field compatibility and suggests sibling alternatives for failed
fields, then reports the results to the user.

This skill is **self-contained**: discovering which fields work as
aggregation dimensions is its whole job, so it finds the financials table and
its candidate fields itself (inline, Step 2). It does not depend on
a saved profile, a learn step, or any prior setup — and it does **not**
write its findings to disk; it reports them in-conversation so the current
session (and any skill that reuses the discovered table/fields) can act on
them.

## Purpose

The Datarails aggregation API works for nearly all fields — an all-PASS
result is the norm — but occasionally a field fails per-client (500 errors).
This skill:
1. Discovers the financials table and its candidate categorical fields
2. Tests each candidate field against aggregation
3. Reports pass/fail with timing
4. Discovers sibling alternatives for those that fail
5. Reports the full compatibility result to the user (which fields work as
   dimensions, which 500, and the suggested sibling for each failure)

## Arguments

No arguments required. Uses the currently authenticated environment.

## What this skill discovers and reports

This skill discovers everything it needs inline and **reports** the result —
it does not persist anything to disk.

### What It Discovers (inline, Step 2)
- The financials table to test against (`list_data_models`)
- The candidate categorical fields to test (`list_aliased_fields` if the
  table has an alias, else `get_fields_by_id`)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

### What It Reports (to the user, Phase 5)
- Whether aggregation works at all for this table
- Which fields PASS as aggregation dimensions and which FAIL (500)
- The suggested sibling alternative for each failed field — a sibling
  account-level field from the discovered schema (orgs often carry
  in-between levels)
- When the test was run

Run this skill whenever a downstream skill reports an unexpected aggregation
failure, after a schema change, or to learn the field-compatibility map for
an environment up front. The reported map applies to the current session;
other skills handle field failures reactively (swap to a sibling and retry)
on their own.

## Workflow

### Phase 1: Setup

#### Step 1: Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

#### Step 2: Discover the financials table

**If you already discovered the financials table earlier in THIS
conversation, reuse it — skip to Phase 2.** Discovery is cheap but not free;
do it once per conversation.

1. `list_data_models`. Pick the financials table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Note **both** its numeric `id` (call it
   `<financials_table_id>`) and its `alias` (call it `<financials_alias>` —
   the alias may be empty). **Prefer the alias path when an alias exists** —
   friendlier field names, far fewer tokens. (If nothing matches, list the
   tables you found and ask the user which one holds their financial data.)

This skill's whole purpose is to probe which of this table's fields work as
aggregation dimensions, so the candidate field list is built directly from
the live schema in Phase 2 — there's no saved profile to read from.

### Phase 2: Discovery

#### Step 3: Get Full Schema

If the table has an alias, list its fields by alias:
```
Use: mcp__datarails-finance-os__list_aliased_fields
alias: <financials_alias>
```

Otherwise list fields by id (capture each field's numeric `id` — the by-id
tools address fields by id):
```
Use: mcp__datarails-finance-os__get_fields_by_id
table_id: <financials_table_id>
```

From the schema, also bind the two fields the probe call itself needs (by
case-insensitive name/alias match, respecting type):
- `<amount_field>`   — numeric metric: `^amount$` → `transaction_amount` → `value`
- `<scenario_field>` — categorical filter: `^scenario$` → `^version$`

If neither chain matches (e.g. non-English field names), show the schema's
field list and ask the user which fields hold the amount and the scenario.

Then build the list of candidate categorical/string fields to test —
**every** categorical/string field in the schema is a candidate. Don't skip
any; discovering which ones work is the point.

#### Step 4: Build Test Plan

Order the candidate fields so the most useful ones are probed first (the test
still covers all of them):
1. `<scenario_field>`
2. the date field (`reporting_date` → `posting_date` → `^date$`)
3. account-hierarchy fields, matched case-insensitively from the schema —
   e.g. `DR_ACC_L0`, `DR_ACC_L1`, `DR_ACC_L2`, plus any sibling/alternate
   account-level fields the discovered schema carries (orgs often have
   in-between levels)
4. department / cost-center fields if present
5. every other categorical field from the schema

When a primary account level is in the list, make sure any sibling
account-level fields from the discovered schema (orgs often carry in-between
levels) are also in the candidate list so Step 6 can suggest a working
alternative.

### Phase 3: Aggregation Testing

#### Step 5: Test Each Field

**Aggregation rules:**
- Any field can be probed as a `dimensions` entry — date fields included.
  Date columns now also filter directly via an **advanced** filter
  (`total_range` with epoch-second strings), so a date dimension is optional,
  not mandatory.
- To limit to a specific period you can add the date as a dimension and filter
  client-side, or pass an advanced date-range filter directly.
- Text fields (`Scenario`, `Account Group L0`, etc.) go in `filters` as a
  value list, the same as before.

For each field, run the alias-path probe when the table has an alias:
```
Use: mcp__datarails-finance-os__get_aggregated_data_by_alias
Parameters:
  alias: <financials_alias>
  dimensions: ["<field_alias>"]
  metrics: [{"field": "<amount_field>", "agg": "SUM"}]
  filters: [
    {"name": "<scenario_field>", "values": ["<scenario_value>"], "is_excluded": false}
  ]
```

By-id probe (no alias — `dimensions` and `metrics`/`filters` are field-id based):
```
Use: mcp__datarails-finance-os__get_aggregated_data_by_id
Parameters:
  table_id: <financials_table_id>
  dimensions: [<field_id>]
  metrics: [{"field_id": <amount_field_id>, "agg": "SUM"}]
  filters: [
    {"field_id": <scenario_field_id>, "values": ["<scenario_value>"]}
  ]
```

`<scenario_value>` is any value from the discovered scenario domain
(commonly an actuals-like one) — it just keeps each probe cheap; the probe is
testing whether the *dimension* field aggregates, not the filter. If a probe returns empty (rather than 500) for every field, the
scenario value may differ for this client — drop the filter and re-probe, or
use a scenario value seen in a quick `get_data_by_alias` / `get_data_by_id`
pull (small `limit`).

Record for each field (in memory, for the session — nothing is written to
disk):
- **Status:** PASS or FAIL
- **Groups returned:** Number of distinct values (if PASS)
- **Error:** Error message (if FAIL)

#### Step 6: Identify Alternatives

For each failed field (especially account-hierarchy levels like `DR_ACC_L1`,
`DR_ACC_L2`):
- Look for sibling fields in the schema (e.g., an alternate/in-between
  account level such as `Account_L1_Alt`)
- Probe those siblings the same way
- If a sibling works, note it as the suggested alternative for the failed
  field (this goes into the report in Phase 5, not into any file)

### Phase 4: Report the Results

This skill **does not persist anything** — no profile, no disk cache. It
reports the compatibility map directly to the user (and optionally drops a
diagnostic text file in `tmp/`). The in-conversation report is the deliverable:
the current session and any sibling skill reusing the discovered table/fields
can act on it immediately, and other skills already fall back reactively
(swap to a sibling and retry) when a field 500s.

#### Step 7: (Optional) Save a Diagnostic File

For the user's records, you may write a plain-text copy of the results to
`tmp/` (gitignored session artifact — not a profile, not read back by any
skill):

```
Use: Write
file_path: tmp/API_Diagnostic_<table_name>_<timestamp>.txt
```

### Phase 5: Present Results

#### Step 8: Show Summary

Display results. The block below is **illustrative — your org's field names,
group counts, and pass/fail results will differ**; an all-PASS result is the
norm, and the FAIL lines here only show what the report looks like when a
field does fail:

```
API Diagnostic Results
======================
Table: <table_name> (ID: <table_id>)

Aggregation Tests:
  [PASS]  Scenario         -> 4 groups
  [PASS]  Reporting Date   -> 101 groups
  [PASS]  DR_ACC_L0        -> 5 groups
  [FAIL]  DR_ACC_L1        -> 500 error
  [FAIL]  DR_ACC_L2        -> 500 error
  [PASS]  Account_L1_Alt   -> 18 groups
  [PASS]  Department L1    -> 3 groups
  [PASS]  Cost Center      -> 24 groups

Result: 6/8 fields work (75%)

Suggested Sibling Alternatives (for the failed fields):
  DR_ACC_L1 -> Account_L1_Alt (18 groups)
  DR_ACC_L2 -> Account_L1_Alt (18 groups)

Diagnostic file (optional): tmp/API_Diagnostic_<table_name>_<timestamp>.txt

What to do with this:
  - When a skill 500s on a FAIL field, use its suggested sibling from the
    discovered schema instead (aggregation in seconds vs minutes of
    pagination).
  - Fields marked PASS are safe to use directly as aggregation dimensions.
  - This map applies to the current environment/session; nothing is saved to
    disk, so re-run /dr-test after a schema change.
```

Present this same content as the in-conversation answer (a markdown table of
PASS/FAIL per field plus the suggested siblings works well). The report —
not a file write — is the deliverable.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No table matches the financials pattern | List the tables found and ask the user which one holds their financial data |
| All fields fail | Aggregation API may not work in this environment; skills will fall back to pagination |
| Every probe returns empty (not 500) | The default `"Actuals"` scenario value may not exist for this client — drop the scenario filter or use a value from a small `get_data_by_alias` / `get_data_by_id` pull, then re-probe |
| Auth expires during testing | Tests run sequentially, each ~5s; reconnect via Connectors UI if needed |

## Related Skills

- Connect via Connectors UI before testing.
- `/dr-intelligence`, `/dr-financial-summary`, and other aggregation skills
  benefit from the compatibility map this skill reports — they discover the
  table/fields themselves and handle field failures reactively.
