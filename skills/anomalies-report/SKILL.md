---
name: dr-anomalies-report
description: Generate comprehensive anomaly detection report with Excel deliverables. Discovers data quality issues without requiring configuration.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__list_finance_tables
  - mcp__datarails-finance-os__get_table_schema
  - mcp__datarails-finance-os__profile_numeric_fields
  - mcp__datarails-finance-os__profile_categorical_fields
  - mcp__datarails-finance-os__detect_anomalies
  - mcp__datarails-finance-os__get_records_by_filter
  - Write
  - Read
  - Bash
argument-hint: "[--table-id <id>] [--severity <level>] [--env <env>] [--output <file>]"
---

# Anomaly Detection Report

Generate comprehensive data quality assessment report with automated anomaly detection.

This skill automatically discovers your data structure and detects issues without requiring pre-configuration. Works with any Datarails Finance OS table.

## Design Principles

**General-Purpose**:
- ✅ No hardcoded table IDs or field names
- ✅ Adapts to any client structure
- ✅ Works with and without client profiles
- ✅ Falls back to discovery mode if profile missing

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--table-id <id>` | Specific table to analyze | Uses profile or discovers automatically |
| `--severity <level>` | Filter results: critical, high, medium, low | All |
| `--env <env>` | Environment: dev, demo, testapp, app | Active |
| `--output <file>` | Output filename | `tmp/Anomaly_Report_TIMESTAMP.xlsx` |

## What It Reports

### Summary Sheet
- **Data Quality Score** (0-100)
- Health status indicator
- Anomaly count by severity
- Key metrics

### Critical Findings Sheet
- Anomalies requiring immediate attention
- Sample records for investigation
- Field-specific details
- Recommended actions

### High Priority Sheet
- Issues to address this week
- Full descriptions
- Count and context

### Analysis Sheets
- **Numeric Analysis**: Min, max, mean, std dev for numeric fields
- **Categorical Analysis**: Distinct values, cardinality, frequency
- **Sample Records**: Actual data samples for top anomalies

## Workflow

**Phase 1: Discovery**
1. Verify authentication (`check_auth_status`)
2. If no `--table-id`, discover tables or use profile
3. Load table schema

**Phase 2: Anomaly Detection**
1. Run `detect_anomalies` - Automated data quality checks
2. Profile numeric fields - Statistics and outliers
3. Profile categorical fields - Cardinality and frequencies
4. Fetch sample records - Get actual data for investigation

**Phase 3: Report Generation**
1. Categorize findings by severity
2. Generate Excel workbook with multiple sheets
3. Apply professional formatting
4. Calculate data quality score

**Phase 4: Summary**
1. Display key findings
2. Show health status
3. Guide next steps

## Examples

### Analyze default financials table
```bash
/dr-anomalies-report --env app
```

Output:
```
🔍 Discovering financials table...
✓ Found financials table: 16528

📊 Analyzing table 16528...
  🔬 Running anomaly detection...
  📈 Profiling numeric fields...
  📝 Profiling categorical fields...
  🔍 Fetching sample records...
  📊 Summarizing results...
  📄 Generating Excel report...

✅ Report generated: tmp/Anomaly_Report_2026-02-03_143022.xlsx

==================================================
ANOMALY DETECTION SUMMARY
==================================================
Table: 16528
Total Anomalies: 45
Data Quality Score: 87/100

By Severity:
  Critical: 2
  High: 8
  Medium: 23
  Low: 12

Report: tmp/Anomaly_Report_2026-02-03_143022.xlsx
==================================================
```

### Analyze specific table for critical issues only
```bash
/dr-anomalies-report --table-id 16528 --severity critical
```

### Analyze development environment
```bash
/dr-anomalies-report --env dev
```

### Save to custom location
```bash
/dr-anomalies-report --env app --output tmp/Quality_Check_Feb_2026.xlsx
```

## Data Quality Score

Score ranges from 0-100:
- **90-100** ✅ **Excellent** - Minimal issues, data is reliable
- **80-90** 🟢 **Good** - Minor issues, generally usable
- **70-80** 🟡 **Fair** - Moderate issues, needs attention
- **70** 🟠 **Poor** - Significant issues, requires action
- **<70** 🔴 **Critical** - Major issues, immediate action required

Calculation:
```
Score = 100 - (critical×10 + high×5 + medium×2 + low×0.5)
Clamped to 0-100 range
```

## Adaptive Behavior

### With Client Profile
- Uses table IDs from `config/client-profiles/<env>.json`
- Uses discovered field names and mappings
- Applies business rules from profile notes

### Without Client Profile
- Lists available tables
- Automatically discovers table schema
- Infers field purposes from names and data types
- Uses general data quality rules

### Fallback Discovery
If profile incomplete or unavailable:
1. List all Finance OS tables
2. Identify likely data tables (those with numeric fields)
3. Get full schema
4. Discover field purposes automatically
5. Run analysis

## Use Cases

### Monthly Data Quality Check
```bash
/dr-anomalies-report --env app --output tmp/DQ_Check_$(date +%Y-%m).xlsx
```

### Pre-Month-End Close Validation
```bash
/dr-anomalies-report --env app --severity critical
```
*Alerts on critical issues that could affect close*

### Department Data Audit
```bash
/dr-anomalies-report --table-id 12345 --severity high
```
*Checks specific department data for issues*

### Exploratory Analysis
```bash
/dr-anomalies-report --env dev --table-id unknown_table_id
```
*Discovers what's in an unfamiliar table*

## Output Files

Reports are saved to: `tmp/Anomaly_Report_YYYY-MM-DD_HHMMSS.xlsx`

Each report includes:
- Professional formatting with colors
- Severity-based highlighting
- Embedded sample data
- Statistical analysis
- Investigation queries

## Troubleshooting

**"Not authenticated" error**
- Run `/dr-auth --env app` first

**"No tables found" error**
- Check that authentication succeeded
- Verify you have access to Finance OS

**"Table not found" error**
- Verify table ID is correct
- Run `/dr-tables --env app` to see available tables

**"Incomplete profile" error**
- Run `/dr-learn --env app` to refresh profile
- Or specify `--table-id` to override

## Related Skills

- `/dr-tables` - List and explore available tables
- `/dr-learn` - Discover and create client profiles
- `/dr-extract` - Extract validated financial data
- `/dr-reconcile` - Compare P&L vs KPI data

## Performance

- Small tables (< 10K rows): ~30 seconds
- Medium tables (10-100K rows): ~1-2 minutes
- Large tables (100K+ rows): ~5-10 minutes

Scaling handled automatically via pagination and efficient MCP tools.
