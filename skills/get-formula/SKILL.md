---
name: dr-get-formula
description: Generate Excel workbooks with DR.GET formulas that pull live financial data from Datarails. Creates P&L templates, budget models, and variance reports with validated dimension values. Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
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
  - mcp__datarails-finance-os__list_xl_functions
  - Write
  - Read
  - Bash
  - execute_office_js
argument-hint: "[--type summary|detail|budget|variance] [--year <YYYY>] [--output <file>]"
---

# DR.GET Formula Workbook Generator

Generate Excel workbooks containing DR.GET formulas that pull live financial data from Datarails when opened with the Datarails Excel Add-in.

**DR.GET** is a custom Excel function that bridges Datarails' centralized financial database and Excel-based models. Formulas auto-refresh when the workbook is opened with the add-in active.

> **⚠️ Excel context — refresh through the agent after writing formulas.** If this skill runs
> in a **live Excel context** (add-in agent bridge available) and writes `=DR.GET(...)` formulas
> into the open workbook, the cells show **"Loading…" / `#BUSY!` / `#N/A`** until refreshed.
> You **MUST** fire an agent refresh afterward — `refresh_selected_cells_ribbon` (written range)
> or `refresh_ribbon` (whole workbook) via the Excel Add-In bridge (the refresh-after-insert
> delegation point of the Excel Context Contract in CLAUDE.md) — and **never** report a value before that refresh,
> and **never** substitute a native Excel recalc (it won't pull Datarails data). Writing DR.GET
> formulas and refreshing them is one atomic step. (File-output mode in Claude Code is exempt —
> the formulas populate when the user opens the file with the add-in.)

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--type <type>` | Report type: `summary`, `detail`, `budget`, `variance` | `summary` |
| `--year <YYYY>` | Calendar year for date headers | Current year |
| `--output <file>` | Output file path | `tmp/DR_GET_<type>_<YEAR>.xlsx` |

## Adapting to the client's environment

This skill is **self-contained**: every Datarails environment names its
financials table and fields differently, so it discovers the table, the
field mappings, and the valid dimension values it needs **inline**, as the
first data step of its own workflow (Phase 1, Step 2). It does not depend on
a saved profile, a learn step, or any prior setup. Every value written into
a DR.GET formula is validated against the live table during discovery.

---

## DR.GET Syntax Reference

```
=DR.GET(Value, "[Dimension1]", CellRef1, "[Dimension2]", CellRef2, ...)
```

### Syntax Rules

| Rule | Detail |
|------|--------|
| **Function name** | Always `Value` (no brackets, no quotes) — and the workbook must define the name `Value` (see below) |
| **Dimension names** | In square brackets inside double quotes: `"[Reporting Date]"` |
| **Dimension values** | Always **cell references**, never hardcoded strings |
| **Pair structure** | Every dimension is a `"[DimensionName]", CellRef` pair |
| **Cell references** | Use `$A$1` (absolute), `$A1` (mixed), or `A1` (relative) as appropriate |

### CRITICAL: Pin the `Value` token with a defined name

`Value` is a bare identifier, so Excel parses it as a **defined-name
reference**. Workbooks authored by the Datarails Add-in resolve it; a
workbook generated from scratch does not — and Excel autocorrects the
unknown token to its built-in `VALUE` function, silently turning
`=DR.GET(Value, …)` into Excel's `VALUE` formula and breaking it for the
add-in.

Neutralize this by creating a workbook-scoped defined name `Value` that
refers to the string constant `"Value"`, immediately after constructing the
workbook:

```python
from openpyxl.workbook.defined_name import DefinedName
wb = openpyxl.Workbook()
wb.defined_names.add(DefinedName("Value", attr_text='"Value"'))  # openpyxl >= 3.1
```

With the name defined the token resolves, Excel has nothing to autocorrect,
and the formula text is preserved exactly as the add-in expects. Never skip
this step, and never quote the token in the formula instead — `"Value"` as a
string literal diverges from the canonical form the add-in recognizes.

### Date Dimension

`[Reporting Date]` requires **Excel serial date numbers** (end-of-month), NOT text strings.

**How to calculate EOM serial dates:**
```python
from datetime import date
EXCEL_EPOCH = date(1899, 12, 30)
# January 2026 EOM = Jan 31, 2026
serial = (date(2026, 1, 31) - EXCEL_EPOCH).days  # = 46053
```

Store the serial number as the cell value and apply `'MMM-YY'` number format so it displays as "Jan-26" while DR.GET reads the numeric serial.

### Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Writing formulas without the `Value` defined name | Add the workbook-scoped name `Value` = `"Value"` first — otherwise Excel autocorrects the token to its `VALUE()` function |
| Transliterating an MCP/API call into the formula: `=DR.GET(Value,"financials","Amount","SUM",...)` | DR.GET takes no table/field/aggregation arguments — only `"[Dimension]", CellRef` pairs after `Value` |
| Hardcoding values in DR.GET: `"Actuals"` | Always reference a cell: `$B$1` |
| Using text month: `"January 2026"` | Use EOM serial number: `46053` |
| Writing API epoch timestamps as date headers | Compute EOM serials from the calendar (see Date Dimension) — raw epochs land a day early with a time component |
| Using `[Account]` or `[Month]` | Use the actual field names discovered in Step 2 |
| Using Report_Field without scoping | Always include `[DR_ACC_L2]` alongside `[Report_Field]` |
| Inventing or guessing dimension values | Validate against actual distinct values first |
| Using `Scenario="Budget"` | Use `Scenario="Forecast"` + `Scenario Cycle` + `Planning Scenario` |
| Wrapping DR.GET in IFERROR/IF/other functions | DR.GET must be bare: `=DR.GET(...)` only |
| Adding fallback values for missing data | Let DR.GET return empty/0 — users need to see gaps |
| Pointing to cells that don't contain data | Every cell reference must point to an actual parameter or header cell |

### CRITICAL: DR.GET Formulas Must Be Simple

**NEVER** wrap DR.GET formulas in any other Excel function. Write them as bare formulas only.

```
WRONG:  =IFERROR(DR.GET(Value, "[Scenario]", $B$1, ...), 0)
WRONG:  =IF(DR.GET(Value, ...) > 0, DR.GET(Value, ...), "")
WRONG:  =ROUND(DR.GET(Value, ...), 2)
RIGHT:  =DR.GET(Value, "[Scenario]", $B$1, "[DR_ACC_L1.5]", $A6, "[Reporting Date]", B$5)
```

**Why:** The Datarails Add-in manages DR.GET formulas. Wrapping them in other functions breaks the add-in's ability to refresh, track, and drill down on them. If data is missing, the cell should show 0 or empty — this is valuable information that users need to see, not mask.

**Cell references must be intentional.** Every cell reference in a DR.GET formula must point to a specific cell that contains a validated parameter value (scenario name, account name, date serial). Never generate references to empty cells or cells outside the data layout.

---

## Workflow

### Phase 1: Setup

#### Step 1: Verify Authentication
```
If any tool call fails with a connection error, guide the user to connect via Connectors UI.
```

#### Step 2: Discover the financials table and its fields

**If you already discovered the financials table and its field mappings
earlier in THIS conversation, reuse them — skip to Phase 2.** Discovery is
cheap but not free; do it once per conversation, then carry the values
forward.

1. `list_data_models`. Pick the financials table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Note **both** its numeric `id` (call it
   `<financials_table_id>`) and its `alias` (call it `<financials_alias>`; the
   alias may be empty). **Prefer the alias path when an alias exists** —
   friendlier field names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<financials_alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each field's
   numeric `id` — the by-id tools address fields by id). From the fields, bind
   these by case-insensitive match on the field alias/name (respecting the
   noted type). Only the fields this skill actually puts into formulas are
   needed:
   - `<amount_field>`     — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`   — categorical: `^scenario$` → `^version$`
   - `<date_field>`       — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_5_field>` — `dr_acc_l1.5` → `dr_acc_l1_5` → `account_l1_5` → `dr_acc_l1` → `account_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2`
   - `<report_field>`     — `report_field` → `report field`
   - `<cycle_field>`      — `scenario cycle` → `scenario_cycle`
   - `<planning_field>`   — `planning scenario` → `planning_scenario`

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue. The cycle / planning / report fields
   are only needed for `--type budget`, `--type variance`, and `--type
   detail`; if they're absent and the requested report type doesn't use them,
   ignore them.

3. Discover the DR.GET function token. `list_xl_functions`. Each entry's
   `name` is the exact token DR.GET expects as its **first** argument
   (`=DR.GET(<FunctionName>, "[Dimension]", CellRef, …)`), and its
   `template.id` is the owning table — match the function whose `template`
   resolves to `<financials_table_id>`, and bind its `name` as
   `<value_function>`. Most environments name it `Value`; do not assume that —
   use the discovered token. (If `list_xl_functions` returns nothing usable,
   fall back to `Value`, the canonical default the add-in resolves.) Wherever
   this skill writes the literal `Value` token below, substitute
   `<value_function>`; the defined-name guidance in the Syntax Reference
   applies to whatever token you use.

The valid dimension **values** for these fields (account categories,
scenarios, cycles, planning scenarios) are discovered and validated in
Phase 2 below — every value written into a DR.GET formula must come from the
live table.

**Aggregation-field failures are handled reactively, not pre-probed.** If a
later aggregation call (used in Phase 2 for value discovery) 500s on a
dimension field, re-inspect the Step 2 schema for a sibling (e.g.
`DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`) and retry with
it; if an alias call fails, fall back to the by-id twin.

### Phase 2: Dimension Discovery & Validation

**CRITICAL: Every value used in a DR.GET formula must be validated against the live Datarails table.**

#### Step 3: Discover Account Hierarchy

Use the financials table (alias or id) and the fields discovered in Step 2.

Discover the account values directly from the distinct-values API:
```
# Alias path (preferred)
get_distinct_values_by_alias(<financials_alias>, <account_l1_5_field>)
get_distinct_values_by_alias(<financials_alias>, <account_l2_field>)
# By-id fallback (no alias)
get_distinct_values_by_id(<financials_table_id>, <account_l1_5_field_id>)
```
If a distinct call errors, fall back to sampling rows and collect the values
client-side:
```
get_data_by_alias(<financials_alias>, select=[<account_l1_5_field>, <account_l2_field>], limit=500)
#   (or get_data_by_id(<financials_table_id>, select=[<account_l1_5_field_id>, ...], limit=500))
#   → distinct <account_l1_5_field> values, distinct <account_l2_field> values
```

If you need exact totals or a fuller value set, aggregation also surfaces the
distinct values as group keys:
```
get_aggregated_data_by_alias(<financials_alias>, dimensions=[<account_l1_5_field>], metrics=[{"field": <amount_field>, "agg": "SUM"}])
#   (or get_aggregated_data_by_id(<financials_table_id>, dimensions=[<account_l1_5_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]))
```
(If this 500s on `<account_l1_5_field>`, swap to a sibling per Step 2's
reactive-retry note; if the alias call fails, fall back to the by-id twin.)

#### Step 4: Discover Scenario Values

Collect the distinct values for the scenario dimensions with
`get_distinct_values_by_alias(<financials_alias>, <scenario_field>)` (or the
by-id twin). For `--type budget` / `--type variance` you also need
`<cycle_field>` and `<planning_field>` values; do the same distinct call for
each, or confirm them via aggregation:
```
get_aggregated_data_by_alias(<financials_alias>, dimensions=[<scenario_field>], metrics=[{"field": <amount_field>, "agg": "SUM"}])
#   (or get_aggregated_data_by_id(<financials_table_id>, dimensions=[<scenario_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]))
# and likewise for <cycle_field>, <planning_field> when the report type uses them
```

#### Step 5: Map Parent-Child Relationships (for detail reports)

For `--type detail`, discover which child values belong to which parent:
```
# For each L1.5 value, find which L2 values belong to it
get_aggregated_data_by_alias(
  <financials_alias>,
  dimensions=[<account_l1_5_field>, <account_l2_field>],
  metrics=[{"field": <amount_field>, "agg": "COUNT"}],
  filters=[{"name": <scenario_field>, "values": ["Actuals"], "is_excluded": false}]
)
#   (by-id twin: get_aggregated_data_by_id(<financials_table_id>,
#    dimensions=[<account_l1_5_field_id>, <account_l2_field_id>],
#    metrics=[{"field_id": <amount_field_id>, "agg": "COUNT"}],
#    filters=[{"field_id": <scenario_field_id>, "values": ["Actuals"]}]))
```

For Report_Field detail, also map L2 → Report_Field relationships.

#### Step 6: Build Validated Value Registry

Store all discovered values in a dict structure:
```python
registry = {
    "account_l1_5": ["Revenues", "COGS", ...],  # from live API
    "account_l2": {"Revenues": ["Income"], "S&M": ["Marketing", "Sales", ...], ...},
    "report_fields": {"Sales": ["Events", "Payroll & Benefits", ...], ...},
    "scenarios": ["Actuals", "Forecast"],
    "scenario_cycles": ["0+12", "1+11", ...],
    "planning_scenarios": ["Actuals", "Bottom up", "Budget", ...]
}
```

**Every value in the workbook MUST come from this registry. Never hardcode or guess values.**

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

### Phase 3: Workbook Generation

#### Step 7: Generate Excel with openpyxl

Use Bash to run a Python script (inline or from file) that generates the workbook using openpyxl.

**First line of workbook setup — before writing any formula:** add the
`Value` defined name (`wb.defined_names.add(DefinedName("Value",
attr_text='"Value"'))`, see the Syntax Reference). Without it, Excel
autocorrects `Value` to its built-in `VALUE` function on open and every
DR.GET formula in the file breaks.

**Workbook Structure by Report Type:**

##### `--type summary` (Summary P&L)
- **Parameter cells** (Row 1-3): Scenario, Scenario Cycle, Planning Scenario
- **Date headers** (Row 5): EOM serial dates formatted as MMM-YY
- **P&L rows** (Row 6+): One row per L1.5 value (from registry)
- **Calculated rows**: Gross Profit, Total OpEx, Operating Income, Net Income
- **Two sheets**: Actuals, Budget

##### `--type detail` (Departmental Detail)
- Same parameter/date structure as summary
- Rows grouped by L1.5 parent with L2 children indented
- Subtotal rows per L1.5 group

##### `--type budget` (Budget Template)
- Scenario pre-set to Forecast
- Scenario Cycle defaults to 0+12
- Planning Scenario defaults to Bottom up
- All L1.5 line items with monthly columns

##### `--type variance` (Actuals vs Budget)
- Two formula blocks: Actuals and Budget
- Variance columns (Actual - Budget) as Excel formulas (not DR.GET)
- Variance % columns

#### DR.GET Formula Construction

**Every DR.GET formula must be a bare `=DR.GET(...)` call. No IFERROR, no IF, no ROUND, no wrapping of any kind.**

**Actuals formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{date_field}]", {{col}}$5)'
```

**Budget formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{cycle_field}]", $B$2, "[{planning_field}]", $B$3, "[{date_field}]", {{col}}$5)'
```

**Detail formula (with L2 scoping):**
```python
f'=DR.GET(Value, "[{report_field}]", $A{{row}}, "[{l2_field}]", $B{{row}}, "[{scenario_field}]", $D$2, "[{date_field}]", {{col}}$5)'
```

**Cell reference map** — each reference in the formula must point to:
- `$A{row}` → the account/line item label in column A of that row
- `$B$1` → the Scenario parameter cell (e.g., "Actuals")
- `$B$2` → the Scenario Cycle parameter cell (e.g., "0+12")
- `$B$3` → the Planning Scenario parameter cell (e.g., "Bottom up")
- `{col}$5` → the date header in row 5 of that column (EOM serial number)
- `$B{row}` → the L2 scoping value in column B of that row (detail reports)

If a reference doesn't map to one of these known locations, it is wrong. Do not invent references.

#### Excel Formatting

```python
# Date headers: serial number with MMM-YY format
cell.value = serial_number
cell.number_format = 'MMM-YY'

# Financial cells: number format
cell.number_format = '#,##0'

# Parameter cells: clear labels
ws['A1'] = 'Scenario:'
ws['B1'] = 'Actuals'  # validated value from registry

# Calculated rows: Excel formulas (NOT DR.GET)
# Gross Profit = Revenue - COGS
ws.cell(row=gp_row, column=col).value = f'={get_column_letter(col)}{rev_row}-{get_column_letter(col)}{cogs_row}'
```

#### Calculated Lines (No DR.GET)

These P&L lines are always Excel formulas referencing other rows:

| Line | Formula Pattern |
|------|----------------|
| Gross Profit | `= Revenue_row - COGS_row` |
| Total OpEx | `= SUM(opex_line_rows)` |
| Operating Income | `= Gross_Profit_row - Total_OpEx_row` |
| Net Income | `= Operating_Income_row - Finance_row - Tax_row` |

### Phase 4: Save & Report

#### Step 8: Save Output & Verify

Save to `tmp/DR_GET_<type>_<YEAR>.xlsx` or the user-specified `--output` path.

Then re-open the saved file and verify it before reporting success:

```python
check = openpyxl.load_workbook(out_path)
assert "Value" in check.defined_names, "defined name 'Value' is missing — Excel will autocorrect the token to VALUE()"
for ws in check.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "DR.GET" in c.value:
                assert c.value.replace(" ", "").startswith("=DR.GET(Value,"), \
                    f"bad DR.GET formula in {ws.title}!{c.coordinate}"
```

If either assertion fails, fix the workbook and re-save — do not hand the
user a file that fails verification.

#### Step 9: Report to User

Report what was generated:
- Number of validated dimension values used
- Number of DR.GET formulas written
- Number of calculated rows
- Output file path
- Reminder: "Open this workbook with the Datarails Excel Add-in active to refresh formulas."

---

## Examples

### Summary P&L with Actuals
```bash
/dr-get-formula --type summary --year 2026
```

### Detailed departmental breakdown
```bash
/dr-get-formula --type detail --year 2026
```

### Budget template
```bash
/dr-get-formula --type budget --year 2026
```

### Actuals vs Budget variance
```bash
/dr-get-formula --type variance --year 2026
```

### Custom output location
```bash
/dr-get-formula --type summary --year 2026 --output tmp/PnL_Template_2026.xlsx
```

---

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**No table matches the financials pattern in Step 2**
- List the tables you found and ask the user which one holds their P&L /
  financial data, then continue with that table.

**A field can't be bound in Step 2 (e.g. no scenario cycle / planning field)**
- For report types that don't use it, ignore it. For `--type budget` /
  `--type variance`, ask the user which field to use, or fall back to a
  single-scenario formula pattern.

**`Value` turned into Excel's `VALUE` function after opening the workbook**
- The workbook was generated without the `Value` defined name, so Excel
  autocorrected the unknown token to its built-in `VALUE()` function.
- Regenerate with this skill — it now always writes the defined name and
  verifies it after saving. To repair an existing file instead: add a
  workbook-scoped name `Value` referring to `="Value"`, then restore each
  formula's first argument to the bare token `Value`.

**DR.GET formulas return 0 or errors when opened in Excel**
- Verify the Datarails Excel Add-in is active
- Check that dimension values match exactly (case-sensitive, exact spelling)
- Re-run the skill to re-validate values against live data

**A distinct-values call errors**
- Use `get_distinct_values_by_alias` / `get_distinct_values_by_id`. If a call
  errors, the skill falls back to sampling rows (`get_data_by_alias` /
  `get_data_by_id`, small limit) or aggregation group keys for value discovery.

**Missing dimension values**
- The live data may not contain all expected categories
- Check with `/dr-query` to investigate the table directly

**Date headers show numbers instead of month names**
- The serial numbers are correct; apply `MMM-YY` number format in Excel
- The generated workbook should already have this format applied
