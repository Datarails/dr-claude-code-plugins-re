---
name: dr-intelligence
description: Comprehensive FP&A financial-analysis intelligence workbook for a FULL FISCAL YEAR — Excel, up to 10 sheets, with ranked auto-detected insights, findings and recommendations, and professional formatting; no PowerPoint. For a one-month KPI snapshot use dashboard; for an executive deck use insights. Self-contained — discovers the client's tables and fields on its own, no profile or setup step required.
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
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - Write
  - Read
  - Bash
argument-hint: "[--year <YYYY>] [--output <file>]"
---

# FP&A Intelligence Workbook

Generate a comprehensive 10-sheet FP&A intelligence workbook with auto-detected insights, recommendations, and professional Excel formatting.

This is the **most powerful** financial analysis skill — it answers real business questions, not just data dumps. All data is pulled via MCP tools and the workbook is built locally with openpyxl. No server-side rendering.

## Excel Context — Routing Preamble

Before any data pull, establish whether this skill is running in a **live Excel context**
(Claude for Excel with the Datarails Add-In loaded) and route accordingly.

**Detect — never infer from the user's wording.** A sheet list containing `__dr_agent`
means the add-in is loaded. Confirm with the `agent.get_session` probe, which you run by
executing Office.js through the `execute_office_js` tool (see the Excel Context Contract
in CLAUDE.md, §Transport) — it is not an MCP tool and has no MCP equivalent.
**A failed probe is a normal detection result**, not an error: it means "no bridge here",
which is the expected outcome in Claude Code. Do not surface it, do not retry it, and do
not apply this skill's connection-error or Connectors-UI guidance to it — that guidance is
about `datarails-finance-os` connector calls only.
**A successful probe means Excel context, on either transport.** The bridge serves two
add-in tracks and their session payloads differ: Flex (Office.js task pane) exposes
`isLoggedIn`; the COM desktop add-in — the majority of live workbooks — exposes
`isConnected` instead, and **`isConnected: false` is not a login failure, an error, or a
reason to stop or send the user anywhere**. It merely means the workbook isn't connected
to a Datarails file, which matters only to `drilldown_*` / `create_dynamic_range` (the
bridge skill gates those itself). Only Flex's explicit `isLoggedIn: false` means
sign-in is needed.

**Route by the target of the request, not by whether a workbook is open.**

- **Org / server data** — which tables, models and fields exist, aggregations, raw rows,
  distinct values, metrics, profiling — always the `datarails-finance-os` MCP connector,
  **even in Excel**. The bridge cannot answer these.
- **Workbook actions** — refresh, drill a cell, insert a DR function, read what a cell
  returns, publish, submit — always the add-in bridge. Never a native Excel recalc
  (`calculate()`, F9): it does not pull Datarails data and silently yields stale values.

**In a live Excel context this skill cannot produce its file deliverable.** Its generation
steps depend on the `Bash` tool, which that surface does not provide. Say so plainly and
offer the real alternatives — a scoped answer in chat, or re-running this skill from
Claude Code where file output works. Never improvise another route to a file, never hand
back a partial artifact, and never silently substitute a different deliverable: writing
into someone's live workbook instead of giving them the file they asked for is a
different and irreversible outcome, not a smaller version of the same one.

**If you do write DR formulas into the workbook, writing and refreshing are one atomic
step.** Write to a **new sheet**, fire `refresh_selected_cells_ribbon` scoped to that
range — a new-sheet block is one contiguous range, so one scoped call covers any cell
count — then read the range back. `refresh_ribbon` is not the tool for this: it repulls
every DR cell in the file and can silently move numbers elsewhere in the user's model.
It is reserved for the one case the scoped command can't cover — scattered inserts
across multiple sheets, per `excel-context`'s refresh-after-insert rule — and
even then only with the user's explicit OK, after snapshotting the DR ranges you can
bound, reporting each changed cell in them before → after with the compared ranges
named, and saying plainly that cells beyond them may also have updated. If the user
declines the whole-workbook refresh, fall back to scoped `refresh_selected_cells_ribbon`
calls sheet-by-sheet — slower, but nothing outside the written cells moves. A freshly
written DR formula reads `Missing` / `Loading…` / `#BUSY!` until an agent refresh lands,
so never quote a value you have not read back after a successful refresh, and never
present a figure fetched from the MCP connector as though it were the cell's value.
`/dr-get-formula` is the full authority for DR.GET workbooks.

**If the user asks you to elaborate on a DR-backed figure** — "explain", "break down",
"what's driving this", "why is X" — and the figures in scope are DR formula cells, offer
the add-in's drill-down instead of silently re-deriving the number through the MCP
connector. A drill resolves the exact filters behind that cell; a hand-rebuilt query only
approximates them.
<!-- end:excel-context-preamble -->

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
| `--year <YYYY>` | Calendar year to analyze | Latest complete fiscal year (or trailing 12 closed months) from the discovered date range — never an unscoped all-time total |
| `--output <file>` | Output file path | `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx` |

## Workflow

### Step 1: Verify Connection

If a `datarails-finance-os` **connector** call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

(A failed `agent.get_session` probe is **not** this case — that is normal Excel-context
detection, handled by the routing preamble above, and never a reason to send the user
to Connectors UI.)

### Step 2: Discover the financials table, its fields, and (if present) a KPI table

**If you already discovered these earlier in THIS conversation, reuse them —
skip to Step 3.** Discovery is cheap but not free; do it once per
conversation, then carry the values forward.

1. `list_data_models`. Pick the **financials** table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the largest
   by row count. Note **both** its numeric `id` (`<financials_table_id>`) and its
   `alias` (`<financials_alias>`; the alias may be empty). **Prefer the alias
   path when an alias exists** — friendlier field names, far fewer tokens. Also
   note any **KPI / metrics** table — name (or alias) matches `/kpi|metric|saas/i`
   — as `<kpis_table_id>` / `<kpis_alias>` if one exists. If you found a
   KPI/metrics table, the SaaS Metrics sheet pulls from it; otherwise build it
   from whatever metrics live in the financials table.

2. Fields. If the table has an alias, `list_aliased_fields(<financials_alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each field's
   numeric `id` — the by-id tools address fields by id). Bind these by
   case-insensitive match on the field alias/name (respecting the noted type) —
   bind only those the sheets use:
   - `<amount_field>`     — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`   — categorical: `^scenario$` → `^version$`
   - `<month_field>`      — date/period: `reporting_date` → `posting_date` → `^month$` → `^date$`
   - `<account_l1_field>` — `dr_acc_l1` → `account_l1` → `account_group_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2` → `account_group_l2`
   - `<vendor_field>`     — `^vendor$` → `vendor_name` → `supplier` (Vendor Analysis sheet)
   - `<cost_center_field>` — `cost_center` → `department` → `dr_cost_center` (Cost Center P&L sheet)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   If `<kpis_table_id>` exists, `list_aliased_fields(<kpis_alias>)` (or
   `get_fields_by_id(<kpis_table_id>)`) and bind:
   - `<metric_name_field>` — `^metric$` → `metric_name` → `kpi_name`
   - `<quarter_field>`     — `^quarter$` → `quarter` → the KPI table's date field
   - `<kpi_value_field>`   — numeric: `^value$` → `^amount$`

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use. A missing `<vendor_field>` or `<cost_center_field>`
   just omits that sheet — don't block on it.

3. Find the account grain and the category values the insight rules and
   filters need. Call
   `start_distinct_values_by_alias(<financials_alias>, <account_l1_field>)` (or
   `start_distinct_values_by_id(<financials_table_id>, <account_l1_field_id>)`)
   → poll the matching `get_distinct_values_result_by_alias`/`_by_id` with the
   handle until ready (async-fetch pattern; pass `limit` to the result tool),
   and the same for `<account_l2_field>`. Per the data-scope preamble below,
   pick the **P&L grain**: the level whose values partition into
   revenue/COGS/opex-like buckets — if the top level's values are
   balance-sheet-equation buckets rather than P&L flows, the P&L line items
   live one level deeper. Rebind `<account_l1_field>` to that P&L-grain level
   (and `<account_l2_field>` to the next level down, when one exists) so every
   category pull, filter, and sheet downstream uses the discovered grain. If a
   distinct call errors, fall back to
   `get_data_by_alias(<financials_alias>, select=[<account_l1_field>], limit=500)`
   (or the by-id twin) and collect the distinct values. Match:
   - `<revenue_value>` ← `/revenue|sales|income/i`
   - `<cogs_value>`    ← `/cogs|cost of goods|cost of sales|direct cost/i`
   - `<opex_value>`    ← `/operating|opex|expense|sg&a/i`

   If a category has several candidates, pick the broadest one at the P&L
   grain; if genuinely ambiguous, ask the user once. Scope every P&L pull in
   Step 3 to these buckets — never present balance-sheet
   (asset/liability/equity-like) totals as revenue or expenses.

Aggregation-field failures are handled reactively, not pre-probed (see Step 3).

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Each response returns **exactly one row per requested group** — no subtotal rows and no grand-total row mixed into the `data` list; grand totals arrive in a separate top-level `totals` field beside the rows (`{"data": [...], "totals": {...}}`), computed across **all** groups, not just the returned prefix. **For a grand total, read `totals` — never sum the rows when the response carries `truncated: true`** (summing the returned prefix silently under-counts; dev repro: 474 of 31,455 rows summed to 21% of the true total). **`totals` combines the per-group results rather than re-scanning the rows**, so it is exact exactly when the aggregation is decomposable: SUM (sum of the group sums), COUNT (sum of the group counts), MIN, and MAX. It is **WRONG for AVG** (unweighted mean of the group averages) and **COUNT_UNIQUE** (sum of the per-group distinct counts, so a value recurring across groups is counted once per group) — true average = SUM total ÷ COUNT total (two calls: a field may be aggregated at most once per request); true distinct count = the distinct-values tools. Treat every aggregation type not named exact above — **`UNIQUE_VALUES` included**, whose cross-group de-duplication is unverified (the `COUNT_UNIQUE` behaviour above is evidence the engine may not de-duplicate across groups at all) — as not decomposable: derive it from complete rows or the distinct-values tools, never from `totals`. `totals` is absent on dimension-less aggregations (the single returned row IS the total) and may be absent on responses cached before the rollout (cache TTL ≤ 7 days) — only in those two cases is a total obtained by summing complete (untruncated) rows. Null groups arrive explicitly labeled `[null]` and are real groups; read null counts from that bucket. **Defensive filter:** keep only rows in which **every requested dimension key is present** — a roll-up row *omits* one or more keys entirely, whereas a genuine null is *present* with the value `[null]`. On a correct response this is a no-op; it guards against a stale cached response still carrying legacy subtotal and grand-total rows, each of which equals the whole total and would inflate any sum. When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~50 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. On aggregations the top-level `totals` field is **unaffected by truncation** (computed across all groups, not just the returned prefix) — read grand totals from it instead of re-fetching. Narrow the query (fewer dimensions, more filters, fewer selected columns — or a business metric for a named KPI) and re-fetch **only when the rows themselves are needed** beyond the cap; with `totals` present, a SUM/COUNT/MIN/MAX grand total never requires a re-fetch or chunking by dimension (AVG, COUNT_UNIQUE and UNIQUE_VALUES never read `totals` — true average = SUM total ÷ COUNT total from two calls; true distinct count = the distinct-values tools). A truncated response **without** `totals` (pre-rollout cache) cannot answer a grand-total question from its prefix. Re-run the aggregation **once** — a fresh run may miss the stale entry and return `totals`. If the re-run still carries no `totals`, stop re-running and fall back to narrowing or chunking by dimension until the responses are complete, then sum those rows. Never total the prefix.

### Step 3: Fetch Data via MCP

Run these data pulls in parallel where possible. Use the aggregation
start→poll tools first (`start_aggregation_by_alias` when the table has an
alias, else `start_aggregation_by_id` — you can start several jobs, then poll
their handles); fall back to row fetches (`get_data_by_alias` /
`get_data_by_id`) only if aggregation fails outright.

Aggregation call shapes:
- Alias path: `start_aggregation_by_alias(alias=<financials_alias>,
  dimensions=[<field_aliases>], metrics=[{"field": <amount_field>, "agg": "SUM"}],
  filters=[...])` → poll `get_aggregation_result_by_alias(handle)` until ready
  (async-fetch pattern).
- By-id path: `start_aggregation_by_id(table_id=<financials_table_id>,
  dimensions=[<field_ids>], metrics=[{"field_id": <amount_field_id>, "agg":
  "SUM"}], filters=[...])` → poll `get_aggregation_result_by_id(handle)` until
  ready (async-fetch pattern).

**Default scope (data-scope preamble):** filter every P&L pull to a single
scenario — the actuals-like value from the discovered scenario domain unless
the user asked for another — and to `--year` (or, when `--year` was omitted,
the latest complete fiscal year / trailing 12 closed months from the
discovered date range). Carry the period + scenario into every sheet label.

**Reading responses (preamble rule 4):** every row is a real group and no total
row is appended to the rows — grand totals and share denominators read from the
response's top-level `totals` field (exact even when the rows are truncated;
never sum a truncated prefix). But most pulls below
are **multi-dimensional** (e.g. `[account_l1, month]`), so a row is *not* a
time-series point — **aggregate to the intended grain first**: by month alone
for company-level trends, by `group + month` for per-account or per-department
trends (per-grain series and subtotals come from complete rows — `totals` is
the overall grand total, not a series). Only then compute totals, shares,
MoM/YoY deltas and the σ anomaly
rule. Skipping that step compares different accounts as adjacent periods and
repeats the same month. Read null counts only from the explicit `[null]`
bucket.

1. **Monthly P&L** — aggregate on the financials table grouped by
   `[<account_l1_field>, <month_field>]`, summed by `<amount_field>`. Scope
   `--year` either by an advanced date filter on `<month_field>` (see below) or
   by keeping `<month_field>` as a dimension and filtering client-side.
2. **Monthly P&L by L2** — same, grouped by `[<account_l1_field>, <account_l2_field>, <month_field>]`. Used for top-20 expense drilldown and cost center P&L.
3. **Vendor spend** — only if `<vendor_field>` was found: aggregate grouped by `[<vendor_field>]`, summed by `<amount_field>`, filtered to the `<opex_value>` accounts (from Step 2.3) for `--year`.
4. **Cost center spend** — only if `<cost_center_field>` was found: aggregate grouped by `[<cost_center_field>, <month_field>]`.
5. **KPIs** — only if `<kpis_table_id>` was found: aggregate on it grouped by `[<metric_name_field>, <quarter_field>]`, summed by `<kpi_value_field>`, for the year and one prior. For named-KPI questions you can also discover canonical KPIs via `list_business_metrics` (flat list — id, name, category, dimensions) and compute their values from the aggregated financials/KPI table here.
6. **Anomalies** — `profile_numeric_fields` for baseline MIN/MAX/AVG/COUNT per
   numeric field. This tool does NOT return outliers, std dev, or percentiles —
   it returns baseline aggregates. There is no server-side anomaly tool; compute
   outlier flags client-side using the σ-rule below applied to the monthly P&L
   time series pulled in step 1.

**Scoping by year (date filter):** date ranges now filter directly via an
**advanced** filter — no epoch workaround. Pass
`{"name": <month_field>, "values": {"type": "advanced", "val": [{"condition":
"total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}` (by-alias) or the
`{"field_id": <month_field_id>, ...}` form (by-id); epoch seconds go in as
strings. Keeping `<month_field>` as a dimension and filtering client-side still
works and is optional.

**If an aggregation call fails on a dimension field with a 500:** that field
isn't usable as a dimension for this client. Re-inspect the Step 2 schema for
a sibling account-level field from the discovered schema (orgs often carry
in-between levels, or a name variant like `account_group_l1`) and retry with it. If the alias call errors, retry the by-id twin. If no
sibling works, tell the user which field failed.

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

Budget-dependent rules (e.g. cost center over budget) apply only when a
budget-like scenario or planning-version field was discovered (data-scope
preamble, item 1); otherwise skip them — never fabricate a budget baseline.

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

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

1. **Insights Dashboard** — Top 5 findings with severity color, current period KPIs (Revenue, Gross Margin, OpEx from the discovered P&L grain; Burn and Runway only if sourced per the KPI-honesty rule above — omit those cards otherwise), and the ranked recommendations list.
2. **Expense Deep Dive** — Top 20 expense accounts: amount, % of total OpEx, MoM Δ%, YoY Δ%. Color the % cells with a green→red color scale.
3. **Variance Waterfall** — Current period vs. prior period: contribution to total variance line by line. Use a bar chart.
4. **Trend Analysis** — 12-month rolling P&L: Revenue, COGS, Gross Profit, OpEx, Net Income. One line per metric, secondary axis for margin %.
5. **Anomaly Report** — Outlier rows identified by applying the σ-based
   rule to the monthly P&L series. Use `profile_numeric_fields` for the
   field-level baselines that feed the computation (there is no server-side
   anomaly tool — the findings are computed client-side). Severity column,
   drill-down hint per row.
6. **Vendor Analysis** — Top 20 vendors: spend, % of OpEx, MoM Δ. Concentration risk flag column. Pie chart for top-10.
7. **SaaS Metrics** — only the SaaS/unit-economics metrics actually sourced per the KPI-honesty rule (e.g. ARR, NRR, CAC, LTV when they exist as populated metrics in the KPI table or metric catalog). Quarterly columns; YoY column at right. Omit the sheet entirely when none are sourced.
8. **Sales Performance** — Rep-level: bookings, win rate, ACV, ramp status. Cohort table by hire quarter. Only if a sales/bookings-like table or populated metrics were discovered; omit the sheet otherwise (KPI-honesty rule).
9. **Cost Center P&L** — Department × month grid with totals row and YoY column. Conditional formatting on Δ%.
10. **Raw Data** — Long-form pivot-ready dataset (the monthly L1×L2 frame). No formatting — just headers + data.

Each sheet must include a generation timestamp footer and the period +
scenario analyzed (data-scope preamble: label every output).

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
- **Every rule here applies to the retrieval/period family** — `DR.GET`,
  `DR.QTD`, `DR.YTD`, `DR.MTD` share one form (`=DR.QTD(Value, "[Dim]",
  CellRef, ...)`), one cell-reference discipline, one `Value` defined-name
  requirement, one no-wrapping rule. "DR.GET" in this contract means that
  family. Helper functions with their own documented signatures (e.g.
  `DR.INCLUDE`, `DR.RANGE`) are **not** covered here — author those only from
  their own documentation, never by analogy with this form.
- **In a live Excel context, writing DR formulas and refreshing them is one
  atomic step** — a freshly written DR cell reads `Missing` until an agent
  refresh lands, and only read-back values may be quoted. The Excel-context
  routing preamble (or the skill's own Step 0 workflow) owns that procedure;
  this contract owns the formula text.

The get-formula skill (`/dr-get-formula`) is the full reference — parameter
cells, validated dimension values, report layouts. Prefer it for whole formula
workbooks; apply this contract when adding any retrieval/period DR formula
(`DR.GET`/`DR.QTD`/`DR.YTD`/`DR.MTD`) to a workbook here.
<!-- end:drget-authoring-contract -->

## Step 6: Output

After writing the file, surface it to the user:

- **Claude.ai web / ChatGPT**: present the xlsx as a downloadable artifact.
- **Claude Code**: print the absolute path and a one-line summary of what was generated.

Always include in the summary:
- Output file path
- Period + scenario analyzed
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

Questions 7 and 8 depend on sales/SaaS data existing in the org — when none
was discovered, the workbook omits those sheets rather than fabricating
answers (KPI-honesty rule).

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
  (`<vendor_field>`, `<cost_center_field>`, KPI table) wasn't found — or
  whose KPIs couldn't be sourced (KPI-honesty rule) — is omitted by design.

## Related Skills

- `/dr-extract` — Basic data extraction (P&L + KPIs only, faster).
- `/dr-insights` — Executive PowerPoint + Excel combo.
- `/dr-anomalies-report` — Focused on data quality issues.
- `/dr-reconcile` — P&L vs KPI validation.
