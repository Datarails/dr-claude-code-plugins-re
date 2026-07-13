---
name: dr-query
description: Query Datarails Finance OS tables with filters. Fetch specific records or page through rows for investigation. The filter API supports value-list AND advanced operators — comparisons, ranges, text matching, null checks, and date ranges all work.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__start_aggregation_by_alias
  - mcp__datarails-finance-os__get_aggregation_result_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__start_aggregation_by_id
  - mcp__datarails-finance-os__get_aggregation_result_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__start_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_result_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__start_distinct_values_by_id
  - mcp__datarails-finance-os__get_distinct_values_result_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_id
argument-hint: "<table or alias> [filter_expression] [--sample] [--limit N]"
---

# Datarails Data Query

Query Finance OS tables — fetch records by filter, sample rows, or page through
data. The filter API supports both value-list and advanced (comparison / range /
text / null / date-range) operators, so most questions can be answered with a
single `get_data_by_*` call.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide
the user to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect).

### Step 2: Resolve the table and its fields

`list_data_models` to find the table by name or alias. **Prefer the alias path**
when the table has an alias: `list_aliased_fields(<alias>)` gives friendly field
names and you query with `get_data_by_alias`. Otherwise `get_fields_by_id(<id>)`
gives numeric field ids and you query with `get_data_by_id` (`select` and
`filters` are field-id based). Always `select` only the columns you need — raw
tables can be hundreds of columns wide in some orgs.

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

### Step 3: Pick the right tool

- **Sample / quick look** → `get_data_by_alias` / `get_data_by_id` with a small
  `limit` (e.g. 20) and no filters.
- **Filtered records** → `get_data_by_alias` / `get_data_by_id` with `filters`
  (≤500 rows/page; use `offset` to page).
- **Totals / grouped** → `start_aggregation_by_alias` / `start_aggregation_by_id`
  (same dimensions/metrics/filters arguments; no row cap) → poll the matching
  `get_aggregation_result_by_alias` / `get_aggregation_result_by_id` with the
  returned `handle` until ready (async-fetch pattern). Use this when you want a
  sum/count rather than individual rows.

### Step 4: Execute and Present

Format results as a readable table. Highlight any notable patterns. If a result
is empty, say so plainly (it may be a too-narrow filter, not missing data). If a
response carries `"truncated": true`, the returned rows are an incomplete
prefix — narrow the query per the `guidance` (more filters / fewer columns /
lower limit+offset paging) and re-fetch; never present the prefix as complete.

## Arguments

| Argument | Description |
|----------|-------------|
| `<table or alias>` | Required — the table id or alias to query |
| `[filter]` | Filter expression (see syntax below) |
| `--sample` | Fetch a small unfiltered page (default 20 rows) |
| `--limit N` | Limit results (max 500 per page; use offset to page further) |

## Filter syntax

`filters` is a list of per-field objects. Address the field by **alias** (`name`)
for the by-alias tools, or by numeric **field id** (`field_id`) for the by-id
tools. Two forms:

**Value list** — match any of the listed values (set membership / IN):
```json
{"name": "payment_status", "values": ["Paid", "Pending"]}
```
Set `"is_excluded": true` to exclude the listed values (NOT IN).

**Advanced** — a condition tree for comparisons, ranges, text matching, and null:
```json
{"name": "amount", "values": {"type": "advanced", "val": [
    {"condition": "gte", "value": "1000"},
    {"condition": "lt",  "value": "5000", "operator": "and"}
]}}
```

Each `val` entry is `{condition, value, operator?}`:
- **condition**: `equals`, `dn_equals` (does not equal), `contains`,
  `dn_contains`, `bw` (begins with), `ew` (ends with), `gt`, `gte`, `lt`, `lte`,
  `in`, `range` (exclusive between), `total_range` (inclusive between), `is null`.
- **value**: a string for scalar conditions; a list of strings for `in`; a
  two-item `[from, to]` list for `range`/`total_range`. Numbers and dates are
  passed as strings (dates as epoch seconds, e.g. `"1750000000"`); the backend
  casts per field. For `is null`, set `value` to `""`.
- **operator**: how this condition chains with the previous one — `and` (default)
  or `or` to start an alternative branch.

`is_excluded` applies to value lists only, not advanced filters.

### Common patterns (all natively supported now)

- **Numeric range:** advanced `total_range` on the amount field, e.g.
  `{"condition": "total_range", "value": ["1000", "5000"]}`.
- **Comparison:** advanced `gt`/`gte`/`lt`/`lte` (e.g. amount over 100000).
- **Substring match:** advanced `contains` / `bw` / `ew` (e.g. account name
  contains "adj"). No need to pre-fetch distinct values.
- **Null check:** advanced `is null` (with `value: ""`).
- **Date range:** advanced `total_range` on the date field with epoch-second
  strings — date filters are accepted (no longer rejected as epoch ints). You can
  still add the date as an aggregation dimension and filter client-side if you
  prefer.

## Example Interactions

(Illustrative — `financials` and the field names below stand in for whatever
alias and field aliases Step 2 discovered in your org; your org's names and
values will differ.)

**User: "/dr-query financials --sample"**
```
📋 Sample: financials (20 rows)

| account_code | amount    | reporting_date | department |
|--------------|-----------|----------------|------------|
| 4000-100     | 12,500.00 | 2024-01-15     | Sales      |
| 5100-200     | -3,200.00 | 2024-01-14     | Operations |
...
```

**User: "/dr-query financials department = 'Sales'"**
```
get_data_by_alias(alias="financials", select=["account_code","amount","department"],
  filters=[{"name": "department", "values": ["Sales"]}], limit=100)
```

**User: "/dr-query financials amount > 100000"**
```
get_data_by_alias(alias="financials", select=["account_code","amount","department"],
  filters=[{"name": "amount", "values": {"type": "advanced",
    "val": [{"condition": "gt", "value": "100000"}]}}], limit=100)
```

## Limits

| Method | Max Rows | Use Case |
|--------|----------|----------|
| `get_data_by_alias` / `get_data_by_id` | 500/page (use `offset`) | Row-level records, samples, filtered queries |
| `start_aggregation_by_alias` / `start_aggregation_by_id` → poll `get_aggregation_result_by_*` | none | Totals, grouped breakdowns (no row cap) |

## Tips

- Start with a small unfiltered page to learn the data shape and field names.
- If you need a total rather than rows, use the aggregate tools — no row cap.
- If you need more than a few hundred rows of raw data, that's usually a signal
  you want aggregation, not extraction.

## Related Skills

- `/dr-tables` — discover tables / fields and aggregate totals (no row cap).
- `/dr-anomalies` — find issues to investigate (computes findings client-side
  from baseline aggregates).
- `/dr-profile` — field-level statistics.
