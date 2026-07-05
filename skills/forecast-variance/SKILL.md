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

Analyze variances between your actual, plan, and forecast data. Scenario names are **discovered from your data, never assumed** — many orgs have no `Budget` scenario at all (plan data often lives in a separate planning-version field), so the plan side of the comparison is resolved at runtime (Step 1b).

Essential for FP&A reviews, planning adjustments, and performance tracking.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to analyze | — |
| `--scenarios <list>` | Comma-separated scenario names, resolved against the discovered scenario domain (Step 1b) | Resolved at runtime — actual side + plan side + forecast, whichever exist |
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
response (see the Excel Context Contract in CLAUDE.md, §Transport). Do **not** call the
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

If multiple candidates exist for either dimension, pick the most specific / granular one. If no candidate is identifiable by name (e.g., non-English field names), list the discovered fields and ask the user which to use. Document both discovered field names — use them in **every aggregation** for this analysis session. These two dimensions are mandatory; omitting either produces commentary that is not actionable.

If the schema genuinely has no identifiable cost center field, flag this in the Read Me block and fall back to the next-best grouping available (e.g., account hierarchy). Never silently drop the dimension.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`get_distinct_values_by_alias`/`_by_id`) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

### Step 1b — Resolve the scenario domain and the plan side (never assume `Budget` exists)

Scenario names vary by org, and a `Budget` scenario frequently does not exist — filtering on it returns an empty result and a silently wrong analysis. Resolve every side of the comparison against **discovered** values before any pull:

1. **Discover the scenario domain.** Pull distinct values of the discovered scenario field — `get_distinct_values_by_alias(alias=<financials_alias>, field=<scenario_field>)` if the field is aliased, else `get_distinct_values_by_id(table_id=<id>, field_id=<scenario_field_id>)`.
2. **Resolve the actual side** — the discovered value matching `/actual/i`.
3. **Resolve the plan side:**
   - **A budget-like scenario exists** (a discovered value matches `/budget|plan|aop|target/i`) → use it as the plan-side scenario filter.
   - **No budget-like scenario** → look for a **planning-version-like field** in the Step 1 schema (alias/name matching `/plan|version|cycle|budget/i`). If one exists, pull **its** distinct values the same way, present the versions, and ask the user which plan version to compare against (default to the most recent only if the user already indicated it). Use `{<planning_version_field>: <chosen version>}` as the plan-side filter in Step 3 instead of a scenario value — and check which scenario values the rows under that version carry before also filtering on scenario.
   - **Neither exists** → tell the user what you found, then offer what IS possible:
     > I found actuals data but couldn't locate any budget or plan data in your financials table — there's no budget-like scenario and no planning-version field.
     >
     > The available scenarios are: [list the discovered values]
     >
     > Options:
     > - Would you like me to compare Actuals against Forecast instead?
     > - Or should I just show you the Actuals breakdown?
4. **Resolve the forecast side** (if in scope) — the discovered value matching `/forecast/i`; if absent, drop it from the comparison and say so.
5. **If `--scenarios` was passed**, map each requested name onto the discovered domain (case-insensitive). Any name with no match goes through the plan-side fallback above — never filter on a scenario value you did not see in the distinct-values response.

**If the plan side is incomplete** (it exists but doesn't cover all the categories or periods that Actuals covers), say so and offer:
- Compare only the overlapping categories/periods
- Show where plan data is missing

Record the resolved sides — actual, plan (scenario value or plan-version filter), forecast — and use them verbatim in every Step 3 pull and in every output label.

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
    {"name": <scenario_field>,      "values": [<side resolved in Step 1b>],                "is_excluded": false},
    {"name": <account_level_field>, "values": [<P&L flow buckets from data-scope item 2>], "is_excluded": false},
    {"name": <gaap_field>,          "values": [<discovered GAAP-adjustment values>],       "is_excluded": true}
  ]
)
```

All filter values are placeholders — every one comes from Step 1b / the data-scope discovery, never from this template. **Plan side:** when Step 1b resolved a plan-version fallback, replace the scenario filter with `{"name": <planning_version_field>, "values": [<chosen version>], "is_excluded": false}`. **Account scope:** use the account-hierarchy level whose discovered values partition P&L flows (data-scope item 2) — on many orgs the top level is the balance-sheet equation and P&L buckets live one level deeper. **GAAP exclusion:** only if a GAAP-adjustment-like field exists — discover its values first, otherwise omit the filter.

Scope by year either by adding `<date_field>` to `dimensions` and filtering the result client-side, or with an **advanced** date-range filter: `{"name": <date_field>, "values": {"type": "advanced", "val": [{"condition": "total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}` (epoch seconds as strings). Both work — date filtering is no longer rejected.

By-id fallback (no alias): `get_aggregated_data_by_id(table_id=<id>, dimensions=[<period_field_id>, <cost_center_field_id>, <report_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}], filters=[{"field_id": <scenario_field_id>, "values": [...]}])`. If an alias call 500s on a dimension, re-inspect the Step 1 schema for a sibling and retry, or fall back to the by-id twin.

Assign each distinct pull a Source ID: `S1`, `S2`, `S3`, ...

| Source ID | Side |
|-----------|------|
| S1 | Actual side (resolved actuals-like scenario) |
| S2 | Plan side (budget-like scenario, or plan-version filter from Step 1b) |
| S3 | Forecast side (if in scope) |

**An empty result from a scenario filter is a resolution failure, not a zero plan** — go back to Step 1b rather than presenting $0 as the plan side.

**Also pull HeadCount** whenever compensation lines are in scope and the org has a headcount-like table (discover it via `list_data_models`; if none exists, skip the decomposition and say so). Comp $ alone cannot distinguish volume (headcount change) from rate (salary / bonus change) — always decompose. See the HC inference trap in `datarails-excel-multi-table-analysis`.

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

**Example commentary cells** (illustrative — `<report_field>` and the plan-side label come from Step 1 / Step 1b):
> `Marketing expense +$120K (+14%) vs Plan, driven by Events cost center (+$95K, <report_field>: T&E); remaining $25K in Digital/Software. [S1, S2]`

> `R&D compensation +$280K (+18%) vs Plan: $230K (82%) is rate-driven (Q4 bonus accrual on flat HC of 23), $50K (18%) is volume (2 new hires in Oct). [S1, S2, S3]`

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
  Period:    <explicit window, e.g., 2025-01 through 2025-09>
  Scenarios: <resolved sides from Step 1b, e.g., Actuals vs "FY25 Plan v2" (plan version) vs Forecast>
  Accounts:  <account_level_field> = <discovered P&L flow buckets>; <gaap_field> excluded (if present)
  Cost Center field:  <discovered field name>
  Report Field:       <discovered field name>

SOURCE TABLES (full detail in Sources sheet)
  S1 — Financials: actual side by period × cost center × report field
  S2 — Financials: plan side (budget-like scenario or plan version) by period × cost center × report field
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
- **Never filter on a scenario value you didn't discover** — `Budget` frequently doesn't exist; resolve every side in Step 1b first
- **Never write commentary without a `[S#]` ref** — every claim must be auditable
- **Never overwrite the user's existing data** — add columns to the right only
- **Never imply freshness you don't have** — flag any missing periods explicitly

---

## Variance Analysis

**Variance math rules (all modes):**
- Compute every side over the **same explicit period window** (data-scope item 3 — default the latest complete fiscal year or trailing 12 closed months, never an unscoped all-time total), pulled with identical dimensions and account scoping so rows line up.
- **Label every table, chart, and commentary output with the period + the resolved sides it covers** (e.g., "2025-01…2025-09, Actuals vs FY25 Plan v2").
- Apply data-scope item 4 to every aggregation response: exclude the trailing keyless grand-total row from sums, shares, and variance denominators (use it only as a checksum); read null counts only from the explicit `[null]` bucket; when COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself.
- Variance $ = actual − plan; variance % = variance $ / |plan|. When the plan side is zero or missing for a row, report the $ variance and mark the % as n/m — never divide by zero or fabricate a value.

### Budget Variance
- Actual vs plan-side amounts (budget-like scenario or plan version, resolved in Step 1b)
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

> Scenario names passed via `--scenarios` are resolved against the discovered scenario domain (Step 1b). If a requested name (e.g. `Budget`) doesn't exist on the org, the plan side falls back to a planning-version field — or you'll be shown the scenarios that do exist and offered Actuals vs Forecast.

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
- Actual > Plan (Revenue) ✅
- Actual < Plan (Expense) ✅

### Unfavorable Variance
- Actual < Plan (Revenue) ❌
- Actual > Plan (Expense) ❌

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

**"Scenario not found"** - The requested name isn't in the discovered scenario domain. Re-run Step 1b: show the scenarios that DO exist, offer them, and try the planning-version fallback for the plan side.

**"No variance data"** - A side returned empty. If the plan-side pull filtered on a scenario value that was never discovered (e.g. `Budget`), that's the bug — go back to Step 1b; plan data often lives in a planning-version field, not a scenario.

**"Large variance"** - Review detailed Excel report for root causes

## Integration

Works with:
- `/dr-extract` - Source of scenario data
- `/dr-insights` - Contextual trend analysis
- `/dr-reconcile` - Validate scenario consistency
- `/dr-dashboard` - Current performance view
- **Excel Add-In bridge** - In Excel context (see the Excel Context Contract in CLAUDE.md for exact params/timeouts):
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
