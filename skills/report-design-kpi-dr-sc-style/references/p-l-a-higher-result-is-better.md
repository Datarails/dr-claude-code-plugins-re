# Spec: kpi-dr-sc-style → sheet "P&L - A higher result is better"

> Source: KPIs for Dashboard — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:Z38`; Everything beyond it is hidden (columns after Z, rows after 38). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 14.5 pt (unlisted rows visible) |
| Used range | A1:AA39 |
| Merged ranges | B13:C13, B21:C21, B5:C5, H10:L10, H12:L13, H18:L18, H20:L21, H2:L2, H4:L5, K15:L15, K16:L16, K23:L23, K24:L24, K7:L7, K8:L8, N10:S10, N18:S18, N2:S2 |
| Data validation | `C4 C12 C20` list `List!$A$2:$A$4` |
| Data validation | `C7:C9 C15:C17 C23:C25 D9 D17 D25` list `List!$B$2:$B$5` |
| Data validation | `E4:F4 E12:F12 E20:F20` list `List!#REF!` |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `FY_Start` | `'P&L - A higher result is better'!$B$2` |
| Defined name `Value` | `"widget_19324_0_tt_1786512183639.7"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.29 | 26.2 |  |
| B | 15.29 | 84.0 |  |
| C | 26.29 | 141.8 |  |
| D | 14.71 | 81.0 |  |
| E | 18.57 | 101.2 |  |
| F | 15.71 | 86.2 |  |
| G | 9.71 | 54.8 |  |
| H | 1.57 | 12.0 |  |
| I | 2.57 | 17.2 |  |
| J:K | 8.57 | 48.8 |  |
| L | 16.57 | 90.8 |  |
| M | 4.43 | 27.0 |  |
| N | 11.14 | 62.2 |  outline 1 |
| O | 24.00 | 129.8 |  outline 1 |
| P | 8.71 | 49.5 |  outline 1 |
| Q | 10.29 | 57.8 |  outline 1 |
| R | 13.29 | 73.5 |  outline 1 |
| S | 13.29 | 73.5 |  outline 1 |
| U:V | 10.71 | 60.0 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 11.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S2 | Calibri | 11.0 | B | 000000 | E7F4FF | – | `–` | – | – | – | – |
| S3 | Calibri | 11.0 |  | 000000 | E7F4FF | – | `–` | – | – | – | – |
| S4 | Calibri | 11.0 | B | FFA500 | – | – | `–` | – | – | – | – |
| S5 | Calibri | 11.0 |  | 000000 | – | B:thin:auto | `–` | – | – | – | – |
| S6 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | – | `[$-409]mmm\-yy;@` | center | center | – | – |
| S7 | Calibri | 11.0 | B | 000000 | – | – | `mm-dd-yy` | – | – | – | – |
| S8 | Calibri | 11.0 |  | 000000 | – | R:thin:auto | `–` | – | – | – | – |
| S9 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S10 | Calibri | 11.0 |  | 000000 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S11 | Calibri | 11.0 | B | 7FFFD4 | – | L:thin:auto | `–` | – | – | – | – |
| S12 | Calibri | 11.0 | B | 7FFFD4 | FFFFFF | – | `–` | – | – | – | – |
| S13 | Calibri | 11.0 |  | 000000 | FFFFFF | – | `–` | – | – | – | – |
| S14 | Calibri | 11.0 | B | 000000 | FFFFFF | – | `–` | left | center | – | – |
| S15 | Calibri | 11.0 | B | 000000 | – | – | `–` | – | – | – | – |
| S16 | Calibri | 11.0 |  | 000000 | – | R:thin:auto | `0.00` | – | – | – | – |
| S17 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S18 | Calibri | 11.0 |  | 000000 | FFFFFF | B:thin:auto | `–` | – | – | – | – |
| S19 | Poppins | 32.0 | B | 333333 | FFFFFF | – | `#,##0,\ "K"` | left | top | 1.0 | – |
| S20 | Calibri | 9.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S21 | Calibri | 9.0 | B | 000000 | – | – | `–` | – | – | – | – |
| S22 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S23 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S24 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S25 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto | `–` | – | – | – | – |
| S26 | Calibri | 9.0 |  | 000000 | – | – | `mm-dd-yy` | – | – | – | – |
| S27 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S28 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S29 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S30 | Poppins | 30.0 | B | 000000 | FFFFFF | – | `#,##0,\ "K"` | left | center | – | – |
| S31 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S32 | Calibri | 11.0 |  | 000000 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `0%` | – | – | – | – |
| S33 | Calibri | 11.0 |  | 000000 | – | L:thin:auto | `–` | – | – | – | – |
| S34 | Wingdings 3 | 14.0 |  | 037C5A | FFFFFF | – | `0%` | center | top | – | – |
| S35 | Poppins | 12.0 | B | 037C5A | FFFFFF | – | `0%` | center | center | – | – |
| S36 | Poppins | 12.0 |  | 333333 | FFFFFF | – | `–` | left | center | – | – |
| S37 | Calibri | 12.0 |  | 000000 | FFFFFF | – | `–` | left | center | – | – |
| S38 | Calibri | 9.0 |  | 000000 | – | – | `–` | right | – | – | – |
| S39 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S40 | Wingdings 3 | 14.0 |  | C00000 | FFFFFF | – | `0%` | center | top | – | – |
| S41 | Poppins | 12.0 | B | C00000 | FFFFFF | – | `0%` | center | center | – | – |
| S42 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `–` | – | – | – | – |
| S43 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `0%` | – | – | – | – |
| S44 | Calibri | 11.0 |  | 000000 | FFFFFF | – | `–` | – | center | – | – |
| S45 | Calibri | 8.0 |  | C00000 | FFFFFF | – | `0%` | – | center | – | – |
| S46 | Calibri | 8.0 |  | 000000 | FFFFFF | – | `–` | left | center | – | – |
| S47 | Calibri | 11.0 |  | 000000 | – | – | `0.00000` | – | – | – | – |
| S48 | Calibri | 40.0 | B | 000000 | – | – | `#,##0,\ "K"` | left | – | 1.0 | – |
| S49 | Calibri | 12.0 |  | 000000 | FFFFFF | – | `–` | left | center | 1.0 | – |
| S50 | Calibri | 9.0 |  | 000000 | – | – | `–` | center | – | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=14.5 rows 1: A=S1 B=S2 C=S3 D:U=S1 V=S4 W:Z=S1
- **T2** h=16.15 rows 2: A=S1 B:C=S5 D:G=S1 H:L=S6 M=S1 N:S=S6 T:U=S1 V=S7 W:Z=S1
- **T3** h=14.5 rows 3: A=S8 B=S9 C=S10 D=S11 E=S12 F:G=S13 H=S14 I:Y=S1 Z=S15
- **T4** h=12.0 rows 4: A=S16 B=S9 C=S10 D=S17 E:F=S18 G=S13 H:L=S19 M=S1 N=S20 O:T=S21 U:Z=S1
- **T5** h=32.15 rows 5: A=S8 B:C=S22 D=S23 E:F=S24 G=S25 H:L=S19 M=S1 N=S21 O:Q=S20 R=S26 S:T=S20 U:Z=S1
- **T6** h=8.15 rows 6: A=S1 B:C=S27 D=S28 E:F=S29 G=S13 H:L=S30 M=S1 N=S21 O:Q=S20 R=S26 S:T=S20 U:Z=S1
- **T7** h=20.15 rows 7: A=S8 B:C=S9 D=S31 E:F=S32 G=S33 H=S1 I=S34 J=S35 K:L=S36 M=S37 N=S21 O:Q=S20 R=S26 S=S38 T=S20 U:Z=S1
- **T8** h=20.15 rows 8: A=S8 B:C=S9 D=S39 E:F=S32 G=S33 H=S1 I=S40 J=S41 K:L=S36 M=S37 N=S21 O:Q=S20 R=S26 S=S38 T=S20 U:Z=S1
- **T9** h=14.5 rows 9: A=S1 B:D=S42 E:F=S43 G=S13 H:I=S44 J=S45 K=S46 L=S44 M:T=S1 U=S15 V:X=S1 Y=S47 Z=S1
- **T10** h=16.15 rows 10,18: A=S1 B:C=S5 D:G=S1 H:L=S6 M=S1 N:S=S6 T:Z=S1
- **T11** h=14.5 rows 11,19: A=S8 B=S9 C=S10 D=S33 E:G=S13 H=S14 I:Z=S1
- **T12** h=12.0 rows 12,20: A=S8 B=S9 C=S10 D=S17 E:F=S18 G=S13 H:L=S19 M=S1 N=S20 O:T=S21 U:Z=S1
- **T13** h=30.0 rows 13,21: A=S8 B:C=S22 D=S23 E:F=S24 G=S25 H:L=S19 M=S1 N=S21 O:Q=S20 R=S26 S:T=S20 U:Z=S1
- **T14** h=8.15 rows 14,22: A=S1 B:C=S27 D=S28 E:F=S29 G=S1 H:L=S48 M=S1 N=S21 O:Q=S20 R=S26 S:T=S20 U:Z=S1
- **T15** h=20.15 rows 15,23: A=S8 B:C=S9 D=S31 E:F=S32 G=S33 H=S1 I=S34 J=S35 K:L=S36 M=S49 N=S21 O:Q=S20 R=S26 S=S38 T=S20 U:Z=S1
- **T16** h=20.15 rows 16: A=S8 B:C=S9 D=S39 E:F=S32 G=S33 H=S1 I=S40 J=S41 K:L=S36 M=S49 N=S21 O:Q=S20 R=S26 S=S38 T=S20 U:Z=S1
- **T17** h=14.5 rows 17,25: A=S1 B:D=S42 E:F=S43 G=S13 H:I=S44 J=S45 K=S46 L=S44 M:Z=S1
- **T18** h=20.15 rows 24: A=S8 B:C=S9 D=S39 E:F=S32 G=S33 H=S1 I=S34 J=S35 K:L=S36 M=S49 N=S21 O:Q=S20 R=S26 S=S50 T=S20 U:Z=S1
- **T19** h=None rows 26-28,31-37: A:Z=S1
- **T20** h=36.75 rows 29: A:S=S1 T=S21 U:Z=S1
- **T21** h=22.5 rows 30: A:Z=S1
- **T22** h=14.5 rows 38: A:Z=S1

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r1: {"B": "Fill in Cells", "V": "Date Picker"}
- r2: {"B": 1, "H": "Published Item", "N": "Formula Components"}
- r3: {"A": 1, "B": "Field", "C": "Account Group L2"}
- r4: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r5: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below --> Red", "F": "If % of change is Above --> Green", "N": "Base", "O": "Income", "P": "Activity", "Q": "Actuals"}
- r7: {"B": "Compare A", "C": "Previous Month", "E": -0.05, "F": 0.05, "N": "Compare A", "O": "Income", "P": "Activity"}
- r8: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1, "N": "Compare B", "O": "Income", "P": "Activity"}
- r10: {"H": "Published Item", "N": "Formula Components"}
- r11: {"B": "Field", "C": "Account Group L1"}
- r12: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r13: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below --> Red", "F": "If % of change is Above --> Green", "N": "Base", "O": "Net_Income", "P": "Activity", "Q": "Actuals"}
- r15: {"B": "Compare A", "C": "Previous Month", "E": -0.05, "F": 0.05, "N": "Compare A", "O": "Net_Income", "P": "Activity"}
- r16: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1, "N": "Compare B", "O": "Net_Income", "P": "Activity"}
- r18: {"H": "Published Item", "N": "Formula Components"}
- r19: {"B": "Field", "C": "Account Group L2"}
- r20: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r21: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below --> Red", "F": "If % of change is Above --> Green", "N": "Base", "O": "Operating Profit", "P": "Activity", "Q": "Actuals"}
- r23: {"B": "Compare A", "C": "Previous Month", "E": 0.08, "F": 0.09, "N": "Compare A", "O": "Operating Profit", "P": "Activity"}
- r24: {"B": "Compare B", "C": "Forecast", "E": -0.4, "F": -0.38, "N": "Compare B", "O": "Operating Profit", "P": "Activity"}
- r38: {"Z": "name: cells_DR_PUBv2__1678796143, id: 13921"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at V2 (example `V2`): `=DR_DATE_PICKER`
- **F2** at H3 (example `H3`): `=IF(C4="MTD","Income","Income"&" "&C4)`
- **F3** at H4, H12, H20 (example `H4`): `=IF(C4="MTD",_xldudf_DR_GET(Value,O4,O5,P4,P5,Q4,Q5,R4,R5),IF(C4="YTD",_xldudf_DR_YTD(Value,O4,O5,P4,P5,Q4,Q5,R4,R5),IF(C4="QTD",_xldudf_DR_QTD(Value,O4,O5,P4,P5,Q4,Q5,R4,R5),"Error in Aggregation method")))`
- **F4** at O4, O12, O20 (example `O4`): `=C3`
- **F5** at R5, R7:R8 (example `R5`): `=EOMONTH(DR_DATE_PICKER,IF(C5="Previous Year",-12,IF(C5="Previous Month",-1,0)))`
- **F6** at D7, D15, D23 (example `D7`): `=IF(C4="MTD",IF(C7="Forecast",_xldudf_DR_GET(Value,O4,O7,P4,P7,Q4,Q7,R4,R7,S4,S7),_xldudf_DR_GET(Value,O4,O7,P4,P7,Q4,Q7,R4,R7)),IF(C4="YTD",IF(C7="Forecast",_xldudf_DR_GET(Value,O4,O7,P4,P7,Q4,Q7,R4,R7,S4,S7)+IF(S7="0+12",0,_xldudf_DR_YTD(Value,O4,O7,P4,P7,Q4,"Actuals",R4,EOMONTH(R7,-1))),_xldudf_DR_YTD(Value,O4,O7,P4,P7,Q4,Q7,R4,R7)),IF(C4="QTD",IF(C7="Forecast",_xldudf_DR_GET(Value,O4,O7,P4,P7,Q4,Q7,R4,R7,S4,S7)+IF(MOD(LEFT(S7,FIND("+",S7,1)-1),3)=0,0,_xldudf_DR_QTD(Value,O4,O7,P4,P7,Q4,"Actuals",R4,EOMONTH(R7,-1))),_xldudf_DR_QTD(Value,O4,O7,P4,P7,Q4,Q7,R4,R7)),"Error in Aggregation method")))`
- **F7** at I7, I15, I23 (example `I7`): `=IF(H4>D7,List!$D$2,List!$E$2)`
- **F8** at J7, J15, J23 (example `J7`): `=IFERROR((H4-D7)/ABS(D7),"NA")`
- **F9** at K7:K8, K15:K16, K23:K24 (example `K7`): `=LOWER(C7)`
- **F10** at Q7:Q8, Q15:Q16, Q23:Q24 (example `Q7`): `=IF(OR(C7="Budget",C7="Forecast"),C7,"Actuals")`
- **F11** at S7:S8, S15:S16, S23:S24 (example `S7`): `=IF(C7="Forecast",MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12)&"+"&12-MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12),"")`
- **F12** at D8, D16, D24 (example `D8`): `=IF(C4="MTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O4,O8,P4,P8,Q4,Q8,R4,R8,S4,S8),_xldudf_DR_GET(Value,O4,O8,P4,P8,Q4,Q8,R4,R8)),IF(C4="YTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O4,O8,P4,P8,Q4,Q8,R4,R8,S4,S8)+IF(S8="0+12",0,_xldudf_DR_YTD(Value,O4,O8,P4,P8,Q4,"Actuals",R4,EOMONTH(R8,-1))),_xldudf_DR_YTD(Value,O4,O8,P4,P8,Q4,Q8,R4,R8)),IF(C4="QTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O4,O8,P4,P8,Q4,Q8,R4,R8,S4,S8)+IF(MOD(LEFT(S8,FIND("+",S8,1)-1),3)=0,0,_xldudf_DR_QTD(Value,O4,O8,P4,P8,Q4,"Actuals",R4,EOMONTH(R8,-1))),_xldudf_DR_QTD(Value,O4,O8,P4,P8,Q4,Q8,R4,R8)),"Error in Aggregation method")))`
- **F13** at I8, I16, I24 (example `I8`): `=IF(H4>D8,List!$D$2,List!$E$2)`
- **F14** at J8, J16, J24 (example `J8`): `=IFERROR((H4-D8)/ABS(D8),"NA")`
- **F15** at A11 (example `A11`): `=A3+1`
- **F16** at H11 (example `H11`): `=IF(C12="MTD","Net Income","Net Income"&" "&C12)`
- **F17** at R13, R15:R16, R21, R23:R24 (example `R13`): `=EOMONTH(DR_DATE_PICKER,_xlfn.SWITCH(C13,"Previous Year",-12,"Previous Month",-1,0))`
- **F18** at H19 (example `H19`): `=IF(C20="MTD","Operating Profit","Operating Profit"&" "&C20)`

## 6. Pictures

None.

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **cell value lessThan** `E15` → fontColor `BF1D30` — on J15
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["E15"], "kind": "cellIs", "op": "lessThan", "priority": 1, "ranges": "J15"}`
- [P2] **cell value between** `E15` and `F15` → fontColor `FFB800` — on J15
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E15", "F15"], "kind": "cellIs", "op": "between", "priority": 2, "ranges": "J15"}`
- [P3] **cell value greaterThan** `F15` → fontColor `037C5A` — on J15
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["F15"], "kind": "cellIs", "op": "greaterThan", "priority": 3, "ranges": "J15"}`
- [P7] **cell value lessThan** `F23` → fontColor `BF1D30` — on J23:J24
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["F23"], "kind": "cellIs", "op": "lessThan", "priority": 7, "ranges": "J23:J24"}`
- [P8] **cell value between** `F23` and `G23` → fontColor `FFB800` — on J23:J24
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["F23", "G23"], "kind": "cellIs", "op": "between", "priority": 8, "ranges": "J23:J24"}`
- [P9] **cell value greaterThan** `G23` → fontColor `037C5A` — on J23:J24
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["G23"], "kind": "cellIs", "op": "greaterThan", "priority": 9, "ranges": "J23:J24"}`
- [P16] **cell value lessThan** `F16` → fontColor `BF1D30` — on J16
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["F16"], "kind": "cellIs", "op": "lessThan", "priority": 16, "ranges": "J16"}`
- [P17] **cell value between** `F16` and `G16` → fontColor `FFB800` — on J16
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["F16", "G16"], "kind": "cellIs", "op": "between", "priority": 17, "ranges": "J16"}`
- [P18] **cell value greaterThan** `G16` → fontColor `037C5A` — on J16
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["G16"], "kind": "cellIs", "op": "greaterThan", "priority": 18, "ranges": "J16"}`
- [P79] **icon set `3Triangles`** thresholds [percent 0; percent $E$7; percent $F$7] — on J9 J17 J25
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "percent", "value": "$E$7"}, {"gte": true, "type": "percent", "value": "$F$7"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 79, "ranges": "J9 J17 J25"}`
- [P141] **cell value lessThan** `E7` → fontColor `BF1D30` — on J7:J8
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["E7"], "kind": "cellIs", "op": "lessThan", "priority": 141, "ranges": "J7:J8"}`
- [P142] **cell value between** `E7` and `F7` → fontColor `FFB800` — on J7:J8
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E7", "F7"], "kind": "cellIs", "op": "between", "priority": 142, "ranges": "J7:J8"}`
- [P143] **cell value greaterThan** `F7` → fontColor `037C5A` — on J7:J8
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["F7"], "kind": "cellIs", "op": "greaterThan", "priority": 143, "ranges": "J7:J8"}`
- [P203] **formula** `$J7<$E7` → fontColor `BF1D30` — on I7:I8
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["$J7<$E7"], "kind": "expression", "priority": 203, "ranges": "I7:I8"}`
- [P204] **formula** `AND($J7<$F7,$J7>$E7)` → fontColor `FFB800` — on I7:I8
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["AND($J7<$F7,$J7>$E7)"], "kind": "expression", "priority": 204, "ranges": "I7:I8"}`
- [P205] **formula** `$I7>$F7` → fontColor `037C5A` — on I7:I8
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["$I7>$F7"], "kind": "expression", "priority": 205, "ranges": "I7:I8"}`
- [P208] **formula** `$I15<$E15` → fontColor `BF1D30` — on I15:I16 I23:I24
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["$I15<$E15"], "kind": "expression", "priority": 208, "ranges": "I15:I16 I23:I24"}`
- [P209] **formula** `AND($I15<$F15,$I15>$E15)` → fontColor `FFB800` — on I15:I16 I23:I24
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["AND($I15<$F15,$I15>$E15)"], "kind": "expression", "priority": 209, "ranges": "I15:I16 I23:I24"}`
- [P210] **formula** `$J$16>0` → fontColor `037C5A` — on I15:I16 I23:I24
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["$J$16>0"], "kind": "expression", "priority": 210, "ranges": "I15:I16 I23:I24"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## 9. Known gaps in the official template (read before building)

- The data-validation dropdowns in §1 read from a sheet named `List` that is **not part of this template**, and some of them point at
  `List!#REF!`, which is broken in the template itself. If the workbook already has a `List` sheet, apply the validations that point
  at real ranges; otherwise build the sheet without them and say so. Do not recreate the `#REF!` ones.
- A defined name in §1 can point at another sheet of this workbook (for example `FY_Start`). Define it on the sheet you built, or skip
  it, and say which.

## Template defect in the status colours (read before building)

In the higher-is-better sheet, the red / amber / green font rules of the status cells in column `I` mix the status cell with the percentage result in column `J` (and the green rule of the Operating Profit block is fixed to `$J$16`). Apply them against the row's own result in `J` instead: red `$J<row><$E<row>`, amber `AND($J<row><$F<row>,$J<row>>$E<row>)`, green `$J<row>>$F<row>`, for every `I` range listed (first row of each range as `<row>`). Tell the user you corrected it.
