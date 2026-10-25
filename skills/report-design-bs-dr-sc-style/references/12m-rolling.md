# Spec: bs-dr-sc-style → sheet "12M rolling"

> Source: Balance Sheet - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:O56`; Everything beyond it is hidden (columns after O, rows after 56). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 0 pt (unlisted rows HIDDEN (zeroHeight)) |
| Used range | A1:XFB62 |
| Merged ranges | none |
| Defined name `DR_DATE_PICKER` | `46022` |
| Defined name `Value` | `"widget_19324_0_tt_1774777138118.73"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 40.57 | 216.8 |  |
| C:L | 16.57 | 90.8 |  |
| M:N | 14.57 | 80.2 |  |
| O | 4.57 | 27.8 |  |
| P | 9.14 | 51.8 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S2 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S3 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S4 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S5 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S6 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S7 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S8 | Poppins | 11.0 |  | F7F7F7 | – | – | `–` | – | – | – | – |
| S9 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | center | top | – | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S11 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S12 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S13 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S14 | Poppins | 14.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S15 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S16 | Poppins | 12.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S17 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S18 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S19 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S20 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S21 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S22 | Poppins | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | – | – | – |
| S23 | Poppins | 8.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S24 | Poppins | 11.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S25 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S26 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S27 | Poppins | 10.0 | I | 001F37 | – | – | `–` | left | center | 1.0 | – |
| S28 | Poppins | 8.0 |  | 001F37 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S29 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S30 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S31 | Poppins | 8.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S32 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S33 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S34 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | wrap |
| S35 | Poppins | 9.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S36 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S37 | Poppins | 10.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | left | center | – | – |
| S38 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S39 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S40 | Poppins | 12.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S41 | Poppins | 12.0 | B | 626364 | – | – | `@` | left | center | 1.0 | – |
| S42 | Poppins | 12.0 | B | 626364 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S43 | Poppins | 14.0 | B | 0C142B | – | – | `–` | left | center | 1.0 | – |
| S44 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S45 | Poppins | 9.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:O=S1
- **T2** h=24.0 rows 2: A:B=S1 C:N=S2 O=S1
- **T3** h=8.25 rows 3: A:O=S1
- **T4** h=24.0 rows 4: A=S1 B=S3 C:N=S4 O=S1
- **T5** h=24.0 rows 5: A=S1 B=S5 C:N=S6 O=S1
- **T6** h=16.0 rows 6: A:O=S1
- **T7** h=24.0 rows 7: A=S7 B=S8 C=S7 D:F=S9 G:O=S10
- **T8** h=24.0 rows 8: A=S7 B=S11 C:N=S12 O=S13
- **T9** h=24.0 rows 9: A=S7 B:I=S14 J:O=S13
- **T10** h=24.0 rows 10: A=S7 B=S15 C:N=S16 O=S13
- **T11** h=24.0 rows 11: A=S7 B:N=S17 O=S13
- **T12** h=24.0 rows 12,39-41,49: A=S18 B=S19 C:N=S20 O=S21
- **T13** h=24.0 rows 13-15,48,52: A=S22 B=S19 C:N=S20 O=S21
- **T14** h=24.0 rows 16,21-24,47: A=S23 B=S19 C:N=S20 O=S21
- **T15** h=24.0 rows 17,25: A=S24 B=S25 C:N=S26 O=S7
- **T16** h=24.0 rows 18: A=S24 B=S27 C:N=S28 O=S7
- **T17** h=24.0 rows 19: A=S7 B=S15 C:N=S29 O=S7
- **T18** h=24.0 rows 20: A=S7 B:N=S30 O=S7
- **T19** h=24.0 rows 26,55: A=S31 B=S32 C:N=S33 O=S7
- **T20** h=24.0 rows 27: A=S24 B=S13 C=S34 D:N=S13 O=S7
- **T21** h=24.0 rows 28: A=S35 B=S11 C:N=S12 O=S7
- **T22** h=24.0 rows 29: A=S7 B:I=S14 J:N=S13 O=S7
- **T23** h=24.0 rows 30: A=S36 B=S15 C:N=S16 O=S7
- **T24** h=24.0 rows 31: A=S7 B=S37 C:I=S38 J:N=S39 O=S13
- **T25** h=24.0 rows 32-34,50-51: A=S18 B=S19 C:N=S20 O=S40
- **T26** h=24.0 rows 35: A=S24 B=S25 C:N=S26 O=S13
- **T27** h=24.0 rows 36: A=S31 B=S41 C=S42 D:N=S43 O=S7
- **T28** h=24.0 rows 37: A=S24 B=S15 C:N=S29 O=S7
- **T29** h=24.0 rows 38: A=S36 B:N=S44 O=S7
- **T30** h=24.0 rows 42: A=S7 B=S25 C:N=S26 O=S7
- **T31** h=24.0 rows 43: A=S7 B=S32 C:N=S33 O=S7
- **T32** h=24.0 rows 44: A:B=S7 C=S34 D:O=S7
- **T33** h=24.0 rows 45: A=S31 B=S11 C:N=S12 O=S13
- **T34** h=24.0 rows 46: A=S7 B:I=S38 J:N=S39 O=S13
- **T35** h=24.0 rows 53: A=S45 B=S19 C:N=S20 O=S21
- **T36** h=24.0 rows 54: A=S31 B=S25 C:N=S26 O=S7
- **T37** h=24.0 rows 56: A=S24 B=S32 C:N=S33 O=S7

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"C": "Monthly View"}
- r4: {"B": "BS - Rolling 12M"}
- r5: {"C": "Actuals", "D": "Actuals", "E": "Actuals", "F": "Actuals", "G": "Actuals", "H": "Actuals", "I": "Actuals", "J": "Actuals", "K": "Actuals", "L": "Actuals", "M": "Actuals", "N": "Actuals"}
- r8: {"B": "Assets"}
- r10: {"B": "Current Assets"}
- r12: {"B": "Cash & Cash Equivalents"}
- r13: {"B": "Short Term Investments"}
- r14: {"B": "Accounts Receivable"}
- r15: {"B": "Other Current Asset"}
- r16: {"B": "Prepayments"}
- r17: {"B": "Total Current Assets"}
- r19: {"B": "Non Current Assets"}
- r21: {"B": "Intercompany receivable"}
- r22: {"B": "Long Term Investments"}
- r23: {"B": "Net Fixed Assets"}
- r24: {"B": "Net Intangible Assets"}
- r25: {"B": "Total Non Current Assets"}
- r26: {"B": "Total Assets"}
- r28: {"B": "Liabilities"}
- r30: {"B": "Current Liabilities "}
- r32: {"B": "Accounts Payable"}
- r33: {"B": "Deferred Revenue"}
- r34: {"B": "Other Current Liability"}
- r35: {"B": "Total Current Liabilities"}
- r37: {"B": "Long Term Liabilites"}
- r39: {"B": "Bank Loan"}
- r40: {"B": "Intercompany payables"}
- r41: {"B": "Long Term Liability"}
- r42: {"B": "Total Long Term Liabilities"}
- r43: {"B": "Total Liabilities"}
- r45: {"B": "Shareholders' Equity"}
- r47: {"B": "Non-Controlling Interest"}
- r48: {"B": "Non-Controlling Interest Income"}
- r49: {"B": "Ordinary Shares"}
- r50: {"B": "Other Equity"}
- r51: {"B": "Equity"}
- r52: {"B": "Net Income Calc"}
- r53: {"B": "Retained Earnings"}
- r54: {"B": "Total Equity"}
- r55: {"B": "Total Equity & Liabilities "}
- r56: {"B": "Validation"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at C4:M4 (example `C4`): `=EOMONTH(D4,-1)`
- **F2** at N4 (example `N4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F3** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F4** at C12:N16 (example `C12`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Assets","[Report_Field]",$B12,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F5** at C17:N17 (example `C17`): `=SUM(C12:C16)`
- **F6** at C21:N24 (example `C21`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Non Current Assets","[Report_Field]",$B21,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F7** at C25:N25 (example `C25`): `=SUM(C21:C24)`
- **F8** at C26:N26 (example `C26`): `=C25+C17`
- **F9** at C32:N34 (example `C32`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Liabilities","[Report_Field]",$B32,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F10** at C35:N35, C42:N42 (example `C35`): `=SUM(C32:C34)`
- **F11** at C39:N41 (example `C39`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B39,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F12** at C43:N43 (example `C43`): `=C42+C35`
- **F13** at C47:N53 (example `C47`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Equity","[Report_Field]",$B47,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F14** at C54:N54 (example `C54`): `=SUM(C47:C53)`
- **F15** at C55:N55 (example `C55`): `=C54+C43`
- **F16** at C56:N56 (example `C56`): `=+C26-C55`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
