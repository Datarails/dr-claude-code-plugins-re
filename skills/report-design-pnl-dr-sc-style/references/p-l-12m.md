# Spec: pnl-dr-sc-style → sheet "P&L 12M"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:Q62`; Everything beyond it is hidden (columns after Q, rows after 62). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:XFD68 |
| Merged ranges | D2:P2 |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 56.57 | 300.8 |  |
| C | 4.57 | 27.8 |  |
| D:E | 16.57 | 90.8 |  |
| F:Q | 16.57 | 90.8 |  |
| R | 16.86 | 92.2 | HIDDEN |

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
| S9 | Poppins | 12.0 |  | FFFFFF | 0C142B | – | `–` | right | center | 1.0 | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S12 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S13 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S14 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S15 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S16 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S17 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | center | – | – |
| S18 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S19 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S20 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S21 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S22 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S23 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S24 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S25 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S26 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S27 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S28 | Poppins | 12.0 | B | 333333 | – | L:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S29 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S30 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S31 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S32 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S33 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S34 | Poppins | 12.0 | B | 333333 | – | – | `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |
| S35 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S36 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S37 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S38 | Poppins | 14.0 | B | 0C142B | – | – | `–` | left | center | 1.0 | – |
| S39 | Poppins | 12.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S40 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S41 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S42 | Poppins | 12.0 | B | 333333 | – | – | `0.0%` | right | center | 1.0 | – |
| S43 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S44 | Poppins | 4.0 |  | F0F1F4 | – | R:thin:9EA1AA | `0` | – | – | – | – |
| S45 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S46 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S47 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S48 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S49 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S50 | Poppins | 12.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S51 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S52 | Calibri | 11.0 |  | 001F37 | – | T:thin:9EA1AA | `–` | – | – | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:Q=S3
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:P=S4 Q=S3
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S5 G:O=S1 P:Q=S3
- **T4** h=24.0 rows 4: A=S1 B=S6 C=S2 D:P=S7 Q=S3
- **T5** h=24.0 rows 5: A=S1 B=S8 C=S2 D:P=S9 Q=S10
- **T6** h=15.95 rows 6: A=S1 B=S11 C:E=S2 F=S5 G:H=S1 I=S12 J:O=S1 P=S3 Q=S13
- **T7** h=24.0 rows 7: A:B=S14 C:D=S15 E=S16 F:Q=S14
- **T8** h=24.0 rows 8: A=S17 B:P=S18 Q=S19
- **T9** h=24.0 rows 9: A=S14 B:G=S20 H=S21 I:L=S20 M=S21 N:O=S20 P=S22 Q=S23
- **T10** h=24.0 rows 10-12,47,54,60: A=S24 B=S25 C=S26 D:O=S27 P=S28 Q=S14
- **T11** h=24.0 rows 13: A=S29 B:C=S30 D:O=S31 P=S32 Q=S14
- **T12** h=24.0 rows 14: A=S29 B=S33 C:G=S34 H=S14 I:L=S34 M=S14 N:P=S34 Q=S14
- **T13** h=24.0 rows 15: A=S14 B=S18 C:P=S35 Q=S19
- **T14** h=24.0 rows 16: A=S14 B:G=S36 H=S37 I:L=S36 M=S37 N:O=S36 P=S38 Q=S14
- **T15** h=24.0 rows 17: A=S39 B=S25 C=S40 D:O=S27 P=S28 Q=S14
- **T16** h=24.0 rows 18-19: A=S24 B=S25 C=S40 D:O=S27 P=S28 Q=S14
- **T17** h=24.0 rows 20: A=S41 B:C=S30 D:O=S31 P=S32 Q=S14
- **T18** h=24.0 rows 21: A=S41 B:C=S33 D:P=S32 Q=S14
- **T19** h=24.0 rows 22: A=S41 B:C=S33 D:O=S42 P=S43 Q=S14
- **T20** h=24.0 rows 23: A=S41 B:Q=S14
- **T21** h=24.0 rows 24,58: A=S29 B=S18 C:P=S35 Q=S14
- **T22** h=24.0 rows 25: A=S29 B:G=S36 H=S37 I:L=S36 M=S37 N:O=S36 P=S38 Q=S14
- **T23** h=24.0 rows 26-27,29: A=S44 B=S45 C=S40 D:O=S27 P=S28 Q=S14
- **T24** h=24.0 rows 28: A=S44 B=S45 C=S40 D:O=S27 P=S28 Q=S19
- **T25** h=24.0 rows 30-35: A=S46 B=S45 C=S40 D:O=S27 P=S28 Q=S14
- **T26** h=24.0 rows 36,42: A=S47 B:C=S48 D:O=S49 P=S32 Q=S14
- **T27** h=24.0 rows 37,44: A=S47 B:Q=S14
- **T28** h=24.0 rows 38,45: A=S47 B=S18 C:P=S35 Q=S14
- **T29** h=24.0 rows 39: A=S47 B:G=S20 H=S37 I:L=S20 M=S37 N:O=S20 P=S22 Q=S14
- **T30** h=24.0 rows 40-41: A=S46 B=S25 C=S26 D:O=S27 P=S28 Q=S14
- **T31** h=24.0 rows 43: A=S47 B:C=S50 D:P=S42 Q=S14
- **T32** h=None rows 46: A=S14 B:O=S37 P:Q=S14
- **T33** h=24.0 rows 48,55: A=S14 B:C=S48 D:O=S49 P=S32 Q=S19
- **T34** h=24.0 rows 49,56: A=S14 B:C=S50 D:P=S42 Q=S14
- **T35** h=None rows 50,57: A:Q=S14
- **T36** h=24.0 rows 51: A=S14 B=S18 C:P=S35 Q=S14
- **T37** h=24.0 rows 52,59: A=S29 B:O=S37 P:Q=S14
- **T38** h=24.0 rows 53: A=S44 B=S25 C=S26 D:O=S27 P=S28 Q=S14
- **T39** h=24.0 rows 61: A=S14 B=S51 C=S52 D:O=S49 P=S32 Q=S19
- **T40** h=24.0 rows 62: A=S14 B:C=S50 D:P=S43 Q=S14

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": "Monthly View"}
- r4: {"B": "P&L - Rolling 12M", "P": "Total"}
- r5: {"P": "Actuals"}
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
- r24: {"B": "Operating Expenses ex D&A"}
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
- r53: {"B": "Interest Expense"}
- r54: {"B": "Interest Income"}
- r55: {"B": "EBT"}
- r56: {"B": "EBT %"}
- r58: {"B": "Taxes"}
- r60: {"B": "Tax"}
- r61: {"B": "Net Profit"}
- r62: {"B": "Net Margin %"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D4:N4 (example `D4`): `=EOMONTH(E4,-1)`
- **F2** at O4 (example `O4`): `=B5`
- **F3** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F4** at D5:O5 (example `D5`): `=IF(D4<=DR_DATE_PICKER,"Actuals","Forecast")`
- **F5** at D10:O12 (example `D10`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B10,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Income")`
- **F6** at P10:P12, P17:P19, P26:P35, P40:P41, P47, P53:P54, P60:P61 (example `P10`): `=IFERROR(SUM(D10:O10),"NA")`
- **F7** at D13:P13, D20:P20 (example `D13`): `=IFERROR(SUM(D10:D12),"NA")`
- **F8** at D17:O19 (example `D17`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B17,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Cost of Goods Sold")`
- **F9** at D21:P21 (example `D21`): `=IFERROR(D13-D20,"NA")`
- **F10** at D22:P22 (example `D22`): `=IFERROR(D21/D13,"NA")`
- **F11** at D26:O35 (example `D26`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B26,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Operating Expense")`
- **F12** at D36:P36 (example `D36`): `=IFERROR(SUM(D26:D35),"NA")`
- **F13** at D40:O41, D60:O60 (example `D40`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Report_Field]",$B40)`
- **F14** at D42:P42 (example `D42`): `=IFERROR(D21-D36+D40-D41,"NA")`
- **F15** at D43:P43 (example `D43`): `=IFERROR(D42/D13,"NA")`
- **F16** at D47:O47, D53:O54 (example `D47`): `=_xldudf_DR_GET(Value,"[Reporting Month]",D$4,"[Scenario]",D$5,"[DR_KPI]",$B47)`
- **F17** at D48:P48 (example `D48`): `=IFERROR(D42-D47,"NA")`
- **F18** at D49:P49 (example `D49`): `=IFERROR(D48/D13,"NA")`
- **F19** at D55:P55 (example `D55`): `=IFERROR(D48+D53-D54,"NA")`
- **F20** at D56:P56 (example `D56`): `=IFERROR(D55/D13,"NA")`
- **F21** at D61:O61 (example `D61`): `=D55-D60`
- **F22** at D62:P62 (example `D62`): `=IFERROR(D61/D13,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
