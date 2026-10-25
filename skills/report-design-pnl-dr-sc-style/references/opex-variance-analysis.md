# Spec: pnl-dr-sc-style → sheet "OpEx Variance Analysis"

> Source: P&L EBITDA - DR SC Style — Workspace > Reports > Datarails templates of the AI demo org (financeos.ai.demo.1103). Exact values from the template workbook (colours resolved to hex). Generic build rules, traps and the verify checklist are in the `report-design` router skill — read them first.

Visible area = `A1:M28`; Everything beyond it is hidden (columns after M, rows after 28). Gridlines **off**. Row heights in points; column widths in points (Office.js `columnWidth`) or chars (file writers). In §3 `–` = none/General/no fill, font colour `auto` = automatic. Formulas in §5.2 are written for the first cell shown; fill them to the other listed cells with relative references shifting (like copy/paste). Pictures are in z-order, anchored in px from the top-left of the anchor cell.

## 1. Sheet settings

| Setting | Value |
|---|---|
| Gridlines | off |
| Freeze panes | `D7` (freeze BEFORE hiding columns) |
| Tab colour | none |
| Zoom | 100 |
| Default row height | 24 pt (unlisted rows visible) |
| Used range | A1:AB58 |
| Merged ranges | G2:J2 |
| Defined name `DR_DATE_PICKER` | `46203` |
| Defined name `Value` | `"widget_19324_0_tt_1791797074177"` |

## 2. Columns

| Col | chars | pt | note |
|---|---|---|---|
| A | 4.57 | 27.8 |  |
| B | 56.57 | 300.8 |  |
| C | 4.57 | 27.8 |  |
| D:E | 16.57 | 90.8 |  outline 1 |
| F | 3.57 | 22.5 |  outline 1 |
| G:J | 16.57 | 90.8 |  outline 1 |
| K | 4.57 | 27.8 |  |
| L | 40.57 | 216.8 |  |
| M | 16.57 | 90.8 |  |
| N | 16.86 | 92.2 | HIDDEN |

## 3. Style catalog

| id | font | size | b/i | font colour | fill | borders (L/R/T/B style:colour) | numfmt | h-align | v-align | indent | wrap |
|---|---|---|---|---|---|---|---|---|---|---|---|
| S1 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | – |
| S2 | Poppins | 12.0 |  | 001F37 | 0C142B | – | `–` | – | – | – | wrap |
| S3 | Poppins | 12.0 |  | 0C142B | 0C142B | – | `–` | – | – | – | – |
| S4 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | centerContinuous | top | – | – |
| S5 | Poppins | 14.0 | B | 333333 | FFDBE5 | – | `–` | center | top | – | – |
| S6 | Poppins | 20.0 |  | 0C142B | 0C142B | – | `mmm-yy` | left | center | – | – |
| S7 | Poppins | 20.0 | B | FFFFFF | 0C142B | – | `–` | – | center | – | – |
| S8 | Poppins | 12.0 | B | F7F7F7 | 0C142B | – | `mmm-yy` | right | center | 1.0 | – |
| S9 | Poppins | 14.0 |  | FFFFFF | 0C142B | – | `mmm-yy` | left | top | – | – |
| S10 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | right | center | 1.0 | – |
| S11 | Poppins | 12.0 |  | F9AB10 | 0C142B | – | `@` | right | center | 1.0 | – |
| S12 | Poppins | 12.0 |  | F7F7F7 | 0C142B | – | `@` | – | center | – | – |
| S13 | Calibri | 11.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S14 | Poppins | 12.0 |  | 333333 | – | – | `–` | left | center | 1.0 | wrap |
| S15 | Poppins | 12.0 |  | 333333 | – | – | `–` | center | – | – | wrap |
| S16 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | top | 1.0 | – |
| S17 | Poppins | 14.0 | B | 333333 | F2F2FB | – | `–` | left | – | 1.0 | – |
| S18 | Poppins | 12.0 |  | 001F37 | – | – | `–` | – | – | – | – |
| S19 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | – | 1.0 | – |
| S20 | Poppins | 14.0 | B | 333333 | – | B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S21 | Poppins | 14.0 | B | 333333 | – | – | `–` | left | center | 1.0 | – |
| S22 | Poppins | 12.0 |  | 001F37 | – | B:thin:9EA1AA | `–` | – | – | – | – |
| S23 | Calibri | 11.0 |  | 001F37 | – | R:thin:9EA1AA | `–` | – | – | – | – |
| S24 | Poppins | 12.0 |  | 333333 | – | L:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S25 | Poppins | 12.0 |  | 333333 | – | R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S26 | Poppins | 12.0 |  | 333333 | DFE0E3 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S27 | Poppins | 14.0 | B | 333333 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | left | center | 1.0 | – |
| S28 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `#,##0,\ "K"` | right | center | 1.0 | – |
| S29 | Poppins | 12.0 |  | 333333 | F0F1F4 | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `0.0%;\(0.0%\)` | right | center | 1.0 | – |
| S30 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA,R:thin:9EA1AA | `–` | – | – | – | – |
| S31 | Poppins | 12.0 |  | 4646CE | EAEAFF | L:thin:9EA1AA,R:thin:9EA1AA,T:thin:9EA1AA,B:thin:9EA1AA | `@` | left | center | 1.0 | – |
| S32 | Calibri | 11.0 |  | 001F37 | – | L:thin:9EA1AA | `–` | – | – | – | – |

## 4. Row templates (height + style per column run; rows sharing a template are styled identically)

- **T1** h=24.0 rows 1: A:B=S1 C:E=S2 F:K=S1 L=S3 M=S1
- **T2** h=24.0 rows 2: A:B=S1 C=S2 D:E=S4 F=S1 G:J=S5 K=S1 L=S4 M=S1
- **T3** h=8.25 rows 3: A:B=S1 C:E=S2 F=S1 G:I=S6 J:K=S1 L=S3 M=S1
- **T4** h=24.0 rows 4: A=S1 B=S7 C=S2 D:E=S8 F=S1 G:I=S8 J:K=S1 L=S3 M=S1
- **T5** h=24.0 rows 5: A=S1 B=S9 C=S2 D=S10 E=S11 F=S1 G=S10 H=S11 I=S10 J=S12 K=S1 L=S3 M=S1
- **T6** h=15.95 rows 6: A=S1 B=S9 C=S2 D:E=S10 F=S1 G:J=S10 K=S1 L=S3 M=S1
- **T7** h=24.0 rows 7: A:B=S13 C:D=S14 E=S15 F:M=S13
- **T8** h=24.0 rows 8: A=S13 B=S16 C:J=S17 K=S18 L=S19 M=S18
- **T9** h=24.0 rows 9: A=S13 B:E=S20 F=S21 G:J=S20 K=S18 L=S22 M=S18
- **T10** h=24.0 rows 10-28: A=S23 B=S24 C=S25 D:E=S26 F=S27 G:H=S26 I=S28 J=S29 K=S30 L=S31 M=S32

## 5. Cell contents and formulas

### 5.1 Constants (one line per row)

- r2: {"D": "MTD", "G": "YTD", "L": "Variance Explanation"}
- r4: {"B": "P&L - OpEx VA"}
- r5: {"D": "Actuals", "E": "Budget", "G": "Actuals", "H": "Budget", "I": "∆ vs Budget", "J": "% ∆ vs Budget"}
- r8: {"B": "Operating Expenses ex. D&A"}
- r10: {"B": "Airtable"}
- r11: {"B": "Asana"}
- r12: {"B": "DocuSign"}
- r13: {"B": "Dropbox"}
- r14: {"B": "Figma"}
- r15: {"B": "Freshworks"}
- r16: {"B": "GitHub"}
- r17: {"B": "Jellyfish"}
- r18: {"B": "Kimble"}
- r19: {"B": "Microsoft"}
- r20: {"B": "Monday.com"}
- r21: {"B": "NetSuite"}
- r22: {"B": "Notion"}
- r23: {"B": "Planhat"}
- r24: {"B": "SalesForce"}
- r25: {"B": "Slack"}
- r26: {"B": "Snowflake"}
- r27: {"B": "Trello"}
- r28: {"B": "Zoom"}

### 5.2 Formulas (same relative pattern for every listed cell)

- **F1** at D4, G4 (example `D4`): `=EOMONTH(DR_DATE_PICKER,0)`
- **F2** at E4, H4 (example `E4`): `=D4`
- **F3** at B5 (example `B5`): `=DR_DATE_PICKER`
- **F4** at D10:E28 (example `D10`): `=_xldudf_DR_GET(Value,"[Vendor]",$B10,"[Reporting Month]",D$4,"[Scenario]",D$5,"[Account Group L2]","Operating Expense")`
- **F5** at G10:H28 (example `G10`): `=_xldudf_DR_YTD(Value,"[Vendor]",$B10,"[Reporting Month]",G$4,"[Scenario]",G$5,"[Account Group L2]","Operating Expense")`
- **F6** at I10:I28 (example `I10`): `=IFERROR(D10-E10,"NA")`
- **F7** at J10:J28 (example `J10`): `=IFERROR(I10/D10,"")`

## 6. Pictures

- picture 1: logo `fpa-header` — displayed **240x35 px**, anchor B1(+5px,+29px)

## 7. Conditional formatting, sparklines

### 7.1 Conditional formats (add in priority order; formulas are relative to the FIRST cell of each range — select that cell first when using COM)

- [P1] **cell value equal** `"Budget"` → fontColor `F9AB10` — on H5 E5
  - json: `{"dxf": {"fontColor": "F9AB10"}, "formulas": ["\"Budget\""], "kind": "cellIs", "op": "equal", "priority": 1, "ranges": "H5 E5"}`
- [P5931] **icon set `3Triangles`** thresholds [percent 0; num 0; num 0] — on I10:I28
  - json: `{"iconSet": {"criteria": [{"gte": true, "type": "percent", "value": "0"}, {"gte": true, "type": "num", "value": "0"}, {"gte": true, "type": "num", "value": "0"}], "reverse": false, "showValue": true, "style": "3Triangles"}, "kind": "iconSet", "priority": 5931, "ranges": "I10:I28"}`

## 8. Adapt to the user's data

Row labels (account / department / entity names) are the template's demo labels: replace them with the org's real values and repeat each item row template per account; re-point SUM ranges; keep section titles, totals and column blocks; scenario, date and dimension values must exist in the org.
