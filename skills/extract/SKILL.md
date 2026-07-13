---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (ARR and other SaaS metrics only when sourceable from the org's data), and validation checks. Self-contained — discovers the client's tables and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__start_aggregation_by_alias
  - mcp__datarails-finance-os__get_aggregation_result_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__start_aggregation_by_id
  - mcp__datarails-finance-os__get_aggregation_result_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__start_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_result_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__start_distinct_values_by_id
  - mcp__datarails-finance-os__get_distinct_values_result_by_id
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
- **KPI Data**: quarterly KPIs the org's data can actually source — revenue by quarter always; SaaS metrics (ARR, Net New ARR, Churn, LTV) only when a KPI source exists (see the KPI-honesty rule under Sheets to Generate)
- **Validation**: Cross-checks between P&L and KPI tables

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--output <file>` | Output filename | `tmp/Financial_Extract_YYYY.xlsx` |
| `--scenario <name>` | Primary scenario | The discovered actuals-like scenario (a passed name is validated against the discovered scenario domain) |
| `--year <YYYY>` | Calendar year to extract | Latest complete fiscal year in the data (per the data-scope discovery in Step 2) |

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
   sections: `start_distinct_values_by_alias(<financials_alias>, <account_l1_field>)`
   (or `start_distinct_values_by_id(<financials_table_id>, <account_l1_field_id>)`)
   → poll the matching `get_distinct_values_result_by_alias`/`_by_id(handle)`
   until ready (async-fetch pattern).
   If the distinct call errors, fall back to
   `get_data_by_alias(<financials_alias>, select=[<account_l1_field>], limit=500)`
   (or the by-id twin) and collect the distinct values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`
   - balance-sheet categories ← `/asset|liabilit|equity/i`

   If a category has several candidates, pick the broadest top-level one; if
   genuinely ambiguous, ask the user once. If the L1 values partition as the
   balance-sheet equation (asset / liability / equity / income-like) rather
   than P&L buckets, the P&L categories live one level deeper — pull the
   `<account_l2_field>` distinct values and match `<revenue_value>` /
   `<cogs_value>` / `<opex_value>` there instead (see the data-scope
   discovery below).

Aggregation-field failures are handled reactively, not pre-probed (see Step 3).

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

### Step 3: Fetch Data via MCP

Aggregation-first. Run in parallel where possible. Use the alias path
(`start_aggregation_by_alias`) when `<financials_alias>` exists; otherwise the
by-id twin (`start_aggregation_by_id`).

1. **Monthly P&L** — `start_aggregation_by_alias(<financials_alias>,
   dimensions=[<account_l1_field>, <account_l2_field>, <month_field>],
   metrics=[{"field": <amount_field>, "agg": "SUM"}], filters=[{"name":
   <scenario_field>, "values": [<--scenario> or <discovered actuals-like scenario>], "is_excluded":
   false}])` → poll `get_aggregation_result_by_alias(handle)` until ready
   (async-fetch pattern). First validate the scenario against the domain from the
   data-scope discovery — if it isn't there, list the scenarios that do exist
   and ask rather than running an empty extract. Scope to `--year` with an
   advanced date filter (see below) or by filtering the `<month_field>`
   dimension client-side; when `--year` wasn't given, use the latest complete
   fiscal year from the discovered date range — never an unscoped all-time
   pull.
2. **Balance Sheet items** — same table grouped by `[<account_l1_field>,
   <account_l2_field>, <month_field>]`, filtered client-side to the balance-sheet
   account categories found in Step 2.3.
3. **Quarterly KPIs** — only if `<kpis_table_id>` was found:
   `start_aggregation_by_alias(<kpis_alias>, dimensions=[<metric_name_field>,
   <quarter_field>], metrics=[{"field": <kpi_value_field>, "agg": "SUM"}], …)`
   → poll `get_aggregation_result_by_alias(handle)` until ready (async-fetch
   pattern) (or the by-id twins), for `--year` and the prior year (for YoY). For named
   KPIs that aren't in a table (e.g. ARR), call `list_business_metrics` to
   check whether the org defines them as populated metrics — but this skill's
   toolset reads KPI *values* only from tables, so a KPI found in neither the
   KPI table nor the P&L-derivable grain is **omitted** from the workbook
   (see the KPI-honesty rule under Sheets to Generate). Never back into a
   SaaS metric by aggregating the P&L.
4. **Distinct values for validation** — derive the distinct `<scenario_field>`,
   `<month_field>`, and `<account_l1_field>` values from the aggregation results,
   or run the distinct-values start→poll tools (`start_distinct_values_by_alias`
   / `start_distinct_values_by_id` → the matching result tool) directly,
   to confirm the extract covers the expected dimensions.

**Reading the responses:** apply rule 4 of the data-scope discovery to every
aggregation payload — drop the trailing keyless grand-total row before
computing monthly totals, subtotals, or YoY math (keep it only as a checksum
for the Validation sheet), and treat `[null]` groups as their own explicit
bucket.

**Filter rules:**
- **Date ranges filter directly** via an advanced filter — no epoch workaround
  needed. To scope to `--year`, pass `{"name": <month_field>, "values": {"type":
  "advanced", "val": [{"condition": "total_range", "value": ["<jan1_epoch>",
  "<dec31_epoch>"]}]}}` (epoch seconds as strings; by-id uses the `field_id`
  form). Jan 1–Dec 31 assumes a calendar-aligned fiscal year — if the org's
  discovered fiscal calendar is offset, use its fiscal-year boundary dates
  instead. Adding `<month_field>` as a dimension and filtering by `--year`
  client-side still works and is optional.
- **Value-list filters** take `values: [...]` (set `is_excluded: true` for
  NOT-IN); advanced filters also support comparisons, ranges, text matching, and
  null checks.

**If an aggregation call fails on a dimension field with a 500:** that field
isn't usable as a dimension for this client. Re-inspect the Step 2 schema for
a sibling account-level field from the discovered schema (orgs often carry
in-between levels, or an `account_group_l1`-style alternative)
and retry with it. If the alias call errors, retry the by-id twin. If no sibling
works, tell the user which field failed.

Auto-refresh tokens are handled by the MCP layer; fall back to
`get_data_by_alias` / `get_data_by_id` with paging only if aggregation fails
outright. On `"truncated": true`, the returned rows are an incomplete prefix —
narrow the query per the `guidance` (more filters / fewer columns / lower
limit+offset paging) and re-fetch; never present the prefix as complete.

### Step 4: Build the Workbook Locally

Generate the xlsx with openpyxl. **Do not** call any server-side workbook tool — they have been removed.

Write a single Python script and execute it via `Bash`. The script reads a JSON payload of the extracted data and writes the xlsx.

If openpyxl is missing:
- Claude Code: `pip install openpyxl`.
- Claude.ai web / ChatGPT: openpyxl is preinstalled in the analysis/code interpreter sandbox.

## Sheets to Generate

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

1. **Summary**
   - Year, scenario, generation timestamp.
   - Totals: Revenue, COGS, Gross Profit, Gross Margin %, Operating Expenses, Operating Income, Net Income — each labeled with the period + scenario it covers (e.g. "FY<year> · <scenario>"), never presented as bare all-time numbers.
   - Balance Sheet snapshot: Total Assets, Total Liabilities, Total Equity (period-end, labeled with the as-of month).
   - KPI snapshot: only KPIs actually sourced per the rule above; drop the block entirely if none were sourceable.
   - Row-by-row validation checks (see sheet 4) summarized as PASS / FAIL count.

2. **P&L**
   - Rows: account categories discovered in Step 2.3, indented by L1/L2.
   - Columns: 12 months + Total + Prior Year + YoY Δ%.
   - Subtotals (Revenue, COGS, Gross Profit, Total OpEx, Operating Income) bolded.
   - Number format: `$#,##0` for dollars, `0.0%` for percentages.

3. **KPIs** *(only when at least one KPI was sourced — otherwise omit the sheet)*
   - One row per **sourced** metric. Columns: Q1 / Q2 / Q3 / Q4 / FY / Prior FY / YoY Δ%.
   - Candidate SaaS metrics (ARR, Net New ARR, Gross/Net Churn %, LTV, CAC, LTV/CAC, NRR, GRR) appear only when sourced per the rule above; P&L-derivable KPIs (revenue, gross/operating margin) are always fair game. No placeholder or estimated rows or columns — omit them instead.

4. **Validation**
   - One row per cross-check:
     - "P&L Revenue total equals KPI Revenue total" → PASS/FAIL with both values (skip when no KPI source exists).
     - "Sum of monthly Revenue equals annual Revenue" → PASS/FAIL.
     - "Grand-total checksum" — computed P&L total matches the aggregation response's keyless grand-total row → PASS/FAIL.
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
- Year and scenario extracted (every quoted total carries this label)
- Validation result count (e.g. "5/5 PASS")
- Any warnings (missing months, scenario gaps, KPIs omitted as unsourceable)

## Troubleshooting

**No table matches the financials pattern (Step 2)**
- List the tables you found and ask the user which one holds their P&L /
  financial data, then continue.

**Extract comes back empty for the requested scenario**
- Re-check the scenario domain from the data-scope discovery: the scenario
  name you filtered on may simply not exist in this org (budget-like data
  often lives in a planning-version field instead). Offer the scenarios that
  do exist.

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
