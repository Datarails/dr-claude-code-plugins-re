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

**Ocean is a navy-banded card design, not a plain statement.** Getting this wrong is the
documented failure mode: an earlier version of this file described Ocean as "no banner, no
page fill, small grey type", a report built from it came out black-on-white with no logo,
and the verdict was *"it doesn't look like Ocean design"* / *"there are no colors"*.
Everything below is re-extracted with theme colours resolved -- see the trap immediately
below, which is why the first pass was wrong.

> ### The theme-colour trap -- read before re-extracting anything
>
> **Ocean's colours are theme colours, and openpyxl reports them as `None`.**
> `cell.font.color.rgb` returns `None` when `color.type == 'theme'`; only `color.theme`
> (an index) and `color.tint` are set. Treating that `None` as "no colour" silently
> deletes the entire palette -- which is exactly what happened.
>
> To resolve one: read `xl/theme/theme1.xml` -> `<a:clrScheme>`, map the index through
> **`[lt1, dk1, lt2, dk2, accent1...accent6, hlink, folHlink]`** (note `lt1`/`dk1` are
> swapped relative to a naive reading of the XML), then apply `tint` via HLS luminance:
> `L' = L*(1+tint)` when `tint < 0`, `L' = L*(1-tint) + tint` when `tint > 0`.
>
> The Ocean workbooks carry the **Datarails brand palette as their theme**:
> `dk1`/`dk2` `001F37`, `lt1`/`lt2` `F7F7F7`, `accent1` `0C142B`, `accent2` `F93576`,
> `accent3` `F9AB10`, `accent4` `F7F6F0`, `accent5` `00CC96`, `accent6` `1BC7EF`,
> `hlink` `4646CE`. Genesis does **not** -- it uses the stock Office theme and states its
> colours as direct RGB, which is why Genesis survived the first pass intact.
>
> Every hex in this file is already resolved. Use it literally; never re-derive.

One formatting vocabulary, five geometries -- and the same is true of Genesis below.
Neither look is a single sheet: profile one and you bake that sheet's flavour into every
report. `P&L - Ocean style`, `Balance Sheet - Ocean style`, `Cash Flow - Ocean style`,
`P&L - EBITDA JT style` and `Financial Statement - Summary` share the palette and band
structure below and differ only in grid.

## Ocean palette

| Token | Hex | Used for |
|---|---|---|
| Navy | `001F37` | Every header band; the vertical rule in gutter columns |
| Band text | `F7F7F7` | All text **on** a navy band |
| Page | `F7F7F7` | The body canvas -- every non-band cell in the block |
| Data cell | `FFFFFF` | DR.GET cells only -- they pop white against the page |
| Subtotal band | `DEDEDE` | The full-width stripe behind a subtotal / total row |
| Item text | `7F7F7F` | Line-item labels, variance columns |
| Data text | `3F3F3F` | DR.GET cell text |
| Subtotal text | `4D6ECD` | "Total ..." rows |
| Grand-total text | `253D84` | Gross Profit, Operating Income, Net Income |
| Margin text | `C55A11` | Margin / ratio rows |

## Ocean band structure

**The bands are the design, and they differ per variant.** A block with the right fonts
and no bands is the failure the user rejected. The exact fill map and row heights for every
variant are in **"Per-variant band structure"** below, generated from the source workbooks.
Read your variant's table and paint that; do not generalise from `ocean`, which is precisely
what the earlier version of this file got wrong.

Two fills that are easy to miss and very visible when absent:

- **A full-height rule fills the gutter column between period blocks** -- `001F37` in most
  Ocean variants, `D8D8D8` in Genesis. Which column varies (`I`, `J`, or two of them), and
  `ocean-ebitda` has none at all. Take it from your variant's table.
- **Subtotal rows are a `DEDEDE` stripe** spanning the block width, not merely bolder text.

## Ocean formatting

All Poppins. "navy" / "page" refer to the band structure above.

| Element | Font | Colour | Fill | Number format |
|---|---|---|---|---|
| Period title | 12 | `F7F7F7` | navy | `[$-409]yyyy\ mmmm;@` |
| Report title | 12 | `F7F7F7` | navy | -- |
| Units note | 9 | `F7F7F7` | navy | -- |
| "Month" label | 14 | `F7F7F7` | navy | -- |
| Period header | 9 | `F7F7F7` | navy | `[$-409]mmm\-yy`, bottom border |
| Scenario label | 9 | `F7F7F7` | navy | -- |
| Section header | **12** | `001F37` | page | bottom border, indent 0 |
| Sub-section header *(BS only)* | 10 | `001F37` | page | indent 0 |
| Line item label | 8 | `7F7F7F` | page | indent **3** |
| DR.GET data cell | 8 | `3F3F3F` | **`FFFFFF`** | `#,##0,\ "K"` |
| Subtotal ("Total ...") | 8 | **`4D6ECD`** | **`DEDEDE`** | `#,##0,\ "K"`, indent 3 |
| Grand total / Gross Profit | **9** | **`253D84`** | **`DEDEDE`** | `#,##0,\ "K"`, indent 1 |
| Margin / ratio row | 8 | `C55A11` | `DEDEDE` | `0.0%` |
| Variance delta column | 8 | `7F7F7F` | page | `#,##0,\ "K"` |
| Variance % column | 8 | `7F7F7F` | page | `0.0%;\(0.0%\)` |

## Logos

Committed under `references/assets/`. **Place every logo at native pixel size -- never
scale one.** The source templates place them 1:1, and a stretched logo was a specific user
complaint.

**Ocean uses two, in two places:**

| Asset | Native size | Placement |
|---|---|---|
| `datarails-logo-white-143x33.png` | **143 x 33** | `B1`, on the navy title band |
| `powered-by-datarails-364x48.png` | **364 x 48** | Footer, below the last body row, under the data columns |

The header mark is white-on-transparent -- legible **only** on the navy band, so if you
skip the band you must skip the logo too, and say so.

The footer's exact anchor **varies per source sheet** (observed at `H65`, `H66`, `P64`,
`I30` across the Ocean sheets), so it is positional rather than a fixed cell: put it a few
rows under the last body row, left-aligned with the first data column. Nothing keys off it.

**Genesis uses one, and it is a different asset in a different place** -- getting this
wrong by analogy with Ocean is easy:

| Asset | Native size | Placement |
|---|---|---|
| `powered-by-datarails-364x48.png` | **364 x 48** | **`B1`** -- in the *header*, not a footer |

Genesis has **no** white header mark and **no** footer image. It reuses the same
"Powered by Datarails" wordmark Ocean puts in its footer, but anchors it at `B1` on every
report sheet, where the navy-on-transparent artwork reads against the light `D8D8D8`
canvas. That is also why Genesis carries a white `B2` patch under it. Do not put Ocean's
white mark on Genesis -- it would be invisible on a light canvas.

**If the surface cannot insert an image, say so and build the rest.** A missing logo that
you reported is fine; a stretched or misplaced one is not, and silently omitting it while
claiming the Ocean look is the failure this section exists to prevent.

### Asset bytes (base64)

Reading a PNG with the file tools yields an image, not bytes, so the assets are inlined here for surfaces that need base64 (`shapes.addImage`). These are the same bytes as the files under `references/assets/`, which file-mode builds read from disk instead.

<details><summary><code>datarails-logo-white-143x33.png</code> (1972 chars)</summary>

```
iVBORw0KGgoAAAANSUhEUgAAAI8AAAAhCAYAAADgdfgNAAAACXBIWXMAACE3AAAhNwEzWJ96AAAFeElEQVR4nO2b3XGjPBSGn3yzwz0tsCV4TQWkBG8JdgeWSzAlxCXEJdgVMOsS4hLCtbnhu5BOpBDxGybx7uidYQxIR0eIo/OLH+q6JiBgCv777gkE/L0IwhMwGUF4Aibjx3dPIOD7UaVqBcTOrRK4AIuoyI+NvmvgHBX5NWieAIAEWABP5jcBMuC5SlUmncz5k2kLZisAoiLPgdxc5uZasHbOlUsXzFZAF65AVqUqwWqnqzQGzRPQhyNa+6yAg9sQNE9AHw7AyZz/QgsREDRPQA+iIr+gI69jVOTXd411XYcjHNR1zW25TRrXsfvbPH+o61lqWwvze5ljsIC/A3OYrRXwxxxZT9+Afwg+h3mP1SRtuAA7c5449xNP34AJqFIVo6OcDP0+Ymzm9wwcoiIve8ZIGmPQoL+20Q6Bz2yd6NcgZ+DRnMdogSuxAhXwCVSpUuiEXNzRrQQ2zfKBM8YC/S7bxiiBR+MQT0KX2doBDy3Ho9OvBDYEwZkFVaqe0JsxRofJj1GRP8gB/EZv3hhdPlh7xoixgnMEfjr0j2jtEwMn03cSujTPDpuy7kKMVYln576o2is2KynqU9TvUKmX7Gbi0InK9vGZm3+GNclX3j/nbLRG4+zN5SYq8kNH3zW6zgTw29VATts1KvKfHtoEeDGXu0Y5Yjg8Idup1lADQ7ystmgbZ1XX9Wv9Eae6rhcdYy+ccVy8OvNrm+8c/FULnct/FtrbchvfltvX23Jb35bbQWt/W26V6f/Scv/UQbu4LbdZMzwfc3xFhnmFrYkc0Ls+MfcztKb7xXutgaFxbfYRq25X6B06xEGfyv8JWxQU3jIvl//Gw3MK7do823WEJjigfaOkStXao6la1+czvo7gK4RngX7I5iJL2jtGL4Db7trsC9rOuy93Z2j29GMKf4V+mSXWx3AhQrc288pH0C5aaCVI8TrAPkRFXlapktqTGyELz8T4ULu+yGwKuhxm+aajeYwNx9uiMDfcbzp9sgtLtIPnCyndzwjm5i+fHuT4fZSzw7uNdtdC6/J1P3GYmmiVtXl7L0aruPN7rVL1XKVqbfydWdAlPGv0Dmkeqw4aH45Y59bXJnAfSnahmJk2tDqUn+CfYU1ll3BKNOo6pEJb9sxN2mLsswrPWTREVOQ73mu+FdqcvlSpOvmitLHoMltn2nfOGHQlotyFSngfFQ3hJZFU124ay98XOQ6F0JY0Ppz6DpgI7Gi0jUSa4utlVaoWUZH7fLZB6BOeaSHcfBiyC/uE5zuQMMwfc3HGvuAxgtursUwm+QBQpWqHtip7YF2l6tKVEujCvX7PU6IXZYhQ9JVSpmJy8oz3fs2QvvKboTXDmE0rbsQgi2Ac57xRuvinhOeMDbG7IInAuXm7Y7ftaF9y1KV1E5lDIGH3okpVFhV5r/YxScWEho9l/g2RAGWHVhFzPnn97vVjMFm4ZgjaxFjTMAQX7MJ2OZV7dADhzmEorQJqbJZXTItonGdTm2qFaX+LChuhuJjNfUf5wc16T8K9Cs8Bq4Z9hdoYeDb3Z89fYE3OHr/jK7kct+9QWvE3oGEuTITk1p1U8+VXqYqNxvlj+h08SUWJImM8AmQirXWj72jcq9kCnd85YZNqzRoV6MTeivm/IzqitYAkIiWhB3rHyq7d8NG5PZr7Tz20B/y+zaNDJ9pDeLimErTG+eBbRUV+rVIlc1gDqypVshndOeyGmMc23LPwSIJQdrn70JIEOzI+7zQUogUUtigrEIe4beEPaIFRfEysunP/AGN+Nk7mWJKzgtLQHrtefFTkhypVV+w/H9wxLmjBm6x1wF9Vv1e0Vc+/Au6OH+sIf4YWeKuCJ8BlapnB+EjxZzRNE3+T8ATcGf4H3+le8ycjhYwAAAAASUVORK5CYII=
```

</details>

<details><summary><code>powered-by-datarails-364x48.png</code> (8492 chars)</summary>

```
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
```

</details>

## What each column holds (`ocean`)

Widths alone do not say what goes where, and a block built to the right widths with the
wrong contents still reads as the wrong report. For `ocean`'s `P&L Periods` sheet:

| Column | Holds |
|---|---|
| `A` | hairline gutter (page fill) |
| `B` | row labels |
| `C` | hairline gutter |
| **`D`** | **current period** — header `=EOMONTH(DR_DATE_PICKER,0)`, scenario label `Actuals` |
| **`E`** | **comparison, prior year** — `=EOMONTH(D6,-12)` |
| `F` | gutter (2.0 wide) |
| **`G`** | **Δ vs PY** |
| **`H`** | **% Δ vs PY** |
| `I` | hairline — carries the **navy rule** separating the two blocks |
| **`J`** | second block, current — `=D6` |
| **`K`** | second block, prior year — `=EOMONTH(J6,-12)` |
| `L` | gutter |
| **`M`** | **Δ vs PY** |
| **`N`** | **% Δ vs PY** |

**Group labels sit in row 4** and name each block: `D4` is `Month`; `J4` on the source
sheet is **`QTD`** — not YTD. Take the second block's label from the report you are
actually building and say which you used; do not assume year-to-date because a second
block exists.

**The period title is a merged range, not a cell.** `D1:G1` (and `D2:G2`) are merged in the
source. At the preset's 14.1-character data width a `yyyy mmmm` date at 12 pt does not fit
a single cell and renders as `#######`. Merge the range first, then write and fill the
anchor — each variant's merged ranges are listed in its band table.

**A 12-month trend is not an Ocean geometry.** Ocean is period-vs-comparison blocks with
variance columns, not a monthly time series. If the user asks for monthly columns *and*
Ocean, **ask which they want** — twelve month columns stretched into this grid is neither
the preset nor a usable trend. Offer: the Ocean look with its period/comparison blocks, or
a monthly trend in `datarails-default`.

## Layout hygiene (every preset)

Three rules that decide whether a block reads as a report or as a spreadsheet. They apply
to all presets, not just `ocean`.

### Group labels are centred across their block

`Month`, `QTD`, `Year to Date` and the like span the whole block they title — a label
left-aligned in the first cell reads as a column header for that column alone.

**Use Center Across Selection**, not a merge:

```js
// in-sheet (Office.js)
sh.getRange("D4:H4").format.horizontalAlignment = "CenterAcrossSelection";
```

```python
# file mode (openpyxl) — same effect, set on every cell of the span
for col in range(4, 9):                      # D..H
    ws.cell(row=4, column=col).alignment = Alignment(horizontal="centerContinuous")
```

> The source workbooks *merge* these ranges (`D4:H4`, `J4:N4` on `ocean` — the band tables
> record that, because they record what the source **is**). Center Across Selection is the
> better way to build it: it looks identical and does not create merged cells, which break
> selection, copy-down and per-column insertion in a grid users will edit. This is a
> deliberate departure from the source; the period **title** (`D1:G1`) still merges,
> because that one is a single label with nothing to align across.

### Every column in the block gets a scenario-row header

Including the variance columns. A Δ column with no header is the one users misread.

| Column | Header |
|---|---|
| current period | the scenario — `Actuals` |
| comparison | the scenario it compares against — `Budget`, or `Actuals` for a prior-year column |
| Δ | **`vs Prior Year`** / **`vs Plan`** — name what it is measured against |
| % Δ | **`% vs Prior Year`** / **`% vs Plan`** |

Gutter columns take no header — on `ocean` that is `F` and `I`, and they are correctly
empty in the source. Everything else on the scenario row is labelled.

### Helper columns never appear on the report sheet

Monthly detail feeding a year-to-date figure, intermediate movement pulls, scratch
conversions — **none of it goes on the report sheet**, hidden or grouped. Hidden columns
inside a report block are still in its used range: they widen copies, surface in exports and
print ranges, and reappear the moment someone unhides a column.

Put them on a **separate, clearly titled sheet** (`<report name> - working`) with its own
header row naming each column, and reference across. The report sheet then contains exactly
the preset's columns and nothing else, and the working sheet is legible on its own rather
than being a wall of unlabelled numbers.

Say in Step 9 that a working sheet was created and what is on it.

## Ocean geometries

| Variant | Source template | Labels | Data cols | Title | Period hdr | Scenario row | First item | Freeze | Notes |
|---|---|---|---|---|---|---|---|---|---|
| `ocean` | P&L - Ocean style | **B** (32.6) | D, E | `D1`/`D2` | 6 | 7 | 10 | `D8` | Section header row 9; navy rule in `I` |
| `ocean-ebitda` | P&L - EBITDA JT style | **B** (**55.3**) | D, E | `D1`/`D2` | 6 | 7 | 11 | `D9` | Wide labels; **blank row between section header and first item** |
| `ocean-bs` | Balance Sheet - Ocean style | **B** (32.6) | D, **F** | `D1`/`D2` | 6 | 7 | 11 | `D17` | Adds the **sub-section tier** (Poppins 10); navy rule in `E` and `I` |
| `ocean-cf` | Cash Flow - Ocean style | **B** (32.6) | **E**, F | `E1`/`E2` | 6 | 7 | 9 | none | `C` widened to 4.1 as a sub-indent gutter; gridlines left **on** |
| `ocean-summary` | Financial Statement - Summary | **C** (20.0) | **E**, F | -- | 5 | 6-7 | 8 | none | One-screen summary: **no full title band** (navy only on the header rows), **no section tier** -- every line is an item row; inline ratios use `0%` |

Column widths (keep the hairline gutters -- with the navy rule, they are what separates the
period blocks):

- `ocean` / `ocean-ebitda`: `A` 0.4, `B` 32.6/55.3, `C` 0.6, `D` 14.1, `F` 2.0, `G` 14.1, `I` 0.4, `J` 14.1, `L` 2.0, `M` 14.1
- `ocean-bs`: `A` 0.4, `B` 32.6, `C` 0.6, `D` 15.6, `E` 0.4, `F` 14.7, `I` 0.4, `J` 14.7, `M` 0.4, `N` 14.7
- `ocean-cf`: `A` 0.4, `B` 32.6, `C` 4.1, `D` 0.6, `E` 12.7, `G` 2.0, `H` 12.7, `J` 0.4, `K` 14.1
- `ocean-summary`: `A` 6.9, `B` 7.6, `C` 20.0, `D` 1.1, `E` 11.4, `F` 13.7, `G` 1.9, `H` 14.4, `I` 9.6

**`ocean-summary` and `ocean-bs` carry a balance check.** The summary's BS sheet ends with
`=IFERROR(IF(ABS(<total_assets>-<total_liab_equity>)<1,"","OUT OF BALANCE"),"")` -- a
tie-out guard that stays silent when the statement balances. Reproduce it on any balance
sheet: it is the cheapest possible check that the row grouping did not drop or
double-count a line, and it costs one cell.

---

# The Genesis family

> **Genesis has a logo too** -- one image at `B1`, and it is *not* the asset Ocean puts
> there. See the **Logos** section above: Genesis uses the 364x48 "Powered by Datarails"
> wordmark in its header, and none of Ocean's white mark or footer placement applies.


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

# Per-variant band structure (generated from the source workbooks)

**These tables are generated from the template files, not transcribed.** The previous
hand-written version was accurate for `ocean` alone and wrong for every other variant --
different spacer heights, different body heights, a rule column in the wrong place or
absent entirely, and in one case a different white for the data cells. Each table below is
the literal fill map of its source sheet, and every variant has been rebuilt from these numbers
and diffed against the source.

`--` means **no fill at all** (Excel default). That is a real value, not a gap: `genesis`
deliberately leaves its report columns unfilled, and `ocean-summary` leaves `A:B` unfilled.
Do not "helpfully" paint them.

**Merges are resolved here.** openpyxl drops the fill of every cell in a merged range except
the top-left anchor, so reading the raw cells reports a merged band as *unfilled* -- which is
how an earlier version of this file came to show white gaps inside the navy title band. The
fills below are the **rendered** result, with each merge expanded from its anchor, and every
variant lists its merged ranges. Recreate the merges: a merged range takes its anchor's fill,
and merging after painting is what the source workbooks do.

## `ocean`

Source sheet `P&L Periods` - freeze **D8** - gridlines **off** - images **2**

Navy rule in `I`. Data cells `FFFFFF` in **both** period blocks (`D:E` and `J:K`).

Column widths (Excel character units): `A` 0.4, `B` 32.6, `C` 0.6, `D` 14.1, `F` 2.0, `G` 14.1, `I` 0.4, `J` 14.1, `L` 2.0, `M` 14.1, `O` 0.4, `P` 14.1, `R` 2.0, `S` 14.1, `U` 1.4, `V` 41.9, `W` 9.1, `X` 11.0

Full-height fills, rows 10-20: `A` F7F7F7, `I` 001F37

**Merged ranges: `D1:G1`, `D2:G2`, `D4:H4`, `J4:N4`, `P4:T4`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **20.1** | `A:N` 001F37 |
| 2 | **20.1** | `A:N` 001F37 |
| 3 | **4.5** | `A:N` F7F7F7 |
| 4 | **26.25** | `A:B` 001F37, `C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 5 | **3.75** | `A:N` F7F7F7 |
| 6 | **24.0** | `A:C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 7 | **17.45** | `A:C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 8 | **8.25** | `A:N` F7F7F7 |
| 9 | **21.0** | `A:H` F7F7F7, `I` 001F37, `J:N` F7F7F7 |
| 10 | **21.0** | `A:C` F7F7F7, `D:E` FFFFFF, `F:H` F7F7F7, `I` 001F37, `J:K` FFFFFF, `L:N` F7F7F7 |
| 11 | **21.0** | `A:C` F7F7F7, `D:E` FFFFFF, `F:H` F7F7F7, `I` 001F37, `J:K` FFFFFF, `L:N` F7F7F7 |
| 12 | **21.0** | `A:H` F7F7F7, `I` 001F37, `J:N` F7F7F7 |
| 13 | **21.0** | `A` F7F7F7, `B:H` DEDEDE, `I` 001F37, `J:N` DEDEDE |
| 14 | **21.0** | `A:H` F7F7F7, `I` 001F37, `J:N` F7F7F7 |

## `ocean-ebitda`

Source sheet `P&L Periods` - freeze **D9** - gridlines **off** - images **2**

**No navy rule** -- every gutter is page fill. Body rows are 22.5, and rows 9-10 stay empty page before the first item at row 11.

Column widths (Excel character units): `A` 0.4, `B` 55.3, `C` 0.7, `D` 14.1, `F` 2.0, `G` 14.1, `I` 0.7, `J` 14.1, `L` 2.0, `M` 14.1, `O` 0.7, `P` 14.1, `R` 2.0, `S` 14.1, `U` 0.7, `V` 41.9, `W` 9.1, `X` 10.4

Full-height fills, rows 10-20: `A` F7F7F7, `C` F7F7F7, `I` F7F7F7

**Merged ranges: `D1:G1`, `D2:G2`, `D4:H4`, `J4:N4`, `P4:T4`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **20.1** | `A:N` 001F37 |
| 2 | **20.1** | `A:N` 001F37 |
| 3 | **3.75** | `A:N` F7F7F7 |
| 4 | **26.25** | `A:B` 001F37, `C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 5 | **3.75** | `A:N` F7F7F7 |
| 6 | **24.0** | `A:C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 7 | **17.45** | `A:C` F7F7F7, `D:H` 001F37, `I` F7F7F7, `J:N` 001F37 |
| 8 | **8.25** | `A:N` F7F7F7 |
| 9 | **22.5** | `A:N` F7F7F7 |
| 10 | **22.5** | `A:N` F7F7F7 |
| 11 | **22.5** | `A:C` F7F7F7, `D:E` FFFFFF, `F:I` F7F7F7, `J:K` FFFFFF, `L:N` F7F7F7 |
| 12 | **22.5** | `A:N` F7F7F7 |
| 13 | **22.5** | `A` F7F7F7, `B` DEDEDE, `C` F7F7F7, `D:H` DEDEDE, `I` F7F7F7, `J:N` DEDEDE |
| 14 | **22.5** | `A:N` F7F7F7 |

## `ocean-bs`

Source sheet `Summary` - freeze **D17** - gridlines **off** - images **2**

**Two** navy rules (`E` and `I`). Data cells are **`FDFDFC`**, not `FFFFFF`. Row 4 is 28.5, taller than in the other variants.

Column widths (Excel character units): `A` 0.4, `B` 32.6, `C` 0.6, `D` 15.6, `E` 0.4, `F` 14.7, `I` 0.4, `J` 14.7, `M` 0.4, `N` 14.7, `Q` 1.4, `R` 54.4, `S` 11.0

Full-height fills, rows 10-20: `A` F7F7F7, `E` 001F37, `I` 001F37, `M` 001F37

**Merged ranges: `D1:G1`, `D2:G2`, `F4:H4`, `F5:H5`, `F6:H6`, `J4:L4`, `J5:L5`, `J6:L6`, `N4:P4`, `N5:P5`, `N6:P6`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **20.1** | `A:N` 001F37 |
| 2 | **20.1** | `A:N` 001F37 |
| 3 | **4.5** | `A:N` F7F7F7 |
| 4 | **28.5** | `A:B` 001F37, `C` --, `D` 001F37, `E` F7F7F7, `F:H` 001F37, `I` F7F7F7, `J:L` 001F37, `M` F7F7F7, `N` 001F37 |
| 5 | **3.75** | `A:B` F7F7F7, `C` --, `D:N` F7F7F7 |
| 6 | **24.0** | `A:B` F7F7F7, `C` --, `D` 001F37, `E` F7F7F7, `F:H` 001F37, `I` F7F7F7, `J:L` 001F37, `M` F7F7F7, `N` 001F37 |
| 7 | **17.45** | `A:B` F7F7F7, `C` --, `D` 001F37, `E` F7F7F7, `F:H` 001F37, `I` F7F7F7, `J:L` 001F37, `M` F7F7F7, `N` 001F37 |
| 8 | **8.25** | `A:B` F7F7F7, `C` --, `D:E` F7F7F7, `F:H` --, `I:N` F7F7F7 |
| 9 | **21.0** | `A:B` F7F7F7, `C` --, `D` F7F7F7, `E` 001F37, `F:H` F7F7F7, `I` 001F37, `J:L` F7F7F7, `M` 001F37, `N` F7F7F7 |
| 10 | **21.0** | `A:B` F7F7F7, `C` --, `D` F7F7F7, `E` 001F37, `F:H` F7F7F7, `I` 001F37, `J:L` F7F7F7, `M` 001F37, `N` F7F7F7 |
| 11 | **21.0** | `A:B` F7F7F7, `C` --, `D` FDFDFC, `E` 001F37, `F` --, `G:H` F7F7F7, `I` 001F37, `J` --, `K:L` F7F7F7, `M` 001F37, `N` -- |
| 12 | **21.0** | `A:B` F7F7F7, `C` --, `D` FDFDFC, `E` 001F37, `F` --, `G:H` F7F7F7, `I` 001F37, `J` --, `K:L` F7F7F7, `M` 001F37, `N` -- |
| 13 | **21.0** | `A:B` F7F7F7, `C` --, `D` FDFDFC, `E` 001F37, `F` --, `G:H` F7F7F7, `I` 001F37, `J` --, `K:L` F7F7F7, `M` 001F37, `N` -- |
| 14 | **21.0** | `A:B` F7F7F7, `C` --, `D` FDFDFC, `E` 001F37, `F` --, `G:H` F7F7F7, `I` 001F37, `J` --, `K:L` F7F7F7, `M` 001F37, `N` -- |

## `ocean-cf`

Source sheet `Cash Flow Periods` - freeze **none** - gridlines **on** - images **2**

Navy rule in **`J`**. Gridlines left **on**. Subtotal stripe lands at row 9, directly under the header. Row 7 is 17.65.

Column widths (Excel character units): `A` 0.4, `B` 32.6, `C` 4.1, `D` 0.6, `E` 12.7, `G` 2.0, `H` 12.7, `J` 0.4, `K` 14.1, `M` 2.0, `N` 14.1, `P` 0.4, `Q` 14.1, `S` 2.0, `T` 14.1, `V` 8.7

Full-height fills, rows 10-20: `A` F7F7F7, `J` 001F37

**Merged ranges: `E1:I1`, `E2:I2`, `E4:I4`, `K4:O4`, `Q4:U4`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **20.1** | `A:N` 001F37 |
| 2 | **20.1** | `A:N` 001F37 |
| 3 | **4.5** | `A:N` F7F7F7 |
| 4 | **26.25** | `A:C` 001F37, `D` --, `E:I` 001F37, `J` F7F7F7, `K:N` 001F37 |
| 5 | **3.75** | `A:C` F7F7F7, `D` --, `E:N` F7F7F7 |
| 6 | **24.0** | `A:C` F7F7F7, `D` --, `E:I` 001F37, `J` F7F7F7, `K:N` 001F37 |
| 7 | **17.65** | `A:C` F7F7F7, `D` --, `E:I` 001F37, `J` F7F7F7, `K:N` 001F37 |
| 8 | **8.25** | `A:C` F7F7F7, `D` --, `E:N` F7F7F7 |
| 9 | **21.75** | `A` F7F7F7, `B:C` DEDEDE, `D` --, `E:I` DEDEDE, `J` 001F37, `K:N` DEDEDE |
| 10 | **21.75** | `A:C` F7F7F7, `D` --, `E:I` F7F7F7, `J` 001F37, `K:N` F7F7F7 |
| 11 | **21.75** | `A:C` F7F7F7, `D` --, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 12 | **21.75** | `A:C` F7F7F7, `D` --, `E:I` F7F7F7, `J` 001F37, `K:N` F7F7F7 |
| 13 | **21.75** | `A:C` F7F7F7, `D` --, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 14 | **21.75** | `A:C` F7F7F7, `D` --, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |

## `ocean-summary`

Source sheet `P&L` - freeze **none** - gridlines **off** - images **1**

Navy rule in **`J`**. **No title band** -- rows 1-4 carry no fill; navy appears only at `C5`/`E5`, across `E6:I6`, and as a full band `E7:L7`. Columns `A:B` stay unfilled.

Column widths (Excel character units): `A` 6.9, `B` 7.6, `C` 20.0, `D` 1.1, `E` 11.4, `F` 13.7, `G` 1.9, `H` 14.4, `I` 9.6, `J` 1.4, `K` 12.7, `L` 12.1, `M` 1.9, `N` 13.4, `O` 9.6

Full-height fills, rows 10-20: `J` 001F37

**Merged ranges: `E5:I5`, `K5:O5`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **15.0** | `A:N` -- |
| 2 | -- | `A:N` -- |
| 3 | **15.0** | `A:B` --, `C` F7F7F7, `D:N` -- |
| 4 | **15.0** | `A:N` -- |
| 5 | **18.75** | `A:B` --, `C` 001F37, `D` --, `E:I` 001F37, `J` --, `K:N` 001F37 |
| 6 | **19.5** | `A:D` --, `E:I` 001F37, `J` --, `K:N` 001F37 |
| 7 | **24.0** | `A:B` --, `C:D` F7F7F7, `E:N` 001F37 |
| 8 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 9 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 10 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 11 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 12 | **6.75** | `A:B` --, `C:I` F7F7F7, `J` 001F37, `K:N` F7F7F7 |
| 13 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |
| 14 | **17.25** | `A:B` --, `C:D` F7F7F7, `E:F` FFFFFF, `G:I` F7F7F7, `J` 001F37, `K:L` FFFFFF, `M:N` F7F7F7 |

## `genesis`

Source sheet `P&L Rolling 12 month` - freeze **D5** - gridlines **off** - images **1**

**The body is unfilled** -- the `D8D8D8` canvas covers row 1 and the gutter columns `A`/`C` only; report columns `D` onward keep Excel default. The logo sits on a white `B2` patch. Title bar `1F3864` at `D2`; header band `ECECEC` across rows 3-4.

Column widths (Excel character units): `A` 3.1, `B` 32.7, `C` 0.4, `D` 9.6, `Q` 3.1, `R` 10.0, `S` 9.1

Full-height fills, rows 10-20: `A` D8D8D8, `C` D8D8D8

**Merged ranges: `B2:B3`, `D2:P2`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **30.0** | `A:C` D9D9D9, `D:N` D8D8D8 |
| 2 | **30.75** | `A` D8D8D8, `B` FFFFFF, `C` D8D8D8, `D:N` 1F3864 |
| 3 | **21.75** | `A` D8D8D8, `B` FFFFFF, `C` D8D8D8, `D:N` ECECEC |
| 4 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` ECECEC |
| 5 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 6 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 7 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 8 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 9 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 10 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 11 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 12 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 13 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |
| 14 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:N` -- |

## `genesis-bva`

Source sheet `P&L Periods BVA` - freeze **D5** - gridlines **off** - images **1**

As `genesis`, plus a second block: `D8D8D8` rule in `I`, header band continuing across `J:L`, and an accent `4472C4` patch at `J2`.

Column widths (Excel character units): `A` 3.1, `B` 32.9, `C` 0.4, `D` 12.9, `E` 9.6, `F` 3.9, `G` 12.1, `H` 14.1, `I` 1.1, `J` 10.6, `K` 10.1, `L` 4.0, `M` 12.1, `N` 14.1, `O` 1.1, `P` 9.4, `Q` 10.6, `R` 2.4, `S` 12.6, `T` 14.1, `U` 1.1, `V` 9.1

Full-height fills, rows 10-20: `A` D8D8D8, `I` D8D8D8

**Merged ranges: `B2:B3`, `D2:H2`, `J2:N2`, `P2:T2`** -- recreate these. A merged range renders with its anchor cell's fill, so merge first, then fill the anchor.

| Row | Height | Fills across `A:N` |
|---|---|---|
| 1 | **25.5** | `A:N` D8D8D8 |
| 2 | **30.75** | `A` D8D8D8, `B` FFFFFF, `C` D8D8D8, `D:H` 1F3864, `I` D8D8D8, `J:N` 4472C4 |
| 3 | **21.75** | `A` D8D8D8, `B` FFFFFF, `C` D8D8D8, `D:H` ECECEC, `I` D8D8D8, `J:N` ECECEC |
| 4 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` ECECEC, `I` D8D8D8, `J:N` ECECEC |
| 5 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 6 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 7 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 8 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 9 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 10 | **21.75** | `A` D8D8D8, `B:H` --, `I` D8D8D8, `J:N` -- |
| 11 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 12 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 13 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |
| 14 | **21.75** | `A` D8D8D8, `B` --, `C` D8D8D8, `D:H` --, `I` D8D8D8, `J:N` -- |

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
- **`DR_DATE_PICKER` is shared with the add-in.** The preset drives its headers off
  that name, and the add-in's own reference-date commands use the same one, so
  pointing it at the report's period cell also moves what those commands act on.
  Usually what you want — but **say you created or repointed it** rather than
  leaving it to be discovered. *(Observed on a live add-in run.)*
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
