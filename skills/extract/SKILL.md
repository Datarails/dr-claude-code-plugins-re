---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (including ARR), and validation checks. Self-contained — discovers the client's tables and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
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

1. `list_finance_tables`. Pick the **financials** table: the one whose name
   matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest by
   row count. Call it `<financials_table_id>`. Also note any **KPI / metrics**
   table — name matches `/kpi|metric|saas/i` — as `<kpis_table_id>` if one
   exists. If none does, KPI sheets are built only from whatever metrics live
   in the financials table (or omitted).

2. `get_table_schema(<financials_table_id>)`. Bind these by case-insensitive
   name match (respecting the noted type):
   - `<amount_field>`    — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`  — categorical: `^scenario$` → `^version$`
   - `<month_field>`     — date/period: `reporting_date` → `posting_date` → `^month$` → `^date$`
   - `<account_l1_field>` — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2` → `account_group_l2`

   If `<kpis_table_id>` exists, `get_table_schema(<kpis_table_id>)` and bind:
   - `<metric_name_field>` — `^metric$` → `metric_name` → `kpi_name`
   - `<quarter_field>`     — `^quarter$` → `quarter` → the KPI table's date field
   - `<kpi_value_field>`   — numeric: `^value$` → `^amount$`

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue.

3. Find the account category values needed for the P&L and Balance Sheet
   sections. The distinct-values API often returns 409, so call
   `get_sample_records(<financials_table_id>, limit=500)` and collect the
   distinct `<account_l1_field>` values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`
   - balance-sheet categories ← `/asset|liabilit|equity/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively, not pre-probed (see Step 3).

### Step 3: Fetch Data via MCP

Aggregation-first. Run in parallel where possible.

1. **Monthly P&L** — `aggregate_table_data` on `<financials_table_id>` grouped by `[<account_l1_field>, <account_l2_field>, <month_field>]`, summed by `<amount_field>`, filtered to `--scenario` (default `Actuals`). `--year` is applied client-side after pulling the `<month_field>` dimension (date fields must be dimensions, never filters — see below).
2. **Balance Sheet items** — same table grouped by `[<account_l1_field>, <account_l2_field>, <month_field>]`, filtered client-side to the balance-sheet account categories found in Step 2.3.
3. **Quarterly KPIs** — only if `<kpis_table_id>` was found: `aggregate_table_data` on it grouped by `[<metric_name_field>, <quarter_field>]`, summed by `<kpi_value_field>`, for `--year` and the prior year (for YoY).
4. **Distinct values for validation** — the distinct-values API often 409s; derive the distinct `<scenario_field>`, `<month_field>`, and `<account_l1_field>` values from the aggregation results / the Step 2.3 sample to confirm the extract covers the expected dimensions.

**Filter rules:**
- **Date fields must be dimensions, never filters.** Stored as epoch ints — date filters silently return empty. Include `<month_field>` in `dimensions` and filter by `--year` client-side.
- **Only text fields in filters.**

**If an aggregation call fails on a dimension field with a 500:** that field
isn't usable as a dimension for this client. Re-inspect the Step 2 schema for
a sibling (e.g. `DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`)
and retry with it. If no sibling works, tell the user which field failed.

Auto-refresh tokens are handled by the MCP layer; fall back to
`get_records_by_filter` with paging only if aggregation fails outright.

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
