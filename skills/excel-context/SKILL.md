---
name: excel-context
description: |
  Connector that other Datarails finance skills delegate to for the Excel-context
  guard / refresh / refresh-after-insert / drill-down patterns — not a response to
  a direct user request. Centralizes
  Excel-context detection (is a workbook open with the add-in bridge available?)
  and the financial-intent → command-name routing — the command catalog itself
  (parameters, timeouts, wait rules) is fetched from the running add-in via
  agent.get_skill, never hardcoded here. Finance skills delegate here
  at Step 0 (guard) and for refresh/drill instead of implementing Excel-context
  logic inline. It ORCHESTRATES the datarails-excel-agent bridge ("the agent") —
  it does not replace it, and it is not the datarails-finance-os MCP connector.
user-invocable: false
allowed-tools:
  - Read
  - execute_office_js
argument-hint: "[guard|refresh|refresh-after-insert|drilldown] [--cells \"Sheet1!A1,Sheet1!B2\"] [--rows \"<label> Δ$X (Y%),...\"] [--enrichment-mode]"
---

# Datarails Excel Context — Connector Skill

Single source of truth for Excel-context detection and the four standard
Excel-agent integration patterns (guard / refresh / refresh-after-insert /
drilldown), plus the financial-intent → command-name routing. The command
catalog itself — parameters, timeouts, wait rules — is **not** defined here:
it lives in the add-in and is fetched at runtime (see below).

Finance skills delegate here instead of implementing context detection inline.

## Four invocation modes

| Mode | Call when | What it does |
|------|-----------|-------------|
| `guard` | First thing in any skill (Step 0) | Probe `agent.get_session`; confirm Excel context + login. Does **not** gate on `isConnected` (see Connection requirement) |
| `refresh` | After `guard` confirms Excel context | Offer a Datarails data refresh before pulling. Works on unconnected workbooks |
| `refresh-after-insert` | Immediately after `add_function_by_id` inserts a `=DR.GET(...)` formula | Refresh the inserted cell(s) so values populate instead of showing "Loading..." |
| `drilldown` | After writing analysis to sheet | Drill-down menu for high-variance rows; invokes `drilldown_list` on selection. **No connection required** — see Connection requirement |

---

## How to run any command (transport)

Every command in this skill is a **bridge command**, run by executing Office.js via the
`execute_office_js` tool against the `__dr_agent` sheet (write request → poll response) —
see `datarails-excel-agent` §Transport + §2/§3. **None of these are MCP tools**, and none
are satisfied by native Excel recalc or by the `datarails-finance-os` connector. If there is
no `execute_office_js` / Office.js tool, you are not in a live Excel context → file-output mode.

## The command catalog lives in the add-in — fetch it, don't trust this file

Command parameters, request shapes, timeout/wait rules, pagination contracts,
and which commands exist on the current add-in build are defined by the
**operating manual the add-in itself serves**: fetch it via `agent.get_skill`
(the `datarails-excel-agent` §4 bootstrap fetch) before issuing
commands. **On any disagreement between the fetched manual and this file, the
manual wins.** This skill deliberately carries no per-command parameter or
timeout tables — a static copy here would drift from the shipped add-in,
which is exactly the failure the bootstrap redesign eliminated.

`agent.list_commands` remains useful as a quick existence probe, but it only
verifies that a command exists — the fetched manual defines how to call it.

## Financial intent → command routing

This table maps a financial intent to the **command name(s)** to look up in
the fetched manual. Names only — parameters, timeouts, wait rules, and
platform (COM/Flex) differences come from the manual. ⚠ = mutating (see
confirmation rule below).

| Financial intent | Command name(s) |
|---|---|
| Detect Excel context / who is signed in | `agent.get_session` |
| Detailed connection info (filebox, env) | `agent.get_connection_info` |
| Connect workbook to Datarails | ⚠ `connect_file` |
| Refresh full workbook | `refresh_ribbon` |
| Refresh a specific range | `refresh_selected_cells_ribbon` |
| Refresh a single table widget | `refresh_table_table_ribbon` |
| Explain what a cell / range contains | `agent.read_range` — cite `data.sources[]` for every figure |
| Evaluate what a DR.GET formula returns | `agent.evaluate_drget` |
| Drill into a P&L line item | `drilldown_list` |
| Drill a variance by dimension pivot | `drilldown_by_pivot`, `drilldown_by_pivot_favorites_*` |
| List function widgets / org catalog | `agent.list_functions` — paginated; follow the manual's pagination contract, never present a partial list |
| Insert a DR.GET function into the sheet | ⚠ `add_function_by_id` |
| List / create dynamic ranges | `agent.list_dynamic_ranges`, `agent.list_dynamic_range_schemas`, ⚠ `create_dynamic_range` |
| List dashboards / publish a range | `agent.list_dashboards`, ⚠ `publish_to_dashboard` |
| Submit an approved budget | ⚠ `submit` |
| Navigation / diagnostics | `agent.activate_sheet`, `agent.select_range`, `agent.list_sheets`, `agent.get_selection`, `agent.ping`, `agent.list_commands` |

Drill-down commands fire only on DR formula cells (DR.GET/QTD/YTD/MTD/…, any
DR function) — never on raw API values written by
`get_aggregation_result_by_alias`.

### Mutating command confirmation rule

Before issuing any mutating command, always show the user what will happen and
wait for explicit confirmation — the add-in will NOT prompt; confirmation is
the caller's responsibility. Treat the fetched manual's marking of mutating
commands as authoritative; at minimum, the ⚠ commands above (`connect_file`,
`submit`, `create_dynamic_range`, `add_function_by_id`,
`publish_to_dashboard`) always require it.

---

## Detecting Excel context

Excel context is **active** if and only if `agent.get_session` succeeds (per the
`datarails-excel-agent` skill, §2/§3 transport).

**Never infer context from user wording alone** ("I'm in Excel", "the workbook is
open"). The authoritative check is the live probe.

- `agent.get_session` returns successfully → Excel context **active**
- Any error, tool-not-found, or bridge sheet missing → Excel context **absent**

---

## Mode: guard

Verify Excel context and confirm the workbook is connected to Datarails. Block
analysis on disconnected workbooks.

### Steps

1. **Probe** — call `agent.get_session` (per `datarails-excel-agent` skill §2/§3).

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

> **`isConnected` is NOT a guard condition.** Refresh, DR.GET insert, evaluate,
> read **and `drilldown_*`** all work on unconnected workbooks. Only
> `create_dynamic_range` requires `isConnected: true`. Check connection **at the
> call site** for that command only — see §Connection requirement below.

---

## Connection requirement

> **`isConnected` is a COM-only field.** Flex sessions expose `isLoggedIn`, not
> `isConnected`, and have no connection gate — on Flex, skip this whole section
> (a logged-in Flex session can run all commands below). The rule here applies
> **only when `agent.get_session` returned an `isConnected` field** (COM).

On COM, `isConnected: true` is required only for this command:

| Command | Why |
|---|---|
| `create_dynamic_range` | Writes to a filebox-linked range |

All other commands — including `refresh_ribbon`, `add_function_by_id`,
`agent.evaluate_drget`, `agent.read_range` **and every `drilldown_*`** — work on
**unconnected** workbooks.

> **Never gate a drill on `isConnected`**, and never tell a user drill-down is
> unavailable because the workbook is unconnected. A **successful** drill returns
> `data: null` and writes a worksheet, so an empty reply is not failure — see
> `datarails-excel-agent` §6. Never report a drill failure you have not probed — see
> `CLAUDE.md`'s Excel Context Contract.

**Before calling the command in the table above (COM only)**, check
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

2. User confirms → call `refresh_ribbon` with a generous timeout per the
   fetched manual's wait rules (real refreshes legitimately run minutes).
   Wait for terminal status (`done` / `failed`) before continuing to the data
   pull — never abort while `running`.

3. User declines → skip, continue.

4. **Do not re-ask** if already asked earlier in this invocation.

---

## Mode: refresh-after-insert

Refresh the cells that just received a `=DR.GET(...)` formula via
`add_function_by_id`. Without this, the inserted cells display "Loading…" or
`#N/A` until something else triggers a refresh — the user sees a broken
formula instead of the resolved value.

**Scope:** This mode is **specific to DR.GET formula insertion**. Do not use
it for other write paths (raw API values written by `get_aggregation_result_by_alias`,
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

2. **One sheet — any count, contiguous or few ranges:** call
   `refresh_selected_cells_ribbon` on the covering range(s) (call shape per
   the fetched manual). Wait for terminal status — refresh wait rules per the
   manual. Count is not the criterion — a 150-formula block on one new sheet
   is **one** scoped call on one range. What makes the scoped command
   expensive is many *discontiguous* call targets, not many cells.

3. **Scattered inserts across multiple sheets** (or so many discontiguous
   ranges that one call per range is impractical): `refresh_ribbon` is the
   remaining option — but it is a **whole-workbook** refresh that repulls
   every DR cell in the file, and any that were stale move to current values
   (observed live: two untouched cells and a downstream YTD total shifted).
   Treat it as mutating in effect:
   - **Before asking, snapshot what you can bound** — read (`get_cell_ranges`)
     the DR blocks on the sheets you are working in and any totals the user is
     looking at. A whole-workbook baseline is not feasible; a bounded one is
     one or two reads.
   - Get the user's explicit OK, telling them stale cells anywhere in the
     workbook will update.
   - Afterwards, diff the snapshot and report each changed cell before →
     after, **naming the ranges you compared** — and say plainly that sheets
     outside them may also have updated. Never present the bounded diff as a
     whole-workbook all-clear.
   - If the user declines, refresh sheet-by-sheet with scoped calls instead.

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
2. **Elaboration request** — when the **calling skill** sees the user wanting to go
   deeper on a figure or section (*"explain / elaborate / break down / dig into / what
   makes up / why is X / show the detail"*) and the figures in scope are **DR formula
   cells**, it delegates here. This is the **default way for a calling skill to
   elaborate on DR-backed data** — it should prefer this over narrating the cached
   value or re-deriving via the `datarails-finance-os` MCP connector. (Detection is
   the caller's job — this connector never fields the user's request directly.)

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
`get_aggregation_result_by_alias`), `drilldown_list` cannot act — it targets DR formula
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
   on that row's DR.GET cell (call shape and wait rules per the fetched
   manual). Do not drill automatically.

---

## Integration pattern for finance skills

Replace inline Excel-context logic in a finance skill SKILL.md with these three
anchors. Finance skills should not re-implement guard, refresh, or drilldown
logic — they delegate here.

### Anchor A — Step 0: guard (always first)

```
### Step 0 — Excel context guard

Run the **guard** mode from `excel-context`:
- Returns `excel_context: false` → switch to file-output mode (.xlsx / .pptx).
- Returns `excel_context: true, connected: true` → continue to Step 0b.
```

### Anchor B — Step 0b: refresh

```
### Step 0b — Data refresh

Run the **refresh** mode from `excel-context`.
(Only reached if guard returned excel_context: true.)
```

### Anchor B2 — after `add_function_by_id`: refresh-after-insert

```
### Step N — Refresh inserted DR.GET formulas

After each successful `add_function_by_id` call (or after a batch),
run the **refresh-after-insert** mode from `excel-context`, passing
the inserted cell addresses. Without it the cells stay on "Loading…".
Only run this for DR.GET formula insertion — not for raw API value writes.
```

### Anchor C — final step: drilldown (enrichment mode only)

```
### Step N — Drill-down

After writing commentary to the sheet, run the **drilldown** mode from
`excel-context` with the analyzed variance rows.
Applies only in enrichment mode — see connector skill for cold-question gate.
```

---

## What this skill does NOT do

- Pull FinanceOS data — that is the calling finance skill's job.
- Write commentary or analysis output — the calling skill owns the sheet output.
- Detect which sheet has DR.GET formulas — the calling skill must determine
  enrichment vs cold-question mode before invoking `drilldown`.

## Related skills

- `datarails-excel-agent` — bridge transport + the §4 `agent.get_skill`
  manual fetch (the command catalog's single source of truth)
- The Anchor A/B/B2/C blocks above are the reference integration —
  `forecast-variance` still inlines its own copy of the guard (a known fork,
  audit L12, to be closed toward these anchors)
- `financial-summary`, `insights`, `dashboard` — candidates for
  connector adoption
