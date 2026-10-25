# Spec: cf-dr-sc-style → sheet "Cash Flow Rolling 12M"

> Source: Cash Flow - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:V52`; Everything beyond it is hidden (columns after V, rows after 52). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 12.9 pt (unlisted rows HIDDEN (zeroHeight)) |
| Used range | A1:W60 |
| Merged ranges | none |
| Defined name `DR_DATE_PICKER` | `45747` |
| Defined name `Value` | `"widget_19324_0_tt_1773235212"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 40.57 | 216.8 |  |
| C:E | 4.57 | 27.8 |  |
| F:R | 16.57 | 90.8 |  |
| S | 9.29 | 52.5 |  |
| T | 9.57 | 54.0 |  |
| U:W | 8.71 | 49.5 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 10.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S3 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S4 | Calibri | 10.0 |  | 001F37 | FFDBE5 | – | `–` | centerContinuous | – | – | – |
| S5 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S6 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S7 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S8 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S9 | Poppins | 11.0 |  | F2F2F2 | – | – | `[$-409]yyyy\ mmmm;@` | left | – | – | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]yyyy\ mmmm;@` | – | center | – | – |
| S11 | Poppins | 11.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]yyyy\ mmmm;@` | centerContinuous | top | – | – |
| S13 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S14 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S15 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S16 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S17 | Poppins | 10.0 | B | 001F37 | – | – | `#,##0` | center | center | – | – |
| S18 | Poppins | 10.0 | B | 001F37 | – | B:thin:9EA1AA | `#,##0` | center | center | – | – |
| S19 | Poppins | 10.0 | B | 001F37 | – | B:thin:9EA1AA | `0.0%` | center | center | – | – |
| S20 | Poppins | 10.0 | B | 001F37 | – | – | `0.0%` | center | center | – | – |
| S21 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S22 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S23 | Poppins | 9.0 |  | 253D84 | – | L:thin:9EA1AA | `–` | center | center | – | – |
| S24 | Poppins | 9.0 |  | 253D84 | – | – | `–` | center | center | – | – |
| S25 | Poppins | 9.0 |  | 253D84 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S26 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S27 | Poppins | 9.0 |  | 253D84 | – | L:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S28 | Poppins | 9.0 |  | 253D84 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S29 | Poppins | 9.0 |  | 4D6ECD | – | – | `#,##0,\ "K"` | center | center | – | – |
| S30 | Poppins | 9.0 |  | 4D6ECD | – | – | `0.0%;\(0.0%\)` | center | center | – | – |
| S31 | Poppins | 10.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | center | – | – | – |
| S32 | Poppins | 10.0 |  | 333333 | – | – | `–` | center | center | – | – |
| S33 | Poppins | 10.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | – | – | – |
| S34 | Poppins | 8.0 |  | 3F3F3F | – | L:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S35 | Poppins | 8.0 |  | 3F3F3F | – | – | `#,##0,\ "K"` | center | center | – | – |
| S36 | Poppins | 10.0 |  | 7F7F7F | – | – | `#,##0,\ "K"` | center | center | – | – |
| S37 | Poppins | 8.0 |  | 7F7F7F | – | – | `#,##0,\ "K"` | center | center | – | – |
| S38 | Poppins | 8.0 |  | 7F7F7F | – | – | `0.0%;\(0.0%\)` | center | center | – | – |
| S39 | Poppins | 10.0 |  | 7F7F7F | – | L:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S40 | Poppins | 10.0 |  | 7F7F7F | – | – | `0.0%;\(0.0%\)` | center | center | – | – |
| S41 | Poppins | 8.0 |  | 4D6ECD | – | L:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S42 | Poppins | 8.0 |  | 4D6ECD | – | – | `#,##0,\ "K"` | center | center | – | – |
| S43 | Poppins | 8.0 |  | 4D6ECD | – | – | `0.0%;\(0.0%\)` | center | center | – | – |
| S44 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S45 | Poppins | 8.0 |  | 4D6ECD | – | – | `–` | center | center | – | – |
| S46 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S47 | Poppins | 10.0 | B | 000090 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S48 | Poppins | 10.0 | B | 000090 | – | – | `0.0%;\(0.0%\)` | center | center | – | – |
| S49 | Poppins | 8.0 |  | 4D6ECD | – | – | `–` | left | center | 3.0 | – |
| S50 | Poppins | 12.0 | B | 626364 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S51 | Poppins | 10.0 | B | 000090 | – | B:thin:9EA1AA | `–` | center | center | – | – |
| S52 | Poppins | 10.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S53 | Poppins | 10.0 | B | 000090 | – | – | `–` | center | center | – | – |
| S54 | Poppins | 10.0 | B | 000090 | – | B:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S55 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S56 | Poppins | 9.0 |  | 253D84 | – | – | `–` | left | center | 1.0 | – |
| S57 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S58 | Poppins | 10.0 | I | 7F7F7F | – | B:thin:9EA1AA | `–` | center | center | – | – |
| S59 | Poppins | 10.0 | I | 7F7F7F | – | – | `–` | center | center | – | – |
| S60 | Poppins | 10.0 |  | 7F7F7F | – | B:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S61 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S62 | Poppins | 8.0 |  | 7F7F7F | – | – | `–` | center | center | – | – |
| S63 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S64 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:R=S1 S:V=S2
- **T2** h=24.0 rows 2: A:E=S1 F:G=S3 H:Q=S4 R=S1 S:V=S2
- **T3** h=8.25 rows 3: A:R=S1 S:V=S2
- **T4** h=24.0 rows 4: A=S1 B=S5 C:E=S1 F:Q=S6 R=S1 S:V=S2
- **T5** h=24.0 rows 5: A=S1 B=S7 C:E=S1 F:Q=S8 R=S1 S:V=S2
- **T6** h=16.0 rows 6: A:R=S1 S:V=S2
- **T7** h=24.0 rows 7: A=S2 B=S9 C=S10 D=S11 E=S10 F=S2 G:J=S12 K=S10 L:R=S13 S:V=S2
- **T8** h=24.0 rows 8: A=S2 B=S14 C:Q=S15 R=S13 S:V=S2
- **T9** h=24.0 rows 9: A=S2 B=S16 C:E=S17 F:G=S18 H:I=S19 J:M=S18 N:O=S19 P:Q=S18 R=S17 S=S20 T:V=S2
- **T10** h=24.0 rows 10: A=S21 B=S22 C=S23 D=S24 E=S25 F:Q=S26 R=S27 S:T=S28 U=S29 V=S30
- **T11** h=24.0 rows 11-16,24-25,27,34-36: A=S21 B=S22 C=S31 D=S32 E=S33 F:Q=S26 R=S34 S=S35 T=S36 U=S37 V=S38
- **T12** h=24.0 rows 17,23,26,33,37,40: A=S21 B=S22 C=S31 D=S32 E=S33 F:Q=S26 R=S39 S:U=S36 V=S40
- **T13** h=24.0 rows 18: A=S21 B=S22 C=S31 D=S32 E=S33 F:Q=S26 R=S41 S:U=S42 V=S43
- **T14** h=24.0 rows 19: A=S2 B=S44 C:E=S45 F:Q=S46 R:U=S47 V=S48
- **T15** h=24.0 rows 20: A=S2 B=S49 C:E=S45 F:Q=S50 R:T=S28 U=S29 V=S30
- **T16** h=24.0 rows 21: A=S2 B=S14 C:Q=S15 R:T=S28 U=S29 V=S30
- **T17** h=24.0 rows 22: A=S2 B=S51 C=S52 D=S53 E=S52 F:Q=S54 R:T=S28 U=S29 V=S30
- **T18** h=24.0 rows 28: A=S2 B=S44 C:E=S45 F:Q=S46 R:U=S36 V=S40
- **T19** h=24.0 rows 29: A=S2 B=S55 C=S24 D=S56 E=S24 F:Q=S57 R:S=S35 T=S36 U=S37 V=S38
- **T20** h=24.0 rows 30: A=S2 B=S55 C=S24 D=S56 E=S24 F:Q=S57 R:U=S36 V=S40
- **T21** h=24.0 rows 31: A=S2 B=S14 C:Q=S15 R:U=S36 V=S40
- **T22** h=24.0 rows 32: A=S2 B=S58 C=S52 D=S59 E=S52 F:Q=S60 R:U=S36 V=S40
- **T23** h=24.0 rows 38,41: A=S21 B=S22 C=S31 D=S32 E=S33 F:Q=S26 R=S27 S:T=S28 U=S29 V=S30
- **T24** h=24.0 rows 39,42-43: A=S21 B=S22 C=S31 D=S32 E=S33 F:Q=S26 R=S61 S:V=S2
- **T25** h=24.0 rows 44: A=S2 B=S44 C=S24 D=S56 E=S24 F:Q=S46 R:V=S2
- **T26** h=24.0 rows 45-46: A=S2 B=S55 C=S24 D=S56 E=S24 F:Q=S57 R:V=S2
- **T27** h=24.0 rows 47: A=S2 B=S14 C:Q=S15 R:V=S2
- **T28** h=24.0 rows 48: A=S2 B=S58 C=S52 D=S59 E=S52 F:Q=S60 R:V=S2
- **T29** h=24.0 rows 49-51: A=S21 B=S22 C=S31 D=S62 E=S33 F:Q=S26 R=S61 S:V=S2
- **T30** h=24.0 rows 52: A=S2 B=S63 C=S24 D=S56 E=S24 F:Q=S64 R:V=S2

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"F": "End of Month"}
- r4: {"B": "Cash Flow - Rolling 12M"}
- r5: {"F": "Actuals", "G": "Actuals", "H": "Actuals", "I": "Actuals", "J": "Actuals", "K": "Actuals", "L": "Actuals", "M": "Actuals", "N": "Actuals", "O": "Actuals", "P": "Actuals", "Q": "Actuals"}
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
- r24: {"B": "Intercompany receivable"}
- r25: {"B": "Long Term Investments"}
- r26: {"B": "Net Fixed Assets"}
- r27: {"B": "Net Intangible Assets"}
- r28: {"B": "Total Investing Activity"}
- r29: {"B": "Free Cash Flow"}
- r31: {"B": "CF from Financing Activity"}
- r33: {"B": "Bank Loan"}
- r34: {"B": "Intercompany payables"}
- r35: {"B": "Long Term Liability"}
- r36: {"B": "Ordinary Shares"}
- r37: {"B": "Other Equity"}
- r38: {"B": "Non-Controlling Interest"}
- r39: {"B": "Ordinary Shares"}
- r40: {"B": "Other Equity"}
- r41: {"B": "Equity"}
- r42: {"B": "Net Income Calc"}
- r43: {"B": "Retained Earnings"}
- r44: {"B": "Total Financing Activity"}
- r45: {"B": "Total Cash Flow"}
- r47: {"B": "Summary"}
- r49: {"B": "Cash - beginning of period"}
- r50: {"B": "Cash - ending of period"}
- r51: {"B": "Cash PoP Change"}
- r52: {"B": "Gap", "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0, "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at F4:P4 (example `F4`): `=EOMONTH(G4,-1)`
- **F2** at Q4 (example `Q4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F3** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F4** at F10:Q10 (example `F10`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L1]","REVENUE")-_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L1]","EXPENSE")`
- **F5** at D11, D16:D18, D33:D43 (example `D11`): `="( + )"`
- **F6** at F11:Q11 (example `F11`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]",$B11)`
- **F7** at D12:D15, D23:D27 (example `D12`): `="( - )"`
- **F8** at F12:Q15 (example `F12`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Current Assets","[Report_Field]",$B12)`
- **F9** at F16:Q18 (example `F16`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Current Liabilities","[Report_Field]",$B16)`
- **F10** at F19:Q19 (example `F19`): `=IFERROR(F10+F11+SUM(F12:F18),"NA")`
- **F11** at F23:Q23 (example `F23`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Non Current Assets","[DR_KPI]",$B23)-F11`
- **F12** at F24:Q27 (example `F24`): `=-_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Non Current Assets","[Report_Field]",$B24)`
- **F13** at F28:Q28 (example `F28`): `=IFERROR(SUM(F23:F27),"NA")`
- **F14** at F29:Q29 (example `F29`): `=IFERROR(F19+F28,"NA")`
- **F15** at F33:Q35 (example `F33`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B33)`
- **F16** at F36:Q43 (example `F36`): `=_xldudf_DR_GET(Value,"[Data Type]","Activity","[Scenario]",F$5,"[Reporting Month]",F$4,"[Account Group L2]","Equity","[Report_Field]",$B36)`
- **F17** at F44:Q44 (example `F44`): `=IFERROR(SUM(F33:F43),"NA")`
- **F18** at F45:Q45 (example `F45`): `=IFERROR(F29+F44,"NA")`
- **F19** at F49:Q49 (example `F49`): `=_xldudf_DR_GET(Value,"[Data Type]","Beginning Balance","[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]","Cash")`
- **F20** at F50:Q50 (example `F50`): `=_xldudf_DR_GET(Value,"[Scenario]",F$5,"[Reporting Month]",F$4,"[DR_KPI]","Cash")`
- **F21** at F51:Q51 (example `F51`): `=F50-F49`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0 (strictly >)] — on U10:U18 U20:U38 U40:U41
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": false, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 1, "ranges": "U10:U18 U20:U38 U40:U41"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
