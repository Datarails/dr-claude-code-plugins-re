---
name: dr-intelligence
description: "Generate a 10-sheet FP&A intelligence workbook from Datarails Finance OS data with auto-detected insights, variance analysis, anomaly detection, and professional Excel formatting using openpyxl. Use when building financial analysis reports, executive dashboards, FP&A workbooks, budget-vs-actual comparisons, or expense deep-dives."
user-invocable: true
allowed-tools: "mcp__datarails-finance-os__list_finance_tables, mcp__datarails-finance-os__get_table_schema, mcp__datarails-finance-os__aggregate_table_data, mcp__datarails-finance-os__get_records_by_filter, mcp__datarails-finance-os__detect_anomalies, mcp__datarails-finance-os__profile_numeric_fields, mcp__datarails-finance-os__profile_categorical_fields, Write, Read, Bash"
argument-hint: "--year <YYYY> [--output <file>]"
---

# FP&A Intelligence Workbook

Generate a comprehensive 10-sheet FP&A intelligence workbook with auto-detected insights, recommendations, and professional Excel formatting.

This is the most powerful financial analysis skill — it answers real business questions, not just data dumps. All data is pulled via MCP tools and the workbook is built locally with openpyxl. No server-side rendering.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | -- |
| `--output <file>` | Output file path | `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx` |

## Workflow

### Step 1: Verify Connection

Check Datarails connectivity before proceeding. If any tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected. **Expected outcome**: Confirmed API access to Datarails Finance OS.

### Step 2: Load Client Profile

Read the client profile to discover the correct table IDs and field mappings:

```
Read: ${CLAUDE_PLUGIN_DATA}/client-profiles/{env}.json
   (fall back to: config/client-profiles/{env}.json)
```

If no profile exists, tell the user to run `/dr-learn` first and STOP.

**Expected outcome**: Loaded table IDs, field mappings, account hierarchy, and aggregation compatibility hints.

The profile provides:
- `tables.financials.id` and `tables.kpis.id`
- `field_mappings` (semantic name → actual API field, e.g. `account_l1` → `Cost_Center__c`)
- `account_hierarchy` (Revenue / COGS / OpEx categories)
- `aggregation.failed_fields` and `aggregation.field_alternatives` (substitute when an aggregation field is known to fail)

### Step 3: Fetch Data via MCP

Run these 6 data pulls in parallel where possible. Use `aggregate_table_data` first; fall back to `get_records_by_filter` only if aggregation is marked unsupported in the profile. **Expected outcome**: Complete dataset for all 10 workbook sheets.

1. **Monthly P&L** — `aggregate_table_data` grouped by `[account_l1, month]`, summed by `amount`, filtered to `--year`.
2. **Monthly P&L by L2** — same, grouped by `[account_l1, account_l2, month]`. Used for top-20 expense drilldown and cost center P&L.
3. **Vendor spend** — `aggregate_table_data` grouped by `[vendor]`, summed by `amount`, filtered to OpEx accounts in `--year`.
4. **Cost center spend** — `aggregate_table_data` grouped by `[cost_center, month]`.
5. **KPIs** — `aggregate_table_data` on the KPIs table grouped by `[metric_name, quarter]` for the year and one prior.
6. **Anomalies** — `detect_anomalies` on the financials table; `profile_numeric_fields` for outlier statistics if needed.

If a field listed in `aggregation.failed_fields` appears in a query, substitute via `aggregation.field_alternatives` before calling.

### Step 4: Calculate Insights

Apply these detection rules and rank results by severity. **Expected outcome**: Ranked list of findings with quantified impact and actionable recommendations.

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

Write a single Python script and execute it via `Bash`. The script reads a JSON payload of the analyzed data and writes the xlsx. **Expected outcome**: A branded 10-sheet Excel workbook saved to the output path.

## Workbook Specification

See [SHEETS.md](SHEETS.md) for the full 10-sheet specification (order, columns, charts, and formatting per sheet).

See [BRAND.md](BRAND.md) for Datarails brand colors, fonts, layout rules, and number formats to apply with openpyxl.

### Step 6: Output

After writing the file, surface it to the user:

- **Claude.ai web / ChatGPT**: present the xlsx as a downloadable artifact.
- **Claude Code**: print the absolute path and a one-line summary of what was generated.

Always include in the summary:
- Output file path
- Year analyzed
- Number of insights surfaced (by severity)
- Top recommendation

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Not authenticated" | Connect via Connectors UI ("+" → Connectors → Datarails → Connect) |
| "Profile not found" | Run `/dr-learn` first |
| openpyxl not available | Claude Code: `pip install openpyxl`. Claude.ai/ChatGPT: preinstalled |
| Aggregation fails on a field | Run `/dr-test` to refresh `aggregation.failed_fields` |
| Missing data in sheets | Run `/dr-learn` to refresh field mappings |

## Related Skills

- `/dr-extract` — Basic data extraction (P&L + KPIs only, faster).
- `/dr-insights` — Executive PowerPoint + Excel combo.
- `/dr-anomalies-report` — Focused on data quality issues.
- `/dr-reconcile` — P&L vs KPI validation.
- `/dr-learn` — Build/refresh the client profile this skill depends on.
