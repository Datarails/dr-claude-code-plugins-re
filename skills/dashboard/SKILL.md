---
name: dr-dashboard
description: Generate executive KPI dashboard with real-time metrics. Creates Excel dashboards and PowerPoint one-pagers.
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
argument-hint: "[--period <YYYY-MM>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Executive KPI Dashboard

Generate real-time KPI monitoring dashboards for executive teams.

Creates both Excel dashboards (for analysis) and PowerPoint one-pagers (for meetings).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--period <YYYY-MM>` | Month to dashboard for | Latest closed month discovered in the data (never assume the calendar month has data) |
| `--output-xlsx <file>` | Excel output path | `tmp/Executive_Dashboard_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Dashboard_OnePager_TIMESTAMP.pptx` |

## Data Discovery

Before fetching any numbers, discover what the org actually has: `list_data_models` for the financials table, then `get_fields_by_id` / `list_aliased_fields` for its fields. Never assume field names, scenario values, or metric availability — they differ per org.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

## Key Metrics Included

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

The lists below are **candidates**, not guarantees — each card renders only when sourceable per the rule above:

**Growth & Revenue**:
- ARR (Annual Recurring Revenue)
- Revenue
- MoM/QoQ growth rates

**Health & Efficiency**:
- Churn rate (%)
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)

**Operational**:
- Burn rate (monthly)
- Runway (months of cash)
- Burn multiple

**Custom Metrics**: Any KPI in your data (adapts to profile)

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
| Chart 2 | `F93576` | Budget/plan series — whichever plan side discovery found (hot pink) |
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

## Output

### Excel Dashboard
- Summary sheet with top KPIs
- All Metrics sheet with complete list
- Current values
- Status indicators (✅ or ⚠️)
- Period + scenario label on every sheet and figure

### PowerPoint One-Pager
- Single professional slide
- Top metrics in boxes
- Color-coded for quick scanning
- Period + scenario stated on the slide
- Generated timestamp
- Perfect for executive team syncs

## Examples

### Generate dashboard for the latest closed month
```bash
/dr-dashboard
```

Output (illustrative — your org's period, metric count, and values will differ):
```
📊 Generating dashboard for 2026-02...
  📈 Fetching KPI metrics...
  📊 Calculating trends...
  📋 Generating Excel dashboard...
  🎯 Generating PowerPoint one-pager...

✅ Dashboard generated successfully

==================================================
EXECUTIVE DASHBOARD
==================================================
Period: 2026-02
Metrics: 7

Outputs:
  Excel: tmp/Executive_Dashboard_2026-02-03_143022.xlsx
  PowerPoint: tmp/Dashboard_OnePager_2026-02-03_143022.pptx
==================================================
```

### Specific month
```bash
/dr-dashboard --period 2025-12
```

### With custom locations
```bash
/dr-dashboard \
  --output-xlsx reports/dashboard.xlsx \
  --output-pptx reports/dashboard.pptx
```

## Use Cases

### Daily Executive Sync
```bash
/dr-dashboard  # Use PowerPoint for standup
```

### Weekly Team Update
```bash
# Share Excel for details, PowerPoint for overview
/dr-dashboard
```

### Monthly Board Package
```bash
# Generate for month-end
/dr-dashboard --period 2026-01
```

### Investor Demo
```bash
# Professional one-pager
/dr-dashboard --output-pptx investors_dashboard.pptx
```

## Performance

- Generation: <2 minutes
- Real-time KPI data
- Scales to 100+ metrics
- Efficient aggregation

## Color Coding

- ✅ **Green** - Positive metrics (high revenue, low churn)
- ⚠️ **Yellow** - Needs attention (rising burn, declining growth)
- 🔴 **Red** - Critical (low runway, high churn)

## Features

**Excel Dashboard**:
- Sortable data
- Easy drill-down
- Print-friendly
- Shareable format

**PowerPoint One-Pager**:
- Executive-ready
- Meeting-ready (1 slide)
- Branded template
- Easy to share

## Automated Updates

Schedule weekly updates:
```bash
# Every Monday at 8 AM
0 8 * * 1 /dr-dashboard \
  --output-pptx reports/weekly_dashboard.pptx
```

## Integration

Works with:
- `/dr-insights` - Understand why metrics changed
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-extract` - Get latest data

## Related Skills

- `/dr-insights` - Detailed trend analysis
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-forecast-variance` - Forecast vs actual
