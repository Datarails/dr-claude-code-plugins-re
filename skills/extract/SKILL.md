---
name: dr-extract
description: Extract validated financial data from Datarails Finance OS to Excel. Creates workbooks with P&L, Balance Sheet, KPIs (including ARR), and validation checks.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__get_field_distinct_values
  - mcp__datarails-finance-os__get_records_by_filter
  - mcp__datarails-finance-os__get_sample_records
  - Write
  - Read
  - Bash
argument-hint: "[--output <file>] [--scenario <name>] [--year <YYYY>] [--env <env>]"
---

# Datarails Financial Data Extraction

Extract validated financial data from Finance OS to Excel workbooks with:
- **P&L Data**: Revenue, COGS, Operating Expenses by month
- **KPI Data**: ARR, Net New ARR, Churn, LTV, Revenue by quarter
- **Validation**: Cross-checks between P&L and KPI tables

## Client Profile System

This skill uses **client profiles** to adapt to different Datarails environments. Each client may have different table IDs, field names, and account hierarchies.

### Profile Location
Profiles are stored at: `config/client-profiles/<env>.json`

### First-Time Setup
If no profile exists for the target environment:
1. Inform the user: "No profile found for this environment. Run `/dr-learn` first to configure extraction."
2. Guide them to run `/dr-learn --env <env>`

### Profile Structure
```json
{
  "tables": {
    "financials": { "id": "TABLE_ID", "name": "Financials Cube" },
    "kpis": { "id": "34298", "name": "KPI Metrics" }
  },
  "field_mappings": {
    "amount": "Amount",
    "scenario": "Scenario",
    "account_l1": "DR_ACC_L1"
  },
  "account_hierarchy": {
    "pnl_filter": "P&L",
    "revenue": "REVENUE"
  }
}
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--output <file>` | Output filename | `tmp/Financial_Extract_YYYY.xlsx` |
| `--scenario <name>` | Primary scenario | `Actuals` |
| `--year <YYYY>` | Calendar year to extract | Current year |
| `--env <env>` | Environment: dev, demo, testapp, app | Active |

## Data Extraction Approach

This skill extracts **raw records** for Excel workbooks, so pagination is the primary method. However, aggregation can be used for summary sheets.

```
RAW DATA: Paginate via get_records_by_filter with System_Year filter
- Fetch 500 rows per page
- Re-authenticate every ~20K rows to avoid token expiry
- This is the correct approach for raw data extraction

SUMMARY SHEETS: Use aggregation API (~5 seconds per query)
- For P&L summary totals
- For category breakdowns
- Check profile.aggregation.field_alternatives for fields that fail
```

## Workflow

### Phase 1: Setup

#### Step 1: Verify Authentication
```
Use: check_auth_status
If not authenticated, guide to /dr-auth
```

#### Step 2: Confirm Year and Scenario
Parse arguments for year (default: current year) and scenario (default: Actuals).

#### Step 3: Load Client Profile
```
Read: config/client-profiles/<env>.json

If profile exists:
  - Load table IDs and field mappings
  - Continue to extraction

If profile does NOT exist:
  - Check if default profile exists (config/client-profiles/app.json)
  - If no profile at all, inform user:
    "No client profile found for '<env>'. Run '/dr-learn --env <env>' first to discover your table structure."
  - Stop execution
```

### Phase 2: Data Extraction via Python Script

**IMPORTANT**: Use the Python script via Bash for reliable data extraction. The script handles:
- Pagination (500 rows per request)
- Token refresh during long operations
- Client-side aggregation
- Profile-based configuration
- Excel generation with openpyxl

#### Step 4: Run Extraction Script

```bash
# With environment (loads profile automatically)
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --env app

# With explicit profile path
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --profile config/client-profiles/app.json

# Full options
uv --directory mcp-server run python scripts/extract_financials.py \
  --year 2025 \
  --scenario Actuals \
  --env app \
  --output tmp/MyReport.xlsx
```

### Phase 3: Data Extraction (Script Details)

The script uses profile configuration for:

**Table IDs** (from `profile.tables`):
- Financials table: `profile.tables.financials.id`
- KPI table: `profile.tables.kpis.id`

**Field Names** (from `profile.field_mappings`):
- Amount: `profile.field_mappings.amount`
- Date: `profile.field_mappings.date`
- Account L1: `profile.field_mappings.account_l1`
- Scenario: `profile.field_mappings.scenario`

**Account Hierarchy** (from `profile.account_hierarchy`):
- P&L filter: `profile.account_hierarchy.pnl_filter`
- Revenue category: `profile.account_hierarchy.revenue`
- COGS category: `profile.account_hierarchy.cogs`

### Phase 4: Generate Excel

The script generates an Excel workbook with:
1. **Summary sheet**: Key totals and metrics
2. **P&L sheet**: Monthly breakdown by account category
3. **KPIs sheet**: Quarterly KPI values
4. **Validation sheet**: Cross-checks and profile info

Output location: `tmp/` folder (configurable via `--output`)

## Complete Extraction Commands

```bash
# Basic extraction (uses active environment's profile)
uv --directory mcp-server run python scripts/extract_financials.py --year 2025

# Specific environment
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --env app
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --env dev

# With scenario
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --scenario Budget

# Custom output path
uv --directory mcp-server run python scripts/extract_financials.py --year 2025 --output tmp/Budget_2025.xlsx
```

## Expected Output

```
============================================================
Datarails Financial Extraction - 2025 Actuals
Profile: app
============================================================

Authenticating...
  Connected to: https://app.datarails.com
  Loading profile: config/client-profiles/app.json

Extracting 2025 P&L (Actuals)...
  Fetching from table TABLE_ID...
    Total: 52,431 rows
  Months covered: ['2025-01', '2025-02', ..., '2025-12']
  Account categories: ['REVENUE', 'Cost of Good sold', 'Operating Expense', ...]

Extracting 2025 KPIs (Actuals)...
  Fetching from table 34298...
    Total: 2,156 rows
  Quarters: ['Q1 - 25', 'Q2 - 25', 'Q3 - 25', 'Q4 - 25']
  KPIs found: 15

Generating Excel...
  Saved: tmp/Financial_Extract_2025.xlsx

============================================================
SUMMARY
============================================================

P&L (12 months):
  REVENUE: $44,207,281.46
  Cost of Good sold: $5,946,341.55
  Operating Expense: $90,761,485.96

KPIs (4 quarters):
  Revenue: $44,207,281.46
  ARR Opening Balance (Q4): $42,845,641.69
  Net New ARR: $20,747,511.34

Output: tmp/Financial_Extract_2025.xlsx
============================================================
```

## Troubleshooting

### No profile found
```
Run /dr-learn --env <env> first to create a profile for this environment.
```

### Token expires during extraction
The script auto-refreshes tokens every 20K rows. If you still get 401 errors:
1. Run `/dr-auth` to get fresh credentials
2. Reduce batch size in the script

### Missing months in data
Check `System_Year` filter value - must be a **string** ("2025"), not integer.

### P&L and KPI totals don't match
Small differences are normal due to:
- Timing of data loads
- Rounding in KPI calculations
- Adjustments posted to P&L but not reflected in KPIs

### Aggregation API returns 500 for a field
Some fields fail per-client. Run `/dr-test` to discover which fields work. The script uses pagination for raw data extraction regardless.

### Wrong table or field names
Edit the profile directly: `config/client-profiles/<env>.json`

## Related Skills

- `/dr-auth` - Authenticate first
- `/dr-learn` - Create/update client profile
- `/dr-tables` - Explore available tables
- `/dr-query` - Investigate specific records
