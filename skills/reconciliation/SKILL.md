---
name: dr-reconcile
description: Reconcile P&L vs KPI data sources. Validates consistency and identifies discrepancies with variance analysis.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__list_finance_tables
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--scenario <name>] [--tolerance-pct <#>] [--env <env>] [--output <file>]"
---

# P&L vs KPI Reconciliation

Validate consistency between P&L and KPI data sources. Identifies discrepancies and explains variances.

Essential for month-end close and financial validation.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to reconcile | — |
| `--scenario <name>` | Scenario to reconcile | `Actuals` |
| `--tolerance-pct <#>` | Acceptable variance threshold | `5.0` |
| `--env <env>` | Environment: dev, demo, testapp, app | Active |
| `--output <file>` | Output file path | `tmp/Reconciliation_YYYY_TIMESTAMP.xlsx` |

## What It Validates

### Revenue Consistency
- P&L Revenue vs KPI Revenue
- Within tolerance threshold
- Identifies timing differences

### Expense Completeness
- COGS + Operating Expense coverage
- Validation of expense structure
- Missing expense categories

### Data Completeness
- All expected accounts present
- All expected KPI metrics available
- Data quality validation

### Variance Analysis
- Absolute variance amounts
- Percentage variance
- Tolerance compliance
- Root cause identification

## Output

Excel report with multiple sheets:

1. **Summary** - Pass/fail status, metrics, exception count
2. **Validation Rules** - Detailed results of each check
3. **Exceptions** (if any) - Issues exceeding tolerance
4. **P&L Summary** - Revenue, expenses by account
5. **KPI Summary** - All KPI values for verification

## Examples

### Reconcile current year (default 5% tolerance)
```bash
/dr-reconcile --year 2025
```

### Strict reconciliation (1% tolerance)
```bash
/dr-reconcile --year 2025 --tolerance-pct 1.0
```

### Reconcile specific scenario
```bash
/dr-reconcile --year 2025 --scenario Forecast
```

### Development environment
```bash
/dr-reconcile --year 2025 --env dev
```

### Custom output location
```bash
/dr-reconcile --year 2025 --output reports/reconciliation_2025.xlsx
```

## Use Cases

### Month-End Close
Run after data extraction to validate:
```bash
/dr-extract --year 2025
/dr-anomalies-report --severity critical    # Check quality
/dr-reconcile --year 2025 --tolerance-pct 2 # Validate consistency
```

### Financial Review
Reconcile before presentations:
```bash
/dr-reconcile --year 2025 --scenario Actuals
```

### Audit Preparation
Reconcile with strict tolerance:
```bash
/dr-reconcile --year 2025 --tolerance-pct 0.5
```

## Performance

- Year reconciliation: ~30-60 seconds
- Includes 3+ validation checks
- Scalable to large data volumes

## Error Handling

**"Revenue not found"** - Check P&L vs KPI account names in profile

**"Variance exceeds tolerance"** - Review exception sheet for details

**"Incomplete data"** - Run `/dr-extract` to refresh data first

## Related Skills

- `/dr-extract` - Get latest financial data
- `/dr-anomalies-report` - Check data quality
- `/dr-dashboard` - Verify KPI values
- `/dr-insights` - Understand trends driving reconciliation items
