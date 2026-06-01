---
name: datarails-excel-agent
description: |
  Use whenever the user asks for a Datarails operation in their open Excel
  workbook — refresh, drill down, add a function, create a dynamic range,
  publish to a dashboard, read DR.GET values, connect a workbook, or submit.
  Drives the Datarails Excel Add-In through its hidden workbook-bridge sheet.
version: "1.0"
addinSchemaVersion: "1.0"
matchedAddinVersions: ">=2025.9.0"
user-invocable: true
allowed-tools:
  - Read
---

# Datarails Excel Agent — bridge protocol

The Datarails Excel Add-In exposes its ribbon commands to Claude through a
**hidden bridge sheet** (`__dr_agent`) in the open workbook. Write JSON
requests to that sheet; read JSON responses back. All effects on the user's
data sheets are caused by the add-in itself.

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
| `agent.list_functions` | `page?`, `pageSize?` | 30 s | COM: org-wide catalog (paginated). Flex: workbook instances. |
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
| `drilldown_list` | `sheetName`, `cellAddress` | 3 min | Cell must be a DR.GET formula |
| `drilldown_by_pivot` | `sheetName`, `cellAddress` | 3 min | Pivot breakdown |
| `drilldown_by_pivot_favorites_1..5` | `sheetName`, `cellAddress` | 3 min | Saved pivot favorites |

### Formula evaluation

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `agent.evaluate_drget` | `functionName`, `fieldName`, `rowMember`, `dimField?`, `dimValue?` | 10 s | Evaluates DR.GET and returns resolved value; auto-fetches if not cached |

### Authoring

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `add_function_by_id` | `functionId?`, `functionName?` | 60 s | Insert DR.GET widget at active cell |
| `create_dynamic_range` | `dynamicRangeId?`, `dynamicRangeName?`, `listRange`, `formulaRange?`, ... | 60 s | COM only. Columns must match `schema.fieldCount`. Min 20 rows. |
| `publish_to_dashboard` | `rangeAddress`, `dashboardId?`, `dashboardName?` | 3 min | **Mutating — confirm with user first** |

### Workbook lifecycle

| commandId | Params | Timeout | Notes |
|---|---|---|---|
| `connect_file` | — | 3 min | Connect workbook to Datarails. **Mutating — confirm with user first** |
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

---

## Related skills

- `/dr-excel-context` — Excel context detection, guard / refresh / drilldown patterns
- `/dr-forecast-variance` — variance analysis with Excel context mode
