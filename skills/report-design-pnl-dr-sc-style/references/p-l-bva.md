# Spec: pnl-dr-sc-style → sheet "P&L BvA"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:T63`; Everything beyond it is hidden (columns after T, rows after 63). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AI64 |
| Merged ranges | D2:G2, I2:L2, N2:Q2 |
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
| F:G | 16.57 | 90.8 |  outline 1 |
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
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S5 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S6 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S7 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S8 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S9 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S10 | Poppins | 12.0 |  | F9AB10 | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | – | center | – | – |
| S12 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S13 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S14 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S15 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S16 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S17 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S18 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S19 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S20 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S21 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S22 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S23 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S24 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S26 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S27 | Poppins | 12.0 |  | C08405 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
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
| S44 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S45 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S46 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S47 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S48 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S49 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S50 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S51 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S52 | Poppins | 12.0 |  | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S53 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S54 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S55 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S56 | Poppins | 12.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S57 | Poppins | 12.0 | B | 333333 | – | – | `0.0%` | right | center | 1.0 | – |
| S58 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%` | right | center | 1.0 | – |
| S59 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S60 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S61 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | wrap |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:S=S3 T=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:G=S4 H=S1 I:L=S4 M=S1 N:Q=S4 R=S3 S=S4 T=S1
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S5 G:O=S1 P:S=S3 T=S1
- **T4** h=24.0 rows 4: A=S1 B=S6 C=S2 D:E=S7 F=S5 G:H=S1 I:J=S7 K:M=S1 N:O=S7 P:S=S3 T=S1
- **T5** h=24.0 rows 5: A=S1 B=S8 C=S2 D=S9 E=S10 F=S9 G=S11 H=S1 I=S9 J=S10 K=S9 L=S11 M=S1 N:P=S9 Q=S11 R:S=S3 T=S1
- **T6** h=15.95 rows 6: A=S1 B=S12 C:E=S2 F=S5 G:H=S1 I=S13 J:O=S1 P=S3 Q=S14 R:S=S3 T=S1
- **T7** h=24.0 rows 7: A:B=S15 C:D=S16 E=S17 F:T=S15
- **T8** h=24.0 rows 8: A=S15 B:Q=S18 R:S=S19 T=S20
- **T9** h=24.0 rows 9: A=S15 B:G=S21 H=S20 I:L=S21 M=S20 N:Q=S21 R=S20 S=S22 T=S20
- **T10** h=24.0 rows 10-11,47,53-54,60: A=S23 B=S24 C=S25 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T11** h=24.0 rows 12: A=S33 B=S24 C=S25 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T12** h=24.0 rows 13: A=S34 B:C=S35 D:F=S36 G=S37 H=S15 I:K=S36 L=S37 M=S15 N:P=S36 Q=S37 R=S15 S=S38 T=S15
- **T13** h=24.0 rows 14: A=S15 B=S39 C:G=S40 H=S15 I:L=S40 M=S15 N:Q=S40 R:T=S15
- **T14** h=24.0 rows 15,45,51: A=S15 B:Q=S18 R:S=S19 T=S15
- **T15** h=24.0 rows 16: A=S15 B:G=S41 H=S15 I:L=S41 M=S15 N:Q=S41 R=S15 S=S42 T=S15
- **T16** h=24.0 rows 17-19: A=S43 B=S24 C=S44 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T17** h=24.0 rows 20: A=S45 B:C=S35 D:F=S36 G=S37 H=S15 I:K=S36 L=S37 M=S15 N:P=S36 Q=S37 R=S15 S=S38 T=S15
- **T18** h=24.0 rows 21: A=S45 B:C=S39 D:F=S46 G=S47 H=S15 I:K=S46 L=S47 M=S15 N:P=S46 Q=S47 R:T=S15
- **T19** h=24.0 rows 22: A=S45 B:C=S39 D:Q=S47 R:T=S15
- **T20** h=24.0 rows 23,50: A=S34 B:T=S15
- **T21** h=24.0 rows 24: A=S34 B:Q=S18 R:S=S19 T=S15
- **T22** h=24.0 rows 25: A=S34 B:G=S41 H=S15 I:L=S41 M=S15 N:Q=S41 R=S15 S=S42 T=S15
- **T23** h=24.0 rows 26-28: A=S33 B=S48 C=S44 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T24** h=24.0 rows 29-35: A=S49 B=S48 C=S44 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T25** h=24.0 rows 36: A=S50 B:C=S51 D:F=S36 G=S37 H=S52 I:K=S36 L=S37 M=S52 N:P=S36 Q=S37 R=S15 S=S38 T=S15
- **T26** h=24.0 rows 37: A=S50 B:T=S15
- **T27** h=24.0 rows 38: A=S50 B:Q=S18 R:S=S19 T=S15
- **T28** h=24.0 rows 39: A=S50 B:G=S21 H=S15 I:L=S21 M=S15 N:Q=S21 R=S15 S=S42 T=S15
- **T29** h=24.0 rows 40-41: A=S49 B=S24 C=S25 D=S26 E=S27 F=S28 G=S29 H=S30 I=S26 J=S27 K=S28 L=S29 M=S30 N=S26 O=S27 P=S28 Q=S29 R=S30 S=S31 T=S32
- **T30** h=24.0 rows 42: A=S50 B:C=S53 D:F=S54 G=S55 H=S15 I:K=S54 L=S55 M=S15 N:P=S54 Q=S55 R=S15 S=S38 T=S15
- **T31** h=24.0 rows 43: A=S50 B:C=S56 D:Q=S57 R:T=S15
- **T32** h=None rows 44,57: A:T=S15
- **T33** h=None rows 46,52,59: A=S15 B:G=S42 H=S15 I:L=S42 M=S15 N:Q=S42 R=S15 S=S42 T=S15
- **T34** h=24.0 rows 48: A=S15 B:C=S53 D:F=S54 G=S55 H=S15 I:K=S54 L=S55 M=S15 N:P=S54 Q=S55 R=S15 S=S38 T=S15
- **T35** h=24.0 rows 49,56: A=S34 B:C=S56 D:Q=S57 R:T=S15
- **T36** h=24.0 rows 55: A=S34 B:C=S53 D:F=S54 G=S58 H=S15 I:K=S54 L=S58 M=S15 N:P=S54 Q=S58 R=S15 S=S38 T=S15
- **T37** h=24.0 rows 58: A=S15 B=S18 C:Q=S59 R:S=S19 T=S15
- **T38** h=24.0 rows 61: A=S15 B=S60 C=S38 D:F=S54 G=S58 H=S15 I:K=S54 L=S58 M=S15 N:P=S54 Q=S58 R=S15 S=S38 T=S15
- **T39** h=24.0 rows 62: A=S34 B:C=S56 D:G=S47 H=S15 I:L=S47 M=S15 N:R=S47 S:T=S15
- **T40** h=24.0 rows 63: A=S34 B:D=S15 E=S61 F:T=S15

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": "MTD", "I": "QTD", "N": "YTD", "S": "Variance Explanation"}
- r4: {"B": "P&L - BvA"}
- r5: {"D": "Actuals", "E": "Budget", "F": "∆ vs Budget", "G": "% ∆ vs Budget", "I": "Actuals", "J": "Budget", "K": "∆ vs Budget", "L": "% ∆ vs Budget", "N": "Actuals", "O": "Budget", "P": "∆ vs Budget", "Q": "% ∆ vs Budget"}
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
- r36: {"B": "Other Miscellaneous Service Cost"}
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
- r63: {"E": " "}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D4 (example `D4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at E4, J4, O4 (example `E4`): `=D4`
- **F3** at I4, N4 (example `I4`): `=D4`
- **F4** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F5** at D10:E12 (example `D10`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Income")`
- **F6** at F10:F12, K10:K12, P10:P12, F17:F19, K17:K19, P17:P19, F22:G22, K22, P22, F26:F35, K26:K35, P26:P35, F40:F41, K40:K41, P40:P41, F43, K43, P43, F47, K47, P47, F49, K49, P49, F53:F54, K53:K54, P53:P54, F60, K60, P60 (example `F10`): `=IFERROR(D10-E10,"NA")`
- **F7** at G10:G13, L10:L13, Q10:Q13, G17:G21, L17:L22, Q17:Q22, G26:G36, L26:L36, Q26:Q36, G40:G43, L40:L43, Q40:Q43, G47:G49, L47:L49, Q47:Q49, G53:G55, L53:L55, Q53:Q55, G60:G61, L60:L61, Q60:Q61 (example `G10`): `=IFERROR(D10/E10-1,"NA")`
- **F8** at I10:J12 (example `I10`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",I$4,"[Scenario]",I$5,"[Account Group L2]","Income")`
- **F9** at N10:O12 (example `N10`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",N$4,"[Scenario]",N$5,"[Account Group L2]","Income")`
- **F10** at D13:F13, I13:K13, N13:P13, D20:F20, I20:K20, N20:P20 (example `D13`): `=IFERROR(SUM(D10:D12),"NA")`
- **F11** at D17:E19 (example `D17`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Cost of Goods Sold")`
- **F12** at I17:I19 (example `I17`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[Account Group L2]","Cost of Goods Sold")`
- **F13** at J17:J19 (example `J17`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[Account Group L2]","Cost of Goods Sold")`
- **F14** at N17:N19 (example `N17`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[Account Group L2]","Cost of Goods Sold")`
- **F15** at O17:O19 (example `O17`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]","Cost of Goods Sold")`
- **F16** at D21:F21, I21:K21, N21:P21 (example `D21`): `=IFERROR(D13-D20,"NA")`
- **F17** at D22:E22, I22:J22, N22:O22 (example `D22`): `=IFERROR(D21/D13,"NA")`
- **F18** at D26:E35 (example `D26`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Operating Expense")`
- **F19** at I26:I35 (example `I26`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[Account Group L2]","Operating Expense")`
- **F20** at J26:J35 (example `J26`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[Account Group L2]","Operating Expense")`
- **F21** at N26:N35 (example `N26`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[Account Group L2]","Operating Expense")`
- **F22** at O26:O35 (example `O26`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]","Operating Expense")`
- **F23** at D36:F36, I36:K36, N36:P36 (example `D36`): `=IFERROR(SUM(D26:D35),"NA")`
- **F24** at D40:D41, I40:I41, N40:N41 (example `D40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Report_Field]",$B40)`
- **F25** at E40:E41 (example `E40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",E$4,"[Scenario]",E$5,"[Account Group L2]",$B40)`
- **F26** at J40:J41 (example `J40`): `=_xldudf_DR_QTD(Value_EBITDA,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[Account Group L2]",$B40)`
- **F27** at O40:O41 (example `O40`): `=_xldudf_DR_YTD(Value_EBITDA,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[Account Group L2]",$B40)`
- **F28** at D42:F42, I42:K42, N42:P42 (example `D42`): `=IFERROR(D21-D36+D40-D41,"NA")`
- **F29** at D43:E43, I43:J43, N43:O43 (example `D43`): `=IFERROR(D42/D13,"NA")`
- **F30** at D47:E47, D53:E54, D60:E60 (example `D47`): `=_xldudf_DR_GET(Value,"[Reporting Month]",D$4,"[Scenario]",D$5,"[DR_KPI]",$B47)`
- **F31** at I47 (example `I47`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$I$4,"[Scenario]",$I$5,"[DR_KPI]",$B47)`
- **F32** at J47 (example `J47`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$J$4,"[Scenario]",$J$5,"[DR_KPI]",$B47)`
- **F33** at N47 (example `N47`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$N$4,"[Scenario]",$N$5,"[DR_KPI]",$B47)`
- **F34** at O47 (example `O47`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$O$4,"[Scenario]",$O$5,"[DR_KPI]",$B47)`
- **F35** at D48:F48, I48:K48, N48:P48, D61:F61, I61:K61, N61:P61 (example `D48`): `=IFERROR(D42-D47,"NA")`
- **F36** at D49:E49, I49:J49, N49:O49 (example `D49`): `=IFERROR(D48/D13,"NA")`
- **F37** at I53:J54, I60:J60 (example `I53`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",I$4,"[Scenario]",I$5,"[DR_KPI]",$B53)`
- **F38** at N53:O54, N60:O60 (example `N53`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",N$4,"[Scenario]",N$5,"[DR_KPI]",$B53)`
- **F39** at D55:F55, I55:K55, N55:P55 (example `D55`): `=IFERROR(D48+D53-D54,"NA")`
- **F40** at D56:G56, I56:L56, N56:Q56 (example `D56`): `=IFERROR(D55/D13,"NA")`
- **F41** at D62:G62, I62:L62, N62:Q62 (example `D62`): `=IFERROR(D61/D13,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on F10:F12 K10:K12 P10:P12 F17:F19 K17:K19 P17:P19 F26:F35 K26:K35 P26:P35 F40:F41 K40:K41 P40:P41 F47 K47 P47 F53:F54 K53:K54 P53:P54 F60 K60 P60
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 1, "ranges": "F10:F12 K10:K12 P10:P12 F17:F19 K17:K19 P17:P19 F26:F35 K26:K35 P26:P35 F40:F41 K40:K41 P40:P41 F47 K47 P47 F53:F54 K53:K54 P53:P54 F60 K60 P60"}`
- [P47] **cell value equal** `"Budget"` → fontColor `F9AB10` — on E5 J5 O5
  - json: `{"dxf": {"fontColor": "F9AB10"}, "formulas": ["\"Budget\""], "kind": "cellIs", "op": "equal", "priority": 47, "ranges": "E5 J5 O5"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
