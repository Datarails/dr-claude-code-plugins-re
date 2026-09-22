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
argument-hint: "[--type summary|detail|budget|variance] [--year <YYYY>] [--level <field>] [--design datarails-default|ocean|ocean-bs|ocean-cf|ocean-summary|ocean-ebitda|genesis|genesis-bva|plain|<sheet>] [--output <file>] [--file]"
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
| `--type <type>` | Report type: `summary`, `detail`, `budget`, `variance` | `summary` |
| `--year <YYYY>` | Calendar year for date headers | Current year |
| `--output <file>` | Output file path. **Passing it requests file mode** — it is never ignored | `tmp/DR_GET_<type>_<YEAR>.xlsx` |
| `--file` | Request file mode explicitly, without naming a path | Auto-detect (Step 0) |
| `--level <field>` | Account-hierarchy field that drives one P&L row each. Passing it **skips the row-axis half of Step 6.5** | The discovered `<account_l1_5_field>` |
| `--design <preset>` | `datarails-default`, `ocean` (variants: `ocean-bs`, `ocean-cf`, `ocean-summary`, `ocean-ebitda`), `genesis` (variant: `genesis-bva`), `plain`, or the name of a sheet **in the open workbook** to mirror. Passing it **skips the design half of Step 6.5** | Ask (Step 6.5) |

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
   - `<account_l1_5_field>` — `dr_acc_l1.5` → `dr_acc_l1_5` → `account_l1_5` → `dr_acc_l1` → `account_l1`
   - `<account_l2_field>` — `dr_acc_l2` → `account_l2`
   - `<report_field>`     — `report_field` → `report field`
   - `<cycle_field>`      — `scenario cycle` → `scenario_cycle`
   - `<planning_field>`   — `planning scenario` → `planning_scenario`

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   **Also collect the whole account-level ladder, not just the default.** Which level
   the P&L is cut at is the user's call (Step 6.5), so bind a *set* —
   `<account_level_candidates>` — of every field whose alias/name matches an
   account-hierarchy shape, ordered coarsest → finest by the level number in the name:

   - `/^(dr_)?acc(ount)?[ _]?(group[ _]?)?l[ _]?\d+([._]\d+)?$/i` — the numbered levels
     (`dr_acc_l0`, `dr_acc_l_0.5`, `dr_acc_l1`, `dr_acc_l1.5`, `account_group_l2`, …).
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

  1. Datarails default  — the current Datarails brand styling (navy banner, Poppins)
  2. Ocean style        — the Datarails template look: quiet printed statement,
                          hairline gutters, small grey type, K-suffixed thousands
  3. Genesis style      — the Datarails template look: navy title bar on a grey page
                          canvas, blue bold subtotals, management-pack style
  4. Match a sheet in this workbook — name it and I'll mirror its formatting
  5. Plain              — values and number formats only
```

**Offer Ocean and Genesis by name; pick the *variant* yourself.** Both are families of
geometries sharing one formatting vocabulary, and which one applies follows from what is
being built — `ocean` for a P&L, `ocean-bs` for a balance sheet, `ocean-cf` for cash flow,
`ocean-summary` for a one-screen statement summary, `ocean-ebitda` for a wide-label EBITDA
P&L; `genesis` for a P&L, `genesis-bva` **only** for an actual-vs-budget report. Do not make
the user choose between near-identical names; choose the variant from the report type and
say which you used.

`genesis-bva` runs its headings and subtotals a point larger than `genesis` because it
carries a KPI block under Total Revenue. Using it for a plain P&L looks subtly wrong —
headings too large for a sheet with no KPI rows to balance them. **Default to `genesis`.**

**Ocean and Genesis are the shipped Datarails Template Library designs**, extracted from
the real template workbooks and committed as presets in
**`references/report-designs.md`**. Read that file when either is chosen — it carries each
family's formatting vocabulary, its geometries, and the conventions common to both. **Both
looks vary across their own source sheets**, so neither is a single spec: take the base
variant unless the report type calls for another. Offer them by name like this whenever a user asks for
a report; most people do not know the library exists, and "one of our standard looks" is a
better opening than a question about styling.

**Never ask the user to open, download, or fetch another file.** They are working in the
file they have open, and the presets exist precisely so the design needs no external
source. Options 1–3 and 5 need nothing; option 4 reads a sheet **already in this
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

`references/report-designs.md` holds every preset — `datarails-default`, `ocean`,
`genesis`, `plain` — each with its own geometry table and formatting table. **Read it when
the chosen design is anything but `datarails-default`**, and apply one preset whole. Do not
blend two, and do not carry a facet you did not read: half of Genesis over half of Ocean is
neither.

The `ocean-*` and `genesis` presets were extracted from the shipped Datarails Template
Library workbooks, so choosing them is genuinely "build it in the Datarails template style"
— no file to open, nothing to fetch, and no risk of inventing a look and calling it ours.
`KPI for Dashboard` is deliberately **not** a preset (it is a widget-authoring workbook, not
a report design — the reference file says what to tell a user who asks for it by name).

### Option 4: mirroring a sheet in the open workbook

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

### Reporting the design

Step 9 names the design used. For a mirrored sheet, name the sheet and any facet that could
not be carried over (a font that is not installed, conditional formatting, a chart);
for a preset, name the preset. Unreported gaps read as bugs.

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

**Check the defined name before the first formula — and check the token you actually
discovered.** The name to verify is `<value_function>` from Step 2.3, *not* the literal
`Value`: orgs commonly expose several XL functions on the same table (`Value`, `Value_BS`,
`Value_NonGaap`), and validating the wrong one leaves every formula broken while the check
passes. Workbooks authored by the add-in usually already resolve it, but a workbook that
merely *has* the add-in installed may not. Read `workbook.names` via `execute_office_js`
and check **presence and value**, not presence alone:

- **Absent** → add it as a workbook-scoped name referring to the string constant of the
  token (`"<value_function>"`).
- **Present and referring to that string constant** → correct, proceed.
- **Present but referring to something else** — a range, a different literal, a formula —
  → **stop and ask.** This is the dangerous case a presence-only check waves through: the
  formulas will resolve against whatever that name points at, so the block fills with
  wrong numbers and nothing errors. Never silently redefine it; the workbook may depend
  on that name elsewhere. Report what it currently refers to and let the user decide.

Skipping the check risks Excel autocorrecting the token to its built-in `VALUE()`, which
breaks every formula the same way it does in a generated file.

**Placing a single widget vs. writing a grid.** If the user wants one DR value at one
cell in their own sheet, that is not this skill — use the bridge's `add_function_by_id`,
since hand-typing a `=DR.GET(...)` string as a substitute for the insert command is a
documented Do-NOT in the Excel Context Contract. This skill builds a grid (a P&L block is
easily 150+ formulas), where writing the formula strings directly with `set_cell_range` is
the sanctioned path — the contract names `/dr-get-formula` explicitly as a skill that
writes DR.GET formulas into cells — followed by one batched refresh in Step 8-A.

**Number formats and styling** go through `set_cell_range`'s `cellStyles`
(`numberFormat`, `fontWeight`, `backgroundColor`), not the openpyxl calls in the Excel
Formatting block below — that block is file mode's equivalent. **Which** styling depends on
the Step 6.5b answer — a preset from `references/report-designs.md`, or a profile read off
a sheet in this workbook through `execute_office_js`. Under `ocean` / `genesis` the preset's
geometry also moves the label and data columns, so write the block to the preset's grid. The date-serial rule is
identical in both modes: EOM serials with an `MMM-YY` number format.

Then go to **Step 8-A** — the refresh is not optional and not a follow-up task.

#### Step 7-B: File generation with openpyxl

Use Bash to run a Python script (inline or from file) that generates the workbook using openpyxl.

Apply the preset chosen in Step 6.5b from `references/report-designs.md`, geometry
included. File mode cannot offer option 4 (mirroring an open sheet — there is no open
workbook), so on a `--design <sheet>` request in file mode, say that and offer the presets.

**First line of workbook setup — before writing any formula:** add the
`Value` defined name (`wb.defined_names.add(DefinedName("Value",
attr_text='"Value"'))`, see the Syntax Reference). Without it, Excel
autocorrects `Value` to its built-in `VALUE` function on open and every
DR.GET formula in the file breaks.

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

##### `--type variance` (Actuals vs Budget)
- Two formula blocks: Actuals and Budget
- Variance columns (Actual - Budget) as Excel formulas (not DR.GET)
- Variance % columns

#### DR.GET Formula Construction

**Every DR.GET formula must be a bare `=DR.GET(...)` call. No IFERROR, no IF, no ROUND, no wrapping of any kind.**

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
