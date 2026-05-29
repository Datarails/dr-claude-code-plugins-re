# Datarails Brand Styling

Apply these styles when generating the Excel workbook with openpyxl.

## Font

Poppins (fall back to Calibri if unavailable). Weights: 400 regular, 600 semibold, 700 bold.

## Colors

| Role | Hex | Use |
|------|-----|-----|
| Navy | `0C142B` | Header/banner background |
| Main text | `333333` | Primary text |
| Secondary | `6D6E6F` | Muted/subtitle text |
| Border | `9EA1AA` | Cell borders |
| Section bg | `F2F2FB` | Section header / row header background (lavender) |
| Input bg | `EAEAFF` | Editable/input cell background |
| Input text | `4646CE` | Editable cell text (indigo) |
| Favorable | `2ECC71` | Positive variance / good KPI delta |
| Unfavorable | `E74C3C` | Negative variance / bad KPI delta |
| Severity CRITICAL | `C00000` | Critical insight banner |
| Severity WARNING | `ED7D31` | Warning insight banner |
| Severity POSITIVE | `70AD47` | Positive insight banner |
| Severity INFO | `5B9BD5` | Informational insight banner |
| Chart 1 | `0C142B` | Actuals (navy) |
| Chart 2 | `F93576` | Budget (hot pink) |
| Chart 3 | `00B4D8` | Teal |
| Chart 4 | `FFA30F` | Amber |

## Layout Rules

- Content starts at column B (column A is a narrow gutter).
- Rows 1-6: header banner with navy background, white title text, white subtitle.
- Gridlines OFF on every sheet. Freeze panes at B7.
- Footer as last row with generation date and "Datarails FP&A Intelligence Workbook".
- Every cell must have font, fill, alignment, and number format set.

## Number Formats

- Default: `_(* #,##0_);_(* (#,##0);_(* "-"_);_(@_)`
- Dollars: `$#,##0`
- Millions: `$#,##0.0,,"M"`
- Percent: `0.0%`

## Variance Coloring

Any cell showing a delta/change uses green (`2ECC71`) if favorable, red (`E74C3C`) if unfavorable.
