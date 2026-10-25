---
name: report-design-house-style
description: Datarails house style for what the official report templates do not cover — charts, extra tabs with no template, and the sheet a drill-down creates. Load it through report-design when you build a chart, a custom tab or a drill-down follow-up in the open workbook with the Excel agent. Not for generating standalone presales or demo workbooks outside Excel, and not for sheets that have an official template (report-design routes those).
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - execute_office_js
---

# Datarails house style (charts, custom tabs, drill-downs)

Source: the marketing design spec for Datarails-styled Excel output, reduced to what the Excel agent can apply through Office.js. If this skill and an official template skill disagree, **the template skill wins** for that sheet.

## When to use it

| Situation | What to do |
|---|---|
| A sheet that has an official template (P&L, Balance Sheet, Cash Flow, Financial Statement Summary, KPIs) | Do not use this skill. The template's exact spec applies. |
| A **chart**, anywhere (report, drill-down, dashboard sheet) | Follow *Charts* below. |
| A **custom tab** with no official template (an ad-hoc analysis, flux, a rolling table) | Use *Tokens* and *Cells* below. Say it is not an official template. |
| The tab a **drill-down** creates (`Pivot Drill Down N`) | Follow *Drill-down tabs* below: leave its look alone. |

## Tokens

| Token | Hex | Use |
|---|---|---|
| Navy | `0C142B` | banner and column-header fill |
| Lavender | `F2F2FB` | category band, pivot column headers |
| Period pink | `FFDBE5` | period band |
| Input fill / text | `EAEAFF` / `4646CE` | hardcoded values |
| Calculation fill | `F0F1F4` | Excel formulas (not totals) |
| Fixed Output fill | `DFE0E3` | `DR.GET` formulas |
| Body text | `333333` | labels, numbers, grand totals |
| Subtotal text | `626364` | subtotal rows and total columns |
| Border | `9EA1AA` | thin solid border on every styled cell |
| Chart series | `4646CE`, `FFA310`, `F93576`, `4EB7DF` | the only chart fills |

Font: **Poppins** everywhere. If Poppins is missing on the machine, say so; do not silently swap it.

## Cells (custom tabs)

- Style a cell by what it holds: a Datarails retrieval formula (`DR.GET`, `DR.QTD`, `DR.YTD`, `DR.MTD`) → Fixed Output fill; any other formula → Calculation fill; a hardcoded **number or value a user is meant to type over** → Input fill and `4646CE` text. **Static row and column labels are not inputs**: they take the label style below (no fill, regular `333333`). Never leave data cells unfilled, and never encode meaning in the font colour of a number (no green or red; a variance is a plain `333333` number).
- Line-item labels are Poppins 12 **regular** `333333`, not bold. Only headers, subtotals and totals are bold.
- Navy appears only in the banner rows at the top. Unused background cells are white; do not fill the whole sheet. Data cells keep their content fills (Input, Calculation, Fixed Output), and category and period bands keep lavender and pink.
- Gridlines off. Explicit row heights in **points** (Office.js `rowHeight` is in points): 18 pt (24 px) for body rows. No merged cells on a custom tab: fill across the band cell by cell.
- Number format follows what the value is: currency `_($* #,##0_);_($* (#,##0);_($* "-"_);_(@_)` (swap the symbol), percent `0.0%_);\(0.0%\);"-"_)` with no currency symbol, count `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`, ratio `0.0"x"_);\(0.0"x"\);"-"_)`, period header `mmm-yy`. Negatives in parentheses, zero as a dash.
- No logo on a custom tab: the only logos the plugin ships are the template header marks, which belong to the official templates.

## Charts

Every chart the agent adds follows this, on any tab:

- Type: **clustered** or **stacked column** only (not bar, line, pie or 100% stacked).
- **No chart title.** Legend on the **right**. Primary horizontal and vertical axes shown. Horizontal major gridlines only (no vertical, no minor).
- Chart border solid `9EA1AA`; gridlines `DFE0E3`; every text element (axes, data labels, legend) Poppins 10 `333333`.
- Series fills only from `4646CE`, `FFA310`, `F93576`, `4EB7DF`, a different colour per series when there are several.
- Data labels on: **Outside End** on clustered, **Center** on stacked (Excel has no Outside End for stacked columns).

Office.js: `chart.title.visible = false`; `chart.legend.position = "Right"`; `chart.format.border.color = "#9EA1AA"`; `chart.axes.valueAxis.majorGridlines.format.line.color = "#DFE0E3"`; `chart.axes.categoryAxis.majorGridlines.visible = false`; `chart.format.font.name = "Poppins"`, `.size = 10`, `.color = "#333333"`; a loop over the chart's actual series, `chart.series.load("items"); await context.sync(); const pal = ["#4646CE","#FFA310","#F93576","#4EB7DF"]; chart.series.items.forEach((se, i) => se.format.fill.setSolidColor(pal[i % pal.length]))` (fewer than four series simply use the first colours; with more than four the palette cycles, so tell the user the chart is too busy to tell series apart and suggest fewer series); `series.hasDataLabels = true` and `series.dataLabels.position = "OutsideEnd"` (clustered) or `"Center"` (stacked). Read the properties back; do not trust a screenshot.

## Drill-down tabs

How a drill-down tab is made depends on the drill: some are copies of a hidden `Dr_Pivot_Template …` sheet (saved favorites), others are a pivot or a plain list the add-in builds directly. Either way the add-in owns the sheet's content.

- **Do not restyle the pivot or list the add-in produced.** A refresh re-renders it, so cell formatting you apply is lost on the next refresh.
- **Row 1 belongs to the add-in** (table, id, source and saved filters). Never write to, style, resize or hide it.
- If the user wants a different look, do not say it cannot be done. Say the drill-down sheet resets on refresh, and offer to build the styled table or chart on a separate tab (or beside it) from its data, following *Cells* and *Charts*.
- A chart you add next to a drill-down follows *Charts* above.
