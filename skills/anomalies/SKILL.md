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
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
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
| `profile_numeric_fields` | `SUM, AVG, MIN, MAX, COUNT` per numeric field | median, std dev, percentiles, outlier flags, null counts |
| `profile_categorical_fields` | distinct-count + first 10 sample values per field (capped at 5 fields) | per-value frequency, null counts, uniqueness ratio |
| `get_aggregated_data_by_id` / `…_by_alias` | grouped totals with no row limit | anything not expressible as GROUP BY + aggregation |
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
2. `profile_numeric_fields(table_id)` — SUM/AVG/MIN/MAX/COUNT per
   numeric field.
3. `profile_categorical_fields(table_id, fields=[...])` — explicit
   field list (the tool silently caps at 5). Use this to plan rare-value
   checks; the actual per-value counts come from step 4.
4. For each candidate-key or category field: `get_aggregated_data_by_id`
   with that field id as the dimension and `COUNT` as the metric
   (`metrics=[{"field_id": <id>, "agg": "COUNT"}]`). This is the only way
   to get per-value frequencies and null counts.

### Step 3: Compute findings client-side

For each anomaly category, apply the recipe below to the aggregates from
step 2.

**Range outliers (numeric fields)**
- From `profile_numeric_fields`: per field you have `MIN, MAX, AVG, COUNT`.
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
- From the `get_aggregated_data_by_id` GROUP BY result, the null/blank
  group shows up as an unnamed bucket. Sum its `COUNT` and divide by
  total rows for the null rate. (Or filter directly with an advanced
  `is null` condition.)
- Severity heuristic: ≥10% null on a non-nullable field → CRITICAL;
  ≥1% → HIGH; <1% → LOW.

**Duplicates**
- Pick a candidate composite key (e.g. `[transaction_id]` or
  `[amount, vendor, posting_date]`). Call `get_aggregated_data_by_id`
  grouping by those field ids with `COUNT`. Client-side, filter groups where
  `COUNT > 1`.
- Severity heuristic: any duplicate of a primary-key field →
  CRITICAL; duplicates on a composite key → HIGH; near-duplicates
  (suspicious but plausible) → MEDIUM.

**Rare categorical values**
- From the per-field GROUP BY result, flag values whose frequency is
  below a small absolute threshold (e.g. `< 10` rows) or below
  `0.01%` of total. These are often typos, test data, or stale
  enums.
- Severity heuristic: usually LOW or MEDIUM unless the field is a
  required dimension.

**Future-dated or implausible dates**
- Filter the date field directly with an advanced range condition
  (`total_range` with epoch-second strings), or add the date field to
  `dimensions` in `get_aggregated_data_by_id` and inspect the buckets for
  values beyond today or before a plausible earliest date.

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
| `outliers` | Range heuristic on `profile_numeric_fields` MIN/MAX/AVG |
| `missing` | Null bucket from `get_aggregated_data_by_id` GROUP BY |
| `duplicates` | `get_aggregated_data_by_id` GROUP BY candidate key + filter COUNT > 1 |
| `rare-category` | `get_aggregated_data_by_id` GROUP BY field + filter COUNT < threshold |
| `temporal` | Aggregate by date dimension (or advanced date filter) + inspect for future/past-bound values |

## Example Interaction

**User: "/dr-anomalies 11442"**

The skill's response should look like this — but every number in it is
something **the skill computed** from the baseline aggregates, not a
server-returned finding:

```
🔍 Anomaly Detection: GL Transactions (ID: 11442)
═══════════════════════════════════════════════════════════

Scanned 125,432 records | Computed 47 findings

🔴 CRITICAL (3 findings)
───────────────────────────────────────────────────────────

1. DUPLICATE TRANSACTIONS
   • Derived from: aggregate(group_by=[transaction_id], COUNT)
   • 23 transaction_id values appear ≥2 times
   • Examples: [45231×2, 67892×2, 89234×2, ...]

   💡 Recommendation: Review for accidental double-entry.

2. FUTURE-DATED TRANSACTIONS
   • Derived from: aggregate(group_by=[posting_date], COUNT)
   • 5 buckets fall after today (max: 2024-12-31)
   • Fetch the affected rows with an advanced date filter on
     posting_date if needed.

3. HIGH NULL RATE: vendor_name
   • Derived from: aggregate(group_by=[vendor_name], COUNT) →
     null bucket / total rows
   • 2,341 records (1.87%) have a null vendor_name while vendor_id
     is populated.

🟠 HIGH (12 findings)
───────────────────────────────────────────────────────────

4. AMOUNT RANGE OUTLIERS
   • Derived from: profile_numeric_fields(amount)
     MIN=-1,250,000  AVG=42,310  MAX=8,750,000  COUNT=125,432
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
- `/dr-tables` — schema discovery + `get_aggregated_data_by_id` source
