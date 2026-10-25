# Spec: pnl-dr-sc-style → sheet "P&L YoY"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:T62`; Everything beyond it is hidden (columns after T, rows after 62). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 85 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AI64 |
| Merged ranges | none |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 56.57 | 300.8 |  |
| C | 4.57 | 27.8 |  |
| D:E | 16.57 | 90.8 |  outline 1 |
| F | 19.57 | 106.5 |  outline 1 |
| G | 16.57 | 90.8 |  outline 1 |
| H | 4.57 | 27.8 |  |
| I:L | 16.57 | 90.8 |  outline 1 |
| M | 4.57 | 27.8 |  |
| N:Q | 16.57 | 90.8 |  outline 1 |
| R | 4.57 | 27.8 |  |
| S | 40.57 | 216.8 |  |
| T | 16.57 | 90.8 |  |
| U | 16.86 | 92.2 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S5 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S6 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S7 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S8 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S9 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S10 | Poppins | 9.0 | B | 0C142B | 0C142B | – | `–` | left | top | – | – |
| S11 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S12 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S13 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S14 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S15 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S16 | Poppins | 12.0 | B | 8A2BE2 | – | – | `–` | – | center | – | – |
| S17 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S18 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S19 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S20 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S21 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S22 | Poppins | 14.0 | B | 7FFFD4 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S23 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S24 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S25 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S26 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S27 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S28 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S29 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S30 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S31 | Poppins | 12.0 |  | 4646CE | EAEAFF | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S32 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S33 | Poppins | 4.0 |  | F0F1F4 | – | R:thin:9EA1AA | `0` | – | – | – | – |
| S34 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S35 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S36 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S37 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S38 | Calibri | 11.0 |  | 001F37 | – | T:thin:9EA1AA | `–` | – | – | – | – |
| S39 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S40 | Poppins | 12.0 | B | 333333 | – | – | `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |
| S41 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S42 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S43 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S44 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S45 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S46 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S47 | Poppins | 12.0 | B | 626364 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S48 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S49 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S50 | Poppins | 12.0 | B | 8A2BE2 | – | – | `–` | – | – | – | – |
| S51 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S52 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S53 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `–` | centerContinuous | center | – | – |
| S54 | Poppins | 12.0 |  | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S55 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S56 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S57 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S58 | Poppins | 12.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S59 | Poppins | 12.0 | B | 333333 | – | – | `0.0%` | right | center | 1.0 | – |
| S60 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%` | right | center | 1.0 | – |
| S61 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S62 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:S=S3 T=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:G=S4 H=S1 I:L=S4 M=S1 N:Q=S4 R=S3 S=S4 T=S1
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S5 G:O=S1 P:S=S3 T=S1
- **T4** h=24.0 rows 4: A=S1 B=S6 C=S2 D:E=S7 F=S5 G:H=S1 I:J=S7 K:M=S1 N:O=S7 P:S=S3 T=S1
- **T5** h=24.0 rows 5: A=S1 B=S8 C=S2 D:G=S9 H=S1 I:L=S9 M=S1 N:Q=S9 R:S=S3 T=S1
- **T6** h=15.95 rows 6: A=S1 B=S10 C:E=S2 F=S5 G:H=S1 I=S11 J:O=S1 P=S3 Q=S12 R:S=S3 T=S1
- **T7** h=24.0 rows 7: A:B=S13 C:D=S14 E=S15 F:T=S13
- **T8** h=24.0 rows 8: A=S16 B=S17 C:Q=S18 R:S=S19 T=S20
- **T9** h=24.0 rows 9: A=S13 B:C=S21 D=S22 E:G=S21 H=S20 I:L=S21 M=S20 N:Q=S21 R=S20 S=S23 T=S20
- **T10** h=24.0 rows 10-11,47,53-54,60: A=S24 B=S25 C=S26 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T11** h=24.0 rows 12: A=S33 B=S25 C=S26 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T12** h=24.0 rows 13: A=S34 B:C=S35 D:F=S36 G=S37 H=S13 I:K=S36 L=S37 M=S13 N:P=S36 Q=S37 R=S13 S=S38 T=S13
- **T13** h=24.0 rows 14: A=S13 B=S39 C:G=S40 H=S13 I:L=S40 M=S13 N:Q=S40 R:T=S13
- **T14** h=24.0 rows 15,45,58: A=S13 B=S17 C:Q=S18 R:S=S19 T=S13
- **T15** h=24.0 rows 16: A=S13 B:G=S41 H=S13 I:L=S41 M=S13 N:Q=S41 R=S13 S=S42 T=S13
- **T16** h=24.0 rows 17-19: A=S43 B=S44 C=S45 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T17** h=24.0 rows 20: A=S46 B:C=S35 D:F=S36 G=S37 H=S47 I:K=S36 L=S37 M=S47 N:P=S36 Q=S37 R=S13 S=S38 T=S13
- **T18** h=24.0 rows 21: A=S46 B:C=S39 D:F=S48 G=S49 H=S13 I:K=S48 L=S49 M=S13 N:P=S48 Q=S49 R:T=S13
- **T19** h=24.0 rows 22: A=S46 B:C=S39 D:Q=S49 R:T=S13
- **T20** h=24.0 rows 23,50,57: A=S34 B:T=S13
- **T21** h=24.0 rows 24,51: A=S34 B=S17 C:Q=S18 R:S=S19 T=S13
- **T22** h=24.0 rows 25: A=S34 B:G=S41 H=S13 I:L=S41 M=S50 N:Q=S41 R=S50 S=S42 T=S13
- **T23** h=24.0 rows 26-28: A=S33 B=S44 C=S45 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T24** h=24.0 rows 29-35: A=S51 B=S44 C=S45 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T25** h=24.0 rows 36: A=S52 B=S35 C=S53 D:F=S36 G=S37 H=S54 I:K=S36 L=S37 M=S54 N:P=S36 Q=S37 R=S13 S=S38 T=S13
- **T26** h=24.0 rows 37,44: A=S52 B:T=S13
- **T27** h=24.0 rows 38: A=S52 B=S17 C:Q=S18 R:S=S19 T=S13
- **T28** h=24.0 rows 39: A=S52 B:G=S21 H=S13 I:L=S21 M=S13 N:Q=S21 R=S13 S=S42 T=S13
- **T29** h=24.0 rows 40-41: A=S51 B=S25 C=S26 D:E=S27 F=S28 G=S29 H=S30 I:J=S27 K=S28 L=S29 M=S30 N:O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T30** h=24.0 rows 42: A=S52 B:C=S55 D:F=S56 G=S57 H=S13 I:K=S56 L=S57 M=S13 N:P=S56 Q=S57 R=S13 S=S38 T=S13
- **T31** h=24.0 rows 43: A=S52 B:C=S58 D:Q=S59 R:T=S13
- **T32** h=None rows 46,52,59: A=S13 B:G=S42 H=S13 I:L=S42 M=S13 N:Q=S42 R=S13 S=S42 T=S13
- **T33** h=24.0 rows 48: A=S13 B:C=S55 D:F=S56 G=S57 H=S13 I:K=S56 L=S57 M=S13 N:P=S56 Q=S57 R=S13 S=S38 T=S13
- **T34** h=24.0 rows 49: A=S13 B:C=S58 D:Q=S59 R:T=S13
- **T35** h=24.0 rows 55: A=S13 B:C=S55 D:F=S56 G=S60 H=S13 I:K=S56 L=S60 M=S13 N:P=S56 Q=S60 R=S13 S=S38 T=S13
- **T36** h=24.0 rows 56: A=S34 B:C=S58 D:Q=S59 R:T=S13
- **T37** h=24.0 rows 61: A=S13 B=S61 C=S38 D=S62 E:F=S56 G=S60 H=S13 I:K=S56 L=S60 M=S13 N:P=S56 Q=S60 R=S13 S=S38 T=S13
- **T38** h=24.0 rows 62: A=S13 B:C=S58 D:G=S49 H=S13 I:L=S49 M=S13 N:R=S49 S=S50 T=S13

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": "MTD", "I": "QTD", "N": "YTD", "S": "Variance Explanation"}
- r5: {"D": "Actuals", "E": "Actuals", "F": "∆ vs PY", "G": "% ∆ vs PY", "I": "Actuals", "J": "Actuals", "K": "∆ vs PY", "L": "% ∆ vs PY", "N": "Actuals", "O": "Actuals", "P": "∆ vs PY", "Q": "% ∆ vs PY"}
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
- r36: {"B": "Total Operating Expense"}
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
- r53: {"B": "Interest Expense"}
- r54: {"B": "Interest Income"}
- r55: {"B": "EBT"}
- r56: {"B": "EBT %"}
- r58: {"B": "Taxes"}
- r60: {"B": "Tax"}
- r61: {"B": "Net Profit"}
- r62: {"B": "Net Margin %"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at B4 (example `B4`): `="P&L - YoY "`
- **F2** at D4 (example `D4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F3** at E4, J4, O4 (example `E4`): `=EOMONTH(D4,-12)`
- **F4** at I4, N4 (example `I4`): `=D4`
- **F5** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F6** at D10:E12 (example `D10`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Income")`
- **F7** at F10:F12, K10:K12, P10:P12, F17:F19, K17:K19, P17:P19, F22:G22, K22, P22, F26:F35, K26:K35, P26:P35, F40:F41, K40:K41, P40:P41, F43, K43, P43, F47, K47, P47, F49, K49, P49, F53:F54, K53:K54, P53:P54, F60, K60, P60 (example `F10`): `=IFERROR(D10-E10,"NA")`
- **F8** at G10:G13, L10:L13, Q10:Q13, G17:G21, L17:L22, Q17:Q22, G26:G36, L26:L36, Q26:Q36, G40:G43, L40:L43, Q40:Q43, G47:G49, L47:L49, Q47:Q49, G53:G55, L53:L55, Q53:Q55, G60:G61, L60:L61, Q60:Q61 (example `G10`): `=IFERROR(D10/E10-1,"NA")`
- **F9** at I10:J12 (example `I10`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",I$4,"[Scenario]",I$5,"[Account Group L2]","Income")`
- **F10** at N10:O12 (example `N10`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",N$4,"[Scenario]",N$5,"[Account Group L2]","Income")`
- **F11** at D13:F13, I13:K13, N13:P13, F20 (example `D13`): `=IFERROR(SUM(D10:D12),"NA")`
- **F12** at D17:E19 (example `D17`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Cost of Goods Sold")`
- **F13** at I17:I19 (example `I17`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[Account Group L2]","Cost of Goods Sold")`
- **F14** at J17:J19 (example `J17`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[Account Group L2]","Cost of Goods Sold")`
- **F15** at N17:N19 (example `N17`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[Account Group L2]","Cost of Goods Sold")`
- **F16** at O17:O19 (example `O17`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]","Cost of Goods Sold")`
- **F17** at D20:E20 (example `D20`): `=SUM(D17:D19)`
- **F18** at I20:K20, N20:P20 (example `I20`): `=IFERROR(SUM(I19:I19),"NA")`
- **F19** at D21:F21, I21:K21, N21:P21 (example `D21`): `=IFERROR(D13-D20,"NA")`
- **F20** at D22:E22, I22:J22, N22:O22 (example `D22`): `=IFERROR(D21/D13,"NA")`
- **F21** at D26:E35 (example `D26`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Operating Expense")`
- **F22** at I26:I35 (example `I26`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[Account Group L2]","Operating Expense")`
- **F23** at J26:J35 (example `J26`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[Account Group L2]","Operating Expense")`
- **F24** at N26:N35 (example `N26`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[Account Group L2]","Operating Expense")`
- **F25** at O26:O35 (example `O26`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]","Operating Expense")`
- **F26** at D36:F36, I36:K36, N36:P36 (example `D36`): `=IFERROR(SUM(D26:D35),"NA")`
- **F27** at D40:E41, I40:J41, N40:N41 (example `D40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Report_Field]",$B40)`
- **F28** at O40:O41 (example `O40`): `=_xldudf_DR_YTD(Value_EBITDA,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]",$B40)`
- **F29** at D42:F42, I42:K42, N42:P42 (example `D42`): `=IFERROR(D21-D36+D40-D41,"NA")`
- **F30** at D43:E43, I43:J43, N43:O43 (example `D43`): `=IFERROR(D42/D13,"NA")`
- **F31** at D47:E47, D53:E54, D60:E60 (example `D47`): `=_xldudf_DR_GET(Value,"[Reporting Month]",D$4,"[Scenario]",D$5,"[DR_KPI]",$B47)`
- **F32** at I47, I53:I54 (example `I47`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[DR_KPI]",$B47)`
- **F33** at J47, J53:J54 (example `J47`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[DR_KPI]",$B47)`
- **F34** at N47, N53:N54 (example `N47`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[DR_KPI]",$B47)`
- **F35** at O47, O53:O54 (example `O47`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[DR_KPI]",$B47)`
- **F36** at D48:F48, I48:K48, N48:P48, D61:F61, I61:K61, N61:P61 (example `D48`): `=IFERROR(D42-D47,"NA")`
- **F37** at D49:E49, I49:J49, N49:O49 (example `D49`): `=IFERROR(D48/D13,"NA")`
- **F38** at D55:F55, I55:K55, N55:P55 (example `D55`): `=IFERROR(D48+D53-D54,"NA")`
- **F39** at D56:G56, I56:L56, N56:Q56 (example `D56`): `=IFERROR(D55/D13,"NA")`
- **F40** at I60:J60 (example `I60`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",I$4,"[Scenario]",I$5,"[DR_KPI]",$B60)`
- **F41** at N60:O60 (example `N60`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",N$4,"[Scenario]",N$5,"[DR_KPI]",$B60)`
- **F42** at D62:G62, I62:L62, N62:Q62 (example `D62`): `=IFERROR(D61/D13,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+4px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **formula** `$B$6="GBP"` → numFmt `\£#,##0,\ "K"` — on D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61
  - json: `{"dxf": {"numFmt": "\\£#,##0,\\ \"K\""}, "formulas": ["$B$6=\"GBP\""], "kind": "expression", "priority": 1, "ranges": "D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61"}`
- [P2] **formula** `$B$6="EUR"` → numFmt `\€#,##0,\ "K"` — on D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61
  - json: `{"dxf": {"numFmt": "\\€#,##0,\\ \"K\""}, "formulas": ["$B$6=\"EUR\""], "kind": "expression", "priority": 2, "ranges": "D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61"}`
- [P3] **formula** `$B$6="USD"` → numFmt `"$"#,##0,\ "K"` — on D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61
  - json: `{"dxf": {"numFmt": "\"$\"#,##0,\\ \"K\""}, "formulas": ["$B$6=\"USD\""], "kind": "expression", "priority": 3, "ranges": "D10:F13 I10:K13 N10:P13 D17:F21 I17:K21 N17:P21 D26:F36 I26:K36 N26:P36 D40:F42 I40:K42 N40:P42 D47:F48 I47:K48 N47:P48 D53:F55 I53:K55 N53:P55 D60:F61 I60:K61 N60:P61"}`
- [P4] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on F10:F12 K10:K12 P10:P12 F17:F19 K17:K19 P17:P19 F26:F35 K26:K35 P26:P35 F40:F41 K40:K41 P40:P41 F47 K47 P47 F53:F54 K53:K54 P53:P54 F60 K60 P60
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 4, "ranges": "F10:F12 K10:K12 P10:P12 F17:F19 K17:K19 P17:P19 F26:F35 K26:K35 P26:P35 F40:F41 K40:K41 P40:P41 F47 K47 P47 F53:F54 K53:K54 P53:P54 F60 K60 P60"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
