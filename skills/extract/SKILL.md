---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (including ARR), and validation checks.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_field_distinct_values
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

### Step 2: Load Client Profile

```
Read: ${CLAUDE_PLUGIN_DATA}/client-profiles/{env}.json
   (fall back to: config/client-profiles/{env}.json)
```

If no profile exists, tell the user to run `/dr-learn` first and STOP.

The profile provides:
- `tables.financials.id` and `tables.kpis.id`
- `field_mappings` (semantic → actual API field)
- `account_hierarchy` (Revenue / COGS / OpEx / Balance Sheet categories)
- `aggregation.failed_fields` and `aggregation.field_alternatives`

### Step 3: Fetch Data via MCP

Aggregation-first. Run in parallel where possible.

1. **Monthly P&L** — `aggregate_table_data` on the financials table grouped by `[account_l1, account_l2, month]`, summed by `amount`, filtered to `--year` and `--scenario` (default `Actuals`).
2. **Balance Sheet items** — same table grouped by `[account_l1, account_l2, month]`, filtered to balance-sheet account categories from the profile.
3. **Quarterly KPIs** — `aggregate_table_data` on the KPIs table grouped by `[metric_name, quarter]` for `--year` and the prior year (for YoY).
4. **Distinct values for validation** — `get_field_distinct_values` on `scenario`, `month`, `account_l1` to confirm the extract covers the expected dimensions.

If a field is in `aggregation.failed_fields`, substitute via `aggregation.field_alternatives` before calling.

If aggregation is marked unsupported in the profile, fall back to `get_records_by_filter` with paging. Auto-refresh tokens are handled by the MCP layer.

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
   - Rows: account categories from the profile's `account_hierarchy`, indented by L1/L2.
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
     - "Profile field mapping coverage" — list mapped semantic fields used and confirm each returned data.
   - Footer: profile path + last-modified timestamp.

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

**"Profile not found"**
- Run `/dr-learn` first to create a profile.

**Token expires during extraction**
- The MCP layer auto-refreshes. If 401 errors persist, reconnect via Connectors UI.

**Missing months in data**
- Check the `month` field type. If the API stores year as a string, ensure the filter is `"2025"` not `2025`.

**openpyxl not available**
- Claude Code: `pip install openpyxl`.
- Claude.ai / ChatGPT: should be preinstalled in code-execution sandbox.

## Related Skills

- `/dr-learn` — Create/update client profile.
- `/dr-tables` — Explore available tables.
- `/dr-query` — Investigate specific records.
- `/dr-intelligence` — Full 10-sheet insights workbook (this skill is the simpler 4-sheet variant).
- `/dr-insights` — Executive PowerPoint + Excel combo.
