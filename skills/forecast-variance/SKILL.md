---
name: dr-forecast-variance
description: Analyze budget vs forecast vs actual variances. Compares multi-scenario financial data for planning and performance review.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--scenarios <list>] [--period <YYYY-MM>] [--env <env>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Forecast Variance Analysis

Analyze variances between Actuals, Budget, and Forecast scenarios.

Essential for FP&A reviews, planning adjustments, and performance tracking.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year to analyze | — |
| `--scenarios <list>` | Comma-separated scenarios | `Actuals,Budget,Forecast` |
| `--period <YYYY-MM>` | Specific period to focus on | All year |
| `--env <env>` | Environment: dev, demo, testapp, app | Active |
| `--output-xlsx <file>` | Excel output path | `tmp/Forecast_Variance_YYYY_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Forecast_Summary_YYYY_TIMESTAMP.pptx` |

## Variance Analysis

### Budget Variance
- Actual vs Budget amounts
- Percentage difference
- Favorable/unfavorable identification
- Trend analysis

### Forecast Variance
- Actual vs Forecast amounts
- Track forecast accuracy
- Identify forecast bias
- Forecast adjustment recommendations

### Multi-Account Analysis
- Revenue variance by product/segment
- Expense variance by department
- Account-level drill-down
- Root cause identification

## Output

### Excel Report
- **Summary**: Total variances by scenario
- **Variance Analysis**: Account-by-account comparison
- **Scenario Totals**: Total by scenario
- **Exception Report**: Large variances highlighted

### PowerPoint Summary
- Overview slide: Scenario totals
- Variance slide: Top variances
- Executive summary
- Key findings

## Examples

### Annual variance analysis
```bash
/dr-forecast-variance --year 2025
```

### With custom scenarios
```bash
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
```

### Specific period focus
```bash
/dr-forecast-variance --year 2025 --period 2025-Q4
```

### Strict analysis (1% threshold)
```bash
/dr-forecast-variance --year 2025 --env app
```

### Development environment
```bash
/dr-forecast-variance --year 2025 --env dev
```

### Custom output
```bash
/dr-forecast-variance --year 2025 \
  --output-xlsx reports/variance_2025.xlsx \
  --output-pptx reports/variance_summary.pptx
```

## Use Cases

### Monthly FP&A Review
```bash
# Compare latest actuals vs budget
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
```

### Forecast Accuracy Tracking
```bash
# Compare forecast prediction accuracy
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast
```

### Full Scenario Planning
```bash
# Complete comparison for board review
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget,Forecast
```

### Department Review
```bash
# Analyze departmental performance vs budget
/dr-forecast-variance --year 2025
```

### Investor Update
```bash
# Professional variance analysis for stakeholders
/dr-forecast-variance --year 2025
```

## Performance

- Analysis: ~1-3 minutes
- Scales to multiple years
- Handles 100+ accounts
- Efficient aggregation

## Interpretation

### Favorable Variance
- Actual > Budget (Revenue) ✅
- Actual < Budget (Expense) ✅

### Unfavorable Variance
- Actual < Budget (Revenue) ❌
- Actual > Budget (Expense) ❌

### % Variance
- <5%: Excellent forecast/budget accuracy
- 5-10%: Good, within normal range
- 10%+: Needs investigation

## Workflow

**FP&A Process**:
```
1. /dr-extract --year 2025       (Get actuals)
2. /dr-reconcile --year 2025     (Validate data)
3. /dr-forecast-variance --year 2025  (Analyze variances)
4. Present findings to leadership (Board meeting)
```

## Advanced Usage

### Track forecast improvement
```bash
# Monthly variance tracking
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast --period 2025-01
/dr-forecast-variance --year 2025 --scenarios Actuals,Forecast --period 2025-02
# Compare forecast accuracy trend
```

### Multi-year comparison
```bash
/dr-forecast-variance --year 2024 --scenarios Actuals,Budget
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget
# Compare year-over-year performance
```

### Scenario sensitivity
```bash
# Three different budget scenarios
/dr-forecast-variance --year 2025 --scenarios Actuals,Budget_Conservative,Budget_Aggressive
```

## Error Handling

**"Scenario not found"** - Verify scenario exists in data

**"No variance data"** - Confirm Budget/Forecast scenarios available

**"Large variance"** - Review detailed Excel report for root causes

## Integration

Works with:
- `/dr-extract` - Source of scenario data
- `/dr-insights` - Contextual trend analysis
- `/dr-reconcile` - Validate scenario consistency
- `/dr-dashboard` - Current performance view

## Related Skills

- `/dr-extract` - Extract scenario data
- `/dr-insights` - Understand drivers of variances
- `/dr-reconcile` - Validate data consistency
- `/dr-dashboard` - Real-time performance
