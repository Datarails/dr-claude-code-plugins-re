---
name: dr-anomalies-report
description: Generate a comprehensive data-quality Excel workbook from Finance OS tables. The MCP tools return baseline aggregates only; this skill derives findings, severity buckets, and the Data Quality Score client-side, then writes a multi-sheet workbook. Self-contained — pass --table-id to target a table directly, or it discovers the financials table on its own; no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__detect_anomalies
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - Write
  - Read
  - Bash
argument-hint: "[--table-id <id>] [--severity <level>] [--output <file>]"
---

# Anomaly Detection Report

Generate a comprehensive data-quality Excel workbook for a Finance OS
table. Works with any table — no pre-configuration required.

> **Tool reality check:** the MCP `detect_anomalies`,
> `profile_numeric_fields`, and `profile_categorical_fields` tools are
> thin wrappers — they return baseline aggregates only (MIN/MAX/AVG/COUNT
> for numerics, distinct-value samples capped at 5 fields for
> categoricals). **This skill computes every finding, severity bucket,
> and the Data Quality Score client-side.** See `/dr-anomalies` for the
> per-category recipes; this skill consumes those same recipes and
> packages the result as an Excel workbook.

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
- **Numeric Analysis**: MIN, MAX, AVG, COUNT per numeric field (from
  `profile_numeric_fields`) plus a skill-derived range-band outlier
  flag. Std dev and percentiles are not returned by the API and are
  not reported unless the skill bucketed the field via
  `aggregate_table_data` (note that in the sheet when present).
- **Categorical Analysis**: Distinct count and sample values from
  `profile_categorical_fields` (capped at 5 fields per call), plus
  per-value frequencies derived from `aggregate_table_data`.
- **Sample Records**: Actual data samples for top findings, fetched
  via `get_records_by_filter` after the skill identifies the IDs to
  pull.

## Workflow

**Phase 1: Discovery**
1. Verify connection (if tools fail, guide user to Connectors UI)
2. Resolve the target table (see below)
3. Load that table's schema with `get_table_schema(<table_id>)`

**Resolve the target table:**

- **If `--table-id <id>` was passed:** use it directly as `<table_id>`. **No
  discovery needed** — the user named the table. This works for any table,
  financial or not; skip straight to loading its schema. (Don't try to
  name-match or look for category values that may not exist on an arbitrary
  table.)

- **Otherwise (default / no-arg path):** discover the financials table inline.
  **If you already discovered it earlier in THIS conversation, reuse it.**
  1. `list_finance_tables`. Pick the financials table: the one whose name
     matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest by
     row count. Call it `<table_id>`.
  2. `get_table_schema(<table_id>)`. The anomaly analysis is field-agnostic —
     it profiles whatever numeric and categorical fields the schema exposes —
     so no semantic field binding is required here. When per-value frequency,
     null, or duplicate detection needs a grouping dimension, take the
     categorical fields straight from this schema.
  3. If category-aware findings (rare-value, future-dated) need the account
     dimension, collect distinct values via
     `get_sample_records(<table_id>, limit=500)` (the distinct-values API
     often 409s) rather than the distinct-values API.

Aggregation-field failures are handled reactively, not pre-probed: if
`aggregate_table_data` 500s on a dimension field, re-inspect the schema for a
sibling and retry; if none works, tell the user which field failed.

**Phase 2: Gather baseline aggregates**

1. `detect_anomalies(table_id)` — baseline MIN/MAX/AVG/COUNT for the
   first 5 numeric fields. Treat the result as a starting point, not
   as classified findings.
2. `profile_numeric_fields(table_id)` — full numeric coverage.
3. `profile_categorical_fields(table_id, fields=[...])` — pass an
   explicit field list (tool silently caps at 5 per call; loop as
   needed to cover them all).
4. For per-value frequencies, null counts, and duplicate detection:
   `aggregate_table_data` grouped by the relevant dimension(s) with
   `COUNT` as the metric. **This is where the actual findings come
   from** — the profile tools alone can't produce them.
5. For top-finding row samples: `get_records_by_filter` with an
   IN-list of the offending IDs (the filter API rejects raw
   comparisons; identify candidate IDs from the aggregation step
   first).

**Phase 2b: Derive findings (client-side)**

Apply the recipes from `/dr-anomalies` (range-band outliers, null
rates, duplicates, rare-category values, future-dated rows) to the
aggregates from Phase 2. Bucket by severity using the heuristics in
that skill. Drop categories the API can't support (referential
integrity, character-level hygiene).

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
  📈 Profiling numeric fields (MIN/MAX/AVG/COUNT)...
  📝 Profiling categorical fields (distinct + samples)...
  🔬 Running baseline numeric summary (detect_anomalies)...
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
1. Get the full schema
2. Identify numeric fields (for range-band / outlier checks) and categorical
   fields (for frequency / null / duplicate checks) from it
3. For category-aware findings, collect distinct values via
   `get_sample_records` (the distinct-values API often 409s)
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
