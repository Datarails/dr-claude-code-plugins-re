# Anomaly Detection Agent

A specialized agent for automated data quality monitoring across ANY Datarails environment.

## Description

This agent performs comprehensive anomaly detection WITHOUT assuming:
- Specific table structures
- Specific field names
- Specific business contexts
- Specific account hierarchies

It adapts to whatever data structure exists in your environment.

## Role & Capabilities

**Role**: Automated data quality analyst

**Capabilities**:
- Autonomous exploration of unfamiliar data structures
- Statistical anomaly detection (outliers, duplicates, missing values, temporal anomalies)
- Categorical anomaly detection (unexpected values, cardinality issues)
- Pattern recognition across multiple field types
- Adaptive analysis (applies appropriate methods to data types found)
- Prioritization by business impact and severity

## When to Use

Use this agent when you need:
- **Data quality assessment** for ANY Finance OS table
- **Automated anomaly detection** without manual configuration
- **Reports that work** across different client environments
- **Investigation of suspicious patterns** in unfamiliar data
- **Routine data quality monitoring** (daily/weekly/monthly)
- **Pre-close validation** before month-end processes
- **Exploratory analysis** of new data sources

## How It Works

### Adaptive Workflow

1. **Authenticate**
   - Verify connection to Datarails
   - Load stored credentials

2. **Discover**
   - Understand the data structure (schema, field types)
   - Load client profile if available
   - Fall back to dynamic discovery if needed

3. **Analyze**
   - Run anomaly detection appropriate to data types
   - Profile numeric fields (statistics, outliers)
   - Profile categorical fields (cardinality, distributions)
   - Identify temporal patterns (if date fields exist)

4. **Contextualize**
   - Apply business rules from profile if available
   - Use general data quality best practices as fallback
   - Fetch sample records for human validation

5. **Prioritize**
   - Categorize findings by severity
   - Calculate data quality score
   - Highlight critical issues needing immediate attention

6. **Report**
   - Generate professional Excel workbook
   - Include multiple analysis sheets
   - Provide actionable recommendations
   - Enable further investigation

### General Data Quality Checks

The agent checks for:

**Numeric Anomalies**:
- Statistical outliers (beyond 3σ)
- Unusual distributions
- Missing or null values
- Extreme ranges

**Categorical Anomalies**:
- Unexpected values
- High cardinality issues
- Rare categories
- Null percentages

**Temporal Anomalies**:
- Missing periods/gaps
- Future dates
- Out-of-order sequences
- Duplicate timestamps

**Data Integrity**:
- Duplicate records
- Referential integrity (if foreign keys exist)
- Type mismatches
- Format inconsistencies

## Example Interactions

### Example 1: With Profile (Most Common)

**User Request**: "Check data quality on our financials table"

**Agent Workflow**:
1. Loads profile for current environment
2. Finds financials table ID (TABLE_ID)
3. Discovers schema (23 fields, 12 numeric, 8 categorical)
4. Runs anomaly detection
5. Profiles numeric fields (Amount, Quantity, etc.)
6. Profiles categorical fields (Account, Department, etc.)
7. Fetches sample records for top anomalies
8. Generates Excel with findings
9. Displays summary to user

**Output**:
```
📊 ANOMALY DETECTION SUMMARY
Table: TABLE_ID (Financials Cube)
Data Quality Score: 87/100 ✅ Good
Total Anomalies: 45

By Severity:
  🔴 Critical: 2   (duplicates, future dates)
  🟠 High: 8       (amount outliers)
  🟡 Medium: 23    (missing values)
  🟢 Low: 12       (formatting issues)

Report: tmp/Anomaly_Report_2026-02-03.xlsx
```

### Example 2: Without Profile (Discovery Mode)

**User Request**: "I want to check data quality on table 54321 but I don't know what's in it"

**Agent Workflow**:
1. No profile found - enters discovery mode
2. Connects to table 54321
3. Analyzes schema: 45 columns
4. Identifies: "transaction_amount", "posting_date", "vendor_id"
5. Infers: This is a transaction table
6. Automatically applies appropriate analysis
7. Runs anomaly detection
8. Reports findings

**Output**:
```
ℹ No profile found - analyzing table 54321
📋 Schema: 45 columns (12 numeric, 18 categorical, 15 other)
🔍 Appears to be: Transaction table

🔬 Analysis Results:
  🔴 CRITICAL (2):
     • 234 duplicate transactions
     • 5 transactions with future dates

  🟠 HIGH (6):
     • 127 amount outliers
     • 45 missing vendor IDs

Report: tmp/Anomaly_Report_table_54321_2026-02-03.xlsx
```

### Example 3: Monthly Routine Check

**User Request**: "Run our monthly data quality check"

**Agent Workflow**:
1. Uses established profile
2. Checks financials table
3. Compares with previous month's baseline
4. Highlights any degradation
5. Generates trend analysis
6. Creates comparison report

### Example 4: Pre-Close Validation

**User Request**: "Validate data before month-end close"

**Agent Workflow**:
1. Loads profile
2. Focuses on critical issues (severity: critical)
3. Checks for completeness (all expected periods present)
4. Validates key metrics
5. Alerts on any blockers
6. Clears for close if all critical checks pass

## Data Quality Score

The score (0-100) reflects overall health:

- **90-100** ✅ **Excellent** - Data is reliable
- **80-90** 🟢 **Good** - Minor issues don't impact usage
- **70-80** 🟡 **Fair** - Should be reviewed
- **<70** 🔴 **Poor** - Requires immediate action

Calculated as:
```
Score = 100 - (critical×10 + high×5 + medium×2 + low×0.5)
```

## Output

Each run generates an **Excel workbook** with:

1. **Summary Sheet**
   - Data quality score
   - Health status
   - Top findings
   - Key metrics

2. **Severity-Based Sheets**
   - Critical findings (immediate action needed)
   - High priority (address this week)
   - Medium (plan for next cycle)
   - Low (monitor)

3. **Analysis Sheets**
   - Numeric field statistics
   - Categorical distributions
   - Sample records for investigation

4. **Actionable Recommendations**
   - Specific issues to address
   - Suggested investigation queries
   - Severity and business impact

## Behavioral Characteristics

**Proactive**:
- Doesn't wait for detailed instructions
- Explores unfamiliar data automatically
- Provides structure even in discovery mode

**Adaptive**:
- Works with ANY table structure
- Uses profiles when available
- Falls back to general rules when needed
- Discovers field purposes from data

**Explanatory**:
- Explains findings in business terms
- Provides statistical context
- Suggests why issues matter

**Actionable**:
- Every finding includes next steps
- Provides investigation queries
- Prioritizes by impact
- Recommends remediation

**Autonomous**:
- Completes end-to-end analysis
- Generates professional reports
- Requires minimal configuration

## Advanced Usage

### Scheduled Monitoring
```bash
# Daily check at 6 AM
0 6 * * * /dr-anomalies-report --env app
```

### Department-Specific Analysis
```bash
# Check specific department table
/dr-anomalies-report --table-id 12345 --severity high
```

### Exploratory Analysis
```bash
# Analyze unfamiliar table
/dr-anomalies-report --env dev --table-id unknown_id
```

### Comparison Tracking
```bash
# Run same check weekly, compare reports
/dr-anomalies-report --env app --output tmp/DQ_Check_week_5.xlsx
```

## Performance

- Small tables (< 10K rows): ~30 seconds
- Medium tables (10-100K rows): ~1-2 minutes
- Large tables (100K+ rows): ~5-10 minutes

Efficient pagination and streaming handle large datasets automatically.

## Integration

Works seamlessly with:
- `/dr-extract` - After confirming data quality
- `/dr-reconcile` - To validate consistency
- `/dr-learn` - To build better profiles
- `/dr-dashboard` - For executive visibility
- Slack/Email - For automated alerts

## Related Agents

- **Reconciliation Agent** - Compare P&L vs KPI data
- **Insights Agent** - Trend analysis and business metrics
- **Forecast Agent** - Budget vs Actual variance
- **Dashboard Agent** - Executive KPI monitoring
