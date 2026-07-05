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
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
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
   two grouped calls over the audited window — by scenario and by period: in
   each response the labeled group rows (including `[null]`) must sum to the
   appended keyless grand-total row (Data-scope preamble, item 4), and the
   two grand totals must equal each other. Tools:
   `get_distinct_values_by_alias`/`_by_id`,
   `get_aggregated_data_by_alias`/`_by_id`.
2. **Consistency / reconciliation.** The reconciliation control is the
   `/dr-reconcile` skill's four independent-source checks — cross-endpoint
   agreement, balance-sheet identity, cross-grain roll-up, and
   scenario/period integrity. Delegate the method to that skill (do not
   re-derive a weaker inline copy) and record its per-check
   pass/fail/skipped results as the evidence here.
3. **Account-mapping integrity.** The cross-grain roll-up check: two
   aggregates over the same scope — `dimensions=[<parent_level>]` and
   `dimensions=[<parent_level>, <child_level>]`, both `SUM(<amount>)`. For
   each parent bucket, the sum of its child rows — **including the `[null]`
   bucket** — must equal the parent's own row to the cent; accounts landing
   in the `[null]` child bucket are flagged as **unmapped** in the exception
   log.
4. **Substantive sampling.** For the material buckets (largest by absolute
   amount in the audited window), pull row-level detail via
   `get_data_by_alias` / `get_data_by_id` with `select` on the load-bearing
   columns and `filters` scoping bucket + period, so a human auditor can
   trace reported figures to source line items. Respect the 500-row cap —
   sample per bucket, never attempt a full extract.

**Out of scope — requires external evidence:** access control, change
management, and IT general controls. No tool available to this skill can
observe user access, permission grants, or change history — do not test,
score, or opine on these families; list them on the out-of-scope sheet
instead.

All of these checks aggregate live data. Run this discovery before any check that queries or aggregates:

> **Data-scope discovery — run before any aggregate (reuse anything already discovered this conversation).**
> 1. **Scenario domain.** Pull distinct values of the scenario field (`get_distinct_values_by_alias`/`_by_id`) — never assume a scenario name exists (`Budget` frequently doesn't; many orgs carry only `{Actuals, Forecast}`). For budget/plan questions, if no budget-like scenario exists, look for a planning-version-like field (alias/name matching `/plan|version|cycle|budget/i`) and use its versions as the plan side; if neither exists, say so and offer a comparison across the scenarios that do exist.
> 2. **Account grain.** Pull distinct values of each account-hierarchy level field (L0/L1/L2-like). Use the level whose values partition P&L flows into revenue/COGS/opex-like buckets — on many orgs the top level is the balance-sheet equation (ASSET/LIABILITY/EQUITY/INCOME) and P&L line items live one level deeper. For P&L work, scope to P&L flows and exclude balance-sheet buckets; never present asset/liability/equity totals as revenue or expenses.
> 3. **Period scope.** Discover the date field's range (distinct values of the reporting-month field, or MIN and MAX in two separate calls — one aggregation per field per call). Default every P&L question to the latest complete fiscal year (or trailing 12 closed months) — never an unscoped all-time total: financials tables are multi-year cumulative and mix balance-sheet stock with P&L flow. **Label every output with the period + scenario it covers.**
> 4. **Reading GROUP BY responses.** Null groups arrive explicitly labeled `[null]` — read null counts only from that bucket. Every aggregation response also appends a **keyless row equal to the grand total**; exclude it from sums, shares, trends, and bucket counts (at most use it as a checksum). When COUNT-ing rows per group, aggregate a different field than the GROUP BY dimension itself — a same-field COUNT of the grouped dimension can 500.

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
