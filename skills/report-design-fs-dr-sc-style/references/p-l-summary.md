# Spec: fs-dr-sc-style → sheet "P&L Summary"

> Source: Financial Statement - Summary DR Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:L19`; Everything beyond it is hidden (columns after L, rows after 19). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `C6` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 22.8 pt (unlisted rows visible) |
| Used range | A1:AA240 |
| Merged ranges | C2:F2, H2:K2 |
| Defined name `DR_DATE_PICKER` | `45900` |
| Defined name `Value` | `"widget_19324_0_tt_1773235214"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 2.57 | 17.2 |  |
| B | 32.57 | 174.8 |  |
| C:D | 16.57 | 90.8 |  |
| E:F | 16.57 | 90.8 |  |
| G | 4.57 | 27.8 |  |
| H:K | 16.57 | 90.8 |  |
| L | 4.57 | 27.8 |  |
| M | 16.86 | 92.2 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `mmm-yy` | center | center | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | center | – | – |
| S5 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S6 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S7 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S8 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | – | – |
| S9 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S10 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S11 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S12 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S13 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | wrap |
| S14 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `–` | center | – | – | wrap |
| S15 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S16 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S17 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S18 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S19 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S20 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S21 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S22 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S23 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `\$#,##0,\ "K"` | right | center | 1.0 | – |
| S24 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S25 | Poppins | 12.0 | B | 626364 | – | – | `–` | – | – | – | – |
| S26 | Poppins | 12.0 | B | 626364 | – | – | `@` | left | center | 1.0 | – |
| S27 | Poppins | 12.0 | B | 626364 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S28 | Poppins | 12.0 | B | 626364 | – | – | `0.0%;\(0.0%\)` | – | – | – | – |
| S29 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S30 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S31 | Poppins | 12.0 | B | 333333 | – | B:thin:9EA1AA | `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |
| S32 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | wrap |
| S33 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S34 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `\$#,##0,\ "K"` | right | center | 1.0 | – |
| S35 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S36 | Poppins | 12.0 |  | 333333 | – | – | `–` | – | – | – | – |
| S37 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S38 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:D=S2 E:L=S1
- **T2** h=24.0 rows 2: A:B=S1 C:F=S3 G=S1 H:K=S4 L=S1
- **T3** h=8.2 rows 3: A:B=S1 C:D=S2 E=S5 F:L=S1
- **T4** h=24.0 rows 4: A=S1 B=S6 C=S7 D=S8 E:F=S7 G=S1 H=S7 I=S8 J:K=S7 L=S1
- **T5** h=8.2 rows 5: A=S1 B=S9 C:D=S2 E=S5 F:G=S1 H=S10 I:L=S1
- **T6** h=24.0 rows 6: A=S11 B=S12 C=S13 D=S14 E:F=S12 G=S11 H:K=S12 L=S11
- **T7** h=24.0 rows 7-8,12,16-17: A=S15 B=S16 C:D=S17 E=S18 F=S19 G=S20 H:I=S17 J=S18 K=S19 L=S21
- **T8** h=32.2 rows 9,13: A=S11 B=S22 C:E=S23 F=S24 G=S25 H:J=S23 K=S24 L=S11
- **T9** h=32.2 rows 10: A=S11 B=S26 C:F=S27 G=S28 H:K=S27 L=S11
- **T10** h=16.0 rows 11: A=S29 B=S30 C:F=S31 G=S11 H:K=S31 L=S11
- **T11** h=32.2 rows 14: A=S11 B=S26 C:F=S27 G=S25 H:K=S27 L=S11
- **T12** h=16.0 rows 15: A=S11 B=S12 C:D=S32 E:F=S12 G=S11 H:K=S12 L=S11
- **T13** h=32.2 rows 18: A=S11 B=S33 C:E=S34 F=S35 G=S36 H:J=S34 K=S35 L=S11
- **T14** h=32.2 rows 19: A=S11 B=S37 C:F=S38 G=S36 H:K=S38 L=S11

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r4: {"C": "Actuals", "D": "Previous Year", "E": "∆ vs PY", "F": "% ∆ vs PY", "H": "Actuals", "I": "Previous Year", "J": "∆ vs PY", "K": "% ∆ vs PY"}
- r7: {"B": "Income"}
- r8: {"B": "Cost of Goods Sold"}
- r9: {"B": "Gross Profit "}
- r10: {"B": "Gross Profit %"}
- r12: {"B": "Operating Expense"}
- r13: {"B": "Operating Profit"}
- r14: {"B": "Operating Profit %"}
- r16: {"B": "Other Income"}
- r17: {"B": "Other Expense"}
- r18: {"B": "Net Income"}
- r19: {"B": "Net Income %"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at C2 (example `C2`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at H2 (example `H2`): `=YEAR(C2)&" YTD"`
- **F3** at C7:C8, C12, C16:C17, H16:H17 (example `C7`): `=_xldudf_DR_GET(Value,"[Reporting Month]",$C$2,"[Account Group L2]",$B7,"[Data Type]","Activity","[Scenario]",C$4)`
- **F4** at D7:D8, D12, D16:D17, I16:I17 (example `D7`): `=_xldudf_DR_GET(Value,"[Reporting Month]",EOMONTH($C$2,-12),"[Account Group L2]",$B7,"[Data Type]","Activity","[Scenario]",C$4)`
- **F5** at E7:E10, J7:J10, E12:E14, J12:J14, E16:E19, J16:J19 (example `E7`): `=C7-D7`
- **F6** at F7:F10, K7:K10, F12:F14, K12:K14, F16:F19, K16:K19 (example `F7`): `=IFERROR(C7/D7-1,0)`
- **F7** at H7:H8, H12 (example `H7`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$C$2,"[Account Group L2]",$B7,"[Data Type]","Activity","[Scenario]",H$4)`
- **F8** at I7:I8, I12 (example `I7`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",EOMONTH($C$2,-12),"[Account Group L2]",$B7,"[Data Type]","Activity","[Scenario]",H$4)`
- **F9** at C9:D9, H9:I9 (example `C9`): `=C7-C8`
- **F10** at C10:D10, H10:I10 (example `C10`): `=IFERROR(C9/C7,0)`
- **F11** at C13:D13, H13:I13 (example `C13`): `=C9-C12`
- **F12** at C14:D14, H14:I14 (example `C14`): `=IFERROR(C7/C13,0)`
- **F13** at C18:D18, H18:I18 (example `C18`): `=C13+C16+C17`
- **F14** at C19:D19, H19:I19 (example `C19`): `=IFERROR(C18/C7,0)`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **220x35 px**, anchor B1(+8px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on E7:E10 J7:J10 E12:E14 J12:J14 E16:E19 J16:J19
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 1, "ranges": "E7:E10 J7:J10 E12:E14 J12:J14 E16:E19 J16:J19"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## Template defect (read before building)

**Operating Profit % (row 14, formula F12):** the template divides Income by Operating Profit (`C7/C13`), which is the reciprocal of the margin. Build `=IFERROR(C13/C7,0)` (Operating Profit / Income), copied across the same cells, and tell the user you corrected it.
