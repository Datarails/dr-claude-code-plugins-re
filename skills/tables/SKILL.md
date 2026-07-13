---
name: dr-tables
description: List and explore Datarails Finance OS tables. Use to discover available data, view schemas, and understand table structure.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__start_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_result_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__start_distinct_values_by_id
  - mcp__datarails-finance-os__get_distinct_values_result_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__list_business_metrics
argument-hint: "[table_id] [--schema] [--field <field_name>]"
---

# Datarails Table Discovery

Explore Finance OS tables - list available tables, view schemas, and understand data structure.

## Workflow

### Step 1: Verify Authentication

If any Datarails tool call fails with an authentication or connection error, tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

### Step 2: Handle Request

**List all tables (no arguments):**
- Use `mcp__datarails-finance-os__list_data_models`
- Each entry carries both a numeric `id` and an `alias` (empty when the table has
  no business alias) — note both, they drive which schema/field tools to use next
- Present tables in a formatted list with IDs, aliases, and names
- Group by category if available

**View specific table (with table_id):**
- If the table has an alias, use `mcp__datarails-finance-os__list_aliased_fields`
  (business-friendly field aliases); otherwise use
  `mcp__datarails-finance-os__get_fields_by_id` (capture each field's numeric `id`)
- For a quick data overview, run `mcp__datarails-finance-os__profile_numeric_fields`
  (stats per numeric field) and `mcp__datarails-finance-os__profile_categorical_fields`
  (cardinality/top values per categorical field)
- Present schema in a readable table format

> **Alias coverage is per field, not per table.** A table having an alias does *not* mean its fields are aliased — real orgs often expose only a handful of aliased fields (e.g. ~5 of ~185 on a mapped financials table), and the load-bearing fields (`amount`, `scenario`, account groups, dates) are frequently *not* among them. Treat the alias/by-id choice **per field**: `get_fields_by_id(<id>)` returns every field with its numeric `id` and its `alias` (empty if none). Address a field by alias (via the `*_by_alias` tools) when it has one, else by numeric `id` (via the `*_by_id` tools). By-id always works — never abandon the query because the aliased set is thin.

> **Async fetch — aggregations and distinct values run as start → poll.** `start_aggregation_by_id`/`_by_alias` and `start_distinct_values_by_id`/`_by_alias` take the same arguments as the retired blocking calls (dimensions/metrics/filters; table id + field id, or alias + field alias) and return immediately with `{"status": "pending", "handle": {...}}`. Echo that `handle` back verbatim to the matching `get_aggregation_result_by_*` / `get_distinct_values_result_by_*` tool: a `{"status": "running", "retry_after_seconds": N}` response means poll again with the same handle after ~N seconds (≈5s) — it is not an error, and large jobs may take several polls; when ready, the result arrives in the familiar shape (for distinct values, pass `limit` to the result tool). An expired/unknown-handle error means restart with the `start_*` tool. *Transitional fallback:* if the `start_*` tools aren't available on the connector (older server), the blocking twins `get_aggregated_data_by_*` / `get_distinct_values_by_*` still work with the same arguments.

**Explore field values (with --field):**
- Use `mcp__datarails-finance-os__start_distinct_values_by_alias` (aliased tables) or
  `mcp__datarails-finance-os__start_distinct_values_by_id` (by-id fallback)
- → poll the matching `get_distinct_values_result_by_alias` /
  `get_distinct_values_result_by_id` with the returned `handle` until ready
  (async-fetch pattern); pass `limit` to the result tool
- Show unique values with counts
- Useful for understanding categorical data
- If a distinct-values call errors, fall back to sampling rows and dedupe client-side
- On `"truncated": true` in any data response, the returned rows are an
  incomplete prefix — narrow the query per the `guidance` (more filters / fewer
  columns / lower limit+offset paging) and re-fetch; never present the prefix as
  complete

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | List all available tables |
| `<table_id>` | Show schema and summary for specific table |
| `--schema` | Show detailed schema (columns, types, constraints) |
| `--field <name>` | Show distinct values for a specific field |

## Example Interactions

(Illustrative — table ids, names, and values below are invented;
your org's tables and fields will differ.)

**User: "/dr-tables"**
```
📊 Finance OS Tables

| ID     | Name                    | Alias      |
|--------|-------------------------|------------|
| 999901 | GL Transactions         | financials |
| 999902 | Budget Data             | —          |
| 999903 | Vendor Master           | —          |
...
```

**User: "/dr-tables 999901"**
```
📋 Table: GL Transactions (ID: 999901)

Fields: 24 (from the schema call — row counts are not available from any tool; never invent one)

Schema:
| Column          | Type      | Nullable | Description          |
|-----------------|-----------|----------|----------------------|
| transaction_id  | INTEGER   | No       | Primary key          |
| account_code    | VARCHAR   | No       | GL account number    |
| amount          | DECIMAL   | No       | Transaction amount   |
| posting_date    | DATE      | No       | Date posted          |
...
```

**User: "/dr-tables 999901 --field account_code"**
```
🔍 Distinct Values: account_code (Table 999901)

Found 156 unique values:

| Value      | Count  | % of Total |
|------------|--------|------------|
| 4000-100   | 12,543 | 10.0%      |
| 4000-200   | 8,291  | 6.6%       |
| 5100-300   | 7,892  | 6.3%       |
...
```

## Tips

- Use this skill first when starting analysis to understand available data
- Table IDs (and aliases) are needed for other skills like `/dr-profile` and `/dr-anomalies`
- Check distinct values to understand categorical field cardinality
- The numeric/categorical field profiles give a quick data quality overview
## Related Skills

- Connect via Connectors UI
- `/dr-profile` - Deep profiling of numeric and categorical fields
- `/dr-anomalies` - Detect data quality issues
- `/dr-query` - Query specific records
