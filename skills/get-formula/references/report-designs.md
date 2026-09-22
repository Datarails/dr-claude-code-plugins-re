# Report design presets

The looks `get-formula` Step 6.5b offers. Apply exactly one preset whole — never blend two.

Every value below was extracted from the shipped Datarails Template Library workbooks
(the `Datarails templates` filebox folder) by reading their real report sheets with
openpyxl. **They are product design, not client data** — no account name, dimension value
or figure from the source workbooks is reproduced here, and none may be: rows always come
from `<row_level_field>`'s validated registry and numbers always from a fresh DR.GET.

> **Read the source sheets, not the pivot sheets — and read *all* of them.** Every template
> also carries `Dr_Pivot_Template N` sheets (drill-output artifacts in default Calibri),
> excluded from every profile below. Two report sheets are excluded too, and named where
> they belong: `KPI for Dashboard` (a widget-authoring workbook) and Genesis's
> `P&L Summary by Entity` (unstyled Calibri). Both looks turned out to vary **across** their
> own report sheets, so each is documented as a family with a base variant.

**Geometry is per-preset, and the DR.GET reference map follows it.** Phase 3's Cell
reference map describes `datarails-default` only. Under any Datarails-template preset the
labels sit in a different column and the header rows move, so derive every reference from
the chosen variant's geometry row. This is the one place the Cell reference map is a
**variable, not a constant** — safe only because each variant states its whole grid.

---

## `datarails-default` — Datarails brand styling

SKILL.md § "Datarails Brand Styling", and the default when nobody is asked. Geometry is
the Phase 3 Cell reference map as written: block at A1 on a new sheet, labels in column A,
parameter cells `$B$1`–`$B$3`, date headers in row 5.

## `plain`

Values and number formats only — `#,##0` on data, `0.0%` on percents. No fonts, fills,
borders or width changes. Geometry is `datarails-default`'s.

---

# The Ocean family

**One formatting vocabulary, five geometries** — and the same is true of Genesis below.
Neither look is a single sheet: profile one and you bake that sheet's flavour into every
report. `P&L - Ocean style`,
`Balance Sheet - Ocean style`, `Cash Flow - Ocean style`, `P&L - EBITDA JT style` and
`Financial Statement - Summary` all share the formatting table below and differ only in
grid. Pick the variant that matches the statement being built.

Reads as a quiet printed statement: no banner, no page fill, hairline gutters between
period blocks, small grey type.

## Ocean formatting (all variants)

| Element | Font | Colour | Fill | Number format |
|---|---|---|---|---|
| Period title | Poppins 12 | default | — | `[$-409]yyyy\ mmmm;@` |
| Report title | Poppins 12 | default | — | — |
| Units note | Poppins 9 | default | — | — |
| "Month" / period-group label | Poppins 14 | default | — | — |
| Period header | Poppins 9 | default | — | `[$-409]mmm\-yy`, bottom border |
| Scenario label | Poppins 9 | default | — | — |
| Section header | Poppins **12** | default | — | bottom border, indent 0 |
| Sub-section header *(BS only)* | Poppins 10 | default | — | indent 0 |
| Line item label | Poppins 8 | `FF7F7F7F` | — | indent **3** |
| DR.GET data cell | Poppins 8 | `FF3F3F3F` | `FFFFFFFF` | `#,##0,\ "K"` |
| Subtotal ("Total …") | Poppins 8 | default | — | `#,##0,\ "K"`, indent 3 |
| Grand total / Gross Profit | Poppins **9** | default | — | `#,##0,\ "K"`, indent 1 |
| Margin / ratio row | Poppins 8 | **`FFC55A11`** | — | `0.0%` |
| Variance Δ column | Poppins 8 | `FF7F7F7F` | — | `#,##0,\ "K"` |
| Variance % column | Poppins 8 | `FF7F7F7F` | — | `0.0%;\(0.0%\)` |

## Ocean geometries

| Variant | Source template | Labels | Data cols | Title | Period hdr | Scenario row | First item | Freeze | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `ocean` | P&L - Ocean style | **B** (32.6) | D, E | `D1`/`D2` | 6 | 7 | 10 | `D8` | Section header row 9 |
| `ocean-ebitda` | P&L - EBITDA JT style | **B** (**55.3**) | D, E | `D1`/`D2` | 6 | 7 | 11 | `D9` | Wide labels; **blank row between section header and first item** |
| `ocean-bs` | Balance Sheet - Ocean style | **B** (32.6) | D, **F** | `D1`/`D2` | 6 | 7 | 11 | `D17` | Adds the **sub-section tier** (Poppins 10) between section and items |
| `ocean-cf` | Cash Flow - Ocean style | **B** (32.6) | **E**, F | `E1`/`E2` | 6 | 7 | 9 | none | `C` widened to 4.1 as a sub-indent gutter; gridlines left **on** |
| `ocean-summary` | Financial Statement - Summary | **C** (20.0) | **E**, F | — | 5 | 6–7 | 8 | none | One-screen summary: **no section tier at all** — every line is an item row; inline ratio rows use `0%`, not `0.0%` |

Column widths (keep the hairline gutters — they are what makes the style read as separated
blocks rather than one wide grid):

- `ocean` / `ocean-ebitda`: `A` 0.4, `B` 32.6/55.3, `C` 0.6, `D` 14.1, `F` 2.0, `G` 14.1, `I` 0.4, `J` 14.1, `L` 2.0, `M` 14.1
- `ocean-bs`: `A` 0.4, `B` 32.6, `C` 0.6, `D` 15.6, `E` 0.4, `F` 14.7, `I` 0.4, `J` 14.7, `M` 0.4, `N` 14.7
- `ocean-cf`: `A` 0.4, `B` 32.6, `C` 4.1, `D` 0.6, `E` 12.7, `G` 2.0, `H` 12.7, `J` 0.4, `K` 14.1
- `ocean-summary`: `A` 6.9, `B` 7.6, `C` 20.0, `D` 1.1, `E` 11.4, `F` 13.7, `G` 1.9, `H` 14.4, `I` 9.6

**`ocean-summary` and `ocean-bs` carry a balance check.** The summary's BS sheet ends with
`=IFERROR(IF(ABS(<total_assets>-<total_liab_equity>)<1,"","OUT OF BALANCE"),"")` — a
tie-out guard that stays silent when the statement balances. Reproduce it on any balance
sheet: it is the cheapest possible check that the row grouping did not drop or double-count
a line, and it costs one cell.

---

# The Genesis family

**`P&L - Genesis Style`, and like Ocean it is a family.** Four of its five report sheets
share one sizing; the budget-vs-actual sheet runs a size larger because it carries KPI rows.
Same trap as Ocean: profiling a single sheet and calling it "the Genesis spec" bakes one
sheet's flavour into every report.

The one genuinely different look in the library: a dark navy title bar on a light grey page
canvas, blue bold subtotals. Reads as a management pack rather than a statement.

## Genesis formatting

`genesis` is the base. `genesis-bva` differs **only** in the three rows marked ★.

| Element | Font | Colour | Fill | Number format |
|---|---|---|---|---|
| Title bar | Poppins **16 bold** | default | **`FF1F3864`** | `[$-409]mmm\-yy`, top+bottom border |
| Period header | Poppins 10 **bold** | `FF44546A` | `FFECECEC` | `[$-409]mmm\-yy`, top border |
| Scenario label | Poppins 10 **bold** | `FF44546A` | `FFECECEC` | bottom border |
| Units note (`B4`) | Poppins 10 **bold** | `FF000090` | — | top+bottom border |
| ★ Section header | Poppins 10 **bold** — *`genesis-bva`: **11 bold*** | **`FF000090`** | — | indent 0 |
| ★ Line item label | Poppins 10, indent **0** — *`genesis-bva`: indent **1*** | `FF7F7F7F` | — | — |
| ★ Subtotal ("Total …") | Poppins 10 **bold** — *`genesis-bva`: **11 bold*** | **`FF000090`** | — | `#,##0,\ "K"` |
| DR.GET data cell | Poppins 10 | `FF7F7F7F` | — | `#,##0,\ "K"` |
| KPI row (e.g. Revenue/FTE) | Poppins 11 | `FF000090` | — | `#,##0,\ "K"` |
| Variance Δ / % Δ | Poppins 10 | `FF7F7F7F` | — | `#,##0,\ "K"` / `0.0%;\(0.0%\)` |

**Use `genesis-bva` only for an actual-vs-budget report**, and only there — its larger
headings exist to hold the KPI block (FTE, Revenue/FTE) that sits under Total Revenue. A
plain P&L in `genesis-bva` sizing looks subtly wrong: headings a point too large for a sheet
with no KPI rows to balance them. Default to `genesis`.

## Genesis geometries

Labels are always in **B**, data starts at **D**, title bar `D2`, period headers row **3**,
scenario labels row **4**, section header row **6**, first item row **7**, gridlines off.
What varies:

| Variant | Source sheet | Freeze | `B` | `C` | `D` | Notes |
|---|---|---|---|---|---|---|
| `genesis` | P&L Rolling 12 month | `D5` | 32.7 | 0.4 | 9.6 | The base sizing |
| `genesis` | P&L YOY | `D16` | 32.9 | 0.4 | 10.6 | |
| `genesis` | P&L Multi-Year Overview | `D17` | 32.9 | **2.9** | 10.4 | Wider gutter between labels and data |
| `genesis-bva` | P&L Periods BVA | `D5` | 32.9 | 0.4 | 12.9 | KPI rows; ★ sizing above |

Pick the freeze row from where the report's own header band ends — the three base sheets
disagree (`D5`/`D16`/`D17`) because each carries a different amount of preamble above the
grid, not because the style demands a particular row. Freeze immediately below the
scenario-label row of the block you actually wrote.

**Page canvas:** fill the whole used sheet area `FFD8D8D8` and leave the report columns
unfilled, so the grid reads as a card on a grey page. This is the trait that identifies
Genesis at a glance — without it the preset is just a bold Ocean.

**`P&L Summary by Entity` is not a design source.** It is **Calibri**, unstyled, with entity
codes down column B — an entity pivot that never got the Genesis treatment. Do not profile
it, and do not treat its Calibri as evidence that Genesis permits a non-Poppins fallback.

---

# Conventions shared by every Datarails-template preset

Carry these whenever any `ocean-*` or `genesis` preset is chosen — they are what make the
output look Datarails-native rather than merely similar.

- **Poppins throughout.** Fall back to Calibri only if Poppins is unavailable, and say so.
- **Thousands with a K suffix:** `#,##0,\ "K"` on every currency cell, not `#,##0`.
- **Variance percent** is `0.0%;\(0.0%\)` — negatives in parentheses, not a minus sign.
- **Date headers** are `[$-409]mmm\-yy`.
- **Gridlines off** and freeze panes below the scenario-label row (except `ocean-cf` /
  `ocean-summary`, which ship unfrozen — see the geometry table).
- **Period headers are formulas off one date anchor**, never typed serials. Every template
  defines `DR_DATE_PICKER` and drives all headers from it: `=EOMONTH(DR_DATE_PICKER,0)`
  for the current period, then `=EOMONTH(D<row>,-12)` for prior year, `=EOMONTH(D<row>,-1)`
  for prior month, or `=D<row>` for a same-period budget column. Reproduce that: add the
  `DR_DATE_PICKER` workbook name, point it at the report's period cell, and one edit
  re-dates the whole report. If you write literal serials instead, **say so** — the user
  loses the single-cell repoint these templates are built around.
- **Variance layout** is `value │ value │ (spacer) │ Δ │ % Δ`, Δ columns at the right of
  each block — the side-by-side shape `CLAUDE.md` mandates for multi-period grids.
- **`IFERROR(…,"NA")` wraps calculated cells** — subtotals, Δ, % Δ, margins — so a gap
  reads as `NA` rather than `#DIV/0!`. **DR.GET cells stay bare**, exactly as the DR.GET
  authoring contract requires. The source templates do this too, so matching the design
  and honouring the contract never conflict.
- **The XL function token is not always `Value`.** The EBITDA template's formulas call a
  `Value_EBITDA`-style token instead. That is Step 2.3's `<value_function>` discovery doing
  real work — use the token you discovered, never the one written in a preset example.

## Deliberately not a preset

**`KPI for Dashboard`** is not a report design — it is a widget-authoring workbook (Calibri,
an `FFE7F4FF` "Fill in Cells" input band, sheets named for metric polarity, a widget-size
backlog). Offering it as a report look would produce something that resembles a form, not a
statement. If a user asks for it by name, say what it actually is and point them at
`/dr-dashboard`.
