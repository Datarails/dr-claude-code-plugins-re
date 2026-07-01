---
name: dr-reconcile
description: Reconcile P&L vs KPI data sources. Validates consistency and identifies discrepancies with variance analysis.
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
argument-hint: "--year <YYYY> [--scenario <name>] [--tolerance-pct <#>] [--output <file>]"
---

# P&L vs KPI Reconciliation

Validate consistency between P&L and KPI data sources. Identifies discrepancies and explains variances.

Essential for month-end close and financial validation.

## How it pulls the two sides

This skill is **self-contained** — it discovers the client's financials table,
fields, and account categories inline (every Datarails environment names them
differently; there is no saved profile). Do discovery once per conversation,
then carry the values forward.

1. **Discover the financials table and fields.** `list_data_models` → pick the
   table whose name/alias matches `/financial|cube|p&?l|ledger|gl/i`, else the
   largest by row count; note **both** its numeric `id` and its `alias` (alias
   may be empty — prefer the alias path when present). Then
   `list_aliased_fields(<alias>)` if it has an alias, else
   `get_fields_by_id(<id>)` (capture each field's numeric `id`). Bind by
   case-insensitive match: `amount` (`^amount$` → `transaction_amount` →
   `value`), `scenario` (`^scenario$` → `^version$`), `date` (`reporting_date` →
   `posting_date` → `^date$`), `account_l1` (`dr_acc_l1` → `account_l1` →
   `account_group_l1`).

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

2. **Discover the account categories.**
   `get_distinct_values_by_alias(<alias>, <account_field>)` (or
   `get_distinct_values_by_id(<id>, <account_field_id>)`); if that errors, fall
   back to `get_data_by_alias(<alias>, select=[<account_field>], limit=500)` (or
   the by-id twin) and dedupe. Match `revenue` `/revenue|sales|income/i`, `cogs`
   `/cogs|cost of goods|cost of sales|direct cost/i`, `opex`
   `/operating|opex|expense|sg&a/i`.

3. **P&L side — real totals by category.**
   `get_aggregated_data_by_alias(<alias>, dimensions=[<account_field>],
   metrics=[{"field": <amount_field>, "agg": "SUM"}], filters=[{"name":
   <scenario_field>, "values": [<--scenario> or "Actuals"], "is_excluded":
   false}])` (preferred), or the by-id twin
   `get_aggregated_data_by_id(<id>, dimensions=[<account_field_id>],
   metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}], filters=[{"field_id":
   <scenario_field_id>, "values": [...]}])`. Scope the year with an **advanced**
   date filter — `{"name": <date_field>, "values": {"type": "advanced", "val":
   [{"condition": "total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}`
   (epoch seconds as strings) — or add `<date_field>` as a dimension and filter
   client-side.

4. **KPI side — named metrics.** `list_business_metrics` returns the flat KPI
   catalog (each entry: `id`, `name`, `description`, `category`, `kind`,
   `dimensions[]`, `status_info{}`). Match the revenue / expense KPIs by name and
   compute their values from the **same aggregated data** (`get_aggregated_data_by_alias`
   / `get_aggregated_data_by_id`) so both sides are reconciled against the same
   underlying rows. Reconciliation then compares the P&L total against the KPI
   value for each line.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to reconcile | — |
| `--scenario <name>` | Scenario to reconcile | `Actuals` |
| `--tolerance-pct <#>` | Acceptable variance threshold | `5.0` |
| `--output <file>` | Output file path | `tmp/Reconciliation_YYYY_TIMESTAMP.xlsx` |

## What It Validates

### Revenue Consistency
- P&L Revenue vs KPI Revenue
- Within tolerance threshold
- Identifies timing differences

### Expense Completeness
- COGS + Operating Expense coverage
- Validation of expense structure
- Missing expense categories

### Data Completeness
- All expected accounts present
- All expected KPI metrics available
- Data quality validation

### Variance Analysis
- Absolute variance amounts
- Percentage variance
- Tolerance compliance
- Root cause identification

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

## Output

Excel report with multiple sheets:

1. **Summary** - Pass/fail status, metrics, exception count
2. **Validation Rules** - Detailed results of each check
3. **Exceptions** (if any) - Issues exceeding tolerance
4. **P&L Summary** - Revenue, expenses by account
5. **KPI Summary** - All KPI values for verification

## Examples

### Reconcile current year (default 5% tolerance)
```bash
/dr-reconcile --year 2025
```

### Strict reconciliation (1% tolerance)
```bash
/dr-reconcile --year 2025 --tolerance-pct 1.0
```

### Reconcile specific scenario
```bash
/dr-reconcile --year 2025 --scenario Forecast
```

### Custom output location
```bash
/dr-reconcile --year 2025 --output reports/reconciliation_2025.xlsx
```

## Use Cases

### Month-End Close
Run after data extraction to validate:
```bash
/dr-extract --year 2025
/dr-anomalies-report --severity critical    # Check quality
/dr-reconcile --year 2025 --tolerance-pct 2 # Validate consistency
```

### Financial Review
Reconcile before presentations:
```bash
/dr-reconcile --year 2025 --scenario Actuals
```

### Audit Preparation
Reconcile with strict tolerance:
```bash
/dr-reconcile --year 2025 --tolerance-pct 0.5
```

## Performance

- Year reconciliation: ~30-60 seconds
- Includes 3+ validation checks
- Scalable to large data volumes

## Error Handling

**"Revenue not found"** - Re-run discovery (`list_data_models` → `list_aliased_fields`/`get_fields_by_id` → `get_distinct_values_by_alias`/`get_distinct_values_by_id`) and confirm the P&L account category and the matching KPI metric name. There is no profile — discovery happens inline.

**"Variance exceeds tolerance"** - Review exception sheet for details

**"Incomplete data"** - Run `/dr-extract` to refresh data first

## Related Skills

- `/dr-extract` - Get latest financial data
- `/dr-anomalies-report` - Check data quality
- `/dr-dashboard` - Verify KPI values
- `/dr-insights` - Understand trends driving reconciliation items
