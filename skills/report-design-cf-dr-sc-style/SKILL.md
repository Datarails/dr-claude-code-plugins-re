---
name: report-design-cf-dr-sc-style
description: Exact build specs for the official Datarails Cash Flow - DR SC Style template, one per sheet, covering layout, colours, fonts, column widths, row heights, logos, conditional formats, sparklines and formula patterns. Use when the user wants a cash flow statement in the official Datarails look, loaded through the report-design router while the Excel add-in agent builds the report. Not for the P&L, balance sheet, Financial Statement Summary or KPI templates, which have their own report-design skills.
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - execute_office_js
---

# Cash Flow - DR SC Style — build specs

Self-contained: everything needed to build the template is in this skill. **Nothing has to be attached or downloaded by the user.** The data side (accounts, scenario, date, DR.GET formulas, refresh) stays with the Excel add-in agent and `dr-get-formula`; this skill gives the exact look and layout.

## Which spec

Pick the sheet that matches the request and apply **only that file** (all files are delivered together, the others are for other requests).

| Sheet | File | Use when the user wants |
|---|---|---|
| Cash Flow - YoY | `references/cash-flow-yoy.md` | current period vs prior year |
| Cash Flow Rolling 12M | `references/cash-flow-rolling-12m.md` | twelve months of cash flow |
| Dashboard | `references/dashboard.md` | a small dashboard sheet with three KPI cards and icons |

Logos as base64: `references/logos.md`.

Source: Cash Flow - DR SC Style, Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Each spec was rebuilt from its markdown in desktop Excel and diffed against the template workbook with 0 mismatches.

## How to read a spec

Sections: 1 sheet settings (gridlines, freeze, merges, defined names) · 2 columns · 3 style catalog (resolved hex colours, fonts, borders, number formats) · 4 row templates (each row's height and the style of every column run) · 5 constants and formulas (formulas written for the first listed cell, filled to the others with relative references) · 6 pictures · 7 conditional formats and sparklines · 8 adapting to the user's data.

## Build traps (each one cost a real run a visible defect)
- `columnWidth` and `rowHeight` are in **points** (the specs list pt). Colours, fonts, number formats are exact — never "default".
- **Merge first, then format** the merged range (merging resets its font to the workbook default); read `font.name` back on each merged anchor.
- Borders are per cell; a range border draws only the outer edges, so border every cell or set the inside edges too. Where two cells disagree about a shared edge the heavier line wins; the specs already list the winning edge.
- **Freeze panes before hiding or collapsing columns** (freezing afterwards puts the split after the hidden columns). If `columnHidden` does not take on a wide range, set the width to 0.
- Conditional-format formulas are relative to the first cell of each range (select it first when using COM). Rules that reference another sheet need that sheet to exist first.
- Pictures: `references/logos.md` has each logo as base64. Insert with `sheet.shapes.addImage(base64)` at the **displayed** size given in the spec, aspect ratio locked, never stretched. If the surface cannot insert images, say so — do not skip silently.
- Account / department / entity labels in the specs are the template's demo labels. Real rows come from the org: repeat the item row template per account, re-point the SUM ranges, keep section titles, totals and column blocks. If the org has no `Actuals`, use its real scenario; if the latest month with data is older than the last closed month, use that month — and say what you adapted.
- **Function names.** The spec formulas show the names as the new add-in stores them in the file (`_xldudf_DR_GET`, `_xldudf_DR_QTD`, `_xldudf_DR_YTD`, `_xldudf_DR_INCLUDE`, in general `_xldudf_DR_X`). Type them as the add-in function (any `_xldudf_DR_X` becomes `DR.X`): `DR.GET`, `DR.QTD`, `DR.YTD`, `DR.INCLUDE` (the COM add-in stores the same functions as `_xll.DR.GET` and so on). That is the only difference between the two versions of each template; the formulas, layout and styles are identical.
- The DR.GET authoring contract of the add-in agent (argument syntax, field names that exist in the org, `Value` handling) always wins over a template formula; map any field name the org lacks and tell the user.
- Do not say the sheet matches the template unless you read back fonts, borders and widths from the workbook (a screenshot is not enough) and walked the checks below.

## Checks before you report done
Gridlines and freeze panes as in the spec; every column width (pt) and row height; every merge present with its font; one row of each template spot-read (fill, font, border, number format); formulas as listed with relative patterns kept; conditional formats, sparklines and pictures (at displayed size); hidden ranges.
