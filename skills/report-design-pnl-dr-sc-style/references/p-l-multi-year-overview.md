# Spec: pnl-dr-sc-style → sheet "P&L Multi-Year Overview"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:AN62`; Everything beyond it is hidden (columns after AN, rows after 62). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AR70 |
| Merged ranges | AF2:AM2, D2:P2, R2:AD2 |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `DR_FY_START` | `1` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 56.57 | 300.8 |  |
| C | 4.57 | 27.8 |  |
| D:O | 16.57 | 90.8 |  outline 1 |
| P | 16.57 | 90.8 |  |
| Q | 4.57 | 27.8 |  |
| R:AC | 16.57 | 90.8 |  outline 1 |
| AD | 16.57 | 90.8 |  |
| AE | 4.57 | 27.8 |  |
| AF:AN | 16.57 | 90.8 |  |
| AO | 10.86 | 60.8 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S5 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | center | – | – |
| S6 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S7 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S8 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S9 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S10 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S11 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `–` | right | center | 1.0 | – |
| S13 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | right | center | 1.0 | – |
| S14 | Poppins | 12.0 |  | FFFFFF | 0C142B | – | `@` | right | center | 1.0 | – |
| S15 | Poppins | 12.0 |  | FFFFFF | 0C142B | – | `–` | right | center | 1.0 | – |
| S16 | Poppins | 12.0 |  | F9AB10 | 0C142B | – | `@` | right | center | 1.0 | – |
| S17 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S18 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S19 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S20 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S21 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S22 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S23 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S24 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S26 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S27 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S28 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S29 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S30 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S31 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S32 | Poppins | 12.0 | B | 333333 | – | L:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S33 | Poppins | 12.0 |  | C08405 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S34 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S35 | Poppins | 12.0 |  | C08405 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S36 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S37 | Poppins | 4.0 |  | F0F1F4 | – | R:thin:9EA1AA | `0` | – | – | – | – |
| S38 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S39 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S40 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S41 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S42 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S43 | Poppins | 12.0 | B | 333333 | – | – | `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |
| S44 | Poppins | 12.0 | B | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S45 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S46 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S47 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S48 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S49 | Poppins | 12.0 |  | 001F37 | – | – | `#,##0,\ "K"` | – | – | – | – |
| S50 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S51 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S52 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S53 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S54 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S55 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S56 | Poppins | 12.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S57 | Poppins | 12.0 | B | 333333 | – | – | `0.0%` | right | center | 1.0 | – |
| S58 | Poppins | 12.0 |  | 001F37 | – | – | `0.0%` | – | – | – | – |
| S59 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `_(* #,##0_);_(* \(#,##0\);_(* "-"_);_(@_)` | right | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:Q=S3 R:AN=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:P=S4 Q=S3 R:AD=S4 AE=S1 AF:AM=S4 AN=S5
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S6 G:O=S1 P:Q=S3 R:AN=S1
- **T4** h=24.0 rows 4: A=S1 B=S7 C=S2 D:O=S8 P=S9 Q=S3 R:AC=S8 AD=S9 AE=S1 AF:AM=S8 AN=S5
- **T5** h=24.0 rows 5: A=S1 B=S10 C=S2 D:Q=S11 R:T=S12 U=S13 V:AD=S12 AE=S1 AF:AI=S14 AJ:AM=S15 AN=S16
- **T6** h=15.95 rows 6: A=S1 B=S17 C:E=S2 F=S6 G:H=S1 I=S18 J:O=S1 P=S3 Q=S19 R:AN=S1
- **T7** h=24.0 rows 7: A:B=S20 C=S21 D:AN=S20
- **T8** h=24.0 rows 8,15,45: A=S20 B=S22 C:AM=S23 AN=S20
- **T9** h=24.0 rows 9: A=S20 B:E=S24 F=S25 G:J=S24 K=S25 L:N=S24 O=S25 P:Q=S26 R:AC=S25 AD=S26 AE=S20 AF:AM=S27 AN=S20
- **T10** h=24.0 rows 10-11,47,53,60: A=S28 B=S29 C=S30 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T11** h=24.0 rows 12: A=S37 B=S29 C=S30 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T12** h=24.0 rows 13: A=S38 B:C=S39 D:O=S40 P=S41 Q=S20 R:AC=S40 AD=S41 AE=S20 AF:AM=S40 AN=S20
- **T13** h=24.0 rows 14: A=S20 B=S42 C:E=S43 F=S20 G:J=S43 K=S20 L:N=S43 O:AN=S20
- **T14** h=24.0 rows 16: A=S20 B=S44 C:E=S45 F=S27 G:J=S45 K=S27 L:N=S45 O=S27 P:Q=S20 R:AC=S27 AD:AE=S20 AF:AM=S27 AN=S20
- **T15** h=24.0 rows 17-19: A=S46 B=S29 C=S47 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T16** h=24.0 rows 20: A=S48 B:C=S39 D:O=S40 P=S41 Q=S20 R:AC=S40 AD=S41 AE=S20 AF:AM=S40 AN=S49
- **T17** h=24.0 rows 21: A=S38 B:C=S42 D:P=S41 Q=S20 R:AD=S41 AE=S20 AF:AM=S41 AN=S20
- **T18** h=24.0 rows 22: A=S38 B:C=S42 D:P=S50 Q=S20 R:AD=S50 AE=S20 AF:AM=S50 AN=S20
- **T19** h=24.0 rows 23,50,57: A=S38 B:AN=S20
- **T20** h=24.0 rows 24,51,58: A=S38 B=S22 C:AM=S23 AN=S20
- **T21** h=24.0 rows 25: A=S38 B:E=S45 F=S27 G:J=S45 K=S27 L:N=S45 O=S27 P:Q=S20 R:AC=S27 AD:AE=S20 AF:AM=S27 AN=S20
- **T22** h=24.0 rows 26: A=S37 B=S51 C=S47 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T23** h=24.0 rows 27-35: A=S52 B=S51 C=S47 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T24** h=24.0 rows 36: A=S53 B:C=S54 D:O=S55 P=S41 Q=S20 R:AC=S55 AD=S41 AE=S20 AF:AM=S55 AN=S20
- **T25** h=24.0 rows 37: A=S53 B:AN=S20
- **T26** h=24.0 rows 38: A=S53 B=S22 C:AM=S23 AN=S20
- **T27** h=24.0 rows 39: A=S53 B:E=S24 F=S27 G:J=S24 K=S27 L:N=S24 O=S27 P:Q=S20 R:AC=S27 AD:AE=S20 AF:AM=S27 AN=S20
- **T28** h=24.0 rows 40-41: A=S52 B=S29 C=S30 D:O=S31 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T29** h=24.0 rows 42: A=S53 B:C=S54 D:O=S55 P=S41 Q=S20 R:AC=S55 AD=S41 AE=S20 AF:AM=S55 AN=S49
- **T30** h=24.0 rows 43: A=S53 B:C=S56 D:O=S57 P=S50 Q=S20 R:AC=S57 AD=S50 AE=S20 AF:AM=S57 AN=S58
- **T31** h=None rows 44: A:AN=S20
- **T32** h=None rows 46,52,59: A=S20 B:O=S27 P:Q=S20 R:AC=S27 AD:AE=S20 AF:AM=S27 AN=S20
- **T33** h=24.0 rows 48,55,61: A=S20 B:C=S54 D:O=S55 P=S41 Q=S20 R:AC=S55 AD=S41 AE=S20 AF:AM=S55 AN=S20
- **T34** h=24.0 rows 49,56: A=S20 B:C=S56 D:O=S57 P=S50 Q=S20 R:AC=S57 AD=S50 AE=S20 AF:AM=S57 AN=S20
- **T35** h=24.0 rows 54: A=S28 B=S29 C=S30 D:O=S59 P=S32 Q=S28 R:AC=S33 AD=S32 AE=S28 AF:AI=S34 AJ:AM=S35 AN=S36
- **T36** h=24.0 rows 62: A=S20 B:C=S56 D:P=S50 Q=S20 R:AD=S50 AE=S20 AF:AM=S50 AN=S20

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": 2024, "R": 2025, "AF": 2025}
- r4: {"B": "P&L - Multi Year", "P": "FY 2024", "AD": "FY 2025"}
- r5: {"D": "Actuals", "E": "Actuals", "F": "Actuals", "G": "Actuals", "H": "Actuals", "I": "Actuals", "J": "Actuals", "K": "Actuals", "L": "Actuals", "M": "Actuals", "N": "Actuals", "O": "Actuals", "P": "Actuals", "AF": "Actuals", "AG": "Actuals", "AH": "Actuals", "AI": "Actuals"}
- r8: {"B": "Income"}
- r10: {"B": "Revenue - Licenses"}
- r11: {"B": "Revenue - Professional Services"}
- r12: {"B": "Revenue - Integrations"}
- r13: {"B": "Total Income"}
- r15: {"B": "Cost of Sales"}
- r17: {"B": "Cost of Sales - License"}
- r18: {"B": "Cost of Sales - Integrations"}
- r19: {"B": "Cost of Sales - Professional Services"}
- r20: {"B": "Total Cost of Sales"}
- r21: {"B": "Gross Profit"}
- r22: {"B": "Gross Margin (%)"}
- r24: {"B": "Operating Expenses ex. D&A"}
- r26: {"B": "Marketing"}
- r27: {"B": "Finance"}
- r28: {"B": "G&A"}
- r29: {"B": "IT & Equipment"}
- r30: {"B": "Legal"}
- r31: {"B": "Office Expenses"}
- r32: {"B": "Payroll Related"}
- r33: {"B": "People Development"}
- r34: {"B": "Software Subscriptions"}
- r35: {"B": "Travel"}
- r36: {"B": "Total Operating Expenses ex. D&A"}
- r38: {"B": "Other Income and Expenses"}
- r40: {"B": "Other Expense"}
- r41: {"B": "Other Income"}
- r42: {"B": "EBITDA"}
- r43: {"B": "EBITDA Margin %"}
- r45: {"B": "Depreciation & Amortization"}
- r47: {"B": "Depreciation & Amortization"}
- r48: {"B": "EBIT"}
- r49: {"B": "EBIT %"}
- r51: {"B": "Interest and Income Expenses"}
- r53: {"B": "Interest Income"}
- r54: {"B": "Interest Expense"}
- r55: {"B": "EBT"}
- r56: {"B": "EBT %"}
- r58: {"B": "Taxes"}
- r60: {"B": "Tax"}
- r61: {"B": "Net Profit"}
- r62: {"B": "Net Margin %"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D4, R4 (example `D4`): `=IF(DR_FY_START<=6,EOMONTH(DATE(D2,DR_FY_START,1),0),EOMONTH(DATE(D2-1,DR_FY_START,1),0))`
- **F2** at E4:O4, S4:AC4 (example `E4`): `=EOMONTH(D4,1)`
- **F3** at AF4 (example `AF4`): `="Q1 - "&RIGHT($P4,2)`
- **F4** at AG4 (example `AG4`): `="Q2 - "&RIGHT($P$4,2)`
- **F5** at AH4 (example `AH4`): `="Q3 - "&RIGHT($P$4,2)`
- **F6** at AI4, AM4 (example `AI4`): `="Q4 - "&RIGHT($AD$4,2)`
- **F7** at AJ4 (example `AJ4`): `="Q1 - "&RIGHT($AD$4,2)`
- **F8** at AK4 (example `AK4`): `="Q2 - "&RIGHT($AD$4,2)`
- **F9** at AL4 (example `AL4`): `="Q3 - "&RIGHT($AD$4,2)`
- **F10** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F11** at R5:AC5 (example `R5`): `=IF(R4<=$R$3,"Actuals","Budget")`
- **F12** at AD5 (example `AD5`): `=AC5`
- **F13** at AJ5 (example `AJ5`): `=IF(R5=T5,R5,"A+B")`
- **F14** at AK5 (example `AK5`): `=IF(U5=W5,U5,"A+B")`
- **F15** at AL5 (example `AL5`): `=IF(X5=Z5,X5,"A+B")`
- **F16** at AM5 (example `AM5`): `=IF(AA5=AC5,AA5,"A+B")`
- **F17** at D10:D12, R10:AC12 (example `D10`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B10,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Income")`
- **F18** at E10:O12 (example `E10`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B$10,"[Reporting Month]",E$4,"[Scenario]",E$5,"[Account Group L2]","Income")`
- **F19** at P10:P13, AD10:AD13, P17:P20, AD17:AD21, P26:P36, AD26:AD36, P40:P42, AD40:AD42, P47:P48, AD47:AD48, P53:P55, AD53:AD55, P60:P61, AD60:AD61 (example `P10`): `=IFERROR(SUM(D10:O10),"NA")`
- **F20** at AF10:AF12, AF17:AF19, AF26:AF35, AF40:AF41, AF47, AF53:AF54, AF60 (example `AF10`): `=IFERROR(SUM(D10:F10),"NA")`
- **F21** at AG10:AG12, AG17:AG19, AG26:AG35, AG40:AG41, AG47, AG53:AG54, AG60 (example `AG10`): `=IFERROR(SUM(G10:I10),"NA")`
- **F22** at AH10:AH12, AH17:AH19, AH26:AH35, AH40:AH41, AH47, AH53:AH54, AH60 (example `AH10`): `=IFERROR(SUM(J10:L10),"NA")`
- **F23** at AI10:AI12, AI17:AI19, AI26:AI35, AI40:AI41, AI47, AI53:AI54, AI60 (example `AI10`): `=IFERROR(SUM(M10:O10),"NA")`
- **F24** at AJ10:AJ12, AJ17:AJ19, AJ26:AJ35, AJ40:AJ41, AJ47, AJ53:AJ54, AJ60 (example `AJ10`): `=IFERROR(SUM(R10:T10),"NA")`
- **F25** at AK10:AK12, AK17:AK19, AK26:AK35, AK40:AK41, AK47, AK53:AK54, AK60 (example `AK10`): `=IFERROR(SUM(U10:W10),"NA")`
- **F26** at AL10:AL12, AL17:AL19, AL26:AL35, AL40:AL41, AL47, AL53:AL54, AL60 (example `AL10`): `=IFERROR(SUM(X10:Z10),"NA")`
- **F27** at AM10:AM12, AM17:AM19, AM26:AM35, AM40:AM41, AM47, AM53:AM54, AM60 (example `AM10`): `=IFERROR(SUM(AA10:AC10),"NA")`
- **F28** at D13:O13, R13:AC13, AF13:AM13, D20:O20, R20:AC20, AF20:AM20 (example `D13`): `=IFERROR(SUM(D10:D12),"NA")`
- **F29** at D17:O19, R17:AC19 (example `D17`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Cost of Goods Sold")`
- **F30** at D21:P21, R21:AC21, AF21:AM21 (example `D21`): `=IFERROR(D13-D20,"NA")`
- **F31** at D22:P22, R22:AD22, AF22:AM22 (example `D22`): `=IFERROR(D21/D13,"NA")`
- **F32** at D26:O35, R26:AC35 (example `D26`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Operating Expense")`
- **F33** at D36:O36, R36:AC36, AF36:AM36 (example `D36`): `=IFERROR(SUM(D26:D35),"NA")`
- **F34** at D40:O41 (example `D40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Report_Field]",$B40)`
- **F35** at R40:AC41 (example `R40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",R$4,"[Scenario]",R$5,"[Account Group L2]",$B40)`
- **F36** at D42:O42, R42:AC42, AF42:AM42 (example `D42`): `=IFERROR(D21-D36+D40-D41,"NA")`
- **F37** at D43:P43, R43:AD43, AF43:AM43 (example `D43`): `=IFERROR(D42/D13,"NA")`
- **F38** at D47:O47, R47:AC47, D53:O54, R53:AC54, D60:O60, R60:AC60 (example `D47`): `=_xldudf_DR_GET(Value,"[Reporting Month]",D$4,"[Scenario]",D$5,"[DR_KPI]",$B47)`
- **F39** at D48:O48, R48:AC48, AF48:AM48 (example `D48`): `=IFERROR(D42-D47,"NA")`
- **F40** at D49:P49, R49:AD49, AF49:AM49 (example `D49`): `=IFERROR(D48/D13,"NA")`
- **F41** at D55:O55, R55:AC55, AF55:AM55 (example `D55`): `=IFERROR(D48+D53-D54,"NA")`
- **F42** at D56:P56, R56:AD56, AF56:AM56 (example `D56`): `=IFERROR(D55/D13,"NA")`
- **F43** at D61:O61, R61:AC61, AF61:AM61 (example `D61`): `=D55-D60`
- **F44** at D62:P62, R62:AD62, AF62:AM62 (example `D62`): `=IFERROR(D61/D13,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **cell value equal** `"Budget"` → fontColor `F9AB10` — on AF5:AR5 R5:AD5
  - json: `{"dxf": {"fontColor": "F9AB10"}, "formulas": ["\"Budget\""], "kind": "cellIs", "op": "equal", "priority": 1, "ranges": "AF5:AR5 R5:AD5"}`
- [P3] **cell value equal** `"Budget"` → bold `False`, fontColor `F93576`, italic `False` — on D5:P5
  - json: `{"dxf": {"bold": false, "fontColor": "F93576", "italic": false}, "formulas": ["\"Budget\""], "kind": "cellIs", "op": "equal", "priority": 3, "ranges": "D5:P5"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
