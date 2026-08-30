---
name: dr-dashboard
description: Executive KPI dashboard — a ONE-MONTH metrics snapshot for the latest closed month (not real-time; the in-progress month is excluded) — Excel dashboard + single-slide PowerPoint one-pager. For a full-fiscal-year narrative deck use insights; for a year-long analysis workbook use intelligence; for a raw data export use extract.
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
argument-hint: "[--period <YYYY-MM>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Executive KPI Dashboard

Generate executive KPI monitoring dashboards for the latest closed month.

Creates both Excel dashboards (for analysis) and PowerPoint one-pagers (for meetings).

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
across multiple sheets, per `excel-context__internal`'s refresh-after-insert rule — and
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

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--period <YYYY-MM>` | Month to dashboard for | Latest closed month discovered in the data (never assume the calendar month has data) |
| `--output-xlsx <file>` | Excel output path | `tmp/Executive_Dashboard_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Dashboard_OnePager_TIMESTAMP.pptx` |

## Data Discovery

Before fetching any numbers, discover what the org actually has: `list_data_models` for the financials table, then `get_fields_by_id` / `list_aliased_fields` for its fields. Never assume field names, scenario values, or metric availability — they differ per org.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Each response returns **exactly one row per requested group** — no subtotal rows and no grand-total row mixed into the `data` list; grand totals arrive in a separate top-level `totals` field beside the rows (`{"data": [...], "totals": {...}}`), computed across **all** groups, not just the returned prefix. **For a grand total, read `totals` — never sum the rows when the response carries `truncated: true`** (summing the returned prefix silently under-counts; dev repro: 474 of 31,455 rows summed to 21% of the true total). **`totals` combines the per-group results rather than re-scanning the rows**, so it is exact exactly when the aggregation is decomposable: SUM (sum of the group sums), COUNT (sum of the group counts), MIN, and MAX. It is **WRONG for AVG** (unweighted mean of the group averages) and **COUNT_UNIQUE** (sum of the per-group distinct counts, so a value recurring across groups is counted once per group) — true average = SUM total ÷ COUNT total (two calls: a field may be aggregated at most once per request); true distinct count = the distinct-values tools. Treat every aggregation type not named exact above — **`UNIQUE_VALUES` included**, whose cross-group de-duplication is unverified (the `COUNT_UNIQUE` behaviour above is evidence the engine may not de-duplicate across groups at all) — as not decomposable: derive it from complete rows or the distinct-values tools, never from `totals`. `totals` is absent on dimension-less aggregations (the single returned row IS the total) and may be absent on responses cached before the rollout (cache TTL ≤ 7 days) — only in those two cases is a total obtained by summing complete (untruncated) rows. Null groups arrive explicitly labeled `[null]` and are real groups; read null counts from that bucket. **Defensive filter:** keep only rows in which **every requested dimension key is present** — a roll-up row *omits* one or more keys entirely, whereas a genuine null is *present* with the value `[null]`. On a correct response this is a no-op; it guards against a stale cached response still carrying legacy subtotal and grand-total rows, each of which equals the whole total and would inflate any sum. When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~50 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. On aggregations the top-level `totals` field is **unaffected by truncation** (computed across all groups, not just the returned prefix) — read grand totals from it instead of re-fetching. Narrow the query (fewer dimensions, more filters, fewer selected columns — or a business metric for a named KPI) and re-fetch **only when the rows themselves are needed** beyond the cap; with `totals` present, a SUM/COUNT/MIN/MAX grand total never requires a re-fetch or chunking by dimension (AVG, COUNT_UNIQUE and UNIQUE_VALUES never read `totals` — true average = SUM total ÷ COUNT total from two calls; true distinct count = the distinct-values tools). A truncated response **without** `totals` (pre-rollout cache) cannot answer a grand-total question from its prefix. Re-run the aggregation **once** — a fresh run may miss the stale entry and return `totals`. If the re-run still carries no `totals`, stop re-running and fall back to narrowing or chunking by dimension until the responses are complete, then sum those rows. Never total the prefix.

## Key Metrics Included

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

The lists below are **candidates**, not guarantees — each card renders only when sourceable per the rule above:

**Growth & Revenue**:
- ARR (Annual Recurring Revenue)
- Revenue
- MoM/QoQ growth rates

**Health & Efficiency**:
- Churn rate (%)
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)

**Operational**:
- Burn rate (monthly)
- Runway (months of cash)
- Burn multiple

**Custom Metrics**: Any KPI in your data (adapts to profile)

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
| Chart 2 | `F93576` | Budget/plan series — whichever plan side discovery found (hot pink) |
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

## Output

### Excel Dashboard
- Summary sheet with top KPIs
- All Metrics sheet with complete list
- Current values
- Status indicators (✅ or ⚠️)
- Period + scenario label on every sheet and figure

### PowerPoint One-Pager
- Single professional slide
- Top metrics in boxes
- Color-coded for quick scanning
- Period + scenario stated on the slide
- Generated timestamp
- Perfect for executive team syncs

## Examples

### Generate dashboard for the latest closed month
```bash
/dr-dashboard
```

Output (illustrative — your org's period, metric count, and values will differ):
```
📊 Generating dashboard for 2026-02...
  📈 Fetching KPI metrics...
  📊 Calculating trends...
  📋 Generating Excel dashboard...
  🎯 Generating PowerPoint one-pager...

✅ Dashboard generated successfully

==================================================
EXECUTIVE DASHBOARD
==================================================
Period: 2026-02
Metrics: 7

Outputs:
  Excel: tmp/Executive_Dashboard_2026-02-03_143022.xlsx
  PowerPoint: tmp/Dashboard_OnePager_2026-02-03_143022.pptx
==================================================
```

### Specific month
```bash
/dr-dashboard --period 2025-12
```

### With custom locations
```bash
/dr-dashboard \
  --output-xlsx reports/dashboard.xlsx \
  --output-pptx reports/dashboard.pptx
```

## Use Cases

### Daily Executive Sync
```bash
/dr-dashboard  # Use PowerPoint for standup
```

### Weekly Team Update
```bash
# Share Excel for details, PowerPoint for overview
/dr-dashboard
```

### Monthly Board Package
```bash
# Generate for month-end
/dr-dashboard --period 2026-01
```

### Investor Demo
```bash
# Professional one-pager
/dr-dashboard --output-pptx investors_dashboard.pptx
```

## Performance

- Generation: <2 minutes
- Real-time KPI data
- Scales to 100+ metrics
- Efficient aggregation

## Color Coding

- ✅ **Green** - Positive metrics (high revenue, low churn)
- ⚠️ **Yellow** - Needs attention (rising burn, declining growth)
- 🔴 **Red** - Critical (low runway, high churn)

## Features

**Excel Dashboard**:
- Sortable data
- Easy drill-down
- Print-friendly
- Shareable format

**PowerPoint One-Pager**:
- Executive-ready
- Meeting-ready (1 slide)
- Branded template
- Easy to share

## Automated Updates

Schedule weekly updates:
```bash
# Every Monday at 8 AM
0 8 * * 1 /dr-dashboard \
  --output-pptx reports/weekly_dashboard.pptx
```

## Integration

Works with:
- `/dr-insights` - Understand why metrics changed
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-extract` - Get latest data

## Related Skills

- `/dr-insights` - Detailed trend analysis
- `/dr-reconcile` - Validate KPI accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-forecast-variance` - Forecast vs actual
