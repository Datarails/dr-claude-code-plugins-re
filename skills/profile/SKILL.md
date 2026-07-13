---
name: dr-profile
description: Profile Datarails Finance OS table fields. The MCP tools return baseline aggregates (SUM/AVG/MIN/MAX/COUNT for numeric, distinct-value samples for categorical); this skill derives percentiles, range-outlier flags, null rates, and cardinality interpretation client-side.
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
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__list_business_metrics
argument-hint: "<table_id> [--numeric] [--categorical] [--field <field_name>]"
---

# Datarails Table Profiling

Field-level statistics for Finance OS tables. The MCP profile tools are
thin — they return only the basic aggregates listed below. Everything
richer (percentiles, std dev, outlier flags, null rates, cardinality
interpretation) is computed by this skill, not the tool. State the
provenance of every number you present.

## Tool reality check

| Tool | What it returns |
|---|---|
| `profile_numeric_fields` | `SUM, AVG, MIN, MAX, COUNT` per numeric field — relayed in the backend-native `DR_Values`/`col_keys`/`row_keys` layout, with **no aggregator label attached to individual values** (see the reading rule in Step 2) |
| `profile_categorical_fields` | distinct-count + first 10 sample values per field (capped at 5 fields per call — pass an explicit `fields` list; **without one it defaults to upload/mapping metadata columns, not business dimensions**) |
| `start_aggregation_by_alias` / `…_by_id` → poll `get_aggregation_result_by_alias` / `…_by_id` | grouped totals; the only path to per-value frequencies and null counts |
| `start_distinct_values_by_alias` / `…_by_id` → poll `get_distinct_values_result_by_alias` / `…_by_id` (pass `limit` to the result tool) | the full distinct-value list for one field |

What the tools do NOT return: median, std dev, variance, percentiles,
mode, distribution shape, outlier flags, per-value frequency for
categorical fields, null counts. The skill derives these.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide
the user to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect).

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

### Step 2: Resolve the table, then gather baseline aggregates

**If you already identified this table and its fields earlier in THIS
conversation, reuse them.** Discovery is cheap but not free.

1. Resolve the table. If you were handed a name/alias rather than a numeric
   id, call `list_data_models` first — each entry carries **both** the numeric
   `id` (for the by-id tools) and the `alias` (for the by-alias tools; empty
   when a table has no alias). **Prefer the alias path when an alias exists.**
2. Field schema. If the table has an alias, `list_aliased_fields(<alias>)`
   (business-friendly aliases); otherwise `get_fields_by_id(<table_id>)`
   (capture each field's numeric `id` — the by-id tools address fields by id).
3. `profile_numeric_fields(table_id)` — per-field SUM/AVG/MIN/MAX/COUNT.

   **Reading the profiling response.** The response is not a labeled
   per-field dict — it arrives in the backend-native aggregate layout
   (`DR_Values` / `col_keys` / `row_keys` arrays), with values possibly
   duplicated per stat and **no aggregator label attached to individual
   values**. Inspect the keys and map every value to its statistic via
   those keys before labeling anything. NEVER present a number as
   MIN/MAX/AVG/COUNT without confirming which key it belongs to —
   mislabeling here (e.g. calling a MAX an AVG) silently corrupts every
   downstream derivation. If the mapping is ambiguous, cross-check ONE
   field with a direct `start_aggregation_by_alias` / `…_by_id` call →
   poll the matching `get_aggregation_result_by_*` (handle) until ready
   (async-fetch pattern) — MIN and MAX in two separate calls (one
   aggregation per field per call) — and use that to anchor the
   interpretation before deriving outliers or ranges from it.

4. `profile_categorical_fields(table_id, fields=[...])` — **always pass an
   explicit `fields` list of business dimensions chosen from the field
   schema discovered in item 2** (account-hierarchy levels, scenario,
   entity/department-like fields, dates). Called without `fields`, the
   tool defaults to the table's upload/mapping **metadata** columns
   (tab/label/user/mapper-style bookkeeping fields) — profiling those
   tells the user nothing about their data. Never call it bare. The tool
   also silently drops fields beyond 5 per call. Use this to get distinct
   counts and sample values.
5. For per-value frequency or null counts: `start_aggregation_by_alias`
   (or `…_by_id`) grouping by the field with `COUNT` as the metric →
   poll `get_aggregation_result_by_alias` / `…_by_id` (handle) until
   ready (async-fetch pattern).
6. For the full distinct-value list of a single field:
   `start_distinct_values_by_alias(<alias>, <field_alias>)` (or
   `start_distinct_values_by_id(<table_id>, <field_id>)`) → poll
   `get_distinct_values_result_by_alias` / `…_by_id` (handle, `limit`)
   until ready (async-fetch pattern). If a distinct call errors, fall
   back to sampling rows via `get_data_by_alias` /
   `get_data_by_id` (small `limit`, project just that field) and dedupe.

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

### Step 3: Derive richer stats client-side

**Range / outlier flags (numeric)**
- From the `profile_numeric_fields` call you have `MIN, MAX, AVG, COUNT` —
  **each mapped to its statistic via the response keys** (the reading rule
  in Step 2). Do not derive bands from an unmapped or ambiguous value.
- Approximate spread = `MAX - MIN`; flag values beyond
  `[AVG - spread, AVG + spread]` as out-of-band candidates. This is a
  coarse substitute for `|z| > 3` — true std dev is not available.
- To surface the specific flagged rows you can filter directly:
  `get_data_by_alias(<alias>, select=[...], filters=[{"name": <amount_alias>,
  "values": {"type": "advanced", "val": [{"condition": "gt", "value":
  "<upper_band>"}]}}])` (or the by-id twin, or an `or`-chained `lt` for the
  low tail). Advanced comparison filters are supported.
- For tighter bounds, call `start_aggregation_by_alias` (or `…_by_id`) with
  the numeric field bucketed into deciles or sign×magnitude buckets → poll
  `get_aggregation_result_by_*` (handle) until ready; the
  per-bucket row counts give a usable distribution shape.

**Percentiles (numeric)**
- Not returned by the tool. Approximate via `start_aggregation_by_alias`
  (or `…_by_id`) with a sign×magnitude bucketing of the numeric field →
  poll `get_aggregation_result_by_*` (handle) until ready;
  cumulative row counts across buckets give approximate P25/P50/P75/P95.
- If the user needs exact percentiles, say so honestly: the only way is to
  pull every value (`get_data_by_alias` / `get_data_by_id` page at ≤500
  rows/page), which is rarely the whole table.

**Null counts and rates**
- `start_aggregation_by_alias` (or `…_by_id`) with the field as a dimension
  → poll `get_aggregation_result_by_*` (handle) until ready —
  surfaces the null/blank bucket alongside named values; divide its COUNT by
  the total to get the rate. (Or filter directly with an advanced `is null`
  condition.)

**Per-value frequencies (categorical)**
- `profile_categorical_fields` returns a sample of values but no
  counts. Get counts via `start_aggregation_by_alias` (or `…_by_id`)
  grouped by the field → poll `get_aggregation_result_by_*` until ready.

**Cardinality interpretation**
- Compute `distinct_count / total_rows`. Conventional bands:
  `< 0.001` very low, `< 0.05` low, `< 0.5` medium, `≥ 0.5` high.
  High cardinality on a column that should be a key (or that should
  be a dimension table) is worth flagging.

### Step 4: Present results

When showing derived statistics, annotate which tool call sourced the
inputs. Always be honest about which numbers are exact (returned by the
tool) versus approximated (computed by this skill from bucketed
aggregates).

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required — the table to profile |
| `--numeric` | Profile only numeric fields |
| `--categorical` | Profile only categorical fields |
| `--field <name>` | Profile a specific field in depth |
| `--fields <a,b,c>` | Profile specific fields (comma-separated) |

## Example Interactions

(Illustrative — table ids, field names, and figures below are invented;
your org's tables, fields, and values will differ. Stat annotations like
`(tool: MIN, MAX)` are only legitimate after key-mapping the
`DR_Values`/`col_keys`/`row_keys` response per the reading rule in Step 2 —
the tool itself does not label values.)

**User: "/dr-profile 999901"**

The narrative below is the target presentation. Annotate every line with
its source so the user can re-derive it.

```
📊 Profile: GL Transactions (ID: 999901)

═══════════════════════════════════════════════════
📈 NUMERIC FIELDS (8 columns)  (from profile_numeric_fields)
═══════════════════════════════════════════════════

amount
├── Range: -1,250,000 to 8,750,000     (tool: MIN, MAX)
├── Mean: 45,231                        (tool: AVG)
├── Count: 125,432                      (tool: COUNT)
├── Null rate: derived from start_aggregation_by_alias → poll
│   get_aggregation_result_by_alias (dimensions=[amount],
│   count null bucket / total) → 0%
├── Range-band outliers: 127 values outside [AVG±spread]
│   (skill heuristic, not z-score; std dev unavailable)
└── Decile bucketing: see start_aggregation_by_alias(amount, deciles)
    → get_aggregation_result_by_alias for an approximate distribution.

quantity
├── Range: 0 to 10,000                  (tool)
├── Mean: 125                           (tool)
├── Null rate: 0.98% (derived from aggregate)
└── Distribution: see start_aggregation_by_alias → result poll for buckets.

═══════════════════════════════════════════════════
📋 CATEGORICAL FIELDS (5 of 16 — tool caps at 5)
═══════════════════════════════════════════════════

account_code  (156 distinct, from profile_categorical_fields)
├── Sample values: 4000-100, 4000-200, 5100-300, ...
├── Frequencies: derived from start_aggregation_by_alias → result poll
│   Top: 4000-100 (10.0%), 4000-200 (6.6%), 5100-300 (6.3%)
└── Cardinality: 156 / 125,432 = 0.12% → LOW (skill interpretation)

department  (12 distinct)
├── Top: Sales (35%), Marketing (22%), Operations (18%)
├── Null rate: 0.71% (derived from aggregate)
└── Cardinality: VERY LOW (12 / 125,432 = 0.01%)

vendor_id  (45,231 distinct → HIGH CARDINALITY ⚠️)
├── Cardinality: 36% — likely a key or dimension reference.
├── Null rate: 1.87% (derived)
└── Recommendation (skill): consider whether vendor_id should be
    joined against a vendor master.

Note: profile_categorical_fields only returns 5 fields per call.
The remaining 11 categorical fields were not profiled in this run —
re-invoke with --fields a,b,c to cover them.
```

**User: "/dr-profile 999901 --numeric"**

```
📈 Numeric Profile: GL Transactions

Source: profile_numeric_fields(999901) for MIN/MAX/AVG/COUNT;
        start_aggregation_by_alias → get_aggregation_result_by_alias
        per field for null rates and decile distributions.

| Field     | Min    | Max     | Mean    | Count   | Null %  | Out-of-band |
|-----------|--------|---------|---------|---------|---------|-------------|
| amount    | -1.25M | 8.75M   | 45,231  | 125,432 | 0%      | 127 (skill) |
| quantity  | 0      | 10,000  | 125     | 124,198 | 0.98%   | 23 (skill)  |
| unit_cost | 0.01   | 15,000  | 89.50   | 125,432 | 0%      | 45 (skill)  |

"Out-of-band" uses the range heuristic, not std dev. For tighter
bounds on a specific field run /dr-profile 999901 --field <name>.
```

**User: "/dr-profile 999901 --field amount"**

```
📊 Field Profile: amount (GL Transactions)

Source: profile_numeric_fields(999901) +
        start_aggregation_by_alias(<alias>, dimensions=[amount-bucket], COUNT)
        → poll get_aggregation_result_by_alias(handle) until ready

Type: DECIMAL                          (schema)
Tool-provided stats:
├── Count: 125,432
├── Min: -1,250,000
├── Max: 8,750,000
├── Mean (AVG): 45,231.45
└── Sum: 5,672,541,330.00

Skill-derived (from bucketed aggregate):
├── Null rate: 0%
├── Approximate percentiles (sign × magnitude buckets):
│   P25 ≈ 5,000   P50 ≈ 12,500   P75 ≈ 35,000   P95 ≈ 250,000
├── Distribution: right-skewed (small values dominant, long
│   positive tail).
└── Range-band outliers: 127 values outside [AVG ± (MAX-MIN)].
    115 above, 12 below. This is a coarser flag than a true
    z-score test because std dev is not returned by the API.

💡 Recommendation: Investigate the 127 flagged transactions.
   Workflow:
   1. Fetch the flagged rows directly with an advanced comparison
      filter: get_data_by_alias(<alias>, select=[...], filters=[{"name":
      <amount_alias>, "values": {"type": "advanced", "val": [{"condition":
      "gt", "value": "<upper_band>"}]}}]) (or the by-id twin; or-chain a
      `lt` for the low tail).
   2. Or bucket the field via start_aggregation_by_alias (group by
      sign and order-of-magnitude; poll get_aggregation_result_by_alias
      until ready) to surface specific values, then hand
      them to /dr-query for deeper investigation.
```

## Data Quality Indicators

| Symbol | Meaning |
|--------|---------|
| ⚠️ | Potential issue requiring attention |
| ❌ | Data quality problem detected |
| ✅ | Field looks healthy |
| 📊 | Statistical insight (skill-derived) |

## Tips

- Profile before running `/dr-anomalies` so you understand the baseline.
- A high null rate (>5%) usually points to a data-collection problem.
- High cardinality on a non-key column may indicate a missing
  dimension table.
- "Out-of-band" flags from this skill are heuristic — verify against
  business rules before treating them as errors.
- Be explicit when answering: "MIN was returned by the tool;
  P25 is approximated from a bucketed aggregate."
- Never label a profiling number MIN/MAX/AVG/COUNT until you've mapped
  it via the response keys; when unsure, anchor with one aggregation
  start→poll cross-check (`start_aggregation_by_*` →
  `get_aggregation_result_by_*`; MIN and MAX in separate calls).
- Never call `profile_categorical_fields` without `fields` — the bare
  call profiles upload/mapping metadata columns, not business data.

## Related Skills

- `/dr-tables` — discover available tables and call `start_aggregation_by_alias` → `get_aggregation_result_by_alias`
- `/dr-anomalies` — same client-side computation pattern, focused on
  data-quality findings
- `/dr-query` — fetch specific rows once you know the IDs
