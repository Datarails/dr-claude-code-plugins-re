---
name: dr-anomalies-report
description: Detect data anomalies and generate a comprehensive data-quality Excel WORKBOOK from Finance OS tables, computed over the table's ALL-TIME history (use the anomalies skill for a chat-only answer scoped to the latest fiscal year — the two baselines differ by design, so counts won't match). The MCP tools return baseline aggregates only; this skill derives findings, severity buckets, and the Data Quality Score client-side, then writes a multi-sheet workbook. Self-contained — pass --table-id to target a table directly, or it discovers the financials table on its own; no profile or setup step required.
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
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__list_business_metrics
  - Write
  - Read
  - Bash
argument-hint: "[--table-id <id>] [--severity <level>] [--output <file>]"
---

# Anomaly Detection Report

Generate a comprehensive data-quality Excel workbook for a Finance OS
table. Works with any table — no pre-configuration required.

> **Tool reality check:** the MCP `profile_numeric_fields` and
> `profile_categorical_fields` tools are thin wrappers — they return
> baseline aggregates only (SUM/AVG/MIN/MAX/COUNT for numerics,
> distinct-value samples capped at 5 fields for categoricals). There is
> no server-side anomaly tool. **This skill computes every finding,
> severity bucket, and the Data Quality Score client-side.** See
> `/dr-anomalies` for the per-category recipes; this skill consumes those
> same recipes and packages the result as an Excel workbook.

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

## Design Principles

**General-Purpose**:
- ✅ No hardcoded table IDs or field names
- ✅ Adapts to any client structure
- ✅ Pass `--table-id` to target any table directly (zero discovery)
- ✅ Otherwise discovers the financials table inline

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--table-id <id>` | Specific table to analyze (used directly, no discovery) | Discovers the financials table |
| `--severity <level>` | Filter results: critical, high, medium, low | All |
| `--output <file>` | Output filename | `tmp/Anomaly_Report_TIMESTAMP.xlsx` |

## What It Reports

### Summary Sheet
- **Data Quality Score** (0-100)
- Health status indicator
- Anomaly count by severity
- Key metrics

### Critical Findings Sheet
- Anomalies requiring immediate attention
- Sample records for investigation
- Field-specific details
- Recommended actions

### High Priority Sheet
- Issues to address this week
- Full descriptions
- Count and context

### Analysis Sheets
- **Numeric Analysis**: SUM, AVG, MIN, MAX, COUNT per numeric field (from
  `profile_numeric_fields`) plus a skill-derived range-band outlier
  flag. Std dev and percentiles are not returned by the API and are
  not reported unless the skill bucketed the field via the aggregation
  start→poll tools (`start_aggregation_by_*` →
  `get_aggregation_result_by_*`) (note that in the sheet when present).
- **Categorical Analysis**: Distinct count and sample values from
  `profile_categorical_fields` (capped at 5 fields per call), plus
  per-value frequencies derived from the aggregation start→poll tools
  (`start_aggregation_by_*` → `get_aggregation_result_by_*`) (nulls
  appear as the explicit `[null]` bucket; every returned row is a real
  group, so the frequency table needs no total-row exclusion).
- **Sample Records**: Actual data samples for top findings, fetched
  via `get_data_by_alias` / `get_data_by_id` after the skill identifies
  the IDs to pull.

## Workflow

**Phase 1: Discovery**
1. Verify connection (if a `datarails-finance-os` connector call fails, guide the user to Connectors UI — this never applies to the Excel-context probe, whose failure is normal detection per the routing preamble)
2. Resolve the target table (see below) — note **both** its numeric `id` and
   its `alias` (the alias may be empty)
3. Load that table's fields — if it has an alias, `list_aliased_fields(<alias>)`
   (business-friendly aliases); otherwise `get_fields_by_id(<table_id>)`
   (capture each field's numeric `id` — the by-id tools need ids). **Prefer the
   alias path when an alias exists.**

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

**Resolve the target table:**

- **If `--table-id <id>` was passed:** use it directly as `<table_id>`. **No
  discovery needed** — the user named the table. This works for any table,
  financial or not; skip straight to loading its fields. (Don't try to
  name-match or look for category values that may not exist on an arbitrary
  table.) Resolve its alias via `list_data_models` if you want the alias path.

- **Otherwise (default / no-arg path):** discover the financials table inline.
  **If you already discovered it earlier in THIS conversation, reuse it.**
  1. `list_data_models`. Pick the financials table: the one whose name (or
     alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
     largest by row count. Note its numeric `id` and its `alias`.
  2. Load fields with `list_aliased_fields(<alias>)` (if aliased) or
     `get_fields_by_id(<table_id>)`. The anomaly analysis is field-agnostic —
     it profiles whatever numeric and categorical fields the schema exposes —
     so no semantic field binding is required here. When per-value frequency,
     null, or duplicate detection needs a grouping dimension, take the
     categorical fields straight from this schema.
  3. If category-aware findings (rare-value, future-dated) need the account
     dimension, collect distinct values via
     `start_distinct_values_by_alias(<alias>, <account_field>)` (or
     `start_distinct_values_by_id(<table_id>, <account_field_id>)`) → poll
     the matching `get_distinct_values_result_by_*(handle)` until ready
     (async-fetch pattern). If the distinct call errors, fall back to
     `get_data_by_alias(<alias>, select=[<account_field>], limit=500)` (or the
     by-id twin) and dedupe.

Aggregation-field failures are handled reactively, not pre-probed: if an
aggregation start→poll call (`start_aggregation_by_*` →
`get_aggregation_result_by_*`) 500s on a dimension field, re-inspect the
schema for a sibling and retry; if the alias call fails, fall back to the
by-id twin; if none works, tell the user which field failed.

**Phase 2: Gather baseline aggregates**

> **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**

**Period: this skill deliberately overrides item 3 above.** Its baseline is
**ALL-TIME by design** — a data-quality scan covers the whole table, because
the future-dated-rows check and out-of-range detection only work if the
queries can see rows *outside* the expected window. (Filtering to the
*discovered* range would in any case be a no-op: the range is derived from
the data's own MIN/MAX, so it already contains every row — including the
future-dated ones the check exists to find.) The period rule in item 3
governs financial *reporting*; this workbook is a data-quality artifact.
Consequence: its outlier counts, null rates, and severity-bucket sizes **will
not match `/dr-anomalies`**, which scopes the same recipes to the latest
complete fiscal year — state the baseline in the workbook so the two are
never read as the same measurement, and never let the Numeric Analysis
SUM/AVG columns be read as period P&L figures.

**Scenario: NOT exempt — discover it and split on it.** The period override
above does *not* extend to scenario, and an unscoped multi-scenario scan
produces false findings rather than broader ones:

- **Duplicates.** The same account + period appearing under `Actuals` and
  `Budget` is the table working correctly, not a duplicate. Cross-scenario
  pairs must never be reported as duplicate rows.
- **Range-band outliers.** Plan/forecast rows carry different magnitudes than
  actuals, so pooling them widens `MAX - MIN` and can both mask real actuals
  outliers and flag ordinary forecast values.
- **Null rates.** Plan rows legitimately leave different fields empty, so a
  pooled null rate describes no scenario in particular.

So in Phase 1, **discover the scenario domain** the same way `/dr-anomalies`
does — pull distinct values of the scenario-like field
(`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool);
never assume a scenario name exists. Then either add the scenario field as a
grouping dimension to the duplicate / rare-value / null-rate aggregates and
report findings **per scenario**, or scope the scan to the actuals-like
scenario and say so. Either way the workbook names the scenarios it covers —
which it cannot do honestly without discovering them first.

1. `profile_numeric_fields(table_id)` — full numeric coverage
   (SUM/AVG/MIN/MAX/COUNT per numeric field). Treat the result as a
   starting point, not as classified findings.
2. `profile_categorical_fields(table_id, fields=[...])` — pass an
   explicit field list (tool silently caps at 5 per call; loop as
   needed to cover them all).
3. For per-value frequencies, null counts, and duplicate detection:
   `start_aggregation_by_alias` (preferred) or
   `start_aggregation_by_id` grouped by the relevant dimension(s) with
   `COUNT` of a **different dense field** as the metric — never COUNT
   the grouped dimension itself (see "Reading GROUP BY responses"
   below) — by-alias `metrics=[{"field": <other_field_alias>, "agg":
   "COUNT"}]`, by-id `metrics=[{"field_id": <other_field_id>, "agg":
   "COUNT"}]` → poll the matching `get_aggregation_result_by_alias` /
   `get_aggregation_result_by_id` with the `handle` until ready
   (async-fetch pattern). **This is where the actual findings come
   from** — the profile tools alone can't produce them.
4. For top-finding row samples: `get_data_by_alias` /
   `get_data_by_id`. You can filter directly with an advanced condition
   tree — e.g. comparison `{"name": <amount_alias>, "values":
   {"type": "advanced", "val": [{"condition": "gt", "value":
   "<band>"}]}}` to pull outlier rows, or a value-list IN of the
   offending IDs (`{"name": <id_alias>, "values": [...]}`). Comparisons,
   ranges, and `is null` are all supported — no need to pre-identify IDs
   purely because the filter API can't express a comparison.

> **Reading GROUP BY responses.** Each response returns **exactly one row per requested group** — no subtotal rows and no grand-total row mixed into the `data` list; grand totals arrive in a separate top-level `totals` field beside the rows (`{"data": [...], "totals": {...}}`), computed across **all** groups, not just the returned prefix. **For a grand total, read `totals` — never sum the rows when the response carries `truncated: true`** (summing the returned prefix silently under-counts; dev repro: 474 of 31,455 rows summed to 21% of the true total). **`totals` combines the per-group results rather than re-scanning the rows**, so it is exact exactly when the aggregation is decomposable: SUM (sum of the group sums), COUNT (sum of the group counts), MIN, and MAX. It is **WRONG for AVG** (unweighted mean of the group averages) and **COUNT_UNIQUE** (sum of the per-group distinct counts, so a value recurring across groups is counted once per group) — true average = SUM total ÷ COUNT total (two calls: a field may be aggregated at most once per request); true distinct count = the distinct-values tools. Treat every aggregation type not named exact above — **`UNIQUE_VALUES` included**, whose cross-group de-duplication is unverified (the `COUNT_UNIQUE` behaviour above is evidence the engine may not de-duplicate across groups at all) — as not decomposable: derive it from complete rows or the distinct-values tools, never from `totals`. `totals` is absent on dimension-less aggregations (the single returned row IS the total) and may be absent on responses cached before the rollout (cache TTL ≤ 7 days) — only in those two cases is a total obtained by summing complete (untruncated) rows. Null groups arrive explicitly labeled `[null]` and are real groups; read null counts from that bucket. **Defensive filter:** keep only rows in which **every requested dimension key is present** — a roll-up row *omits* one or more keys entirely, whereas a genuine null is *present* with the value `[null]`. On a correct response this is a no-op; it guards against a stale cached response still carrying legacy subtotal and grand-total rows, each of which equals the whole total and would inflate any sum. When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

> **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~50 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. On aggregations the top-level `totals` field is **unaffected by truncation** (computed across all groups, not just the returned prefix) — read grand totals from it instead of re-fetching. Narrow the query (fewer dimensions, more filters, fewer selected columns — or a business metric for a named KPI) and re-fetch **only when the rows themselves are needed** beyond the cap; with `totals` present, a SUM/COUNT/MIN/MAX grand total never requires a re-fetch or chunking by dimension (AVG, COUNT_UNIQUE and UNIQUE_VALUES never read `totals` — true average = SUM total ÷ COUNT total from two calls; true distinct count = the distinct-values tools). A truncated response **without** `totals` (pre-rollout cache) cannot answer a grand-total question from its prefix. Re-run the aggregation **once** — a fresh run may miss the stale entry and return `totals`. If the re-run still carries no `totals`, stop re-running and fall back to narrowing or chunking by dimension until the responses are complete, then sum those rows. Never total the prefix.

**Phase 2b: Derive findings (client-side)**

**First normalize each GROUP BY response**: keep only rows in which every
requested dimension key is present (data-scope preamble, item 4), preserving
genuine `[null]` values — during the stale-cache window this drops legacy
roll-up rows that would otherwise inflate the null-rate denominator and the
per-value frequency shares. Then apply the recipes from `/dr-anomalies`
(range-band outliers, null rates, duplicates, rare-category values,
future-dated rows) to the aggregates from Phase 2 — **but over this skill's all-time baseline,
not the fiscal-year window the recipes are specified for in
`/dr-anomalies`** (the borrowed recipes carry their window with them;
the counts will differ from a `/dr-anomalies` run by design). When tabulating a
GROUP BY response, every row is a real group — no total row is appended to the
rows — and the **total-row-count denominator is the response's top-level
`totals` COUNT when present** (exact even under truncation), else your own sum
of all group counts (including `[null]`) from a complete response. Null rate =
the `[null]`-bucket count ÷ that denominator. Bucket by severity using the
heuristics in that skill. Drop categories the API can't support
(referential integrity, character-level hygiene).

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

**Phase 3: Report Generation**
1. Categorize the skill-derived findings into Critical / High / Medium / Low
   per the heuristics in `/dr-anomalies` (the skill, not the tool).
2. Compute the Data Quality Score from those counts (formula below).
3. Generate the Excel workbook with the sheets described in
   "What It Reports". Use openpyxl locally — no server-side rendering.
4. Apply Datarails brand styling (see below).

**Phase 4: Summary**
1. Display key findings — make clear in the spoken summary that every
   number was derived from baseline aggregates, not produced by a
   single tool call.
2. Show health status (Excellent / Good / Fair / Poor / Critical).
3. Guide next steps (e.g. "drill into the 23 duplicate transaction_ids
   via `/dr-query` with an IN list").

## Examples

### Analyze default financials table
```bash
/dr-anomalies-report
```

Output:
```
🔍 Discovering financials table...
✓ Found financials table: TABLE_ID

📊 Analyzing table TABLE_ID...
  📈 Profiling numeric fields (SUM/AVG/MIN/MAX/COUNT)...
  📝 Profiling categorical fields (distinct + samples)...
  📊 Aggregating per-value counts for duplicate / null detection...
  🧮 Computing findings + severity buckets client-side...
  🔍 Fetching sample records for top findings...
  📄 Generating Excel report...

✅ Report generated: tmp/Anomaly_Report_2026-02-03_143022.xlsx

==================================================
ANOMALY DETECTION SUMMARY
==================================================
Table: TABLE_ID
Total Anomalies: 45
Data Quality Score: 87/100

By Severity:
  Critical: 2
  High: 8
  Medium: 23
  Low: 12

Report: tmp/Anomaly_Report_2026-02-03_143022.xlsx
==================================================
```

### Analyze specific table for critical issues only
```bash
/dr-anomalies-report --table-id TABLE_ID --severity critical
```

### Save to custom location
```bash
/dr-anomalies-report --env app --output tmp/Quality_Check_Feb_2026.xlsx
```

## Data Quality Score

Score ranges from 0-100:
- **90-100** ✅ **Excellent** - Minimal issues, data is reliable
- **80-90** 🟢 **Good** - Minor issues, generally usable
- **70-80** 🟡 **Fair** - Moderate issues, needs attention
- **70** 🟠 **Poor** - Significant issues, requires action
- **<70** 🔴 **Critical** - Major issues, immediate action required

Calculation:
```
Score = 100 - (critical×10 + high×5 + medium×2 + low×0.5)
Clamped to 0-100 range
```

## Adaptive Behavior

### With `--table-id`
- Uses the supplied table directly — no discovery, no name-matching
- Reads the schema and profiles whatever numeric/categorical fields it exposes
- Works on any table, financial or not

### Default (no `--table-id`)
- Lists available tables and picks the financials table by name pattern (else largest)
- Automatically reads the table schema
- Infers field purposes from names and data types
- Uses general data quality rules

### Field discovery
Whichever path resolved the table:
1. Get the full field list (`list_aliased_fields` if aliased, else
   `get_fields_by_id`)
2. Identify numeric fields (for range-band / outlier checks) and categorical
   fields (for frequency / null / duplicate checks) from it
3. For category-aware findings, collect distinct values via the
   distinct-values start→poll tools (`start_distinct_values_by_*` →
   `get_distinct_values_result_by_*`) (fall back to
   sampling rows with `get_data_by_alias` / `get_data_by_id` only if the
   distinct call errors)
4. Run analysis

## Use Cases

### Monthly Data Quality Check
```bash
/dr-anomalies-report --env app --output tmp/DQ_Check_$(date +%Y-%m).xlsx
```

### Pre-Month-End Close Validation
```bash
/dr-anomalies-report --severity critical
```
*Alerts on critical issues that could affect close*

### Department Data Audit
```bash
/dr-anomalies-report --table-id 12345 --severity high
```
*Checks specific department data for issues*

### Exploratory Analysis
```bash
/dr-anomalies-report --table-id unknown_table_id
```
*Discovers what's in an unfamiliar table*

## Output Files

Reports are saved to: `tmp/Anomaly_Report_YYYY-MM-DD_HHMMSS.xlsx`

Each report includes:
- Professional formatting with colors
- Severity-based highlighting
- Embedded sample data
- Statistical analysis
- Investigation queries

## Troubleshooting

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**"No tables found" error**
- Check that authentication succeeded
- Verify you have access to Finance OS

**"Table not found" error**
- Verify the `--table-id` value is correct
- Run `/dr-tables` to see available tables

**No table matches the financials pattern (default path)**
- List the tables you found and ask the user which one to analyze, or have
  them re-run with `--table-id <id>`.

## Related Skills

- `/dr-tables` - List and explore available tables
- `/dr-extract` - Extract validated financial data
- `/dr-reconcile` - Compare P&L vs KPI data

## Performance

- Small tables (< 10K rows): ~30 seconds
- Medium tables (10-100K rows): ~1-2 minutes
- Large tables (100K+ rows): ~5-10 minutes

Scaling handled automatically via pagination and efficient MCP tools.
