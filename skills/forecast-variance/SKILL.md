---
name: dr-forecast-variance
description: Analyze budget vs forecast vs actual variances. Compares multi-scenario financial data for planning and performance review.
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
  - execute_office_js
argument-hint: "--year <YYYY> [--scenarios <list>] [--period <YYYY-MM>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Forecast Variance Analysis

Analyze variances between Actuals, Budget, and Forecast scenarios.

Essential for FP&A reviews, planning adjustments, and performance tracking.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to analyze | — |
| `--scenarios <list>` | Comma-separated scenarios | `Actuals,Budget,Forecast` |
| `--period <YYYY-MM>` | Specific period to focus on | All year |
| `--output-xlsx <file>` | Excel output path | `tmp/Forecast_Variance_YYYY_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Forecast_Summary_YYYY_TIMESTAMP.pptx` |

## Excel Context Mode (Claude in Excel)

When this skill is invoked from within **Claude in Excel** (the task pane add-in), switch to in-sheet enrichment mode instead of generating output files. This mode integrates the row-commentary approach from `datarails-excel-multi-table-analysis` and is the **preferred mode** when the user is working directly in a workbook.

**How to detect the context:** Excel context mode activates when the user has an open workbook and wants in-sheet enrichment — with or without an existing range. This applies in Claude for Excel (task pane), Claude Code with an open workbook, or any context where the user is working directly in a spreadsheet. Do **not** generate `.xlsx` or `.pptx` output files. Write all output directly into the active workbook using whichever Excel cell-write tool is available to you. Never use the `Write` tool to write spreadsheet content in this context. If no cell-write tool is available, fall back to file output mode and tell the user.

### Step 0 — Verify Excel context (always first in Excel context)

Before any data pull or schema discovery, run the `agent.get_session` probe through the
bridge. **`agent.get_session` is not an MCP tool** — you run it by executing Office.js via
the `execute_office_js` tool to write the request to the `__dr_agent` sheet and read the
response (see `datarails-excel-agent` §Transport + §2/§3). Do **not** call the
`datarails-finance-os` MCP connector for this.

- **Probe fails** (no `execute_office_js` / Office.js tool, or no bridge sheet) → not in Excel context. Fall back to file-output mode. Stop here.
- **Probe succeeds** → Excel context confirmed. Now branch on login state:
  - **Flex** (response has `isLoggedIn`): if `isLoggedIn` is **false**, tell the user to sign in to Datarails and **stop** — do not reach Step 0b. If **true**, proceed to Step 0b.
  - **COM** (response has no `isLoggedIn` — it exposes `isConnected` instead): a successful probe means the session is active. Proceed to Step 0b. Do **not** treat `isConnected: false` as a login failure.

> **Do NOT gate analysis on `isConnected`.** Refresh, DR-formula reads, and evaluate all work on an unconnected workbook. `connect_file` is required **only** for `create_dynamic_range` and `drilldown_*`, and **only on COM** (Flex sessions have no `isConnected` field). Check `isConnected` at the drill-down step (Step 6), not here, and only when the session payload contains it. If a drill needs it and `isConnected` is false, ask: *"This drill-down requires the workbook connected to Datarails. Connect now with `connect_file`?"* — wait for explicit yes (mutating command, never auto-call).

**Step 0b — Data refresh (ask once per session, Excel context only):** If `agent.get_session` succeeded, ask: *"Should I refresh data from Datarails before pulling? (Recommended if you haven't refreshed today.)"* If the user confirms, call `refresh_ribbon` (`timeoutMs: 600000`) and wait for terminal status. Skip if the user says no. **On follow-up questions in the same session, do NOT re-ask or re-refresh** — data is already fresh. In non-Excel context, skip entirely — `refresh_ribbon` is not available.

### Step 1 — Discover client-specific dimensions (always first)

Every Datarails customer structures their Financials table differently. **Never hardcode dimension field names.** Before pulling any data, discover the financials table and its two key dimensions.

**If you already discovered these this conversation, reuse them — skip to Step 2.**

`list_data_models` first. Pick the financials table: the one whose name (or alias) matches `/financial|cube|p&?l|ledger|gl/i`, else the largest by row count. Note **both** its numeric `id` and its `alias` (alias may be empty). **Prefer the alias path when an alias exists** — friendlier field names, far fewer tokens.

**Then read the schema — `list_aliased_fields(<alias>)` if the table has an alias, else `get_fields_by_id(<id>)` (capture each field's numeric `id` — the by-id tools address fields by id) — and identify:**

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

| Dimension | What to look for | Common field names |
|-----------|------------------|--------------------|
| **Cost Center** | The field that identifies the organizational unit / department incurring the cost | `Cost_Center`, `DR_Cost_Center`, `Department`, `Dept_Name`, `CostCenter` |
| **Report Field** | The field that identifies the P&L line item / account category as it appears in the customer's report | `Report_Field`, `Report_Line`, `DR_ACC_L1`, `DR_ACC_L2`, `Account_Name`, `Line_Item` |

If multiple candidates exist for either dimension, pick the most specific / granular one. Document both discovered field names — use them in **every aggregation** for this analysis session. These two dimensions are mandatory; omitting either produces commentary that is not actionable.

If the schema genuinely has no identifiable cost center field, flag this in the Read Me block and fall back to the next-best grouping available (e.g., account hierarchy). Never silently drop the dimension.

### Step 2 — Read the active sheet (Phase 0)

Before pulling data, read what is in the active sheet:

- **Enrichment mode**: the user has a range (rows × period columns, variance grid, P&L block). Identify row labels, column headers, data bounds, and the empty space to the right where Commentary + Source Ref columns will go.
- **Cold-question mode**: the sheet is empty or unrelated. Build a fresh variance block from scratch, including Commentary + Source Ref columns from the start.

Do not assume which mode — read the sheet first.

### Step 3 — Pull data using the discovered dimensions (in parallel)

Issue all scenario pulls in a single turn (concurrent tool calls). Use `get_aggregated_data_by_alias` (preferred) or its by-id twin `get_aggregated_data_by_id`. For each pull, always include the discovered **cost center** and **report field** dimensions alongside the period dimension:

```
get_aggregated_data_by_alias(
  alias=<financials_alias>,
  dimensions=[<period_field>, <cost_center_field>, <report_field>],
  metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[
    {"name": <scenario_field>, "values": [<scenario>], "is_excluded": false},
    {"name": <acc_l0_field>,   "values": ["P&L"],      "is_excluded": false},
    {"name": <gaap_field>,     "values": ["Gaap"],     "is_excluded": true}
  ]
)
```

Scope by year either by adding `<date_field>` to `dimensions` and filtering the result client-side, or with an **advanced** date-range filter: `{"name": <date_field>, "values": {"type": "advanced", "val": [{"condition": "total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}` (epoch seconds as strings). Both work — date filtering is no longer rejected.

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>, dimensions=[<period_field_id>, <cost_center_field_id>, <report_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}], filters=[{"field_id": <scenario_field_id>, "values": [...]}])`. If an alias call 500s on a dimension, re-inspect the Step 1 schema for a sibling and retry, or fall back to the by-id twin.

Assign each distinct pull a Source ID: `S1`, `S2`, `S3`, ...

| Source ID | Scenario |
|-----------|----------|
| S1 | Actuals |
| S2 | Budget |
| S3 | Forecast (if in scope) |

**Also pull HeadCount** whenever compensation lines are in scope. Comp $ alone cannot distinguish volume (headcount change) from rate (salary / bonus change) — always decompose. See the HC inference trap in `datarails-excel-multi-table-analysis`.

**Verify data freshness** for each table before quoting period boundaries. If a table is short of the requested period, narrow the window and flag it in the Read Me block and in each affected commentary row.

### Step 4 — Write per-row commentary and source refs

Add two columns to the right of the user's range (or include them in the fresh block):

| ... existing columns ... | Commentary | Source Ref |
|--------------------------|------------|------------|

**Commentary cell rules:**
- One sentence per row, quantified (Δ$ and Δ%)
- Always call out **both** the cost center and the report field in the sentence — these are the two dimensions that make commentary actionable
- End with inline source refs: `[S1, S2]`
- If a decomposition applies (e.g., HC volume vs rate), include it
- If data freshness is a caveat, name it inline

**Example commentary cells:**
> `Marketing expense +$120K (+14%) vs Budget, driven by Events cost center (+$95K, DR_ACC_L2: T&E); remaining $25K in Digital/Software. [S1, S2]`

> `R&D compensation +$280K (+18%) vs Budget: $230K (82%) is rate-driven (Q4 bonus accrual on flat HC of 23), $50K (18%) is volume (2 new hires in Oct). [S1, S2, S3]`

**Source Ref cell:** bracketed refs only — `[S1, S2]`. No commentary in this cell.

> **Citing live DR-formula reads (Excel context):** When a $ figure comes from reading a DR cell (`agent.read_range` / `agent.evaluate_drget`) rather than a `get_aggregated_data_by_alias` pull, cite the cell's `data.sources[]` (sheet!cell + widget) returned by the read — **every $ figure must carry a source**. If a read returns empty `sources`, do not present the figure; re-read or tell the user it isn't Datarails-tracked.

### Step 5 — Build the Sources sheet and Read Me block

**Sources sheet** (`Sources` tab — create if it doesn't exist):

| Source ID | Table | Table ID | Dimensions | Metrics | Filters | Period Window | Rows | Freshness Note |
|-----------|-------|----------|------------|---------|---------|---------------|------|----------------|

One row per distinct Source ID. Every `[S#]` cited in Commentary must have a matching row here.

**Read Me block** (top of the analysis sheet, above the data):

```
SCOPE & FILTERS
  Period:    <e.g., Q1–Q3 2025>
  Scenarios: Actuals vs Budget vs Forecast
  Accounts:  DR_ACC_L0 = "P&L", GAAP excluded
  Cost Center field:  <discovered field name>
  Report Field:       <discovered field name>

SOURCE TABLES (full detail in Sources sheet)
  S1 — Financials: Actuals by period × cost center × report field
  S2 — Financials: Budget by period × cost center × report field
  S3 — HeadCount: FTE by month × cost center (if applicable)

DATA FRESHNESS
  Financials: <latest loaded period>
  HeadCount:  <latest loaded period, or "N/A">
```

### Step 6 — Drill-down menu (mandatory in Excel context — do not skip)

**Excel context + enrichment mode only.** Two conditions must both be true:
1. `agent.get_session` succeeded in Step 0 (Excel context confirmed).
2. You are in **enrichment mode** — the user's sheet had existing **DR formula cells** (`DR.GET`, `DR.QTD`, `DR.YTD`, `DR.MTD`, etc. — any DR function) that you added commentary alongside.

If either condition is false, skip this step entirely and state why:
- Non-Excel context → `drilldown_list` not available.
- **Cold-question mode** → data cells were written as **raw values** from the FinanceOS API (`get_aggregated_data_by_alias`), not DR formulas. `drilldown_list` targets DR formula cells — it has nothing to act on. Tell the user drill-down is unavailable in this mode.

> **Drill-down works on any DR function cell**, not just `DR.GET`. The cell must resolve to a Datarails widget (DR.GET/QTD/YTD/MTD/...). Before firing, if `isConnected` is false, confirm `connect_file` with the user (see Step 0).

If both conditions are true: after writing commentary, you **MUST** output a **Drill-Down Menu** block directly in chat. Do not end the response without it.

The block must list every row where |variance| > 10% or flagged unfavorable, one row per line with its Δ$ and Δ%:

```
📋 Drill-Down Menu — rows with |variance| > 10%
  1. <Row label>  Δ$X.XM  (ΔY%)
  2. <Row label>  Δ$X.XM  (ΔY%)
  ...
```

Then explicitly ask: *"Which rows would you like me to drill into for a cell-level breakdown? I'll call `drilldown_list` on each selected row."*

Only invoke `drilldown_list` (params: `sheetName`, `cellAddress`; `timeoutMs: 180000`) after the user selects rows — do not drill automatically.

### Anti-patterns (Excel context)

- **Never omit the cost center dimension** from commentary — "R&D over budget" is insufficient; name the cost center
- **Never omit the report field dimension** — "expenses up" is insufficient; name the line item
- **Never hardcode dimension field names** — always discover from schema; they vary by client
- **Never write commentary without a `[S#]` ref** — every claim must be auditable
- **Never overwrite the user's existing data** — add columns to the right only
- **Never imply freshness you don't have** — flag any missing periods explicitly

---

## Variance Analysis

### Budget Variance
- Actual vs Budget amounts
- Percentage difference
- Favorable/unfavorable identification
- Trend analysis

### Forecast Variance
- Actual vs Forecast amounts
- Track forecast accuracy
- Identify forecast bias
- Forecast adjustment recommendations

### Multi-Account Analysis
- Revenue variance by product/segment
- Expense variance by department
- Account-level drill-down
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

### Excel Report
- **Summary**: Total variances by scenario
- **Variance Analysis**: Account-by-account comparison
- **Scenario Totals**: Total by scenario
- **Exception Report**: Large variances highlighted

### PowerPoint Summary
- Overview slide: Scenario totals
- Variance slide: Top variances
- Executive summary
- Key findings

## Examples

### Annual variance analysis
```bash
/dr-forecast-variance --year 2025
```

### With custom scenarios
```bash
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
```

### Specific period focus
```bash
/dr-forecast-variance --year 2025 --period 2025-Q4
```

### Custom output
```bash
/dr-forecast-variance --year 2025 \
  --output-xlsx reports/variance_2025.xlsx \
  --output-pptx reports/variance_summary.pptx
```

## Use Cases

### Monthly FP&A Review
```bash
# Compare latest actuals vs budget
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
```

### Forecast Accuracy Tracking
```bash
# Compare forecast prediction accuracy
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast
```

### Full Scenario Planning
```bash
# Complete comparison for board review
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget,Forecast
```

### Department Review
```bash
# Analyze departmental performance vs budget
/dr-forecast-variance --year 2025
```

### Investor Update
```bash
# Professional variance analysis for stakeholders
/dr-forecast-variance --year 2025
```

## Performance

- Analysis: ~1-3 minutes
- Scales to multiple years
- Handles 100+ accounts
- Efficient aggregation

## Interpretation

### Favorable Variance
- Actual > Budget (Revenue) ✅
- Actual < Budget (Expense) ✅

### Unfavorable Variance
- Actual < Budget (Revenue) ❌
- Actual > Budget (Expense) ❌

### % Variance
- <5%: Excellent forecast/budget accuracy
- 5-10%: Good, within normal range
- 10%+: Needs investigation

## Workflow

**FP&A Process**:
```
1. /dr-extract --year 2025       (Get actuals)
2. /dr-reconcile --year 2025     (Validate data)
3. /dr-forecast-variance --year 2025  (Analyze variances)
4. Present findings to leadership (Board meeting)
```

## Advanced Usage

### Track forecast improvement
```bash
# Monthly variance tracking
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast --period 2025-01
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast --period 2025-02
# Compare forecast accuracy trend
```

### Multi-year comparison
```bash
/dr-forecast-variance --year 2024 --scenarios Actuals,Budget
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
# Compare year-over-year performance
```

### Scenario sensitivity
```bash
# Three different budget scenarios
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget_Conservative,Budget_Aggressive
```

## Error Handling

**"Scenario not found"** - Verify scenario exists in data

**"No variance data"** - Confirm Budget/Forecast scenarios available

**"Large variance"** - Review detailed Excel report for root causes

## Integration

Works with:
- `/dr-extract` - Source of scenario data
- `/dr-insights` - Contextual trend analysis
- `/dr-reconcile` - Validate scenario consistency
- `/dr-dashboard` - Current performance view
- `datarails-excel-agent` - In Excel context (see that skill's catalog for exact params/timeouts):
  - `agent.get_session` — verify Excel context + login state (Step 0)
  - `connect_file` — connect workbook; **only** needed for `create_dynamic_range` / `drilldown_*`, confirm with user first
  - `refresh_ribbon` — refresh stale data before pulling (`timeoutMs: 600000`); ask once per session
  - `agent.read_range` / `agent.evaluate_drget` — read a DR formula cell's value + `data.sources[]` for citation
  - `drilldown_list` — cell-level breakdown on large-variance rows after analysis (`timeoutMs: 180000`)
  - `publish_to_dashboard` — publish summary range to a Datarails dashboard (mutating, confirm first)

## Related Skills

- `/dr-extract` - Extract scenario data
- `/dr-insights` - Understand drivers of variances
- `/dr-reconcile` - Validate data consistency
- `/dr-dashboard` - Real-time performance
- `datarails-excel-multi-table-analysis` - Row-commentary pattern used in Excel context mode (per-row attribution, source refs, Sources sheet, HC decomposition)
