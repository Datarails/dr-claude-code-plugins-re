# Spec: kpi-dr-sc-style → sheet "Cash Flow"

> Source: KPIs for Dashboard — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:AA33`; Everything beyond it is hidden (columns after AA, rows after 33). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 136 |
| Default row height | 14.5 pt (unlisted rows visible) |
| Used range | A1:AB34 |
| Merged ranges | B12:C12, B28:C28, B5:C5, I27:M28, I2:Q2, I4:M5, L30:M30, L31:M31, N4:R5, T25:AA25, T2:AA2 |
| Data validation | `E27:F27 F4:G4` list `List!#REF!` |
| Data validation | `C6:C8 C30:C31 D8:E8` list `List!$B$2:$B$5` |
| Data validation | `C4 C27` list `List!$A$2:$A$4` |
| Defined name `Burn_Rate` | `'Cash Flow'!$C$13` |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `DR_FY_START` | `1` |
| Defined name `FY_Start` | `'P&L - A higher result is better'!$B$2` |
| Defined name `Value` | `"widget_19324_0_tt_1786512183639.7"` |
| Defined name `Value_CF_KPI` | `"widget_19314_0_tt_1786512183641.7"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1786512183634.7"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 2.71 | 18.0 |  |
| B | 11.71 | 65.2 |  |
| C | 18.57 | 101.2 |  |
| D:E | 16.57 | 90.8 |  |
| G | 8.71 | 49.5 |  |
| H | 6.43 | 37.5 |  |
| I | 1.57 | 12.0 |  |
| J | 2.57 | 17.2 |  |
| K:L | 8.57 | 48.8 |  |
| M | 16.57 | 90.8 |  |
| N | 6.43 | 37.5 |  |
| O | 2.57 | 17.2 |  |
| P | 7.29 | 42.0 |  |
| Q | 18.71 | 102.0 |  |
| R | 6.43 | 37.5 |  |
| S | 12.86 | 71.2 |  |
| T | 10.71 | 60.0 |  |
| U | 15.29 | 84.0 |  |
| V | 15.29 | 84.0 |  |
| W | 13.43 | 74.2 |  |
| X | 8.29 | 47.2 |  |
| Y | 12.86 | 71.2 |  |
| Z | 13.29 | 73.5 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 11.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S2 | Calibri | 11.0 | B | 000000 | E7F4FF | – | `–` | – | – | – | – |
| S3 | Calibri | 11.0 |  | 000000 | E7F4FF | – | `–` | – | – | – | – |
| S4 | Calibri | 11.0 |  | 000000 | – | B:thin:auto | `–` | – | – | – | – |
| S5 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | – | `[$-409]mmm\-yy;@` | center | center | – | – |
| S6 | Calibri | 11.0 |  | 000000 | – | R:thin:auto | `–` | – | – | – | – |
| S7 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S8 | Calibri | 11.0 |  | 000000 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S9 | Calibri | 11.0 | B | 7FFFD4 | – | L:thin:auto | `–` | – | – | – | – |
| S10 | Calibri | 11.0 | B | 7FFFD4 | – | – | `–` | – | – | – | – |
| S11 | Calibri | 11.0 | B | 7FFFD4 | FFFFFF | – | `–` | – | – | – | – |
| S12 | Calibri | 11.0 |  | 000000 | FFFFFF | – | `–` | – | – | – | – |
| S13 | Calibri | 11.0 | B | 000000 | – | – | `–` | centerContinuous | – | – | – |
| S14 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S15 | Calibri | 11.0 |  | 000000 | FFFFFF | B:thin:auto | `–` | – | – | – | – |
| S16 | Poppins | 32.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | left | top | 1.0 | – |
| S17 | Poppins | 72.0 | B | 000000 | FFFFFF | – | `#,##0.0` | center | center | – | – |
| S18 | Calibri | 9.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S19 | Calibri | 9.0 | B | 000000 | – | – | `–` | – | – | – | – |
| S20 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S21 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S22 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S23 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto | `–` | – | – | – | – |
| S24 | Calibri | 22.0 | B | 000000 | FFFFFF | – | `#,##0.0` | center | center | – | – |
| S25 | Calibri | 9.0 |  | 000000 | – | – | `mm-dd-yy` | – | – | – | – |
| S26 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S27 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0.00` | – | – | – | – |
| S28 | Calibri | 11.0 |  | 000000 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `0%` | – | – | – | – |
| S29 | Calibri | 11.0 |  | 000000 | – | L:thin:auto | `–` | – | – | – | – |
| S30 | Calibri | 40.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | – | center | – | – |
| S31 | Calibri | 64.0 | B | 000000 | FFFFFF | – | `#,##0.0` | – | center | – | – |
| S32 | Calibri | 10.0 |  | 000000 | FFFFFF | – | `–` | left | – | – | – |
| S33 | Calibri | 9.0 |  | 000000 | – | – | `–` | right | – | – | – |
| S34 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S35 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `–` | – | – | – | – |
| S36 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `0%` | – | – | – | – |
| S37 | Calibri | 11.0 |  | 000000 | – | – | `_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)` | – | – | – | – |
| S38 | Calibri | 11.0 |  | 000000 | DBDBDB | – | `–` | – | – | – | – |
| S39 | Calibri | 11.0 |  | 000000 | – | L:thin:auto | `_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)` | – | – | – | – |
| S40 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `_(* #,##0_);_(* \(#,##0\);_(* "-"??_);_(@_)` | – | – | – | – |
| S41 | Calibri | 11.0 |  | 000000 | – | T:thin:auto | `–` | – | – | – | – |
| S42 | Calibri | 11.0 |  | 000000 | – | – | `0.0` | – | – | – | – |
| S43 | Wingdings 3 | 11.0 |  | C00000 | FFFFFF | – | `0%` | – | – | – | – |
| S44 | Calibri | 9.0 |  | C00000 | FFFFFF | – | `0%` | center | – | – | – |
| S45 | Calibri | 8.0 |  | 000000 | FFFFFF | – | `–` | left | – | – | – |
| S46 | Calibri | 8.0 |  | C00000 | FFFFFF | – | `0%` | – | – | – | – |
| S47 | Calibri | 8.0 |  | 000000 | FFFFFF | – | `–` | left | – | 1.0 | – |
| S48 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | – | `[$-409]mmm\-yy;@` | – | center | – | – |
| S49 | Calibri | 11.0 | B | 000000 | FFFFFF | – | `–` | left | – | 1.0 | – |
| S50 | Poppins | 32.0 | B | 333333 | FFFFFF | – | `#,##0,\ "K"` | left | top | 1.0 | – |
| S51 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S52 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S53 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S54 | Calibri | 40.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | left | center | 1.0 | – |
| S55 | Wingdings 3 | 14.0 |  | C00000 | FFFFFF | – | `0%` | center | top | – | – |
| S56 | Poppins | 12.0 | B | C00000 | FFFFFF | – | `0%` | center | center | – | – |
| S57 | Poppins | 12.0 |  | 333333 | FFFFFF | – | `–` | left | center | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=14.5 rows 1: A=S1 B=S2 C=S3 D:AA=S1
- **T2** h=14.5 rows 2: A=S1 B:C=S4 D:H=S1 I:Q=S5 R:S=S1 T:AA=S5
- **T3** h=14.5 rows 3: A=S6 B=S7 C=S8 D=S9 E=S10 F=S11 G:H=S12 I=S1 J:L=S13 M=S1 N:P=S13 Q:AA=S1
- **T4** h=30.0 rows 4: A=S6 B=S7 C=S8 D=S14 E=S4 F:G=S15 H=S12 I:M=S16 N:R=S17 S=S1 T=S18 U:AA=S19
- **T5** h=30.0 rows 5: A=S6 B:C=S20 D:E=S21 F:G=S22 H=S23 I:M=S16 N:R=S17 S=S24 T=S19 U:Y=S18 Z=S25 AA=S18
- **T6** h=15.75 rows 6: A=S6 B:C=S7 D=S26 E=S27 F:G=S28 H=S29 I:M=S30 N:R=S31 S=S32 T=S19 U:Y=S18 Z=S25 AA=S33
- **T7** h=15.75 rows 7: A=S6 B:C=S7 D=S34 E=S27 F:G=S28 H=S29 I:M=S30 N:R=S31 S=S32 T=S19 U:Y=S18 Z=S25 AA=S33
- **T8** h=14.5 rows 8: A=S1 B:E=S35 F:G=S36 H=S12 I:M=S30 N:R=S31 S:AA=S1
- **T9** h=14.5 rows 9: A:C=S1 D:E=S37 F:H=S1 I:Q=S38 R:AA=S1
- **T10** h=14.5 rows 10,16: A:C=S1 D:E=S37 F:L=S1 M:N=S37 O:S=S1 T=S19 U=S1 V:Y=S18 Z=S25 AA=S1
- **T11** h=14.5 rows 11: A=S1 B:C=S4 D:E=S37 F:L=S1 M:N=S37 O:S=S1 T=S19 U=S1 V:Y=S18 Z=S25 AA=S1
- **T12** h=14.5 rows 12: A=S6 B:C=S21 D=S39 E=S37 F:L=S1 M:N=S37 O:S=S1 T=S19 U=S1 V:Y=S18 Z=S25 AA=S1
- **T13** h=14.5 rows 13-14: A=S6 B=S7 C=S40 D=S39 E=S37 F:L=S1 M:N=S37 O:AA=S1
- **T14** h=14.5 rows 15: A=S1 B:C=S41 D:E=S37 F:S=S1 T=S19 U=S1 V:Y=S18 Z=S25 AA=S1
- **T15** h=14.5 rows 17: A:S=S1 T=S19 U=S1 V:Y=S18 Z=S25 AA=S1
- **T16** h=None rows 18: A:AA=S1
- **T17** h=14.5 rows 19: A:L=S1 M:O=S37 P=S42 Q:AA=S1
- **T18** h=14.5 rows 20-21: A:L=S1 M:N=S37 O:S=S1 T=S19 U:W=S1 X:Y=S18 Z=S25 AA=S1
- **T19** h=14.5 rows 22: A:S=S1 T=S19 U:W=S1 X:Y=S18 Z=S25 AA=S1
- **T20** h=14.5 rows 23: A:G=S1 H=S12 I=S43 J=S44 K:L=S45 M=S12 N:AA=S1
- **T21** h=14.5 rows 24: A:G=S1 H:I=S12 J=S46 K:L=S47 M=S12 N:AA=S1
- **T22** h=14.5 rows 25: A=S1 B:C=S4 D:H=S1 I:M=S48 N:S=S1 T:AA=S5
- **T23** h=14.5 rows 26: A=S6 B=S7 C=S8 D=S29 E:G=S12 H=S1 I=S49 J:AA=S1
- **T24** h=12.0 rows 27: A=S6 B=S7 C=S8 D=S14 E:F=S15 G=S12 H=S1 I:M=S50 N:S=S1 T=S18 U:W=S1 X:AA=S19
- **T25** h=30.0 rows 28: A=S6 B:C=S20 D=S21 E:F=S22 G=S23 H=S1 I:M=S50 N:S=S1 T=S19 U:V=S1 W=S18 X=S1 Y=S18 Z=S25 AA=S18
- **T26** h=8.15 rows 29: A=S1 B:C=S51 D=S52 E:F=S53 G=S12 H=S1 I:M=S54 N:S=S1 T=S19 U:V=S1 W=S18 X=S1 Y=S18 Z=S25 AA=S18
- **T27** h=20.15 rows 30: A=S6 B:C=S7 D=S26 E:F=S28 G=S29 H:I=S1 J=S55 K=S56 L:M=S57 N:S=S1 T=S19 U:V=S1 W=S18 X=S1 Y=S18 Z=S25 AA=S18
- **T28** h=20.15 rows 31: A=S6 B:C=S7 D=S34 E:F=S28 G=S29 H:I=S1 J=S55 K=S56 L:M=S57 N:S=S1 T=S19 U:V=S1 W=S18 X=S1 Y=S18 Z=S25 AA=S18
- **T29** h=None rows 32: A=S1 B:F=S41 G:AA=S1
- **T30** h=14.5 rows 33: A:H=S1 I:M=S38 N:AA=S1

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r1: {"B": "Fill in Cells"}
- r2: {"B": 1, "I": "Published Item", "T": "Formula Components"}
- r3: {"A": 1, "B": "Field", "C": "Account Group L1", "J": "Net Monthly Burn", "O": "Runway Duration"}
- r4: {"B": "Aggregation", "C": "MTD", "V": "Account Group L2", "X": "Data Type", "Y": "Scenario", "Z": "Reporting Month", "AA": "DR_KPI"}
- r5: {"B": "Compare Analysis", "D": "Compare Result 1", "E": "Compare Result 2", "F": "If % of change is below --> Red", "G": "If % of change is Above --> Green", "T": "Base", "U": "REVENUE", "X": "Activity", "Y": "Actuals"}
- r6: {"B": "Compare A", "C": "Previous Month", "F": -0.05, "G": 0.05, "T": "Compare A", "U": "REVENUE", "X": "Activity"}
- r7: {"B": "Compare B", "C": "Previous Year", "F": -0.1, "G": 0.1, "T": "Compare B", "U": "REVENUE", "X": "Activity"}
- r9: {"K": "Widget Size:2X5", "O": "Widget Size:2X5"}
- r10: {"T": "Base", "V": "Cost of Goods Sold", "X": "Activity", "Y": "Actuals"}
- r11: {"T": "Compare A", "V": "Cost of Goods Sold", "X": "Activity"}
- r12: {"B": "Named Ranges (Formulas)", "T": "Compare B", "V": "Cost of Goods Sold", "X": "Activity"}
- r13: {"B": "Burn Rate"}
- r14: {"B": "Runway"}
- r15: {"T": "Base", "V": "Operating Expense", "W": "Other Expense", "X": "Activity", "Y": "Actuals"}
- r16: {"T": "Compare A", "V": "Operating Expense", "W": "Other Expense", "X": "Activity"}
- r17: {"T": "Compare B", "V": "Operating Expense", "W": "Other Expense", "X": "Activity"}
- r20: {"T": "Base", "Y": "Actuals", "AA": "Cash"}
- r21: {"T": "Compare A", "Y": "Actuals", "AA": "Cash"}
- r22: {"T": "Compare B", "Y": "Actuals", "AA": "Cash"}
- r25: {"I": "Published Item", "T": "Formula Components"}
- r26: {"B": "Field", "C": "DR_KPI", "I": "Cash Balance"}
- r27: {"B": "Aggregation", "C": "MTD", "X": "Data Type", "Y": "Scenario", "Z": "Reporting Month"}
- r28: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below --> Red", "F": "If % of change is Above --> Green", "T": "Base", "Y": "Actuals", "AA": "Cash"}
- r30: {"B": "Compare A", "C": "Previous Month", "E": 0.08, "F": 0.09, "T": "Compare A", "AA": "Cash"}
- r31: {"B": "Compare B", "C": "Previous Year", "E": -0.4, "F": -0.38, "T": "Compare B", "AA": "Cash"}
- r33: {"K": "Widget Size:2X5"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at I4 (example `I4`): `=IF(Burn_Rate>0,"Positive CF",Burn_Rate)`
- **F2** at N4 (example `N4`): `=IF(Burn_Rate>0,"∞",Runway)`
- **F3** at U4 (example `U4`): `=C3`
- **F4** at W4 (example `W4`): `=V4`
- **F5** at Z5:Z7, Z28, Z30:Z31 (example `Z5`): `=EOMONTH(DR_DATE_PICKER,IF(C5="Previous Year",-12,IF(C5="Previous Month",-1,0)))`
- **F6** at D6 (example `D6`): `=IF(C4="MTD",(_xldudf_DR_GET(Value_EBITDA,U4,U6,X4,X6,Y4,Y6,Z4,Z6)-_xldudf_DR_GET(Value_EBITDA,V4,V11,X4,X11,Y4,Y11,Z4,Z11))-_xldudf_DR_GET(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V16,W16),X4,X16,Y4,Y16,Z4,Z16),IF(C4="YTD",(_xldudf_DR_YTD(Value_EBITDA,U4,U6,X4,X6,Y4,Y6,Z4,Z6)-_xldudf_DR_YTD(Value_EBITDA,V4,V11,X4,X11,Y4,Y11,Z4,Z11))-_xldudf_DR_YTD(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V16,W16),X4,X16,Y4,Y16,Z4,Z16),IF(C4="QTD",(_xldudf_DR_QTD(Value_EBITDA,U4,U6,X4,X6,Y4,Y6,Z4,Z6)-_xldudf_DR_QTD(Value_EBITDA,V4,V11,X4,X11,Y4,Y11,Z4,Z11))-_xldudf_DR_QTD(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V16,W16),X4,X16,Y4,Y16,Z4,Z16),"Error in Aggregation method")))`
- **F7** at E6 (example `E6`): `=ABS(_xldudf_DR_GET(Value,Y4,Y21,Z4,Z21,AA4,AA21)/D6)`
- **F8** at Y6:Y7, Y11:Y12, Y16:Y17, Y30:Y31 (example `Y6`): `=IF(OR(C6="Budget",C6="Forecast"),C6,"Actuals")`
- **F9** at AA6:AA7 (example `AA6`): `=IF(C6="Forecast",MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12)&"+"&12-MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12),"")`
- **F10** at D7 (example `D7`): `=IF(C4="MTD",(_xldudf_DR_GET(Value_EBITDA,U4,U7,X4,X7,Y4,Y7,Z4,Z7)-_xldudf_DR_GET(Value_EBITDA,V4,V12,X4,X12,Y4,Y12,Z4,Z12))-_xldudf_DR_GET(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V17,W17),X4,X17,Y4,Y17,Z4,Z17),IF(C4="YTD",(_xldudf_DR_YTD(Value_EBITDA,U4,U7,X4,X7,Y4,Y7,Z4,Z7)-_xldudf_DR_YTD(Value_EBITDA,V4,V12,X4,X12,Y4,Y12,Z4,Z12))-_xldudf_DR_YTD(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V17,W17),X4,X17,Y4,Y17,Z4,Z17),IF(C4="QTD",(_xldudf_DR_QTD(Value_EBITDA,U4,U7,X4,X7,Y4,Y7,Z4,Z7)-_xldudf_DR_QTD(Value_EBITDA,V4,V12,X4,X12,Y4,Y12,Z4,Z12))-_xldudf_DR_QTD(Value_EBITDA,V4,_xldudf_DR_INCLUDE(V17,W17),X4,X17,Y4,Y17,Z4,Z17),"Error in Aggregation method")))`
- **F11** at E7 (example `E7`): `=ABS(_xldudf_DR_GET(Value,Y4,Y22,Z4,Z22,AA4,AA22)/D7)`
- **F12** at Z10 (example `Z10`): `=EOMONTH(DR_DATE_PICKER,IF(B5="Previous Year",-12,IF(B5="Previous Month",-1,0)))`
- **F13** at Z11:Z12 (example `Z11`): `=EOMONTH(DR_DATE_PICKER,IF(C6="Previous Year",-12,IF(C6="Previous Month",-1,0)))`
- **F14** at C13 (example `C13`): `=IF(C4="MTD",(_xldudf_DR_GET(Value_CF_KPI,U4,U5,X4,X5,Y4,Y5,Z4,Z5)-_xldudf_DR_GET(Value_CF_KPI,V4,V10,X4,X10,Y4,Y10,Z4,Z10))-_xldudf_DR_GET(Value_CF_KPI,V4,_xldudf_DR_INCLUDE(V15,W15),X4,X15,Y4,Y15,Z4,Z15),IF(C4="YTD",(_xldudf_DR_YTD(Value_CF_KPI,U4,U5,X4,X5,Y4,Y5,Z4,Z5)-_xldudf_DR_YTD(Value_CF_KPI,V4,V10,X4,X10,Y4,Y10,Z4,Z10))-_xldudf_DR_YTD(Value_CF_KPI,V4,_xldudf_DR_INCLUDE(V15,W15),X4,X15,Y4,Y15,Z4,Z15),IF(C4="QTD",(_xldudf_DR_QTD(Value_CF_KPI,U4,U5,X4,X5,Y4,Y5,Z4,Z5)-_xldudf_DR_QTD(Value_CF_KPI,V4,V10,X4,X10,Y4,Y10,Z4,Z10))-_xldudf_DR_QTD(Value_CF_KPI,V4,_xldudf_DR_INCLUDE(V15,W15),X4,X15,Y4,Y15,Z4,Z15),"Error in Aggregation method")))`
- **F15** at C14 (example `C14`): `=ABS(_xldudf_DR_GET(Value,Y4,Y20,Z4,Z20,AA4,AA20)/(I4/IF(C4="MTD",1,IF(C4="QTD",IF(OR(MONTH(DR_DATE_PICKER)-DR_FY_START={0,3,6,9}),1,IF(OR(MONTH(DR_DATE_PICKER)-DR_FY_START={1,4,7,10}),2,3)),MONTH(DR_DATE_PICKER)-DR_FY_START+1))))`
- **F16** at Z15 (example `Z15`): `=EOMONTH(DR_DATE_PICKER,IF(B5="Previous Year",-12,IF(B5="Previous Month",-1,0)))`
- **F17** at Z16:Z17 (example `Z16`): `=EOMONTH(DR_DATE_PICKER,IF(C6="Previous Year",-12,IF(C6="Previous Month",-1,0)))`
- **F18** at Z20 (example `Z20`): `=EOMONTH(DR_DATE_PICKER,IF(B5="Previous Year",-12,IF(B5="Previous Month",-1,0)))`
- **F19** at Z21:Z22 (example `Z21`): `=EOMONTH(DR_DATE_PICKER,IF(C6="Previous Year",-12,IF(C6="Previous Month",-1,0)))`
- **F20** at A26 (example `A26`): `='P&L - A higher result is better'!A19+1`
- **F21** at I27 (example `I27`): `=IF(C27="MTD",_xldudf_DR_GET(Value,AA27,AA28,Y27,Y28,Z27,Z28),IF(C27="YTD",_xldudf_DR_YTD(Value,AA27,AA28,Y27,Y28,Z27,Z28),IF(C27="QTD",_xldudf_DR_QTD(Value,AA27,AA28,Y27,Y28,Z27,Z28))))`
- **F22** at AA27 (example `AA27`): `=C26`
- **F23** at D30 (example `D30`): `=IF(C27="MTD",_xldudf_DR_GET(Value,AA27,AA30,Y27,Y30,Z27,Z30),IF(C27="YTD",_xldudf_DR_YTD(Value,AA27,AA30,Y27,Y30,Z27,Z30),IF(C27="QTD",_xldudf_DR_QTD(Value,AA27,AA30,Y27,Y30,Z27,Z30))))`
- **F24** at J30 (example `J30`): `=IF(I27>D30,List!$D$2,List!$E$2)`
- **F25** at K30 (example `K30`): `=IFERROR((I27-D30)/ABS(D30),"NA")`
- **F26** at L30:L31 (example `L30`): `=LOWER(C30)`
- **F27** at D31 (example `D31`): `=IF(C27="MTD",_xldudf_DR_GET(Value,AA27,AA31,Y27,Y31,Z27,Z31),IF(C27="YTD",_xldudf_DR_YTD(Value,AA27,AA31,Y27,Y31,Z27,Z31),IF(C27="QTD",_xldudf_DR_QTD(Value,AA27,AA31,Y27,Y31,Z27,Z31))))`
- **F28** at J31 (example `J31`): `=IF(I27>D31,List!$D$2,List!$E$2)`
- **F29** at K31 (example `K31`): `=IFERROR((I27-D31)/ABS(D31),"NA")`

## 6. Pictures

None.

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **cell value equal** `"∞"` → fontColor `037C5A` — on N4
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["\"∞\""], "kind": "cellIs", "op": "equal", "priority": 1, "ranges": "N4"}`
- [P2] **text contains** `Positive CF` → fontColor `037C5A` — on I4
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["NOT(ISERROR(SEARCH(\"Positive CF\",I4)))"], "kind": "containsText", "op": "containsText", "priority": 2, "ranges": "I4", "text": "Positive CF"}`
- [P16] **cell value lessThan** `0` → fontColor `BF1D30` — on K30:K31
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["0"], "kind": "cellIs", "op": "lessThan", "priority": 16, "ranges": "K30:K31"}`
- [P17] **cell value equal** `0` → fontColor `FFB800` — on K30:K31
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["0"], "kind": "cellIs", "op": "equal", "priority": 17, "ranges": "K30:K31"}`
- [P18] **cell value greaterThan** `0` → fontColor `037C5A` — on K30:K31
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["0"], "kind": "cellIs", "op": "greaterThan", "priority": 18, "ranges": "K30:K31"}`
- [P34] **icon set `3Triangles`** thresholds [percent 0; percent $E$6; percent $F$6] — on J24
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "percent", "value": "$E$6"}, {"gte": true, "type": "percent", "value": "$F$6"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 34, "ranges": "J24"}`
- [P35] **cell value lessThan** `E23` → fontColor `BF1D30` — on J23
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["E23"], "kind": "cellIs", "op": "lessThan", "priority": 35, "ranges": "J23"}`
- [P36] **cell value between** `E23` and `F23` → fontColor `FFB800` — on J23
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E23", "F23"], "kind": "cellIs", "op": "between", "priority": 36, "ranges": "J23"}`
- [P37] **cell value greaterThan** `F23` → fontColor `037C5A` — on J23
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["F23"], "kind": "cellIs", "op": "greaterThan", "priority": 37, "ranges": "J23"}`
- [P38] **formula** `$J23<$D23` → fontColor `BF1D30` — on I23
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["$J23<$D23"], "kind": "expression", "priority": 38, "ranges": "I23"}`
- [P39] **formula** `AND($J23<$E23,$J23>$D23)` → fontColor `FFB800` — on I23
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["AND($J23<$E23,$J23>$D23)"], "kind": "expression", "priority": 39, "ranges": "I23"}`
- [P40] **formula** `$I23>$E23` → fontColor `037C5A` — on I23
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["$I23>$E23"], "kind": "expression", "priority": 40, "ranges": "I23"}`
- [P210] **formula** `$K30<0` → fontColor `BF1D30` — on J30:J31
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["$K30<0"], "kind": "expression", "priority": 210, "ranges": "J30:J31"}`
- [P211] **formula** `$K$30=0` → fontColor `FFB800` — on J30:J31
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["$K$30=0"], "kind": "expression", "priority": 211, "ranges": "J30:J31"}`
- [P212] **formula** `$K30>0` → fontColor `037C5A` — on J30:J31
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["$K30>0"], "kind": "expression", "priority": 212, "ranges": "J30:J31"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## 9. Known gaps in the official template (read before building)

- The data-validation dropdowns in §1 read from a sheet named `List` that is **not part of this template**, and some of them point at
  `List!#REF!`, which is broken in the template itself. If the workbook already has a `List` sheet, apply the validations that point
  at real ranges; otherwise build the sheet without them and say so. Do not recreate the `#REF!` ones.
- A defined name in §1 can point at another sheet of this workbook (for example `FY_Start`). Define it on the sheet you built, or skip
  it, and say which.

## Template defect (read before building)

`E6` and `E7` divide by `D6` / `D7` without a zero guard, so a legitimate zero shows `#DIV/0!`. Wrap them: `=IFERROR(ABS(<the template expression>/D6),0)` (and `D7` for `E7`).
