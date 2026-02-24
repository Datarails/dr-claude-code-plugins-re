---
name: dr-tables
description: List and explore Datarails Finance OS tables. Use to discover available data, view schemas, and understand table structure.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__auth_status
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__profile_table_summary
argument-hint: "[table_id] [--schema] [--field <field_name>]"
---

# Datarails Table Discovery

Explore Finance OS tables - list available tables, view schemas, and understand data structure.

## Workflow

### Step 1: Verify Authentication

Always check auth status first with `mcp__datarails-finance-os__auth_status`. If not authenticated, guide user to run `/dr-auth`.

### Step 2: Handle Request

**List all tables (no arguments):**
- Use `mcp__datarails-finance-os__list_finance_tables`
- Present tables in a formatted list with IDs and names
- Group by category if available

**View specific table (with table_id):**
- Use `mcp__datarails-finance-os__get_table_schema` to get columns and types
- Use `mcp__datarails-finance-os__profile_table_summary` for quick overview
- Present schema in a readable table format

**Explore field values (with --field):**
- Use `mcp__datarails-finance-os__get_field_distinct_values`
- Show unique values with counts
- Useful for understanding categorical data

## Arguments

| Argument | Description |
|----------|-------------|
| (none) | List all available tables |
| `<table_id>` | Show schema and summary for specific table |
| `--schema` | Show detailed schema (columns, types, constraints) |
| `--field <name>` | Show distinct values for a specific field |

## Example Interactions

**User: "/dr-tables"**
```
📊 Finance OS Tables

| ID    | Name                    | Rows    |
|-------|-------------------------|---------|
| 11442 | GL Transactions         | 125,432 |
| 11443 | Budget Data             | 8,291   |
| 11444 | Vendor Master           | 1,847   |
...
```

**User: "/dr-tables 11442"**
```
📋 Table: GL Transactions (ID: 11442)

Rows: 125,432 | Columns: 24 | Last Updated: 2024-01-15

Schema:
| Column          | Type      | Nullable | Description          |
|-----------------|-----------|----------|----------------------|
| transaction_id  | INTEGER   | No       | Primary key          |
| account_code    | VARCHAR   | No       | GL account number    |
| amount          | DECIMAL   | No       | Transaction amount   |
| posting_date    | DATE      | No       | Date posted          |
...
```

**User: "/dr-tables 11442 --field account_code"**
```
🔍 Distinct Values: account_code (Table 11442)

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
- Table IDs are needed for other skills like `/dr-profile` and `/dr-anomalies`
- Check distinct values to understand categorical field cardinality
- The profile summary gives a quick data quality overview
## Related Skills

- `/dr-auth` - Authenticate
- `/dr-profile` - Deep profiling of numeric and categorical fields
- `/dr-anomalies` - Detect data quality issues
- `/dr-query` - Query specific records
