# Spec: pnl-dr-sc-style → sheet "FP&A"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:U21`; Everything beyond it is hidden (columns after U, rows after 21). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | FED7E4 |
| Zoom | 100 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:V23 |
| Merged ranges | B19:C19, B21:C21, B7:O7 |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 16.57 | 90.8 |  |
| C | 4.57 | 27.8 |  |
| D:V | 16.57 | 90.8 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | – | – | `–` | – | – | – | – |
| S4 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S5 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S6 | Poppins | 12.0 | B | F7F7F7 | – | – | `mmm-yy` | right | center | 1.0 | – |
| S7 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S8 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S9 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S10 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 12.0 |  | 0C142B | – | – | `@` | right | center | 1.0 | – |
| S13 | Poppins | 24.0 | B | F7F7F7 | – | – | `–` | left | top | – | – |
| S14 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | wrap |
| S15 | Poppins | 20.0 |  | 0C142B | – | – | `mmm-yy` | left | center | – | – |
| S16 | Poppins | 12.0 |  | F93576 | – | – | `–` | – | – | – | – |
| S17 | Poppins | 24.0 | B | F7F7F7 | – | – | `–` | left | center | – | – |
| S18 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `@` | left | top | 1.0 | – |
| S19 | Poppins | 12.0 | B | 001F37 | – | B:thin:9EA1AA | `–` | – | center | – | – |
| S20 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S21 | Poppins Regular | 12.0 |  | 4646CE | EAEAFF | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `_(* #,##0_);_(* \(#,##0\);_(* "-"_);_(@_)` | right | top | – | – |
| S22 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |
| S23 | Poppins Regular | 12.0 |  | 333333 | – | – | `@` | left | center | 1.0 | – |
| S24 | Calibri | 11.0 |  | 001F37 | – | T:thin:9EA1AA,B:thin:9EA1AA | `–` | – | – | – | – |
| S25 | Calibri | 11.0 |  | 333333 | – | – | `–` | – | – | – | – |
| S26 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `_(* #,##0_);_(* \(#,##0\);_(* "-"_);_(@_)` | – | center | – | – |
| S27 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `_(* #,##0_);_(* \(#,##0\);_(* "-"_);_(@_)` | right | center | – | – |
| S28 | Poppins | 12.0 |  | C08405 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S29 | Poppins | 12.0 |  | FF0000 | – | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S30 | Calibri | 11.0 |  | 001F37 | – | T:thin:9EA1AA | `–` | – | – | – | – |
| S31 | Poppins | 12.0 | B | 626364 | – | – | `@` | left | center | 1.0 | – |
| S32 | Poppins | 12.0 | B | 333333 | – | – | `@` | left | center | 1.0 | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:O=S1 P:S=S3 T:U=S4
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:O=S5 P:U=S6
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S7 G:O=S1 P=S3 Q:U=S4
- **T4** h=24.0 rows 4: A=S1 B=S8 C=S2 D:O=S5 P:U=S6
- **T5** h=15.95 rows 5: A=S1 B=S9 C=S2 D:H=S10 I=S11 J:N=S10 O=S11 P:U=S12
- **T6** h=24.0 rows 6: A=S4 B=S13 C:E=S14 F=S15 G:H=S4 I=S16 J:O=S4 P=S3 Q=S17 R:S=S3 T:U=S4
- **T7** h=24.0 rows 7: A=S4 B:O=S18 P:U=S4
- **T8** h=24.0 rows 8: A=S4 B=S19 C:U=S4
- **T9** h=24.0 rows 9: A=S20 B=S21 C=S22 D=S23 E:U=S4
- **T10** h=24.0 rows 10,12: A=S4 B=S24 C=S4 D=S25 E:U=S4
- **T11** h=24.0 rows 11: A=S20 B=S26 C=S22 D=S23 E:U=S4
- **T12** h=24.0 rows 13: A=S20 B=S27 C=S22 D=S23 E:U=S4
- **T13** h=None rows 14,16: A=S4 B=S24 C:U=S4
- **T14** h=24.0 rows 15: A=S20 B=S28 C=S22 D=S23 E:U=S4
- **T15** h=24.0 rows 17: A=S20 B=S29 C=S22 D=S23 E:U=S4
- **T16** h=None rows 18: A=S4 B=S30 C:U=S4
- **T17** h=24.0 rows 19: A=S4 B:C=S31 D=S23 E:U=S4
- **T18** h=None rows 20: A:U=S4
- **T19** h=24.0 rows 21: A=S4 B:C=S32 D=S23 E:U=S4

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r4: {"B": "Instructions"}
- r7: {"B": "Field Legend"}
- r9: {"B": "Input", "D": "Data you input"}
- r11: {"B": "Fixed Output", "D": "Data from the Datarails database"}
- r13: {"B": "Calculation", "D": "Excel calculations"}
- r15: {"B": 0, "D": "Budget"}
- r17: {"B": 0, "D": "Forecast"}
- r19: {"B": "Total Income", "D": "Subtotal "}
- r21: {"B": "Gross Profit", "D": "Grand total"}

### 5.2 Formulas (same relative pattern for every listed cell)


## 6. Pictures

- picture 1: logo `fpa-header` — displayed **234x35 px**, anchor B1(+5px,+30px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
