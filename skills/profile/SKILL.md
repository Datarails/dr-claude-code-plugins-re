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
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
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
| `profile_numeric_fields` | `SUM, AVG, MIN, MAX, COUNT` per numeric field |
| `profile_categorical_fields` | distinct-count + first 10 sample values per field (capped at 5 fields per call — pass an explicit `fields` list) |
| `get_aggregated_data_by_alias` / `…_by_id` | grouped totals; the only path to per-value frequencies and null counts |
| `get_distinct_values_by_alias` / `…_by_id` | the full distinct-value list for one field |

What the tools do NOT return: median, std dev, variance, percentiles,
mode, distribution shape, outlier flags, per-value frequency for
categorical fields, null counts. The skill derives these.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide
the user to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect).

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
4. `profile_categorical_fields(table_id, fields=[...])` — pass an explicit
   list; the tool silently drops fields beyond 5. Use this to get distinct
   counts and sample values.
5. For per-value frequency or null counts: `get_aggregated_data_by_alias`
   (or `…_by_id`) grouping by the field with `COUNT` as the metric.
6. For the full distinct-value list of a single field:
   `get_distinct_values_by_alias(<alias>, <field_alias>)` (or
   `get_distinct_values_by_id(<table_id>, <field_id>)`). If a distinct call
   errors, fall back to sampling rows via `get_data_by_alias` /
   `get_data_by_id` (small `limit`, project just that field) and dedupe.

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

### Step 3: Derive richer stats client-side

**Range / outlier flags (numeric)**
- From step 3 you have `MIN, MAX, AVG, COUNT`.
- Approximate spread = `MAX - MIN`; flag values beyond
  `[AVG - spread, AVG + spread]` as out-of-band candidates. This is a
  coarse substitute for `|z| > 3` — true std dev is not available.
- To surface the specific flagged rows you can filter directly:
  `get_data_by_alias(<alias>, select=[...], filters=[{"name": <amount_alias>,
  "values": {"type": "advanced", "val": [{"condition": "gt", "value":
  "<upper_band>"}]}}])` (or the by-id twin, or an `or`-chained `lt` for the
  low tail). Advanced comparison filters are supported.
- For tighter bounds, call `get_aggregated_data_by_alias` (or `…_by_id`) with
  the numeric field bucketed into deciles or sign×magnitude buckets; the
  per-bucket row counts give a usable distribution shape.

**Percentiles (numeric)**
- Not returned by the tool. Approximate via `get_aggregated_data_by_alias`
  (or `…_by_id`) with a sign×magnitude bucketing of the numeric field;
  cumulative row counts across buckets give approximate P25/P50/P75/P95.
- If the user needs exact percentiles, say so honestly: the only way is to
  pull every value (`get_data_by_alias` / `get_data_by_id` page at ≤500
  rows/page), which is rarely the whole table.

**Null counts and rates**
- `get_aggregated_data_by_alias` (or `…_by_id`) with the field as a dimension
  surfaces the null/blank bucket alongside named values; divide its COUNT by
  the total to get the rate. (Or filter directly with an advanced `is null`
  condition.)

**Per-value frequencies (categorical)**
- `profile_categorical_fields` returns a sample of values but no
  counts. Get counts via `get_aggregated_data_by_alias` (or `…_by_id`)
  grouped by the field.

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

**User: "/dr-profile 11442"**

The narrative below is the target presentation. Annotate every line with
its source so the user can re-derive it.

```
📊 Profile: GL Transactions (ID: 11442)

═══════════════════════════════════════════════════
📈 NUMERIC FIELDS (8 columns)  (from profile_numeric_fields)
═══════════════════════════════════════════════════

amount
├── Range: -1,250,000 to 8,750,000     (tool: MIN, MAX)
├── Mean: 45,231                        (tool: AVG)
├── Count: 125,432                      (tool: COUNT)
├── Null rate: derived from get_aggregated_data_by_alias
│   (dimensions=[amount], count null bucket / total) → 0%
├── Range-band outliers: 127 values outside [AVG±spread]
│   (skill heuristic, not z-score; std dev unavailable)
└── Decile bucketing: see get_aggregated_data_by_alias(amount, deciles)
    for an approximate distribution.

quantity
├── Range: 0 to 10,000                  (tool)
├── Mean: 125                           (tool)
├── Null rate: 0.98% (derived from aggregate)
└── Distribution: see get_aggregated_data_by_alias for buckets.

═══════════════════════════════════════════════════
📋 CATEGORICAL FIELDS (5 of 16 — tool caps at 5)
═══════════════════════════════════════════════════

account_code  (156 distinct, from profile_categorical_fields)
├── Sample values: 4000-100, 4000-200, 5100-300, ...
├── Frequencies: derived from get_aggregated_data_by_alias
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

**User: "/dr-profile 11442 --numeric"**

```
📈 Numeric Profile: GL Transactions

Source: profile_numeric_fields(11442) for MIN/MAX/AVG/COUNT;
        get_aggregated_data_by_alias per field for null rates and
        decile distributions.

| Field     | Min    | Max     | Mean    | Count   | Null %  | Out-of-band |
|-----------|--------|---------|---------|---------|---------|-------------|
| amount    | -1.25M | 8.75M   | 45,231  | 125,432 | 0%      | 127 (skill) |
| quantity  | 0      | 10,000  | 125     | 124,198 | 0.98%   | 23 (skill)  |
| unit_cost | 0.01   | 15,000  | 89.50   | 125,432 | 0%      | 45 (skill)  |

"Out-of-band" uses the range heuristic, not std dev. For tighter
bounds on a specific field run /dr-profile 11442 --field <name>.
```

**User: "/dr-profile 11442 --field amount"**

```
📊 Field Profile: amount (GL Transactions)

Source: profile_numeric_fields(11442) +
        get_aggregated_data_by_alias(<alias>, dimensions=[amount-bucket], COUNT)

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
   2. Or bucket the field via get_aggregated_data_by_alias (group by
      sign and order-of-magnitude) to surface specific values, then hand
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

## Related Skills

- `/dr-tables` — discover available tables and call `get_aggregated_data_by_alias`
- `/dr-anomalies` — same client-side computation pattern, focused on
  data-quality findings
- `/dr-query` — fetch specific rows once you know the IDs
