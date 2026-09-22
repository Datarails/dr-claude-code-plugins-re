# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin for Datarails Finance OS. It provides skills (`skills/*/SKILL.md`) and commands (`commands/*.md`) that connect to a remote MCP server at `https://mcp.datarails.com/mcp` (configured in `.claude-plugin/plugin.json`). There is no local server code — the MCP server is hosted remotely.

## Critical Rules

**NEVER generate reports, Excel files, or any artifacts without first fetching fresh data from the live Datarails API.** Reports with fake/placeholder data have zero value.

**NEVER hardcode client-specific information in skills or committed files.** Table IDs, field names, and account hierarchies differ per client — every skill **discovers them inline at runtime** (see "Client Data Discovery" below). Never bake them into a skill, a committed config, or a persisted profile file.

**Prefer the engine over local computation for metric values.** When the business-metrics data layer is available (`use_semantic_layer_v2`) and `get_business_metric_data` returns empty for a CALC metric that `list_business_metrics` shows as clean (no `status_info.error_message` / `source_warning`), sweep parameters (`date_end`, `aggregation_period`, `scenario`) before deriving the value from base metrics yourself. The most common cause of an empty response is bucket-end clipping: the engine only emits a bucket when `bucket_end <= date_end`, so a mid-bucket `date_end` silently drops the in-progress period — round `date_end` up to the bucket end. If after the sweep you still need to compute client-side as a fallback, **label it explicitly** in the user-facing output: *"derived from <bases> client-side because get_business_metric_data returned empty for these parameters — not the canonical engine value."* Never present a derived number as if it came from the metrics layer.

## Build & Release

```bash
# Bump version in plugin.json (single source of truth)
#   .claude-plugin/plugin.json  →  "version": "X.Y.Z"

# Publish release — GitHub Actions builds the ZIP automatically
git tag vX.Y.Z && git push origin main --tags
```

## Installation

**Cowork (Claude Desktop):** Browse plugins > Personal > **+** > Add marketplace from GitHub > `Datarails/dr-claude-code-plugins-re`

**Claude Code:** `/plugin marketplace add Datarails/dr-claude-code-plugins-re`

## Architecture

### Data-access layers — prefer the highest one that answers the question

The MCP exposes the same data through three layers (token cost rises down the
list). Always reach for the highest layer that fits:

| Layer | Tools | Use when |
|-------|-------|----------|
| Business metrics (KPI) | `list_business_metrics` (always available) → `get_business_metric_data`*  | Named KPIs — revenue, margin, expenses, budget variance, headcount, ratios |
| Aliased tables (**preferred** for raw data) | `list_aliased_fields`, `get_data_by_alias`, `start_aggregation_by_alias` → `get_aggregation_result_by_alias`, `start_distinct_values_by_alias` → `get_distinct_values_result_by_alias` | A table's aliased fields — friendly names, ~95% fewer tokens. **Note: a table alias does not imply its fields are aliased (real orgs often alias only a few); use the by-id tools for any un-aliased field — see "Client Data Discovery".** |
| Raw by-id (fallback) | `get_fields_by_id`, `get_data_by_id`, `start_aggregation_by_id` → `get_aggregation_result_by_id`, `start_distinct_values_by_id` → `get_distinct_values_result_by_id` | Tables without an alias, or when an alias call fails |

`list_data_models` is the entry point for both raw layers — every entry carries
both the numeric `id` (for the by-id tools) and the `alias` (for the by-alias
tools; empty when a table has no alias).

*`get_business_metric_data` and the other `get_business_metric_*` data tools are
**feature-flag gated** (`use_semantic_layer_v2`, default-deny). `list_business_metrics`
is ungated — use it for discovery, and degrade to aliased/by-id aggregation for the
actual values when the metric-data tools aren't enabled for the org.

**Aggregation vs. pagination (speed):** aggregation (`start_aggregation_by_*` →
`get_aggregation_result_by_*`, non-blocking start→poll, typically seconds, no row
limit) is the default for summaries and totals. Page raw rows (`get_data_by_*`,
≤500/page) only when you need individual records. See "Async fetch — start → poll"
below for the polling contract.

### Server prefix varies by surface — match tools by name, not prefix

Skills and docs here write connector tools as `mcp__datarails-finance-os__<tool>`,
after the `mcpServers` key in `plugin.json`. Other surfaces register the same
server under their own key — **Claude for Excel exposes it as
`mcp__datarails__<tool>`** — so the full prefixed string from a skill body may
match nothing there while the tool itself is present. When resolving or searching
for a connector tool, match on the bare tool name (`start_aggregation_by_id`,
`list_data_models`, …), never on the server prefix, and never conclude a
capability is missing because the prefixed name failed to resolve. (Observed live
2026-08-13: prefixed lookups from a skill body cost several failed searches and
two failed code-execution calls before the bare name matched.)

### Backward compatibility — retired tool names (old → new)

The MCP consolidated its tool surface in v3.0.0. If a user (or an old workflow /
muscle memory from the previous MCP) references a **retired** tool name, silently
map it to the current tool below and proceed — do **not** tell the user the tool
"doesn't exist." The `/dr-*` skill and command names are unchanged, so existing
invocations keep working.

| Retired tool | Current equivalent |
|---|---|
| `list_finance_tables` | `list_data_models` |
| `get_table_schema` | `get_fields_by_id` |
| `get_field_distinct_values` | `get_distinct_values_by_id` (or `_by_alias`) |
| `get_records_by_filter`, `get_sample_records` | `get_data_by_id` (or `_by_alias`) |
| `aggregate_table_data` | `get_aggregated_data_by_id` (or `_by_alias`) |
| `list_semantic_tables`, `get_semantic_table_schema` | `list_aliased_fields` |
| `semantic_query` / `semantic_aggregate` / `semantic_distinct_values` | `get_data_by_alias` / `get_aggregated_data_by_alias` / `get_distinct_values_by_alias` |
| `get_metric_definitions` | `list_business_metrics` |
| `get_metric_detail` / `get_metric_data` / `drill_down_metric` | `get_business_metric_details` / `_data` / `_drilled_down_data` |
| `list_metrics_by_category` / `_by_dimension` / `get_metric_dimension_matrix` | filter the `list_business_metrics` result client-side |
| `profile_table_summary` | `profile_numeric_fields` + `profile_categorical_fields` |
| `detect_anomalies` | (removed) compute client-side from `profile_*` + aggregates |
| `execute_query` | (removed) use `get_data_by_*` advanced filters (or `sql_query` where the org's `mcp_use_llm_sql_tool` flag is on) |

**Deprecated blocking tools (v3.1, async migration).** The four blocking fetch tools
were superseded by the async start→poll pairs and are now hidden from the tool list
but **still callable** — treat a reference to them the same way (map silently, don't
report them as missing):

| Deprecated blocking tool | Current async pair |
|---|---|
| `get_aggregated_data_by_id` | `start_aggregation_by_id` → `get_aggregation_result_by_id` |
| `get_aggregated_data_by_alias` | `start_aggregation_by_alias` → `get_aggregation_result_by_alias` |
| `get_distinct_values_by_id` | `start_distinct_values_by_id` → `get_distinct_values_result_by_id` |
| `get_distinct_values_by_alias` | `start_distinct_values_by_alias` → `get_distinct_values_result_by_alias` |

The `start_*` tools take the **same arguments** as their blocking twins; for distinct
values the `limit` moves to the result tool.

### Aggregation / query API notes

- **Date ranges filter directly — but date values MUST be epoch seconds.** The
  `filters` argument accepts an **advanced** condition tree per field; for a date
  column pass e.g. `{"name": <date_alias>, "values": {"type": "advanced", "val":
  [{"condition": "total_range", "value": ["<start_epoch>", "<end_epoch>"]}]}}`
  (by-alias) or the `{"field_id": <date_id>, …}` form (by-id). In the **ordered**
  conditions (`gt`/`gte`/`lt`/`lte`/`range`/`total_range`) a date value must be
  **epoch seconds passed as a string** (the backend casts per field); calendar
  strings like `"2026-01-01"` are **rejected** — a calendar string in a `gte`
  condition returns an opaque 500, while the identical call with an epoch string
  (`"1767225600"`) succeeds. Never send calendar dates in
  ordered conditions. (You can still put the date in `dimensions` and filter
  client-side if you prefer.) Advanced conditions: `equals`, `dn_equals`, `contains`,
  `dn_contains`, `bw`, `ew`, `gt`, `gte`, `lt`, `lte`, `in`, `range` (exclusive
  between), `total_range` (inclusive between), `is null`.
- **Aggregation guardrails (server-enforced):** a field may not appear in
  both `dimensions` and `metrics` of the same aggregation call; at most **one
  aggregation per field per call** (no SUM + AVG of the same field in one request —
  split into two calls); **SUM/AVG are rejected on Text fields** — use `COUNT`,
  `COUNT_UNIQUE`, `UNIQUE_VALUES`, `MIN` or `MAX` instead, on a field you are
  **not** also grouping by (counting a requested dimension violates the first
  guardrail above and can 500), or pick a numeric sibling. **How a violation surfaces varies per guardrail, not per
  build** — the duplicate-aggregation and text-field shapes return a structured 422,
  while the dimensions/metrics overlap and the calendar-date shape return an opaque
  `internal_server_error` 500 with the cause in a suppressed HTML body. Treat every one of them as a contract violation to fix
  client-side, not a server bug to retry — a 500 here does not mean an outage or an
  old build.
- **Simple value-list filters** still work: by-alias `{"name": <field_alias>,
  "values": [...], "is_excluded": false}`; by-id `{"field_id": <field_id>, "values":
  [...]}`. `is_excluded: true` turns a value list into NOT-IN.
- **Some fields fail per-client** (500 errors). Discover lazily and retry reactively:
  if a dimension/metric field errors, re-inspect the schema for a sibling and retry.
  There is no profile file. Run `/dr-test` if you want the compatibility map up front.
- **Distinct values** come from `start_distinct_values_by_alias` / `_by_id` →
  `get_distinct_values_result_by_alias` / `_by_id` (pass `limit` to the result tool).
  If a distinct-values fetch errors, fall back to sampling rows via `get_data_by_*`
  (`limit=500`, project just the field you need) and dedupe client-side.
- **JWT tokens expire in 5 minutes.** Auto-refreshes for aggregation; manual refresh
  every 20K rows for pagination.

### Client Data Discovery

Every Datarails environment names its financials table and fields differently, so skills can't hardcode them. Each profile-aware skill **discovers what it needs inline, as the first step of its own workflow** — self-contained, with no shared profile file, no separate learn/setup command, and no hooks.

**Why inline — and not a cached profile, a `/dr-learn` dependency, or a hook (all tried, all failed):**

- **Cowork runs in an isolated sandbox** with an ephemeral per-session home (`/sessions/<name>`); the user's workspace folder is mounted but is *not* the cwd. A profile written to `./.datarails/profile.json` lands in the throwaway home and does **not** survive between sessions — a disk cache can't be relied on.
- **Plugin command hooks do not dispatch in Cowork** (confirmed across multiple builds — pure-shell probe left no trace), so harness-level enforcement of a setup step isn't available.
- **Cross-skill / cross-file handoffs get skipped** — "invoke `/dr-learn-v2` first" or "read this shared reference, then proceed" are planning steps Claude routinely optimizes away (PRs #41-44 chronicle four failed prose variants). Inlining the critical discovery in the skill's own workflow is the only reliably-executed form.

Re-discovering on each cold session is also *more correct* than risking a stale cache.

**Session-memory caching (within one conversation):** the first skill that discovers the table/fields/categories carries them forward; later skills in the same conversation reuse them. Each skill's discovery step opens with *"if you already discovered these this conversation, reuse them."*

#### Canonical inline-discovery recipes (maintainer source of truth)

When writing or updating a skill, copy the relevant recipe so heuristics stay consistent. **This doc is the source of truth; the skill inlines the recipe — do NOT make skills `Read` this file at runtime** (that's a handoff the planner skips).

**Raw-tables skills (P&L / financials) — alias-first, by-id fallback:**
1. `list_data_models` → financials table = name (or alias) matches
   `/financial|cube|p&?l|ledger|gl/i`, else largest by row count. Note **both** its
   `id` and its `alias` (alias may be empty). Prefer the alias path when present.
2. Fields — if the table has an alias, `list_aliased_fields(<alias>)`
   (business-friendly aliases); otherwise `get_fields_by_id(<id>)` (capture each
   field's numeric `id` — the by-id tools need ids). **A table alias does NOT mean its
   fields are aliased: real orgs often expose only a handful of aliased fields (e.g.
   ~5 of ~185 on a mapped financials table), and `amount`/`scenario`/account-groups/
   dates are frequently NOT among them. Make the alias/by-id choice PER FIELD, not per
   table — call `get_fields_by_id(<id>)` whenever the aliased set is thin (it returns
   every field with its `id` AND its `alias`); address each field by its alias
   (`*_by_alias` tools) when it has one, else by its numeric `id` (`*_by_id` tools).
   By-id always works — never abandon the query because the alias set is sparse.** Bind
   by case-insensitive match
   on the alias/name: `amount` (numeric: `^amount$`→`transaction_amount`→`value`),
   `scenario` (`^scenario$`→`^version$`), `date` (`reporting_date`→`posting_date`→`^date$`),
   `account_l1` (`dr_acc_l1`→`account_l1`→`account_group_l1`). Ask the user if
   `amount`/`scenario` is unclear.
3. Account categories — `start_distinct_values_by_alias(<alias>, <account_alias>)` (or
   `start_distinct_values_by_id(<id>, <account_field_id>)`), then poll the matching
   `get_distinct_values_result_by_alias`/`_by_id` with the returned handle (pass `limit`
   to the result tool) — see the async-fetch pattern below. If the distinct fetch errors,
   fall back to `get_data_by_alias(<alias>, select=[<account_alias>], limit=500)` (or the
   by-id twin) and dedupe. Match `revenue` `/revenue|sales|income/i`, `cogs`
   `/cogs|cost of goods|cost of sales|direct cost/i`, `opex` `/operating|opex|expense|sg&a/i`.
4. Aggregate — `start_aggregation_by_alias(<alias>, dimensions=[…aliases],
   metrics=[{"field": <amount_alias>, "agg": "SUM"}], filters=[…])` (preferred), or
   `start_aggregation_by_id(<id>, dimensions=[…ids], metrics=[{"field_id": <amount_id>,
   "agg": "SUM"}], filters=[…])`, then poll the matching `get_aggregation_result_by_*`
   with the returned handle (async-fetch pattern below). Scope dates with an **advanced**
   filter (see "Aggregation / query API notes") or by adding the date as a dimension and
   filtering client-side.
5. **Failures are handled reactively, not pre-probed:** if a call 500s on a dimension/
   metric field, re-inspect the Step-2 schema for a sibling account-level field from the
   discovered schema (orgs often carry in-between levels) and
   retry; if an alias call fails, fall back to the by-id twin.

**Async fetch pattern (inline into every skill that fetches aggregates or distinct values):**

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

**Data-scope preamble (inline into every skill that aggregates financial data):**

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Each response returns **exactly one row per requested group** — no subtotal rows and no grand-total row mixed into the `data` list; grand totals arrive in a separate top-level `totals` field beside the rows (`{"data": [...], "totals": {...}}`), computed across **all** groups, not just the returned prefix. **For a grand total, read `totals` — never sum the rows when the response carries `truncated: true`** (summing the returned prefix silently under-counts; dev repro: 474 of 31,455 rows summed to 21% of the true total). **`totals` combines the per-group results rather than re-scanning the rows**, so it is exact exactly when the aggregation is decomposable: SUM (sum of the group sums), COUNT (sum of the group counts), MIN, and MAX. It is **WRONG for AVG** (unweighted mean of the group averages) and **COUNT_UNIQUE** (sum of the per-group distinct counts, so a value recurring across groups is counted once per group) — true average = SUM total ÷ COUNT total (two calls: a field may be aggregated at most once per request); true distinct count = the distinct-values tools. Treat every aggregation type not named exact above — **`UNIQUE_VALUES` included**, whose cross-group de-duplication is unverified (the `COUNT_UNIQUE` behaviour above is evidence the engine may not de-duplicate across groups at all) — as not decomposable: derive it from complete rows or the distinct-values tools, never from `totals`. `totals` is absent on dimension-less aggregations (the single returned row IS the total) and may be absent on responses cached before the rollout (cache TTL ≤ 7 days) — only in those two cases is a total obtained by summing complete (untruncated) rows. Null groups arrive explicitly labeled `[null]` and are real groups; read null counts from that bucket. **Defensive filter:** keep only rows in which **every requested dimension key is present** — a roll-up row *omits* one or more keys entirely, whereas a genuine null is *present* with the value `[null]`. On a correct response this is a no-op; it guards against a stale cached response still carrying legacy subtotal and grand-total rows, each of which equals the whole total and would inflate any sum. When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~50 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. On aggregations the top-level `totals` field is **unaffected by truncation** (computed across all groups, not just the returned prefix) — read grand totals from it instead of re-fetching. Narrow the query (fewer dimensions, more filters, fewer selected columns — or a business metric for a named KPI) and re-fetch **only when the rows themselves are needed** beyond the cap; with `totals` present, a SUM/COUNT/MIN/MAX grand total never requires a re-fetch or chunking by dimension (AVG, COUNT_UNIQUE and UNIQUE_VALUES never read `totals` — true average = SUM total ÷ COUNT total from two calls; true distinct count = the distinct-values tools). A truncated response **without** `totals` (pre-rollout cache) cannot answer a grand-total question from its prefix. Re-run the aggregation **once** — a fresh run may miss the stale entry and return `totals`. If the re-run still carries no `totals`, stop re-running and fall back to narrowing or chunking by dimension until the responses are complete, then sum those rows. Never total the prefix.

**KPI honesty (inline into every skill/agent that renders KPI cards, dashboards, or executive summaries):**

> **Render only KPIs you can source.** A KPI may come from (a) the org's metric catalog — `list_business_metrics` (ungated) for discovery; the `get_business_metric_*` data tools are feature-gated and may be absent, and USER-kind metrics often return empty — or (b) aggregation over the discovered P&L grain (revenue, expense buckets, gross/operating margin when COGS/OpEx-like buckets exist). SaaS/unit-economics metrics (ARR, MRR, churn, LTV, CAC, burn, runway, NRR) are **not** derivable from a P&L table — include them only if discovered as populated metrics; otherwise omit the card/slide entirely. Never render a placeholder, estimate, or fabricated value for a KPI you could not source.

**Metric-v1 skills (`__internal`, business-metrics / aliased layer):**
Run the catalog calls in parallel — `list_data_models(has_alias=true)` and
`list_business_metrics` (~5s) — and use the result directly; cache in session.
(`list_aliased_fields` requires an `alias` argument, so it can never join a blind
parallel fan-out — call it per table once the alias is known.) Metric values via `get_business_metric_data`; drill via
`get_business_metric_drilled_down_data` (both `use_semantic_layer_v2`-gated — the dev
MCP has the flag on).

#### Status: migration complete

Every profile-aware skill and agent now discovers inline. `/dr-learn`, `/dr-learn-v2`, the `./.datarails/profile.json` cache, and `config/profile-schema.json` have all been **removed**. There is no profile file anywhere — do not add one or reintroduce a learn/setup command. When writing a new skill, inline the recipe above; never depend on a saved profile or a sibling skill to discover for you (Cowork skips those handoffs).

### DR.GET authoring contract (single-sourced, inlined)

Any skill that can be asked to write live DR.GET formulas into a workbook
must carry the **"DR.GET Formulas — Authoring Contract"** block inline —
same rationale as the discovery recipes above: a runtime "read the shared
reference first" handoff gets skipped in Cowork, and a session without the
contract in context invents DR.GET syntax by analogy with the MCP call it
just made.

The block is **single-sourced**:

- Canonical copy: `docs/internal/drget-authoring-contract.md` (internal-only;
  stripped at publish — the skills carry the inlined copies to public).
- Inlined verbatim in every Excel-writing skill, ending with the
  `<!-- end:drget-authoring-contract -->` marker.
- **Edit the canonical file, never an inlined copy**, then run
  `python3 tools/sync-drget-authoring-contract.py --write` to re-stamp all
  copies. CI runs the check mode and fails the advisory job on any drift.
- Adding a new Excel-writing skill: add it to `TARGET_SKILLS` in the sync
  script, insert the block after the skill's brand-styling section, and run
  `--write`.

get-formula remains the full authority for formula workbooks (parameter
cells, validated values, layouts); the contract is the minimum that must be
in context everywhere else.

### Excel Context Contract

> **Ships publicly.** The Excel Add-In bridge skills this contract governs —
> `datarails-excel-agent` and `excel-context` — are promoted to the public mirror like
> any other skill. The contract only *applies* where a live Excel Add-In bridge exists;
> on a surface without one the probe fails as a normal detection result and finance
> skills fall through to their MCP path.

> **Terminology — "agent" means the `datarails-excel-agent` skill, NOT the MCP connector.**
> Throughout these skills, **"the agent" / "agent bridge" / "agent refresh" / "agent
> drill-down" / "agent commands" / "agent mode"** all refer to the **`datarails-excel-agent`
> skill**, which drives the **Datarails Excel Add-In** via the hidden `__dr_agent` bridge
> sheet (commands like `refresh_ribbon`, `drilldown_list`, `add_function_by_id`,
> `agent.get_session`). It is **NOT** the `datarails-finance-os` MCP connector (the FinanceOS
> REST API: `start_aggregation_by_alias`, `get_fields_by_id`, etc.). When a skill says "fire the
> agent" / "refresh via the agent", use the add-in bridge — never the MCP connector, and never
> native Excel. The split is by **target**, not by whether Excel is open: the bridge acts on
> the **open workbook**; the MCP connector answers **org-data questions** — which
> tables/models/fields/metrics exist, aggregations, raw queries, distinct values, profiling,
> org users, FX rates — and it remains the correct tool for those questions **even while a
> workbook is open**. The bridge is not a data-query engine; the connector is not a workbook
> actuator.

Any skill that offers Excel-context behavior (in-sheet enrichment, agent refresh,
drill-down) **must delegate to `excel-context`** rather than implementing
Excel context detection inline. This contract applies globally; it overrides
inline logic in individual skill files.

**Workbook operations** route to the add-in bridge — NEVER native Excel, never the connector.
In Excel context, when the user asks for a Datarails operation, satisfy it by
firing the **agent bridge command** through `datarails-excel-agent` — never by
driving Excel directly (no `Excel.run` `calculate()`/`calculateFull()`, no
manual recalc, no formula re-write, no simulated ribbon click). A native Excel
recalc does **not** pull fresh Datarails data, does **not** resolve DR widgets,
and silently produces stale/`#BUSY!`/wrong results. The add-in owns these
operations; the bridge is the only correct path **for workbook operations**.

| User intent (in Excel context) | Bridge command (via `datarails-excel-agent`) | Do NOT |
|---|---|---|
| "Refresh" / "recalculate" / "update the numbers" / "pull latest" | `refresh_ribbon` (or `refresh_selected_cells_ribbon` / `refresh_table_table_ribbon`) | Excel `calculate()` / F9 / re-typing formulas |
| "Drill into / break down this cell" | `drilldown_list` / `drilldown_by_pivot` | Manually querying via MCP when a bridge + DR cell exist |
| "What does this cell return" | `agent.evaluate_drget` / `agent.read_range` | Reading the cached cell value as truth |
| "Add/insert this function" (place one widget at a cell) | `add_function_by_id` | Hand-typing a `=DR.GET(...)` string as a substitute for the insert command |
| "Connect / submit / publish" | `connect_file` / `submit` / `publish_to_dashboard` | Any native-Excel equivalent |

**Org-data questions route to the MCP connector — even in Excel.** Route by the
**target** of the request, never by whether a workbook is open:

| Request class (workbook open or not) | Route | Examples |
|---|---|---|
| **Workbook state & actions** — refresh/recalculate, drill a cell, insert a DR.GET / dynamic range, read or evaluate cells in *this* workbook, list functions/sheets *in this workbook*, select/activate, publish, connect, submit | **Bridge** (`datarails-excel-agent` via `execute_office_js`) — never native Excel, never the connector | "refresh", "what's behind B4", "insert the Value function at D2", "publish this range" |
| **Org / server data** — list data models/tables, list/inspect fields, aggregated queries, raw row queries, distinct values, business metrics, profiling, org users, currency rates | **MCP connector** (`datarails-finance-os`) — **even when a workbook is open** | "list my dr models", "total OpEx by month 2025", "distinct values of Legal Entity" |
| **Hybrid** — derive/verify from server data, then write it to the sheet | Connector for the data legs; bridge for every workbook write **plus the mandatory refresh** | "find 2025 revenue in my data and insert a DR.GET for it" |

**Tie-breakers.** If the request names a cell, range, sheet, or formula, or asks to
change what is in the workbook → bridge. If the answer would be identical with the
workbook closed → connector. "Refresh", "recalculate", "drill down", "insert",
"evaluate this cell", "publish", "connect", "submit" are **never** connector calls —
the connector cannot see or touch the workbook. "What tables/models/fields do I have",
"total X by Y", "distinct values of Z" are **never** bridge calls — the bridge cannot
answer them. Watch the near-miss pair: *"list functions in this workbook"* = bridge
`agent.list_functions`; *"list my Datarails models/tables"* = connector `list_data_models`.

If unsure whether a request maps to a bridge command, call `agent.list_commands`
and match — do not fall back to native Excel; if it matches no bridge command and
is a data question, it belongs to the connector.

**Transport:** these bridge commands are **not MCP tools and not callable functions** — each
is JSON written to the `__dr_agent` sheet and read back, done by running Office.js via the
**`execute_office_js`** tool (see `datarails-excel-agent` §Transport). "Call `agent.get_session`"
≡ "run the bridge probe through `execute_office_js`". Never look for an MCP tool named after a
command, and never use the `datarails-finance-os` connector to perform an Excel operation.

**MANDATORY: writing DR.GET formulas + refresh is one atomic step.** This applies
to **any skill and any write path** — `add_function_by_id`, `create_dynamic_range`,
**or a skill that writes `=DR.GET(...)` formulas directly into cells** (e.g.
`/dr-get-formula`, in-sheet enrichment). Whenever DR formulas land in a workbook
**in Excel context**, you **must** fire a refresh through the agent
(`refresh_selected_cells_ribbon` for the written cells, or `refresh_ribbon` for a
batch) **before reading or reporting any value**. A freshly written DR.GET shows
"Loading…" / `#BUSY!` / `#N/A` until refreshed — never present that as the value,
and never satisfy the refresh with native Excel recalc. This is the most common
Excel-context mistake. (Connector: `excel-context refresh-after-insert`.)

**MANDATORY: confirm the LAYOUT before building any multi-period grid.** Any skill about to
write an analysis grid spanning two or more scenario sides (actual / plan / forecast) across
periods **must ask the user which layout they want**, in the same clarifying turn as scope and
granularity, before pulling data and before writing a cell. Offer **side by side** (`Actual │
Plan` column pair per period, variance columns at the far right — recommend this), **stacked
blocks**, or **totals only**; on a deferred answer use side-by-side and say so. In **enrichment
mode** the user's existing structure wins. Layout is formula topology, not cosmetics — changing
it later means rebuilding the grid, and a side-by-side grid's two-columns-per-period stride
breaks cross-sheet links into single-scenario source blocks (`datarails-excel-agent`
§7). Reference implementation: `forecast-variance` Step 2b.

**MANDATORY: confirm the ACCOUNT LEVEL and the DESIGN before building an account-grouped
report.** Any skill about to write a P&L or other account-grouped grid **must ask which level
of the account hierarchy each row represents**, and **where the design comes from**, in the
same clarifying turn as scope, granularity and layout — before pulling data and before writing
a cell. Default the level to the L1.5-style field the org exposes and **offer the rest of the
discovered ladder with the row count each would produce**; never present a hardcoded `L1`/`L2`
pair, because the ladder is per-org (some carry `L0`…`L3`, some a half-level, some neither) and
hardcoding it is the client-specific assumption the Critical Rules forbid. Offer the design as
Datarails default styling, one of the **shipped Datarails Template Library looks** (the
`ocean` family or `genesis` — extracted into `get-formula/references/report-designs.md`), mirroring a sheet
**already open in the workbook**, or plain. On a deferred answer take both defaults **and say
which you took**. Level is not cosmetic — it sets the row set, the
DR.GET row dimension, and which subtotals are even derivable, so a wrong pick is a rebuild; and
a subtotal whose membership is not derivable at the chosen level is **omitted and named**, never
`SUM`-ed over a guess. **Never send the user off to open, download or fetch a
file** — they are acting on the workbook they have open, which is why the template looks ship
as committed presets rather than being read from the org at runtime (`download_file` cannot
fetch a filebox document anyway). Never reconstruct a template's design from its name: if a
requested look is not a preset, say so and offer the closest one. A preset carries its own
**geometry** as well as its formatting, so the DR.GET reference map is derived from the chosen
preset — the one sanctioned exception to a fixed cell contract, safe only because the preset
states the whole grid. Offer the looks by name but **pick the geometry variant yourself** from
the report type; do not make the user choose between near-identical names. Reference implementation: `get-formula` Step 6.5 +
`references/report-designs.md`.

**MANDATORY: elaborating on DR-backed data → offer a drill-down.** When the user wants
to go deeper on a figure or section — *"explain / elaborate / break down / dig into / what
makes up / why is X / show me the detail"* — and you are in Excel context, first determine
whether the figures in scope are **DR formula cells**: read them with `agent.get_selection`
/ `agent.read_range` and check the returned formula text / `data.sources[]` for a DR function
(`DR.GET`/`DR.QTD`/`DR.YTD`/`DR.MTD`/…). **If they are DR cells, you MUST offer a drill-down**
— present the drillable cells/rows and ask which to drill, then run `drilldown_list` /
`drilldown_by_pivot` through the agent. Drill-down is the **default elaboration path** for
DR-backed figures: do not just narrate the cached value or silently re-derive via the
`datarails-finance-os` MCP connector when a live drill is available. (Connector:
`excel-context drilldown`.) **Checklist:** before finalizing any data-elaboration answer
in Excel context — DR cells in scope? drill-down offered? If yes-then-no, add the offer.

**Four mandatory delegation points:**

| Point | When | Delegate to |
|-------|------|-------------|
| Guard | Step 0 — before any data pull (probe Excel context + login) | `excel-context guard` |
| Refresh | Step 0b — after guard confirms Excel context | `excel-context refresh` |
| Refresh after DR.GET insert | Immediately after each `add_function_by_id` call (or batch) | `excel-context refresh-after-insert` |
| Drill-down | Final step — after analysis written to sheet | `excel-context drilldown` |

**Rules enforced by the connector** (bridge command IDs, not `agent.*` aliases):

- `agent.get_session` success is the **only** authoritative Excel context signal.
  Never infer context from user wording.
- `isConnected` is **not** a guard condition. Refresh, DR-formula reads, evaluate
  **and every `drilldown_*`** work on an unconnected workbook. `connect_file` is
  required only for `create_dynamic_range`, and requires explicit user confirmation
  — never called automatically. Never gate a drill on `isConnected`, and never tell a
  user drill-down is unavailable because the workbook is unconnected.
- **A successful `drilldown_*` returns `data: null` and writes a new worksheet** —
  an empty payload is success, not failure. Read the result off the created sheet; row 1
  echoes the source cell's filter context and serves as the citation in place of
  `data.sources[]` (`datarails-excel-agent` §6). The drill-hazard protocol
  (confirm, snapshot, repair, keep-or-delete) lives in `/dr-drilldown` Step 0.
- **Probe before declaring any bridge capability unavailable, and never file a bug on a
  bridge command** until you have (a) run it, (b) re-read the fetched manual's catalog row
  for it, and (c) retried with the manual's exact params — same spirit as the server-prefix
  note above: one failed lookup is not a missing capability. An empty payload is not an error
  either (see the drill rule above). If a probe contradicts a claim you already made to the
  user, correct it in one line and move on.
- `refresh_ribbon` is offered once per invocation and only when Excel context
  is confirmed. Never re-asked on follow-up questions in the same session.
- `refresh-after-insert` is **specific to DR.GET formula insertion** — fires
  silently (no user prompt) after `add_function_by_id`, never for raw-value
  writes or text commentary.
- `drilldown_list` fires only in enrichment mode (DR formula cells exist —
  `DR.GET`/`DR.QTD`/`DR.YTD`/etc., any DR function). Cold-question mode (raw API
  values from the MCP aggregation tools) always skips drill-down.

**Inline Excel-context logic is sanctioned in two forms — audit finding L12 is
retired, its premise reversed by live evidence.** L12 tracked `forecast-variance`'s
inline Step 0/0b guard as debt awaiting migration to the delegation anchors. Two
2026-08-13 sessions on the Claude-for-Excel surface showed the delegation model is
the weaker one there: a runtime `read_skill` hop into a `user-invocable: false`
connector is exactly the kind of handoff that never happens when no skill has
routed yet (the same reason the DR.GET contract is inlined rather than referenced
— see above). The sanctioned forms:

- **A full inline Step 0 workflow** for skills whose behavior *changes* in Excel
  context: `forecast-variance` (the original, now the reference implementation)
  and `get-formula` (its Step 0/7-A/8-A, modeled on it).
- **The synced Excel-context routing preamble** for file-producing skills that
  cannot deliver in Excel context and must detect + decline + route honestly:
  canonical copy at `docs/internal/excel-context-preamble.md`, inlined verbatim
  into the 8 report/workbook generators, kept byte-identical by
  `tools/sync-excel-context-preamble.py` (CI-checked; edit the canonical file,
  never an inlined copy, then `--write`).

`excel-context` remains the delegation target where a skill is already
running and wants the guard/refresh/drilldown patterns mid-flow. What no skill may
do is invent a *third* variant: new skills take the preamble (file producers) or
copy the `forecast-variance` Step 0 shape (Excel-behavior skills), never a bespoke
probe.

### Plugin Content Types

- **Skills** (`skills/*/SKILL.md`): Full-featured workflows for Claude Code. Each has frontmatter with `allowed-tools` listing which MCP tools it can use. Reference: `skills/intelligence/SKILL.md`.
- **Commands** (`commands/*.md`): Lightweight Cowork-friendly commands (no CLI dependencies).

(The plugin ships no `agents/*.md` — the eight former agents were 1:1 mirrors of
same-named skills that had drifted into weaker copies (missing tools, dropped
thresholds) and were removed in the 2026-08 duplication cleanup. Autonomous runs
delegate to a general-purpose agent that invokes the skill, keeping one source
of truth for every workflow's guards.)

### Adding a New Skill

1. Create `skills/<name>/SKILL.md` with frontmatter (name, description, allowed-tools, argument-hint)
2. Include: inline Client Data Discovery as the workflow's first data step (copy the canonical recipe above), Workflow phases, Execution Instructions, Troubleshooting
3. No registration step needed — skills are auto-discovered from the `skills/` directory

## Git Guidelines

**Commit:** Skills, commands, agents, plugin config, schemas, docs (`docs/guides/` for public guides; `docs/internal/` for internal-only analysis — the latter is stripped at publish), notebooks.

**Never commit:** output files (`tmp/`), credentials, `.env.local`.

## Output Files

All generated artifacts (Excel, PowerPoint, CSV, diagnostics) go to `tmp/` (gitignored).

## Authentication

OAuth 2.0 + PKCE at the MCP transport layer. No `/dr-auth` command exists — auth happens when the connector is first connected.

- **Cowork:** Install the plugin via Browse plugins > Personal tab. Auth happens automatically when the connector is first used.
- **Claude Code:** `/plugin marketplace add Datarails/dr-claude-code-plugins-re` then `/plugin install datarails-financeos@datarails-marketplace`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Tools not available | Connect via Connectors UI. Do NOT suggest bash workarounds or mention "MCP" to Cowork users. |
| "Not authenticated" | Disconnect and reconnect via Connectors UI |
| Skill picked the wrong table/field | Skills discover the financials table + fields inline; if it guesses wrong, tell it which to use and it continues. There is no profile to build. |
| Field fails in aggregation | Skills retry a schema sibling automatically (reactive fallback). `/dr-test` reports the full field-compatibility map if you want it up front. |
| Slow extraction | Normal for pagination (~90 rec/sec). Use aggregation for summaries (~5s). |
