---
name: dr-intelligence
description: Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting. The most powerful financial analysis skill.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__get_records_by_filter
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--env <env>] [--output <file>]"
---

# FP&A Intelligence Workbook

Generate comprehensive FP&A intelligence workbooks with auto-detected insights, recommendations, and professional Excel formatting.

This is the **most powerful** financial analysis skill - it answers real business questions, not just data dumps.

## What Makes This Different

| Traditional Report | Intelligence Workbook |
|-------------------|----------------------|
| Shows data | Answers questions |
| Lists numbers | Explains "why" |
| Static tables | Highlights anomalies |
| Manual analysis | Insights auto-surfaced |
| Data dump | Recommendations included |

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--env <env>` | Environment: dev, demo, testapp, app | app |
| `--output <file>` | Output file path | `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx` |

## Client Profile System

This skill uses **client profiles** to adapt to different Datarails environments. Each client may have different table IDs, field names, and account hierarchies.

### Profile Location
Profiles are stored at: `config/client-profiles/<env>.json`

### First-Time Setup
If no profile exists for the target environment:
1. Inform the user: "No profile found for this environment. Run `/dr-learn` first to configure."
2. Guide them to run `/dr-learn --env <env>`

### Profile Structure
```json
{
  "tables": {
    "financials": { "id": "16528", "name": "Financials Cube" },
    "kpis": { "id": "34298", "name": "KPI Metrics" }
  },
  "field_mappings": {
    "amount": "Amount",
    "scenario": "Scenario",
    "account_l1": "DR_ACC_L1",
    "date": "Reporting Date"
  },
  "account_hierarchy": {
    "pnl_filter": "P&L",
    "revenue": "REVENUE",
    "cogs": "Cost of Good sold",
    "opex": "Operating Expense"
  }
}
```

## CRITICAL: Data Extraction Approach

**The aggregation API (`/aggregate`) often returns 500 errors or requires async polling.**

**Working Solution**: Use pagination via `/data` endpoint with filters:

```
PREFERRED: Paginate via get_records_by_filter with System_Year filter
- Fetch 500 rows per page
- Re-authenticate every ~20K rows to avoid token expiry (5 min JWT)
- Aggregate results client-side in Python
```

## Workflow

### Phase 1: Setup

#### Step 1: Verify Authentication
```
Use: check_auth_status
If not authenticated, guide to /dr-auth --env <env>
```

#### Step 2: Load Client Profile
```
Read: config/client-profiles/<env>.json

If profile exists:
  - Load table IDs and field mappings
  - Continue to extraction

If profile does NOT exist:
  - Inform user: "No profile found for '<env>'. Run '/dr-learn --env <env>' first."
  - Stop execution
```

### Phase 2: Data Extraction

#### Step 3: Fetch P&L Data (Paginated)
```python
# Fetch ALL records using pagination (aggregation API unreliable)
all_data = []
offset = 0
while True:
    # Refresh token every 20K rows
    if offset % 20000 == 0:
        await auth.ensure_valid_token()

    page = await fetch_page(offset=offset, limit=500)
    if not page:
        break
    all_data.extend(page)
    offset += 500
```

#### Step 4: Fetch KPI Data
```
Similar pagination approach for KPI table
```

#### Step 5: Client-Side Aggregation
```python
# Since server aggregation fails, aggregate in Python
aggregated = defaultdict(float)
for record in all_data:
    key = (record["Account L1"], record["Month"])
    aggregated[key] += record["Amount"]
```

### Phase 3: Intelligence Calculation

#### Step 6: Generate Insights
Apply business rules to detect issues:
- OpEx > Revenue → CRITICAL
- MoM variance > 20% → WARNING
- Vendor concentration > 10% → INFO

#### Step 7: Generate Recommendations
Based on insights, create actionable recommendations.

### Phase 4: Report Generation

#### Step 8: Create Excel Workbook
Generate 10 sheets with professional formatting using openpyxl.

#### Step 9: Save Output
Save to `tmp/FPA_Intelligence_Workbook_YYYY_TIMESTAMP.xlsx`

## 10 Sheets Generated

1. **Insights Dashboard** - Top 5 findings with severity, key metrics with trends, recommendations
2. **Expense Deep Dive** - Top 20 expense accounts with % of total, MoM change
3. **Variance Waterfall** - What changed vs prior period and why
4. **Trend Analysis** - 12-month trends with growth rates
5. **Anomaly Report** - Auto-detected outliers with severity scores
6. **Vendor Analysis** - Top 20 vendors, concentration risk flags
7. **SaaS Metrics** - ARR waterfall, unit economics, efficiency ratios
8. **Sales Performance** - Rep leaderboard, cohort analysis
9. **Cost Center P&L** - Department-level detail
10. **Raw Data** - Pivot-ready dataset for your own analysis

## Auto-Generated Insights

The workbook automatically detects and surfaces:

| Insight Type | Detection Rule | Severity |
|--------------|----------------|----------|
| OpEx exceeds Revenue | OpEx/Revenue > 1.0 | 🔴 CRITICAL |
| High expense growth | MoM change > 20% | 🟠 WARNING |
| Vendor concentration | Single vendor > 10% of spend | 🟡 INFO |
| Negative margins | Gross profit < 0 | 🔴 CRITICAL |
| Unusual variance | > 3 std deviations | 🔴 CRITICAL |

## Examples

### Generate full intelligence workbook
```bash
/dr-intelligence --year 2025 --env app
```

### Custom output location
```bash
/dr-intelligence --year 2025 --output reports/Q4_Intelligence.xlsx
```

### Development environment
```bash
/dr-intelligence --year 2025 --env dev
```

## Sample Output

```
================================================================================
📊 FP&A INTELLIGENCE WORKBOOK GENERATOR
================================================================================

1️⃣  FETCHING DATA FROM DATARAILS...
  📊 Fetching P&L data...
    ✓ Fetched 54,390 raw records
    ✓ Client-side aggregation: 60 grouped records
  📈 Fetching KPI metrics...
    ✓ Fetched 973 KPI records
  🏢 Fetching vendor data...
    ✓ Fetched 1,082 vendor records
  🏗️ Fetching cost center data...
    ✓ Fetched 25 cost center records

2️⃣  CALCULATING INTELLIGENCE...
    ✓ Generated 9 insights
    ✓ Generated 3 recommendations

3️⃣  CREATING WORKBOOK SHEETS...
  📊 Creating Insights Dashboard...
  💰 Creating Expense Deep Dive...
  📊 Creating Variance Waterfall...
  📈 Creating Trend Analysis...
  🔍 Creating Anomaly Report...
  🏢 Creating Vendor Analysis...
  📊 Creating SaaS Metrics...
  📈 Creating Sales Performance...
  🏗️ Creating Cost Center P&L...
  📋 Creating Raw Data...

4️⃣  SAVING WORKBOOK...
    ✓ Saved: tmp/FPA_Intelligence_Workbook_2025.xlsx

================================================================================
✅ INTELLIGENCE WORKBOOK GENERATED
================================================================================
```

## Technical Details

### Data Sources
- **Financials Table** - P&L data (Revenue, COGS, OpEx by month/account/cost center)
- **KPIs Table** - ARR, Churn, LTV, CAC, Revenue by quarter

### Pagination & Performance
- Fetches ALL records using pagination (500/page)
- Auto-refreshes JWT token every 20K rows
- Implements retry logic for API errors
- Client-side aggregation (server aggregation API unreliable)

### Processing Time
- Small datasets (< 10K rows): ~2 minutes
- Medium datasets (10-50K rows): ~5 minutes
- Large datasets (50K+ rows): ~10 minutes

## Why This Matters

This workbook answers the **Top 10 Business Questions**:

1. **Where is the money going?** → Top 20 expense drivers
2. **What changed vs last month?** → MoM variance waterfall
3. **Which cost centers are over budget?** → Variance by department
4. **Are we efficient?** → OpEx as % of Revenue, Gross Margin
5. **What's unusual?** → Auto-detected anomalies
6. **Who are our biggest vendors?** → Top 10 vendor spend
7. **How are sales reps performing?** → Win rates, ARR by rep
8. **What's our burn situation?** → Runway, burn multiple
9. **What should we investigate?** → Exception report
10. **What actions to take?** → Automated recommendations

## Related Skills

- `/dr-extract` - Basic data extraction (simpler, faster)
- `/dr-insights` - Executive PowerPoint + Excel combo
- `/dr-anomalies-report` - Focused on data quality issues
- `/dr-reconcile` - P&L vs KPI validation

## Troubleshooting

**"Not authenticated" error**
- Run `/dr-auth --env app` first

**Takes too long**
- Normal for large datasets (50K+ records = ~10 min)
- Aggregation API is broken, must fetch all raw data

**Missing data in sheets**
- Check if profile has correct field mappings
- Run `/dr-learn --env app` to refresh profile

**"No profile found" error**
- Run `/dr-learn --env app` to create profile first

---

## Execution Instructions

When this skill is invoked, run the Python script:

```bash
uv --directory mcp-server run python scripts/intelligence_workbook.py --year <YEAR> --env <ENV>
```

### Argument Mapping

| User Argument | Script Argument |
|---------------|-----------------|
| `--year 2025` | `--year 2025` |
| `--env app` | `--env app` |
| `--output file.xlsx` | `--output file.xlsx` |

### Pre-Flight Checks

1. **Verify authentication** before running:
   ```bash
   cd mcp-server && uv run datarails-mcp status
   ```

2. **If not authenticated**, guide user to authenticate:
   ```bash
   cd mcp-server && uv run datarails-mcp auth --env app
   ```

3. **Verify profile exists** at `config/client-profiles/<env>.json`

### Example Invocations

```bash
# Basic usage
uv --directory mcp-server run python scripts/intelligence_workbook.py --year 2025 --env app

# Custom output
uv --directory mcp-server run python scripts/intelligence_workbook.py --year 2025 --env app --output tmp/Q4_Report.xlsx

# Development environment
uv --directory mcp-server run python scripts/intelligence_workbook.py --year 2025 --env dev
```

### Expected Runtime

- **Small datasets** (< 10K rows): ~2 minutes
- **Medium datasets** (10-50K rows): ~5 minutes
- **Large datasets** (50K+ rows): ~10 minutes

The script outputs progress as it runs, so the user can see it's working.
