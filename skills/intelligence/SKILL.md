---
name: dr-intelligence
description: Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting. The most powerful financial analysis skill. Self-contained — discovers the client's tables and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__detect_anomalies
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--output <file>]"
---

# FP&A Intelligence Workbook

Generate a comprehensive 10-sheet FP&A intelligence workbook with auto-detected insights, recommendations, and professional Excel formatting.

This is the **most powerful** financial analysis skill — it answers real business questions, not just data dumps. All data is pulled via MCP tools and the workbook is built locally with openpyxl. No server-side rendering.

## What Makes This Different

| Traditional Report | Intelligence Workbook |
|-------------------|----------------------|
| Shows data | Answers questions |
| Lists numbers | Explains "why" |
| Static tables | Highlights anomalies |
| Manual analysis | Insights auto-surfaced |
| Data dump | Recommendations included |

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | -- |
| `--output <file>` | Output file path | `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx` |

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
   exists. If you found a KPI/metrics table, the SaaS Metrics sheet pulls from
   it; otherwise build it from whatever metrics live in the financials table.

2. `get_table_schema(<financials_table_id>)`. Bind these by case-insensitive
   name match (respecting the noted type) — bind only those the sheets use:
   - `<amount_field>`     — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`   — categorical: `^scenario$` → `^version$`
   - `<month_field>`      — date/period: `reporting_date` → `posting_date` → `^month$` → `^date$`
   - `<account_l1_field>` — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2` → `account_group_l2`
   - `<vendor_field>`     — `^vendor$` → `vendor_name` → `supplier` (Vendor Analysis sheet)
   - `<cost_center_field>` — `cost_center` → `department` → `dr_cost_center` (Cost Center P&L sheet)

   If `<kpis_table_id>` exists, `get_table_schema(<kpis_table_id>)` and bind:
   - `<metric_name_field>` — `^metric$` → `metric_name` → `kpi_name`
   - `<quarter_field>`     — `^quarter$` → `quarter` → the KPI table's date field
   - `<kpi_value_field>`   — numeric: `^value$` → `^amount$`

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use. A missing `<vendor_field>` or `<cost_center_field>`
   just omits that sheet — don't block on it.

3. Find the account category values the insight rules and filters need. The
   distinct-values API often returns 409, so call
   `get_sample_records(<financials_table_id>, limit=500)` and collect the
   distinct `<account_l1_field>` values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once.

Aggregation-field failures are handled reactively, not pre-probed (see Step 3).

### Step 3: Fetch Data via MCP

Run these data pulls in parallel where possible. Use `aggregate_table_data` first; fall back to `get_records_by_filter` only if aggregation fails outright.

1. **Monthly P&L** — `aggregate_table_data` on `<financials_table_id>` grouped by `[<account_l1_field>, <month_field>]`, summed by `<amount_field>`. `--year` is applied client-side after pulling the `<month_field>` dimension.
2. **Monthly P&L by L2** — same, grouped by `[<account_l1_field>, <account_l2_field>, <month_field>]`. Used for top-20 expense drilldown and cost center P&L.
3. **Vendor spend** — only if `<vendor_field>` was found: `aggregate_table_data` grouped by `[<vendor_field>]`, summed by `<amount_field>`, filtered to the `<opex_value>` accounts (from Step 2.3) for `--year`.
4. **Cost center spend** — only if `<cost_center_field>` was found: `aggregate_table_data` grouped by `[<cost_center_field>, <month_field>]`.
5. **KPIs** — only if `<kpis_table_id>` was found: `aggregate_table_data` on it grouped by `[<metric_name_field>, <quarter_field>]`, summed by `<kpi_value_field>`, for the year and one prior.
6. **Anomalies** — `detect_anomalies` and `profile_numeric_fields` for
   baseline MIN/MAX/AVG/COUNT per numeric field. These tools do NOT
   return outliers, std dev, or percentiles — they return baseline
   aggregates. Compute outlier flags client-side using the σ-rule
   below applied to the monthly P&L time series pulled in step 1.

**Date fields must be dimensions, never filters** (stored as epoch ints — date
filters silently return empty). **Only text fields in filters.**

**If an aggregation call fails on a dimension field with a 500:** that field
isn't usable as a dimension for this client. Re-inspect the Step 2 schema for
a sibling (e.g. `DR_ACC_L1.5` when `DR_ACC_L1` fails, or `account_group_l1`)
and retry with it. If no sibling works, tell the user which field failed.

### Step 4: Calculate Insights

Apply these detection rules and rank results by severity:

| Insight | Detection Rule | Severity |
|---------|----------------|----------|
| OpEx exceeds Revenue | `OpEx / Revenue > 1.0` | CRITICAL |
| Negative gross margin | `Gross Profit < 0` | CRITICAL |
| Unusual variance | Monthly value > 3σ from trailing-12 mean | CRITICAL |
| High expense growth | MoM change > 20% on a material account | WARNING |
| Vendor concentration | Single vendor > 10% of total OpEx | WARNING |
| Cost center over budget | Department actual > budget by > 10% | WARNING |
| Gross margin compression | GM% down > 5pp YoY | WARNING |
| Strong revenue growth | Revenue MoM > 10% | POSITIVE |
| Vendor diversification | Top vendor < 5% of OpEx | POSITIVE |

**Materiality thresholds**: only surface a finding if the affected line is ≥ 5% of the relevant total. Variance alerts trigger at 10% MoM change. Concentration risk triggers at 10% single-vendor share.

For each insight, generate:
- A one-sentence finding
- Quantified impact ($ amount and % of relevant total)
- A specific recommendation (what to investigate / what action to take)

### Step 5: Build the Workbook Locally

Generate the xlsx with openpyxl. **Do not** call any server-side workbook generation tool — they have been removed.

If openpyxl is not available in the local environment:
- In Claude Code: `pip install openpyxl` (one time).
- In Claude.ai web / ChatGPT: openpyxl is preinstalled in the analysis/code interpreter sandbox.

Write a single Python script and execute it via `Bash`. The script reads a JSON payload of the analyzed data and writes the xlsx.

## 10 Sheets to Generate

Order matters — the dashboard is sheet 1, raw data is sheet 10.

1. **Insights Dashboard** — Top 5 findings with severity color, current period KPIs (Revenue, Gross Margin, OpEx, Burn, Runway), and the ranked recommendations list.
2. **Expense Deep Dive** — Top 20 expense accounts: amount, % of total OpEx, MoM Δ%, YoY Δ%. Color the % cells with a green→red color scale.
3. **Variance Waterfall** — Current period vs. prior period: contribution to total variance line by line. Use a bar chart.
4. **Trend Analysis** — 12-month rolling P&L: Revenue, COGS, Gross Profit, OpEx, Net Income. One line per metric, secondary axis for margin %.
5. **Anomaly Report** — Outlier rows identified by applying the σ-based
   rule (line 90) to the monthly P&L series. Use `detect_anomalies` /
   `profile_numeric_fields` for the field-level baselines that feed the
   computation. Severity column, drill-down hint per row.
6. **Vendor Analysis** — Top 20 vendors: spend, % of OpEx, MoM Δ. Concentration risk flag column. Pie chart for top-10.
7. **SaaS Metrics** — ARR, Net New ARR, NRR, GRR, CAC, LTV, LTV/CAC, Magic Number, Burn Multiple, CAC Payback. Quarterly columns; YoY column at right.
8. **Sales Performance** — Rep-level: bookings, win rate, ACV, ramp status. Cohort table by hire quarter.
9. **Cost Center P&L** — Department × month grid with totals row and YoY column. Conditional formatting on Δ%.
10. **Raw Data** — Long-form pivot-ready dataset (the monthly L1×L2 frame). No formatting — just headers + data.

Each sheet must include a generation timestamp footer and the year analyzed.

## Datarails Brand Styling

When generating the Excel, apply Datarails brand styling:

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
| Severity CRITICAL | `C00000` | Critical insight banner |
| Severity WARNING | `ED7D31` | Warning insight banner |
| Severity POSITIVE | `70AD47` | Positive insight banner |
| Severity INFO | `5B9BD5` | Informational insight banner |
| Chart 1 | `0C142B` | Actuals (navy) |
| Chart 2 | `F93576` | Budget (hot pink) |
| Chart 3 | `00B4D8` | Teal |
| Chart 4 | `FFA30F` | Amber |

**Layout rules:**
- Content starts at column B (column A is a narrow gutter).
- Rows 1-6: header banner with navy background, white title text, white subtitle.
- Gridlines OFF on every sheet. Freeze panes at B7.
- Footer as last row with generation date and "Datarails FP&A Intelligence Workbook".
- Every cell must have font, fill, alignment, and number format set.

**Number formats:** `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)` (default), `$#,##0` (dollars), `$#,##0.0,,"M"` (millions), `0.0%` (percent).

**Variance coloring:** any cell showing a delta/change uses green (`2ECC71`) if favorable, red (`E74C3C`) if unfavorable.

## Step 6: Output

After writing the file, surface it to the user:

- **Claude.ai web / ChatGPT**: present the xlsx as a downloadable artifact.
- **Claude Code**: print the absolute path and a one-line summary of what was generated.

Always include in the summary:
- Output file path
- Year analyzed
- Number of insights surfaced (by severity)
- Top recommendation

## Why This Matters

This workbook answers the **Top 10 Business Questions**:

1. **Where is the money going?** — Top 20 expense drivers
2. **What changed vs last month?** — MoM variance waterfall
3. **Which cost centers are over budget?** — Variance by department
4. **Are we efficient?** — OpEx as % of Revenue, Gross Margin
5. **What's unusual?** — Auto-detected anomalies
6. **Who are our biggest vendors?** — Top 10 vendor spend
7. **How are sales reps performing?** — Win rates, ARR by rep
8. **What's our burn situation?** — Runway, burn multiple
9. **What should we investigate?** — Exception report
10. **What actions to take?** — Automated recommendations

## Performance

- Small datasets (1-2 years): ~1-2 minutes
- Large datasets (3+ years): ~3-5 minutes

Aggregation-first strategy keeps round-trips small. Pagination is the fallback only when aggregation fails outright.

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" → Connectors → Datarails → Connect).

**No table matches the financials pattern (Step 2)**
- List the tables you found and ask the user which one holds their P&L /
  financial data, then continue.

**openpyxl not available locally**
- Claude Code: `pip install openpyxl`.
- Claude.ai / ChatGPT analysis tools have it preinstalled — if it's missing, the sandbox is unavailable; tell the user the skill needs a code-execution-capable client.

**Aggregation fails on a field**
- Swap to a sibling field from the Step 2 schema and retry (see Step 3). If
  no sibling works, tell the user which field failed.

**Missing data in sheets**
- Re-check the fields bound in Step 2; a sheet whose source field
  (`<vendor_field>`, `<cost_center_field>`, KPI table) wasn't found is
  omitted by design.

## Related Skills

- `/dr-extract` — Basic data extraction (P&L + KPIs only, faster).
- `/dr-insights` — Executive PowerPoint + Excel combo.
- `/dr-anomalies-report` — Focused on data quality issues.
- `/dr-reconcile` — P&L vs KPI validation.
