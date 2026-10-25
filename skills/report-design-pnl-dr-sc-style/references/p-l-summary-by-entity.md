# Spec: pnl-dr-sc-style → sheet "P&L Summary by Entity"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:U13`; Everything beyond it is hidden (columns after U, rows after 13). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AI28 |
| Merged ranges | D2:H2, J2:N2, P2:T2 |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 40.57 | 216.8 |  |
| C | 4.57 | 27.8 |  |
| D:E | 24.57 | 132.8 |  |
| F:H | 24.57 | 132.8 |  |
| I | 4.57 | 27.8 |  |
| J:N | 24.57 | 132.8 |  |
| O | 4.57 | 27.8 |  |
| P:T | 24.57 | 132.8 |  |
| U | 16.57 | 90.8 |  |
| V | 8.57 | 48.8 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `mmm-yy` | center | top | – | – |
| S5 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S6 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S7 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S8 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S9 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S10 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S13 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S14 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S15 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S16 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S17 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S18 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S19 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S20 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S21 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S22 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S23 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S24 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S25 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | – | 1.0 | – |
| S26 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | – | 1.0 | – |
| S27 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S28 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S29 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S30 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S31 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S32 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S33 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:S=S3 T:U=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:H=S4 I=S1 J:N=S5 O=S6 P:T=S5 U=S6
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S7 G:O=S1 P=S3 Q:U=S1
- **T4** h=24.0 rows 4: A=S1 B=S8 C=S2 D:U=S6
- **T5** h=24.0 rows 5: A=S1 B=S9 C=S2 D:H=S10 I=S11 J:N=S10 O=S11 P:U=S10
- **T6** h=15.95 rows 6: A=S1 B=S12 C:E=S2 F=S7 G:H=S1 I=S13 J:O=S1 P=S3 Q=S14 R:S=S3 T:U=S1
- **T7** h=24.0 rows 7: A:B=S15 C:D=S16 E=S17 F:U=S15
- **T8** h=24.0 rows 8: A=S15 B=S18 C:T=S19 U=S20
- **T9** h=24.0 rows 9: A=S15 B:G=S21 H=S22 I=S23 J:L=S21 M=S22 N=S21 O=S23 P:Q=S21 R:T=S22 U=S20
- **T10** h=24.0 rows 10-12: A=S24 B=S25 C=S26 D:E=S27 F=S28 G=S27 H=S28 I=S29 J:K=S27 L=S28 M=S27 N=S28 O=S29 P:Q=S27 R=S28 S=S27 T=S28 U=S30
- **T11** h=24.0 rows 13: A=S15 B:C=S31 D:E=S32 F=S33 G=S32 H=S33 I=S15 J:K=S32 L=S33 M=S32 N=S33 O=S15 P:Q=S32 R=S33 S=S32 T=S33 U=S15

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"I": "QTD", "J": "QTD", "P": "YTD"}
- r4: {"B": "P&L - Entity", "D": "Income", "E": "Gross Profit", "F": "Gross Profit %", "G": "Operating Profit", "H": "Operating Profit %", "J": "Income", "K": "Gross Profit", "L": "Gross Profit %", "M": "Operating Profit", "N": "Operating Profit %", "P": "Income", "Q": "Gross Profit", "R": "Gross Profit %", "S": "Operating Profit", "T": "Operating Profit %"}
- r5: {"D": "Actuals", "E": "Actuals", "F": "Actuals", "G": "Actuals", "H": "Actuals", "J": "Actuals", "K": "Actuals", "L": "Actuals", "M": "Actuals", "N": "Actuals", "P": "Actuals", "Q": "Actuals", "R": "Actuals", "S": "Actuals", "T": "Actuals", "U": "Actuals"}
- r8: {"B": "Profit Center"}
- r10: {"B": "CloudApp Ltd"}
- r11: {"B": "CloudApp Inc."}
- r12: {"B": "CloudApp Pty. Ltd"}
- r13: {"B": "Total"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D2 (example `D2`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F3** at D10:H12, J10:N12 (example `D10`): `=IF($B10="",_xldudf_DR_GET(Value_EBITDA,"[Account Group L2]",D$4,"[Entity]","[null]","[Reporting Month]",$D$2,"[Scenario]",D$5),_xldudf_DR_GET(Value_EBITDA,"[Account Group L2]",D$4,"[Entity]",$B10,"[Reporting Month]",$D$2,"[Scenario]",D$5))`
- **F4** at P10:T12 (example `P10`): `=IF($B10="",_xldudf_DR_YTD(Value_EBITDA,"[Account Group L2]",P$4,"[Entity]","[null]","[Reporting Month]",$D$2,"[Scenario]",P$5),_xldudf_DR_YTD(Value_EBITDA,"[Account Group L2]",P$4,"[Entity]",$B10,"[Reporting Month]",$D$2,"[Scenario]",P$5))`
- **F5** at D13:E13, G13, J13:K13, M13, P13:Q13, S13 (example `D13`): `=IFERROR(SUM(D10:D12),"NA")`
- **F6** at F13, L13, R13 (example `F13`): `=IFERROR(E13/D13,"NA")`
- **F7** at H13, N13, T13 (example `H13`): `=IFERROR(G13/D13,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
