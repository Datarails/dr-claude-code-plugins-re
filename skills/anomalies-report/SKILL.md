---
name: dr-anomalies-report
description: Generate a comprehensive data-quality Excel workbook from Finance OS tables. The MCP tools return baseline aggregates only; this skill derives findings, severity buckets, and the Data Quality Score client-side, then writes a multi-sheet workbook. Self-contained — pass --table-id to target a table directly, or it discovers the financials table on its own; no profile or setup step required.
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
  - Write
  - Read
  - Bash
argument-hint: "[--table-id <id>] [--severity <level>] [--output <file>]"
---

# Anomaly Detection Report

Generate a comprehensive data-quality Excel workbook for a Finance OS
table. Works with any table — no pre-configuration required.

> **Tool reality check:** the MCP `profile_numeric_fields` and
> `profile_categorical_fields` tools are thin wrappers — they return
> baseline aggregates only (SUM/AVG/MIN/MAX/COUNT for numerics,
> distinct-value samples capped at 5 fields for categoricals). There is
> no server-side anomaly tool. **This skill computes every finding,
> severity bucket, and the Data Quality Score client-side.** See
> `/dr-anomalies` for the per-category recipes; this skill consumes those
> same recipes and packages the result as an Excel workbook.

## Design Principles

**General-Purpose**:
- ✅ No hardcoded table IDs or field names
- ✅ Adapts to any client structure
- ✅ Pass `--table-id` to target any table directly (zero discovery)
- ✅ Otherwise discovers the financials table inline

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--table-id <id>` | Specific table to analyze (used directly, no discovery) | Discovers the financials table |
| `--severity <level>` | Filter results: critical, high, medium, low | All |
| `--output <file>` | Output filename | `tmp/Anomaly_Report_TIMESTAMP.xlsx` |

## What It Reports

### Summary Sheet
- **Data Quality Score** (0-100)
- Health status indicator
- Anomaly count by severity
- Key metrics

### Critical Findings Sheet
- Anomalies requiring immediate attention
- Sample records for investigation
- Field-specific details
- Recommended actions

### High Priority Sheet
- Issues to address this week
- Full descriptions
- Count and context

### Analysis Sheets
- **Numeric Analysis**: SUM, AVG, MIN, MAX, COUNT per numeric field (from
  `profile_numeric_fields`) plus a skill-derived range-band outlier
  flag. Std dev and percentiles are not returned by the API and are
  not reported unless the skill bucketed the field via the aggregation
  start→poll tools (`start_aggregation_by_*` →
  `get_aggregation_result_by_*`) (note that in the sheet when present).
- **Categorical Analysis**: Distinct count and sample values from
  `profile_categorical_fields` (capped at 5 fields per call), plus
  per-value frequencies derived from the aggregation start→poll tools
  (`start_aggregation_by_*` → `get_aggregation_result_by_*`) (nulls
  appear as the explicit `[null]` bucket; the trailing keyless
  grand-total row is excluded from the frequency table).
- **Sample Records**: Actual data samples for top findings, fetched
  via `get_data_by_alias` / `get_data_by_id` after the skill identifies
  the IDs to pull.

## Workflow

**Phase 1: Discovery**
1. Verify connection (if tools fail, guide user to Connectors UI)
2. Resolve the target table (see below) — note **both** its numeric `id` and
   its `alias` (the alias may be empty)
3. Load that table's fields — if it has an alias, `list_aliased_fields(<alias>)`
   (business-friendly aliases); otherwise `get_fields_by_id(<table_id>)`
   (capture each field's numeric `id` — the by-id tools need ids). **Prefer the
   alias path when an alias exists.**

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

**Resolve the target table:**

- **If `--table-id <id>` was passed:** use it directly as `<table_id>`. **No
  discovery needed** — the user named the table. This works for any table,
  financial or not; skip straight to loading its fields. (Don't try to
  name-match or look for category values that may not exist on an arbitrary
  table.) Resolve its alias via `list_data_models` if you want the alias path.

- **Otherwise (default / no-arg path):** discover the financials table inline.
  **If you already discovered it earlier in THIS conversation, reuse it.**
  1. `list_data_models`. Pick the financials table: the one whose name (or
     alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
     largest by row count. Note its numeric `id` and its `alias`.
  2. Load fields with `list_aliased_fields(<alias>)` (if aliased) or
     `get_fields_by_id(<table_id>)`. The anomaly analysis is field-agnostic —
     it profiles whatever numeric and categorical fields the schema exposes —
     so no semantic field binding is required here. When per-value frequency,
     null, or duplicate detection needs a grouping dimension, take the
     categorical fields straight from this schema.
  3. If category-aware findings (rare-value, future-dated) need the account
     dimension, collect distinct values via
     `start_distinct_values_by_alias(<alias>, <account_field>)` (or
     `start_distinct_values_by_id(<table_id>, <account_field_id>)`) → poll
     the matching `get_distinct_values_result_by_*(handle)` until ready
     (async-fetch pattern). If the distinct call errors, fall back to
     `get_data_by_alias(<alias>, select=[<account_field>], limit=500)` (or the
     by-id twin) and dedupe.

Aggregation-field failures are handled reactively, not pre-probed: if an
aggregation start→poll call (`start_aggregation_by_*` →
`get_aggregation_result_by_*`) 500s on a dimension field, re-inspect the
schema for a sibling and retry; if the alias call fails, fall back to the
by-id twin; if none works, tell the user which field failed.

**Phase 2: Gather baseline aggregates**

> **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**

A data-quality scan intentionally covers the whole table, so all-time
aggregates are correct *here* — but still discover the date range (it
powers the future-dated check) and label the workbook with the date
range and scenarios it covers, so the Numeric Analysis SUM/AVG columns
are never read as period P&L figures.

1. `profile_numeric_fields(table_id)` — full numeric coverage
   (SUM/AVG/MIN/MAX/COUNT per numeric field). Treat the result as a
   starting point, not as classified findings.
2. `profile_categorical_fields(table_id, fields=[...])` — pass an
   explicit field list (tool silently caps at 5 per call; loop as
   needed to cover them all).
3. For per-value frequencies, null counts, and duplicate detection:
   `start_aggregation_by_alias` (preferred) or
   `start_aggregation_by_id` grouped by the relevant dimension(s) with
   `COUNT` of a **different dense field** as the metric — never COUNT
   the grouped dimension itself (see "Reading GROUP BY responses"
   below) — by-alias `metrics=[{"field": <other_field_alias>, "agg":
   "COUNT"}]`, by-id `metrics=[{"field_id": <other_field_id>, "agg":
   "COUNT"}]` → poll the matching `get_aggregation_result_by_alias` /
   `get_aggregation_result_by_id` with the `handle` until ready
   (async-fetch pattern). **This is where the actual findings come
   from** — the profile tools alone can't produce them.
4. For top-finding row samples: `get_data_by_alias` /
   `get_data_by_id`. You can filter directly with an advanced condition
   tree — e.g. comparison `{"name": <amount_alias>, "values":
   {"type": "advanced", "val": [{"condition": "gt", "value":
   "<band>"}]}}` to pull outlier rows, or a value-list IN of the
   offending IDs (`{"name": <id_alias>, "values": [...]}`). Comparisons,
   ranges, and `is null` are all supported — no need to pre-identify IDs
   purely because the filter API can't express a comparison.

> **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

> **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

**Phase 2b: Derive findings (client-side)**

Apply the recipes from `/dr-anomalies` (range-band outliers, null
rates, duplicates, rare-category values, future-dated rows) to the
aggregates from Phase 2. When tabulating a GROUP BY response, drop the
trailing keyless grand-total row first (keep it only as a checksum /
total-row-count denominator) — counting it as a group inflates
duplicate-group counts, per-value shares, and rare-value flags. Null
rate = the `[null]`-bucket count ÷ total row count; the keyless row is
the grand total, not a null group. Bucket by severity using the
heuristics in that skill. Drop categories the API can't support
(referential integrity, character-level hygiene).

## Datarails Brand Styling

When generating Excel or PowerPoint files, apply Datarails brand styling:

**Font:** Poppins (fall back to Calibri if unavailable). Weights: 400 regular, 600 semibold, 700 bold.

**Colors:**
| Role | Hex | Use |
|------|-----|-----|
| Navy | `0C142B` | Header/banner background |
| Main text | `333333` | Primary text |
| Secondary | `6D6E6F` | Muted/subtitle text |
| Border | `9EA1AA` | Cell borders |
| Section bg | `F2F2FB` | Section header / row header background (lavender) |
| Input bg | `EAEAFF` | Editable/input cell background |
| Input text | `4646CE` | Editable cell text (indigo) |
| Favorable | `2ECC71` | Positive variance / good KPI delta |
| Unfavorable | `E74C3C` | Negative variance / bad KPI delta |
| Chart 1 | `0C142B` | Actuals (navy) |
| Chart 2 | `F93576` | Budget (hot pink) |
| Chart 3 | `00B4D8` | Teal |
| Chart 4 | `FFA30F` | Amber |

**Excel layout:**
- Content starts at column B (column A is a narrow gutter)
- Rows 1-6: header banner with navy background, white title text, white subtitle
- Gridlines OFF. Freeze panes at B7.
- Footer as last row with generation date
- Every cell must have font, fill, alignment, and number format set

**Number formats:** `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)` (default), `$#,##0` (dollars), `$#,##0.0,,"M"` (millions), `0.0%` (percent)

**Variance coloring:** Any cell showing a delta/change: green (`2ECC71`) if favorable, red (`E74C3C`) if unfavorable. Apply automatically based on value sign and metric context.

**PowerPoint:** Navy (`0C142B`) background, 16:9 widescreen, Poppins font, white text, amber (`FFA30F`) accent lines, card backgrounds `001F37`.

## DR.GET Formulas — Authoring Contract

If asked to add live / refreshable Datarails formulas (DR.GET) to a generated
workbook, the only valid form is:

```
=DR.GET(Value, "[DimensionName]", CellRef, "[DimensionName]", CellRef, ...)
```

- **Never transliterate an MCP/API call into a formula.** DR.GET takes no
  table, field, or aggregation arguments — `=DR.GET(Value,"financials","Amount","SUM",...)`
  is invented syntax that the Datarails Add-in cannot parse or refresh.
- Dimension names go in square brackets inside quotes (`"[Scenario]"`).
  Dimension values are **always cell references**, never hardcoded strings.
- Date cells referenced by formulas hold end-of-month **date serials**
  computed from the calendar — never raw epoch timestamps from API responses
  (epochs land a day early with a time component and never match).
- Before writing any formula, create the workbook-scoped defined name `Value`
  referring to the string constant `"Value"`
  (`wb.defined_names.add(DefinedName("Value", attr_text='"Value"'))`) —
  otherwise Excel autocorrects the bare token to its built-in `VALUE()` and
  the formula breaks.
- Bare `=DR.GET(...)` only — never wrapped in IFERROR/IF/ROUND.

The get-formula skill (`/dr-get-formula`) is the full reference — parameter
cells, validated dimension values, report layouts. Prefer it for whole formula
workbooks; apply this contract when adding DR.GET formulas to a workbook here.
<!-- end:drget-authoring-contract -->

**Phase 3: Report Generation**
1. Categorize the skill-derived findings into Critical / High / Medium / Low
   per the heuristics in `/dr-anomalies` (the skill, not the tool).
2. Compute the Data Quality Score from those counts (formula below).
3. Generate the Excel workbook with the sheets described in
   "What It Reports". Use openpyxl locally — no server-side rendering.
4. Apply Datarails brand styling (see below).

**Phase 4: Summary**
1. Display key findings — make clear in the spoken summary that every
   number was derived from baseline aggregates, not produced by a
   single tool call.
2. Show health status (Excellent / Good / Fair / Poor / Critical).
3. Guide next steps (e.g. "drill into the 23 duplicate transaction_ids
   via `/dr-query` with an IN list").

## Examples

### Analyze default financials table
```bash
/dr-anomalies-report
```

Output:
```
🔍 Discovering financials table...
✓ Found financials table: TABLE_ID

📊 Analyzing table TABLE_ID...
  📈 Profiling numeric fields (SUM/AVG/MIN/MAX/COUNT)...
  📝 Profiling categorical fields (distinct + samples)...
  📊 Aggregating per-value counts for duplicate / null detection...
  🧮 Computing findings + severity buckets client-side...
  🔍 Fetching sample records for top findings...
  📄 Generating Excel report...

✅ Report generated: tmp/Anomaly_Report_2026-02-03_143022.xlsx

==================================================
ANOMALY DETECTION SUMMARY
==================================================
Table: TABLE_ID
Total Anomalies: 45
Data Quality Score: 87/100

By Severity:
  Critical: 2
  High: 8
  Medium: 23
  Low: 12

Report: tmp/Anomaly_Report_2026-02-03_143022.xlsx
==================================================
```

### Analyze specific table for critical issues only
```bash
/dr-anomalies-report --table-id TABLE_ID --severity critical
```

### Save to custom location
```bash
/dr-anomalies-report --env app --output tmp/Quality_Check_Feb_2026.xlsx
```

## Data Quality Score

Score ranges from 0-100:
- **90-100** ✅ **Excellent** - Minimal issues, data is reliable
- **80-90** 🟢 **Good** - Minor issues, generally usable
- **70-80** 🟡 **Fair** - Moderate issues, needs attention
- **70** 🟠 **Poor** - Significant issues, requires action
- **<70** 🔴 **Critical** - Major issues, immediate action required

Calculation:
```
Score = 100 - (critical×10 + high×5 + medium×2 + low×0.5)
Clamped to 0-100 range
```

## Adaptive Behavior

### With `--table-id`
- Uses the supplied table directly — no discovery, no name-matching
- Reads the schema and profiles whatever numeric/categorical fields it exposes
- Works on any table, financial or not

### Default (no `--table-id`)
- Lists available tables and picks the financials table by name pattern (else largest)
- Automatically reads the table schema
- Infers field purposes from names and data types
- Uses general data quality rules

### Field discovery
Whichever path resolved the table:
1. Get the full field list (`list_aliased_fields` if aliased, else
   `get_fields_by_id`)
2. Identify numeric fields (for range-band / outlier checks) and categorical
   fields (for frequency / null / duplicate checks) from it
3. For category-aware findings, collect distinct values via the
   distinct-values start→poll tools (`start_distinct_values_by_*` →
   `get_distinct_values_result_by_*`) (fall back to
   sampling rows with `get_data_by_alias` / `get_data_by_id` only if the
   distinct call errors)
4. Run analysis

## Use Cases

### Monthly Data Quality Check
```bash
/dr-anomalies-report --env app --output tmp/DQ_Check_$(date +%Y-%m).xlsx
```

### Pre-Month-End Close Validation
```bash
/dr-anomalies-report --severity critical
```
*Alerts on critical issues that could affect close*

### Department Data Audit
```bash
/dr-anomalies-report --table-id 12345 --severity high
```
*Checks specific department data for issues*

### Exploratory Analysis
```bash
/dr-anomalies-report --table-id unknown_table_id
```
*Discovers what's in an unfamiliar table*

## Output Files

Reports are saved to: `tmp/Anomaly_Report_YYYY-MM-DD_HHMMSS.xlsx`

Each report includes:
- Professional formatting with colors
- Severity-based highlighting
- Embedded sample data
- Statistical analysis
- Investigation queries

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**"No tables found" error**
- Check that authentication succeeded
- Verify you have access to Finance OS

**"Table not found" error**
- Verify the `--table-id` value is correct
- Run `/dr-tables` to see available tables

**No table matches the financials pattern (default path)**
- List the tables you found and ask the user which one to analyze, or have
  them re-run with `--table-id <id>`.

## Related Skills

- `/dr-tables` - List and explore available tables
- `/dr-extract` - Extract validated financial data
- `/dr-reconcile` - Compare P&L vs KPI data

## Performance

- Small tables (< 10K rows): ~30 seconds
- Medium tables (10-100K rows): ~1-2 minutes
- Large tables (100K+ rows): ~5-10 minutes

Scaling handled automatically via pagination and efficient MCP tools.
