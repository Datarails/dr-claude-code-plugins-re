---
name: datarails-excel-agent
description: |
  Datarails operations on the OPEN Excel workbook. Use this whenever — in Excel —
  the user wants to refresh / recalculate / update the Datarails numbers, drill
  down or break down a cell, add or insert a DR.GET function, create a dynamic
  range, evaluate or read what a DR.GET cell returns, publish to a dashboard,
  connect the workbook, or submit. Runs through the Datarails Excel Add-In via the
  hidden __dr_agent bridge sheet — this is "the agent". NOT the datarails-finance-os
  MCP connector (server-side data only, for when no workbook is open). Trigger
  phrases: "refresh", "recalculate", "update the numbers", "drill into this",
  "what's behind this cell", "add a function", "DR.GET", "publish", "submit".
version: "1.0"
addinSchemaVersion: "1.0"
matchedAddinVersions: ">=2025.9.0"
user-invocable: true
allowed-tools:
  - Read
  - execute_office_js
---

# Datarails Excel Agent — bridge protocol

> **"The agent" = THIS skill.** When any Datarails skill says "the agent", "agent
> bridge", "agent refresh", "agent drill-down", "agent commands", or "agent mode",
> it means **`datarails-excel-agent`** (this skill) driving the Excel Add-In through
> the `__dr_agent` bridge. It is **not** the `datarails-finance-os` MCP connector
> (the FinanceOS REST API). Excel-context Datarails operations run through this
> bridge — not the MCP connector, not native Excel.

The Datarails Excel Add-In exposes its ribbon commands to Claude through a
**hidden bridge sheet** (`__dr_agent`) in the open workbook. Write JSON
requests to that sheet; read JSON responses back. All effects on the user's
data sheets are caused by the add-in itself.

> **Every Datarails operation goes through this bridge — never through native Excel.**
> A request to **refresh / recalculate / update numbers** is `refresh_ribbon`, **not**
> Excel `calculate()` / `calculateFull()` / F9 / re-typing a formula. Native Excel recalc
> does NOT fetch fresh Datarails data and does NOT resolve DR widgets — it returns stale
> or `#BUSY!`/wrong values. Likewise: drill = `drilldown_list`/`drilldown_by_pivot`,
> add function = `add_function_by_id`, evaluate = `agent.evaluate_drget`, connect/submit/
> publish = their bridge commands. If a request seems to map to "just recalc in Excel",
> it almost always maps to a bridge command instead — check `agent.list_commands`.

> ## ⚠️ Transport — how you actually run a command (READ FIRST)
>
> **The commandIds below (`agent.get_session`, `refresh_ribbon`, `drilldown_list`, …) are
> NOT MCP tools and NOT functions you can call directly.** There is no `agent.get_session`
> tool. Each command is **JSON you write into the `__dr_agent` sheet, then read the response
> back** — and the only way to touch that sheet in Claude for Excel is to **run Office.js via
> the `execute_office_js` tool** (the Excel JavaScript execution tool).
>
> So "call `agent.get_session`" / "fire `refresh_ribbon`" always means:
> 1. `execute_office_js` → run the §2 `Excel.run` snippet that writes the request JSON to
>    `dr_agent_inbox`, sets `dr_agent_status`, and **increments `dr_agent_seq`** (the doorbell).
> 2. `execute_office_js` → run the §3 snippet that polls `dr_agent_outbox` until `final: true`,
>    then parse the response JSON.
>
> If you find yourself looking for an MCP tool named after a command, or reaching for the
> `datarails-finance-os` connector, **stop** — you must use `execute_office_js` against the
> bridge sheet. (If no `execute_office_js`/Office.js tool is available, you are not in a live
> Excel context — fall back to file-output mode.)

---

## 1. Bridge sheet layout

Sheet name: `__dr_agent` (very-hidden — invisible to the user).

| Defined name | Cell | Purpose |
|---|---|---|
| `dr_agent_meta` | A1 | Schema version. COM writes `"1.0"`; Flex writes `{"schemaVersion":"1.0"}`. Accept both. |
| `dr_agent_next` | E1 | Next-free row index (append-only high-watermark, ≥ 2). |
| `dr_agent_seq` | F1 | Inbox doorbell — increment by 1 on **every** request write. |
| `dr_agent_cancel_seq` | G1 | Cancel doorbell — increment by 1 each time you write `cancel-requested`. |
| `dr_agent_inbox` | A2..A_max | One JSON request per row (you write). |
| `dr_agent_outbox` | B2..B_max | One JSON response per row (add-in writes). |
| `dr_agent_status` | C2..C_max | Status per row: `queued` → `running` → `progress*` → `done\|failed\|cancelled`. |

Always reference cells by defined name, never by absolute address.

---

## 2. Sending a request

```js
await Excel.run(async (ctx) => {
  const wb        = ctx.workbook;
  const nextRange = wb.names.getItem("dr_agent_next").getRange();
  const seqRange  = wb.names.getItem("dr_agent_seq").getRange();
  nextRange.load("values"); seqRange.load("values");
  await ctx.sync();

  const k   = nextRange.values[0][0] || 2;
  const seq = (seqRange.values[0][0] || 0) + 1;

  wb.names.getItem("dr_agent_inbox").getRange().getCell(k-2, 0).values
    = [[ JSON.stringify(request) ]];
  wb.names.getItem("dr_agent_status").getRange().getCell(k-2, 0).values
    = [[ "queued" ]];
  nextRange.values = [[ k + 1 ]];
  seqRange.values  = [[ seq ]];       // ring the doorbell — required
  await ctx.sync();
  return k;
});
```

> **Always increment `dr_agent_seq`** — it is the only signal the COM poll
> watches. Without it the request is missed.

Request schema:
```json
{
  "requestId":       "<uuid>",
  "commandId":       "refresh_ribbon",
  "params":          {},
  "timeoutMs":       60000,
  "clientTimestamp": "2025-09-01T10:00:00Z"
}
```

---

## 3. Reading the response

Poll `dr_agent_outbox` row `k-2` until `final: true`.

| Status | Meaning | Action |
|---|---|---|
| (empty) | Not yet observed by poll | Wait up to 10 s |
| `queued` | Claimed, handler not started | Wait up to 10 s |
| `running` / `progress` | Executing | **Wait indefinitely** — never abort on wall clock |
| `done` / `failed` / `cancelled` | Terminal | Read outbox JSON, stop waiting |
| `cancel-requested` | Cancel pending | Treat as `running`, keep waiting |

> Refresh on a real workbook takes **30–120 s**. Keep waiting while status is
> `running`. Do not apply a wall-clock timeout that aborts before terminal.

---

## 4. Cancellation

Write `cancel-requested` into the status cell **and** increment
`dr_agent_cancel_seq` (G1) in the same `Excel.run` batch. Without the G1
increment the COM poll never wakes to observe the cancel.

> **lateCancel:** If a mutating handler already committed before abort fires,
> the terminal envelope carries `status: "done"` with `data.lateCancel: true`
> — not `status: "cancelled"`. The workbook was changed; do not treat as no-op.

---

## 5. Command catalog

All commands below: `minSkillVersion: 1.0.0`  ·  `addinVersion: >=2025.9.0`

### Discovery / meta

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `agent.ping` | — | 5 s | Liveness check; returns schema + addin version |
| `agent.list_commands` | — | 5 s | Returns capability descriptor with all supported commands |
| `agent.get_session` | — | 5 s | Workbook name, principal, `isConnected` (COM) / `isLoggedIn` (Flex) |
| `agent.cancel_request` | `targetRequestId` | 5 s | Cancel in-flight request by id |

### Reads

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `agent.list_sheets` | — | 5 s | Enumerate sheets in workbook |
| `agent.get_selection` | — | 5 s | Active sheet + range + cell value |
| `agent.get_connection_info` | — | 5 s | `fileboxId`, `environment`, `userName`, `isLoggedIn` |
| `agent.read_range` | `sheetName`, `cellAddress` | 30 s | Values + formulas + `data.sources[]` — **cite sources for every figure** |
| `agent.list_functions` | `page?`, `pageSize?` | 30 s | COM: org-wide catalog (paginated). Flex: workbook instances. Returns `totalCount`/`totalPages`. Response: `id`, `name`, `dimensionField` only. **Always fetch all pages — see §10.** |
| `agent.list_dynamic_ranges` | — | 30 s | DR instances already in workbook (`id`, `name`, `hasForecastModule`) |
| `agent.list_dynamic_range_schemas` | — | 30 s | Available DR schemas (`id`, `name`, `fieldCount`, `fields[]`) |
| `agent.list_dashboards` | — | 30 s | Dashboards available to publish to (`id`, `name`) |

### Refresh

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `refresh_ribbon` | — | 10 min | Refresh all functions in workbook |
| `refresh_selected_cells_ribbon` | `sheetName`, `cellAddress` | 10 min | Refresh specific range |
| `refresh_table_table_ribbon` | `sheetName`, `cellAddress` | 10 min | Refresh table under selection |

### Drill-down

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `drilldown_list` | `sheetName`, `cellAddress` | 3 min | Cell must be a DR formula (`DR.GET`/`DR.QTD`/`DR.YTD`/`DR.MTD`/… — any DR function resolving to a widget) |
| `drilldown_by_pivot` | `sheetName`, `cellAddress`, `rowField`, `targetTemplateId?`, `targetTemplateName?` | 3 min | Pivot breakdown. **`rowField` is required in agent mode** (the field to break down by) — no UI picker is shown. Optional `targetTemplateId`/`targetTemplateName` to drill into a different template; defaults to the source table. |
| `drilldown_by_pivot_favorites_1..5` | `sheetName`, `cellAddress` | 3 min | Saved pivot favorites — fully headless, **no `rowField` needed** (field/template come from the saved favorite). |

### Formula evaluation

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `agent.evaluate_drget` | `functionName`, `fieldName`, `rowMember`, `dimField?`, `dimValue?` | 10 s | Evaluates DR.GET and returns resolved value; auto-fetches if not cached |

### Authoring

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `add_function_by_id` | `functionId?`, `functionName?` | 60 s | Insert DR.GET widget at active cell. **MUST be followed by a refresh** — see rule below. |
| `create_dynamic_range` | `dynamicRangeId?`, `dynamicRangeName?`, `listRange`, `formulaRange?`, ... | 60 s | COM only. Columns must match `schema.fieldCount`. Min 20 rows. Populate `formulaRange` row 1 with DR.GET formulas in the exact shape below. |
| `publish_to_dashboard` | `rangeAddress`, `dashboardId?`, `dashboardName?` | 3 min | **Mutating — confirm with user first** |

#### ⚠️ ALWAYS refresh after inserting DR functions — MANDATORY

`add_function_by_id` (and any `create_dynamic_range` whose `formulaRange` gets
DR.GET formulas) inserts the formula but does **not** populate its value. Until a
refresh runs, the cell shows **"Loading…" / `#BUSY!` / `#N/A`** — the data is not
there yet.

**After every `add_function_by_id` (single or batch), you MUST fire a refresh
before reading or reporting the value:**

1. Single cell / one sheet → `refresh_selected_cells_ribbon` (`sheetName`, `cellAddress`).
2. Many cells / multiple sheets → `refresh_ribbon`.
3. Set `timeoutMs: 600000`; wait for terminal status; then `agent.read_range` /
   `agent.evaluate_drget` to confirm a real value (not "Loading…").

Do **not** present an inserted DR.GET's value without this refresh — it will be
stale/blank. This is the single most common mistake; treat insert + refresh as
one atomic step. (Connector: `/dr-excel-context refresh-after-insert`.)

#### DR.GET formula shape (required for dynamic-range population)

Every DR.GET (and the period variants DR.QTD/YTD/MTD/…) follows the same shape:

```
=DR.GET(<FunctionName>, "[Field1]", <Value1>, "[Field2]", <Value2>, …)
```

- **Arg 1** = the function / widget name — a **bare identifier** (a defined name). **No quotes, no cell reference.** It is a registered token, not a string; quoting it (`"Value"`) breaks resolution. Write it exactly as the widget name, e.g. `Value`.
- Then **alternating** `"[FieldName]"`, `<Value>` pairs. **Field names are bracketed** and quoted: `"[Reporting Date]"`, `"[Account Full]"`, `"[Planning Version]"`, `"[Legal Entity]"`, etc.
- `<Value>` may be a literal (`"REVENUE"`, `"G&A"`) or a cell reference (`$A8`, `H$4`).
- **Dates: ALWAYS Excel end-of-month serial.** Use `EOMONTH(<date>,0)` (or a cell that resolves to a month-end serial). Never a mid-month date, never text. The engine buckets by month-end — a non-EOM serial returns 0/empty. Reference a header cell built with `=EOMONTH(...)` rather than typing a raw date.
- Write the formula **bare** — never wrap in `IFERROR`/`IF`/`ROUND`/etc. (breaks the add-in's refresh/drill tracking).

Example (matches a real workbook):
```
=DR.GET(Value,"[Reporting Date]",H$4,"[Account Full]",$A8,"[Planning Version]",H$5,"[DR_ACC_L2]","G&A","[Legal Entity]",$A$6)
```
where `H$4 = EOMONTH(<quarter month>,0)`.

For `create_dynamic_range`: the `listRange` column count must equal `schema.fieldCount`; the `formulaRange` row-1 cells get this DR.GET shape so the range auto-fills every subsequent row from the list dimension values.

### Workbook lifecycle

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `connect_file` | — | 3 min | Connect workbook to Datarails. **Mutating — confirm with user first.** Required only for `create_dynamic_range` and `drilldown_*`. Refresh, DR.GET insert, and evaluate work without it. |
| `submit` | — | 3 min | Submit workbook. **Mutating — confirm with user first** |

### Navigation

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `agent.activate_sheet` | `sheetName` | 60 s | Activate sheet by name |
| `agent.select_range` | `sheetName`, `cellAddress` | 60 s | Select range on sheet |

---

## 6. `agent.get_session` response shapes

**COM:**
```json
{
  "fileName": "Budget_2026.xlsx", "fullName": "C:\\...\\Budget_2026.xlsx",
  "isConnected": true, "fileBoxId": "abc123",
  "principal": "alice@corp.com", "userFirst": "Alice", "userLast": "Smith",
  "host": "https://app.datarails.com", "environment": "prod"
}
```

**Flex:**
```json
{
  "workbookName": "Budget_2026.xlsx", "fileBoxId": "abc123",
  "environment": "prod", "principal": "alice@corp.com",
  "isLoggedIn": true,
  "features": { "mutationConfirm": false, "cancellation": true }
}
```

Transport detection: `features` present → Flex. `fileName` + `isConnected` → COM.

Connection check: COM → `isConnected`, Flex → `isLoggedIn`.

---

## 7. Error codes

| Code | Action |
|---|---|
| `bad_request` | Show `errorMessage`, fix and retry once |
| `unknown_command` | Command not in catalog — call `agent.list_commands` to check what's available |
| `capability_not_available` | Add-in too old — read `data.requiredVersion`, tell user to update |
| `unauthorized` | Tell user to sign in to Datarails; stop |
| `queue_full` | Wait a few seconds, retry; or close + reopen workbook |
| `handler_failed` | Show `errorMessage` verbatim; do not retry blindly |
| `timeout` | Retry once with higher `timeoutMs`; stop if second timeout |
| `cancelled` | Acknowledge and stop |

---

## 8. Citation rule

Every response that surfaces financial figures includes `data.sources[]`.
**You must cite the source for every figure you present.** No exceptions.
If `sources` is empty for a read/compute response, do not present derived
figures — re-read the range or tell the user the data is not Datarails-tracked.

---

## 9. Mutating command rule

Before issuing any mutating command (`connect_file`, `submit`,
`create_dynamic_range`, `add_function_by_id`, `publish_to_dashboard`):
show the user what will happen and wait for explicit confirmation.
The add-in will **not** prompt — confirmation is the caller's responsibility.

**`connect_file` scope:** Only call `connect_file` when the user explicitly
requests it, or when a command that requires it (`create_dynamic_range`,
`drilldown_*`) is blocked by `isConnected: false`. Do not call it as a
general prerequisite — most operations work without it.

---

## 10. Pagination — `agent.list_functions`

Orgs can have 100+ function widgets. Default `pageSize` is 20. Max is 100.
**Never present a partial list.** Always collect all pages before displaying.

```
page = 1; all = []
do:
  response = agent.list_functions(params: { page: page, pageSize: 100 })
  all += response.data.functions
  page++
while page <= response.data.totalPages
```

Response shape (per page) — handler result is nested under the envelope's
`data` field (same as every command response), so read `response.data.*`:
```json
{
  "final": true,
  "status": "done",
  "data": {
    "functions":  [ { "id": 7872, "name": "...", "dimensionField": "..." } ],
    "page":       1,
    "pageSize":   100,
    "totalCount": 160,
    "totalPages": 2
  }
}
```

After collecting all, present the full list and let the user pick by name or id
before calling `add_function_by_id`.

---

## Related skills

- `/dr-excel-context` — Excel context detection, guard / refresh / drilldown patterns
- `/dr-forecast-variance` — variance analysis with Excel context mode
