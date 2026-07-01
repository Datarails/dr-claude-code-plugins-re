---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (including ARR), and validation checks. Self-contained — discovers the client's tables and fields on its own, no profile or setup step required.
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
argument-hint: "[--output <file>] [--scenario <name>] [--year <YYYY>]"
---

# Datarails Financial Data Extraction

Extract validated financial data from Finance OS to Excel workbooks. Data is pulled via MCP tools and the workbook is built locally with openpyxl. No server-side rendering.

The workbook contains:
- **P&L Data**: Revenue, COGS, Operating Expenses by month
- **KPI Data**: ARR, Net New ARR, Churn, LTV, Revenue by quarter
- **Validation**: Cross-checks between P&L and KPI tables

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--output <file>` | Output filename | `tmp/Financial_Extract_YYYY.xlsx` |
| `--scenario <name>` | Primary scenario | `Actuals` |
| `--year <YYYY>` | Calendar year to extract | Current year |

## Workflow

### Step 1: Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

### Step 2: Discover the financials table, its fields, and (if present) a KPI table

**If you already discovered these earlier in THIS conversation, reuse them —
skip to Step 3.** Discovery is cheap but not free; do it once per
conversation, then carry the values forward.

1. `list_data_models`. Pick the **financials** table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest
   by row count. Note **both** its numeric `id` (call it `<financials_table_id>`)
   and its `alias` (call it `<financials_alias>`; may be empty). **Prefer the
   alias path when an alias exists** — friendlier field names, far fewer tokens.
   Also note any **KPI / metrics** table — name (or alias) matches
   `/kpi|metric|saas/i` — as `<kpis_table_id>` / `<kpis_alias>` if one exists. If
   none does, KPI sheets are built only from whatever metrics live in the
   financials table (or omitted).

2. Fields. If the table has an alias, `list_aliased_fields(<financials_alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each field's
   numeric `id` — the by-id tools address fields by id). Bind these by
   case-insensitive match on the field alias/name (respecting the noted type):
   - `<amount_field>`    — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`  — categorical: `^scenario$` → `^version$`
   - `<month_field>`     — date/period: `reporting_date` → `posting_date` → `^month$` → `^date$`
   - `<account_l1_field>` — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2` → `account_group_l2`

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<kpis_table_id>` exists, `list_aliased_fields(<kpis_alias>)` (or
   `get_fields_by_id(<kpis_table_id>)`) and bind:
   - `<metric_name_field>` — `^metric$` → `metric_name` → `kpi_name`
   - `<quarter_field>`     — `^quarter$` → `quarter` → the KPI table's date field
   - `<kpi_value_field>`   — numeric: `^value$` → `^amount$`

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue.

3. Find the account category values needed for the P&L and Balance Sheet
   sections: `get_distinct_values_by_alias(<financials_alias>, <account_l1_field>)`
   (or `get_distinct_values_by_id(<financials_table_id>, <account_l1_field_id>)`).
   If the distinct call errors, fall back to
   `get_data_by_alias(<financials_alias>, select=[<account_l1_field>], limit=500)`
   (or the by-id twin) and collect the distinct values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`
   - balance-sheet categories ← `/asset|liabilit|equity/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively, not pre-probed (see Step 3).

### Step 3: Fetch Data via MCP

Aggregation-first. Run in parallel where possible. Use the alias path
(`get_aggregated_data_by_alias`) when `<financials_alias>` exists; otherwise the
by-id twin (`get_aggregated_data_by_id`).

1. **Monthly P&L** — `get_aggregated_data_by_alias(<financials_alias>,
   dimensions=[<account_l1_field>, <account_l2_field>, <month_field>],
   metrics=[{"field": <amount_field>, "agg": "SUM"}], filters=[{"name":
   <scenario_field>, "values": [<--scenario> or "Actuals"], "is_excluded":
   false}])`. Scope to `--year` with an advanced date filter (see below) or by
   filtering the `<month_field>` dimension client-side.
2. **Balance Sheet items** — same table grouped by `[<account_l1_field>,
   <account_l2_field>, <month_field>]`, filtered client-side to the balance-sheet
   account categories found in Step 2.3.
3. **Quarterly KPIs** — only if `<kpis_table_id>` was found:
   `get_aggregated_data_by_alias(<kpis_alias>, dimensions=[<metric_name_field>,
   <quarter_field>], metrics=[{"field": <kpi_value_field>, "agg": "SUM"}], …)`
   (or the by-id twin), for `--year` and the prior year (for YoY). For named
   KPIs that aren't in a table (e.g. ARR), call `list_business_metrics` to
   discover the metric and its dimensions, then aggregate the underlying
   financials/KPI table via the same aggregation tools to compute the value.
4. **Distinct values for validation** — derive the distinct `<scenario_field>`,
   `<month_field>`, and `<account_l1_field>` values from the aggregation results,
   or call `get_distinct_values_by_alias` / `get_distinct_values_by_id` directly,
   to confirm the extract covers the expected dimensions.

**Filter rules:**
- **Date ranges filter directly** via an advanced filter — no epoch workaround
  needed. To scope to `--year`, pass `{"name": <month_field>, "values": {"type":
  "advanced", "val": [{"condition": "total_range", "value": ["<jan1_epoch>",
  "<dec31_epoch>"]}]}}` (epoch seconds as strings; by-id uses the `field_id`
  form). Adding `<month_field>` as a dimension and filtering by `--year`
  client-side still works and is optional.
- **Value-list filters** take `values: [...]` (set `is_excluded: true` for
  NOT-IN); advanced filters also support comparisons, ranges, text matching, and
  null checks.

**If an aggregation call fails on a dimension field with a 500:** that field
isn't usable as a dimension for this client. Re-inspect the Step 2 schema for
a sibling (e.g. `DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`)
and retry with it. If the alias call errors, retry the by-id twin. If no sibling
works, tell the user which field failed.

Auto-refresh tokens are handled by the MCP layer; fall back to
`get_data_by_alias` / `get_data_by_id` with paging only if aggregation fails
outright.

### Step 4: Build the Workbook Locally

Generate the xlsx with openpyxl. **Do not** call any server-side workbook tool — they have been removed.

Write a single Python script and execute it via `Bash`. The script reads a JSON payload of the extracted data and writes the xlsx.

If openpyxl is missing:
- Claude Code: `pip install openpyxl`.
- Claude.ai web / ChatGPT: openpyxl is preinstalled in the analysis/code interpreter sandbox.

## Sheets to Generate

1. **Summary**
   - Year, scenario, generation timestamp.
   - Totals: Revenue, COGS, Gross Profit, Gross Margin %, Operating Expenses, Operating Income, Net Income.
   - Balance Sheet snapshot: Total Assets, Total Liabilities, Total Equity (period-end).
   - KPI snapshot: ARR, Net New ARR, Churn %, LTV, CAC, LTV/CAC.
   - Row-by-row validation checks (see sheet 4) summarized as PASS / FAIL count.

2. **P&L**
   - Rows: account categories discovered in Step 2.3, indented by L1/L2.
   - Columns: 12 months + Total + Prior Year + YoY Δ%.
   - Subtotals (Revenue, COGS, Gross Profit, Total OpEx, Operating Income) bolded.
   - Number format: `$#,##0` for dollars, `0.0%` for percentages.

3. **KPIs**
   - One row per metric. Columns: Q1 / Q2 / Q3 / Q4 / FY / Prior FY / YoY Δ%.
   - Include ARR, Net New ARR, Gross Churn %, Net Churn %, LTV, CAC, LTV/CAC, NRR, GRR.

4. **Validation**
   - One row per cross-check:
     - "P&L Revenue total equals KPI Revenue total" → PASS/FAIL with both values.
     - "Sum of monthly Revenue equals annual Revenue" → PASS/FAIL.
     - "All 12 months present in extract" → PASS/FAIL.
     - "Scenario coverage" — list distinct scenarios and confirm `--scenario` is among them.
     - "Discovered field coverage" — list the fields bound in Step 2 and confirm each returned data.
   - Footer: generation timestamp.

## Datarails Brand Styling

Apply the same brand styling block as `/dr-insights` and `/dr-intelligence`:

**Font:** Poppins (fall back to Calibri). Weights: 400 / 600 / 700.

**Colors:**
| Role | Hex |
|------|-----|
| Navy (header bg) | `0C142B` |
| Main text | `333333` |
| Secondary text | `6D6E6F` |
| Border | `9EA1AA` |
| Section bg (lavender) | `F2F2FB` |
| Input bg | `EAEAFF` |
| Input text (indigo) | `4646CE` |
| Favorable | `2ECC71` |
| Unfavorable | `E74C3C` |
| Validation PASS | `2ECC71` |
| Validation FAIL | `E74C3C` |

**Layout:**
- Content starts at column B (column A narrow gutter).
- Rows 1-6 header banner: navy background, white title, white subtitle (year + scenario).
- Gridlines OFF. Freeze panes at B7.
- Footer row: generation date + "Datarails Financial Extract".
- Every cell needs font, fill, alignment, number format.

**Number formats:** `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)` (default), `$#,##0` (dollars), `0.0%` (percent).

**Variance coloring:** YoY Δ% cells use green (`2ECC71`) for favorable, red (`E74C3C`) for unfavorable. For expenses, lower is favorable; for revenue/margin, higher is favorable.

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

## Step 5: Output

- **Claude.ai web / ChatGPT**: present the xlsx as a downloadable artifact.
- **Claude Code**: print the absolute path.

Always include in the summary:
- Output file path
- Year and scenario extracted
- Validation result count (e.g. "5/5 PASS")
- Any warnings (missing months, scenario gaps)

## Troubleshooting

**No table matches the financials pattern (Step 2)**
- List the tables you found and ask the user which one holds their P&L /
  financial data, then continue.

**Aggregation rejected on a dimension field (500)**
- Swap to a sibling field from the Step 2 schema and retry (see Step 3). If
  no sibling works, tell the user which field failed.

**Token expires during extraction**
- The MCP layer auto-refreshes. If 401 errors persist, reconnect via Connectors UI.

**Missing months in data**
- Check the `<month_field>` type. If the API stores year as a string, ensure the client-side `--year` comparison is against `"2025"` not `2025`.

**openpyxl not available**
- Claude Code: `pip install openpyxl`.
- Claude.ai / ChatGPT: should be preinstalled in code-execution sandbox.

## Related Skills

- `/dr-tables` — Explore available tables.
- `/dr-query` — Investigate specific records.
- `/dr-intelligence` — Full 10-sheet insights workbook (this skill is the simpler 4-sheet variant).
- `/dr-insights` — Executive PowerPoint + Excel combo.
