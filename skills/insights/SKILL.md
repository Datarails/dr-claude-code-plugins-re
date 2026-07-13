---
name: dr-insights
description: Generate executive-ready insights with trend analysis and visualizations. Creates professional PowerPoint presentations and Excel data books.
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
  - mcp__datarails-finance-os__list_business_metrics
  - Write
  - Read
  - Bash
argument-hint: "[--year <YYYY>] [--quarter <Q#>] [--output-pptx <file>] [--output-xlsx <file>]"
---

# Financial Insights Report

Generate executive-ready insights with trend analysis, KPI dashboards, and professional visualizations.

Creates both PowerPoint presentations (for meetings) and Excel data books (for detailed analysis).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | Calendar year to analyze | Latest complete fiscal year in the data (see data-scope preamble) |
| `--quarter <Q#>` | Quarter: Q1, Q2, Q3, Q4 | None — full-year scope unless given |
| `--period <period>` | Combined period: YYYY-QX or YYYY-MM | Auto-determined |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Insights_TIMESTAMP.pptx` |
| `--output-xlsx <file>` | Excel output path | `tmp/Insights_Data_TIMESTAMP.xlsx` |

## What It Analyzes

### Revenue & Growth
- Monthly revenue trends (12+ months)
- Period-over-period growth rates (MoM, QoQ)
- Revenue by account category (at the discovered P&L grain)
- Trend analysis and momentum

### Key Performance Indicators

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

The KPIs below come from the org's metric catalog and are included
**only when discovered as populated metrics** — otherwise their cards
and slides are omitted entirely:
- ARR (Annual Recurring Revenue) and Net New ARR
- Churn rate and dollar churn
- LTV (Lifetime Value) / CAC (Customer Acquisition Cost)
- Burn rate and runway

### Operational Metrics
- Gross profit and margins (when COGS/OpEx-like buckets exist at the
  discovered grain)
- Operating expenses by category
- Headcount trends, per-employee productivity, and department
  performance (when the relevant fields or metrics exist in the
  discovered data)

### Financial Health
Catalog-sourced only — rendered when discovered as populated metrics,
omitted otherwise:
- Cash burn multiple
- CAC payback period
- LTV/CAC ratio
- Efficiency score

## Output: PowerPoint Presentation

Professional presentation, up to 7 slides — any KPI card or slide whose
metrics could not be sourced is omitted (see the KPI-honesty rule under
Key Performance Indicators):

1. **Title Slide** - Report period, scenario, and date
2. **Executive Summary** - Top metrics with trend indicators
3. **Key Findings** - Top 5 insights with business impact
4. **Recommendations** - Actionable next steps
5. **Metrics Dashboard** - KPI summary with sparklines (sourced KPIs only)
6. **Efficiency Analysis** - Ratios and operational metrics (sourced KPIs only)
7. **Data Summary** - Data sources, period + scenario scope, methodology

### Design Features
- Professional color scheme matching Datarails brand
- Embedded charts and visualizations
- Metrics boxes with trend indicators
- Every chart, table, and metrics box labeled with the period +
  scenario it covers
- Consistent formatting across all slides
- Executive-friendly layout

## Output: Excel Data Book

Comprehensive workbook includes:

1. **Summary Sheet**
   - Period + scenario scope of the report (repeated on every sheet header)
   - Key findings formatted as table
   - Severity and category indicators
   - Current vs prior period comparison

2. **Recommendations Sheet**
   - Prioritized action items
   - Implementation guidance
   - Expected impact

3. **Metrics Sheet**
   - Current KPI values (sourced KPIs only — no placeholders)
   - Targets (if available)
   - Prior period comparison

4. **Detailed Trends**
   - Monthly P&L breakdown
   - Account-level detail
   - Year-over-year comparison

5. **Data Sources**
   - Tables and fields used
   - Data refresh timestamp
   - Methodology notes

## Workflow

### Phase 1: Data Collection
1. Verify authentication
2. Discover the financials table and its fields — see below
3. Fetch P&L trends via `start_aggregation_by_alias` (or by-id) → poll
   `get_aggregation_result_by_alias` (or by-id) with the handle until
   ready (async-fetch pattern) — scoped to the requested period
   (default: latest complete fiscal year or trailing 12 closed months),
   filtered to the discovered scenario and P&L grain (data-scope
   preamble, items 1–3)
4. Fetch KPI metrics — discover named KPIs via `list_business_metrics`;
   compute P&L-derivable KPIs (revenue, expense buckets, margins) by
   aggregating the financials table over the discovered grain
   (`start_aggregation_by_alias` / `start_aggregation_by_id` → poll the
   matching `get_aggregation_result_by_*` until ready).
   Catalog-only KPIs are included solely when sourced — see the
   KPI-honesty rule under Key Performance Indicators

#### Discover the financials table and its fields

**If you already discovered these earlier in THIS conversation, reuse
them — skip to fetching data.** Discovery is cheap but not free; do it
once per conversation, then carry the values forward.

1. `list_data_models`. Pick the financials table: the one whose name
   (or alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match,
   the largest by row count. Note **both** its numeric `id`
   (`<financials_table_id>`) and its `alias` (the alias may be empty).
   **Prefer the alias path when an alias exists** — friendlier field
   names, far fewer tokens. For named KPIs (ARR, churn, LTV/CAC, etc.),
   also call `list_business_metrics` and keep the flat list — each entry
   carries `id`, `name`, `description`, `category`, `kind`,
   `dimensions[]`, `status_info{}`.

2. Fields. If the table has an alias, `list_aliased_fields(<alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each
   field's numeric `id` — the by-id tools address fields by id). Bind
   these by case-insensitive match on the field alias/name (respecting
   the noted type):
   - `<amount_field>`       — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`     — categorical: `^scenario$` → `^version$`
   - `<date_field>`         — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_level_fields>` — categorical: **all** account-hierarchy
     level fields, shallowest to deepest (names/aliases matching
     patterns like `dr_acc_l1`/`dr_acc_l2` → `account_l1`/`account_l2`
     → `account_group_l1`). Capture every level — do **not** assume the
     L1-style level is the P&L grain; the grain is chosen from distinct
     values in step 3 (a deeper level is often the detail dimension)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the
   user which field to use, then continue.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

3. Bind the P&L grain and its category values (preamble item 2 above):
   pull distinct values of each account-level field, shallowest first —
   `start_distinct_values_by_alias(<alias>, <field>)` (or
   `start_distinct_values_by_id(<financials_table_id>, <field_id>)`) →
   poll the matching `get_distinct_values_result_by_*(handle, limit)`
   until ready (async-fetch pattern).
   If a distinct call errors, fall back to
   `get_data_by_alias(<alias>, select=[<field>], limit=500)`
   (or the by-id twin) and collect the distinct values. The level whose
   values partition P&L flows into revenue/COGS/opex-like buckets is
   `<account_grain_field>`. Match its values:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   Scope every P&L figure to these flow buckets and exclude
   balance-sheet buckets (asset/liability/equity-like values). If a
   category has several candidates at the grain, pick the broadest one;
   if genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively (see Error Handling),
not pre-probed. On auth/connection failure during discovery: show the
reconnect message and STOP — do not generate reports without fresh data.

### Phase 2: Analysis
1. Apply the aggregate-reading rules (preamble item 4) to every GROUP BY
   response before computing: exclude the trailing keyless grand-total
   row from sums, shares, trends, and bucket counts (at most use it as
   a checksum); read null counts only from the `[null]` bucket
2. Calculate growth rates
3. Compute efficiency ratios (sourced KPIs only — see the KPI-honesty
   rule under Key Performance Indicators)
4. Identify trends and anomalies
5. Generate business insights
6. Create recommendations

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

### Phase 3: Presentation Generation
1. Create PowerPoint (up to 7 professional slides — omit any KPI card
   or slide whose metrics could not be sourced)
2. Generate Excel data book
3. Embed charts and metrics
4. Label every slide, chart, table, and metrics box with the period +
   scenario it covers
5. Apply professional formatting

### Phase 4: Output
1. Save both files to tmp/
2. Display summary to user
3. Provide file locations

## Examples

### Generate insights for the default period
```bash
/dr-insights
```

Output (period and scenario values are illustrative — both come from
discovery):
```
📊 Generating insights for FY2025 (latest complete fiscal year) · Scenario: Actuals...
  📊 Fetching P&L trends...
  📈 Fetching KPI metrics...
  💡 Calculating insights...
  📄 Generating PowerPoint presentation...
  📋 Generating Excel data book...

✅ Insights generated successfully

==================================================
INSIGHTS GENERATED
==================================================
Period: FY2025 · Scenario: Actuals
Key Findings: 5

Outputs:
  PowerPoint: tmp/Insights_2026-02-03_143022.pptx
  Excel: tmp/Insights_Data_2026-02-03_143022.xlsx
==================================================
```

### Generate specific quarter
```bash
/dr-insights --year 2025 --quarter Q4
```

### Generate previous month
```bash
/dr-insights --period 2026-01
```

### Save to custom location
```bash
/dr-insights --year 2025 --quarter Q4 \
  --output-pptx reports/Q4_2025_Insights.pptx \
  --output-xlsx reports/Q4_2025_Data.xlsx
```

## Use Cases

### Board Presentations
```bash
/dr-insights --quarter Q4 --year 2025
# Use PowerPoint for board meeting
```

### Executive Dashboard Updates
```bash
# Weekly insights
/dr-insights
```

### Quarterly Business Reviews
```bash
# Comprehensive analysis for stakeholders
/dr-insights --year 2025 --quarter Q4
```

### Investor Communications
```bash
# Professional presentation for investors
/dr-insights --quarter Q4 --year 2025
```

### Department Reviews
```bash
# Share with teams for transparency
/dr-insights
```

## Key Metrics Included

Per the KPI-honesty rule (see Key Performance Indicators): P&L-derived
metrics render whenever the discovered grain supports them; catalog-only
metrics render only when discovered as populated metrics — otherwise
their cards and slides are omitted entirely, never estimated.

**Growth Metrics** (revenue growth is P&L-derived; ARR is catalog-only):
- Revenue MoM/QoQ/YoY growth
- ARR trends and Net New ARR — only if sourced from the metric catalog

**Profitability Metrics** (P&L-derived when COGS/OpEx-like buckets
exist at the discovered grain):
- Gross profit and margin
- Operating expense ratio
- EBITDA

**Unit Economics** (catalog-only — omitted unless sourced):
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- LTV/CAC ratio
- Payback period

**Cash Metrics** (catalog-only — omitted unless sourced):
- Monthly burn rate
- Runway (months of cash)
- Burn multiple (burn rate / revenue)

**Churn & Retention** (catalog-only — omitted unless sourced):
- Dollar churn
- Percentage churn
- Net revenue retention

## Performance

- Small datasets (1-2 years): ~1-2 minutes
- Large datasets (3+ years): ~3-5 minutes

Fast processing via efficient MCP aggregation tools.

## Error Handling

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**Aggregation field rejected (500)**
- Retry with a sibling account-level field from the discovered schema
  (another level captured in step 2). If none works, note which field
  failed and present what you have.

**"No KPI data found" warning**
- `list_business_metrics` returned no named KPIs, or the financials
  table had no usable data to compute them — agent adapts and focuses
  on P&L trends
- Unsourced KPI cards and slides are omitted, never estimated
- Recommendations still generated

**"Incomplete data for period" warning**
- Agent includes available data
- Highlights gaps in report

## Related Skills

- `/dr-anomalies-report` - Data quality assessment
- `/dr-reconcile` - P&L vs KPI validation
- `/dr-dashboard` - Executive KPI monitoring
- `/dr-extract` - Full financial data extraction

## Advanced Usage

### Automated Insights
```bash
# Schedule weekly insights
0 8 * * 1 /dr-insights --env app --output-pptx tmp/weekly_insights.pptx
```

### Comparative Analysis
```bash
# Generate for multiple quarters
/dr-insights --year 2025 --quarter Q1 --output-pptx tmp/Q1.pptx
/dr-insights --year 2025 --quarter Q2 --output-pptx tmp/Q2.pptx
# Compare side-by-side
```

### Custom Reporting
```bash
# Export data in custom location
/dr-insights --env app \
  --output-xlsx /shared/reports/latest_analysis.xlsx \
  --output-pptx /shared/reports/latest_presentation.pptx
```

## Customization

Insights adapt automatically to whatever the discovery step (Phase 1)
finds in the client's environment:
- Different account hierarchies
- Custom KPI definitions (whatever `list_business_metrics` surfaces)
- Department structures
- Business rules

No setup or profile file is needed — the skill rediscovers the table
and fields on each cold session.

## Data Freshness

Reports include generation timestamp. Data reflects:
- The default report scope: latest complete fiscal year or trailing 12
  closed months (data-scope preamble, item 3) — never an unscoped
  all-time total
- Latest available KPIs (typically current quarter)
- Calculations performed at generation time

For historical comparison, generate reports for multiple periods.
