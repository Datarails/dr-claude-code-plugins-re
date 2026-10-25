# Spec: cf-dr-sc-style → sheet "Cash Flow - YoY"

> Source: Cash Flow - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:T55`; Everything beyond it is hidden (columns after T, rows after 55). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 13.9 pt (unlisted rows HIDDEN (zeroHeight)) |
| Used range | A1:U77 |
| Merged ranges | none |
| Defined name `DR_DATE_PICKER` | `45747` |
| Defined name `DR_FY_START` | `1` |
| Defined name `Value` | `"widget_19324_0_tt_1773235212"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 40.57 | 216.8 |  |
| C | 4.57 | 27.8 |  |
| D | 4.57 | 27.8 |  |
| E | 4.57 | 27.8 |  |
| F:I | 16.57 | 90.8 |  |
| J | 4.57 | 27.8 |  |
| K:N | 16.57 | 90.8 |  |
| O | 4.57 | 27.8 |  |
| P:S | 16.57 | 90.8 |  |
| T | 16.57 | 90.8 |  |
| U | 16.57 | 90.8 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 10.0 | B | 7FFFD4 | 0C142B | – | `–` | – | – | – | – |
| S2 | Calibri | 10.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S3 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | center | – | – |
| S4 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | left | center | – | – |
| S5 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S6 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S7 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S8 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S9 | Poppins | 11.0 |  | F2F2F2 | – | – | `[$-409]yyyy\ mmmm;@` | left | – | – | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]yyyy\ mmmm;@` | – | center | – | – |
| S11 | Poppins | 11.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]yyyy\ mmmm;@` | centerContinuous | top | – | – |
| S13 | Calibri | 10.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S14 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S15 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S16 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S17 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S18 | Poppins | 10.0 | B | 001F37 | – | – | `#,##0` | center | center | – | – |
| S19 | Poppins | 10.0 | B | 001F37 | – | B:thin:9EA1AA | `#,##0` | center | center | – | – |
| S20 | Poppins | 10.0 | B | 001F37 | – | B:thin:9EA1AA | `0.0%` | center | center | – | – |
| S21 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S22 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S23 | Poppins | 9.0 |  | 253D84 | – | L:thin:9EA1AA | `–` | center | center | – | – |
| S24 | Poppins | 10.0 |  | 333333 | – | – | `–` | center | center | – | – |
| S25 | Poppins | 9.0 |  | 253D84 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S26 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S27 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S28 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S29 | Poppins | 14.0 |  | 253D84 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | center | center | – | – |
| S30 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S31 | Poppins | 10.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | center | – | – | – |
| S32 | Poppins | 10.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | – | – | – |
| S33 | Poppins | 14.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | center | center | – | – |
| S34 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S35 | Poppins | 8.0 |  | 4D6ECD | – | – | `–` | center | center | – | – |
| S36 | Poppins | 10.0 | B | 000090 | – | – | `–` | center | center | – | – |
| S37 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S38 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S39 | Poppins | 12.0 | B | 626364 | – | – | `@` | left | center | 1.0 | – |
| S40 | Poppins | 12.0 | B | 626364 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S41 | Poppins | 12.0 | B | 626364 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S42 | Poppins | 10.0 | B | 000090 | – | B:thin:9EA1AA | `–` | center | center | – | – |
| S43 | Poppins | 10.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S44 | Poppins | 10.0 | B | 000090 | – | B:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S45 | Poppins | 10.0 | B | 000090 | – | B:thin:9EA1AA | `0.0%;\(0.0%\)` | center | center | – | – |
| S46 | Poppins | 14.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S47 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S48 | Poppins | 9.0 |  | 253D84 | – | – | `–` | center | center | – | – |
| S49 | Poppins | 9.0 |  | 253D84 | – | – | `–` | left | center | 1.0 | – |
| S50 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S51 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S52 | Poppins | 14.0 |  | 253D84 | – | – | `–` | center | center | – | – |
| S53 | Poppins | 10.0 | I | 7F7F7F | – | B:thin:9EA1AA | `–` | center | center | – | – |
| S54 | Poppins | 10.0 | I | 7F7F7F | – | – | `–` | center | center | – | – |
| S55 | Poppins | 10.0 |  | 7F7F7F | – | B:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S56 | Poppins | 10.0 |  | 7F7F7F | – | B:thin:9EA1AA | `0.0%;\(0.0%\)` | center | center | – | – |
| S57 | Poppins | 8.0 |  | 7F7F7F | – | – | `–` | center | center | – | – |
| S58 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S59 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S60 | Poppins | 9.0 |  | 4D6ECD | – | T:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S61 | Poppins | 9.0 |  | 4D6ECD | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | center | center | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A=S1 B:T=S2
- **T2** h=24.0 rows 2: A:E=S2 F:I=S3 J=S2 K:N=S3 O=S2 P:S=S3 T=S2
- **T3** h=8.25 rows 3: A:T=S2
- **T4** h=24.0 rows 4: A=S2 B=S4 C:E=S2 F:S=S5 T=S2
- **T5** h=24.0 rows 5: A=S2 B=S6 C:E=S2 F:S=S7 T=S2
- **T6** h=16.0 rows 6: A:T=S2
- **T7** h=24.0 rows 7: A=S8 B=S9 C=S10 D=S11 E=S10 F=S8 G:I=S12 J=S13 K:N=S14 O=S13 P=S14 Q:T=S8
- **T8** h=24.0 rows 8,21,34,50: A=S8 B=S15 C:S=S16 T=S8
- **T9** h=24.0 rows 9: A=S8 B=S17 C:E=S18 F:G=S19 H=S20 I=S19 J=S18 K:L=S19 M=S20 N=S19 O=S18 P=S19 Q=S20 R:S=S17 T=S8
- **T10** h=24.0 rows 10: A=S21 B=S22 C=S23 D=S24 E=S25 F:G=S26 H=S27 I=S28 J=S29 K:L=S26 M=S27 N=S28 O=S29 P:Q=S26 R=S27 S=S28 T=S30
- **T11** h=24.0 rows 11-18,23-30,36-46: A=S21 B=S22 C=S31 D=S24 E=S32 F:G=S26 H=S27 I=S28 J=S33 K:L=S26 M=S27 N=S28 O=S33 P:Q=S26 R=S27 S=S28 T=S30
- **T12** h=24.0 rows 19: A=S8 B=S34 C=S35 D=S36 E=S35 F:H=S37 I=S38 J=S35 K:M=S37 N=S38 O=S35 P:R=S37 S=S38 T=S8
- **T13** h=24.0 rows 20: A=S8 B=S39 C=S35 D=S36 E=S35 F:H=S40 I=S41 J=S35 K:M=S40 N=S41 O=S35 P:R=S40 S=S41 T=S8
- **T14** h=24.0 rows 22: A=S8 B=S42 C=S43 D=S36 E=S43 F:H=S44 I=S45 J=S46 K:M=S44 N=S45 O=S46 P:R=S44 S=S45 T=S8
- **T15** h=24.0 rows 31: A=S8 B=S34 C:E=S35 F:H=S37 I=S38 J=S35 K:M=S37 N=S38 O=S35 P:R=S37 S=S38 T=S8
- **T16** h=24.0 rows 32-33,48-49: A=S8 B=S47 C=S48 D=S49 E=S48 F:H=S50 I=S51 J=S52 K:M=S50 N=S51 O=S52 P:R=S50 S=S51 T=S8
- **T17** h=24.0 rows 35,51: A=S8 B=S53 C=S43 D=S54 E=S43 F:H=S55 I=S56 J=S46 K:M=S55 N=S56 O=S46 P:R=S55 S=S56 T=S8
- **T18** h=24.0 rows 47: A=S8 B=S34 C=S48 D=S49 E=S48 F:H=S37 I=S38 J=S52 K:M=S37 N=S38 O=S52 P:R=S37 S=S38 T=S8
- **T19** h=24.0 rows 52-54: A=S21 B=S22 C=S31 D=S57 E=S32 F:G=S26 H=S27 I=S28 J=S33 K:L=S26 M=S27 N=S28 O=S33 P:Q=S26 R=S27 S=S28 T=S30
- **T20** h=24.0 rows 55: A=S8 B=S58 C=S48 D=S49 E=S48 F:G=S59 H=S60 I=S61 J=S52 K:L=S59 M=S60 N=S61 O=S52 P:Q=S59 R=S60 S=S61 T=S8

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"F": "MTD", "K": "QTD", "P": "YTD"}
- r4: {"B": "Cash Flow -  YoY"}
- r5: {"F": "Actuals", "G": "Actuals", "H": "∆ vs PY", "I": "% ∆ vs PY", "K": "Actuals", "L": "Actuals", "M": "∆ vs PY", "N": "% ∆ vs PY", "P": "Actuals", "Q": "Actuals", "R": "∆ vs PY", "S": "% ∆ vs PY"}
- r8: {"B": "CF from Operating Activity"}
- r10: {"B": "Net Income"}
- r11: {"B": "Depreciation & Amortization"}
- r12: {"B": "Cash & Cash Equivalents"}
- r13: {"B": "Accounts Receivable"}
- r14: {"B": "Other Current Asset"}
- r15: {"B": "Prepayments"}
- r16: {"B": "Accounts Payable"}
- r17: {"B": "Deferred Revenue"}
- r18: {"B": "Other Current Liability"}
- r19: {"B": "Total Operating Activity"}
- r21: {"B": "CF from Investing Activity"}
- r23: {"B": "Fixed Asset"}
- r24: {"B": "Accumulated Depreciation"}
- r25: {"B": "Gross Fixed Assets"}
- r26: {"B": "Intangible Assets"}
- r27: {"B": "Intercompany receivable"}
- r28: {"B": "Long Term Investments"}
- r29: {"B": "Net Fixed Assets"}
- r30: {"B": "Net Intangible Assets"}
- r31: {"B": "Total Investing Activity"}
- r32: {"B": "Free Cash Flow"}
- r34: {"B": "CF from Financing Activity"}
- r36: {"B": "Bank Loan"}
- r37: {"B": "Intercompany payables"}
- r38: {"B": "Long Term Liability"}
- r39: {"B": "Ordinary Shares"}
- r40: {"B": "Other Equity"}
- r41: {"B": "Non-Controlling Interest"}
- r42: {"B": "Ordinary Shares"}
- r43: {"B": "Other Equity"}
- r44: {"B": "Equity"}
- r45: {"B": "Net Income Calc"}
- r46: {"B": "Retained Earnings"}
- r47: {"B": "Total Financing Activity"}
- r48: {"B": "Total Cash Flow"}
- r50: {"B": "Summary"}
- r52: {"B": "Cash - beginning of period"}
- r53: {"B": "Cash - ending of period"}
- r54: {"B": "Cash PoP Change"}
- r55: {"B": "Gap", "F": 0, "G": 0, "K": 0, "L": 0, "P": 0, "Q": 0}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at F4 (example `F4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at G4, L4, Q4 (example `G4`): `=EOMONTH(F4,-12)`
- **F3** at K4 (example `K4`): `=F4`
- **F4** at P4 (example `P4`): `=F4`
- **F5** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F6** at F10:G10 (example `F10`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L1]","REVENUE")-_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L1]","EXPENSE")`
- **F7** at H10:H19, M10:M19, R10:R19, H23:H32, M23:M32, R23:R32, H36:H46, M36:M48, R36:R46, H48, R48, H52:H54, M52:M54, R52:R54 (example `H10`): `=IFERROR(F10-G10,"NA")`
- **F8** at I10:I19, N10:N19, S10:S19, I23:I32, N23:N32, S23:S32, I36:I48, N36:N48, S36:S48, I52:I54, N52:N54, S52:S54 (example `I10`): `=IFERROR(F10/G10-1,"NA")`
- **F9** at K10:L10 (example `K10`): `=_xldudf_DR_QTD(Value,"[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L1]","REVENUE")-_xldudf_DR_QTD(Value,"[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L1]","EXPENSE")`
- **F10** at P10:Q10 (example `P10`): `=_xldudf_DR_YTD(Value,"[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L1]","REVENUE")-_xldudf_DR_YTD(Value,"[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L1]","EXPENSE")`
- **F11** at D11, D16:D18, D36:D46 (example `D11`): `="( + )"`
- **F12** at F11:G11 (example `F11`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]",$B11)`
- **F13** at K11:L11 (example `K11`): `=_xldudf_DR_QTD(Value,"[Scenario]",K$5,"[Reporting Month]",K$4,"[DR_KPI]",$B11)`
- **F14** at P11:Q11 (example `P11`): `=_xldudf_DR_YTD(Value,"[Scenario]",P$5,"[Reporting Month]",P$4,"[DR_KPI]",$B11)`
- **F15** at D12:D15, D23:D30 (example `D12`): `="( - )"`
- **F16** at F12:G15 (example `F12`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Current Assets","[Report_Field]",$B12)`
- **F17** at K12:L15 (example `K12`): `=-_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Current Assets","[Report_Field]",$B12)`
- **F18** at P12:Q15 (example `P12`): `=-_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Current Assets","[Report_Field]",$B12)`
- **F19** at F16:G18 (example `F16`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Current Liabilities","[Report_Field]",$B16)`
- **F20** at K16:L18 (example `K16`): `=_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Current Liabilities","[Report_Field]",$B16)`
- **F21** at P16:Q18 (example `P16`): `=_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Current Liabilities","[Report_Field]",$B16)`
- **F22** at F19:G19, K19:L19, P19:Q19 (example `F19`): `=IFERROR(F10+F11+SUM(F12:F18),"NA")`
- **F23** at F23:G24, F26:G30 (example `F23`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Non Current Assets","[Report_Field]",$B23)`
- **F24** at K23:L24, K26:L30 (example `K23`): `=-_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Non Current Assets","[Report_Field]",$B23)`
- **F25** at P23:Q24, P26:Q30 (example `P23`): `=-_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Non Current Assets","[Report_Field]",$B23)`
- **F26** at F25:G25 (example `F25`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Non Current Assets","[DR_KPI]",$B25)-F11`
- **F27** at K25:L25 (example `K25`): `=-_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Non Current Assets","[DR_KPI]",$B25)-K11`
- **F28** at P25:Q25 (example `P25`): `=-_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Non Current Assets","[DR_KPI]",$B25)-P11`
- **F29** at F31, K31:L31, P31:Q31 (example `F31`): `=IFERROR(SUM(F23:F30),"NA")`
- **F30** at G31 (example `G31`): `=IFERROR(SUM(G22:G30),"NA")`
- **F31** at F32:G32, K32:L32, P32:Q32 (example `F32`): `=IFERROR(F19+F31,"NA")`
- **F32** at F36:G38 (example `F36`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B36)`
- **F33** at K36:L38 (example `K36`): `=_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B36)`
- **F34** at P36:Q38 (example `P36`): `=_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B36)`
- **F35** at F39:G46 (example `F39`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Equity","[Report_Field]",$B39)`
- **F36** at K39:L46 (example `K39`): `=_xldudf_DR_QTD(Value,"[Data Type]","Activity","[Scenario]",K$5,"[Reporting Month]",K$4,"[Account Group L2]","Equity","[Report_Field]",$B39)`
- **F37** at P39:Q46 (example `P39`): `=_xldudf_DR_YTD(Value,"[Data Type]","Activity","[Scenario]",P$5,"[Reporting Month]",P$4,"[Account Group L2]","Equity","[Report_Field]",$B39)`
- **F38** at F47:G47, K47:L47, P47:Q47 (example `F47`): `=IFERROR(SUM(F36:F46),"NA")`
- **F39** at H47, R47 (example `H47`): `=IFERROR(SUM(H35:H46),"NA")`
- **F40** at F48:G48, K48:L48, P48:Q48 (example `F48`): `=IFERROR(F32+F47,"NA")`
- **F41** at F52:G52 (example `F52`): `=_xldudf_DR_GET(Value,"[Data Type]","Beginning Balance","[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]","Cash")`
- **F42** at K52:L52 (example `K52`): `=_xldudf_DR_GET(Value,"[Data Type]","Beginning Balance","[Scenario]",K$5,"[Reporting Month]",EOMONTH(K$4,-MOD(MONTH(DR_DATE_PICKER)-DR_FY_START,3)),"[DR_KPI]","Cash")`
- **F43** at P52:Q52 (example `P52`): `=_xldudf_DR_GET(Value,"[Data Type]","Beginning Balance","[Scenario]",P$5,"[Reporting Month]",EOMONTH(P$4,-MOD(MONTH(DR_DATE_PICKER)-DR_FY_START,12)),"[DR_KPI]","Cash")`
- **F44** at F53:G53, K53:L53, P53:Q53 (example `F53`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]","Cash")`
- **F45** at F54:G54, K54:L54, P54:Q54 (example `F54`): `=F53-F52`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **icon set `3Triangles`** thresholds [percent 0; percent 0; percent 0 (strictly >)] — on H10:H18 M10:M18 R10:R18 H23:H30 M23:M30 R23:R30 H36:H46 M36:M46 R36:R46 H52:H54 M52:M54 R52:R54
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "percent", "value": "0"}, {"gte": false, "type": "percent", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 1, "ranges": "H10:H18 M10:M18 R10:R18 H23:H30 M23:M30 R23:R30 H36:H46 M36:M46 R36:R46 H52:H54 M52:M54 R52:R54"}`
- [P18] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0 (strictly >)] — on H35 M35 R35 H51 M51 R51 H55 M55 R55
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": false, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 18, "ranges": "H35 M35 R35 H51 M51 R51 H55 M55 R55"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
