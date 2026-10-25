# Spec: kpi-dr-sc-style → sheet "Widget Size Backlog"

> Source: KPIs for Dashboard — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:F18`; Everything beyond it is hidden (columns after F, rows after 18). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 14.5 pt (unlisted rows visible) |
| Used range | A1:L19 |
| Merged ranges | B5:F13, H5:L14 |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| B | 7.71 | 44.2 |  |
| C | 4.14 | 25.5 |  |
| D | 7.86 | 45.0 |  |
| E | 24.86 | 134.2 |  |
| F | 9.57 | 54.0 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 11.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S2 | Calibri | 12.0 | B | 000000 | – | – | `–` | – | – | – | – |
| S3 | Calibri | 62.0 | B | 037C5A | FFFFFF | – | `#,##0,\ "K"` | center | center | – | – |
| S4 | Calibri | 72.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | – | center | – | – |
| S5 | Wingdings 3 | 18.0 |  | C00000 | FFFFFF | – | `0%` | – | – | – | – |
| S6 | Calibri | 18.0 |  | C00000 | FFFFFF | – | `0%` | center | – | – | – |
| S7 | Calibri | 18.0 |  | 000000 | FFFFFF | – | `–` | left | – | – | – |
| S8 | Calibri | 18.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | – | center | – | – |
| S9 | Calibri | 18.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S10 | Calibri | 11.0 |  | 000000 | DBDBDB | – | `–` | centerContinuous | – | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=None rows 1-3,16-17: A:F=S1
- **T2** h=15.5 rows 4: A=S1 B:F=S2
- **T3** h=15.0 rows 5-10,13: A=S1 B:F=S3
- **T4** h=18.75 rows 11-12: A=S1 B:F=S3
- **T5** h=21.75 rows 14: A=S1 B=S4 C=S5 D=S6 E=S7 F=S8
- **T6** h=23.5 rows 15: A:B=S1 C=S5 D=S6 E=S7 F=S9
- **T7** h=14.5 rows 18: A=S1 B:F=S10

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r4: {"B": "Net Monthly Burn"}
- r18: {"C": "Widget Size:2X6"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at B5 (example `B5`): `='Cash Flow'!I4`
- **F2** at C14:D15 (example `C14`): `='Cash Flow'!J6`
- **F3** at E14:E15 (example `E14`): `='Cash Flow'!M6`

## 6. Pictures

None.

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

**Cross-sheet rules:** these formulas reference sheet(s) `Cash Flow` — create that sheet in the same workbook BEFORE adding the rules, or Excel rejects them.

- [P1] **cell value equal** `"Positive CF"` → fontColor `037C5A` — on B5:F13
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["\"Positive CF\""], "kind": "cellIs", "op": "equal", "priority": 1, "ranges": "B5:F13"}`
- [P2] **cell value equal** `"∞"` → fontColor `037C5A` — on H5:L14
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["\"∞\""], "kind": "cellIs", "op": "equal", "priority": 2, "ranges": "H5:L14"}`
- [P3] **formula** `'Cash Flow'!$K6>'Cash Flow'!$G6` → fontColor `037C5A` — on C14:C15
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["'Cash Flow'!$K6>'Cash Flow'!$G6"], "kind": "expression", "priority": 3, "ranges": "C14:C15"}`
- [P4] **formula** `'Cash Flow'!$K6>'Cash Flow'!$F6` → fontColor `BF1D30` — on C14:C15
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["'Cash Flow'!$K6>'Cash Flow'!$F6"], "kind": "expression", "priority": 4, "ranges": "C14:C15"}`
- [P5] **formula** `AND('Cash Flow'!$K6<'Cash Flow'!$G6,'Cash Flow'!$K6>'Cash Flow'!$F6)` → fontColor `FFB800` — on C14:C15
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["AND('Cash Flow'!$K6<'Cash Flow'!$G6,'Cash Flow'!$K6>'Cash Flow'!$F6)"], "kind": "expression", "priority": 5, "ranges": "C14:C15"}`
- [P6] **cell value greaterThan** `'Cash Flow'!G6` → fontColor `037C5A` — on D14:D15
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["'Cash Flow'!G6"], "kind": "cellIs", "op": "greaterThan", "priority": 6, "ranges": "D14:D15"}`
- [P7] **cell value lessThan** `'Cash Flow'!F6` → fontColor `BF1D30` — on D14:D15
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["'Cash Flow'!F6"], "kind": "cellIs", "op": "lessThan", "priority": 7, "ranges": "D14:D15"}`
- [P8] **cell value between** `'Cash Flow'!F6` and `"0'Cash Flow'!G6"` → fontColor `FFB800` — on D14:D15
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["'Cash Flow'!F6", "\"0'Cash Flow'!G6\""], "kind": "cellIs", "op": "between", "priority": 8, "ranges": "D14:D15"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## 9. Known gaps in the official template (read before building)

- The data-validation dropdowns in §1 read from a sheet named `List` that is **not part of this template**, and some of them point at
  `List!#REF!`, which is broken in the template itself. If the workbook already has a `List` sheet, apply the validations that point
  at real ranges; otherwise build the sheet without them and say so. Do not recreate the `#REF!` ones.
- A defined name in §1 can point at another sheet of this workbook (for example `FY_Start`). Define it on the sheet you built, or skip
  it, and say which.
