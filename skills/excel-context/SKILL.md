---
name: dr-excel-context
description: |
  Connector / guard for running Datarails finance skills in an Excel context.
  Centralizes Excel-context detection (is a workbook open with the add-in bridge
  available?), the refresh / refresh-after-insert / drill-down patterns, and the
  financial-context → agent-command mapping. Finance skills delegate here at Step 0
  (guard) and for refresh/drill instead of implementing Excel-context logic inline.
  It ORCHESTRATES the datarails-excel-agent bridge ("the agent") — it does not
  replace it, and it is not the datarails-finance-os MCP connector. Invoke directly
  to check connection/bridge state, or run a guard / refresh / refresh-after-insert /
  drilldown. Use whenever a skill needs "am I in Excel, and how do I refresh or
  drill through the add-in?"
user-invocable: true
allowed-tools:
  - Read
  - execute_office_js
argument-hint: "[guard|refresh|refresh-after-insert|drilldown] [--cells \"Sheet1!A1,Sheet1!B2\"] [--rows \"<label> Δ$X (Y%),...\"] [--enrichment-mode]"
---

# Datarails Excel Context — Connector Skill

Single source of truth for Excel-context detection, financial context → agent
command mapping, and the four standard Excel-agent integration patterns
(guard / refresh / refresh-after-insert / drilldown).

Finance skills delegate here instead of implementing context detection inline.

## Four invocation modes

| Mode | Call when | What it does |
|------|-----------|-------------|
| `guard` | First thing in any skill (Step 0) | Probe `agent.get_session`; confirm Excel context + login. Does **not** gate on `isConnected` (see Connection requirement) |
| `refresh` | After `guard` confirms Excel context | Offer a Datarails data refresh before pulling. Works on unconnected workbooks |
| `refresh-after-insert` | Immediately after `add_function_by_id` inserts a `=DR.GET(...)` formula | Refresh the inserted cell(s) so values populate instead of showing "Loading..." |
| `drilldown` | After writing analysis to sheet | Drill-down menu for high-variance rows; invokes `drilldown_list` on selection (requires `isConnected`) |

---

## How to run any command (transport)

Every command in this skill is a **bridge command**, run by executing Office.js via the
`execute_office_js` tool against the `__dr_agent` sheet (write request → poll response) —
see `datarails-excel-agent` §Transport + §2/§3. **None of these are MCP tools**, and none
are satisfied by native Excel recalc or by the `datarails-finance-os` connector. If there is
no `execute_office_js` / Office.js tool, you are not in a live Excel context → file-output mode.

## Financial context → agent command reference

Use this table to pick the right command for each financial operation. Always
call `agent.list_commands` at session start to verify a command is available on
the current add-in version before issuing it.

### Session and connection

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| Detect Excel context / who is signed in | `agent.get_session` | — | COM: check `isConnected`; Flex: check `isLoggedIn` |
| Detailed connection info (filebox, env) | `agent.get_connection_info` | — | Returns `fileboxId`, `environment`, `userName` |
| Connect workbook to Datarails | `connect_file` | — | **Mutating — requires explicit user confirmation first** |

### Data freshness

| Financial context | Command | Key params | Typical duration |
|---|---|---|---|
| Refresh full workbook before analysis | `refresh_ribbon` | — | 30–300 s |
| Refresh specific P&L range only | `refresh_selected_cells_ribbon` | `sheetName`, `cellAddress` | 30–300 s |
| Refresh a single table widget | `refresh_table_table_ribbon` | `sheetName`, `cellAddress` | 30–300 s |

Set `timeoutMs: 600000` (10 min) for all refresh commands — real workbooks
commonly take 30–120 s. Never abort while status is `running`.

### Reading and explaining figures

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| Explain what a cell / range contains | `agent.read_range` | `sheetName`, `cellAddress` | Returns values + `data.sources[]` — **must cite sources for every figure** |
| Evaluate what a DR.GET formula returns | `agent.evaluate_drget` | `sheetName`, `cellAddress` | In-cache: < 1 s; set `timeoutMs: 10000` |

### Variance drill-down

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| Drill into a P&L line item (list) | `drilldown_list` | `sheetName`, `cellAddress` | Enrichment mode only — cell must be a DR formula (DR.GET/QTD/YTD/MTD/…, any DR function) |
| Drill into a variance by dimension pivot | `drilldown_by_pivot` | `sheetName`, `cellAddress` | Enrichment mode only |
| Drill into a variance using saved pivot | `drilldown_by_pivot_favorites_*` | `sheetName`, `cellAddress` | Variant of pivot drill-down |

Set `timeoutMs: 180000` (3 min). Only fire on DR formula cells (DR.GET/QTD/YTD/MTD/…,
any DR function) — never on raw API values written by `get_aggregated_data_by_alias`.

### Function widgets (DR.GET)

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| List function widgets / org catalog | `agent.list_functions` | `page?`, `pageSize?` | COM: org-wide catalog (paginated). Flex: workbook instances. **Always paginate — see pagination rule below.** |
| Insert a DR.GET function into the sheet | `add_function_by_id` | `functionId?`, `functionName?` | Use `id` from list response as `functionId`; or pass `functionName` for case-insensitive resolve |

**`agent.list_functions` pagination rule:** Orgs can have 100+ functions.
Always fetch with `pageSize: 100` (max). Check `totalPages` in the first
response and loop — `page: 2`, `page: 3`, … — until all pages collected.
Never present a partial list to the user.

```
// Pseudocode
page = 1; all = []
do:
  r = agent.list_functions(page=page, pageSize=100)
  all += r.data.functions
  page++
while page <= r.data.totalPages
```

### Dynamic ranges

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| List dynamic ranges in this workbook | `agent.list_dynamic_ranges` | — | Returns `id`, `name`, `suppressZeros`, `hasForecastModule` |
| Browse available dynamic range schemas | `agent.list_dynamic_range_schemas` | — | Returns `id`, `name`, `fieldCount`, `fields[]` |
| Create a live auto-updating table | `create_dynamic_range` | `schemaId`, `sheetName`, `cellAddress` | COM only. Min 20 rows. Columns must match `schema.fieldCount` |

### Publishing and submission

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| List dashboards to publish to | `agent.list_dashboards` | — | Call before `publish_to_dashboard` to get `dashboardId` |
| Publish analysis range to a dashboard | `publish_to_dashboard` | `dashboardId` or `dashboardName`, `sheetName`, `cellAddress` | Set `timeoutMs: 180000` |
| Submit an approved budget | `submit` | — | **Mutating — requires explicit user confirmation first** |

### Navigation and diagnostics

| Financial context | Command | Key params |
|---|---|---|
| Activate a sheet | `agent.activate_sheet` | `sheetName` |
| Select a range | `agent.select_range` | `sheetName`, `cellAddress` |
| List sheets in workbook | `agent.list_sheets` | — |
| Get user's current selection | `agent.get_selection` | — |
| Ping the bridge (health check) | `agent.ping` | — |
| Discover all available commands | `agent.list_commands` | — |

### Mutating command confirmation rule

Before issuing any mutating command (`connect_file`, `submit`, `create_dynamic_range`,
`add_function_by_id`, `publish_to_dashboard`), always show the user what will
happen and wait for explicit confirmation. The add-in will NOT prompt — confirmation
is the caller's responsibility.

---

## Detecting Excel context

Excel context is **active** if and only if `agent.get_session` succeeds (per the
`datarails-excel-agent` skill, §6 session probe).

**Never infer context from user wording alone** ("I'm in Excel", "the workbook is
open"). The authoritative check is the live probe.

- `agent.get_session` returns successfully → Excel context **active**
- Any error, tool-not-found, or bridge sheet missing → Excel context **absent**

---

## Mode: guard

Verify Excel context and confirm the workbook is connected to Datarails. Block
analysis on disconnected workbooks.

### Steps

1. **Probe** — call `agent.get_session` (per `datarails-excel-agent` skill §6).

2. **On failure** (any error, tool unavailable):
   - Excel context is absent.
   - Return `excel_context: false` to the calling skill.
   - The calling skill must fall back to file-output mode (generate `.xlsx` /
     `.pptx`). Do not proceed to `refresh` or `drilldown` modes.
   - Do not call `connect_file`.

3. **On success** — read `isLoggedIn` (Flex transport) or treat COM as
   authenticated if session returned without error.

4. **If not logged in (Flex only):**
   Tell the user:
   > *"You are not signed in to Datarails in this workbook. Please sign in
   >  via the Datarails add-in and re-run."*
   Stop. Do **not** call `connect_file` here.

5. **If logged in / COM session active:**
   Return `excel_context: true`. The calling skill continues.

> **`isConnected` is NOT a guard condition.** Many commands (refresh, DR.GET
> insert, evaluate, read) work on unconnected workbooks. Only
> `create_dynamic_range` and `drilldown_*` require `isConnected: true`.
> Check connection **at the call site** for those commands only — see
> §Connection requirement below.

---

## Connection requirement

> **`isConnected` is a COM-only field.** Flex sessions expose `isLoggedIn`, not
> `isConnected`, and have no connection gate — on Flex, skip this whole section
> (a logged-in Flex session can run all commands below). The rule here applies
> **only when `agent.get_session` returned an `isConnected` field** (COM).

On COM, `isConnected: true` is required only for these commands:

| Command | Why |
|---|---|
| `create_dynamic_range` | Writes to a filebox-linked range |
| `drilldown_list` | Resolves drill data via filebox context |
| `drilldown_by_pivot` | Same |
| `drilldown_by_pivot_favorites_*` | Same |

All other commands — including `refresh_ribbon`, `add_function_by_id`,
`agent.evaluate_drget`, `agent.read_range` — work on **unconnected** workbooks.

**Before calling any command in the table above (COM only)**, check
`isConnected` from `agent.get_session`. If the field is present and `false`, ask:
> *"This operation requires the workbook to be connected to Datarails. Should
>  I connect it now with `connect_file`?"*

Wait for explicit "yes". User declines → tell them the specific operation is
unavailable and stop; do not block the rest of the session. If the session has
no `isConnected` field (Flex), do not prompt — proceed.

---

## Mode: refresh

Offer to refresh Datarails data from the server before the analysis pull.

### Precondition

`guard` must have returned `excel_context: true` in this session.
Never call `refresh` if `guard` was skipped or returned `excel_context: false`.

### Steps

1. Ask once per skill invocation:
   > *"Should I refresh data from Datarails before pulling? (Recommended if
   >  you haven't refreshed today.)"*

2. User confirms → call `refresh_ribbon`. Set `timeoutMs: 600000`.
   Wait for terminal status (`done` / `failed`) before continuing to the data pull.

3. User declines → skip, continue.

4. **Do not re-ask** if already asked earlier in this invocation.

---

## Mode: refresh-after-insert

Refresh the cells that just received a `=DR.GET(...)` formula via
`add_function_by_id`. Without this, the inserted cells display "Loading…" or
`#N/A` until something else triggers a refresh — the user sees a broken
formula instead of the resolved value.

**Scope:** This mode is **specific to DR.GET formula insertion**. Do not use
it for other write paths (raw API values written by `get_aggregated_data_by_alias`,
text commentary, headers). Those cells don't need a server roundtrip — only
DR.GET formulas do.

### Preconditions

1. `guard` returned `excel_context: true` in this session.
2. `add_function_by_id` was just called and the response had `status: "done"`.
3. The cell address where the formula landed is known (`add_function_by_id`
   response includes `sheetName` + `cellAddress` of the inserted formula).

### Steps

1. Build the inserted-cell address(es) from the `add_function_by_id`
   response(s). Group by sheet:
   ```
   Sheet1!A1, Sheet1!B2, Sheet2!C5  →  { Sheet1: "A1,B2", Sheet2: "C5" }
   ```

2. **Single cell or one sheet, ≤ 20 cells:** call
   `refresh_selected_cells_ribbon` with `sheetName` + `cellAddress`. Set
   `timeoutMs: 600000`. Wait for terminal status.

3. **Many cells across multiple sheets, or > 20 cells:** call
   `refresh_ribbon` instead (whole-workbook refresh). Same `timeoutMs`. One
   call is cheaper than many targeted ones once the count grows.

4. After refresh terminal status, verify the cell holds a value (not
   "Loading…" or `#N/A`) via `agent.read_range` if the user needs proof
   before continuing.

### Skip conditions

- The inserted formula resolves from cache instantly (rare — only when the
  exact `(functionId, fieldName, rowMember, dim*)` tuple was already loaded).
  When unsure, refresh — it's idempotent.
- The caller used `agent.evaluate_drget` instead of inserting a formula —
  evaluate already auto-fetches the value, no refresh needed.

### Do NOT

- Re-prompt the user for refresh confirmation here — they already asked for
  the formula to be inserted; refresh is the silent completion step.
- Call this for non-DR.GET writes.
- Skip this when batch-inserting many DR.GETs — cells will all stay in
  "Loading…" state until refreshed.

---

## Mode: drilldown

Present a drill-down menu, then invoke `drilldown_list` / `drilldown_by_pivot` on the
rows the user selects.

### When to enter this mode

Two entry points:
1. **Post-analysis** — after a skill writes variance/analysis alongside DR cells (the
   classic flow): offer drill on the high-variance rows.
2. **Elaboration request** — whenever the user wants to go deeper on a figure or section
   (*"explain / elaborate / break down / dig into / what makes up / why is X / show the
   detail"*) and the figures in scope are **DR formula cells**. This is the **default way
   to elaborate on DR-backed data** — prefer it over narrating the cached value or
   re-deriving via the `datarails-finance-os` MCP connector.

**Detecting DR cells in scope:** read the relevant cells with `agent.get_selection` /
`agent.read_range` and inspect each cell's `formula` / `data.sources[]`. A `DR.GET`/`DR.QTD`/
`DR.YTD`/`DR.MTD`/… formula (or `sources[]` carrying a DR widget ref) ⇒ drillable. If none of
the figures are DR cells, this mode does not apply (fall back to MCP/file analysis).

### Preconditions — both must hold

**1. Excel context confirmed.** `guard` returned `excel_context: true` in this
session.

**2. DR formula cells in scope.** The figures to drill are DR formula cells
(DR.GET/QTD/YTD/MTD/…, any DR function) — confirmed by reading their `formula` /
`data.sources[]` (see "Detecting DR cells in scope" above). This holds in two cases:
the parent skill ran in **enrichment mode** (added commentary alongside existing DR
cells), **or** the user's workbook already contains DR cells and they want to elaborate.

In **cold-question mode** (sheet was empty; skill wrote raw API values from
`get_aggregated_data_by_alias`), `drilldown_list` cannot act — it targets DR formula
cells, not raw values. Skip and tell the user:

> *"Drill-down is not available — data was written as raw values, not DR
>  formulas. Open a workbook that has DR formula cells and re-run the skill
>  in enrichment mode to enable drill-down."*

### Steps

1. The calling skill provides the analyzed rows with their Δ$ and Δ% figures.
   Filter to rows where |Δ%| > 10% or flagged unfavorable.

2. Emit the **Drill-Down Menu** block in chat:
   ```
   📋 Drill-Down Menu — rows with |variance| > 10%
     1. <Row label>  Δ$X.XM  (ΔY%)
     2. <Row label>  Δ$X.XM  (ΔY%)
     ...
   ```
   If no rows exceed the threshold:
   > *"No rows exceed the 10% threshold — no drill-down needed."*

3. Ask:
   > *"Which rows would you like me to drill into for a cell-level breakdown?
   >  I'll call `drilldown_list` on each selected row."*

4. Wait for the user's selection. For each selected row, call `drilldown_list`
   with `sheetName` + `cellAddress` of that row's DR.GET cell. Set
   `timeoutMs: 180000`. Do not drill automatically.

---

## Integration pattern for finance skills

Replace inline Excel-context logic in a finance skill SKILL.md with these three
anchors. Finance skills should not re-implement guard, refresh, or drilldown
logic — they delegate here.

### Anchor A — Step 0: guard (always first)

```
### Step 0 — Excel context guard

Run the **guard** mode from `/dr-excel-context`:
- Returns `excel_context: false` → switch to file-output mode (.xlsx / .pptx).
- Returns `excel_context: true, connected: true` → continue to Step 0b.
```

### Anchor B — Step 0b: refresh

```
### Step 0b — Data refresh

Run the **refresh** mode from `/dr-excel-context`.
(Only reached if guard returned excel_context: true.)
```

### Anchor B2 — after `add_function_by_id`: refresh-after-insert

```
### Step N — Refresh inserted DR.GET formulas

After each successful `add_function_by_id` call (or after a batch),
run the **refresh-after-insert** mode from `/dr-excel-context`, passing
the inserted cell addresses. Without it the cells stay on "Loading…".
Only run this for DR.GET formula insertion — not for raw API value writes.
```

### Anchor C — final step: drilldown (enrichment mode only)

```
### Step N — Drill-down

After writing commentary to the sheet, run the **drilldown** mode from
`/dr-excel-context` with the analyzed variance rows.
Applies only in enrichment mode — see connector skill for cold-question gate.
```

---

## What this skill does NOT do

- Pull FinanceOS data — that is the calling finance skill's job.
- Write commentary or analysis output — the calling skill owns the sheet output.
- Detect which sheet has DR.GET formulas — the calling skill must determine
  enrichment vs cold-question mode before invoking `drilldown`.

## Related skills

- `datarails-excel-agent` — full bridge protocol reference
- `/dr-forecast-variance` — reference implementation of Excel context mode
- `/dr-financial-summary`, `/dr-insights`, `/dr-dashboard` — candidates for
  connector adoption
