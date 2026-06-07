---
name: dr-intelligence
description: Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting. The most powerful financial analysis skill.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
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

### Step 2: Load Client Profile

Read the client profile to discover the correct table IDs and field mappings:

```
Read: ${CLAUDE_PLUGIN_DATA}/client-profiles/{env}.json
   (fall back to: config/client-profiles/{env}.json)
```

If no profile exists, tell the user to run `/dr-learn` first and STOP.

The profile provides:
- `tables.financials.id` and `tables.kpis.id`
- `field_mappings` (semantic name → actual API field, e.g. `account_l1` → `Cost_Center__c`)
- `account_hierarchy` (Revenue / COGS / OpEx categories)
- `aggregation.failed_fields` and `aggregation.field_alternatives` (substitute when an aggregation field is known to fail)

### Step 3: Fetch Data via MCP

Run these data pulls in parallel where possible. Use `aggregate_table_data` first; fall back to `get_records_by_filter` only if aggregation is marked unsupported in the profile.

1. **Monthly P&L** — `aggregate_table_data` grouped by `[account_l1, month]`, summed by `amount`, filtered to `--year`.
2. **Monthly P&L by L2** — same, grouped by `[account_l1, account_l2, month]`. Used for top-20 expense drilldown and cost center P&L.
3. **Vendor spend** — `aggregate_table_data` grouped by `[vendor]`, summed by `amount`, filtered to OpEx accounts in `--year`.
4. **Cost center spend** — `aggregate_table_data` grouped by `[cost_center, month]`.
5. **KPIs** — `aggregate_table_data` on the KPIs table grouped by `[metric_name, quarter]` for the year and one prior.
6. **Anomalies** — `detect_anomalies` on the financials table; `profile_numeric_fields` for outlier statistics if needed.

If a field listed in `aggregation.failed_fields` appears in a query, substitute via `aggregation.field_alternatives` before calling.

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
5. **Anomaly Report** — Auto-detected outliers from `detect_anomalies` + the σ-based rule above. Severity column, drill-down hint per row.
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

Aggregation-first strategy keeps round-trips small. Pagination is the fallback only when the profile marks aggregation unsupported.

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" → Connectors → Datarails → Connect).

**"Profile not found"**
- Run `/dr-learn` first to create a profile for the environment.

**openpyxl not available locally**
- Claude Code: `pip install openpyxl`.
- Claude.ai / ChatGPT analysis tools have it preinstalled — if it's missing, the sandbox is unavailable; tell the user the skill needs a code-execution-capable client.

**Aggregation fails on a field**
- The profile's `aggregation.failed_fields` should already redirect to alternatives. If a new field fails, run `/dr-test` to refresh.

**Missing data in sheets**
- Check profile's field mappings. Run `/dr-learn` to refresh.

## Related Skills

- `/dr-extract` — Basic data extraction (P&L + KPIs only, faster).
- `/dr-insights` — Executive PowerPoint + Excel combo.
- `/dr-anomalies-report` — Focused on data quality issues.
- `/dr-reconcile` — P&L vs KPI validation.
- `/dr-learn` — Build/refresh the client profile this skill depends on.
