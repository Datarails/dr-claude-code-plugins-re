---
name: dr-query
description: Query Datarails Finance OS tables with filters. Fetch specific records or random samples for investigation. Filter API supports equality and value-list operators only — for ranges and patterns the skill explains the right alternative.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__execute_query
  - mcp__datarails-finance-os__get_field_distinct_values
argument-hint: "<table_id> [filter_expression] [--sample] [--limit N]"
---

# Datarails Data Query

Query Finance OS tables — fetch records by filter, get random samples, or
pull a raw page of up to 1000 rows. The filter API is value-list only;
this skill explains the supported syntax and the right workaround when the
user asks for something the API can't do natively.

## Workflow

### Step 1: Verify Authentication

If any tool call fails with an authentication or connection error, guide
the user to connect via the Connectors UI ("+" → Connectors → Datarails →
Connect).

### Step 2: Pick the right tool

- **Random sample** → `get_sample_records` (max 20 rows). Use to inspect
  data shape.
- **Filtered records** → `get_records_by_filter` (max 500 rows). Use for
  equality / IN-list filters.
- **Raw page** → `execute_query` (returns up to 1000 rows). The `query`
  argument is currently ignored — it always returns the first page; do
  not advertise it as SQL.
- **Range / comparison / null / pattern** → not supported by the filter
  API. See "Workarounds" below.

### Step 3: Execute and Present

Format results as a readable table. Highlight any notable patterns.

## Arguments

| Argument | Description |
|----------|-------------|
| `<table_id>` | Required — the table to query |
| `[filter]` | Filter expression (equality / IN-list, see syntax below) |
| `--sample` | Get random sample (default 20 rows) |
| `--limit N` | Limit results (max 500 for filters) |

## Filter Syntax

The backend filter API has **value-list semantics only**. The only
supported shapes are:

**Equality (scalar):**
```
status = "active"
amount = 12500
```

**Equality (list of values — implicit OR):**
```
status IN ("active", "pending")
account_code IN ("4000-100", "4000-200", "4000-300")
```

**Exclusion list:**
```
status NOT IN ("archived", "deleted")
```

**Multiple conditions (implicit AND across fields):**
```
status = "active" AND department IN ("Sales", "Marketing")
```

### NOT supported

The following return an explicit `unsupported_filter_operators` error from
the backend — do not include them in the filter string:

- Comparison: `>`, `<`, `>=`, `<=`, `BETWEEN`
- Null check: `IS NULL`, `IS NOT NULL`
- Pattern match: `LIKE`, `ILIKE`
- Disjunction across different fields (`a = 1 OR b = 2`)

### Workarounds

- **Numeric range** (e.g. "amount between 1000 and 5000"): redirect to
  `/dr-tables` aggregate flow. `aggregate_table_data` accepts a numeric
  category bucket field as a dimension and has no row limit.
- **Null check**: call `aggregate_table_data` with the field as a
  dimension and COUNT — null/missing rows show up as a separate
  grouping.
- **Substring match** (e.g. `LIKE "%adj%"`): fetch distinct values with
  `get_field_distinct_values`, do the substring filter client-side, then
  pass the matching subset as an `in` list to `get_records_by_filter`.
- **Date range**: date fields are stored as epoch integers and rejected
  by the filter API entirely. Use `aggregate_table_data` with the date
  field in `dimensions` and filter the response client-side, or call
  `get_metric_data` / `semantic_aggregate` (both accept top-level
  `date_start` / `date_end`).

## Example Interactions

**User: "/dr-query 11442 --sample"**
```
📋 Sample: GL Transactions (20 random records)

| transaction_id | account_code | amount    | posting_date | department |
|----------------|--------------|-----------|--------------|------------|
| 45231          | 4000-100     | 12,500.00 | 2024-01-15   | Sales      |
| 67892          | 5100-200     | -3,200.00 | 2024-01-14   | Operations |
| 23456          | 4000-300     | 45,000.00 | 2024-01-13   | Marketing  |
...

Showing 20 of 125,432 total records
```

**User: "/dr-query 11442 department = 'Sales'"**
```
📋 Query Results: GL Transactions
Filter: department = "Sales"

| transaction_id | account_code | amount    | posting_date | vendor_name     |
|----------------|--------------|-----------|--------------|-----------------|
| 45231          | 4000-100     | 125,000   | 2024-01-15   | ABC Company     |
| 67892          | 4000-100     |  85,000   | 2024-01-14   | DEF Industries  |
...

Found 1,247 records matching filter (showing first 100).
Use --limit 500 to see more, or call /dr-tables aggregate to get totals.
```

**User: "/dr-query 11442 account_code IN ('4000-100', '4000-200')"**
```
📋 Query Results: GL Transactions
Filter: account_code IN ("4000-100", "4000-200")

| transaction_id | account_code | amount    | posting_date | department |
|----------------|--------------|-----------|--------------|------------|
| 45231          | 4000-100     | 125,000   | 2024-01-15   | Sales      |
| 89234          | 4000-200     |  45,000   | 2024-01-10   | Marketing  |
...

Found 892 records (showing first 100).
```

**User: "/dr-query 11442 amount > 100000"** (unsupported)
```
⚠️ The backend filter API doesn't support numeric comparison.

You have two options:
1. Use /dr-tables aggregate with a bucket dimension to find the rows.
2. If you already know which values qualify, pass them as an IN list:
   /dr-query 11442 amount IN (125000, 150000, 200000)

For a recurring need, /dr-anomalies surfaces large-amount outliers
without requiring a comparison filter.
```

## Filter Object Format (API)

When calling `get_records_by_filter` programmatically, supply a dict of
field → value spec:

```json
{
  "status": "active",
  "amount": [12500, 15000, 20000],
  "account_code": {"in": ["4000-100", "4000-200"]},
  "department": {"not_in": ["Archived"]}
}
```

The backend rejects `{">": N}`, `{"<": N}`, `{"is_null": true}`,
`{"like": "..."}`, `{"between": [...]}` with `unsupported_filter_operators`.

## Limits

| Method | Max Rows | Use Case |
|--------|----------|----------|
| `get_sample_records` | 20 | Quick data inspection |
| `get_records_by_filter` | 500 | Investigation queries with equality/IN filters |
| `execute_query` | 1000 | Raw page (no filtering — `query` arg is ignored) |
| `aggregate_table_data` | none | Use when you need totals or ranges (no row cap) |

## Tips

- Start with `--sample` to understand data shape and which fields exist.
- For investigation that needs comparison or range, drive it through
  `/dr-tables` aggregate flow rather than trying to filter raw rows.
- If you need more than 500 rows of raw data, that's usually a signal
  you want aggregation, not extraction.

## Related Skills

- `/dr-tables` — Get schema or aggregate totals (no row cap).
- `/dr-anomalies` — Find issues to investigate (computes findings
  client-side from baseline aggregates).
- `/dr-profile` — Field-level statistics.
