# Spec: bs-dr-sc-style → sheet "YoY"

> Source: Balance Sheet - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:P56`; Everything beyond it is hidden (columns after P, rows after 56). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:Q79 |
| Merged ranges | none |
| Defined name `DR_DATE_PICKER` | `46022` |
| Defined name `DR_FY_START` | `1` |
| Defined name `Value` | `"widget_19324_0_tt_1774777138118.73"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 48.57 | 258.8 |  |
| C | 16.57 | 90.8 |  |
| D | 4.57 | 27.8 |  |
| E:F | 16.57 | 90.8 |  |
| G | 16.57 | 90.8 |  |
| H | 4.57 | 27.8 |  |
| I | 16.57 | 90.8 |  |
| J:Q | 8.71 | 49.5 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S2 | Poppins | 24.0 | B | F7F7F7 | – | – | `–` | left | top | – | – |
| S3 | Poppins | 11.0 |  | F7F7F7 | – | – | `–` | – | – | – | – |
| S4 | Poppins | 11.0 | B | F7F7F7 | – | – | `–` | – | – | – | – |
| S5 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S6 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S7 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S8 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S9 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S10 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S11 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S13 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S14 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S15 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S16 | Poppins | 14.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S17 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S18 | Poppins | 12.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S19 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S20 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S21 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S22 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S23 | Poppins | 8.0 |  | 3F3F3F | – | L:thin:9EA1AA,R:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S24 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S26 | Poppins | 12.0 |  | F7F7F7 | – | L:thin:9EA1AA | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S27 | Poppins | 11.0 |  | 3F3F3F | – | – | `–` | – | – | – | – |
| S28 | Poppins | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | – | – | – |
| S29 | Poppins | 8.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S30 | Poppins | 11.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S31 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S32 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S33 | Poppins | 8.0 |  | 4D6ECD | – | – | `#,##0,\ "K"` | center | center | – | – |
| S34 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S35 | Poppins | 10.0 | I | 001F37 | – | – | `–` | left | center | 1.0 | – |
| S36 | Poppins | 8.0 |  | 001F37 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S37 | Poppins | 8.0 |  | 001F37 | – | – | `0%` | center | center | – | – |
| S38 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S39 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S40 | Poppins | 8.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S41 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S42 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S43 | Poppins | 8.0 |  | 253D84 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S44 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S45 | Poppins | 10.0 | B | F7F7F7 | – | – | `–` | left | center | – | – |
| S46 | Poppins | 8.0 | B | F7F7F7 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S47 | Poppins | 8.0 | B | F7F7F7 | – | – | `0%` | center | center | – | – |
| S48 | Poppins | 9.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S49 | Poppins | 12.0 |  | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S50 | Poppins | 12.0 | B | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S51 | Poppins | 10.0 | B | 3F3F3F | – | – | `–` | left | center | – | – |
| S52 | Poppins | 10.0 |  | 3F3F3F | – | – | `#,##0,\ "K"` | right | center | – | – |
| S53 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S54 | Poppins | 9.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T2** h=24.0 rows 2: A:B=S1 C=S6 D=S1 E:G=S7 H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T3** h=8.25 rows 3: A:H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T4** h=24.0 rows 4: A=S1 B=S8 C=S9 D=S1 E=S9 F:H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T5** h=24.0 rows 5: A=S1 B=S10 C:G=S11 H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T6** h=16.0 rows 6: A:H=S1 I=S2 J:L=S3 M=S4 N:P=S5
- **T7** h=24.0 rows 7: A:G=S2 H:I=S12 J:L=S3 M=S4 N:P=S5
- **T8** h=24.0 rows 8: A=S5 B=S13 C:G=S14 H=S12 I=S15 J:P=S5
- **T9** h=24.0 rows 9: A=S5 B:G=S16 H=S12 I=S15 J:P=S5
- **T10** h=24.0 rows 10: A=S5 B=S17 C:G=S18 H=S12 I=S15 J:P=S5
- **T11** h=24.0 rows 11: A=S5 B:C=S19 D=S15 E:G=S19 H=S12 I=S15 J:P=S5
- **T12** h=24.0 rows 12: A=S20 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I=S27 J:P=S5
- **T13** h=24.0 rows 13-15,23,39,47,50-51: A=S28 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I=S27 J:P=S5
- **T14** h=24.0 rows 16,21-22,24: A=S29 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I=S27 J:P=S5
- **T15** h=24.0 rows 17,25,35: A=S30 B=S31 C=S32 D=S33 E:F=S32 G=S34 H=S12 I=S27 J:P=S5
- **T16** h=24.0 rows 18,36: A=S30 B=S35 C:F=S36 G=S37 H=S12 I=S27 J:P=S5
- **T17** h=24.0 rows 19: A=S5 B=S17 C:G=S38 H=S12 I=S15 J:P=S5
- **T18** h=24.0 rows 20: A=S5 B:C=S39 D=S5 E:G=S39 H=S12 I=S15 J:P=S5
- **T19** h=24.0 rows 26,43: A=S40 B=S41 C=S42 D=S43 E:F=S42 G=S44 H=S12 I=S27 J:P=S5
- **T20** h=24.0 rows 27: A=S30 B=S45 C:F=S46 G=S47 H=S12 I=S27 J:P=S5
- **T21** h=24.0 rows 28: A=S48 B=S13 C:G=S14 H=S12 I=S27 J:P=S5
- **T22** h=24.0 rows 29: A=S5 B:G=S16 H=S12 I=S27 J:P=S5
- **T23** h=24.0 rows 30: A=S5 B=S17 C:G=S18 H=S12 I=S27 J:P=S5
- **T24** h=24.0 rows 31: A=S5 B=S49 C=S50 D=S41 E:G=S50 H=S12 I:P=S15
- **T25** h=24.0 rows 32-34,48-49: A=S20 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I:P=S15
- **T26** h=24.0 rows 37: A=S30 B=S17 C:G=S38 H=S12 I=S27 J:P=S5
- **T27** h=24.0 rows 38: A=S30 B:C=S39 D=S15 E:G=S39 H=S12 I=S27 J:P=S5
- **T28** h=24.0 rows 40-41: A=S20 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I=S15 J:P=S5
- **T29** h=24.0 rows 42: A=S40 B=S31 C=S32 D=S33 E:F=S32 G=S34 H=S12 I=S27 J:P=S5
- **T30** h=24.0 rows 44: A=S5 B=S51 C:E=S52 F=S46 G=S47 H=S12 I=S27 J:P=S5
- **T31** h=24.0 rows 45: A=S40 B=S13 C:G=S14 H=S12 I=S27 J:P=S5
- **T32** h=24.0 rows 46: A=S30 B:C=S53 D=S16 E:G=S53 H=S12 I=S27 J:P=S5
- **T33** h=24.0 rows 52: A=S54 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I=S27 J:P=S5
- **T34** h=24.0 rows 53: A=S20 B=S21 C=S22 D=S23 E=S22 F=S24 G=S25 H=S26 I:P=S5
- **T35** h=24.0 rows 54: A=S48 B=S31 C=S32 D=S33 E:F=S32 G=S34 H=S12 I=S27 J:P=S5
- **T36** h=24.0 rows 55-56: A=S5 B=S41 C=S42 D=S43 E:F=S42 G=S44 H=S12 I:P=S5

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r4: {"B": "Balance Sheet - YoY"}
- r5: {"C": "Actuals", "E": "Actuals", "F": "∆ vs PY", "G": "% ∆ vs PY"}
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

- **F1** at C2 (example `C2`): `=YEAR(EOMONTH(DR_DATE_PICKER,0))+IF(AND(MONTH(EOMONTH(DR_DATE_PICKER,0))>=DR_FY_START,DR_FY_START>=7),1,IF(AND(MONTH(EOMONTH(DR_DATE_PICKER,0))<DR_FY_START,DR_FY_START<=6),-1,0))`
- **F2** at E2 (example `E2`): `=C2-1`
- **F3** at C4 (example `C4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F4** at E4 (example `E4`): `=EOMONTH(C4,-12)`
- **F5** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F6** at C12:C16, E12:E16 (example `C12`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Assets","[Report_Field]",$B12,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F7** at F12:F17, F21:F26, F32:F34, F39:F43, F47:F54, F56 (example `F12`): `=IFERROR(C12-E12,"NA")`
- **F8** at G12:G17, G21:G26, G32:G34, G39:G43, G47:G55 (example `G12`): `=IFERROR(C12/E12-1,"NA")`
- **F9** at C17, E17 (example `C17`): `=SUM(C12:C16)`
- **F10** at C21:C24, E21:E24 (example `C21`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Non Current Assets","[Report_Field]",$B21,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F11** at C25, E25 (example `C25`): `=SUM(C21:C24)`
- **F12** at C26, E26 (example `C26`): `=C25+C17`
- **F13** at C32:C34, E32:E34 (example `C32`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Liabilities","[Report_Field]",$B32,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F14** at C35, E35:G35, C42, E42 (example `C35`): `=SUM(C32:C34)`
- **F15** at C39:C41, E39:E41 (example `C39`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B39,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F16** at C43, E43 (example `C43`): `=C35+C42`
- **F17** at C47:C53, E47:E53 (example `C47`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Equity","[Report_Field]",$B47,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F18** at C54, E54 (example `C54`): `=SUM(C47:C53)`
- **F19** at C55, E55:F55 (example `C55`): `=C54+C43`
- **F20** at C56, E56 (example `C56`): `=+C26-C55`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P2] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on F12:F16 F21:F24 F32:F34 F39:F41 F47:F53
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 2, "ranges": "F12:F16 F21:F24 F32:F34 F39:F41 F47:F53"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
