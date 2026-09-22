---
name: datarails-excel-agent
description: |
  Datarails operations on the OPEN Excel workbook. Use this whenever — in Excel —
  the user wants to refresh / recalculate / update the Datarails numbers, drill
  down or break down a cell, add or insert a DR.GET function, create a dynamic
  range, evaluate or read what a DR.GET cell returns, publish to a dashboard,
  connect the workbook, or submit. Runs through the Datarails Excel Add-In via the
  hidden __dr_agent bridge sheet — this is "the agent". NOT the datarails-finance-os
  MCP connector — the connector answers org-data questions (list tables/models/fields,
  aggregations, distinct values, metrics, org users, FX) and stays correct even while a
  workbook is open; use THIS skill only to act on the open workbook. Trigger
  phrases: "refresh", "recalculate", "update the numbers", "drill into this",
  "what's behind this cell", "add a function", "DR.GET", "publish", "submit".
addinSchemaVersion: "1.0"
matchedAddinVersions: ">=2025.9.0"
user-invocable: true
allowed-tools:
  - Read
  - execute_office_js
  - mcp__datarails-finance-os__list_xl_functions
---

# Datarails Excel Agent — bootstrap

> **This file is a bootstrap.** It teaches you the transport (how to send a request and
> read the response over the `__dr_agent` bridge sheet) and then tells you to **fetch the
> full, always-current operating manual from the running add-in via `agent.get_skill`**.
> The command catalog and rules live in the add-in (generated from its live capabilities),
> so they can never drift from what the add-in actually supports. Do not hardcode the
> catalog from memory — fetch it.

## "The agent" = the add-in bridge, NOT the MCP connector

"The agent" / "agent bridge" / "agent refresh" / "agent commands" all mean driving the
Datarails Excel Add-In through the hidden `__dr_agent` sheet. **Workbook operations**
(refresh, drill, insert DR.GET, read/evaluate cells, publish, connect, submit) go through
this bridge — never native Excel (`calculate()`/F9/re-typing formulas return stale or
`#BUSY!` values). **Org-data questions** (which tables/models/fields exist, aggregations,
distinct values, metrics, org users, FX) go to the `datarails-finance-os` MCP connector —
**even while a workbook is open**. Route by target, not by whether Excel is open.

You touch the bridge sheet only by running Office.js via the **`execute_office_js`** tool.
If no Office.js tool is available you are not in a live Excel context — fall back to
file-output mode.

**Widget → table resolution:** the MCP connector's `list_xl_functions` returns the org's
DR.GET widget catalog in one un-paginated call, each entry carrying the owning
`template: {id, name}` — the widget's actual data source, which the bridge's
`agent.list_functions` does not include. Use it to ground a DR.GET formula to its source
table (the widget name is the formula's first argument), to disambiguate `functionId`
before `add_function_by_id`, or to skip pagination on large catalogs. This is an org-data
lookup (connector territory per the routing rule above), not a bridge command.
Because `agent.list_functions` carries no `template`, it is not a substitute:
without the connector you can still enumerate the tokens placed in this
workbook, but table grounding and `functionId` disambiguation are unavailable —
say so rather than guessing the source. Every other bridge flow proceeds
regardless; never block one on the MCP being connected.

## 1. Bridge sheet layout

Sheet `__dr_agent` (very-hidden). Reference cells **by defined name**, never by address.

| Defined name | Cell | Purpose |
|---|---|---|
| `dr_agent_meta` | A1 | Schema stamp. Flex writes `{"schemaVersion":"1.0"}`; COM writes `"1.0"`. Accept both. |
| `dr_agent_next` | E1 | Next-free row (append-only high-watermark, ≥ 2). |
| `dr_agent_seq` | F1 | Inbox doorbell — **COM only.** Flex does not create it; bump it only if it exists. |
| `dr_agent_cancel_seq` | G1 | Cancel doorbell — increment when you write `cancel-requested`. |
| `dr_agent_inbox` | A2..A_max | One JSON request per row (you write). |
| `dr_agent_outbox` | B2..B_max | One JSON response per row (add-in writes). |
| `dr_agent_status` | C2..C_max | `queued` → `running` → `progress*` → `done\|failed\|cancelled`. |
| `dr_agent_listener_heartbeat` | H1 | Listener liveness (JSON; stamped ~every 2 s while the listener is driving THIS workbook). **May be absent** (older add-in) **or present-but-empty** (COM before its first command) — see below. |

## Listener liveness — check BEFORE you wait

The add-in's bridge listener can stop draining the bridge mid-session — on Excel for the web the
task pane can suspend/detach (co-authoring recovery); on desktop (COM) the add-in can be disabled,
not loaded, or Excel can be blocked on a modal dialog. When that happens **nothing drains the
bridge** and every request sits at `queued` forever, so a blind wait burns your whole execution
budget for nothing. Guard against it by reading the heartbeat (call inside your `Excel.run`, passing
`ctx` — same nested-run rule as §2). This is **transport-agnostic** — the check is identical on COM
and Flex:

```js
// Returns ONE of four states. Branch on `state` — never on booleans.
//   "unsupported" → no heartbeat range at all (older add-in).
//   "unstamped"   → range exists, listener has never stamped it. NORMAL on COM before your first
//                   command (COM only heartbeats a workbook it is actively driving). Also what you
//                   see when the add-in never loaded at all — so it is NOT a licence to wait forever.
//   "stale"       → it was stamped, but not within the last 6 s → nothing is draining the bridge.
//   "alive"       → stamped within the last 6 s → healthy.
async function checkListenerAlive(ctx) {
  const hb = ctx.workbook.names.getItemOrNullObject("dr_agent_listener_heartbeat");
  hb.load("isNullObject"); await ctx.sync();
  if (hb.isNullObject) return { state: "unsupported" };
  const rng = hb.getRange(); rng.load("values"); await ctx.sync();
  const raw = rng.values[0][0];
  // Explicit empty/null check — NOT `!raw`, which would treat a numeric 0 (Office.js may return a
  // non-string cell value) as "unstamped". Only a truly empty/blank cell is unstamped; any other
  // value falls through and is classified below (a non-object payload → "stale").
  if (raw === null || raw === undefined || raw === "") return { state: "unstamped" };
  // Unparseable JSON = something wrote the cell and then stopped → treat as stale, not unstamped.
  let p; try { p = JSON.parse(raw); } catch { return { state: "stale" }; }
  // JSON.parse("null") succeeds with p === null; a non-object payload has no heartbeatAt to read
  // → treat as stale rather than dereferencing and throwing.
  if (p === null || typeof p !== "object") return { state: "stale" };
  // A malformed heartbeatAt makes Date.parse NaN → comparison false → "stale". Fail safe, by design.
  const fresh = (Date.now() - Date.parse(p.heartbeatAt)) < 6000;
  return { state: fresh ? "alive" : "stale", heartbeat: p };
}
```

**Rules.** Call `checkListenerAlive` **before your first command** (including the §4
`agent.get_skill` fetch), and again whenever a row sits at `queued`/empty past ~6 s:

| `state` | Before sending | Re-checked while a row is still `queued`/empty past ~6 s |
|---|---|---|
| `alive` | Proceed. | Listener alive but busy — **keep waiting** (see §3: never abort on wall clock). |
| `unstamped` | **Proceed** — do NOT block. Normal on COM pre-first-command; the first send starts the heartbeat. | **Still `unstamped` → STOP.** A running listener stamps within ~2 s of picking up work, so 6 s unstamped means nothing is draining the bridge. Surface the stalled-listener message. |
| `stale` | **STOP** — do not send, do not wait. Surface the stalled-listener message. | **STOP** — surface the stalled-listener message. |
| `unsupported` | Proceed with the legacy §3 waits (no regression on older add-ins). | No liveness signal exists — fall through to the §5 no-pickup rule (~10 s → fallback catalog). |

**Stalled-listener message** — tell the user verbatim, then retry once they confirm:

> *"The Datarails add-in isn't responding — nothing is picking up requests from the bridge. In
> Excel for the web, reopen the Datarails task pane; on desktop, make sure the Datarails add-in is
> enabled and that Excel isn't waiting on a dialog. Then tell me and I'll retry."*

Never silently keep polling a bridge no listener is draining: `unstamped` buys you one command's
grace, not an unbounded wait.

## 2. Sending a request

> **If your `execute_office_js` runtime already runs inside an `Excel.run` context**
> (it provides a `ctx`/`context` object), use THAT context and DROP the outer
> `await Excel.run(...)` wrapper below — a nested `Excel.run` throws
> `IllegalAccessError: Access to 'run' is blocked`. Keep the body identical.

```js
await Excel.run(async (ctx) => {
  const wb        = ctx.workbook;
  const nextRange = wb.names.getItem("dr_agent_next").getRange();
  // dr_agent_seq is COM-only — getItemOrNullObject so a Flex-fresh workbook (no F1)
  // does NOT throw ItemNotFound on the first send.
  const seqName   = wb.names.getItemOrNullObject("dr_agent_seq");
  nextRange.load("values"); seqName.load("isNullObject");
  await ctx.sync();

  const k = nextRange.values[0][0] || 2;
  // The bridge only needs a unique opaque string. crypto.randomUUID is absent on older
  // Office webviews / the COM desktop track, so guard it (mirrors the add-in's own
  // traceId helper) — calling it bare would throw and abort the send on those runtimes.
  const uid = (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function")
    ? crypto.randomUUID()
    : `${Math.random().toString(36).slice(2)}${Math.random().toString(36).slice(2)}_${Date.now()}`;
  const request = {
    requestId:       uid,
    commandId:       "agent.get_skill",          // or any command from the fetched catalog
    params:          {},
    timeoutMs:       60000,
    clientTimestamp: new Date().toISOString(),   // programmatic — used for latency, never a literal
  };

  wb.names.getItem("dr_agent_inbox").getRange().getCell(k-2, 0).values  = [[ JSON.stringify(request) ]];
  wb.names.getItem("dr_agent_status").getRange().getCell(k-2, 0).values = [[ "queued" ]];
  nextRange.values = [[ k + 1 ]];
  if (!seqName.isNullObject) {                    // COM doorbell; harmless to skip on Flex
    const seqRange = seqName.getRange(); seqRange.load("values"); await ctx.sync();
    seqRange.values = [[ (seqRange.values[0][0] || 0) + 1 ]];
  }
  await ctx.sync();
  return k;                                        // remember the row for polling
});
```

## 3. Reading the response

Poll `dr_agent_outbox` row `k-2` until the envelope has `final: true`.

| Status | Action |
|---|---|
| (empty) / `queued` | Wait — but if it persists past ~6 s, re-run `checkListenerAlive` and apply the right-hand column of the liveness table above: `alive` → keep waiting; `stale` **or still** `unstamped` → nothing is draining the bridge, STOP and surface the stalled-listener message; `unsupported` → no signal, fall through to the §5 no-pickup rule. |
| `running` / `progress` | **Wait indefinitely** — never abort on wall clock (a refresh can take 30–120 s). Do NOT re-check liveness here: the listener may be single-threaded inside a long command, so a stale heartbeat while `running` is expected, not a detach. |
| `done` / `failed` / `cancelled` | Terminal — read `data` / `errorCode`, stop |
| `cancel-requested` | Treat as `running`, keep waiting |

**Cancel:** write `cancel-requested` into the status cell **and** increment
`dr_agent_cancel_seq` (G1) in the same `Excel.run`. (Or send `agent.cancel_request` with the
target `requestId`.)

## 4. First action — fetch the operating manual

Before running any workbook command in a session, **fetch the manual**:

1. Send `agent.get_skill` (params `{}`) and read the response.
2. On `done`: cache `data.content` (markdown) for the rest of this conversation. If
   `data.nextCursor` is not null, send `agent.get_skill` again with
   `params: { "cursor": "<nextCursor>" }` and concatenate `data.content` until `nextCursor`
   is null.
3. **Follow the fetched manual as the authoritative catalog + rules for this session.** It
   lists exactly the commands this add-in build supports, with params and which are mutating.
4. State it in your first user-facing status line, e.g.
   `skill: dynamic v{data.contentVersion} (add-in {data.addinVersion})`.
5. Do **not** re-fetch within a session.

## 5. Fallback (older add-in / COM desktop / no bridge)

Use the fallback when `agent.get_skill` returns `{"status":"failed","errorCode":"unknown_command"}`
(add-in predates dynamic skill, incl. COM desktop), the bridge sheet is absent, or no row is
picked up after ~10 s. State `skill: bootstrap-fallback (<reason>)`, then use this compact
catalog. Read `response.data.*` on every command; **cite `data.sources[]` for every figure**
(exception: the drill commands return no `data` at all — see §6).

> **On `errorCode: "bad_request"` / *"Missing or invalid required param"*, retry before concluding
> anything** — the error names the param the add-in wants. If §4 fetched a manual, take the param
> name from its catalog row, which outranks this table. In fallback there is no manual, so retry
> from the row below. Treat the command as broken only after that retry fails
> (`CLAUDE.md` § Excel Context Contract).

| commandId | Params | Timeout |
|---|---|---|
| `agent.ping` / `agent.list_commands` / `agent.get_session` | — | 5 s |
| `agent.cancel_request` | `targetRequestId` | 5 s |
| `agent.list_sheets` / `agent.get_selection` | — | 5 s |
| `agent.read_range` | `sheetName`, `cellAddress` | 30 s |
| `agent.list_functions` | — (Flex) / `page?`, `pageSize?` (COM) | 30 s — Flex returns the full list in one response; COM paginates (fetch ALL pages) |
| `agent.list_function_definitions` | `query?`, `templateId?`, `pageSize?`, `cursor?` | 30 s — cursor-paginated (follow `nextCursor` to null) |
| `agent.list_dashboards` | — | 30 s |
| `refresh_ribbon` | — | 10 min |
| `refresh_selected_cells_ribbon` / `refresh_table_table_ribbon` | `sheetName`, `cellAddress` | 10 min |
| `drilldown_list` | `sheetName`, `cellAddress` | 3 min — **no `data` in the reply; see §6** |
| `drilldown_by_pivot` | `sheetName`, `cellAddress`, **`rowField`** (required — exactly one dimension to break down by), `targetTemplateId?`/`targetTemplateName?` | 3 min — **no `data` in the reply; see §6** |
| `drilldown_by_pivot_favorites_1..5` | `sheetName`, `cellAddress` | 3 min — **no `data` in the reply; see §6** |
| `add_function_by_id` | `functionId?` / `functionName?` | 60 s |
| `publish_to_dashboard` | `rangeAddress`, `dashboardId?`/`dashboardName?` | 3 min |
| `connect_file` / `submit` | — | 3 min |
| `agent.activate_sheet` / `agent.select_range` | `sheetName`(`, cellAddress`) | 60 s |
| `agent.evaluate_drget` | `functionName`, `fieldName`, `rowMember`, `dimField?`, `dimValue?` | 10 s — **COM only** |
| `agent.get_connection_info` | — | 5 s — **COM only** |
| `create_dynamic_range` | `dynamicRange*`, `listRange`, `formulaRange?`, … | 60 s — **COM only** |
| `agent.list_dynamic_ranges` / `agent.list_dynamic_range_schemas` | — | 30 s — **COM only** |

**Rules that always apply.** Rules 1–4 restate the fetched manual and hold in
fallback too; rule 5 is bootstrap-side only until the add-in's manual mirrors
it — apply all five either way.

1. **Refresh after every insert.** `add_function_by_id` writes the formula but not its value
   (shows "Loading…"/`#BUSY!`). Fire `refresh_selected_cells_ribbon` (or `refresh_ribbon` for
   a batch) with `timeoutMs: 600000` and wait for terminal before reading/reporting. **This
   covers pattern-filled ranges, not just the cell you seeded** — copies of an already-resolved
   seed can stay `Missing`/`#BUSY!` and surface only as `#VALUE!` in a downstream SUM, so refresh
   the whole written range and confirm every cell in it is numeric before reporting any figure.
2. **Confirm before mutating** (`connect_file`, `submit`, `add_function_by_id`,
   `publish_to_dashboard`, `create_dynamic_range`): show what will happen and wait for the
   user. The add-in does not prompt.
3. **Cite `data.sources[]`** for every figure you present. If empty, don't present derived
   figures — re-read or say the data is not Datarails-tracked. **One exception:** the drill
   commands return no `data` at all; their citation is the filter context the add-in echoes into
   row 1 of the sheet it creates (§6).
4. **Wait indefinitely while `running`** — never a wall-clock abort before terminal.
5. **Prefer live DR.GET when writing figures.** A cell holding a
   Datarails-backed figure should be a DR.GET formula, inserted with
   `add_function_by_id` where a widget matches (confirm per rule 2, then
   refresh per rule 1). Fall back, in order, to native Excel arithmetic over
   DR.GET cells (Δ$/Δ%/ratios stay live through their precedents), a reference
   to an existing cell at the exact scope needed, and only last a pasted static
   value — which still needs its source cited per rule 3. Do not hand-author
   DR.GET syntax here; if no widget matches, say so — `/dr-get-formula` owns
   formula authoring.

## 6. Drill-down: no payload, no connection

For `drilldown_list` / `drilldown_by_pivot` / `drilldown_by_pivot_favorites_*`:

- **A successful drill returns `data: null`.** `{"status":"done","final":true}` with an empty
  payload is success — the output is the worksheet the add-in creates. Read the result there; row 1
  echoes the source cell's filter context and is the citation in place of `data.sources[]`.
- **No connection needed.** They run with `isConnected: false`. Never gate a drill on `isConnected`,
  and never tell the user a drill is blocked because the workbook is unconnected.

A drill is mutating in effect and must be confirmed first — that protocol is `/dr-drilldown`
Step 0. Do not restate it here.

## 7. Writing to the sheet — three traps

| Trap | Rule |
|---|---|
| **Whole-column formatting** | Bound every width and format to the used band — `getRange("H1:H120")`, never `getRange("H:H")`. On a sheet holding more than one block, never address a bare column or row: the format bleeds into every other block. |
| **Pattern-fill stride mismatch** | A side-by-side grid advances 2 columns per period; a single-scenario source block advances 1. Give each side its own DR formula rather than filling a cross-sheet link across the pair stride, and verify `formulas` — not values — at a middle and a last pair. |
| **Formatting verified by reading values** | Reading a range back does not show what the user sees. After formatting a block, capture it with `getRange(...).getImage()` + `attachImage(...)` and look at it. |

## Related skills

- `/dr-get-formula` — **builds DR.GET formulas**; owns formula authoring when
  no widget matches
- `excel-context` — Excel context detection, guard / refresh / drilldown patterns
- `/dr-drilldown` — owns the **drill-hazard protocol** (confirm-before-firing, snapshot, repair,
  keep-or-delete)
- `/dr-forecast-variance` — variance analysis with Excel context mode; its Step 2b confirms layout
  before any write (see §7's stride trap)
