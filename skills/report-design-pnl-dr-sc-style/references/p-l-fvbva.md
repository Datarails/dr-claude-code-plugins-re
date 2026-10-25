# Spec: pnl-dr-sc-style → sheet "P&L FvBvA"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:AC64`; Everything beyond it is hidden (columns after AC, rows after 64). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D8` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 80 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AR65 |
| Merged ranges | D2:J2, L2:R2, T2:Z2 |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `DR_REFERENCE_DATE` | `DR_DATE_PICKER` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |
| Defined name `Value_EBITDA` | `"widget_19313_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 56.57 | 300.8 |  |
| C | 4.57 | 27.8 |  |
| D:H | 16.57 | 90.8 |  outline 1 |
| I:J | 16.57 | 90.8 |  outline 1 |
| K | 4.57 | 27.8 |  |
| L:R | 16.57 | 90.8 |  outline 1 |
| S | 4.57 | 27.8 |  |
| T:Z | 16.57 | 90.8 |  outline 1 |
| AA | 4.57 | 27.8 |  |
| AB | 40.57 | 216.8 |  |
| AC | 16.57 | 90.8 |  |
| AD | 16.86 | 92.2 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S5 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S6 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S7 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S8 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S9 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 12.0 |  | F9AB10 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 12.0 |  | F93576 | 0C142B | – | `@` | right | center | 1.0 | – |
| S13 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | – | center | – | – |
| S14 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | top | – | – |
| S15 | Poppins | 12.0 |  | F93576 | 0C142B | – | `–` | – | – | – | – |
| S16 | Poppins | 24.0 | B | F7F7F7 | 0C142B | – | `–` | left | center | – | – |
| S17 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S18 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S19 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S20 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S21 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S22 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S23 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S24 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S26 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S27 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S28 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S29 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S30 | Poppins | 12.0 |  | C08405 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S31 | Poppins | 12.0 |  | C9245B | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S32 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S33 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S34 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S35 | Poppins | 12.0 |  | 4646CE | EAEAFF | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S36 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S37 | Poppins | 4.0 |  | F0F1F4 | – | R:thin:9EA1AA | `0` | – | – | – | – |
| S38 | Poppins | 4.0 |  | F0F1F4 | – | – | `0` | – | – | – | – |
| S39 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S40 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S41 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S42 | Calibri | 11.0 |  | 001F37 | – | T:thin:9EA1AA | `–` | – | – | – | – |
| S43 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |
| S44 | Poppins | 12.0 | B | 333333 | – | – | `_(* #,##0.00_);_(* \(#,##0.00\);_(* "-"??_);_(@_)` | right | center | 1.0 | – |
| S45 | Poppins | 12.0 | B | 333333 | – | B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S46 | Poppins | 14.0 | B | 0C142B | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S47 | Calibri | 11.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S48 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S49 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S50 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S51 | Poppins | 12.0 | B | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S52 | Poppins | 12.0 | B | 333333 | – | – | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S53 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA,R:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S54 | Poppins | 4.0 |  | F0F1F4 | – | L:thin:9EA1AA | `0` | left | center | 1.0 | – |
| S55 | Poppins | 12.0 | B | 626364 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S56 | Poppins | 12.0 |  | 333333 | – | – | `#,##0,\ "K"` | right | center | 1.0 | – |
| S57 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S58 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S59 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S60 | Poppins | 12.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S61 | Poppins | 12.0 | B | 333333 | – | – | `0.0%` | right | center | 1.0 | – |
| S62 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S63 | Poppins | 12.0 | B | 333333 | – | T:thin:9EA1AA | `0.0%` | right | center | 1.0 | – |
| S64 | Poppins | 12.0 |  | 001F37 | – | T:thin:9EA1AA | `0.0%` | – | – | – | – |
| S65 | Poppins | 12.0 |  | 001F37 | – | T:thin:9EA1AA | `#,##0,\ "K"` | – | – | – | – |
| S66 | Poppins | 12.0 |  | 001F37 | – | – | `0.0%;\(0.0%\)` | – | – | – | – |
| S67 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | wrap |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:H=S2 I:X=S1 Y:AB=S3 AC=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:J=S4 K=S1 L:R=S4 S=S1 T:Z=S4 AA=S3 AB=S5 AC=S1
- **T3** h=8.25 rows 3: A:B=S1 C:H=S2 I=S6 J:X=S1 Y:AB=S3 AC=S1
- **T4** h=24.0 rows 4: A=S1 B=S7 C=S2 D:H=S8 I=S6 J:K=S1 L:P=S8 Q:S=S1 T:X=S8 Y:AB=S3 AC=S1
- **T5** h=24.0 rows 5: A=S1 B=S9 C=S2 D=S10 E=S11 F:H=S12 I=S10 J=S13 K=S1 L=S10 M=S11 N:P=S12 Q=S10 R=S13 S=S1 T:U=S10 V:X=S12 Y=S10 Z=S13 AA:AB=S3 AC=S1
- **T6** h=24.0 rows 6: A=S1 B=S9 C=S2 D=S10 E=S11 F:I=S10 J=S13 K=S1 L=S10 M=S11 N:Q=S10 R=S13 S=S1 T:Y=S10 Z=S13 AA:AB=S3 AC=S1
- **T7** h=15.95 rows 7: A=S1 B=S14 C:H=S2 I=S6 J:K=S1 L=S15 M:X=S1 Y=S3 Z=S16 AA:AB=S3 AC=S1
- **T8** h=24.0 rows 8: A:B=S17 C:D=S18 E:H=S19 I:AC=S17
- **T9** h=24.0 rows 9: A=S17 B=S20 C:Z=S21 AA:AB=S22 AC=S23
- **T10** h=24.0 rows 10: A=S17 B:J=S24 K=S23 L:R=S24 S=S23 T:Z=S24 AA=S23 AB=S25 AC=S23
- **T11** h=24.0 rows 11-12,54-55: A=S26 B=S27 C=S28 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T12** h=24.0 rows 13: A=S37 B=S27 C=S28 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T13** h=24.0 rows 14: A=S38 B:C=S39 D:I=S40 J=S41 K=S17 L:Q=S40 R=S41 S=S17 T:Y=S40 Z=S41 AA=S17 AB=S42 AC=S17
- **T14** h=24.0 rows 15: A=S17 B=S43 C:J=S44 K=S17 L:R=S44 S=S17 T:Z=S44 AA:AC=S17
- **T15** h=24.0 rows 16,46,59: A=S17 B=S20 C:Z=S21 AA:AB=S22 AC=S17
- **T16** h=24.0 rows 17: A=S17 B=S45 C:J=S46 K=S17 L:R=S46 S=S17 T:Z=S46 AA=S17 AB=S47 AC=S17
- **T17** h=24.0 rows 18-20: A=S48 B=S27 C=S49 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T18** h=24.0 rows 21: A=S50 B:C=S39 D:I=S40 J=S41 K=S17 L:Q=S40 R=S41 S=S17 T:Y=S40 Z=S41 AA=S17 AB=S42 AC=S17
- **T19** h=24.0 rows 22: A=S38 B:C=S43 D:I=S51 J=S52 K=S17 L:Q=S51 R=S52 S=S17 T:Y=S51 Z=S52 AA:AC=S17
- **T20** h=24.0 rows 23: A=S38 B:C=S43 D:Z=S52 AA:AC=S17
- **T21** h=24.0 rows 24,51,58: A=S38 B:AC=S17
- **T22** h=24.0 rows 25,52: A=S38 B=S20 C:Z=S21 AA:AB=S22 AC=S17
- **T23** h=24.0 rows 26: A=S38 B:J=S46 K=S17 L:R=S46 S=S17 T:Z=S46 AA=S17 AB=S47 AC=S17
- **T24** h=24.0 rows 27: A=S37 B=S27 C=S49 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T25** h=24.0 rows 28-36: A=S53 B=S27 C=S49 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T26** h=24.0 rows 37: A=S54 B:C=S55 D:I=S40 J=S41 K=S56 L:Q=S40 R=S41 S=S56 T:Y=S40 Z=S41 AA=S17 AB=S42 AC=S17
- **T27** h=24.0 rows 38: A=S54 B:AC=S17
- **T28** h=24.0 rows 39: A=S54 B=S20 C:Z=S21 AA:AB=S22 AC=S17
- **T29** h=24.0 rows 40: A=S54 B:J=S24 K=S17 L:R=S24 S=S17 T:Z=S24 AA=S17 AB=S47 AC=S17
- **T30** h=24.0 rows 41-42: A=S53 B=S27 C=S28 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T31** h=24.0 rows 43: A=S54 B:C=S57 D:I=S58 J=S59 K=S17 L:Q=S58 R=S59 S=S17 T:Y=S58 Z=S59 AA=S17 AB=S42 AC=S17
- **T32** h=24.0 rows 44: A=S54 B:C=S60 D:Z=S61 AA:AC=S17
- **T33** h=None rows 45: A:AC=S17
- **T34** h=None rows 47,53,60: A=S17 B:J=S47 K=S17 L:R=S47 S=S17 T:Z=S47 AA=S17 AB=S47 AC=S17
- **T35** h=24.0 rows 48,61: A=S26 B=S62 C=S28 D=S29 E=S30 F:H=S31 I=S32 J=S33 K=S34 L=S29 M=S30 N:P=S31 Q=S32 R=S33 S=S34 T=S29 U=S30 V:X=S31 Y=S32 Z=S33 AA=S34 AB=S35 AC=S36
- **T36** h=24.0 rows 49: A=S17 B:C=S57 D:I=S58 J=S59 K=S17 L:Q=S58 R=S59 S=S17 T:Y=S58 Z=S59 AA=S17 AB=S42 AC=S17
- **T37** h=24.0 rows 50: A=S17 B:C=S60 D:Z=S61 AA:AC=S17
- **T38** h=24.0 rows 56: A=S17 B:C=S57 D:I=S58 J=S63 K=S17 L:Q=S58 R=S63 S=S17 T:Y=S58 Z=S63 AA=S17 AB=S42 AC=S17
- **T39** h=24.0 rows 57: A=S38 B:C=S60 D:Z=S61 AA:AC=S17
- **T40** h=24.0 rows 62: A=S17 B:C=S57 D:I=S58 J=S64 K=S17 L:P=S58 Q=S65 R=S64 S=S17 T:X=S58 Y=S65 Z=S64 AA=S17 AB=S42 AC=S17
- **T41** h=24.0 rows 63: A=S17 B:C=S60 D:I=S52 J=S66 K=S17 L:P=S52 Q:R=S66 S=S17 T:X=S52 Y:Z=S66 AA:AC=S17
- **T42** h=24.0 rows 64: A=S38 B:D=S17 E=S67 F:AC=S17

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": "MTD", "L": "QTD", "T": "YTD", "AB": "Variance Explanation"}
- r4: {"B": "P&L - FvBvA"}
- r5: {"D": "Actuals", "E": "Budget", "F": "Forecast", "G": "Forecast", "H": "Forecast", "I": "∆ vs Budget", "J": "% ∆ vs Budget", "L": "Actuals", "M": "Budget", "N": "Forecast", "O": "Forecast", "P": "Forecast", "Q": "∆ vs Budget", "R": "% ∆ vs Budget", "T": "Actuals", "U": "Budget", "V": "Forecast", "W": "Forecast", "X": "Forecast", "Y": "∆ vs Budget", "Z": "% ∆ vs Budget"}
- r6: {"F": "Worst", "G": "Base", "H": "Best", "N": "Worst", "O": "Base", "P": "Best", "V": "Worst", "W": "Base", "X": "Best"}
- r9: {"B": "Income"}
- r11: {"B": "Revenue - Licenses"}
- r12: {"B": "Revenue - Professional Services"}
- r13: {"B": "Revenue - Integrations"}
- r14: {"B": "Total Income"}
- r16: {"B": "Cost of Sales"}
- r18: {"B": "Cost of Sales - License"}
- r19: {"B": "Cost of Sales - Integrations"}
- r20: {"B": "Cost of Sales - Professional Services"}
- r21: {"B": "Total Cost of Sales"}
- r22: {"B": "Gross Profit"}
- r23: {"B": "Gross Margin (%)"}
- r25: {"B": "Operating Expenses ex. D&A"}
- r27: {"B": "Marketing"}
- r28: {"B": "Finance"}
- r29: {"B": "G&A"}
- r30: {"B": "IT & Equipment"}
- r31: {"B": "Legal"}
- r32: {"B": "Office Expenses"}
- r33: {"B": "Payroll Related"}
- r34: {"B": "People Development"}
- r35: {"B": "Software Subscriptions"}
- r36: {"B": "Travel"}
- r37: {"B": "Total Operating Expenses ex. D&A"}
- r39: {"B": "Other Income and Expenses"}
- r41: {"B": "Other Expense"}
- r42: {"B": "Other Income"}
- r43: {"B": "EBITDA"}
- r44: {"B": "EBITDA Margin %"}
- r46: {"B": "Depreciation & Amortization"}
- r48: {"B": "Depreciation & Amortization"}
- r49: {"B": "EBIT"}
- r50: {"B": "EBIT %"}
- r52: {"B": "Interest and Income Expenses"}
- r54: {"B": "Interest Expense"}
- r55: {"B": "Interest Income"}
- r56: {"B": "EBT"}
- r57: {"B": "EBT %"}
- r59: {"B": "Taxes"}
- r61: {"B": "Tax"}
- r62: {"B": "Net Profit"}
- r63: {"B": "Net Margin %"}
- r64: {"E": " "}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D4 (example `D4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at E4:H4, M4:P4, U4:X4 (example `E4`): `=D4`
- **F3** at L4, T4 (example `L4`): `=D4`
- **F4** at B5 (example `B5`): `=DR_REFERENCE_DATE`
- **F5** at D11:E13 (example `D11`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Income")`
- **F6** at F11:H13 (example `F11`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",F$4,"[Scenario]",F$5,"[Account Group L2]","Income","[Planning Scenario]",F$6)`
- **F7** at I11:I13, Q11:Q13, Y11:Y13, I18:I20, Q18:Q20, Y18:Y20, I27:I36, Q27:Q36, Y27:Y36, I41:I42, Q41:Q42, Y41:Y42, I48, Q48, Y48, I54:I55, Q54:Q55, Y54:Y55, I61, Q61, Y61 (example `I11`): `=IFERROR(D11-E11,"NA")`
- **F8** at J11:J14, R11:R14, Z11:Z14, J18:J21, R18:R21, Z18:Z21, J27:J37, R27:R37, Z27:Z37, J41:J42, R41:R42, Z41:Z42, J48, R48, Z48, J54:J55, R54:R55, Z54:Z55, J61, R61, Z61 (example `J11`): `=IFERROR(D11/E11-1,"NA")`
- **F9** at L11:M13 (example `L11`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",L$4,"[Scenario]",L$5,"[Account Group L2]","Income")`
- **F10** at N11:P13 (example `N11`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",N$4,"[Scenario]",N$5,"[Account Group L2]","Income","[Planning Scenario]",N$6)`
- **F11** at T11:U13 (example `T11`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",T$4,"[Scenario]",T$5,"[Account Group L2]","Income")`
- **F12** at V11:X13 (example `V11`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B11,"[Reporting Month]",V$4,"[Scenario]",V$5,"[Account Group L2]","Income","[Planning Scenario]",V$6)`
- **F13** at D14:I14, L14:Q14, T14:Y14, D21:I21, L21:Q21, T21:Y21 (example `D14`): `=IFERROR(SUM(D11:D13),"NA")`
- **F14** at D18:E20 (example `D18`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B18,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Cost of Goods Sold")`
- **F15** at F18:H20 (example `F18`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B18,"[Reporting Month]",F$4,"[Scenario]",F$5,"[Account Group L2]","Cost of Goods Sold","[Planning Scenario]",F$6)`
- **F16** at L18:L20 (example `L18`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B18,"[Reporting Month]",$L$4,"[Scenario]",$L$5,"[Account Group L2]","Cost of Goods Sold")`
- **F17** at M18:M20 (example `M18`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B18,"[Reporting Month]",$M$4,"[Scenario]",$M$5,"[Account Group L2]","Cost of Goods Sold")`
- **F18** at N18:P20, V18:X20 (example `N18`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B18,"[Reporting Month]",N$4,"[Scenario]",N$5,"[Account Group L2]","Cost of Sales","[Planning Scenario]",N$6)`
- **F19** at T18:T20 (example `T18`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B18,"[Reporting Month]",$T$4,"[Scenario]",$T$5,"[Account Group L2]","Cost of Goods Sold")`
- **F20** at U18:U20 (example `U18`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B18,"[Reporting Month]",$U$4,"[Scenario]",$U$5,"[Account Group L2]","Cost of Goods Sold")`
- **F21** at D22:I22, L22:Q22, T22:Y22 (example `D22`): `=IFERROR(D14-D21,"NA")`
- **F22** at J22, R22, Z22, J43:J44, R43:R44, Z43:Z44, J49:J50, R49:R50, Z49:Z50, J56, R56, Z56, J62, R62, Z62 (example `J22`): `=IFERROR(G22/H22-1,"NA")`
- **F23** at D23:H23, L23:P23, T23:X23 (example `D23`): `=IFERROR(D22/D14,"NA")`
- **F24** at I23:J23, Q23:R23, Y23:Z23, I44, Q44, Y44, I50, Q50, Y50 (example `I23`): `=IFERROR(G23-H23,"NA")`
- **F25** at D27:D36 (example `D27`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$D$4,"[Scenario]",$D$5,"[Account Group L2]","Operating Expense")`
- **F26** at E27:E36 (example `E27`): `=_xldudf_DR_GET(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$E$4,"[Scenario]",$E$5,"[Account Group L2]","Operating Expense")`
- **F27** at F27:H36, N27:P36, V27:X36 (example `F27`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B27,"[Reporting Month]",F$4,"[Scenario]",F$5,"[Account Group L2]","Operating Expense","[Planning Scenario]",F$6)`
- **F28** at L27:L36 (example `L27`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$L$4,"[Scenario]",$L$5,"[Account Group L2]","Operating Expense")`
- **F29** at M27:M36 (example `M27`): `=_xldudf_DR_QTD(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$M$4,"[Scenario]",$M$5,"[Account Group L2]","Operating Expense")`
- **F30** at T27:T36 (example `T27`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$T$4,"[Scenario]",$T$5,"[Account Group L2]","Operating Expense")`
- **F31** at U27:U36 (example `U27`): `=_xldudf_DR_YTD(Value_EBITDA,"[Report_Field]",$B27,"[Reporting Month]",$U$4,"[Scenario]",$U$5,"[Account Group L2]","Operating Expense")`
- **F32** at D37:I37, L37:Q37, T37:Y37 (example `D37`): `=IFERROR(SUM(D27:D36),"NA")`
- **F33** at D41:D42, L41:L42, T41:T42 (example `D41`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Report_Field]",$B41)`
- **F34** at E41:E42 (example `E41`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",$E$4,"[Scenario]",$E$5,"[Account Group L2]",$B41)`
- **F35** at F41:H42, N41:P42, V41:X42 (example `F41`): `=_xldudf_DR_GET(Value,"[Report_Field]",$B41,"[Reporting Month]",F$4,"[Scenario]",F$5,"[Account Group L2]",$B41,"[Planning Scenario]",F$6)`
- **F36** at M41:M42 (example `M41`): `=_xldudf_DR_QTD(Value_EBITDA,"[Reporting Month]",$M$4,"[Scenario]",$M$5,"[Account Group L2]",$B41)`
- **F37** at U41:U42 (example `U41`): `=_xldudf_DR_YTD(Value_EBITDA,"[Reporting Month]",$U$4,"[Scenario]",$U$5,"[Account Group L2]",$B41)`
- **F38** at D43:I43, L43:Q43, T43:Y43 (example `D43`): `=IFERROR(D22-D37+D41-D42,"NA")`
- **F39** at D44:H44, L44:P44, T44:X44 (example `D44`): `=IFERROR(D43/D14,"NA")`
- **F40** at D48 (example `D48`): `=_xldudf_DR_GET(Value,"[Reporting Month]",$D$4,"[Scenario]",$D$5,"[DR_KPI]",$B48)`
- **F41** at E48 (example `E48`): `=_xldudf_DR_GET(Value,"[Reporting Month]",$E$4,"[Scenario]",$E$5,"[DR_KPI]",$B48)`
- **F42** at F48:H48, N48:P48, V48:X48, F61:H61, N61:P61, V61:X61 (example `F48`): `=_xldudf_DR_GET(Value,"[Reporting Month]",F$4,"[Scenario]",F$5,"[DR_KPI]",$B48,"[Planning Scenario]",F$6)`
- **F43** at L48 (example `L48`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$L$4,"[Scenario]",$L$5,"[DR_KPI]",$B48)`
- **F44** at M48 (example `M48`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",$M$4,"[Scenario]",$M$5,"[DR_KPI]",$B48)`
- **F45** at T48 (example `T48`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$T$4,"[Scenario]",$T$5,"[DR_KPI]",$B48)`
- **F46** at U48 (example `U48`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",$U$4,"[Scenario]",$U$5,"[DR_KPI]",$B48)`
- **F47** at D49:I49, L49:Q49, T49:Y49, D62:I62, L62:Q62, T62:Y62 (example `D49`): `=IFERROR(D43-D48,"NA")`
- **F48** at D50:H50, L50:P50, T50:X50 (example `D50`): `=IFERROR(D49/D14,"NA")`
- **F49** at D54:E55, D61:E61 (example `D54`): `=_xldudf_DR_GET(Value,"[Reporting Month]",D$4,"[Scenario]",D$5,"[DR_KPI]",$B54)`
- **F50** at F54:H55, N54:P55, V54:X55 (example `F54`): `=_xldudf_DR_GET(Value_EBITDA,"[Reporting Month]",F$4,"[Scenario]",F$5,"[Account Group L2]",$B54,"[Planning Scenario]",F$6)`
- **F51** at L54:M55, L61:M61 (example `L54`): `=_xldudf_DR_QTD(Value,"[Reporting Month]",L$4,"[Scenario]",L$5,"[DR_KPI]",$B54)`
- **F52** at T54:U55, T61:U61 (example `T54`): `=_xldudf_DR_YTD(Value,"[Reporting Month]",T$4,"[Scenario]",T$5,"[DR_KPI]",$B54)`
- **F53** at D56:I56, L56:Q56, T56:Y56 (example `D56`): `=IFERROR(D49+D54-D55,"NA")`
- **F54** at D57:J57, L57:R57, T57:Z57 (example `D57`): `=IFERROR(D56/D14,"NA")`
- **F55** at D63:J63, L63:R63, T63:Z63 (example `D63`): `=IFERROR(D62/D14,"NA")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **formula** `$B$6="GBP"` → numFmt `\£#,##0,\ "K"` — on I22
  - json: `{"dxf": {"numFmt": "\\£#,##0,\\ \"K\""}, "formulas": ["$B$6=\"GBP\""], "kind": "expression", "priority": 1, "ranges": "I22"}`
- [P2] **formula** `$B$6="EUR"` → numFmt `\€#,##0,\ "K"` — on I22
  - json: `{"dxf": {"numFmt": "\\€#,##0,\\ \"K\""}, "formulas": ["$B$6=\"EUR\""], "kind": "expression", "priority": 2, "ranges": "I22"}`
- [P3] **formula** `$B$6="USD"` → numFmt `"$"#,##0,\ "K"` — on I22
  - json: `{"dxf": {"numFmt": "\"$\"#,##0,\\ \"K\""}, "formulas": ["$B$6=\"USD\""], "kind": "expression", "priority": 3, "ranges": "I22"}`
- [P7] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0], reversed — on I18:I20 Q18:Q20 Y18:Y20 I27:I36 Q27:Q36 Y27:Y36 I48 Q48 Y48 I61 Q61 Y61
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": true, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 7, "ranges": "I18:I20 Q18:Q20 Y18:Y20 I27:I36 Q27:Q36 Y27:Y36 I48 Q48 Y48 I61 Q61 Y61"}`
- [P13] **cell value equal** `"Budget"` → fontColor `F9AB10` — on E5:E6 M5:M6 U5:U6
  - json: `{"dxf": {"fontColor": "F9AB10"}, "formulas": ["\"Budget\""], "kind": "cellIs", "op": "equal", "priority": 13, "ranges": "E5:E6 M5:M6 U5:U6"}`
- [P5623] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on I11:I13 Q11:Q13 Y11:Y13 I41:I42 Q41:Q42 Y41:Y42 I54:I55 Q54:Q55 Y54:Y55
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 5623, "ranges": "I11:I13 Q11:Q13 Y11:Y13 I41:I42 Q41:Q42 Y41:Y42 I54:I55 Q54:Q55 Y54:Y55"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
