# Spec: fs-dr-sc-style → sheet "BS"

> Source: Financial Statement - Summary DR Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:J20`; Everything beyond it is hidden (columns after J, rows after 20). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `C6` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 120 |
| Default row height | 22.8 pt (unlisted rows visible) |
| Used range | A1:V238 |
| Merged ranges | E2:F2, H2:I2 |
| Defined name `DR_DATE_PICKER` | `45900` |
| Defined name `DR_FY_START` | `1` |
| Defined name `Value` | `"widget_19324_0_tt_1773235214"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 2.57 | 17.2 |  |
| B | 32.57 | 174.8 |  |
| C | 16.57 | 90.8 |  |
| D | 4.57 | 27.8 |  |
| E:F | 16.57 | 90.8 |  |
| G | 4.57 | 27.8 |  |
| H:I | 16.57 | 90.8 |  |
| J | 4.57 | 27.8 |  |
| K | 16.86 | 92.2 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `mmm-yy` | center | center | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | center | – | – |
| S5 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S6 | Poppins | 12.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S7 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S8 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S9 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | wrap |
| S10 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S11 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S12 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S13 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | wrap |
| S14 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S15 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S16 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S17 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S18 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S19 | Poppins | 12.0 | B | 7FFFD4 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S20 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S21 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `\$#,##0,\ "K"` | right | center | 1.0 | – |
| S22 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | wrap |
| S23 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S24 | Poppins | 12.0 | B | 333333 | – | – | `\$#,##0,\ "K"` | right | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S26 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | wrap |
| S27 | Poppins | 10.0 |  | F0F1F4 | – | – | `–` | left | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C=S2 D:J=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S3 D=S1 E:F=S4 G=S1 H:I=S4 J=S1
- **T3** h=8.2 rows 3: A:B=S1 C=S2 D:J=S1
- **T4** h=24.0 rows 4: A=S1 B=S5 C=S6 D=S1 E=S6 F=S7 G=S1 H=S6 I=S7 J=S1
- **T5** h=8.2 rows 5: A=S1 B=S8 C=S9 D:J=S10
- **T6** h=24.0 rows 6: A=S11 B=S12 C=S13 D=S11 E:F=S12 G=S11 H:I=S12 J=S11
- **T7** h=24.0 rows 7,11-12,15-16: A=S14 B=S15 C=S16 D=S17 E:F=S16 G=S17 H:I=S16 J=S18
- **T8** h=24.0 rows 8: A=S14 B=S15 C=S16 D=S17 E:F=S16 G=S17 H:I=S16 J=S19
- **T9** h=32.2 rows 9,13,17: A=S11 B=S20 C=S21 D=S11 E:F=S21 G=S11 H:I=S21 J=S11
- **T10** h=16.0 rows 10,14: A=S11 B=S12 C=S22 D=S11 E:F=S12 G=S11 H:I=S12 J=S11
- **T11** h=32.2 rows 18: A=S11 B=S23 C=S24 D=S11 E:F=S24 G=S11 H:I=S24 J=S11
- **T12** h=22.8 rows 19: A=S11 B=S25 C=S26 D=S11 E:F=S25 G=S11 H:I=S25 J=S11
- **T13** h=22.8 rows 20: A=S11 B=S25 C=S27 D=S11 E:F=S25 G=S11 H:I=S25 J=S11

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"C": "Month", "E": "Previous Quarter", "H": "Previous Year"}
- r4: {"F": "∆ vs PQ", "I": "∆ vs PY"}
- r5: {"C": "Actuals", "E": "Actuals", "H": "Actuals"}
- r7: {"B": "Current Assets"}
- r8: {"B": "Non Current Assets"}
- r9: {"B": "Total Asset"}
- r11: {"B": "Current Liabilities"}
- r12: {"B": "Long Term Liabilities"}
- r13: {"B": "Total Liabilites"}
- r15: {"B": "Equity"}
- r16: {"B": "Net Income Calc"}
- r17: {"B": "Total Equity"}
- r18: {"B": "Total Liability & Equity"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at C4 (example `C4`): `=DR_DATE_PICKER`
- **F2** at E4, H4 (example `E4`): `=IFERROR(EOMONTH($C4,-IF(MOD(MONTH($C4)-(DR_FY_START-1),3)=0,3,MOD(MONTH($C4)-(DR_FY_START-1),3))),"NA")`
- **F3** at C7:C8, E7:E8, H7:H8, C11:C12, E11:E12, H11:H12, C15:C16, E15:E16, H15:H16 (example `C7`): `=_xldudf_DR_GET(Value,"[Reporting Month]",C$4,"[Account Group L2]",$B7,"[Scenario]",C$5)`
- **F4** at F7:F8, I7, F11:F12, F15:F16, I15 (example `F7`): `=IFERROR(C7-E7,"NA")`
- **F5** at I8, I11:I12, I16 (example `I8`): `=IFERROR(C8-H8,"NA")`
- **F6** at C9, E9:F9, H9:I9, C13, E13:F13, H13:I13, C17, E17:F17, H17:I17 (example `C9`): `=IFERROR(C7+C8,"NA")`
- **F7** at C18, E18:F18, H18:I18 (example `C18`): `=IFERROR(C13+C17,"NA")`
- **F8** at C20, E20, H20 (example `C20`): `=IFERROR(IF(ABS(C9-C18)<1,"","Check Balance"),"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **221x36 px**, anchor B1(+7px,+28px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## Template defects (read before building)

The official template has formula mistakes in this sheet. Build the corrected versions below and tell the user you did:

- **Previous Year date (`H4`):** the template reuses the previous-quarter formula, so the Previous Year column shows a quarter-end date. Use `=IFERROR(EOMONTH($C4,-12),"NA")` in `H4`; keep the quarter formula (F2) in `E4` only.
- **Previous Year deltas (`I7`, `I15`):** the template computes `C-E` (current minus previous quarter). Use the previous-year balance: `=IFERROR(C7-H7,"NA")` in `I7` and `=IFERROR(C15-H15,"NA")` in `I15`, like the other `I` cells.
