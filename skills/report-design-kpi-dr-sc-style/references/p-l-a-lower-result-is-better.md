# Spec: kpi-dr-sc-style → sheet "P&L - A lower result is better"

> Source: KPIs for Dashboard — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:S28`; Everything beyond it is hidden (columns after S, rows after 28). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 14.5 pt (unlisted rows visible) |
| Used range | A1:T33 |
| Merged ranges | B16:C16, B25:C25, B6:C6, H11:L11, H15:L16, H21:L21, H25:L25, H2:L2, H6:L6, K18:L18, K19:L19, K27:L27, K28:L28, K8:L8, K9:L9, N11:S11, N21:S21, N2:S2 |
| Data validation | `E14:F15 E24:F24` list `List!#REF!` |
| Data validation | `C8:C10 C18:C20 C27:C28 D10 D20` list `List!$B$2:$B$5` |
| Data validation | `C5 C14:C15 C24` list `List!$A$2:$A$4` |
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
| E | 21.86 | 118.5 |  |
| F | 20.14 | 109.5 |  |
| G | 9.71 | 54.8 |  |
| H | 1.57 | 12.0 |  |
| I | 2.57 | 17.2 |  |
| J | 8.57 | 48.8 |  |
| K | 8.57 | 48.8 |  |
| L | 16.57 | 90.8 |  |
| M | 4.43 | 27.0 |  |
| N | 11.14 | 62.2 |  outline 1 |
| O | 10.86 | 60.8 |  outline 1 |
| P | 8.71 | 49.5 |  outline 1 |
| Q | 10.29 | 57.8 |  outline 1 |
| R | 13.29 | 73.5 |  outline 1 |
| S | 8.71 | 49.5 |  outline 1 |

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
| S9 | Calibri | 11.0 |  | 000000 | – | L:thin:auto | `–` | – | – | – | – |
| S10 | Calibri | 11.0 |  | 000000 | FFFFFF | – | `–` | – | – | – | – |
| S11 | Calibri | 11.0 | B | 000000 | FFFFFF | B:medium:E7E6E6 | `–` | left | – | 1.0 | – |
| S12 | Calibri | 11.0 | B | 000000 | FFFFFF | B:medium:E7E6E6 | `–` | center | center | – | – |
| S13 | Calibri | 11.0 |  | 000000 | FFFFFF | B:medium:E7E6E6 | `–` | right | – | – | – |
| S14 | Calibri | 11.0 |  | 000000 | FFFFFF | B:medium:E7E6E6 | `–` | – | – | – | – |
| S15 | Calibri | 11.0 |  | 000000 | – | L:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S16 | Calibri | 11.0 |  | 000000 | FFFFFF | B:thin:auto | `–` | – | – | – | – |
| S17 | Calibri | 11.0 |  | 000000 | FFFFFF | T:medium:E7E6E6 | `–` | – | – | – | – |
| S18 | Calibri | 11.0 |  | 000000 | FFFFFF | T:medium:E7E6E6 | `–` | center | center | – | – |
| S19 | Calibri | 11.0 |  | 000000 | FFFFFF | T:medium:E7E6E6 | `–` | right | – | – | – |
| S20 | Calibri | 9.0 |  | 000000 | – | – | `–` | – | – | – | – |
| S21 | Calibri | 9.0 | B | 000000 | – | – | `–` | – | – | – | – |
| S22 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S23 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S24 | Calibri | 11.0 | B | FFFFFF | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S25 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto | `–` | – | – | – | – |
| S26 | Poppins | 32.0 | B | 333333 | FFFFFF | – | `#,##0,\ "K"` | left | top | 1.0 | – |
| S27 | Calibri | 9.0 |  | 000000 | – | – | `mm-dd-yy` | – | – | – | – |
| S28 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S29 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S30 | Calibri | 11.0 | B | FFFFFF | – | T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S31 | Calibri | 40.0 | B | 000000 | – | – | `#,##0,\ "K"` | left | – | 1.0 | – |
| S32 | Calibri | 11.0 |  | 000000 | FFFFFF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S33 | Calibri | 11.0 |  | 000000 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `0%` | – | – | – | – |
| S34 | Wingdings 3 | 14.0 |  | C00000 | FFFFFF | – | `0%` | center | top | – | – |
| S35 | Poppins | 12.0 | B | C00000 | FFFFFF | – | `0%` | center | center | – | – |
| S36 | Poppins | 12.0 |  | 333333 | FFFFFF | – | `–` | left | center | – | – |
| S37 | Calibri | 9.0 |  | 000000 | – | – | `–` | right | – | – | – |
| S38 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `–` | – | – | – | – |
| S39 | Calibri | 11.0 |  | 000000 | FFFFFF | T:thin:auto | `0%` | – | – | – | – |
| S40 | Calibri | 11.0 |  | 000000 | FFFFFF | – | `–` | center | center | – | – |
| S41 | Calibri | 8.0 |  | C00000 | FFFFFF | – | `0%` | right | – | – | – |
| S42 | Calibri | 8.0 |  | 000000 | FFFFFF | – | `–` | left | – | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=14.5 rows 1: A=S1 B=S2 C=S3 D:S=S1
- **T2** h=16.15 rows 2: A=S1 B:C=S4 D:G=S1 H:L=S5 M=S1 N:S=S5
- **T3** h=14.5 rows 3,12,22: A=S6 B=S7 C=S8 D=S9 E:G=S10 H:S=S1
- **T4** h=15.0 rows 4,13,23: A=S6 B=S7 C=S8 D=S9 E:G=S10 H=S11 I=S12 J=S13 K:L=S14 M:S=S1
- **T5** h=14.5 rows 5,24: A=S6 B=S7 C=S8 D=S15 E:F=S16 G=S10 H=S17 I=S18 J=S19 K:L=S17 M=S1 N=S20 O:S=S21
- **T6** h=43.4 rows 6: A=S6 B:C=S22 D=S23 E:F=S24 G=S25 H:L=S26 M=S1 N=S21 O:Q=S20 R=S27 S=S20
- **T7** h=8.15 rows 7,17,26: A=S1 B:C=S28 D=S29 E:F=S30 G=S1 H:L=S31 M=S1 N=S21 O:Q=S20 R=S27 S=S20
- **T8** h=20.15 rows 8-9,18-19,27-28: A=S6 B:C=S7 D=S32 E:F=S33 G=S9 H=S1 I=S34 J=S35 K:L=S36 M=S1 N=S21 O:Q=S20 R=S27 S=S37
- **T9** h=14.5 rows 10,20: A=S1 B:D=S38 E:F=S39 G:H=S10 I=S40 J=S41 K=S42 L=S10 M:S=S1
- **T10** h=14.5 rows 11,21: A=S1 B:C=S4 D:G=S1 H:L=S5 M=S1 N:S=S5
- **T11** h=14.5 rows 14: A=S6 B=S7 C=S8 D=S9 E:G=S10 H=S17 I=S18 J=S19 K:L=S17 M=S1 N=S20 O:S=S21
- **T12** h=12.0 rows 15: A=S6 B=S7 C=S8 D=S15 E:F=S16 G=S10 H:L=S26 M=S1 N=S20 O:S=S21
- **T13** h=30.0 rows 16: A=S6 B:C=S22 D=S23 E:F=S24 G=S25 H:L=S26 M=S1 N=S21 O:Q=S20 R=S27 S=S20
- **T14** h=61.5 rows 25: A=S6 B:C=S22 D=S23 E:F=S24 G=S25 H:L=S26 M=S1 N=S21 O:Q=S20 R=S27 S=S20

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r1: {"B": "Fill in Cells"}
- r2: {"B": 1, "H": "Published Item", "N": "Formula Components"}
- r3: {"A": 1, "B": "Field", "C": "Account Group L2"}
- r4: {"B": "Field Value", "C": "Cost of Goods Sold"}
- r5: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r6: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below this then color in Green", "F": "If % of change is above this then color in Red", "N": "Base", "P": "Activity", "Q": "Actuals"}
- r8: {"B": "Compare A", "C": "Previous Month", "E": -0.02, "F": 0.02, "N": "Compare A", "P": "Activity"}
- r9: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1, "N": "Compare B", "P": "Activity"}
- r11: {"H": "Published Item", "N": "Formula Components"}
- r12: {"B": "Field", "C": "Account Group L2"}
- r13: {"B": "Field Value", "C": "Operating Expense"}
- r14: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r16: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below this then color in Green", "F": "If % of change is above this then color in Red", "N": "Base", "P": "Activity", "Q": "Actuals"}
- r18: {"B": "Compare A", "C": "Previous Month", "E": -0.05, "F": 0.05, "N": "Compare A", "P": "Activity"}
- r19: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1, "N": "Compare B", "P": "Activity"}
- r21: {"H": "Published Item", "N": "Formula Components"}
- r22: {"B": "Field", "C": "Account Group L1"}
- r23: {"B": "Field Value", "C": "EXPENSE"}
- r24: {"B": "Aggregation", "C": "YTD", "P": "Data Type", "Q": "Scenario", "R": "Reporting Month", "S": "System_Forecast"}
- r25: {"B": "Compare Analysis", "D": "Compare Result", "E": "If % of change is below this then color in Green", "F": "If % of change is above this then color in Red", "N": "Base", "P": "Activity", "Q": "Actuals"}
- r27: {"B": "Compare A", "C": "Previous Month", "E": -0.05, "F": 0.05, "N": "Compare A", "P": "Activity"}
- r28: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1, "N": "Compare B", "P": "Activity"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at H4, H13, H23 (example `H4`): `=IF(C5="MTD",C4,C4&" "&C5)`
- **F2** at O5:O6, O14, O24:O25 (example `O5`): `=C3`
- **F3** at H6, H25 (example `H6`): `=IF(C5="MTD",_xldudf_DR_GET(Value,O5,O6,P5,P6,Q5,Q6,R5,R6),IF(C5="YTD",_xldudf_DR_YTD(Value,O5,O6,P5,P6,Q5,Q6,R5,R6),IF(C5="QTD",_xldudf_DR_QTD(Value,O5,O6,P5,P6,Q5,Q6,R5,R6),"Error in Aggregation method")))`
- **F4** at R6, R8:R9, R16, R18:R19, R25, R27:R28 (example `R6`): `=EOMONTH(DR_DATE_PICKER,IF(C6="Previous Year",-12,IF(C6="Previous Month",-1,0)))`
- **F5** at D8, D27 (example `D8`): `=IF(C5="MTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O5,O8,P5,P8,Q5,Q8,R5,R8,S5,S8),_xldudf_DR_GET(Value,O5,O8,P5,P8,Q5,Q8,R5,R8)),IF(C5="YTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O5,O8,P5,P8,Q5,Q8,R5,R8,S5,S8)+IF(S8="0+12",0,_xldudf_DR_YTD(Value,O5,O8,P5,P8,Q5,"Actuals",R5,EOMONTH(R8,-1))),_xldudf_DR_YTD(Value,O5,O8,P5,P8,Q5,Q8,R5,R8)),IF(C5="QTD",IF(C8="Forecast",_xldudf_DR_GET(Value,O5,O8,P5,P8,Q5,Q8,R5,R8,S5,S8)+IF(MOD(LEFT(S8,FIND("+",S8,1)-1),3)=0,0,_xldudf_DR_QTD(Value,O5,O8,P5,P8,Q5,"Actuals",R5,EOMONTH(R8,-1))),_xldudf_DR_QTD(Value,O5,O8,P5,P8,Q5,Q8,R5,R8)),"Error in Aggregation method")))`
- **F6** at I8, I27 (example `I8`): `=IF(H6>D8,List!$D$2,List!$E$2)`
- **F7** at J8, J27 (example `J8`): `=IFERROR((H6-D8)/ABS(D8),"NA")`
- **F8** at K8:K9, K18:K19, K27:K28 (example `K8`): `=LOWER(C8)`
- **F9** at O8, O27 (example `O8`): `=C4`
- **F10** at Q8:Q9, Q18:Q19, Q27:Q28 (example `Q8`): `=IF(OR(C8="Budget",C8="Forecast"),C8,"Actuals")`
- **F11** at S8:S9, S18:S19, S27:S28 (example `S8`): `=IF(C8="Forecast",MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12)&"+"&12-MOD(MONTH(EOMONTH(DR_DATE_PICKER,0))-FY_Start,12),"")`
- **F12** at D9, D18, D28 (example `D9`): `=IF(C5="MTD",IF(C9="Forecast",_xldudf_DR_GET(Value,O5,O9,P5,P9,Q5,Q9,R5,R9,S5,S9),_xldudf_DR_GET(Value,O5,O9,P5,P9,Q5,Q9,R5,R9)),IF(C5="YTD",IF(C9="Forecast",_xldudf_DR_GET(Value,O5,O9,P5,P9,Q5,Q9,R5,R9,S5,S9)+IF(S9="0+12",0,_xldudf_DR_YTD(Value,O5,O9,P5,P9,Q5,"Actuals",R5,EOMONTH(R9,-1))),_xldudf_DR_YTD(Value,O5,O9,P5,P9,Q5,Q9,R5,R9)),IF(C5="QTD",IF(C9="Forecast",_xldudf_DR_GET(Value,O5,O9,P5,P9,Q5,Q9,R5,R9,S5,S9)+IF(MOD(LEFT(S9,FIND("+",S9,1)-1),3)=0,0,_xldudf_DR_QTD(Value,O5,O9,P5,P9,Q5,"Actuals",R5,EOMONTH(R9,-1))),_xldudf_DR_QTD(Value,O5,O9,P5,P9,Q5,Q9,R5,R9)),"Error in Aggregation method")))`
- **F13** at I9, I18, I28 (example `I9`): `=IF(H6>D9,List!$D$2,List!$E$2)`
- **F14** at J9, J18, J28 (example `J9`): `=IFERROR((H6-D9)/ABS(D9),"NA")`
- **F15** at O9, O18, O28 (example `O9`): `=C4`
- **F16** at A12 (example `A12`): `=A3+1`
- **F17** at H15 (example `H15`): `=IF(C14="MTD",_xldudf_DR_GET(Value,O14,O16,P14,P16,Q14,Q16,R14,R16),IF(C14="YTD",_xldudf_DR_YTD(Value,O14,O16,P14,P16,Q14,Q16,R14,R16),IF(C14="QTD",_xldudf_DR_QTD(Value,O14,O16,P14,P16,Q14,Q16,R14,R16),"Error in Aggregation method")))`
- **F18** at O16 (example `O16`): `=C13`
- **F19** at D19 (example `D19`): `=IF(C14="MTD",IF(C19="Forecast",_xldudf_DR_GET(Value,O14,O19,P14,P19,Q14,Q19,R14,R19,S14,S19),_xldudf_DR_GET(Value,O14,O19,P14,P19,Q14,Q19,R14,R19)),IF(C14="YTD",IF(C19="Forecast",_xldudf_DR_GET(Value,O14,O19,P14,P19,Q14,Q19,R14,R19,S14,S19)+IF(S19="0+12",0,_xldudf_DR_YTD(Value,O14,O19,P14,P19,Q14,"Actuals",R14,EOMONTH(R19,-1))),_xldudf_DR_YTD(Value,O14,O19,P14,P19,Q14,Q19,R14,R19)),IF(C14="QTD",IF(C19="Forecast",_xldudf_DR_GET(Value,O14,O19,P14,P19,Q14,Q19,R14,R19,S14,S19)+IF(MOD(LEFT(S19,FIND("+",S19,1)-1),3)=0,0,_xldudf_DR_QTD(Value,O14,O19,P14,P19,Q14,"Actuals",R14,EOMONTH(R19,-1))),_xldudf_DR_QTD(Value,O14,O19,P14,P19,Q14,Q19,R14,R19)),"Error in Aggregation method")))`
- **F20** at I19 (example `I19`): `=IF(H15>D19,List!$D$2,List!$E$2)`
- **F21** at J19 (example `J19`): `=IFERROR((H15-D19)/ABS(D19),"NA")`
- **F22** at O19 (example `O19`): `=C13`
- **F23** at A22 (example `A22`): `=A12+1`

## 6. Pictures

None.

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **cell value lessThan** `E27` → fontColor `037C5A` — on J27:J28
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["E27"], "kind": "cellIs", "op": "lessThan", "priority": 1, "ranges": "J27:J28"}`
- [P2] **cell value between** `E27` and `F27` → fontColor `FFB800` — on J27:J28
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E27", "F27"], "kind": "cellIs", "op": "between", "priority": 2, "ranges": "J27:J28"}`
- [P3] **cell value greaterThan** `F27` → fontColor `BF1D30` — on J27:J28
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["F27"], "kind": "cellIs", "op": "greaterThan", "priority": 3, "ranges": "J27:J28"}`
- [P7] **cell value lessThan** `E18` → fontColor `037C5A` — on J18:J19
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["E18"], "kind": "cellIs", "op": "lessThan", "priority": 7, "ranges": "J18:J19"}`
- [P8] **cell value between** `E18` and `F18` → fontColor `FFB800` — on J18:J19
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E18", "F18"], "kind": "cellIs", "op": "between", "priority": 8, "ranges": "J18:J19"}`
- [P9] **cell value greaterThan** `F18` → fontColor `BF1D30` — on J18:J19
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["F18"], "kind": "cellIs", "op": "greaterThan", "priority": 9, "ranges": "J18:J19"}`
- [P37] **icon set `3Triangles`** thresholds [percent 0; percent $E$8; percent $F$8] — on J10 J20
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "percent", "value": "$E$8"}, {"gte": true, "type": "percent", "value": "$F$8"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 37, "ranges": "J10 J20"}`
- [P41] **cell value lessThan** `E8` → fontColor `037C5A` — on J8:J9
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["E8"], "kind": "cellIs", "op": "lessThan", "priority": 41, "ranges": "J8:J9"}`
- [P42] **cell value between** `E8` and `F8` → fontColor `FFB800` — on J8:J9
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["E8", "F8"], "kind": "cellIs", "op": "between", "priority": 42, "ranges": "J8:J9"}`
- [P43] **cell value greaterThan** `F8` → fontColor `BF1D30` — on J8:J9
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["F8"], "kind": "cellIs", "op": "greaterThan", "priority": 43, "ranges": "J8:J9"}`
- [P207] **formula** `AND($J8<$F8,$J8>$E8)` → fontColor `FFB800` — on I8:I9 I18:I19 I27:I28
  - json: `{"dxf": {"fontColor": "FFB800"}, "formulas": ["AND($J8<$F8,$J8>$E8)"], "kind": "expression", "priority": 207, "ranges": "I8:I9 I18:I19 I27:I28"}`
- [P208] **formula** `$J8<=$E8` → fontColor `037C5A` — on I8:I9 I18:I19 I27:I28
  - json: `{"dxf": {"fontColor": "037C5A"}, "formulas": ["$J8<=$E8"], "kind": "expression", "priority": 208, "ranges": "I8:I9 I18:I19 I27:I28"}`
- [P209] **formula** `$J8>=$F8` → fontColor `BF1D30` — on I8:I9 I18:I19 I27:I28
  - json: `{"dxf": {"fontColor": "BF1D30"}, "formulas": ["$J8>=$F8"], "kind": "expression", "priority": 209, "ranges": "I8:I9 I18:I19 I27:I28"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## 9. Known gaps in the official template (read before building)

- The data-validation dropdowns in §1 read from a sheet named `List` that is **not part of this template**, and some of them point at
  `List!#REF!`, which is broken in the template itself. If the workbook already has a `List` sheet, apply the validations that point
  at real ranges; otherwise build the sheet without them and say so. Do not recreate the `#REF!` ones.
- A defined name in §1 can point at another sheet of this workbook (for example `FY_Start`). Define it on the sheet you built, or skip
  it, and say which.
