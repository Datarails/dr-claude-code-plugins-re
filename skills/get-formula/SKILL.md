---
name: dr-get-formula
description: Generate Excel workbooks with DR.GET formulas that pull live financial data from Datarails. Creates P&L templates, budget models, and variance reports with validated dimension values. Asks which account level to cut the P&L at and which design to use before building. Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
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
  - mcp__datarails-finance-os__list_xl_functions
  - AskUserQuestion
  - Write
  - Read
  - Bash
  - execute_office_js
  - set_cell_range
  - get_cell_ranges
argument-hint: "[--type summary|detail|budget|variance|balance-sheet|cash-flow] [--year <YYYY>] [--level <field>] [--design datarails-templates|datarails-default|plain|<sheet>] [--output <file>] [--file]"
---

# DR.GET Formula Workbook Generator

Generate Excel workbooks containing DR.GET formulas that pull live financial data from Datarails when opened with the Datarails Excel Add-in.

**DR.GET** is a custom Excel function that bridges Datarails' centralized financial database and Excel-based models. Formulas auto-refresh when the workbook is opened with the add-in active.

> **⚠️ Two output modes — resolve one in Step 0, never guess.** In a **live Excel context**
> (add-in agent bridge available) this skill writes into the **open workbook** and refreshes
> through the agent (**in-sheet mode**, Step 7-A). With no bridge it generates an `.xlsx`
> with openpyxl (**file mode**, Step 7-B). A user who asks for a file — `--file`, `--output`,
> or plain phrasing — gets file mode regardless of the bridge; mutating live cells is never a
> substitute for a file someone asked for. Writing DR.GET formulas and refreshing them is
> **one atomic step** in in-sheet mode: freshly written formulas read `Missing` / `Loading…` /
> `#BUSY!` / `#N/A` until an agent refresh lands, so **never report a value — or call the job
> done — before the refresh and the read-back in Step 8-A**, and never substitute a native
> Excel recalc (it does not pull Datarails data). File mode is exempt: those formulas populate
> when the user opens the file with the add-in.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--type <type>` | Report type: `summary`, `detail`, `budget`, `variance`, `balance-sheet`, `cash-flow` | `summary` |
| `--year <YYYY>` | Calendar year for date headers | Current year |
| `--output <file>` | Output file path. **Passing it requests file mode** — it is never ignored | `tmp/DR_GET_<type>_<YEAR>.xlsx` |
| `--file` | Request file mode explicitly, without naming a path | Auto-detect (Step 0) |
| `--level <field>` | Account-hierarchy field that drives one P&L row each. Passing it **skips the row-axis half of Step 6.5** | The discovered `<account_l1_5_field>` |
| `--design <preset>` | `datarails-templates` (the official Datarails templates, loaded through `report-design`), `datarails-default`, `plain`, or the name of a sheet **in the open workbook** to mirror. Passing it **skips the design half of Step 6.5**. Legacy presets (`ocean*`, `genesis*`) are accepted only when passed explicitly and are never offered | Ask (Step 6.5) |

## Adapting to the client's environment

This skill is **self-contained**: every Datarails environment names its
financials table and fields differently, so it discovers the table, the
field mappings, and the valid dimension values it needs **inline**, as the
first data step of its own workflow (Phase 1, Step 2). It does not depend on
a saved profile, a learn step, or any prior setup. Every value written into
a DR.GET formula is validated against the live table during discovery.

---

## DR.GET Syntax Reference

```
=DR.GET(Value, "[Dimension1]", CellRef1, "[Dimension2]", CellRef2, ...)
```

### Syntax Rules

| Rule | Detail |
|------|--------|
| **Function name** | Always `Value` (no brackets, no quotes) — and the workbook must define the name `Value` (see below) |
| **Dimension names** | In square brackets inside double quotes: `"[Reporting Date]"` |
| **Dimension values** | Always **cell references**, never hardcoded strings |
| **Pair structure** | Every dimension is a `"[DimensionName]", CellRef` pair |
| **Cell references** | Use `$A$1` (absolute), `$A1` (mixed), or `A1` (relative) as appropriate |

### CRITICAL: Pin the `Value` token with a defined name

`Value` is a bare identifier, so Excel parses it as a **defined-name
reference**. Workbooks authored by the Datarails Add-in resolve it; a
workbook generated from scratch does not — and Excel autocorrects the
unknown token to its built-in `VALUE` function, silently turning
`=DR.GET(Value, …)` into Excel's `VALUE` formula and breaking it for the
add-in.

Neutralize this by creating a workbook-scoped defined name `Value` that
refers to the string constant `"Value"`, immediately after constructing the
workbook:

```python
from openpyxl.workbook.defined_name import DefinedName
wb = openpyxl.Workbook()
wb.defined_names.add(DefinedName("Value", attr_text='"Value"'))  # openpyxl >= 3.1
```

With the name defined the token resolves, Excel has nothing to autocorrect,
and the formula text is preserved exactly as the add-in expects. Never skip
this step, and never quote the token in the formula instead — `"Value"` as a
string literal diverges from the canonical form the add-in recognizes.

### Date Dimension

`[Reporting Date]` requires **Excel serial date numbers** (end-of-month), NOT text strings.

**How to calculate EOM serial dates:**
```python
from datetime import date
EXCEL_EPOCH = date(1899, 12, 30)
# January 2026 EOM = Jan 31, 2026
serial = (date(2026, 1, 31) - EXCEL_EPOCH).days  # = 46053
```

Store the serial number as the cell value and apply `'MMM-YY'` number format so it displays as "Jan-26" while DR.GET reads the numeric serial.

### Common Mistakes to Avoid

| Mistake | Correct Approach |
|---------|-----------------|
| Writing formulas without the `Value` defined name | Add the workbook-scoped name `Value` = `"Value"` first — otherwise Excel autocorrects the token to its `VALUE()` function |
| Transliterating an MCP/API call into the formula: `=DR.GET(Value,"financials","Amount","SUM",...)` | DR.GET takes no table/field/aggregation arguments — only `"[Dimension]", CellRef` pairs after `Value` |
| Hardcoding values in DR.GET: `"Actuals"` | Always reference a cell: `$B$1` |
| Using text month: `"January 2026"` | Use EOM serial number: `46053` |
| Writing API epoch timestamps as date headers | Compute EOM serials from the calendar (see Date Dimension) — raw epochs land a day early with a time component |
| Using `[Account]` or `[Month]` | Use the actual field names discovered in Step 2 |
| Using Report_Field without scoping | Always include the L2 account dimension discovered in Step 2 alongside `[Report_Field]` |
| Inventing or guessing dimension values | Validate against actual distinct values first |
| Assuming a scenario value like `"Budget"` exists | Use only scenario values discovered in Phase 2 — many orgs model budget as a forecast-like scenario plus `Scenario Cycle` + `Planning Scenario` |
| Wrapping DR.GET in IFERROR/IF/other functions | DR.GET must be bare: `=DR.GET(...)` only |
| Adding fallback values for missing data | Let DR.GET return empty/0 — users need to see gaps |
| Pointing to cells that don't contain data | Every cell reference must point to an actual parameter or header cell |

### CRITICAL: DR.GET Formulas Must Be Simple

**NEVER** wrap DR.GET formulas in any other Excel function. Write them as bare formulas only.

```
WRONG:  =IFERROR(DR.GET(Value, "[Scenario]", $B$1, ...), 0)
WRONG:  =IF(DR.GET(Value, ...) > 0, DR.GET(Value, ...), "")
WRONG:  =ROUND(DR.GET(Value, ...), 2)
RIGHT:  =DR.GET(Value, "[Scenario]", $B$1, "[Account Group L1]", $A6, "[Reporting Date]", B$5)
```

(Dimension names here are illustrative — always use the dimension names discovered from the client's own workbook/schema.)

**Why:** The Datarails Add-in manages DR.GET formulas. Wrapping them in other functions breaks the add-in's ability to refresh, track, and drill down on them. If data is missing, the cell should show 0 or empty — this is valuable information that users need to see, not mask.

**Cell references must be intentional.** Every cell reference in a DR.GET formula must point to a specific cell that contains a validated parameter value (scenario name, account name, date serial). Never generate references to empty cells or cells outside the data layout.

---

## Workflow

### Phase 0: Mode selection

#### Step 0: Excel context routing (ALWAYS FIRST)

Before discovery, before any data pull, decide where the workbook is going to be
written. Run the `agent.get_session` probe through the bridge. **`agent.get_session`
is not an MCP tool** — you run it by executing Office.js via the `execute_office_js`
tool to write the request to the `__dr_agent` sheet and read the response (see the
Excel Context Contract in CLAUDE.md, §Transport). Do **not** call the
`datarails-finance-os` MCP connector for this, and **never infer bridge availability from
the user's wording** — only the probe establishes Excel context. Their wording does decide
one thing, below: whether they asked for a file.

**Resolve the mode in this order — the user's stated intent outranks the probe.**

1. **Did the user ask for a file?** `--file`, `--output <path>`, or any phrasing that
   names a file, a path, or a download ("generate a workbook", "send me the xlsx") is a
   **file-mode request**. Never silently satisfy it by mutating the open workbook
   instead — writing live cells is not a substitute for handing someone a file.
2. **Probe `agent.get_session`.** On success, branch on login state exactly as the
   contract specifies: **Flex** (response has `isLoggedIn`) — if `false`, tell the user
   to sign in to Datarails and stop; **COM** (no `isLoggedIn`, exposes `isConnected`
   instead) — a successful probe means the session is active, proceed. Do **not** gate
   on `isConnected`; DR-formula writes and refresh both work on an unconnected workbook.

   > **A failed probe is a normal result, not an error.** It is how this step detects
   > "no bridge here", and in Claude Code — where there is no add-in — it is the
   > *expected* outcome. Do not surface it to the user, do not retry it, and do not
   > treat it as an authentication or connectivity problem: Step 1's Connectors UI
   > guidance is about the `datarails-finance-os` connector and does **not** apply to
   > this probe. Record the result and move on to the resolution table.
3. **Resolve:**

| User asked for | Bridge probe | Bash available | → Mode |
|---|---|---|---|
| nothing specific | succeeds | — | **In-sheet** (Step 7-A) |
| nothing specific | fails | yes | **File** (Step 7-B) |
| a file | — | yes | **File** (Step 7-B) — say the open workbook was left untouched |
| a file | — | **no** | **Stop and say so** (below) |
| nothing specific | fails | **no** | **Stop and say so** (below) |

**When file mode is required but unreachable, say it plainly and stop.** File generation
needs a Python runtime (`Bash` + `openpyxl`), and **Claude for Excel has neither** — so a
file request on that surface cannot be honoured. Tell the user exactly that, and offer
the two real options: write the report into the open workbook instead (in-sheet mode), or
re-run the skill from Claude Code where file output works. Do **not** quietly downgrade to
in-sheet mode, and do **not** produce a partial or fake file.

> **A sheet list containing `__dr_agent` means the add-in is loaded and in-sheet mode
> is the expected path.** It is a strong signal, not a substitute for the probe — still
> run `agent.get_session`, because only the probe distinguishes a live listener from a
> bridge sheet left behind in a saved file.

**In-sheet mode changes three things**, and each has bitten before:

| | In-sheet mode (Step 7-A) | File mode (Step 7-B) |
|---|---|---|
| Destination | A **new sheet** in the open workbook, block at A1 | A new `.xlsx` |
| Write path | `set_cell_range` | openpyxl via Bash |
| After writing | **Mandatory** agent refresh, then read-back (Step 8-A) | Nothing — formulas populate on open |
| `<value_function>` defined name | Verify presence *and* value; add via Office.js if absent | Always add with openpyxl |

**There is no Bash in a live Excel context.** Once in-sheet mode is resolved, do not plan
an openpyxl script, a temp file, or a `python3` call — those tools do not exist on that
surface, and a run that ends in a file is not the deliverable that mode produces.

### Phase 1: Setup

#### Step 1: Verify Authentication
```
If a datarails-finance-os connector call fails with a connection error, guide the
user to connect via Connectors UI.
```

**Scope:** this applies to the MCP connector calls from Step 2 onward. It does **not**
apply to the Step 0 bridge probe — a failed `agent.get_session` means "no add-in here"
and has already been handled as mode detection.

#### Step 2: Discover the financials table and its fields

**If you already discovered the financials table and its field mappings
earlier in THIS conversation, reuse them — skip to Phase 2.** Discovery is
cheap but not free; do it once per conversation, then carry the values
forward.

1. `list_data_models`. Pick the financials table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Note **both** its numeric `id` (call it
   `<financials_table_id>`) and its `alias` (call it `<financials_alias>`; the
   alias may be empty). **Prefer the alias path when an alias exists** —
   friendlier field names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<financials_alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each field's
   numeric `id` — the by-id tools address fields by id). From the fields, bind
   these by case-insensitive match on the field alias/name (respecting the
   noted type). Only the fields this skill actually puts into formulas are
   needed:
   - `<amount_field>`     — numeric: `^amount$` → `transaction_amount` → `value`
   - `<scenario_field>`   — categorical: `^scenario$` → `^version$`
   - `<date_field>`       — date/timestamp: `reporting_date` → `posting_date` → `^date$`
   - `<account_l1_5_field>` — `dr_acc_l1.5` → `dr_acc_l1_5` → `account_l1_5` → `account group l1.5` → `dr_acc_l1` → `account_l1` → `account group l1` → `account_group_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2` → `account group l2` → `account_group_l2`
   - `<report_field>`     — `report_field` → `report field`
   - `<data_type_field>` — `data type` → `data_type` (**`--type cash-flow` only**)
   - `<kpi_field>` — `dr_kpi` → `dr kpi` → `kpi` (**`--type cash-flow` only**)
   - `<account_group_l1_field>` — `^dr_acc_l1$` → `account group l1` → `account_group_l1` (cash flow's
     Net Income, and Phase 3B's preferred balance-sheet/P&L split)
   - `<account_group_field>` — `^dr_acc_l2$` → `account group l2` → `account_group_l2` → `account group` (**`--type balance-sheet` only**; it supplies the
     balance-sheet sections. If it is absent the balance sheet cannot be built — say so
     rather than substituting an account-level field, whose values are P&L groups)
   - `<cycle_field>`      — `scenario cycle` → `scenario_cycle`
   - `<planning_field>`   — `planning scenario` → `planning_scenario`

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   **Also collect the whole account-level ladder, not just the default.** Which level
   the P&L is cut at is the user's call (Step 6.5), so bind a *set* —
   `<account_level_candidates>` — of every field whose alias/name matches an
   account-hierarchy shape, ordered coarsest → finest by the level number in the name:

   - `/^(dr_)?acc(ount)?[ _]?(group[ _]?)?l[ _]?\d+([._]\d+)?$/i` — the numbered levels
     (`dr_acc_l0`, `dr_acc_l_0.5`, `dr_acc_l1`, `dr_acc_l1.5`, `dr_acc_l2`, …).
     Sort on the number, so a half-level lands between its neighbours.
   - `<report_field>` and the leaf account fields (`account name`, `account id`) — the
     fine end of the ladder, after the numbered levels.

   Orgs carry different subsets: one exposes `L0`…`L3`, another only `L1`/`L2`, another an
   in-between half-level. **Never assume a fixed ladder** — the set is whatever this
   schema returned, and hardcoding `L1`/`L2` as the alternatives is exactly the
   client-specific assumption the plugin's Critical Rules forbid.
   `<account_l1_5_field>` stays the **default** pick, not the only one.

   If `<amount_field>` or `<scenario_field>` has no clear match, ask the user
   which field to use, then continue. The cycle / planning / report fields
   are only needed for `--type budget`, `--type variance`, and `--type
   detail`; if they're absent and the requested report type doesn't use them,
   ignore them.

3. Discover the DR.GET function token. `list_xl_functions`. Each entry's
   `name` is the exact token DR.GET expects as its **first** argument
   (`=DR.GET(<FunctionName>, "[Dimension]", CellRef, …)`), and its
   `template.id` is the owning table — match the function whose `template`
   resolves to `<financials_table_id>`, and bind its `name` as
   `<value_function>`. Most environments name it `Value`; do not assume that —
   use the discovered token. (If `list_xl_functions` returns nothing usable,
   fall back to `Value`, the canonical default the add-in resolves.) Wherever
   this skill writes the literal `Value` token below, substitute
   `<value_function>`; the defined-name guidance in the Syntax Reference
   applies to whatever token you use.

The valid dimension **values** for these fields (account categories,
scenarios, cycles, planning scenarios) are discovered and validated in
Phase 2 below — every value written into a DR.GET formula must come from the
live table.

**Aggregation-field failures are handled reactively, not pre-probed.** If a
later aggregation call (used in Phase 2 for value discovery) 500s on a
dimension field, re-inspect the Step 2 schema for a sibling account-level
field from the discovered schema (orgs often carry in-between levels, or an
`account_group_l1`-style alternative) and retry with it; if an alias call
fails, fall back to the by-id twin.

### Phase 2: Dimension Discovery & Validation

**CRITICAL: Every value used in a DR.GET formula must be validated against the live Datarails table.**

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~50 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. On aggregations the top-level `totals` field is **unaffected by truncation** (computed across all groups, not just the returned prefix) — read grand totals from it instead of re-fetching. Narrow the query (fewer dimensions, more filters, fewer selected columns — or a business metric for a named KPI) and re-fetch **only when the rows themselves are needed** beyond the cap; with `totals` present, a SUM/COUNT/MIN/MAX grand total never requires a re-fetch or chunking by dimension (AVG, COUNT_UNIQUE and UNIQUE_VALUES never read `totals` — true average = SUM total ÷ COUNT total from two calls; true distinct count = the distinct-values tools). A truncated response **without** `totals` (pre-rollout cache) cannot answer a grand-total question from its prefix. Re-run the aggregation **once** — a fresh run may miss the stale entry and return `totals`. If the re-run still carries no `totals`, stop re-running and fall back to narrowing or chunking by dimension until the responses are complete, then sum those rows. Never total the prefix.

#### Step 3: Discover Account Hierarchy

Use the financials table (alias or id) and the fields discovered in Step 2.

**Run the distinct call across `<account_level_candidates>`, not just the default field.**
Step 6.5a offers the user each level *with the row count it would produce*, and these are
those counts — one `start_distinct_values_*` per candidate, the same call shown below. It
is a handful of cheap parallel calls, and without them the question degenerates into asking
someone to pick a field name blind. If a candidate's call errors, drop it from the offered
list rather than guessing its size — and if only one candidate survives, skip 6.5a's
question and say which level you used.

Discover the account values directly from the distinct-values API:
```
# Alias path (preferred)
start_distinct_values_by_alias(<financials_alias>, <account_l1_5_field>)
start_distinct_values_by_alias(<financials_alias>, <account_l2_field>)
# By-id fallback (no alias)
start_distinct_values_by_id(<financials_table_id>, <account_l1_5_field_id>)
# → poll get_distinct_values_result_by_alias(handle) / get_distinct_values_result_by_id(handle) until ready (async-fetch pattern)
```
If a distinct call errors, fall back to sampling rows and collect the values
client-side:
```
get_data_by_alias(<financials_alias>, select=[<account_l1_5_field>, <account_l2_field>], limit=500)
#   (or get_data_by_id(<financials_table_id>, select=[<account_l1_5_field_id>, ...], limit=500))
#   → distinct <account_l1_5_field> values, distinct <account_l2_field> values
```

If you need exact totals or a fuller value set, aggregation also surfaces the
distinct values as group keys:
```
start_aggregation_by_alias(<financials_alias>, dimensions=[<account_l1_5_field>], metrics=[{"field": <amount_field>, "agg": "SUM"}])
#   (or start_aggregation_by_id(<financials_table_id>, dimensions=[<account_l1_5_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]))
# → poll get_aggregation_result_by_alias(handle) (or get_aggregation_result_by_id) until ready (async-fetch pattern)
```
(If this 500s on `<account_l1_5_field>`, swap to a sibling per Step 2's
reactive-retry note; if the alias call fails, fall back to the by-id twin.)

#### Step 4: Discover Scenario Values

Collect the distinct values for the scenario dimensions with
`start_distinct_values_by_alias(<financials_alias>, <scenario_field>)` (or the
by-id twin) → poll `get_distinct_values_result_by_alias(handle)` until ready
(async-fetch pattern). For `--type budget` / `--type variance` you also need
`<cycle_field>` and `<planning_field>` values; do the same distinct call for
each, or confirm them via aggregation:
```
start_aggregation_by_alias(<financials_alias>, dimensions=[<scenario_field>], metrics=[{"field": <amount_field>, "agg": "SUM"}])
#   (or start_aggregation_by_id(<financials_table_id>, dimensions=[<scenario_field_id>], metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}]))
# → poll get_aggregation_result_by_alias(handle) (or get_aggregation_result_by_id) until ready (async-fetch pattern)
# and likewise for <cycle_field>, <planning_field> when the report type uses them
```

#### Step 5: Map Parent-Child Relationships (for detail reports)

For `--type detail`, discover which child values belong to which parent. The **parent is
`<row_level_field>`** and the child is the next-finer entry in `<account_level_candidates>`
— the L1.5 → L2 pair below is the default case, not the only one:
```
# For each L1.5 value, find which L2 values belong to it
# (<actuals_scenario> = the actuals-like scenario value discovered in Step 4)
start_aggregation_by_alias(
  <financials_alias>,
  dimensions=[<account_l1_5_field>, <account_l2_field>],
  metrics=[{"field": <amount_field>, "agg": "COUNT"}],
  filters=[{"name": <scenario_field>, "values": [<actuals_scenario>], "is_excluded": false}]
)
#   (by-id twin: start_aggregation_by_id(<financials_table_id>,
#    dimensions=[<account_l1_5_field_id>, <account_l2_field_id>],
#    metrics=[{"field_id": <amount_field_id>, "agg": "COUNT"}],
#    filters=[{"field_id": <scenario_field_id>, "values": [<actuals_scenario>]}]))
# → poll get_aggregation_result_by_alias(handle) (or get_aggregation_result_by_id) until ready (async-fetch pattern)
```

For Report_Field detail, also map L2 → Report_Field relationships.

#### Step 6: Build Validated Value Registry

Store all discovered values in a dict structure (illustrative — your org's values will differ):
```python
registry = {
    "account_l1_5": ["Revenues", "COGS", ...],  # from live API
    "account_l2": {"Revenues": ["Income"], "S&M": ["Marketing", "Sales", ...], ...},
    "report_fields": {"Sales": ["Events", "Payroll & Benefits", ...], ...},
    "scenarios": ["Actuals", "Forecast"],
    "scenario_cycles": ["0+12", "1+11", ...],
    "planning_scenarios": ["Actuals", "Bottom up", "Budget", ...]
}
```

**Every value in the workbook MUST come from this registry. Never hardcode or guess values.**

#### Step 6.5: Confirm the row axis and the design — ask, once, before building

Discovery is done and nothing has been written yet. Two choices shape the whole
deliverable, and both have historically been made silently on the user's behalf.
**Ask them together, in one `ask_user_question` turn, then build** — the same
clarifying-turn discipline `CLAUDE.md` mandates for grid layout, and for the same reason:
both are decided before a cell is written because changing either afterwards means
rebuilding, not reformatting. One turn, not two round trips.

**Skip the question when the answer is already known:**

| Situation | Do |
|---|---|
| `--level` / `--design` passed | Honour it, don't re-ask that half |
| User already said it in prose ("P&L by L2", "match my Quarterly P&L tab") | Honour it, don't re-ask that half |
| Already answered earlier in THIS conversation | Reuse it — don't re-ask on the second report |
| No interactive user (autonomous / scheduled run) | Take both defaults, and **say in the final report which defaults you took** |

##### (a) Which level should each P&L row be?

Default is `<account_l1_5_field>` — the level this skill has always used, and the right
answer for most summary P&Ls. Offer the rest of `<account_level_candidates>` alongside it,
**with the row count each would produce**, so the choice is concrete rather than a guess
about someone else's naming convention. You already have those counts: they are the
distinct-value sets from Step 3, so extend Step 3's distinct call across the candidates
(it is one `start_distinct_values_*` per field, the same call you already make).

Present it as the shape of the report, not as a schema quiz — illustrative, your org's
ladder and counts will differ:

```
How should I cut the P&L?

  1. Level 1.5 — 14 rows  (default — Revenues, COGS, S&M, R&D, G&A, …)
  2. Level 1   — 5 rows   (coarser: Revenue, COGS, OpEx, Finance, Tax)
  3. Level 2   — 47 rows  (finer: Marketing, Sales, Salaries, Rent, …)
  4. Report Field — 130 rows (finest — long report; consider --type detail instead)

Or say a field name if you have another in mind.
```

Bind the answer as **`<row_level_field>`** and carry it forward. Everything downstream —
Step 3's value set, the row labels, the DR.GET row dimension, the report-type layouts —
uses `<row_level_field>`, not `<account_l1_5_field>`.

**Three things that must follow the chosen level, not the default:**

1. **The calculated lines.** Gross Profit / Total OpEx / Operating Income / Net Income are
   Excel formulas over *named row groups* (see Calculated Lines below). Those groups were
   implicitly the L1.5 names. At another level the same lines still exist but sit over
   different row sets — re-derive which rows roll into each subtotal from the chosen
   level's own values, and if you cannot map them confidently, **write the line items and
   say which subtotals you left out** rather than emitting a `SUM` over a guess. A
   plausible-but-wrong Total OpEx is worse than a missing one.
2. **Row count sanity.** Past ~60 rows a "summary" P&L is not a summary. Say so and offer
   `--type detail` (which nests children under parents) instead of silently emitting a
   150-row block.
3. **`--type detail`'s parent/child pair.** Step 5 maps parent → child. The parent is
   `<row_level_field>`; the child is the **next finer** candidate in the ladder, not
   hardcoded L2. If `<row_level_field>` is already the finest candidate, there is no child
   level — say so and build the summary shape.

##### (b) Which design?

```
And how should it look?

  1. Datarails template   — the official Datarails report templates (P&L, balance sheet,
                            cash flow, financial statement summary): exact layout, colours
                            and logo
  2. Datarails default    — the current Datarails brand styling (navy banner, Poppins)
  3. Match a sheet in this workbook — name it and I'll mirror its formatting
  4. Plain                — values and number formats only
```

**This skill builds all three statements.** `--type summary` / `detail` / `budget` /
`variance` are P&L; `--type balance-sheet` is the balance sheet (Phase 3B);
`--type cash-flow` is the indirect-method cash flow (Phase 3C). **Never build one
statement and label it as another** — if a statement's required dimensions are missing
from the org's schema, say so and stop.

**Offer the official Datarails templates first, by that name.** Which template applies follows from what is being built: a P&L, a balance sheet, a cash flow, a one-screen statement summary or KPI cards. Choose it from the report type and say which you used. Most people do not know the library exists, so "one of our standard Datarails templates" is a better opening than a question about styling.

**Picking a Datarails template means its colours and logo, not a monochrome skeleton.** The banded header, fills, borders and logo *are* the look — apply them exactly as `report-design` specifies, and do not ship a stripped version and call it the template. If a facet genuinely cannot be applied on the surface (no `shapes` API for the logo, Poppins not installed), say which, rather than quietly omitting it.

The older Ocean and Genesis looks (`references/report-designs.md`) are legacy: never offer them in the menu or by name; use them only when the user passes `--design ocean*` or `genesis*` explicitly.

**A Datarails template look in the open workbook → also load `report-design`.** The companion
skill **`report-design`** is a router to self-contained template skills (the official DR SC Style set: P&L EBITDA, Balance Sheet, Cash Flow, Financial
Statement Summary, KPIs for Dashboard), each carrying an exact,
build-tested spec per sheet (every width, height, fill, border, logo as base64, conditional format).
Invoke it **before writing the first cell**; it names the template skill to read for the request
(`read_skill` in Claude for Excel, the Skill tool in Claude Code). **Never ask the user to attach or
open a template file** — the specs are inside the plugin. Where a template skill and the preset below
disagree on grid, fills, borders, widths, heights or logo placement, **the template skill wins**.
`report-design` supplies design only — discovery, `<row_level_field>`, the DR.GET formulas and the
refresh stay here. If it is unavailable, say so and fall back to the preset; do not guess the look.
A look or statement with no template skill still uses the presets in `references/report-designs.md`.

**Never ask the user to open, download, or fetch another file.** They are working in the
file they have open, and the presets exist precisely so the design needs no external
source. Options 1, 2 and 4 need nothing; option 3 reads a sheet **already in this
workbook** via `execute_office_js` (see below). There is no sixth option that involves the
user going and getting something — if a template is not one of the presets, say so and
offer the closest one rather than sending them to the Template Library.

**Geometry travels with the preset.** Every Datarails-template preset puts labels outside
column A (B for most, C for `ocean-summary`), starts data at D or E, and drives period
headers off a `DR_DATE_PICKER` name rather than `$B$1`–`$B$3` parameter cells — so the
Phase 3 Cell reference map's `$A{row}` becomes `$B{row}`/`$C{row}` and the header rows
move. Derive every reference from the chosen variant's geometry row; never mix one
variant's map with another's grid. This is the one place the Cell reference map is a
**variable, not a constant** — safe only because each variant states its whole grid, so
references stay derivable rather than guessed.

**Building a balance sheet under `ocean-bs` or `ocean-summary`? Carry the balance check.**
Those templates end with a silent `ABS(assets - liabilities&equity) < 1` guard. It is one
cell and it is the cheapest possible detection of a row grouping that dropped or
double-counted a line.

## Datarails Brand Styling — the `default` design

This is the design used when the user picks **Datarails default** in Step 6.5 (or when no
one is there to ask). If they picked a report to mirror, this section is superseded by the
extracted profile — see the next section.

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

## Applying a design

`references/report-designs.md` holds every preset — `datarails-default`, the `ocean`
family, the `genesis` family, `plain` — each with its palette, band structure, geometry and
formatting. (For a Datarails template look in the open workbook, the `report-design` template skills take
precedence — see Step 6.5b — and their build traps apply on top of the order below.) **Read it when the chosen design is anything but `datarails-default`**, and
apply one preset whole. Do not blend two, and do not carry a facet you did not read: half
of Genesis over half of Ocean is neither.

### A preset is fills, heights and images — not fonts and number formats

**This is the step that has actually failed in production.** A run applied the fonts and
the number formats, skipped the fills, the row heights and the logo, and reported the
Ocean look as delivered. What the user saw was black text on white, and they said so:
*"it doesn't look like Ocean design"*, *"design colors and logos are still missing"*,
*"there are no colors"*. Fonts are the least visible half of these designs.

Apply a preset in this order, and do not report until all five are done:

1. **Column widths**, including the hairline gutters. They are structural — a 0.4-wide
   gutter carrying a navy rule is what separates one period block from the next.
2. **Row heights** for the header band and its thin spacer rows. Ocean's 4.5 / 3.75 / 8.25
   spacers are what make the bands read as bands rather than as one striped mass.
3. **Merges, then fills.** Each variant's table lists its **merged ranges** — recreate
   them first (`sh.getRange("D1:G1").merge()`), because a merged range renders with its
   *anchor* cell's fill. Then fill **every cell in the block** — bands, page canvas,
   gutters, spacer rows, white data cells, subtotal stripes. *Every* cell: an unfilled
   cell renders Excel white and punches a hole in the card. Fill by range, not cell by
   cell.
4. **Fonts, colours, indents, borders, number formats** per the preset's formatting table,
   then the **Layout hygiene** rules in that file: group labels centred across their block
   (Center Across Selection, not a merge), a scenario-row header on **every** column
   including Δ and % Δ, and **no helper columns on the report sheet**.
5. **Logos** from `references/assets/`, at native size. **Both families have one** —
   Ocean places two (a white mark on the navy band plus a footer), Genesis places one
   (the wordmark, in its *header*, and **not** Ocean's white mark, which is invisible on
   Genesis's light canvas). Never scale them — a stretched logo was a specific user
   complaint. See **Logos** in the preset file for which asset goes where.

**The band tables show rendered fills, with merges already expanded.** A row that reads
`A:N 001F37` is a solid navy band — paint the whole span and merge what the table says to
merge. (Reading the source workbooks directly reports merged cells as unfilled, which once
put white gaps in the title band; the tables correct for that, so trust them over a raw
read.)

**Each variant has its own band table — read yours.** `ocean`'s spacer heights, rule
column and data-cell white are not shared: `ocean-ebitda` has no rule at all, `ocean-bs`
uses a different white and two rules, `ocean-cf` puts its rule elsewhere and keeps
gridlines on, `ocean-summary` has no title band, and `genesis` leaves its report body
**unfilled** on purpose. "Paint the page" against a design that paints nothing is as wrong
as dropping a banner. The tables are generated from the source workbooks and verified against
them; `--` in one means *no fill*, which you must not paint.

**Colours in the preset file are already resolved hex.** Do not re-derive them from the
source workbooks: Ocean's palette lives in the workbook *theme*, and openpyxl reports theme
colours as `None`, which is precisely how the palette got dropped the first time. The
reference file documents the trap; the hexes there are correct as written.

The `ocean-*` and `genesis` presets were extracted from the shipped Datarails Template
Library workbooks, so choosing them is genuinely "build it in the Datarails template style"
— no file to open, nothing to fetch, and no risk of inventing a look and calling it ours.
`KPI for Dashboard` is deliberately **not** a preset (it is a widget-authoring workbook, not
a report design — the reference file says what to tell a user who asks for it by name).

### Option 3: mirroring a sheet in the open workbook

Only when the user named a sheet **in the workbook they already have open**. Read a
representative slice with `execute_office_js` — the header rows, one label cell, one data
cell, one subtotal row, the date-header row — and capture: grid origin, header/banner rows,
fonts per role, fills, number-format strings, totals treatment, indentation, date format,
column widths, gridlines and freeze position. That slice characterises the look and is
cheap; reading the whole sheet is not.

**Copy the design, never the content.** Take formatting, geometry and number formats. Do
**not** copy the source's row labels, values or formulas — rows come from
`<row_level_field>`'s validated registry, every number from a fresh DR.GET. A mirrored
report that inherits the source's hardcoded account names is wrong even when it looks
right.

If the named sheet is not in this workbook, say so and offer the presets — do not ask the
user to go open it.

### Verify the design before you report it

**Read the block back and compare it against the preset — do not report a design from the
instructions you intended to follow.** This is not the generic write-then-read rule; it is
specific, because a design failure is invisible to a value read: every number can be right
while the sheet looks nothing like the template. A run that skipped this told the user the
design matched, and was told *"not true"*, then *"now look at the template and check if it
matches"*.

Read back, for a representative slice (a band row, a spacer row, a gutter cell, an item
row, a data cell, a subtotal row):

| Check | Fails as |
|---|---|
| Band rows carry the band fill | black-on-white header |
| Body cells carry the page fill | patchy white holes in the card |
| Data cells carry the data fill | data does not stand out from the page |
| Subtotal rows carry their stripe | totals read as ordinary rows |
| Gutter column carries its rule | period blocks run together |
| Row heights match the band table | bands look like one striped mass |
| Fonts, colours, indents, formats | wrong family / everything black |
| Logo present and at native size | missing, or stretched |

Then **report what you actually observed**, naming the preset and variant. State any facet
you could not apply — a font that is not installed, an image the surface cannot insert —
rather than leaving it to be discovered. Never describe a design as matching the template
on the strength of having written the instructions; say what you read back. If a check
fails, fix it and re-read before reporting.

For a mirrored sheet, the same applies against the source sheet's own facets.

When a `report-design` template skill supplied the spec, walk **its** checks as the read-back and read
the properties back (font name on each merged anchor, border edges on one item row,
`columnWidth` in points) rather than trusting a screenshot.

### Phase 3: Workbook Generation

Run **either** Step 7-A **or** Step 7-B, per the mode chosen in Step 0. Everything
after them in this phase — report-type structure, formula construction, calculated
lines — is shared by both modes.

#### Step 7-A: In-sheet generation (Excel context)

Write into the open workbook with `set_cell_range`. No Bash, no openpyxl, no file.

**Always a new sheet, block anchored at A1. No exceptions.** This is a correctness
constraint, not a layout preference. The formula patterns and the Cell reference map
below are written against that origin (`$B$1` = Scenario, `$B$2` = Cycle, `$B$3` =
Planning Scenario, row 5 = date headers, column A = row labels). On a new sheet at A1
every documented reference is correct as written, the destination is guaranteed empty,
and nothing pre-existing can be overwritten or disturbed.

**Writing into an existing sheet is not supported.** If the user asks for the block at a
named sheet or anchor, say so plainly and put it on a new sheet instead — they can cut
and paste it wherever they want afterwards, and Excel will carry the references with it.
Do not improvise an offset layout: every literal in the Cell reference map would then
point at whatever the workbook already holds there, filling the block with plausible,
incorrect numbers while nothing visibly fails.

**Clean up after yourself.** If you place scratch or probe cells anywhere while working,
clear them before you report — a stray cell left in someone's live template is a defect
even when the numbers are right.

**Register the function through the bridge before the first formula — do not hand-create
a defined name here.**

> **This is the "all zeros" bug.** Creating a workbook name `Value = "Value"` by hand makes
> the formulas *parse*, so nothing errors — but no widget is registered, every DR cell
> refreshes to **0**, and `evaluate_drget` returns `Widget not found: 'Value'`. Numbers that
> are silently zero are worse than a visible failure. The openpyxl defined-name step is
> **file mode only**.

In-sheet, work through this in order. **The token to check is `<value_function>` from
Step 2.3, not the literal `Value`** — orgs commonly expose several XL functions on one
table (`Value`, `Value_BS`, `Value_NonGaap`), and checking the wrong one leaves every
formula broken while the check passes.

**Step 0 — classify any existing name.** Read `workbook.names` via `execute_office_js`
and check presence *and* what it refers to. **The value it points at is what tells you
whether it is healthy** — presence alone says nothing:

| `<value_function>` name | Meaning | Do |
|---|---|---|
| **Absent** | normal before registration | Go to step 1. **Never add it in-sheet.** |
| Refers to a **`widget_<id>_…` token** | **the add-in wrote it** when it registered the widget — healthy | **Leave it alone.** Go to step 1; the probe will confirm it resolves. |
| Refers to the **literal `"<value_function>"`** (e.g. `Value` → `"Value"`) | the hand-made trap, probably from an earlier run | **Report it and remove it**, then go to step 1 |
| Refers to **anything else** — a range, a formula | unknown | **Stop and ask.** Formulas would resolve against whatever it points at, so the block fills with wrong numbers and nothing errors. Report what it refers to and let the user decide. |

> **Measured on a live add-in (2026.9.0.70, catalog v1.14.0):** registering with
> `add_function_by_id {registerOnly: true}` creates the workbook name `Value` pointing at a
> **`widget_<functionId>_…` string**, not at the literal `"Value"`. Treating any existing
> name as the trap would therefore halt on every workbook the add-in has already set up.
> Distinguish by the **value**, not by presence.
>
> **And "absent" is the rare case, not the common one.** The same workbook carried ~120
> such names — the add-in registers the org's whole XL-function catalog, including the
> sibling tokens this skill already warns you to tell apart (`Value`, `Value_BS`,
> `Value_NonGaap`). Expect to find your token already there and healthy; check the one
> named `<value_function>` and ignore the rest. The probe in step 1, not this step, is
> what decides whether registration is needed.

**Step 1 — probe before registering.** Many workbooks already have the widget registered —
anything authored by the add-in does. Write **one** DR cell to a scratch location, refresh
it, and read it back (or use `evaluate_drget`):

- **Resolves to a number** → the widget is registered. **Skip registration entirely**,
  clear the scratch cell, and go on to the grid.
- **Reads `#VALUE!`** → not registered. With no widget behind the token, Excel autocorrects
  the bare `<value_function>` to its built-in `VALUE()` and the cell errors; an add-in
  refresh does **not** repair it. *(Measured: this, not `0`, is what a fresh workbook
  actually shows.)* Go to step 2.
- **Reads `0`, or `evaluate_drget` reports `Widget not found`** → also not registered.
  Go to step 2.

**Clean up what the probe leaves behind.** A probe that hit `#VALUE!` leaves Excel's own
artifacts in `workbook.names` — a hidden `_xleta.VALUE` resolving to `#NAME?`, and
`_xlfn.*` entries once `IFERROR` and similar are written. Delete the probe cell and any
`_xleta.*` name you created; leave `_xlfn.*` alone, as Excel manages those.

**Step 2 — register through the bridge.** Resolve the `functionId` for `<value_function>`
from the connector's `list_xl_functions` (it carries the owning `template`, so you can
confirm the function belongs to `<financials_table_id>`) or from `agent.list_functions`.
Then send **`add_function_by_id`**, **confirming first** — it is on the
confirm-before-mutating list in the Excel Context Contract.

- If the catalog you fetched via `agent.get_skill` exposes a **register-only flag**, use it:
  the add-in registers the widget without inserting a formula. **Take the exact parameter
  name from that catalog** — it is generated from the running add-in and is the authority.
  *(Confirmed present on add-in 2026.9.0.70 / catalog v1.14.0 as
  `add_function_by_id {functionId?, functionName?, registerOnly?}`; a successful call
  replies `done` with `tokenName` and `formulaInserted: false` — check both.)*
- If it does not, send a **plain `add_function_by_id` into a scratch cell**. Inserting the
  function registers the widget just the same; then clear the cell under the
  "Clean up after yourself" rule above. **Do not stop merely because the flag is absent**,
  and never fall back to hand-creating the name.

**Step 3 — verify.** Refresh and read one cell back. A number means the widget resolved; a
`0` means it did not — go back to step 2 rather than writing 150 more formulas on top of a
broken token.

**Placing a single widget vs. writing a grid.** If the user wants one DR value at one
cell in their own sheet, that is not this skill — use the bridge's `add_function_by_id`,
since hand-typing a `=DR.GET(...)` string as a substitute for the insert command is a
documented Do-NOT in the Excel Context Contract. This skill builds a grid (a P&L block is
easily 150+ formulas), where writing the formula strings directly with `set_cell_range` is
the sanctioned path — the contract names `/dr-get-formula` explicitly as a skill that
writes DR.GET formulas into cells — followed by one batched refresh in Step 8-A.

**Number formats and basic styling** go through `set_cell_range`'s `cellStyles`
(`numberFormat`, `fontWeight`, `backgroundColor`), not the openpyxl calls in the Excel
Formatting block below — that block is file mode's equivalent. **Which** styling depends on
the Step 6.5b answer — a preset from `references/report-designs.md`, or a profile read off
a sheet in this workbook through `execute_office_js`. Under `ocean` / `genesis` the preset's
geometry also moves the label and data columns, so write the block to the preset's grid. The
date-serial rule is identical in both modes: EOM serials with an `MMM-YY` number format.

**`cellStyles` alone cannot deliver a Datarails-template preset.** It has no column width,
no row height, no font family or size, no font colour, no indent, no border and no image —
and those are most of what makes Ocean or Genesis recognisable. Everything `cellStyles`
does not cover goes through **`execute_office_js`**, batched by range rather than per cell:

```js
const sh = context.workbook.worksheets.getItem(name);
// Widths in the preset are Excel CHARACTER units; Office.js wants POINTS.
const wPt = ch => (ch * 7 + 5) * 0.75;              // chars -> px -> points
sh.getRange("B:B").format.columnWidth = wPt(32.6);  // 32.6 chars -> ~174.9 pt
sh.getRange("3:3").format.rowHeight   = 4.5;        // heights are ALREADY points - pass as-is
const band = sh.getRange("A1:J2");                  // paint by range, never cell by cell
band.format.fill.color = "#001F37";
band.format.font.name  = "Poppins";
band.format.font.color = "#F7F7F7";
sh.getRange("A9:J60").format.fill.color = "#F7F7F7";  // page canvas, then overlay
sh.getRange("D10:E10").format.fill.color = "#FFFFFF"; // data cells
sh.getRange("I9:I60").format.fill.color = "#001F37";  // the gutter rule
sh.getRange("B10").format.indentLevel = 3;
sh.freezePanes.freezeRows(8);
```

**Widths and heights are in different units — converting one and not the other is the
easy mistake.** The preset's column widths are Excel *character* units (what the UI shows
when you drag a column); `format.columnWidth` is in **points**, so convert with
`(chars * 7 + 5) * 0.75`. Passing the raw number, or multiplying by 7 and stopping, makes
every column roughly a third too wide and the whole block visibly wrong. Row heights need
no conversion: the preset's values are already points, which is what `format.rowHeight`
takes. In **file mode** it is the reverse — openpyxl's `column_dimensions[c].width` takes
the character units verbatim and `row_dimensions[r].height` takes points, so the preset's
numbers go in unconverted on both.

Paint the page canvas as one range first, then overlay the bands, the data cells, the
subtotal stripes and the gutter rule on top. Painting cell by cell is slow enough to look
like a hang on a 150-row block.

**The logo** — every Datarails-template preset has one; see **Logos** in the preset file
for which asset each family uses. Insert with `sh.shapes.addImage(<base64>)`.

**`Shape.width`/`Shape.height` are in POINTS, but the preset states native PIXELS** —
convert with `px * 0.75`, or the logo renders about a third too large, which is exactly the
stretching the "never scale" rule exists to prevent:

```js
const img = sh.shapes.addImage(LOGO_B64);   // base64, no data: prefix
img.width  = 143 * 0.75;                    // native px -> points
img.height = 33  * 0.75;
img.left = ...; img.top = ...;              // over the anchor cell
```

**Getting the bytes.** Reading a PNG with the file tools yields an image, not base64, so
the preset file carries each asset **inline as base64** — copy it from there. The files
under `references/assets/` are the same bytes for file-mode builds, where openpyxl reads
them from disk directly.

If the Excel surface has no `shapes` API, say the logo could not be inserted — do not
substitute a stretched one, a text stand-in, or silence.

Then go to **Step 8-A** — the refresh is not optional and not a follow-up task.

#### Step 7-B: File generation with openpyxl

Use Bash to run a Python script (inline or from file) that generates the workbook using openpyxl.

Apply the preset chosen in Step 6.5b from `references/report-designs.md`, geometry
included. File mode cannot offer option 3 (mirroring an open sheet — there is no open
workbook), so on a `--design <sheet>` request in file mode, say that and offer the presets.

**File mode cannot build the official Datarails templates** (`--design datarails-templates`, option 1): their specs are applied to an open workbook through `execute_office_js`. On that request in file mode, say so and offer to build it in the open workbook; if the user wants a file anyway, use `datarails-default` and say that it is not the official template.

**First line of workbook setup — before writing any formula:** add the defined name for
`<value_function>` (`wb.defined_names.add(DefinedName("<value_function>",
attr_text='"<value_function>"'))`, see the Syntax Reference). Without it, Excel autocorrects
the bare token to its built-in `VALUE` function on open and every DR.GET formula in the
file breaks.

**This is the file-mode half of the token check, and it is the opposite of the in-sheet
rule.** Here you *create* the name, because there is no add-in to register a widget with —
the file resolves when it is opened with the add-in active. In-sheet you must never create
it (Step 7-A). Verify presence *and* value the same way: referring to the string constant
`"<value_function>"` is correct; referring to a range, another literal or a formula means
**stop and ask**, since the formulas would resolve against whatever it points at.

**Workbook Structure by Report Type:**

##### `--type summary` (Summary P&L)
- **Parameter cells** (Row 1-3): Scenario, Scenario Cycle, Planning Scenario
- **Date headers** (Row 5): EOM serial dates formatted as MMM-YY
- **P&L rows** (Row 6+): One row per `<row_level_field>` value (from registry)
- **Calculated rows**: Gross Profit, Total OpEx, Operating Income, Net Income — derived
  from the chosen level's own row groups (Step 6.5a), not from L1.5 names
- **Two sheets**: Actuals, Budget

##### `--type detail` (Departmental Detail)
- Same parameter/date structure as summary
- Rows grouped by `<row_level_field>` parent with the next-finer level's children indented
- Subtotal rows per `<row_level_field>` group

##### `--type budget` (Budget Template)
- Scenario pre-set to the forecast-like scenario value discovered in Step 4
- Scenario Cycle defaults to the current cycle from the registry (e.g. `0+12`, if the org uses cycles)
- Planning Scenario defaults to a planning-scenario value discovered in Step 4
- All `<row_level_field>` line items with monthly columns

##### `--type balance-sheet` (Balance Sheet)

Structure and discovery are in **Phase 3B** below — the row axis is built differently from
every P&L type, so it does not reduce to a row list here.

##### `--type cash-flow` (Cash Flow, indirect method)

Structure and discovery are in **Phase 3C** below.

##### `--type variance` (Actuals vs Budget)
- Two formula blocks: Actuals and Budget
- Variance columns (Actual - Budget) as Excel formulas (not DR.GET)
- Variance % columns

### Phase 3B: Balance-sheet construction (`--type balance-sheet`)

A balance sheet is **not a P&L with different rows.** Three things differ, and each is a
correctness matter rather than a layout preference.

#### The row axis is inverted

In the P&L types the account level supplies the **row labels** and is referenced from the
formula as a cell. In the balance sheet the account group is a **literal** that scopes the
section, and the *line items within it* come from `<report_field>`:

```
=DR.GET(<value_function>, "[<account_group_field>]", "<group literal>",
                          "[<report_field>]", $B{row},
                          "[<date_field>]", {col}$6,
                          "[<scenario_field>]", $D$7)
```

So `<row_level_field>` and the Step 6.5a level question **do not apply** to
`--type balance-sheet`. Skip that half of the question and say so; asking someone to pick a
P&L grain for a balance sheet is a confusing question with no right answer.

#### Discover the balance-sheet groups — never hardcode them

The groups are values of an account-group field (the observed template uses an
`Account Group L2`-style field). **Which values are balance-sheet groups is per-org and
must be discovered**, exactly like every other dimension value in this skill:

1. Take the distinct values of `<account_group_field>` (Phase 2's distinct call).
2. Split balance-sheet groups from P&L groups. Prefer a **structural** signal when the
   schema offers one — a parent level (`L1`/`L0`) or a statement/report-type field whose
   values separate balance-sheet accounts from income-statement accounts. Bind it the same
   way Step 2 binds fields, by case-insensitive match on alias/name.
3. **Only if no structural signal exists**, fall back to matching the group names
   (`/asset/i`, `/liabilit/i`, `/equity/i`). This is a sanctioned runtime heuristic, not a
   hardcoded list — it reads the org's own values and never invents one.
4. Order them **Assets → Liabilities → Equity**, current before non-current within each
   (`/current/i` and not `/non.?current/i` first). If ordering cannot be determined, keep
   the discovered order and say so rather than guessing an accounting sequence.

If step 2 and step 3 both fail to identify any balance-sheet group, **stop and ask** which
groups belong on the balance sheet. Do not build a statement out of every group you found.

#### Check the Data Type dimension before trusting any balance

If the org's schema has a `<data_type_field>` (bind it as Phase 3C does —
`data type` → `data_type`), **the balance-sheet formulas above have no filter on it**, so
each cell is whatever DR.GET's sum over that dimension produces. On the observed tenant
that happens to yield a closing balance, because the data splits into an opening balance
plus period activity and summing them is the balance. **That is a property of that tenant,
not a guarantee.**

So: discover the field's distinct values and check the shape before building.

| What you find | Do |
|---|---|
| No `<data_type_field>` in the schema | Proceed — nothing to filter, the amount column is the balance |
| Exactly an opening-balance value + a movement value (`/beginning\|opening/i` and `/activity\|movement\|delta\|change/i`) | Proceed — their sum is the closing balance |
| Any other shape — movement only, or extra values you cannot classify | **Stop and say so** |

The third case is the dangerous one: with activity only, every figure is a *movement*
presented as a *balance*. It still produces numbers, and the tie-out can pass or fail for
reasons unrelated to the group split — so a passing balance check would be meaningless
rather than reassuring.

#### The three-tier row tree

| Tier | Source | Ocean formatting |
|---|---|---|
| Section (`Assets`, `Liabilities`, `Shareholders' Equity`) | the top-level split from discovery | Poppins 12, indent 0 |
| Sub-section (`Current Assets`, `Long Term Liabilities`, …) | each `<account_group_field>` value | Poppins 10, indent 0 |
| Line item | each `<report_field>` value mapped to that group (Step 5's parent→child call, with the group as parent) | Poppins 8, `7F7F7F`, indent 3 |

Subtotals and totals are Excel formulas, never DR.GET:

| Line | Formula |
|---|---|
| `Total <sub-section>` | `=IFERROR(SUM(<first..last of that group>),"NA")` |
| `Total Assets` | `= <sum of the asset sub-section totals>` |
| `Total Liabilities` | `= <sum of the liability sub-section totals>` |
| `Total Equity` | `= <sum of the equity sub-section totals>` |
| `Total Liabilities & Equity` | `= Total Liabilities + Total Equity` |

Leave a blank row between the last item of a group and its `Total` row, and span the SUM
from the sub-section header row through that blank — the source templates do this, and it
makes an inserted row fall inside the total automatically.

#### The balance check is mandatory here — and blank must not mean "fine"

The source template's tie-out is:

```
=IFERROR(IF(ABS(<total_assets> - <total_liabilities_and_equity>)<1,"","OUT OF BALANCE"),"")
```

**That cell cannot tell "balanced" from "broken."** The subtotals feeding it are
`=IFERROR(SUM(…),"NA")`, so any upstream error — or an `"NA"` text flowing into a `+`
total — makes the tie-out fall to its own `IFERROR` branch and render **blank**, which is
exactly what "balanced" looks like. A broken sheet would be read back and reported as
balanced.

So write it with a **visible** failure branch:

```
=IF(ISNUMBER(<total_assets>)*ISNUMBER(<total_liabilities_and_equity>),
    IF(ABS(<total_assets>-<total_liabilities_and_equity>)<1,"BALANCED","OUT OF BALANCE"),
    "CHECK - totals not numeric")
```

Three distinguishable states, none of them blank.

**And do not rely on that cell alone.** Read back **`<total_assets>` and
`<total_liabilities_and_equity>` themselves**, confirm both are numeric, and compare them
in your own report. A blank or stale tie-out cell then cannot masquerade as a pass. Never
present a balance sheet without stating whether it balanced *and* the two totals you
compared.

#### Signs — one policy, shared with the cash flow

**DR.GET cells stay bare in every statement. All sign handling lives in the Excel
arithmetic that aggregates them, and the sign of each contributing row is visible in that
formula.** This is the single policy for Phase 3B and Phase 3C; neither statement negates a
DR.GET cell.

Two reasons it is the aggregation and not the cell:

- A DR.GET cell returns text sentinels (`Missing`, `Loading…`) before and during refresh.
  Negating one turns that text into `#VALUE!`, which destroys exactly the signal the
  refresh and read-back checks look for — a cell reading `Missing` is diagnosable, a cell
  reading `#VALUE!` is not.
- One policy across both statements means a reviewer does not have to hold two conventions
  in mind, and the line items always sum to their totals as written.

Write the totals so each row's sign is explicit rather than hidden in a blanket negation:

```
Total Liabilities & Equity  = <liab subtotal> + <equity subtotal>          (stored positive)
Total Liabilities & Equity  = -<liab subtotal> - <equity subtotal>         (stored negative)
```

**Which one is a question about the data, not an assumption.** Orgs differ on whether
liabilities and equity are stored negative. After the first refresh, compare `Total Assets`
against the liability + equity side. Equal → stored positive. Equal and opposite → stored
negative; use the second form and **say in Step 9 that you did**. If neither orientation
balances, the problem is the **group split**, not the signs — report the imbalance and the
groups you used. Never flip signs line by line until something ties: that yields a
statement that balances and is still wrong.

#### Period semantics

A balance sheet is a **point-in-time** balance, not a period sum. The source templates pass
a single `<date_field>` value per column exactly as the P&L types do, so the grammar is
unchanged — but the comparison column is a **prior period balance**, not a prior-period
total: `ocean-bs` uses `=EOMONTH(D6,-1)` (prior month), where the P&L variants use `-12`.
Follow the preset's geometry table for which comparison the design expects.

### Phase 3C: Cash-flow construction (`--type cash-flow`)

An indirect-method cash flow, grounded in the shipped `Cash Flow - Ocean style` workbook.
It reuses the balance sheet's group discovery (Phase 3B) and adds two dimensions.

#### Two extra dimensions, both discovered

| Bind | Match on alias/name | Carries |
|---|---|---|
| `<data_type_field>` | `data type` → `data_type` | **movement vs balance.** One value means the period's movement, another the opening balance |
| `<kpi_field>` | `dr_kpi` → `dr kpi` → `kpi` | named metrics (depreciation, cash) that are not account-group lines |

**`DR_KPI` is a dimension, not a function.** The XL function stays `<value_function>`; the
KPI name goes in as a dimension value. Do not look for a second function token.

Discover the `<data_type_field>` **values** with the Phase 2 distinct call — do not assume
their spelling. You need two, identified from the org's own values:

- the **movement** value (the observed template uses `Activity`) — matches `/activity|movement|delta|change/i`
- the **opening-balance** value (observed: `Beginning Balance`) — matches `/beginning|opening/i`

If either is missing, **stop and say which**: without a movement value there is no cash
flow to compute, and a statement built from balances instead of movements would be wrong
in a way that still produces numbers.

Likewise bind `<account_group_l1_field>` (`^dr_acc_l1$` → `account group l1` → `account_group_l1`) and
discover its income-statement values (observed: `REVENUE`, `EXPENSE`) — Net Income is
derived from them. **`revenue - expense` assumes both are stored positive** — the same
assumption Phase 3B forbids making about liabilities. Check it the same way: if the derived
Net Income is the negative of what the P&L reports for the period, the org stores one side
signed, so use `revenue + expense` and say so. If neither form reconciles, report that
rather than picking the one that looks right. This is the same structural signal Phase 3B prefers for splitting
balance-sheet groups from P&L groups; if you found it there, reuse it.

#### Statement structure

| Row | How it is built |
|---|---|
| **Net Income** | two **bare** cells — `DR.GET(…"[<l1>]","<revenue>")` and `DR.GET(…"[<l1>]","<expense>")` — in a scratch column, with `= <revenue cell> - <expense cell>` on the Net Income row |
| Non-cash add-backs | `DR.GET(…"[<kpi_field>]", $B{row})` — the row label *is* the KPI name |
| Working-capital movements | `DR.GET(…"[<data_type>]","<movement>", "[<group>]","<group literal>", "[<report_field>]", $B{row})` |
| **Operating Cash Flow** | `= NetIncome + addbacks + SUM(working-capital rows)` |
| Investing movements | as working capital, over the non-current asset groups |
| **Total Investing** | `= SUM(investing rows)` |
| **Free Cash Flow** | `= Operating + Investing` |
| Financing movements | as working capital, over liability / equity groups |
| **Total Financing** | `= SUM(financing rows)` |
| **Total Cash Flow** | `= Free Cash Flow + Total Financing` |
| Cash — beginning | `DR.GET(…"[<data_type>]","<opening value>", "[<kpi_field>]","<cash KPI>")` |
| Cash — ending | `DR.GET(…"[<kpi_field>]","<cash KPI>")` — **no** `<data_type>` |
| Cash change | `= ending - beginning` |
| **Gap** | `= Total Cash Flow - Cash change` |

#### Signs follow the group — and live in the totals, not the cells

An increase in an **asset** consumes cash; an increase in a **liability or equity**
provides it. **Derive the sign from the discovered group, never from a hardcoded line
list.**

The source template carries the sign with a leading minus on the asset cells
(`=-DR.GET(…)`). **Do not copy that.** DR.GET returns text sentinels (`Missing`,
`Loading…`) before and during refresh, and arithmetic on a text sentinel yields `#VALUE!`
— which the read-back cannot diagnose and which is not treated as transient. A cell
reading `Missing` tells you to re-check a dimension value; a cell reading `#VALUE!` tells
you nothing. This is the same policy Phase 3B uses, and it is why the authoring contract
bans a leading minus alongside `IFERROR`.

So: **every movement cell is a bare DR.GET of the raw movement**, and the subtotal carries
the signs explicitly, one term per row:

```
Operating Cash Flow = <net income> + <addback rows> - <asset movement rows> + <liability movement rows>
Total Investing     = - <non-current asset movement rows>
Total Financing     = + <non-current liability and equity movement rows>
```

Write the terms out rather than `SUM`-ming a range, so each row's sign is visible in the
formula and the line items still tie to the total as displayed.

**Capex:** the template's fixed-asset line also subtracts the depreciation add-back so it
reads as capex rather than gross movement. Keep that as arithmetic in the investing
subtotal (`- <fixed asset movement> - <D&A row>`), not in a cell. If no depreciation
add-back was discovered, use the plain movement and say so.

#### Which group belongs in which section

Left vague, this produces a non-zero Gap that looks like a sign error and is not. Map the
discovered groups explicitly:

| Section | Groups |
|---|---|
| Working capital (inside Operating) | **current** asset groups **excluding cash**, plus **current** liability groups |
| Investing | **non-current** asset groups |
| Financing | **non-current** liability groups, plus equity **excluding current-period earnings** |

Three exclusions, each of which otherwise double-counts and shows up only as a Gap:

- **Cash itself is never a working-capital line.** Its movement *is* what the statement
  explains; including it counts the answer as one of the inputs. Identify the cash group or
  line by the same `<kpi_field>` value used for the beginning/ending balances — discover
  that value by matching `/^cash/i` against the field's distinct values, and if none
  matches, **stop and ask** rather than guessing which line is cash.
- **Current liabilities belong to working capital, not financing.** Financing takes only
  the non-current liability groups.
- **Current-period earnings are already in Net Income.** If the equity groups carry a
  retained-earnings or current-year-earnings value, exclude it from financing or the period
  profit is counted twice. Where the split cannot be determined from the discovered values,
  say so and leave it out, naming what you excluded.

#### The Gap check is mandatory

`Total Cash Flow - Cash change` must be ~0. It is the cash-flow equivalent of the balance
sheet's tie-out and the only self-check this statement has:

- **Read it back and report it**, always — never present a cash flow without saying whether
  it tied.
- A non-zero Gap usually means a movement line was missed, double-counted, or given the
  wrong sign. **Report the gap and the groups you used**; do not flip signs line by line
  until it closes, which produces a statement that ties and is still wrong.

#### Period semantics

Every line except the opening cash balance is a **period movement**, which is what the
`<data_type_field>` movement value selects. The comparison column in `ocean-cf` is the
prior *year* (`EOMONTH(…,-12)`), unlike the balance sheet's prior month — follow the
preset's geometry.

#### DR.GET Formula Construction

**Every DR.GET formula must be a bare `=DR.GET(...)` call. No IFERROR, no IF, no ROUND,
no leading minus, no wrapping of any kind.** Where a statement needs a negated or combined
figure — a cash-flow asset movement, a Net Income built from two pulls — the DR.GET cells
stay bare and the arithmetic goes in the row that aggregates them, with each contributing
sign visible there. See Phase 3C.

**The row dimension is `<row_level_field>` — the level chosen in Step 6.5a.** The patterns
below are written with `{l1_5_field}` because L1.5 is the default; substitute the chosen
field wherever it appears. Getting this wrong is silent: the formula resolves against a
dimension whose values do not match the labels in column A, and the block fills with
`Missing` or, worse, with plausible numbers from the wrong grain.

**Actuals formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{date_field}]", {{col}}$5)'
```

**Budget formula pattern:**
```python
f'=DR.GET(Value, "[{l1_5_field}]", $A{{row}}, "[{scenario_field}]", $B$1, "[{cycle_field}]", $B$2, "[{planning_field}]", $B$3, "[{date_field}]", {{col}}$5)'
```

**Detail formula (with L2 scoping):**
```python
f'=DR.GET(Value, "[{report_field}]", $A{{row}}, "[{l2_field}]", $B{{row}}, "[{scenario_field}]", $D$2, "[{date_field}]", {{col}}$5)'
```

**Cell reference map** — these addresses assume the block's origin is A1, which both
modes guarantee: file mode writes a fresh workbook, and in-sheet mode always writes a new
sheet (Step 7-A). Use them as written; never offset the layout. Each reference in the
formula must point to:
- `$A{row}` → the account/line item label in column A of that row
- `$B$1` → the Scenario parameter cell (e.g., "Actuals")
- `$B$2` → the Scenario Cycle parameter cell (e.g., "0+12")
- `$B$3` → the Planning Scenario parameter cell (e.g., "Bottom up")
- `{col}$5` → the date header in row 5 of that column (EOM serial number)
- `$B{row}` → the L2 scoping value in column B of that row (detail reports)

If a reference doesn't map to one of these known locations, it is wrong. Do not invent references.

#### Excel Formatting

```python
# Date headers: serial number with MMM-YY format
cell.value = serial_number
cell.number_format = 'MMM-YY'

# Financial cells: number format
cell.number_format = '#,##0'

# Parameter cells: clear labels
ws['A1'] = 'Scenario:'
ws['B1'] = 'Actuals'  # validated value from registry

# Calculated rows: Excel formulas (NOT DR.GET)
# Gross Profit = Revenue - COGS
ws.cell(row=gp_row, column=col).value = f'={get_column_letter(col)}{rev_row}-{get_column_letter(col)}{cogs_row}'
```

#### Year-to-date columns

The retrieval family shares one form, so `DR.YTD` is written exactly like `DR.GET`
(`=DR.YTD(<value_function>, "[Dim]", CellRef, …)`) and is covered by the same authoring
contract — bare cell, same `<value_function>`, same reference discipline.

**What is *not* settled here is its date semantics** — which date argument anchors the
year, and whether it follows the fiscal or calendar year. Do not guess: take the signature
from the catalog you fetched via `agent.get_skill`, or from the connector's
`list_xl_functions` entry. If neither states it, use the fallback below and say why.

**Fallback — monthly helpers plus `SUMIFS`.** Build the YTD column from ordinary `DR.GET`
cells rather than a function whose semantics you could not confirm:

1. Create a **separate working sheet**, named for the report (`<report name> - working`),
   with its own header row.
2. Write one bare `DR.GET` per month there, with the month-end serials in a matching header
   range.
3. On the report sheet, bound the sum at **both** ends:
   `YTD = SUMIFS(<helper row>, <helper dates>, ">="&<year start cell>, <helper dates>,
   "<="&<period header cell>)`.

**The year start is a real decision, not a detail.** A `SUMIFS` with only an upper bound is
year-to-date *only* if the helper row happens to begin at the year start — which just moves
the fiscal-vs-calendar question into the helper range instead of answering it. Put the year
start in its own cell and reference it: derive it from the org's fiscal year if the schema
or the workbook states one, and **ask the user if it does not**. Say which you used.

**Do not hide the helpers on the report sheet.** Hidden columns are still inside the
block's used range — they widen copies, surface in exports and print ranges, and reappear
the moment someone unhides a column. See **Layout hygiene** in the preset file.

This is auditable — every figure still comes from a bare DR.GET, and both bounds are
visible cells rather than implied by where a hidden range happens to start. Say in Step 9
that YTD is helper-derived, and which year start it used.

#### Calculated Lines (No DR.GET)

These P&L lines are always Excel formulas referencing other rows. The row groups they span
follow `<row_level_field>` (Step 6.5a) — at a coarser level a subtotal may collapse to a
single line and should be dropped rather than emitted as a `SUM` of one cell; at a finer
level it spans more rows. Never emit a subtotal whose membership you had to guess:

| Line | Formula Pattern |
|------|----------------|
| Gross Profit | `= Revenue_row - COGS_row` |
| Total OpEx | `= SUM(opex_line_rows)` |
| Operating Income | `= Gross_Profit_row - Total_OpEx_row` |
| Net Income | `= Operating_Income_row - Finance_row - Tax_row` |

### Phase 4: Save & Report

#### Step 8-A: Refresh & verify in place (in-sheet mode)

**This step is what makes the formulas real. A grid of `Missing` is a failed run, not
a delivered one — even if every formula is correct.**

1. **Refresh through the agent — `refresh_selected_cells_ribbon`, scoped to the range you
   wrote.** Never `refresh_ribbon` here. Because the block is always a new sheet, that
   scope contains nothing but the cells you just created: no pre-existing value can move,
   and nothing in the workbook can depend on a sheet that did not exist a moment ago. A
   whole-workbook refresh throws that guarantee away — it repulls every DR cell in the
   file, and any that were stale will change, silently editing the user's model as a side
   effect of your write. If the user explicitly wants everything refreshed, that is their
   call to make, not yours to assume.
   **If the refresh command itself fails** — error, timeout, or a listener that never
   returns terminal status — stop and say so. The workbook is now carrying formulas that
   were written but never resolved. Report exactly which sheet and range hold them, state
   that they are unresolved, and offer to remove the sheet or leave it for the user to
   refresh from the ribbon. Do not retry blindly, do not delete their content without
   asking, and do not report the run as finished.
2. **Read the range back** with `get_cell_ranges` and check every DR cell. None of
   these may survive: `Missing`, `Loading…`, `#BUSY!`, `#N/A`, `#VALUE!`. A native
   Excel recalc does not clear them — only an agent refresh does.
3. **If sentinels remain**, do not report success, and do not just refresh again —
   distinguish the two cases first. `Loading…` / `#BUSY!` are transient: wait for the
   refresh command's own terminal status (the bridge command carries its own timeout —
   do not invent a longer wait around it), then re-read. **Bound the retry**: at most a
   couple of re-reads after terminal status. If sentinels still show, treat it as a
   failed refresh and handle it per item 1 — report the range as unresolved and stop.
   Never loop waiting for a value that may never arrive; an in-progress-looking cell
   that never resolves is indistinguishable from a hung listener, and the user is
   sitting in front of the workbook. `Missing` after a refresh that
   completed is **terminal** — the formula resolved to nothing, which almost always
   means a dimension value that doesn't match the live data. Re-check that row's
   values against the registry from Phase 2 and fix the formula; repeating the refresh
   will return the same result. Either way, name the exact cells and the sentinel each
   one shows rather than leaving them for the user to find.
4. **Only values you have read back after a successful refresh may be quoted.** Never
   report a figure sourced from the MCP aggregation you used during discovery as
   though it were the cell's value — if the cell has not resolved, the honest report
   is that it has not resolved.

#### Step 8-B: Save Output & Verify (file mode)

Save to `tmp/DR_GET_<type>_<YEAR>.xlsx` or the user-specified `--output` path.

Then re-open the saved file and verify it before reporting success:

Both assertions check `<value_function>` — the token discovered in Step 2.3 — not the
literal `Value`. On an org whose function is `Value_BS`, hardcoding `Value` here verifies
a name the formulas never use: the check passes and the workbook is broken.

```python
token = value_function            # from Step 2.3; "Value" only if that is what was discovered
check = openpyxl.load_workbook(out_path)
assert token in check.defined_names, f"defined name '{token}' is missing — Excel will autocorrect the token to VALUE()"
for ws in check.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, str) and "DR.GET" in c.value:
                assert c.value.replace(" ", "").startswith(f"=DR.GET({token},"), \
                    f"bad DR.GET formula in {ws.title}!{c.coordinate}"
```

If either assertion fails, fix the workbook and re-save — do not hand the
user a file that fails verification.

#### Step 9: Report to User

Both modes report: number of validated dimension values used, number of DR.GET
formulas written, number of calculated rows.

**Both modes also state the two Step 6.5 choices** — the level the rows were cut at, and
where the design came from. Say it in one line (`Cut at Level 1.5 (14 rows), Datarails
default styling`) so the user can tell at a glance whether they got what they meant, and
name the default explicitly when nobody was there to ask. If a design was mirrored, name
the source sheet or file and any facet you could not carry over; if a subtotal was dropped
because its membership was not derivable at the chosen level, name it here too.

**In-sheet mode** also reports:
- The name of the new sheet and the range the block occupies
- That the refresh ran and the read-back was clean — or exactly which cells still
  show a sentinel, if any do
- If the user had asked for an existing sheet or anchor: that it went to a new sheet
  instead, and that they can cut and paste it where they want
- If the refresh failed: the sheet and range now holding unresolved formulas, and the
  choice offered (remove the sheet, or leave it for a manual ribbon refresh)
- **No** "open this with the add-in to refresh" line — the formulas are already live,
  and telling the user to refresh a range you just refreshed reads as an unfinished job

**File mode** also reports:
- Output file path
- Reminder: "Open this workbook with the Datarails Excel Add-in active to refresh formulas."
- If the file was requested (`--file` / `--output` / plain phrasing) while a live Excel
  context was available, say that the open workbook was deliberately left untouched

---

## Examples

### Summary P&L with Actuals
```bash
/dr-get-formula --type summary --year 2026
```

### Detailed departmental breakdown
```bash
/dr-get-formula --type detail --year 2026
```

### Budget template
```bash
/dr-get-formula --type budget --year 2026
```

### Actuals vs Budget variance
```bash
/dr-get-formula --type variance --year 2026
```

### Cut the P&L at a different level
```bash
/dr-get-formula --type summary --level dr_acc_l2
```

### Build it in a Datarails template design
```bash
/dr-get-formula --type variance --design ocean
```

### Match the design of a sheet already in the open workbook
```bash
/dr-get-formula --type summary --design "Quarterly P&L"
```

### Cash flow in the Datarails cash-flow design
```bash
/dr-get-formula --type cash-flow --design ocean-cf
```

### Balance sheet in the Datarails balance-sheet design
```bash
/dr-get-formula --type balance-sheet --design ocean-bs
```

### Custom output location (file mode)
```bash
/dr-get-formula --type summary --year 2026 --output tmp/PnL_Template_2026.xlsx
```

### Request file mode explicitly
```bash
/dr-get-formula --type summary --year 2026 --file
```

**How the mode resolves.** With a workbook open and the add-in bridge live, the plain
invocations above go to **in-sheet mode** — the block is written into that workbook and
refreshed. `--file` or `--output` is a file request and is never satisfied by writing to
the open workbook instead; where a Python runtime exists (Claude Code) it produces the
`.xlsx` and leaves any open workbook untouched, and where one does not (Claude for Excel)
Step 0 says so and stops rather than substituting a different deliverable.

---

## Troubleshooting

**Every DR cell refreshes to `0`, or every cell reads `#VALUE!`.** Both are the same
root cause: the function is not registered in the workbook. `#VALUE!` is what a *fresh*
workbook shows — with no widget behind the token Excel autocorrects it to the built-in
`VALUE()`, and an add-in refresh does not repair it. A silent grid of `0` is the variant
produced by a hand-made defined name, which satisfies the parser without registering
anything. It is almost always a hand-created `Value` defined name on a live workbook —
that satisfies the formula parser but registers no widget. Confirm with `evaluate_drget`,
which reports `Widget not found: '<token>'`. Fix by registering through the bridge
(register through the bridge — Step 7-A, steps 1-3) and refreshing; remove the hand-made name.
The openpyxl defined-name step is **file mode only**.

**"Not authenticated" error**
- Connect via Connectors UI ("+" > Connectors > Datarails > Connect)

**No table matches the financials pattern in Step 2**
- List the tables you found and ask the user which one holds their P&L /
  financial data, then continue with that table.

**A field can't be bound in Step 2 (e.g. no scenario cycle / planning field)**
- For report types that don't use it, ignore it. For `--type budget` /
  `--type variance`, ask the user which field to use, or fall back to a
  single-scenario formula pattern.

**`Value` turned into Excel's `VALUE` function after opening the workbook**
- The workbook was generated without the `Value` defined name, so Excel
  autocorrected the unknown token to its built-in `VALUE()` function.
- Regenerate with this skill — it now always writes the defined name and
  verifies it after saving. To repair an existing file instead: add a
  workbook-scoped name `Value` referring to `="Value"`, then restore each
  formula's first argument to the bare token `Value`.

**DR.GET formulas return 0 or errors when opened in Excel**
- Verify the Datarails Excel Add-in is active
- Check that dimension values match exactly (case-sensitive, exact spelling)
- Re-run the skill to re-validate values against live data

**Cells written in-sheet still read `Missing` after the refresh**
- `Missing` is the add-in's "this combination resolved to nothing" sentinel, not a
  loading state — a second refresh will not clear it. Check the dimension values in
  that row/column against the Phase 2 registry; a value the live table doesn't carry
  is the usual cause.
- If the refresh itself never ran, that is the bug, not the formula. A native Excel
  recalc (F9, `calculate()`) does not pull Datarails data and leaves `Missing` in
  place. Only an agent refresh through the bridge resolves DR cells.
- Do not report the numbers you pulled during discovery as if they were the cell
  values. They came from the MCP aggregation, not from the sheet, and quoting them
  hides an unresolved grid behind correct-looking figures.

**The user asked for a file but the skill is running in Claude for Excel**
- File generation needs `Bash` + `openpyxl`; that surface has neither, so the request
  cannot be honoured there. Say so and stop.
- Do **not** substitute in-sheet mode — writing into their live workbook is a different
  and irreversible deliverable, not a smaller version of the one they asked for. Offer it
  as a choice, or point them at Claude Code where file output works.

**In-sheet numbers look plausible but are wrong across the whole block**
- Check where the block was written. The formula patterns and Cell reference map assume
  an A1 origin; placed anywhere else, `$B$1` / `$B$2` / `$B$3` / `{col}$5` point at
  whatever that sheet already holds and every cell resolves against the wrong parameters,
  with nothing visibly failing.
- This is why in-sheet mode always writes a new sheet at A1 (Step 7-A). If a block ended
  up in an existing sheet, that path was not followed — rewrite it to a new sheet rather
  than trying to patch the references.

**A refresh changed cells the skill didn't write**
- It should not be possible on this path: in-sheet mode writes a new sheet and refreshes
  only that range, so the scope holds nothing but cells the skill just created, and no
  pre-existing formula can depend on a sheet that did not exist a moment ago.
- If it happened, a whole-workbook `refresh_ribbon` was used instead of
  `refresh_selected_cells_ribbon`. That repulls every DR cell in the file, and any that
  were stale will move — a real change to the user's model. Report every value that
  moved, and use the scoped command next time.

**A distinct-values call errors**
- Use `start_distinct_values_by_alias` / `start_distinct_values_by_id` → poll
  the matching `get_distinct_values_result_by_*` tool until ready (async-fetch
  pattern). If a call errors, the skill falls back to sampling rows
  (`get_data_by_alias` / `get_data_by_id`, small limit) or aggregation group
  keys for value discovery.

**Missing dimension values**
- The live data may not contain all expected categories
- Check with `/dr-query` to investigate the table directly

**Date headers show numbers instead of month names**
- The serial numbers are correct; apply `MMM-YY` number format in Excel
- The generated workbook should already have this format applied
