---
name: dr-drilldown
description: Drill down on a cell in the Datarails Excel Add-in to see underlying detail — also the skill to use when the user asks to "explain the variance", "explain this number", "what's driving this", "what's behind this cell", or break a figure into its line items. In a live Excel context (add-in agent bridge available) DR formula cells drill through the add-in's own drill-down; with an .xlsx file (Claude Code) it resolves DR.GET formulas, reads hidden "dr control" filters, queries Datarails, and validates totals; with no workbook at all, the user can paste a DR.GET formula, describe the data point, or give structured filters (no-file mode). Self-contained — discovers the client's financials table and fields on its own, no profile or setup step required.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__list_business_metrics
  - Read
  - Write
  - Bash
  - Glob
  - Grep
  - AskUserQuestion
  - execute_office_js
argument-hint: "<cell-reference> [--by <field1,field2,...>] [--file <path-to-xlsx>]"
---

# DR.GET Drill-Down

Drill into any cell that contains Datarails data to see the underlying line-item detail. Works with:
- Cells containing a **DR formula** directly (`DR.GET`/`DR.QTD`/`DR.YTD`/`DR.MTD`/… — any DR function)
- Cells containing an **Excel formula** (SUM, +, -, etc.) whose precedents are DR formula cells

**Three paths.** In a **live Excel context** (add-in agent bridge available — Claude for Excel / an open workbook with the add-in), drilling a DR formula cell goes through the **add-in's own drill-down** via the agent bridge (Step 0 below) — the add-in resolves filters, dates, and totals natively. (Excel context is about the bridge being present, not whether the workbook is connected.) The MCP/openpyxl workflow (Phases 0–5) is the **file fallback** for Claude Code with an `.xlsx` file and no bridge. And with **no workbook at all**, **no-file mode** (below) takes a pasted DR.GET formula, a plain-language description, or structured filters straight from chat.

**Requirements (fallback path only):** the MCP/openpyxl workflow requires Python with openpyxl to read Excel formulas. If not installed, run `pip install openpyxl`. The fallback path runs in Claude Code (not Cowork). The Excel-context path needs no Python.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<cell-reference>` | The cell to drill down on, e.g. `B6` or `Sheet1!B6` | **Required** for the Excel-context and file paths (not used in no-file mode) |
| `--by <fields>` | Fields to break down by (e.g. `Account Full,Vendor`). **MCP/openpyxl fallback** accepts a comma-separated list (multiple `dimensions`). **Excel-context agent pivot** (`drilldown_by_pivot`) takes **exactly one** field — pass the single field as `rowField`; if multiple are given, use the first and tell the user the others aren't supported in one pivot. | All available fields (fallback) / first field (agent pivot) |
| `--file <path>` | Path to the `.xlsx` workbook file | Ask user (omit for no-file mode: pasted formula / description / structured filters) |

## Verify Connection

If any Datarails tool call fails with an authentication or connection error, tell the user:

> The Datarails connector isn't connected. Click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**.

Then STOP — do not retry until the user has reconnected.

## Workflow

### Step 0 - Excel context routing (ALWAYS FIRST)

Decide which path to take **before** opening any file.

Detect Excel context via the **guard** delegation point of the global Excel Context
Contract (see CLAUDE.md — do not probe `agent.get_session` inline).

- **Excel context active** (guard returns `excel_context: true` — live workbook + add-in bridge):
  **Delegate DR formula cells to the add-in agent drill-down. Do NOT use the openpyxl/MCP path below.**
  1. Resolve the target cell address (`sheetName` + `cellAddress`) from the user's reference / current selection.
  2. Confirm the cell holds a DR formula (`DR.GET`/`DR.QTD`/`DR.YTD`/`DR.MTD`/… — any DR function), directly or via a formula chain whose precedents are DR cells. If it's a static value or a non-DR formula with no DR precedents → tell the user drill-down needs a DR cell; stop.
  3. Fire the add-in agent drill-down (via the Excel Add-In bridge — see the Excel Context Contract in CLAUDE.md):
     - **default / list breakdown** → `drilldown_list` (`sheetName`, `cellAddress`; `timeoutMs: 180000`)
     - **break down by a field** (`--by` / pivot) → `drilldown_by_pivot` (`sheetName`, `cellAddress`, `rowField`; optional `targetTemplateId`/`targetTemplateName`). **`rowField` is exactly one field** — if `--by` listed several, pass the first and tell the user a pivot drills one field at a time.
  4. The add-in resolves `dr_control` filters, dates (EOMONTH), and totals **natively** — do not re-derive them. Present what the bridge returns (cite `data.sources[]`). **Skip Phases 0–5.**

  **Connection:** `drilldown_*` requires the workbook connected. **Let the Excel-context connector handle this gate** (per the Excel Context Contract) — its Connection requirement checks `isConnected` (a COM-only field; no gate on Flex) and prompts for explicit `connect_file` confirmation when needed. Do not probe or branch on `isConnected` here.

- **No Excel context, file provided** (guard returns `excel_context: false` — Claude Code with `--file`, no bridge): use the MCP/openpyxl workflow (Phases 0–5 below).

- **No Excel context, no file** (the user pasted a formula or described a number in chat): use **no-file mode** (next section) — skip Phases 0–2 entirely.

See the **Excel Context Contract** (CLAUDE.md) for the bridge protocol, drill-down commands, and gating.

### No-file mode — chat-only intake (no workbook)

The user has no workbook open and no `.xlsx` to hand over — they paste or describe what to drill. Gather the DR.GET parameters from one of three intakes:

- **Intake A — pasted DR.GET formula.** Parse dimension/value pairs from the pasted string with the Step 1.3 pattern (`"[DimensionName]"` followed by its value). Values arrive as literals here (no cell references to resolve) — strings or numbers. Dimension names come from the client's own workbook/schema; match each parsed dimension to the fields discovered in Phase 3.
- **Intake B — plain-language description.** e.g. "Break down January 2026 Actuals Revenue." Map the description to dimension filters via discovery (Step 3.1): the account-like term binds to the discovered account field at the discovered P&L grain, the scenario term is validated against the discovered scenario domain, the period term becomes an advanced date filter. Ask a clarifying question when the mapping is ambiguous — never guess silently.
- **Intake C — structured filters.** e.g. "Scenario=Actuals, Account Group L1=Revenues, Reporting Date=2026-01" (illustrative — the client's own field names). Take the pairs as given, then validate each field name and value against the discovered schema / distinct values before querying.

Then ask whether any **global add-in filters** (entity / reporting-unit / department-style) were active where this number came from — there is no `dr control` sheet to read in this mode, so global filters can only come from the user. If they're unsure, proceed without them and note in the output that totals may differ from their Excel if global filters are active.

Continue at **Phase 3** (discovery + query) and present per **Phase 5**. **Phase 4 validation is limited here:** with no cached workbook value to check against, validate only if the user states the expected total — otherwise label the result "not validated against a workbook value".

### Phase 0 - Open the Workbook

1. If `--file` was provided, use that path. Otherwise ask the user for the workbook path.
2. Ensure openpyxl is available. If not, install it: `pip install openpyxl`.
3. Read the workbook using Python (openpyxl) via Bash to list sheet names.
4. Confirm the target sheet exists (from the cell reference or default to the active sheet).

### Phase 1 - Resolve the Cell to DR.GET Parameters

**Goal:** Determine which DR.GET dimension filters produce the number in the target cell.

#### Step 1.1 - Read the Target Cell Formula

Use openpyxl with `data_only=False` to read the formula string from the target cell.

#### Step 1.2 - Classify the Formula

| Cell Content | Action |
|-------------|--------|
| Contains `DR.GET` | **Direct DR.GET** - parse dimension pairs. Go to Step 1.3. |
| Other formula starting with `=` | **Derived formula** - find precedent cells, check each for DR.GET. Go to Step 1.4. |
| Static number (no formula) | Tell the user this cell has no formula. Cannot drill down. Stop. |

#### Step 1.3 - Parse a DR.GET Formula

Extract all dimension/value pairs from the formula string. A DR.GET formula has the pattern:

    =DR.GET(Value, "[Dim1]", CellRef1, "[Dim2]", CellRef2, ...)

For each `CellRef`, resolve it to the actual value in that referenced cell. Open the workbook twice: once with `data_only=True` (to get cached values for referenced cells) and once with `data_only=False` (to get formulas).

Use this regex to parse dimension pairs from the formula string:

    pattern = r'"\[([^\]]+)\]"\s*,\s*(\$?[A-Z]+\$?\d+)'

For each match, group(1) is the dimension name and group(2) is the cell reference. Strip `$` from the cell reference and read the cached value from the `data_only=True` workbook.

This produces a dict like (illustrative — dimension names come from the client's own workbook):

    {
      "Account Group L1": {"ref": "$A6", "value": "Revenues"},
      "Scenario": {"ref": "$B$1", "value": "Actuals"},
      "Reporting Date": {"ref": "B$5", "value": 46053}
    }

Store this as the **resolved DR.GET parameters** for this cell. Go to Phase 2.

#### Step 1.4 - Trace a Derived Formula to its DR.GET Precedents

If the cell contains a non-DR.GET formula (e.g. `=B6+B7-B8`), extract all cell references from the formula and recursively check each one.

Use regex to extract cell references: `r'(?<![A-Z])(\$?[A-Z]+\$?\d+)'`

For each referenced cell:
- If it contains a DR.GET formula, parse it per Step 1.3 and record it as a leaf node with its cached value.
- If it contains another non-DR.GET formula, recurse into it.
- If it is a static value, skip it.

Build a tree structure where:
- Each leaf is a `drget` node with `params` (resolved dimensions) and `cached_value`
- Each non-leaf is a `derived` node with `formula` and `children`
- The root is the target cell

**Important:** When the target is a derived formula, the drill-down will produce **one breakdown table per DR.GET leaf**. Inform the user which DR.GET sources contribute to the number and show the breakdown for each.

**Important:** When extracting cell references from SUM ranges like `=SUM(C6:C9)`, expand the range into individual cell references: C6, C7, C8, C9. Do not treat `C6:C9` as two separate references.

### Phase 2 - Read the "dr control" Hidden Sheet for Global Filters

The Datarails Excel Add-in stores global filters in a hidden worksheet named **"dr control"** (or similar names like "DR_Control", "drcontrol"). These filters restrict what data DR.GET returns - the drill-down MUST account for them.

#### Step 2.1 - Find the Control Sheet

Search all sheet names for any containing "control" (case-insensitive). Common names: `dr control`, `DR_Control`, `drcontrol`.

#### Step 2.2 - Extract Filter JSON

The control sheet stores filter configuration as JSON strings in cells. Scan all cells for JSON content containing `FilterStorageValues`.

Each cell may contain a JSON array or object. Parse it and look for objects that have a `FilterStorageValues` key.

#### Step 2.3 - Parse Filter Definitions

Each filter object has this structure (values shown are illustrative — your org's fields and values will differ):

    {
      "Key": "global",
      "FilterStorageValues": [
        {
          "Id": 1234567,
          "Name": "Reporting Unit",
          "Type": "Text",
          "Values": ["Unit A"],
          "AllValues": [null, "Unit A", "Unit B", "Unit C", "Unit D"],
          "IsExcluded": false,
          "IncludeNullValues": true
        }
      ]
    }

Parse each filter and build a list of **active global filters**:

| Filter Property | Meaning |
|----------------|---------|
| `Name` | The field/dimension being filtered |
| `Values` | Selected values (whitelist) |
| `AllValues` | All possible values for this field |
| `IsExcluded` | If true, `Values` is an exclusion list (blacklist) |
| `IncludeNullValues` | Whether rows with NULL in this field are included |

**If `Values` equals `AllValues`** (or `Values` is empty and `IsExcluded` is false), the filter is not restricting anything - skip it.

**If `Values` is a proper subset of `AllValues`** and `IsExcluded` is false, this is an active filter:

    Active filter: "Reporting Unit" IN ["Unit A"]

**If `IsExcluded` is true**, the filter means everything EXCEPT these values:

    Active filter: "Reporting Unit" NOT IN ["Unit C", "Unit D"]

Store all active filters - they must be applied to the drill-down query in Phase 3.

### Phase 3 - Query Datarails for the Breakdown

Now build and execute the aggregation query using the resolved DR.GET parameters + global filters from the control sheet.

#### Step 3.1 - Discover the financials table and its fields

This skill is **self-contained**: it discovers the table and the field
mappings it needs inline. **If you already discovered them earlier in THIS
conversation, reuse them — skip to Step 3.2.** Discovery is cheap but not
free; do it once per conversation, then carry the values forward.

1. `list_data_models`. Pick the financials table: the one whose name (or
   alias) matches `/financial|cube|p&?l|ledger|gl/i`; if none match, the
   largest by row count. Note **both** its numeric `id` (call it
   `<financials_table_id>`) and its `alias` (may be empty). **Prefer the alias
   path when an alias exists** — friendlier field names, far fewer tokens.

2. Fields. If the table has an alias, `list_aliased_fields(<alias>)`;
   otherwise `get_fields_by_id(<financials_table_id>)` (capture each field's
   numeric `id` — the by-id tools address fields by id). From the fields, bind
   the ones this skill uses by case-insensitive match on the alias/name
   (respecting the noted type):
   - `<amount_field>` — numeric: `^amount$` → `transaction_amount` → `value`
     (the metric the breakdown sums)
   - the categorical fields you'll break down by (see Step 3.2)

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

   The DR.GET dimension names parsed from the workbook formula in Phase 1 are
   already the client's literal field names, so use them as-is in the
   aggregation `filters`; only fall back to schema matching if one isn't an
   exact field name.

**Aggregation-field failures are handled reactively, not pre-probed.** If the
Step 3.3 aggregation call 500s on a dimension field, re-inspect the schema for
a sibling account-level field from the discovered schema (orgs often carry
in-between levels, or `account_group_l1`-style twins) and retry — this is also
a likely cause of a total mismatch in Phase 4. If an
alias call fails, fall back to the by-id twin.

#### Step 3.2 - Determine Drill-Down Dimensions

If the user supplied `--by <fields>`:
- Use those fields as the `dimensions` for the aggregation query.

If no `--by` was supplied:
- Use the fields from Step 3.1 to find all categorical fields that are NOT already pinned by the DR.GET parameters.
- Common useful drill-down dimensions (name hints — match against the discovered schema): `Account Name`/`Account Full`, `DR_ACC_L2`-style account levels, `Vendor`, `Department L1`/`Department L2`, `Reporting Unit`, `Entity`.
- Ask the user which fields they want to break down by, suggesting the most useful ones.

#### Step 3.3 - Build the Aggregation Query

Combine:
1. **DR.GET dimension filters** (from Phase 1) - these become `filters` on the aggregation
2. **Global filters from dr control** (from Phase 2) - these become additional `filters`
3. **Drill-down dimensions** (from Step 3.2) - these become `dimensions` on the aggregation
4. **Metric:** `SUM` on `<amount_field>` (the value field discovered in Step 3.1)

Build a filters list (alias path):
- For each DR.GET parameter: `{"name": "<dim>", "values": ["<value>"], "is_excluded": false}`
- For each active global filter: `{"name": "<Name>", "values": <Values>, "is_excluded": <IsExcluded>}`

(By-id path: use `{"field_id": <int>, "values": [...]}` instead.)

**Aggregation rules:**
- Date fields (`Reporting Date`, `Reporting Month`, etc.) can be filtered
  directly with an **advanced** filter — pass an inclusive range as
  `{"name": "<Reporting Date>", "values": {"type": "advanced", "val":
  [{"condition": "total_range", "value": ["<start_epoch>", "<end_epoch>"]}]}}`
  (epoch seconds as strings). Alternatively, add the date as a `dimension` and
  filter the results client-side after the response — both work.
- Text fields (`Scenario`, `Account Group L0`, etc.) use value-list filters.

Then call `get_aggregated_data_by_alias` (preferred when the table has an alias):

    get_aggregated_data_by_alias(
        alias="<financials_alias>",
        dimensions=["<drill-down-field-1>", "<drill-down-field-2>"],
        metrics=[{"field": "<amount_field>", "agg": "SUM"}],
        filters=<combined_filters>
    )

By-id fallback (no alias): `get_aggregated_data_by_id(table_id="<financials_table_id>",
dimensions=[<drill-down-field-id-1>, <drill-down-field-id-2>], metrics=[{"field_id":
<amount_field_id>, "agg": "SUM"}], filters=<combined_filters>)`.

**Important:** Use `get_aggregated_data_by_alias` / `get_aggregated_data_by_id` (not
`get_data_by_alias` / `get_data_by_id`) because aggregation has NO row limit and returns
properly computed totals. The row-fetch tools cap at 500 rows and would return incomplete data.

#### Step 3.4 - Handle Derived Formulas (Multiple DR.GET Sources)

If the target cell was a derived formula (Phase 1, Step 1.4), run a **separate aggregation** for each DR.GET leaf node. Present each breakdown individually, showing how they combine per the original formula.

Example for `=B6-B7` where B6 = DR.GET(Revenues) and B7 = DR.GET(COGS):
- Query 1: Breakdown of Revenues by the requested fields
- Query 2: Breakdown of COGS by the requested fields
- Show both tables with a note: "Gross Profit = Revenues - COGS"

### Phase 4 - Validate the Total

**This step is CRITICAL. Never skip it.**

After receiving the aggregation results:

1. Sum all the `Amount` values in the drill-down result.
2. Compare this total to the original cell value (cached value from the workbook).
3. Check the match:

| Condition | Action |
|-----------|--------|
| Totals match (within rounding tolerance of $1) | Proceed to present results |
| Totals do NOT match | **DO NOT present the drill-down.** Diagnose the mismatch. |

#### Diagnosing a Mismatch

Common causes and fixes:

| Cause | Diagnosis | Fix |
|-------|-----------|-----|
| **Missing global filter** | The dr control sheet has a filter you did not apply | Re-read the control sheet, check for additional filter cells or sheets |
| **Wrong field mapping** | A dimension name in DR.GET does not match the Datarails field name exactly | Use `list_aliased_fields` / `get_fields_by_id` to verify field names; try a sibling account-level field from the discovered schema (orgs often carry in-between levels) |
| **Date format mismatch** | Reporting Date serial number not matching | Verify the date value and format being sent |
| **IncludeNullValues not applied** | The global filter includes nulls but the query does not | Add a separate query for NULL values in that field and combine |
| **Exclusion filter reversed** | IsExcluded true was not handled correctly | Double-check: if excluded, the values should be in the exclusion list |
| **Multiple control sheet cells** | Filters are spread across multiple cells in the control sheet | Scan ALL cells, not just the first match |

If the mismatch cannot be resolved after 2 attempts:
- Tell the user the exact numbers: "The cell shows X but the drill-down totals to Y (difference of Z)."
- Explain what filters were applied.
- Ask the user if they want to see the partial results anyway, clearly flagged as unvalidated.

### Phase 5 - Present the Results

#### For Direct DR.GET Cells

Show a single table with the drill-down data:

    Drill-down: Cell B6 = $1,234,567 (Revenues, Actuals, Jan-26)
    Active global filters: Reporting Unit = "Unit A"

    | Account Name           | Amount      |
    |------------------------|-------------|
    | Subscription Revenue   | $1,100,000  |
    | Implementation Revenue | $134,567    |
    | **Total**              | **$1,234,567** |

    Total matches cell value.

#### For Derived Formula Cells

Show each component table plus how they combine:

    Drill-down: Cell B8 = $900,000 (Gross Profit = Revenues - COGS)

    Component 1: Revenues (Cell B6 = $1,234,567)
    | Account Name           | Amount      |
    |------------------------|-------------|
    | ...                    | ...         |

    Component 2: COGS (Cell B7 = $334,567)
    | Account Name              | Amount     |
    |---------------------------|------------|
    | ...                       | ...        |

    Gross Profit = $1,234,567 - $334,567 = $900,000

#### Formatting Rules

- Use markdown tables.
- Format numbers with commas and appropriate decimal places.
- Sort rows by absolute amount descending.
- If there are more than 30 rows, show the top 20 and summarize the rest as "Other (N items)".
- Always show the total row at the bottom.
- Always state whether the total matches the original cell value.

## Error Handling

| Error | Action |
|-------|--------|
| Workbook cannot be opened | Ask user to verify path; check file is not open exclusively in Excel |
| openpyxl not installed | Run `pip install openpyxl` and retry |
| Cell has no formula | Tell user: "This cell contains a static value (no formula). Cannot drill down." |
| No DR.GET found in formula chain | Tell user: "This cell formula does not reference any DR.GET cells. Cannot drill down." |
| No control sheet found | Warn: "No dr control sheet found. Proceeding without global filters - totals may not match if filters are applied in the add-in." |
| Table not found in Datarails | No table matched the financials pattern — list the tables found and ask the user which one holds their P&L / financial data |
| Total mismatch after retries | Report the mismatch clearly and offer partial results flagged as unvalidated |

## Examples

All examples are illustrative — DR.GET dimension names, filter values, and figures come from the client's own workbook and schema; your org's will differ.

### Example 1: Direct DR.GET cell

    User: /dr-drilldown B6 --file budget.xlsx

Cell B6 contains `=DR.GET(Value, "[Account Group L1]", $A6, "[Scenario]", $B$1, "[Reporting Date]", B$5)`
- Resolves: Account Group L1=Revenues, Scenario=Actuals, Reporting Date=46053
- Reads dr control: Reporting Unit filter = "Unit A"
- Queries Datarails with all filters, broken down by all available fields
- Validates total, presents full breakdown

### Example 2: Drill down by specific field

    User: /dr-drilldown B6 --by "Vendor" --file budget.xlsx

Same resolution, but only breaks down by Vendor.

### Example 3: Derived formula (Gross Profit)

    User: /dr-drilldown B8 --file budget.xlsx

Cell B8 contains `=B6-B7` where B6 is DR.GET(Revenues) and B7 is DR.GET(COGS).
- Resolves both DR.GET sources
- Runs two separate breakdowns
- Shows both and how they combine to the Gross Profit number

### Example 4: SUM of DR.GET cells

    User: /dr-drilldown C10 --file model.xlsx

Cell C10 contains `=SUM(C6:C9)` where C6-C9 are all DR.GET cells.
- Resolves all four DR.GET sources
- Runs aggregation for each
- Shows combined breakdown with validated total
