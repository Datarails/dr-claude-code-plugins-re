# Changelog

Release notes for the Datarails Finance OS plugin for Claude.

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
