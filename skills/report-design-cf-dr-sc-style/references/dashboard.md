# Spec: cf-dr-sc-style → sheet "Dashboard"

> Source: Cash Flow - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:M10`; Everything beyond it is hidden (columns after M, rows after 10). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `None` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 98 |
| Default row height | 14.4 pt (unlisted rows visible) |
| Used range | A1:N11 |
| Merged ranges | B8:C8, I2:M2 |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 2.71 | 18.0 |  |
| B | 11.71 | 65.2 |  |
| C | 18.57 | 101.2 |  |
| D | 16.57 | 90.8 |  |
| I | 24.57 | 132.8 |  |
| J | 4.57 | 27.8 |  |
| K | 24.57 | 132.8 |  |
| L | 4.57 | 27.8 |  |
| M | 24.57 | 132.8 |  |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S2 | Calibri | 11.0 |  | 001F37 | – | B:thin:auto | `–` | – | – | – | – |
| S3 | Calibri | 11.0 | B | F7F7F7 | 3BA6FF | – | `[$-409]mmm\-yy;@` | center | center | – | – |
| S4 | Calibri | 11.0 |  | 001F37 | – | R:thin:auto | `–` | – | – | – | – |
| S5 | Calibri | 11.0 |  | 001F37 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S6 | Calibri | 11.0 |  | 001F37 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S7 | Calibri | 11.0 | B | 7FFFD4 | – | L:thin:auto | `–` | – | – | – | – |
| S8 | Calibri | 11.0 | B | 7FFFD4 | – | – | `–` | – | – | – | – |
| S9 | Calibri | 11.0 |  | 001F37 | – | L:thin:auto | `–` | – | – | – | – |
| S10 | Calibri | 24.0 | B | 333333 | – | – | `–` | center | center | – | wrap |
| S11 | Calibri | 24.0 | B | 333333 | – | – | `–` | center | – | – | wrap |
| S12 | Poppins | 20.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S13 | Calibri | 11.0 |  | 001F37 | – | L:thin:auto,B:thin:auto | `–` | – | – | – | – |
| S14 | Calibri | 11.0 | B | F7F7F7 | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | left | center | – | – |
| S15 | Calibri | 11.0 | B | F7F7F7 | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | – |
| S16 | Calibri | 11.0 | B | F7F7F7 | 3BA6FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `[$-409]mmm\-yy;@` | center | center | – | wrap |
| S17 | Calibri | 24.0 | B | 333333 | – | – | `#,##0,\ "K"` | center | center | – | wrap |
| S18 | Calibri | 11.0 |  | 001F37 | F7F7F7 | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S19 | Calibri | 11.0 |  | 001F37 | E7F4FF | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `0%` | – | – | – | – |
| S20 | Calibri | 11.0 |  | 001F37 | – | L:thin:auto,R:thin:auto,T:thin:auto,B:thin:auto | `#,##0,\ "K"` | – | – | – | – |
| S21 | Poppins | 20.0 | B | 333333 | – | – | `#,##0,\ "K"` | center | center | – | wrap |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=None rows 1: A:M=S1
- **T2** h=14.4 rows 2: A=S1 B:C=S2 D:H=S1 I:M=S3
- **T3** h=14.4 rows 3: A=S4 B=S5 C=S6 D=S7 E:F=S8 G:M=S1
- **T4** h=64.5 rows 4: A=S4 B=S5 C=S6 D=S9 E:H=S1 I=S10 J=S11 K=S10 L=S11 M=S10
- **T5** h=8.25 rows 5: A=S4 B=S5 C=S6 D=S9 E:H=S1 I=S10 J=S11 K=S10 L=S11 M=S10
- **T6** h=37.5 rows 6: A=S4 B=S5 C=S6 D=S9 E:H=S1 I:M=S12
- **T7** h=8.25 rows 7: A=S4 B=S5 C=S6 D=S13 E:F=S2 G:H=S1 I:M=S12
- **T8** h=32.25 rows 8: A=S4 B:C=S14 D=S15 E:F=S16 G=S9 H=S1 I=S17 J=S11 K=S17 L=S11 M=S17
- **T9** h=32.25 rows 9: A=S4 B:C=S5 D=S18 E:F=S19 G=S9 H:M=S1
- **T10** h=32.25 rows 10: A=S4 B:C=S5 D=S20 E:F=S19 G=S9 H=S1 I=S21 J=S12 K=S21 L=S12 M=S21

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"B": 1, "I": "Published Item"}
- r3: {"A": 1, "B": "Field", "C": "Account Group L2"}
- r4: {"B": "Field Value", "C": "Investment Activity", "I": "Operating\nCash", "K": "Investing\nCash", "M": "Financing\nCash"}
- r6: {"B": "Aggregation", "C": "YTD"}
- r8: {"B": "Compare Analysis", "D": "Compare Result 1", "E": "If % of change is below --> Red", "F": "If % of change is Above --> Green"}
- r9: {"B": "Compare A", "C": "Previous Month", "E": -0.05, "F": 0.05}
- r10: {"B": "Compare B", "C": "Previous Year", "E": -0.1, "F": 0.1}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at I8 (example `I8`): `=IF($C$6="YTD",'Cash Flow - YoY'!P$19,IF($C$6="QTD",'Cash Flow - YoY'!K$19,'Cash Flow - YoY'!F$19))`
- **F2** at K8 (example `K8`): `=IF($C$6="YTD",'Cash Flow - YoY'!P$31,IF($C$6="QTD",'Cash Flow - YoY'!M$31,'Cash Flow - YoY'!H$31))`
- **F3** at M8 (example `M8`): `=IF($C$6="YTD",'Cash Flow - YoY'!P$47,IF($C$6="QTD",'Cash Flow - YoY'!O$47,'Cash Flow - YoY'!J$47))`

## 6. Pictures

- picture 1: logo `icon-cash-cycle` — displayed **67x66 px**, anchor I4(+54px,+86px)
- picture 2: logo `icon-handshake` — displayed **52x51 px**, anchor K5(+61px,+5px)
- picture 3: logo `icon-money-bag` — displayed **67x66 px**, anchor M4(+57px,+85px)

## 7. Conditional formatting, sparklines

None.

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.

## 9. Dependency and a template defect (read before building)

- The three cards read from the sheet **`Cash Flow - YoY`** (see the formulas in §5.2). Build or locate a populated `Cash Flow - YoY`
  sheet first. If the user asks for the Dashboard alone, build it and tell them the cards stay empty until that sheet exists.
- **Defect in the official template:** the Operating card reads the actual-value columns (`P`, `K`, `F` of `Cash Flow - YoY`), but the
  Investing card reads `M31` / `H31` and the Financing card `O47` / `J47` for QTD / MTD — those are variance or spacer columns, so
  QTD and MTD show a variance or a blank. Use the same actual-value columns as the Operating card (`K31` / `F31` and `K47` / `F47`),
  and tell the user you corrected it. YTD (`P31`, `P47`) is already right.
