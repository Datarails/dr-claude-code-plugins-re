# Reconciliation Agent

A specialized agent for validating consistency between P&L and KPI data sources.

## Description

This agent automatically reconciles financial data across different tables, identifying discrepancies and explaining variances.

Critical for month-end close, audit preparation, and data validation processes.

## Role & Capabilities

**Role**: Financial data validator and consistency auditor

**Key Capabilities**:
- Autonomous P&L vs KPI comparison
- Variance calculation and analysis
- Tolerance threshold validation
- Exception identification and prioritization
- Root cause analysis
- Validation rule execution

## When to Use

Use this agent when you need to:
- **Month-end close** - Validate data consistency before publishing
- **Audit preparation** - Ensure P&L and KPI alignment
- **Data quality review** - Identify reconciliation exceptions
- **Financial review** - Prepare reconciliation schedules
- **System migration** - Validate data after system changes

## Workflow

1. **Load Profile** - Get account mappings and hierarchies
2. **Fetch Data** - Retrieve P&L and KPI data
3. **Execute Checks** - Run validation rules
4. **Analyze Variance** - Calculate differences vs tolerance
5. **Generate Report** - Create Excel with findings
6. **Communicate Results** - Display pass/fail status

## Validation Checks

**Revenue Consistency**: P&L Revenue vs KPI Revenue within tolerance
**Expense Completeness**: COGS + OpEx coverage check
**Data Completeness**: All expected accounts and metrics present
**Threshold Compliance**: Variances within acceptable tolerance

## Output

Excel report with:
- Summary (pass/fail status)
- Validation rules (details of each check)
- Exceptions (issues requiring attention)
- P&L summary (all accounts and amounts)
- KPI summary (all metrics and values)

## Example Interactions

### Annual Reconciliation

**User**: "Reconcile our 2025 financials"

**Agent**:
1. Loads profile for current environment
2. Fetches all P&L data for 2025
3. Fetches all KPI data for 2025
4. Runs 4 validation checks
5. Calculates variances vs 5% tolerance
6. Generates Excel report
7. Displays results

**Output**:
```
Year: 2025
Checks: 4 total
  Passed: 3
  Failed: 1
Exceptions: 2 issues found

Report: tmp/Reconciliation_2025_[timestamp].xlsx
```

### Month-End Close

**User**: "Validate February close"

**Workflow**:
1. Extract latest actuals (/dr-extract)
2. Check data quality (/dr-anomalies-report)
3. Reconcile P&L vs KPI (/dr-reconcile)
4. Approve or investigate exceptions

### Strict Audit

**User**: "Audit reconciliation with 1% tolerance"

**Command**:
```bash
/dr-reconcile --year 2025 --tolerance-pct 1.0
```

**Result**: Identifies even small discrepancies for audit trail

## Performance

- Single year: ~30-60 seconds
- Multiple checks executed automatically
- Exception prioritization
- Scalable to large datasets

## Error Handling

**Revenue Mismatch**: Checks account hierarchy in profile
**Missing KPIs**: Reports incomplete data
**Tolerance Exceeded**: Shows exception details for investigation

## Integration

Works within workflows:
```
/dr-extract --year 2025          (Get latest data)
  ↓
/dr-anomalies-report --severity critical (Check quality)
  ↓
/dr-reconcile --year 2025        (Validate consistency)
  ↓
Present results to leadership
```

## Related Agents

- **Anomaly Detection** - Data quality validation
- **Insights** - Trend context for variances
- **Dashboard** - Real-time KPI monitoring
- **Forecast** - Budget variance analysis
