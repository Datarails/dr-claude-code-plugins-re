---
name: dr-departments
description: Analyze P&L and performance by department. Creates departmental reports and comparative analysis with Excel and PowerPoint outputs.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__auth_status
  - mcp__datarails-finance-os__aggregate_table_data
  - Write
  - Read
  - Bash
argument-hint: "--year <YYYY> [--department <name>] [--output-xlsx <file>] [--output-pptx <file>]"
---

# Department Analytics

Analyze departmental P&L performance and resource allocation.

Creates detailed departmental reports for team leads and management reviews.

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | **REQUIRED** Calendar year | — |
| `--department <name>` | Specific department (optional) | All departments |
| `--output-xlsx <file>` | Excel output path | `tmp/Department_Analysis_YYYY_TIMESTAMP.xlsx` |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Department_Review_YYYY_TIMESTAMP.pptx` |

## Department Metrics

### Revenue & Expense
- Department revenue
- Expense breakdown
- Net contribution

### Performance
- Budget vs actual
- Variance analysis
- Year-over-year comparison

### Efficiency
- Per-employee metrics
- Cost per unit
- Productivity indicators

## Output

### Excel Department Pack
- Summary by department
- Detailed P&L per department
- Variance analysis
- Comparison charts

### PowerPoint Department Review
- One slide per department
- Key metrics highlight
- Budget performance
- Comparison to average

## Examples

### Analyze all departments
```bash
/dr-departments --year 2025
```

### Specific department review
```bash
/dr-departments --year 2025 --department Engineering
```

### Custom output
```bash
/dr-departments --year 2025 \
  --output-xlsx reports/depts_2025.xlsx \
  --output-pptx reports/dept_review.pptx
```

## Use Cases

### Monthly Department Reviews
```bash
# Share with department heads
/dr-departments --year 2025
```

### Department Head Meetings
```bash
# Individual department analysis for team
/dr-departments --year 2025 --department Marketing
```

### Executive Dashboard
```bash
# Department comparison for leadership
/dr-departments --year 2025
```

### Budget Planning
```bash
# Department historical analysis
/dr-departments --year 2024
/dr-departments --year 2025
# Use for next year planning
```

## Performance

- Analysis: 1-2 minutes
- Scales to all departments
- Professional output

## Department Metrics Included

**Financial**:
- Revenue
- Expenses
- Net contribution

**Operational**:
- Headcount
- Per-employee metrics
- Productivity

**Performance**:
- Budget variance
- Trend analysis
- YoY comparison

## Features

**Excel Report**:
- Summary by department
- Per-department P&L sheets
- Sortable data
- Print-friendly

**PowerPoint Review**:
- One slide per dept
- Key metrics
- Trend indicators
- Professional layout

## Integration

Works with:
- `/dr-insights` - Context for trends
- `/dr-dashboard` - Department KPIs
- `/dr-reconcile` - Validation
- `/dr-extract` - Data sourcing

## Related Skills

- `/dr-insights` - Trend analysis
- `/dr-dashboard` - KPI monitoring
- `/dr-reconcile` - Data validation
- `/dr-extract` - Data extraction
