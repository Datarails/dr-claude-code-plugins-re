---
name: dr-departments
description: Analyze P&L and performance by department. Creates departmental reports and comparative analysis with Excel and PowerPoint outputs.
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
  - mcp__datarails-finance-os__list_business_metrics
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--department <name>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Department Analytics

Analyze departmental P&L performance and resource allocation.

Creates detailed departmental reports for team leads and management reviews.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--department <name>` | Specific department (optional) | All departments |
| `--output-xlsx <file>` | Excel output path | `tmp/Department_Analysis_YYYY_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Department_Review_YYYY_TIMESTAMP.pptx` |

## Data Discovery

Run discovery before any aggregation — table, field, and category names differ per org and are never hardcoded:

1. **Table** — `list_data_models` to find the financials table (id + alias).
2. **Fields** — `get_fields_by_id` (or `list_aliased_fields`) to identify the department-like dimension (alias/name matching `/department|cost.?center|team|business.?unit/i`), the account-hierarchy level fields, the scenario field, the date field, and the amount field. If no department-like field exists, say so and offer the closest discovered dimension instead.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`get_distinct_values_by_alias`/`_by_id`) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

Bind the analysis to what discovery returned:

- **Department P&L categories** (revenue / COGS / OpEx-like buckets) come from the account-hierarchy level chosen in item 2 above — build every per-department P&L at that grain, scoped to P&L flows with balance-sheet buckets excluded.
- **Plan comparisons** use whichever plan side the org actually has: a budget-like scenario if one appears in the discovered scenario domain, otherwise versions of the discovered planning-version-like field. If neither exists, drop the plan-vs-actual sections and tell the user which scenarios do exist.
- **Period scope** — filter every aggregate to the requested `--year` via the discovered date field (this is the skill's default scope per item 3; never an unscoped all-time total), and label every sheet and slide with the period + scenario (and plan version, if any) it covers.

## Department Metrics

### Revenue & Expense
- Department revenue
- Expense breakdown
- Net contribution

Categorized at the discovered account grain — P&L flows only; balance-sheet buckets are never presented as revenue or expense.

### Performance
- Plan vs actual (against the discovered plan side — budget-like scenario or planning version; skipped, with a note, if the org has neither)
- Variance analysis
- Year-over-year comparison

### Efficiency
- Per-employee metrics
- Cost per unit
- Productivity indicators

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
| Chart 2 | `F93576` | Budget/Plan (hot pink) |
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

### Excel Department Pack
- Summary by department
- Detailed P&L per department (at the discovered account grain, P&L flows only)
- Variance analysis
- Comparison charts

Every sheet is labeled with the period + scenario (and plan version, if any) it covers.

### PowerPoint Department Review
- One slide per department
- Key metrics highlight
- Plan performance (only when a plan side was discovered — budget-like scenario or planning version)
- Comparison to average

Every slide states the period + scenario it covers.

## Examples

### Analyze all departments
```bash
/dr-departments --year 2025
```

### Specific department review
```bash
/dr-departments --year 2025 --department Engineering
```

### Custom output
```bash
/dr-departments --year 2025 \
  --output-xlsx reports/depts_2025.xlsx \
  --output-pptx reports/dept_review.pptx
```

## Use Cases

### Monthly Department Reviews
```bash
# Share with department heads
/dr-departments --year 2025
```

### Department Head Meetings
```bash
# Individual department analysis for team
/dr-departments --year 2025 --department Marketing
```

### Executive Dashboard
```bash
# Department comparison for leadership
/dr-departments --year 2025
```

### Budget Planning
```bash
# Department historical analysis
/dr-departments --year 2024
/dr-departments --year 2025
# Use for next year planning
```

## Performance

- Analysis: 1-2 minutes
- Scales to all departments
- Professional output

## Department Metrics Included

**Financial**:
- Revenue
- Expenses
- Net contribution

**Operational**:
- Headcount
- Per-employee metrics
- Productivity

**Performance**:
- Plan variance (when a discovered plan side exists)
- Trend analysis
- YoY comparison

## Features

**Excel Report**:
- Summary by department
- Per-department P&L sheets
- Sortable data
- Print-friendly

**PowerPoint Review**:
- One slide per dept
- Key metrics
- Trend indicators
- Professional layout

## Integration

Works with:
- `/dr-insights` - Context for trends
- `/dr-dashboard` - Department KPIs
- `/dr-reconcile` - Validation
- `/dr-extract` - Data sourcing

## Related Skills

- `/dr-insights` - Trend analysis
- `/dr-dashboard` - KPI monitoring
- `/dr-reconcile` - Data validation
- `/dr-extract` - Data extraction
