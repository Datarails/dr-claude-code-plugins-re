---
name: dr-anomalies
description: Detect data anomalies in Datarails Finance OS tables. The MCP tools return baseline aggregates only; this skill is responsible for computing outlier flags, severity buckets, duplicate counts, and missing-value rates client-side from those aggregates.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__start_aggregation_by_alias
  - mcp__datarails-finance-os__get_aggregation_result_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__start_aggregation_by_id
  - mcp__datarails-finance-os__get_aggregation_result_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__start_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_result_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__start_distinct_values_by_id
  - mcp__datarails-finance-os__get_distinct_values_result_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_id
argument-hint: "<table_id> [--severity critical|high|medium|low] [--type <anomaly_type>]"
---

# Datarails Anomaly Detection

Find data quality issues in Finance OS tables. The MCP server's
profile tools are deliberately thin — they return baseline
aggregates and nothing more. **This skill computes the actual findings
(outliers, severity, duplicate counts, null rates) by post-processing
those aggregates.** Be explicit about which numbers came from the tool
versus which the skill derived.

## Tool reality check

Before designing the analysis, read what each tool actually returns:

| Tool | What it returns | What it does NOT compute |
|---|---|---|
| `profile_numeric_fields` | `SUM, AVG, MIN, MAX, COUNT` per numeric field — in the backend-native `DR_Values`/`col_keys`/`row_keys` layout, no per-value aggregator labels | median, std dev, percentiles, outlier flags, null counts |
| `profile_categorical_fields` | distinct-count + first 10 sample values per field (capped at 5 fields; **bare calls default to upload/mapping metadata columns — always pass `fields`**) | per-value frequency, null counts, uniqueness ratio |
| `start_aggregation_by_id` / `…_by_alias` → poll `get_aggregation_result_by_id` / `…_by_alias` | grouped totals with no row limit | anything not expressible as GROUP BY + aggregation |
| `get_data_by_id` / `…_by_alias` | raw rows (≤500/page) with value-list **and** advanced filters | — |

For severity, percentiles, std dev, z-scores, and most named anomaly
categories below — the skill computes them, not the tool. There is no
server-side anomaly tool; everything is derived here.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide
the user to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect).

### Step 2: Gather baseline aggregates

1. `get_fields_by_id(table_id)` — field ids, names, types. (If you only have
   a name/alias, resolve the table via `list_data_models` first.)

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

2. `profile_numeric_fields(table_id)` — SUM/AVG/MIN/MAX/COUNT per
   numeric field. **Reading the response:** it arrives in the
   backend-native `DR_Values`/`col_keys`/`row_keys` layout — values can
   appear duplicated per stat and carry no aggregator label. Map each
   value to its statistic via the keys before labeling it; never present
   a number as MIN/MAX/AVG/COUNT without confirming its key. If the
   mapping is ambiguous, anchor it by cross-checking ONE field with
   `start_aggregation_by_id` (MIN and MAX in two separate calls — one
   aggregation per field per call) → poll `get_aggregation_result_by_id(handle)`
   until ready (async-fetch pattern) before deriving outlier bands.
3. `profile_categorical_fields(table_id, fields=[...])` — pass an
   **explicit `fields` list of business dimensions from the discovered
   schema** (account levels, scenario, entity/department-like, date).
   Omitting `fields` profiles the table's upload/mapping metadata
   columns (tab/label/user/mapper-style bookkeeping fields) instead of
   business data — never call it bare. The tool also silently caps at 5
   fields. Use this to plan rare-value checks; the actual per-value
   counts come from step 4.
4. For each candidate-key or category field: `start_aggregation_by_id`
   with that field id as the dimension and `COUNT` of a **different**
   dense field — e.g. the discovered amount field — as the metric
   (`metrics=[{"field_id": <amount_field_id>, "agg": "COUNT"}]`) →
   poll `get_aggregation_result_by_id(handle)` until ready (async-fetch
   pattern). Never
   COUNT the same field you group by — that pattern can return a 500.
   This is the only way to get per-value frequencies and null counts.

### Step 3: Compute findings client-side

For each anomaly category, apply the recipe below to the aggregates from
step 2. Scope every aggregate to the period from the data-scope preamble
(latest complete fiscal year or trailing 12 closed months by default) —
an all-time baseline mixes years and balance-sheet stock with P&L flow,
which pollutes AVG bands and frequency thresholds. Label each finding
with the period + scenario it covers.

**Range outliers (numeric fields)**
- From `profile_numeric_fields`: per field you have `MIN, MAX, AVG, COUNT` —
  key-mapped per the reading rule in step 2; never derive a band from a
  value whose statistic you haven't confirmed.
- Approximate spread = `(MAX - MIN)`; flag values outside
  `[AVG - k*spread/2, AVG + k*spread/2]` for `k ≈ 2`. This is a
  coarser substitute for the `|z| > 3` rule (true std dev isn't
  available).
- To surface specific rows you can now filter directly:
  `get_data_by_id(table_id, select=[...], filters=[{"field_id": <amount_id>,
  "values": {"type": "advanced", "val": [{"condition": "gt", "value":
  "<upper_band>"}]}}])` (or an `or`-chained `lt` for the low tail). Advanced
  comparison filters are supported — no need for bucketed aggregation just to
  find the rows.
- Severity heuristic: ≥100 rows or ≥1% of total outside the band →
  HIGH; ≥1000 rows or ≥10% → CRITICAL; otherwise MEDIUM.

**Missing values**
- From the `get_aggregation_result_by_id` GROUP BY result, the null group
  arrives explicitly labeled `[null]` — read the null count from that
  bucket only. The response also appends a keyless trailing row equal
  to the **grand total**: use its count as the total-rows denominator
  (or as a checksum), but never treat it as a data bucket — counting it
  as one inflates null rates toward 100% and fakes a giant duplicate.
  Null rate = `[null]` bucket count ÷ grand-total count. (Or filter
  directly with an advanced `is null` condition.)
- Severity heuristic: ≥10% null on a non-nullable field → CRITICAL;
  ≥1% → HIGH; <1% → LOW.

**Duplicates**
- Pick a candidate composite key (e.g. `[transaction_id]` or
  `[amount, vendor, posting_date]`). Call `start_aggregation_by_id`
  grouping by those field ids, with `COUNT` of a **different** dense field
  (e.g. the discovered amount field) as the metric, then poll
  `get_aggregation_result_by_id(handle)` until ready (async-fetch
  pattern) — never COUNT a field
  that is also a GROUP BY dimension. Client-side, drop the keyless
  grand-total row (it is not a duplicate group), then filter groups where
  `COUNT > 1`.
- Severity heuristic: any duplicate of a primary-key field →
  CRITICAL; duplicates on a composite key → HIGH; near-duplicates
  (suspicious but plausible) → MEDIUM.

**Rare categorical values**
- From the per-field GROUP BY result, flag values whose frequency is
  below a small absolute threshold (e.g. `< 10` rows) or below
  `0.01%` of total rows (denominator = the keyless grand-total row,
  which is itself never a bucket). These are often typos, test data, or
  stale enums.
- Severity heuristic: usually LOW or MEDIUM unless the field is a
  required dimension.

**Future-dated or implausible dates**
- Filter the date field directly with an advanced range condition
  (`total_range` with epoch-second strings), or add the date field to
  `dimensions` in `start_aggregation_by_id` (poll
  `get_aggregation_result_by_id(handle)` until ready) and inspect the
  buckets for values beyond today or before a plausible earliest date.

**Out of scope for this skill**
- Referential integrity (would require joining tables, which the
  Finance OS API doesn't expose).
- Per-character data hygiene (trailing whitespace, casing) —
  requires raw-row scanning, which is capped at 500 rows/page.

### Step 4: Present findings

Organize the computed findings by severity:
- 🔴 **CRITICAL** — Requires immediate attention
- 🟠 **HIGH** — Should be addressed soon
- 🟡 **MEDIUM** — Worth investigating
- 🟢 **LOW** — Minor issues or informational

Always state which aggregates the finding was derived from so the user
can re-derive it manually if they want.

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required — the table to analyze |
| `--severity <level>` | Filter results to a specific severity bucket |
| `--type <type>` | Filter to a specific anomaly category (see list below) |

## Anomaly categories handled

| Type | How the skill computes it |
|------|---------------------------|
| `outliers` | Range heuristic on `profile_numeric_fields` MIN/MAX/AVG (key-mapped from the `DR_Values` layout) |
| `missing` | `[null]` bucket from `start_aggregation_by_id` → `get_aggregation_result_by_id` GROUP BY ÷ grand-total row |
| `duplicates` | `start_aggregation_by_id` → `get_aggregation_result_by_id` GROUP BY candidate key + COUNT of a different dense field, filter COUNT > 1 |
| `rare-category` | `start_aggregation_by_id` → `get_aggregation_result_by_id` GROUP BY field + filter COUNT < threshold |
| `temporal` | Aggregate by date dimension (or advanced date filter) + inspect for future/past-bound values |

## Example Interaction

**User: "/dr-anomalies 999999"**

The skill's response should look like this (illustrative — the table
name, id, fields, and figures below are invented; your org's will
differ) — but every number in it is something **the skill computed**
from the baseline aggregates, not a server-returned finding:

```
🔍 Anomaly Detection: GL Transactions (ID: 999999)
═══════════════════════════════════════════════════════════

Scope: FY2024 (latest complete year) | Scenario: Actuals
Scanned 125,000 records | Computed 47 findings

🔴 CRITICAL (3 findings)
───────────────────────────────────────────────────────────

1. DUPLICATE TRANSACTIONS
   • Derived from: aggregate(group_by=[transaction_id], COUNT(amount)),
     grand-total row excluded
   • 23 transaction_id values appear ≥2 times
   • Examples: [45231×2, 67892×2, 89234×2, ...]

   💡 Recommendation: Review for accidental double-entry.

2. FUTURE-DATED TRANSACTIONS
   • Derived from: aggregate(group_by=[posting_date], COUNT(amount))
   • 5 buckets fall after today (max: 2024-12-31)
   • Fetch the affected rows with an advanced date filter on
     posting_date if needed.

3. HIGH NULL RATE: vendor_name
   • Derived from: aggregate(group_by=[vendor_name], COUNT(amount)) →
     [null] bucket ÷ grand-total row
   • 2,500 records (2.0%) have a null vendor_name while vendor_id
     is populated.

🟠 HIGH (12 findings)
───────────────────────────────────────────────────────────

4. AMOUNT RANGE OUTLIERS
   • Derived from: profile_numeric_fields(amount), stats key-mapped
     from the DR_Values/col_keys/row_keys response:
     MIN=-1,250,000  AVG=40,000  MAX=8,750,000  COUNT=125,000
   • Coarse band [AVG - (MAX-MIN), AVG + (MAX-MIN)]:
     115 rows above the band, 12 below.
   • Note: this is a range heuristic — true z-scores are not
     available because std dev isn't returned by the tool.

...

═══════════════════════════════════════════════════════════
📊 SUMMARY
═══════════════════════════════════════════════════════════

| Severity | Count | Action                    |
|----------|-------|---------------------------|
| Critical | 3     | Investigate immediately   |
| High     | 12    | Address this week         |
| Medium   | 18    | Plan for remediation      |
| Low      | 14    | Fix during maintenance    |

Data Quality Score: derived (computed from finding counts, not from
the MCP server).
```

## Investigation Workflow

1. **Review the computed findings** — every number traces back to a
   specific tool call; show that call when asked.
2. **Surface specific rows** — for outliers/duplicates, fetch them
   directly with `get_data_by_id` advanced filters, or aggregate with
   bucketed dimensions to get IDs and pass them to `/dr-query`.
3. **Verify business rules** — some "anomalies" are valid by
   policy.
4. **Document decisions** — note which findings are false positives.
5. **Create a remediation plan** — prioritize by severity.

## Related Skills

- `/dr-profile` — field statistics (same client-side computation pattern)
- `/dr-query` — fetch specific rows once you know the IDs
- `/dr-tables` — schema discovery + `start_aggregation_by_id` source
