---
name: report-design
description: Router for the exact build specs of the official Datarails report templates in Excel. The official set is the DR SC Style templates from Workspace > Reports > Datarails templates (P&L EBITDA, Balance Sheet, Cash Flow, Financial Statement Summary, KPIs for Dashboard). It tells which template skill to load so a report built in the open workbook looks identical to the template on the first try, with no file attached by the user. Use TOGETHER WITH the Excel add-in agent whenever `dr-get-formula` or `datarails-excel-agent` builds a statement the user wants in a Datarails template look. It supplies design and layout only, the agent still discovers the data, writes the DR.GET formulas and refreshes. Not a standalone report builder, not for choosing accounts or levels, not for PowerPoint.
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - execute_office_js
---

# Datarails report design — router

The specs live **inside the plugin**, one self-contained skill per template. **The user never has to attach, download or open a template file** — if you find yourself asking for one, load the skill below instead.

The Excel add-in agent builds the data; the template skill dictates how the sheet must look and be laid out. Do both in one pass so the first build is already right.

## 1. Pick the template skill

Load it with `read_skill("datarails-financeos/<skill>")` in Claude for Excel (the Skill tool in Claude Code). It returns the skill's instructions and every spec file, so read **only the sheet you need** from it.

**The official templates are the DR SC Style set** in the Datarails workspace (Workspace > Reports > Datarails templates): P&L EBITDA, Balance Sheet, Cash Flow, Financial Statement Summary and KPIs for Dashboard. **Use them for every report.**

| The user wants | Load this skill | Sheet |
|---|---|---|
| A P&L, no look named, or "the Datarails template / standard look" | `report-design-pnl-dr-sc-style` | **P&L YoY** (MTD / QTD / YTD vs prior year) is the default |
| …actual vs budget · forecast vs budget vs actual · OpEx variance analysis · 12 months · multi-year · by entity · the instructions cover | `report-design-pnl-dr-sc-style` | P&L BvA · P&L FvBvA · OpEx Variance Analysis · P&L 12M · P&L Multi-Year Overview · P&L Summary by Entity · FP&A |
| A balance sheet | `report-design-bs-dr-sc-style` | Summary · YoY · 12M rolling |
| A cash flow statement | `report-design-cf-dr-sc-style` | Cash Flow - YoY · Cash Flow Rolling 12M · Dashboard |
| A one-screen balance sheet or P&L summary ("Financial Statement Summary") | `report-design-fs-dr-sc-style` | P&L Summary · BS |
| KPI cards / dashboard-widget authoring sheets (only if asked explicitly) | `report-design-kpi-dr-sc-style` | the matching sheet |
| A **chart**, a **custom tab** with no official template, or the sheet a **drill-down** creates | `report-design-house-style` | Charts · Cells · Drill-down tabs (the template skills win wherever a template exists) |

If nothing fits (another statement or look), say so and fall back to `dr-get-formula`'s own preset in `references/report-designs.md` — never improvise a look. Where a template skill exists it overrides that preset for grid, fills, borders, widths, heights and logo placement; do not blend the two. 

## 2. Build

1. **Decide the data first** (the agent's normal flow): account/section list, scenario, reporting date, level field. Ask the usual questions.
2. **Read the sheet's spec in full**, then build in this order: sheet settings → column widths → row heights → merges → constants and formulas → styles (per row template) → conditional formats → sparklines → pictures → **freeze panes** → hide/collapse columns and rows → gridlines. Every template skill repeats the build traps (merge first then format, per-cell borders, freeze before hiding, relative conditional formulas, logos as base64) — follow them.
3. **Template formula patterns win over `dr-get-formula`'s default layout**, but the DR.GET authoring contract (argument syntax, field names that exist in the org, `Value` handling) always wins; map any field the org lacks and tell the user.
4. **Verify by reading properties back** (fonts, borders, widths, merges, freeze, pictures), not from a screenshot, and report what you adapted (real accounts, scenario, date) and anything you could not apply.

## Maintainers

How the specs are generated, proven in real Excel and packaged into these skills — and how to add a template or refresh a revision — is in `docs/internal/report-design/README.md` (internal, not shipped).
