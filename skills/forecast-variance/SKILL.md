---
name: dr-forecast-variance
description: Analyze budget vs forecast vs actual variances. Compares multi-scenario financial data for planning and performance review.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__list_finance_tables
  - Write
  - Read
  - Bash
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

### Step 0 — Verify workbook connection (always first in Excel context)

Before any data pull or schema discovery, call `datarails-excel-agent` → `agent.get_session`.

- If `isConnected` (COM) or `isLoggedIn` (Flex) is **false**: the workbook is not connected to Datarails. Ask the user: *"This workbook is not connected to Datarails. Should I connect it now with `connect_file`?"* Wait for explicit confirmation before calling `agent.connect_file` — it is a mutating command and must not be called automatically. Do not proceed with analysis until connected — FinanceOS API results will not be meaningful for this workbook.
- If connected: note the workspace context for the session. Proceed to Step 1.

**Data refresh — ask only in Excel context:** If `agent.get_session` succeeded above (Excel context confirmed), ask: *"Should I refresh data from Datarails before pulling? (Recommended if you haven't refreshed today.)"* If the user confirms, call `agent.refresh` and wait for it to complete. Skip only if the user explicitly says no. In non-Excel context (no agent bridge), skip entirely — `agent.refresh` is not available.

### Step 1 — Discover client-specific dimensions (always first)

Every Datarails customer structures their Financials table differently. **Never hardcode dimension field names.** Before pulling any data, discover the two key dimensions from the Financials table schema:

**Run `get_table_schema` on the Financials table, then identify:**

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

Issue all scenario pulls in a single turn (concurrent tool calls). For each pull, always include the discovered **cost center** and **report field** dimensions alongside the period dimension:

```
dimensions: [System_Quarter (or System_Month), <cost_center_field>, <report_field>]
metrics:    [SUM(Amount)]
filters:    [System_Year = <year>, Scenario = <scenario>, DR_ACC_L0 = "P&L",
             GAAP/Non GAAP ≠ "Gaap"]
```

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
2. You are in **enrichment mode** — the user's sheet had existing DR.GET formula cells that you added commentary alongside.

If either condition is false, skip this step entirely and state why:
- Non-Excel context → `agent.drill_down` not available.
- **Cold-question mode** → data cells were written as **raw values** from the FinanceOS API (`aggregate_table_data`), not as DR.GET formulas. `agent.drill_down` targets DR.GET formula cells — it has nothing to act on. Tell the user drill-down is unavailable in this mode.

If both conditions are true: after writing commentary, you **MUST** output a **Drill-Down Menu** block directly in chat. Do not end the response without it.

The block must list every row where |variance| > 10% or flagged unfavorable, one row per line with its Δ$ and Δ%:

```
📋 Drill-Down Menu — rows with |variance| > 10%
  1. <Row label>  Δ$X.XM  (ΔY%)
  2. <Row label>  Δ$X.XM  (ΔY%)
  ...
```

Then explicitly ask: *"Which rows would you like me to drill into for a cell-level breakdown? I'll call `agent.drill_down` on each selected row."*

Only invoke `agent.drill_down` after the user selects rows — do not drill automatically.

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
- `datarails-excel-agent` - In Excel context:
  - `agent.get_session` — verify workbook is connected before analysis (Step 0)
  - `agent.connect_file` — connect workbook if not yet connected
  - `agent.refresh` — refresh stale data before pulling from FinanceOS API
  - `agent.drill_down` — cell-level breakdown on large-variance rows after analysis
  - `agent.publish_to_dashboard` — publish summary range to a Datarails dashboard

## Related Skills

- `/dr-extract` - Extract scenario data
- `/dr-insights` - Understand drivers of variances
- `/dr-reconcile` - Validate data consistency
- `/dr-dashboard` - Real-time performance
- `datarails-excel-multi-table-analysis` - Row-commentary pattern used in Excel context mode (per-row attribution, source refs, Sources sheet, HC decomposition)
