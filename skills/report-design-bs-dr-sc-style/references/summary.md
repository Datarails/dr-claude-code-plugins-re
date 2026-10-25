# Spec: bs-dr-sc-style → sheet "Summary"

> Source: Balance Sheet - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:W55`; Everything beyond it is hidden (columns after W, rows after 55). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 70 |
| Default row height | 0 pt (unlisted rows HIDDEN (zeroHeight)) |
| Used range | A1:X61 |
| Merged ranges | E4:G4, I4:K4, M4:O4 |
| Defined name `DR_DATE_PICKER` | `46022` |
| Defined name `DR_FY_START` | `1` |
| Defined name `Value` | `"widget_19324_0_tt_1774777138118.73"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 40.57 | 216.8 |  |
| C | 16.57 | 90.8 |  |
| D | 4.57 | 27.8 |  |
| E:G | 16.57 | 90.8 |  |
| H | 4.57 | 27.8 |  |
| I:K | 16.57 | 90.8 |  |
| L | 4.57 | 27.8 |  |
| M:O | 16.57 | 90.8 |  |
| P | 4.57 | 27.8 |  |
| Q | 11.00 | 61.5 |  |
| R:X | 9.14 | 51.8 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 10.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 11.0 |  | auto | – | – | `–` | – | – | – | – |
| S3 | Poppins | 11.0 |  | F7F7F7 | – | – | `–` | – | – | – | – |
| S4 | Poppins | 11.0 | B | F7F7F7 | – | – | `–` | – | – | – | – |
| S5 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S6 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S7 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S8 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S9 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S10 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | center | center | – | – |
| S11 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S13 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | center | top | – | – |
| S14 | Poppins | 12.0 |  | F7F7F7 | – | – | `[$-409]\ yyyy\ mmmm;@` | – | top | – | – |
| S15 | Poppins | 9.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S16 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S17 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S18 | Poppins | 9.0 |  | F7F7F7 | – | – | `–` | left | center | – | – |
| S19 | Poppins | 10.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S20 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S21 | Poppins | 12.0 | B | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S22 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S23 | Poppins | 8.0 |  | 001F37 | – | B:thin:9EA1AA | `#,##0_);(#,##0)` | center | center | – | – |
| S24 | Poppins | 10.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S25 | Poppins | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | – | – | – |
| S26 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S27 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S28 | Poppins | 10.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | center | – | – | – |
| S29 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S30 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S31 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S32 | Poppins | 8.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S33 | Poppins | 11.0 |  | 001F37 | – | – | `–` | center | – | – | – |
| S34 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S35 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S36 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S37 | Poppins | 10.0 | I | 001F37 | – | – | `–` | left | center | 1.0 | – |
| S38 | Poppins | 8.0 |  | 001F37 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S39 | Poppins | 8.0 |  | 001F37 | – | – | `0%` | center | center | – | – |
| S40 | Poppins | 12.0 |  | 333333 | F2F2FB | – | `@` | left | center | 1.0 | – |
| S41 | Poppins | 8.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S42 | Poppins | 10.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | left | center | – | – |
| S43 | Poppins | 8.0 |  | 001F37 | – | B:thin:9EA1AA | `#,##0,\ "K"` | center | center | – | – |
| S44 | Poppins | 8.0 |  | 001F37 | – | B:thin:9EA1AA | `0%` | center | center | – | – |
| S45 | Poppins | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S46 | Poppins | 9.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | center | center | – | – |
| S47 | Poppins | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S48 | Poppins | 9.0 |  | 001F37 | – | – | `–` | center | center | – | – |
| S49 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S50 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S51 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S52 | Poppins | 10.0 | B | F7F7F7 | – | – | `–` | left | center | – | – |
| S53 | Poppins | 8.0 | B | F7F7F7 | – | – | `#,##0,\ "K"` | center | center | – | – |
| S54 | Poppins | 8.0 | B | F7F7F7 | – | – | `0%` | center | center | – | – |
| S55 | Poppins | 14.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S56 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S57 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S58 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S59 | Poppins | 12.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S60 | Poppins | 10.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T2** h=24.0 rows 2: A:B=S1 C=S6 D=S1 E:G=S7 H=S1 I:K=S7 L=S1 M:O=S7 P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T3** h=8.25 rows 3: A:P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T4** h=24.0 rows 4: A=S1 B=S8 C=S9 D=S1 E:G=S10 H=S1 I:K=S10 L=S1 M:O=S10 P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T5** h=24.0 rows 5: A=S1 B=S11 C=S12 D=S1 E:G=S12 H=S1 I:K=S12 L=S1 M:O=S12 P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T6** h=16.0 rows 6: A:P=S1 Q=S2 R:T=S3 U=S4 V:W=S5
- **T7** h=24.0 rows 7: A=S5 B=S3 C:D=S5 E:F=S13 G=S14 H=S5 I:K=S14 L=S5 M:O=S14 P=S3 Q=S2 R:T=S3 U=S4 V:W=S5
- **T8** h=24.0 rows 8: A=S15 B=S16 C:O=S17 P:W=S5
- **T9** h=24.0 rows 9: A=S15 B:C=S18 D=S19 E:G=S18 H=S19 I:K=S18 L=S19 M:P=S18 Q:W=S5
- **T10** h=24.0 rows 10: A=S5 B=S20 C:O=S21 P:W=S5
- **T11** h=24.0 rows 11: A=S5 B=S22 C=S23 D=S24 E:G=S23 H=S24 I:K=S23 L=S24 M:O=S23 P:W=S5
- **T12** h=24.0 rows 12-15,21,24,52-53: A=S25 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S31 Q:W=S5
- **T13** h=24.0 rows 16,34,41: A=S32 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S31 Q:W=S5
- **T14** h=24.0 rows 17,35: A=S33 B=S34 C=S35 D=S24 E:F=S35 G=S36 H=S24 I:J=S35 K=S36 L=S24 M:N=S35 O=S36 P:W=S5
- **T15** h=24.0 rows 18: A=S33 B=S37 C=S38 D=S24 E:F=S38 G=S39 H=S24 I:J=S38 K=S39 L=S24 M:N=S38 O=S39 P:W=S5
- **T16** h=24.0 rows 19: A=S5 B=S20 C:O=S40 P:W=S5
- **T17** h=24.0 rows 20: A=S41 B=S42 C=S43 D=S24 E:F=S43 G=S44 H=S24 I:J=S43 K=S44 L=S24 M:N=S43 O=S44 P:W=S5
- **T18** h=24.0 rows 22,47: A=S25 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S45 Q:W=S5
- **T19** h=24.0 rows 23,49-51: A=S46 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S31 Q:W=S5
- **T20** h=24.0 rows 25: A=S33 B=S34 C=S35 D=S24 E:F=S35 G=S36 H=S24 I:J=S35 K=S36 L=S24 M:N=S35 O=S36 P=S47 Q:W=S5
- **T21** h=24.0 rows 26: A=S48 B=S49 C=S50 D=S24 E:F=S50 G=S51 H=S24 I:J=S50 K=S51 L=S24 M:N=S50 O=S51 P:W=S5
- **T22** h=24.0 rows 27: A=S48 B=S52 C=S53 D=S24 E:F=S53 G=S54 H=S24 I:J=S53 K=S54 L=S24 M:N=S53 O=S54 P:W=S5
- **T23** h=24.0 rows 28: A=S5 B=S16 C:O=S17 P:W=S5
- **T24** h=24.0 rows 29: A=S33 B:K=S55 L=S56 M:O=S57 P:W=S5
- **T25** h=24.0 rows 30: A=S33 B=S20 C:O=S21 P:W=S5
- **T26** h=24.0 rows 31: A=S5 B=S42 C=S23 D=S24 E:G=S23 H=S24 I:K=S23 L=S24 M:O=S23 P:W=S57
- **T27** h=24.0 rows 32-33,48: A=S58 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S59 Q:W=S57
- **T28** h=24.0 rows 36: A=S33 B=S37 C=S38 D=S24 E:F=S38 G=S39 H=S24 I:J=S38 K=S39 L=S24 M:N=S38 O=S39 P=S47 Q:W=S5
- **T29** h=24.0 rows 37: A=S33 B=S20 C:O=S40 P:W=S5
- **T30** h=24.0 rows 38: A=S5 B=S42 C=S43 D=S24 E:F=S43 G=S44 H=S24 I:J=S43 K=S44 L=S24 M:N=S43 O=S44 P:W=S5
- **T31** h=24.0 rows 39-40: A=S58 B=S26 C=S27 D=S28 E=S27 F=S29 G=S30 H=S28 I=S27 J=S29 K=S30 L=S28 M=S27 N=S29 O=S30 P=S31 Q:W=S5
- **T32** h=24.0 rows 42: A=S41 B=S34 C=S35 D=S24 E:F=S35 G=S36 H=S24 I:J=S35 K=S36 L=S24 M:N=S35 O=S36 P:W=S5
- **T33** h=24.0 rows 43: A=S41 B=S49 C=S50 D=S24 E:F=S50 G=S51 H=S24 I:J=S50 K=S51 L=S24 M:N=S50 O=S51 P:W=S5
- **T34** h=24.0 rows 44: A=S33 B=S52 C=S53 D=S24 E:F=S53 G=S54 H=S24 I:J=S53 K=S54 L=S24 M:N=S53 O=S54 P:W=S5
- **T35** h=24.0 rows 45: A=S41 B=S16 C:O=S17 P:W=S5
- **T36** h=24.0 rows 46: A=S33 B=S22 C=S60 D=S24 E:G=S60 H=S24 I:K=S60 L=S24 M:O=S60 P:W=S5
- **T37** h=24.0 rows 54: A=S5 B=S34 C=S35 D=S19 E:F=S35 G=S36 H=S19 I:J=S35 K=S36 L=S19 M:N=S35 O=S36 P:W=S5
- **T38** h=24.0 rows 55: A=S5 B=S49 C=S50 D=S19 E:F=S50 G=S51 H=S19 I:J=S50 K=S51 L=S19 M:N=S50 O=S51 P:W=S5

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"C": "Month", "E": "Previous Month", "I": "Previous Quarter", "M": "Previous Year End"}
- r4: {"B": "BS Summary"}
- r5: {"C": "Actuals", "E": "Actuals", "F": "∆ vs PM", "G": "% ∆ vs PM", "I": "Actuals", "J": "∆ vs PQ", "K": "% ∆ vs PQ", "M": "Actuals", "N": "∆ vs PY", "O": "% ∆ vs PY"}
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

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at C4 (example `C4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at E4 (example `E4`): `=EOMONTH(C4,-1)`
- **F3** at I4 (example `I4`): `=IFERROR(EOMONTH($C4,-IF(MOD(MONTH($C4)-(DR_FY_START-1),3)=0,3,MOD(MONTH($C4)-(DR_FY_START-1),3))),"NA")`
- **F4** at M4 (example `M4`): `=IFERROR(EOMONTH($C4,-IF(MOD(MONTH($C4)-(DR_FY_START-1),12)=0,12,MOD(MONTH($C4)-(DR_FY_START-1),12))),"NA")`
- **F5** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F6** at C12:C16, E12:E16, I12:I16, M12:M16 (example `C12`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Assets","[Report_Field]",$B12,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F7** at F12:F17, J12:J17, N12:N17, F21:F26, J21:J26, N21:N26, F32:F35, J32:J35, N32:N35, F39:F43, J39:J43, N39:N43, F47:F55, J47:J55, N47:N55 (example `F12`): `=IFERROR($C12-E12,"NA")`
- **F8** at G12:G17, K12:K17, O12:O17, G21:G26, K21:K26, O21:O26, G32:G35, K32:K35, O32:O35, G39:G43, K39:K43, O39:O43, G47:G55, K47:K55, O47:O55 (example `G12`): `=IFERROR(F12/E12,"NA")`
- **F9** at C17, E17, I17, M17 (example `C17`): `=IFERROR(SUM(C11:C16),"NA")`
- **F10** at C21:C24, E21:E24, I21:I24, M21:M24 (example `C21`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Non Current Assets","[Report_Field]",$B21,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F11** at C25, E25, I25, M25 (example `C25`): `=IFERROR(SUM(C20:C24),"NA")`
- **F12** at C26, E26, I26, M26 (example `C26`): `=C17+C25`
- **F13** at C32:C34, E32:E34, I32:I34, M32:M34 (example `C32`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Current Liabilities","[Report_Field]",$B32,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F14** at C35, E35, I35, M35, C42, E42, I42, M42 (example `C35`): `=SUM(C31:C34)`
- **F15** at C39:C41, E39:E41, I39:I41, M39:M41 (example `C39`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Long Term Liabilities","[Report_Field]",$B39,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F16** at C43, E43, I43, M43 (example `C43`): `=C35+C42`
- **F17** at C47:C53, E47:E53, I47:I53, M47:M53 (example `C47`): `=_xldudf_DR_GET(Value,"[Account Group L2]","Equity","[Report_Field]",$B47,"[Reporting Month]",C$4,"[Scenario]",C$5)`
- **F18** at C54, E54, I54, M54 (example `C54`): `=SUM(C47:C53)`
- **F19** at C55, E55, I55, M55 (example `C55`): `=C54+C43`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P4] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on F12:F16 J12:J16 N12:N16 F21:F24 J21:J24 N21:N24 F32:F34 J32:J34 N32:N34 F39:F41 J39:J41 N39:N41 F47:F53 J47:J53 N47:N53
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 4, "ranges": "F12:F16 J12:J16 N12:N16 F21:F24 J21:J24 N21:N24 F32:F34 J32:J34 N32:N34 F39:F41 J39:J41 N39:N41 F47:F53 J47:J53 N47:N53"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
