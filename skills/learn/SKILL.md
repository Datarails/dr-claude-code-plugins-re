---
name: dr-learn
description: Discover and learn a client's table structure for financial data extraction. Creates a client profile that enables /dr-extract to work with any Datarails environment.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_sample_records
  - mcp__datarails-finance-os__profile_categorical_fields
  - Write
  - Read
  - AskUserQuestion
argument-hint: "[--env <env>] [--force]"
---

# Datarails Table Discovery & Profile Generation

Learn a client's table structure and create a profile for `/dr-extract`. This enables the extraction skill to work with any Datarails environment without hardcoded values.

## Purpose

Different clients have different:
- Table IDs (e.g., 16528 vs 45123 for financials)
- Field names (e.g., `Amount` vs `Transaction_Amount`)
- Account hierarchies (e.g., `REVENUE` vs `Revenue` vs `Total Revenue`)
- KPI naming conventions

This skill discovers these mappings and saves them to a client profile.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--env <env>` | Environment: dev, demo, testapp, app | Active environment |
| `--force` | Overwrite existing profile | Prompt for confirmation |

## Workflow

### Phase 1: Setup & Verification

#### Step 1: Check Authentication
```
Use: mcp__datarails-finance-os__check_auth_status
If not authenticated, guide user to run /dr-auth first
```

#### Step 2: Determine Target Environment
Parse `--env` flag or use active environment from config.

#### Step 3: Check for Existing Profile
```
Read: config/client-profiles/<env>.json
If exists and no --force flag, ask user if they want to overwrite
```

### Phase 2: Table Discovery

#### Step 4: List All Available Tables
```
Use: mcp__datarails-finance-os__list_finance_tables
```

Display tables to user in a clear format:
```
Found X tables in <environment>:

ID      | Name                    | Rows
--------|-------------------------|--------
16528   | Financials Cube         | 125,432
34298   | KPI Metrics             | 2,156
...
```

#### Step 5: Identify Financial Data Table
Look for tables that likely contain financial data:
- Names containing: "Financial", "P&L", "PnL", "GL", "Ledger", "Transactions", "Cube"
- Large row counts (typically 10K+ rows)

Ask user to confirm:
```
Use: AskUserQuestion
Question: "Which table contains your main financial/P&L data?"
Options: [detected candidates] + "Other (specify ID)"
```

#### Step 6: Identify KPI Table (if applicable)
Look for tables with:
- Names containing: "KPI", "Metric", "ARR", "Revenue"
- Smaller row counts (typically <10K rows)

Ask user:
```
Use: AskUserQuestion
Question: "Which table contains your KPIs? (optional)"
Options: [detected candidates] + "None" + "Other (specify ID)"
```

### Phase 3: Schema Analysis

#### Step 7: Analyze Financial Table Schema
```
Use: mcp__datarails-finance-os__get_table_schema
table_id: <selected_financials_table>
```

#### Step 8: Map Essential Fields

Identify these field types by analyzing schema and sample data:

| Semantic Name | Look For | Type |
|---------------|----------|------|
| `amount` | "Amount", "Value", "Transaction", currency type | numeric |
| `scenario` | "Scenario", "Version", "Type" | categorical |
| `year` | "Year", "System_Year", "Fiscal_Year" | numeric/string |
| `date` | "Date", "Period", "Reporting", timestamp type | date |
| `account_l0` | "L0", "Level0", "Category", "Type" | categorical |
| `account_l1` | "L1", "Level1", "Account", "Group" | categorical |
| `account_l2` | "L2", "Level2", "Subaccount", "Detail" | categorical |
| `department_l1` | "Department", "Dept", "Cost Center" | categorical |

For each potential match, verify with distinct values:
```
Use: mcp__datarails-finance-os__get_field_distinct_values
table_id: <table>
field_name: <candidate_field>
```

#### Step 9: Confirm Field Mappings with User
Present discovered mappings and ask for confirmation:
```
I've analyzed your financial table and found these field mappings:

Amount field:     Amount (numeric, 125,432 non-null values)
Scenario field:   Scenario (values: Actuals, Budget, Forecast)
Year field:       System_Year (values: 2023, 2024, 2025, 2026)
Date field:       Reporting Date (timestamp)
Account L0:       DR_ACC_L0 (values: P&L, Balance Sheet)
Account L1:       DR_ACC_L1 (values: REVENUE, Cost of Good sold, ...)
Account L2:       DR_ACC_L2 (values: Income, G&A, Marketing, ...)

Are these mappings correct? [Y/n]
```

If user says no, use `AskUserQuestion` to get correct field names.

### Phase 4: Account Hierarchy Discovery

#### Step 10: Discover Account Categories
Get distinct values for the account L1 field:
```
Use: mcp__datarails-finance-os__get_field_distinct_values
table_id: <financials_table>
field_name: <account_l1_field>
```

#### Step 11: Map Account Categories
Identify which values correspond to:
- Revenue (look for: "Revenue", "REVENUE", "Income", "Sales")
- COGS (look for: "COGS", "Cost of Good", "Cost of Sales", "Direct Cost")
- OpEx (look for: "Operating", "OpEx", "Expense", "SG&A")
- Other categories as found

Present to user for confirmation.

### Phase 5: KPI Analysis (if selected)

#### Step 12: Analyze KPI Table Schema
```
Use: mcp__datarails-finance-os__get_table_schema
table_id: <selected_kpi_table>
```

#### Step 13: Map KPI Fields
Identify:
- `kpi_name`: field containing KPI names
- `kpi_value`: field containing KPI values
- `quarter`: period field

#### Step 14: Discover Available KPIs
```
Use: mcp__datarails-finance-os__get_field_distinct_values
table_id: <kpi_table>
field_name: <kpi_name_field>
```

Map common KPIs:
- Revenue, ARR, Net New ARR, New ARR
- Churn $, Churn %
- LTV, LTV/CAC
- Gross Profit

### Phase 6: Save Profile

#### Step 15: Generate Profile JSON
Create the profile structure:

```json
{
  "version": "1.0",
  "environment": "<env>",
  "discovered_at": "<ISO timestamp>",

  "tables": {
    "financials": {
      "id": "<table_id>",
      "name": "<table_name>",
      "purpose": "P&L and Balance Sheet"
    },
    "kpis": {
      "id": "<table_id>",
      "name": "<table_name>",
      "purpose": "KPI Metrics"
    }
  },

  "field_mappings": {
    "amount": "<field_name>",
    "scenario": "<field_name>",
    "year": "<field_name>",
    "date": "<field_name>",
    "account_l0": "<field_name>",
    "account_l1": "<field_name>",
    "account_l2": "<field_name>",
    "kpi_name": "<field_name>",
    "kpi_value": "<field_name>",
    "quarter": "<field_name>"
  },

  "account_hierarchy": {
    "pnl_filter": "<value>",
    "revenue": "<value>",
    "cogs": "<value>",
    "opex": "<value>"
  },

  "kpi_definitions": {
    "revenue": "<KPI name>",
    "arr_opening": "<KPI name>",
    "new_arr": "<KPI name>",
    "churn": "<KPI name>"
  },

  "scenarios": ["<list>"],
  "years_available": ["<list>"]
}
```

#### Step 16: Write Profile
```
Use: Write
file_path: config/client-profiles/<env>.json
content: <generated_profile>
```

#### Step 17: Confirmation
Display summary:
```
Profile saved to config/client-profiles/<env>.json

Summary:
- Financials table: <name> (ID: <id>)
- KPI table: <name> (ID: <id>)
- Fields mapped: <count>
- Scenarios: <list>
- Years available: <list>

You can now use /dr-extract --env <env> to extract financial data.
```

## Example Interaction

**User: "/dr-learn"**

```
Checking authentication... Connected to app.datarails.com

Discovering tables in Production environment...

Found 47 tables:

ID      | Name                    | Type        | Rows
--------|-------------------------|-------------|--------
16528   | Financials Cube         | cube        | 125,432
34298   | KPI Dashboard           | table       | 2,156
45123   | Budget Template         | template    | 8,432
...

Based on the names and sizes, I believe:
- Table 16528 "Financials Cube" is your main financial data
- Table 34298 "KPI Dashboard" contains your KPIs

Is this correct? [Y/n/Other]
```

**User: "y"**

```
Analyzing Financials Cube schema...

Found these field mappings:
- Amount: "Amount" (numeric)
- Scenario: "Scenario" (Actuals, Budget, Forecast)
- Year: "System_Year" (2023-2026)
- Date: "Reporting Date" (timestamp)
- Account L0: "DR_ACC_L0" (P&L, Balance Sheet)
- Account L1: "DR_ACC_L1" (REVENUE, Cost of Good sold, Operating Expense, ...)
- Account L2: "DR_ACC_L2" (Income, G&A, Marketing, Sales, R&D, ...)

Confirm these mappings? [Y/n/Edit]
```

**User: "y"**

```
Profile saved to config/client-profiles/app.json

You can now run:
  /dr-extract --year 2025 --env app
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No tables found | Check authentication, verify Finance OS access |
| Can't identify financial table | User selects manually via "Other" option |
| Field mapping incorrect | User can edit profile JSON directly |
| Missing KPIs | KPI table is optional, can run without it |

## Related Skills

- `/dr-auth` - Authenticate first
- `/dr-tables` - Explore table details
- `/dr-extract` - Uses the generated profile
