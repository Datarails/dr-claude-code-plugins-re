---
name: dr-audit
description: Generate an audit-support evidence package over FinanceOS data - completeness, reconciliation, mapping-integrity, and substantive-sample checks with a PDF report and Excel evidence workbook. Not a SOX certification - access-control, change-management, and IT-general-control evidence is out of scope.
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
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> --quarter <Q#> [--output-pdf <file>] [--output-xlsx <file>]"
---

# Audit Evidence Package

Generate an **audit-support evidence package over FinanceOS data** — the
control checks that this data surface can actually evidence, packaged for
management and auditors.

Creates both a PDF report (for management) and an Excel evidence workbook
(for the audit trail).

**Honest scope — read first.** This is *not* a SOX certification. In scope
are the **data-evidencable control families**: completeness & period
integrity, consistency/reconciliation, account-mapping integrity, and
substantive sampling — each backed by a real query this skill can run.
**Access control, change management, and IT general controls are out of
scope**: the FinanceOS MCP surface has no audit-log, access-history, or
user-activity endpoint, so those control families require
system-administration evidence outside this tool's reach. Never present a
control result this skill cannot substantiate with a tool call — the evidence
workbook carries a mandatory "Out of scope — requires external evidence"
sheet so no reader mistakes the package for full SOX coverage.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--quarter <Q#>` | **REQUIRED** Quarter: Q1, Q2, Q3, Q4 | — |
| `--output-pdf <file>` | PDF output path | `tmp/Audit_Report_YYYY_QX_DATE.pdf` |
| `--output-xlsx <file>` | Excel evidence path | `tmp/Audit_Evidence_YYYY_QX_DATE.xlsx` |

## Control Checks (data-evidencable only)

Each check maps to tools this skill can actually call — nothing goes in the
evidence package without a query behind it:

1. **Completeness & period integrity.** Discover the date field's range and
   confirm every expected period in the audited quarter/year is present
   (distinct values of the reporting-month field). Then verify integrity with
   two grouped calls over the audited window — by scenario and by period:
   **sum each response's rows** (including `[null]`) to get that slicing's
   total — responses carry one row per group and no total row (Data-scope
   preamble, item 4) — and the two totals must equal each other, since both
   describe the same window sliced two ways. Tools:
   `start_distinct_values_by_alias`/`_by_id` → poll
   `get_distinct_values_result_by_alias`/`_by_id`, and
   `start_aggregation_by_alias`/`_by_id` → poll
   `get_aggregation_result_by_alias`/`_by_id` (async-fetch pattern).
2. **Consistency / reconciliation.** The reconciliation control is the
   `/dr-reconcile` skill's four independent-source checks — cross-endpoint
   agreement, balance-sheet identity, cross-grain roll-up, and
   scenario/period integrity. That skill's SKILL.md is the single source of
   the **method** (query shapes, tolerance, pass/fail rules) — but its native
   run is **year-scoped** (`--year` is its only window argument), while this
   audit is quarter-scoped. So do not delegate a bare full-year run: apply
   the four checks' method with the date filter narrowed to the **audited
   window** (`--year` + `--quarter`, the same advanced date-range filter used
   by every other family in this evidence package), and record in the
   evidence which window each check actually covered. A full-year
   reconciliation pass does not evidence a Q-scoped control — a
   quarter-local inconsistency can net out over the year.
3. **Account-mapping integrity.** Deliberately reuses the roll-up
   *mechanics* from the reconciliation control's Check 3 — but for a
   different verdict: not "does the pipeline roll up consistently" (that
   pass/fail belongs to check family 2 above) but "which accounts are
   unmapped". Two aggregates over the same scope —
   `dimensions=[<parent_level>]` and `dimensions=[<parent_level>,
   <child_level>]`, both `SUM(<amount>)`, with the **same parameters,
   tolerance, and audited-window date filter as family 2's roll-up check**
   (year + quarter — never the full year) so both comparisons cover the same
   period. Sharing the scope aligns the comparison; it does not make the
   totals agree — a mismatch is exactly the finding. For each parent bucket,
   the sum of its child rows — **including the `[null]` bucket** — must equal
   the parent's own row to the cent.

   **Then name the accounts — the two aggregates above cannot.** They return
   bucket *totals*, so the presence of a `[null]` child bucket tells you a
   parent has unmapped rows, not which accounts carry them. An exception log
   that names no account is not auditable evidence.

   **Trigger on row presence, never on a non-zero amount.** Unmapped rows with
   offsetting positive and negative amounts net to zero, so a `[null]` bucket
   summing to `0.00` can still hold unmapped accounts — gating on the amount
   would silently drop those exceptions from the evidence package. Add a
   **row count** to the family-3 aggregate alongside the sum — `metrics=[{SUM
   of <amount>}, {COUNT of <non_null_row_identifier>}]` — and treat
   **`count > 0`** as the trigger. `SUM(<amount>)` reports the net unmapped
   amount only; it never decides whether to look.

   Choosing `<non_null_row_identifier>` is load-bearing: `COUNT` skips nulls,
   so it must be a field the discovered schema populates on **every** source
   row (a system row id, or the reporting-date field). It must **not** be the
   account identifier or the child level — those are exactly the fields that
   are null on the rows being hunted, so counting them can return `0` while
   unmapped rows exist, reintroducing the miss this rule prevents. It must
   also differ from `<amount>`, since one call may carry only one aggregation
   per field. Verify non-nullness from the field's profile (null rate `0`)
   before relying on it; if no such field exists, fall back to the bounded
   row-level query below and treat any returned row as the trigger.

   For each parent whose `[null]` child bucket contains rows, run one
   follow-up query under the **same period + scenario filters**:
   - *Preferred* — re-aggregate that parent with the account identifier added
     as a dimension: `dimensions=[<parent_level>, <child_level>,
     <account_id_or_name_field>]`, `SUM(<amount>)`, filtered to that parent.
     Read the rows whose `<child_level>` is the `[null]` bucket — those
     accounts, with their amounts, are the exception-log entries.
   - *When row-level proof is wanted* — `get_data_by_alias` /
     `get_data_by_id` with `select` on the account + amount + date columns
     and `filters` scoping that parent, the audited window, and the scenario
     (the `is null` advanced condition isolates the unmapped child set).
     Respect the 500-row cap and the `truncated` envelope, per family 4.

   The exception log records account identifier, parent bucket, amount, and
   the window. The roll-up pass/fail itself is reported once, under family 2 —
   this family reports only the exception list.
4. **Substantive sampling.** For the material buckets (largest by absolute
   amount in the audited window), pull row-level detail via
   `get_data_by_alias` / `get_data_by_id` with `select` on the load-bearing
   columns and `filters` scoping bucket + period, so a human auditor can
   trace reported figures to source line items. Respect the 500-row cap —
   sample per bucket, never attempt a full extract. If a response arrives
   with `"truncated": true`, the returned rows are an incomplete prefix —
   narrow the query per its `guidance` (more filters / fewer columns / lower
   limit+offset paging) and re-fetch; never present the prefix as a complete
   sample.

**Out of scope — requires external evidence:** access control, change
management, and IT general controls. No tool available to this skill can
observe user access, permission grants, or change history — do not test,
score, or opine on these families; list them on the out-of-scope sheet
instead.

All of these checks aggregate live data. Run this discovery before any check that queries or aggregates:

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`start_distinct_values_by_alias`/`_by_id` → poll the matching result tool) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Each response returns **exactly one row per requested group** — no subtotal rows and no grand-total row. **A total is obtained by summing the rows** — there is no total row to read. Null groups arrive explicitly labeled `[null]` and are real groups; read null counts from that bucket. **Defensive filter:** keep only rows in which **every requested dimension key is present** — a roll-up row *omits* one or more keys entirely, whereas a genuine null is *present* with the value `[null]`. On a correct response this is a no-op; it guards against a stale cached response still carrying legacy subtotal and grand-total rows, each of which equals the whole total and would inflate any sum. When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.
> 5. **Truncated results.** Any data tool may return `{"data": [...], "truncated": true, "total_rows": N, "returned_rows": M, "guidance": "..."}` when the result exceeds the response size limit (~100 KB). The `data` prefix is **incomplete** — never compute totals, shares, or trends from it, and never present it as the full result. Follow the `guidance`: narrow the query (fewer dimensions, more filters, fewer selected columns) or use a business metric for a named KPI, then re-fetch.

In particular, never test a control against a budget-named scenario filter without first confirming it exists in the discovered scenario domain — if the plan side lives in a planning-version-like field, route budget-related evidence through that field's versions instead, and record the actual scenario/version used in the evidence package and audit trail.

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

### PDF Report
- Scope statement — in-scope check families **and** the out-of-scope
  disclaimer (access control / change management / ITGC), on page one
- Executive summary
- Check results (pass/fail/skipped per check, labeled with period + scenario)
- Exception findings
- Recommendations
- Management response section
- Check descriptions with the queries behind each result (appendix)

### Excel Evidence Workbook

Sheets map one-to-one to the in-scope checks:

- **Summary** — check status (pass/fail/skipped) and the scope statement
  (period + scenario/version actually used)
- **Completeness** — period coverage vs expected periods; scenario/period
  checksum results
- **Reconciliation** — the `/dr-reconcile` four-check results (including any
  noted skips)
- **Mapping Integrity** — parent/child roll-up detail with `[null]`-bucket
  (unmapped account) flags
- **Samples** — row-level detail behind material buckets, traceable to
  source line items
- **Exceptions** — findings with severity and recommended action (if any)
- **Out of scope — requires external evidence** — **mandatory** sheet
  listing the control families this tool cannot test (access control, change
  management, IT general controls) and where their evidence must come from
  (system administration / IT), so no reader mistakes this package for full
  SOX coverage

## Examples

### Q4 2025 year-end evidence package
```bash
/dr-audit --year 2025 --quarter Q4
```

### Mid-year evidence package
```bash
/dr-audit --year 2025 --quarter Q2
```

### Custom output locations
```bash
/dr-audit --year 2025 --quarter Q4 \
  --output-pdf audits/audit_q4_2025.pdf \
  --output-xlsx audits/evidence_q4_2025.xlsx
```

## Use Cases

### Data-side evidence for a SOX 404 program
```bash
# Year-end evidence package — in-scope control families only
/dr-audit --year 2025 --quarter Q4
```

### Quarterly data-integrity review
```bash
# Regular check of completeness, reconciliation, and mapping controls
/dr-audit --year 2025 --quarter Q3
```

### Management certification support
```bash
# Data evidence feeding management's SOX 404 process —
# does NOT substitute for access-control or ITGC testing
/dr-audit --year 2025 --quarter Q4
```

### External Auditor Support
```bash
# Provide auditors with the report and traceable evidence
/dr-audit --year 2025 --quarter Q4
```

## Performance

- Execution: ~1-2 minutes
- Data-evidencable checks only — every result backed by a query
- Professional report generation
- Evidence package with explicit scope boundaries

## Control Framework

Mapped to COSO components **only where FinanceOS data provides the
evidence**:

- **Control Activities** (in scope): reconciliation, roll-up validation,
  checksum integrity
- **Risk Assessment** (in scope, data-side): completeness and mapping
  integrity of the reported figures
- **Information & Communication** (in scope): documented evidence trail —
  the query behind every result
- **Monitoring** (partial): recurring runs of this package over each close
- **Control Environment — access controls, segregation of duties, change
  management** (out of scope): requires system-administration evidence this
  tool cannot reach

## Report Contents

### Executive Summary
- Scope statement: in-scope check families + out-of-scope disclaimer
- Audited period and scenario/version actually used
- Check result summary
- Key findings

### Detailed Findings
- Exceptions identified
- Severity assessment
- Management response area

### Check Descriptions
- Each check's objective
- Query performed (tool + parameters, so the result is reproducible)
- Evidence collected
- Status conclusion (pass/fail/skipped — skips are stated, never faked)

### Management Response
- Area for management to address findings
- Remediation timeline
- Owner assignment

## Evidence Package

### Check Summary Sheet
- Check ID and name
- Objective tested
- Result (pass/fail/skipped)
- Evidence gathered (the query behind the result)

### Exception Log
- Finding description
- Severity level
- Supporting evidence
- Recommended action

### Supporting Schedules
- Transaction samples (row-level detail behind material buckets)
- Reconciliation details (per-check results from `/dr-reconcile`)
- Roll-up and checksum workings

### Out of Scope — Requires External Evidence
- Access control, change management, IT general controls
- Why: no audit-log, access-history, or user-activity endpoint on the
  FinanceOS MCP surface
- Where their evidence must come from: system administration / IT

## Recommendations

Professional audit recommendations:
- Continue monthly reconciliation procedures (`/dr-reconcile`)
- Investigate and remap accounts flagged in the `[null]` roll-up bucket
- Re-run this evidence package each close to keep evidence current
- Source access-review and change-management evidence from system
  administration — this package cannot supply it

## Integration

Works with:
- `/dr-anomalies-report` - Data quality validation
- `/dr-reconcile` - Consistency checking
- `/dr-extract` - Data extraction
- `/dr-dashboard` - Control monitoring

## Related Skills

- `/dr-reconcile` - Ongoing reconciliation
- `/dr-anomalies-report` - Data quality
- `/dr-extract` - Data sourcing
- `/dr-dashboard` - KPI monitoring
