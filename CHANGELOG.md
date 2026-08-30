# Changelog

Release notes for the Datarails Finance OS plugin for Claude.

## [3.4.2] — 2026-08-30

This release is about the accuracy of totals on large result sets, and about
the plugin working properly when you run it inside Excel.

### Fixed

- **Totals over large result sets are no longer under-counted.** When a query
  matched more rows than one response can carry, skills added up the rows they
  could see and presented that as the total. The figure was silently low, with
  nothing on screen to say it was partial — in one measured case a total built
  from 474 of 31,455 matching rows came to 21% of the true amount. Every skill
  that reports a total, a share or a percentage now reads the grand total the
  calculation engine returns alongside the rows, which covers all matching
  data however much of it came back. Sums, counts, minimums and maximums are
  exact this way.
- **Averages and distinct counts are derived correctly.** That grand total
  combines per-group results, which is right for a sum but wrong for an average
  (it would average the group averages, ignoring how many rows sit behind each)
  and wrong for a count of distinct values (a value appearing in several groups
  would be counted once per group). Measured against real data, those naive
  readings gave an average of 46,243 where the true figure was 26,052, and 14
  distinct values where there were 9. Averages are now derived from the total
  sum and total count, and distinct counts come from the dedicated lookup.
- **Drill-down works on a workbook that is not connected.** Drilling into a
  cell never required a connected workbook, but several skills said it did — so
  on a workbook reporting itself as unconnected they told you drill-down was
  unavailable and stopped, with the drill sitting there ready to run. Drilling
  now proceeds either way. A connection is still needed to create a dynamic
  range, which genuinely writes back.
- **A completed drill-down is no longer reported as a failure.** A drill writes
  its output to a new worksheet and returns an empty response; skills expecting
  the data in the response read that emptiness as an error and declared the
  drill failed after it had in fact succeeded. They now read the result from
  the sheet it was written to, and use the filter context in that sheet's first
  row to confirm the cell you meant was the cell drilled.
- **Formulas filled across a range are refreshed, not just the one you
  started from.** Copies of an already-resolved formula could stay pending and
  surface later as an error inside a total that summed them. The refresh now
  covers the whole written range, and figures are reported only once every cell
  in it has resolved to a number.
- **Workbook-producing skills behave correctly inside Excel.** The eight skills
  that build workbooks and decks — anomaly report, audit package, dashboard,
  departmental P&L, extract, insights deck, intelligence workbook and
  reconciliation — had no handling for running inside Excel and would take a
  route that only works outside it. Each now detects where it is running and
  chooses accordingly.

### Added

- **You are asked how a multi-period grid should be laid out before it is
  built.** Nothing previously required confirming the shape of a multi-period
  comparison, so a layout was chosen silently and your first sight of it was
  the finished sheet — and a wrong guess means rebuilding it, not reformatting
  it. The variance workflow now settles the layout with you first.
- **Drill-down says what it will leave behind before it runs.** Each drill adds
  a worksheet that stays in the workbook afterwards. The skill now tells you
  that up front and helps you keep or clear those sheets when you are done.
- **Formula building can write into the workbook you have open.** It previously
  produced formulas for you to place yourself. It can now insert them into the
  open workbook, refresh them, and read the values back, so what it reports is
  what the sheet actually shows.

### Changed

- **The formula authoring rules cover the whole retrieval family.** The rules
  that governed `DR.GET` apply equally to the period variants `DR.MTD`,
  `DR.QTD` and `DR.YTD`, and now say so — a period formula is written and
  refreshed exactly like the base one.

## [3.3.4] — 2026-08-09

The first release since 3.0.6. It focuses on the accuracy of the numbers the
skills report, and on making it clearer which skill answers which question.

### Fixed

- **Grouped query results are now read correctly.** Skills that summarise data
  by category, month, entity or account could previously double-count when a
  query grouped by more than one dimension, inflating totals, shares and
  trends. Every skill now reads these results correctly, so the figures it
  reports match the underlying data.
- **Table overviews profile your real business dimensions.** Asking for an
  overview of a table could return statistics about upload and mapping
  bookkeeping columns instead of your actual business fields. Overviews now
  always profile the dimensions that matter — accounts, scenario, entity,
  department, dates — and cover all of them rather than silently stopping at
  the first five.
- **Trends are computed at the right level.** In the financial-summary and
  intelligence workflows, a monthly trend built from data grouped by both month
  *and* account could treat a single account as the month's peak or repeat the
  same month when calculating growth. Both now total each month properly before
  computing direction, peaks and month-over-month change.
- **Data-quality checks count rows correctly.** Anomaly detection and the
  data-quality workbook derive their null rates, duplicate counts and
  rare-value thresholds from an accurate row total.
- **Audit evidence is scoped to the quarter you asked for.** The audit package
  applies its consistency checks to the audited quarter rather than the whole
  year, and its unmapped-account exception log now names the specific accounts
  involved — including cases where unmapped amounts offset to zero and were
  previously missed entirely.
- **Reconciliation's period-integrity check works again.** It compares the same
  window sliced two different ways, which is where its independence comes from.

### Changed

- **Each report skill states what it produces and for what period.** The four
  report generators previously described themselves in near-identical terms
  while covering very different spans — one month versus a full fiscal year.
  Each now says so up front: `dashboard` is a one-month KPI snapshot for the
  latest closed month, `insights` is a full-fiscal-year narrative deck,
  `intelligence` is a full-fiscal-year analysis workbook, and `extract` is a
  raw full-year data export. `dashboard` no longer describes itself as
  real-time, which it never was.
- **Related skills explain how they differ.** `tables` covers a table's schema
  while `profile` covers per-field statistics; `anomalies` answers in chat over
  the latest fiscal year while `anomalies-report` produces a workbook over the
  table's full history — so their counts are expected to differ, and both now
  say so. Skills also state which scenarios their figures cover.
- **Command shortcuts point at the right skill.** The `explore-tables`,
  `data-check`, `budget-comparison` and `test-api` shortcuts now resolve
  reliably to the skill they describe.

### Removed

- **The eight bundled agents.** Every one duplicated a same-named skill, and in
  several cases the agent was the less capable copy — one promised an Excel
  report it had no ability to write, another used different thresholds than the
  skill it mirrored. The skills remain and cover the same work: ask for anomaly
  detection, a dashboard, a reconciliation or a departmental P&L exactly as
  before and the matching skill runs. No capability is lost.

## [3.0.6] — 2026-07-13

Earlier releases were documented in the repository's release history.
