---
name: dr-reconcile
description: Run independent-source consistency checks across Finance OS data - cross-endpoint agreement, balance-sheet identity, cross-grain roll-ups, and scenario/period integrity. Validates the data pipeline and mappings, not source systems.
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
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--scenario <name>] [--tolerance-pct <#>] [--output <file>]"
---

# Data Consistency Reconciliation

Cross-check Finance OS data against itself using **independently-sourced**
numbers — the same aggregate through two different API families, the
balance-sheet identity, hierarchy roll-ups, and scenario/period checksums.
Every check compares two numbers that arrive by different routes; nothing is
ever compared against a re-read of the same aggregate (which would always
"agree" and prove nothing).

**Honest scope:** these are **data-pipeline & mapping consistency checks**,
not source-system reconciliation. A clean pass means the data in Finance OS
is internally consistent across endpoints, grains, and slices — it does not
prove the numbers match the ERP/GL. State this in the report output too.

Essential for month-end close and financial validation.

## How the checks source their numbers

This skill is **self-contained** — it discovers the client's financials table,
fields, and account categories inline (every Datarails environment names them
differently; there is no saved profile). Do discovery once per conversation,
then carry the values forward.

1. **Discover the financials table and fields.** `list_data_models` → pick the
   table whose name/alias matches `/financial|cube|p&?l|ledger|gl/i`; if
   nothing matches, probe candidates with `get_fields_by_id(<id>)` and pick
   the one carrying amount/scenario/date-like fields (no tool returns row
   counts). Note **both** its numeric `id` and its `alias` (alias may be
   empty — prefer the alias path when present). Then
   `list_aliased_fields(<alias>)` if it has an alias, else
   `get_fields_by_id(<id>)` (capture each field's numeric `id`). Bind by
   case-insensitive match: `amount` (`^amount$` → `transaction_amount` →
   `value`), `scenario` (`^scenario$` → `^version$`), `date` (`reporting_date` →
   `posting_date` → `^date$`), and **every account-hierarchy level field**
   present (names matching `/acc(ount)?.*l\d|account_group/i`, or any field
   whose distinct values look like account groupings) — the checks below need
   at least two adjacent levels. Also bind an entity-like field when one
   exists (`/entity|company|subsidiar|legal/i`) for per-entity slicing. If a
   binding can't be resolved by name (e.g., non-English field names), list the
   discovered fields and ask the user which field plays which role.

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`get_distinct_values_by_alias`/`_by_id`) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

2. **Map the account grains.** From the per-level distinct values pulled in
   the data-scope preamble (item 2) — if `get_distinct_values_by_alias`/`_by_id`
   errors, fall back to `get_data_by_alias(<alias>, select=[<account_field>],
   limit=500)` (or the by-id twin) and dedupe — identify two grains: the
   **balance-sheet grain** is the level whose values look like the
   balance-sheet equation (`/asset|liabilit|equity/i` buckets); the **P&L
   grain** is the level whose values partition P&L flows into
   revenue/COGS/opex-like buckets (`/revenue|sales|income/i`,
   `/cogs|cost of goods|cost of sales|direct cost/i`,
   `/operating|opex|expense|sg&a/i`) — often one level deeper. Then discover
   the parent↔child mapping between the two adjacent levels with one
   aggregate: `dimensions=[<parent_level>, <child_level>]`, metric `COUNT` on
   a **different dense field** (a same-field COUNT of a grouped dimension can
   500). Every child bucket should map to exactly one parent; note any that
   map to several parents or to `[null]`.

## The checks — four independent-source comparisons

All checks run under the same scope: the `--year` window as an **advanced**
date filter — `{"name": <date_field>, "values": {"type": "advanced", "val":
[{"condition": "total_range", "value": ["<jan1_epoch>", "<dec31_epoch>"]}]}}`
(epoch seconds as strings; the by-id twin takes `field_id` instead of `name`)
— and, for checks 1–3, one scenario at a time from the **discovered** scenario
domain. Label every reported number with its period + scenario.

3. **Check 1 — Cross-endpoint agreement.** Run the *same* aggregate through
   both API families over the same table and compare per bucket **to the
   cent**: `get_aggregated_data_by_alias(<alias>,
   dimensions=[<account_field>], metrics=[{"field": <amount_field>, "agg":
   "SUM"}], filters=[<scenario>, <date range>])` vs its by-id twin
   `get_aggregated_data_by_id(<id>, dimensions=[<account_field_id>],
   metrics=[{"field_id": <amount_field_id>, "agg": "SUM"}], filters=[...])`.
   This proves something only because the two calls travel different endpoint
   families (aliased vs raw) — and it is only possible for fields that carry
   **both** an alias and a numeric id (per-field rule above). If the
   load-bearing fields (amount, scenario, account level, date) are not all
   aliased, **skip this check and note the skip in the report** — never fake
   it by running the by-id call twice.

4. **Check 2 — Balance-sheet identity.** At the discovered balance-sheet
   grain: `dimensions=[<bs_level>, <period_field>]` (add the entity-like
   field as a third dimension when one exists), `SUM(<amount>)`. Per period
   (and entity), compare **magnitudes**: `|asset-like|` vs `|liability-like +
   equity-like|`, and report the org's **sign convention as discovered** from
   the data (e.g. whether liability/equity buckets arrive negative) — never
   assumed. Balance-sheet values are *stock*, so evaluate per period; never
   sum them across periods. If income/P&L-like buckets also live at this
   grain, exclude them from the identity, and note that it only closes
   exactly when the model rolls P&L into equity — if it visibly doesn't,
   report `|A|` vs `|L + E + cumulative P&L|` and say which form was used.

5. **Check 3 — Cross-grain consistency.** The P&L-grain buckets must sum to
   their parent bucket at the level above (mapping from step 2). Two
   aggregates over the same scope: `dimensions=[<parent_level>]` with
   `SUM(<amount>)`, and `dimensions=[<parent_level>, <child_level>]` with
   `SUM(<amount>)`. For each parent, the sum of its child rows — **including
   the `[null]` bucket** — must equal the parent's own row to the cent. A
   mismatch means the hierarchy mapping leaks rows (unmapped or double-mapped
   accounts).

6. **Check 4 — Scenario/period integrity.** Two grouped calls over the scoped
   window, **no scenario filter** on either: (a)
   `dimensions=[<scenario_field>]`, (b) `dimensions=[<period_field>]`. In
   each response the labeled group rows (including `[null]`) must sum to the
   appended **keyless grand-total row** (data-scope preamble, item 4) to the
   cent — and the two keyless rows must equal each other, since both describe
   the same unfiltered total. A mismatch means rows are escaping the grouping
   (bad scenario/date values) or the two slicings disagree about what is in
   scope.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to reconcile | — |
| `--scenario <name>` | Scenario for checks 1–3 (must exist in the discovered scenario domain) | actuals-like scenario discovered at runtime |
| `--tolerance-pct <#>` | Variance threshold for the balance-sheet identity (checks 1, 3, 4 compare to the cent) | `5.0` |
| `--output <file>` | Output file path | `tmp/Reconciliation_YYYY_TIMESTAMP.xlsx` |

## What It Validates

Every check compares two **independently-sourced** numbers — two different
endpoint families, two different grains, or a group-by against its own
grand-total checksum. Nothing is compared against a copy of itself.

### 1. Cross-Endpoint Agreement
- Same aggregate via the aliased and the raw by-id API families
- Per-bucket match to the cent
- Skipped (with a note) when per-field alias coverage is too thin

### 2. Balance-Sheet Identity
- |Assets| vs |Liabilities + Equity| per period (and entity)
- Sign convention reported as discovered, never assumed
- Evaluated at the discovered balance-sheet grain

### 3. Cross-Grain Consistency
- P&L-grain buckets roll up exactly to their parent bucket
- Flags unmapped / double-mapped accounts (including `[null]` buckets)

### 4. Scenario/Period Integrity
- Group rows sum to the keyless grand-total checksum
- Scenario-sliced and period-sliced totals agree with each other

**Not validated:** agreement with source systems (ERP/GL), completeness of
the load, or business-metric engine values — the `get_business_metric_*` data
tools are feature-gated and may be absent; `list_business_metrics` (ungated)
may be used only to note in the report which named KPIs exist, never to fetch
values.

## Datarails Brand Styling

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

## DR.GET Formulas — Authoring Contract

If asked to add live / refreshable Datarails formulas (DR.GET) to a generated
workbook, the only valid form is:

```
=DR.GET(Value, "[DimensionName]", CellRef, "[DimensionName]", CellRef, ...)
```

- **Never transliterate an MCP/API call into a formula.** DR.GET takes no
  table, field, or aggregation arguments — `=DR.GET(Value,"financials","Amount","SUM",...)`
  is invented syntax that the Datarails Add-in cannot parse or refresh.
- Dimension names go in square brackets inside quotes (`"[Scenario]"`).
  Dimension values are **always cell references**, never hardcoded strings.
- Date cells referenced by formulas hold end-of-month **date serials**
  computed from the calendar — never raw epoch timestamps from API responses
  (epochs land a day early with a time component and never match).
- Before writing any formula, create the workbook-scoped defined name `Value`
  referring to the string constant `"Value"`
  (`wb.defined_names.add(DefinedName("Value", attr_text='"Value"'))`) —
  otherwise Excel autocorrects the bare token to its built-in `VALUE()` and
  the formula breaks.
- Bare `=DR.GET(...)` only — never wrapped in IFERROR/IF/ROUND.

The get-formula skill (`/dr-get-formula`) is the full reference — parameter
cells, validated dimension values, report layouts. Prefer it for whole formula
workbooks; apply this contract when adding DR.GET formulas to a workbook here.
<!-- end:drget-authoring-contract -->

## Output

Excel report with multiple sheets:

1. **Summary** - Pass/fail/skipped per check, exception count, and the scope
   statement: *"Data-pipeline & mapping consistency checks over \<period\> /
   \<scenario\> — not a source-system reconciliation."* Every figure labeled
   with its period + scenario.
2. **Check 1 - Endpoint Agreement** - alias vs by-id value per bucket, delta
   (or the skip note when alias coverage was too thin)
3. **Check 2 - Balance Sheet** - per-period |A| vs |L+E|, sign-convention note
4. **Check 3 - Roll-Up** - parent totals vs child-bucket sums per parent
5. **Check 4 - Integrity** - group sums vs grand-total checksums
6. **Exceptions** (if any) - deltas exceeding each check's threshold

## Examples

### Reconcile current year (default 5% tolerance)
```bash
/dr-reconcile --year 2025
```

### Strict reconciliation (1% tolerance)
```bash
/dr-reconcile --year 2025 --tolerance-pct 1.0
```

### Reconcile specific scenario
```bash
/dr-reconcile --year 2025 --scenario Forecast
```

### Custom output location
```bash
/dr-reconcile --year 2025 --output reports/reconciliation_2025.xlsx
```

## Use Cases

### Month-End Close
Run after data extraction to validate:
```bash
/dr-extract --year 2025
/dr-anomalies-report --severity critical    # Check quality
/dr-reconcile --year 2025 --tolerance-pct 2 # Validate consistency
```

### Financial Review
Reconcile before presentations:
```bash
/dr-reconcile --year 2025 --scenario Actuals
```

### Audit Preparation
Reconcile with strict tolerance:
```bash
/dr-reconcile --year 2025 --tolerance-pct 0.5
```

## Performance

- Year reconciliation: ~30-60 seconds
- Runs 4 independent-source checks (check 1 may be skipped on thin alias coverage)
- Scalable to large data volumes

## Error Handling

**"Account grain not found"** - Re-run discovery (`list_data_models` → `list_aliased_fields`/`get_fields_by_id` → `get_distinct_values_by_alias`/`get_distinct_values_by_id`) and re-derive the balance-sheet and P&L grains from the discovered level values. There is no profile — discovery happens inline.

**422 on aggregation** - At most one aggregation per field per call (split SUM and AVG of the same field into separate calls); SUM/AVG require a numeric or date field.

**500 on COUNT** - A same-field COUNT of the GROUP BY dimension can 500 — aggregate a different dense field instead (data-scope preamble, item 4).

**"Variance exceeds tolerance"** - Review the exception sheet; re-check the discovered sign convention before treating a balance-sheet delta as real.

**"Incomplete data"** - Run `/dr-extract` to refresh data first

## Related Skills

- `/dr-extract` - Get latest financial data
- `/dr-anomalies-report` - Check data quality
- `/dr-dashboard` - Verify KPI values
- `/dr-insights` - Understand trends driving reconciliation items
