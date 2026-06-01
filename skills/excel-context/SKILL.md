---
name: dr-excel-context
description: |
  Connector skill — centralizes Excel-context detection and the financial
  context → agent command mapping for Datarails finance skills. Reference this
  skill instead of implementing Excel context logic inline. May be invoked
  directly to inspect connection state or test the bridge.
user-invocable: true
allowed-tools:
  - Read
argument-hint: "[guard|refresh|drilldown] [--rows \"<label> Δ$X (Y%),...\"] [--enrichment-mode]"
---

# Datarails Excel Context — Connector Skill

Single source of truth for Excel-context detection, financial context → agent
command mapping, and the three standard Excel-agent integration patterns
(guard / refresh / drilldown).

Finance skills delegate here instead of implementing context detection inline.

## Three invocation modes

| Mode | Call when | What it does |
|------|-----------|-------------|
| `guard` | First thing in any skill (Step 0) | Probe session, check connection, block on disconnected workbook |
| `refresh` | After `guard` returns connected | Offer a Datarails data refresh before pulling |
| `drilldown` | After writing analysis to sheet | Drill-down menu for high-variance rows; invokes drill-down on selection |

---

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
| Drill into a P&L line item (list) | `drilldown_list` | `sheetName`, `cellAddress` | Enrichment mode only — cell must be a DR.GET formula |
| Drill into a variance by dimension pivot | `drilldown_by_pivot` | `sheetName`, `cellAddress` | Enrichment mode only |
| Drill into a variance using saved pivot | `drilldown_by_pivot_favorites_*` | `sheetName`, `cellAddress` | Variant of pivot drill-down |

Set `timeoutMs: 180000` (3 min). Only fire on DR.GET formula cells — never on
raw API values written by `aggregate_table_data`.

### Function widgets (DR.GET)

| Financial context | Command | Key params | Notes |
|---|---|---|---|
| List function widgets in this workbook | `agent.list_functions` | — | COM: returns org-wide catalog (deviation). Flex: returns workbook instances. |
| Browse org function catalog | `agent.list_function_definitions` | `functionName`, `pageSize`, `cursor` | Flex only. On COM use `agent.list_functions` |
| Insert a DR.GET function into the sheet | `add_function_by_id` | `functionId`, `sheetName`, `cellAddress` | Use `id` from list response as `functionId` |

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

3. **On success** — read `isConnected` (COM transport) or `isLoggedIn` (Flex
   transport) from the session response.

4. **If not connected / not logged in:**
   Ask the user explicitly:
   > *"This workbook is not connected to Datarails. Should I connect it now
   >  with `connect_file`?"*

   **Wait for an explicit "yes" before calling `connect_file`.** Do not
   call it automatically — it is a mutating command.

   - User confirms → call `connect_file`, wait for completion.
   - User declines / no response → stop the parent skill:
     > *"Analysis requires a connected workbook. Re-run the skill after
     >  connecting."*

5. **If connected / logged in:**
   Return `excel_context: true, connected: true`. The calling skill continues.

---

## Mode: refresh

Offer to refresh Datarails data from the server before the analysis pull.

### Precondition

`guard` must have returned `excel_context: true, connected: true` in this
session. Never call `refresh` if `guard` was skipped or returned
`excel_context: false`.

### Steps

1. Ask once per skill invocation:
   > *"Should I refresh data from Datarails before pulling? (Recommended if
   >  you haven't refreshed today.)"*

2. User confirms → call `refresh_ribbon`. Set `timeoutMs: 600000`.
   Wait for terminal status (`done` / `failed`) before continuing to the data pull.

3. User declines → skip, continue.

4. **Do not re-ask** if already asked earlier in this invocation.

---

## Mode: drilldown

Present a drill-down menu for rows with large variances, then invoke
`drilldown_list` on the rows the user selects.

### Preconditions — both must hold

**1. Excel context confirmed.** `guard` returned `excel_context: true` in this
session.

**2. Enrichment mode.** The parent skill ran in enrichment mode — the active
sheet already had DR.GET formula cells, and the skill added commentary alongside
them.

In **cold-question mode** (sheet was empty; skill wrote raw API values from
`aggregate_table_data`), `drilldown_list` cannot act — it targets DR.GET
formula cells, not raw values. Skip and tell the user:

> *"Drill-down is not available — data was written as raw values, not DR.GET
>  formulas. Open a workbook that has DR.GET formula cells and re-run the skill
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
