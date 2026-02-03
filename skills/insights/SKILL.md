---
name: dr-insights
description: Generate executive-ready insights with trend analysis and visualizations. Creates professional PowerPoint presentations and Excel data books.
user-invocable: true
allowed-tools:
  - mcp__datarails-finance-os__check_auth_status
  - mcp__datarails-finance-os__aggregate_table_data
  - mcp__datarails-finance-os__list_finance_tables
  - Write
  - Read
  - Bash
argument-hint: "[--year <YYYY>] [--quarter <Q#>] [--env <env>] [--output-pptx <file>] [--output-xlsx <file>]"
---

# Financial Insights Report

Generate executive-ready insights with trend analysis, KPI dashboards, and professional visualizations.

Creates both PowerPoint presentations (for meetings) and Excel data books (for detailed analysis).

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--year <YYYY>` | Calendar year to analyze | Current year |
| `--quarter <Q#>` | Quarter: Q1, Q2, Q3, Q4 | Current quarter |
| `--period <period>` | Combined period: YYYY-QX or YYYY-MM | Auto-determined |
| `--env <env>` | Environment: dev, demo, testapp, app | Active |
| `--output-pptx <file>` | PowerPoint output path | `tmp/Insights_TIMESTAMP.pptx` |
| `--output-xlsx <file>` | Excel output path | `tmp/Insights_Data_TIMESTAMP.xlsx` |

## What It Analyzes

### Revenue & Growth
- Monthly revenue trends (12+ months)
- Period-over-period growth rates (MoM, QoQ)
- Revenue by account category
- Trend analysis and momentum

### Key Performance Indicators
- ARR (Annual Recurring Revenue)
- Net New ARR
- Churn rate and dollar churn
- LTV (Lifetime Value)
- CAC (Customer Acquisition Cost)
- Burn rate and runway

### Operational Metrics
- Gross profit and margins
- Operating expenses by category
- Headcount trends
- Per-employee productivity metrics
- Department performance

### Financial Health
- Cash burn multiple
- CAC payback period
- LTV/CAC ratio
- Efficiency score

## Output: PowerPoint Presentation

Professional 7-slide presentation includes:

1. **Title Slide** - Report period and date
2. **Executive Summary** - Top metrics with trend indicators
3. **Key Findings** - Top 5 insights with business impact
4. **Recommendations** - Actionable next steps
5. **Metrics Dashboard** - KPI summary with sparklines
6. **Efficiency Analysis** - Ratios and operational metrics
7. **Data Summary** - Data sources and methodology

### Design Features
- Professional color scheme matching Datarails brand
- Embedded charts and visualizations
- Metrics boxes with trend indicators
- Consistent formatting across all slides
- Executive-friendly layout

## Output: Excel Data Book

Comprehensive workbook includes:

1. **Summary Sheet**
   - Key findings formatted as table
   - Severity and category indicators
   - Current vs prior period comparison

2. **Recommendations Sheet**
   - Prioritized action items
   - Implementation guidance
   - Expected impact

3. **Metrics Sheet**
   - Current KPI values
   - Targets (if available)
   - Prior period comparison

4. **Detailed Trends**
   - Monthly P&L breakdown
   - Account-level detail
   - Year-over-year comparison

5. **Data Sources**
   - Tables and fields used
   - Data refresh timestamp
   - Methodology notes

## Workflow

### Phase 1: Data Collection
1. Verify authentication
2. Load client profile
3. Fetch P&L trends (12 months)
4. Fetch KPI metrics (4+ quarters)

### Phase 2: Analysis
1. Calculate growth rates
2. Compute efficiency ratios
3. Identify trends and anomalies
4. Generate business insights
5. Create recommendations

### Phase 3: Presentation Generation
1. Create PowerPoint with 7 professional slides
2. Generate Excel data book
3. Embed charts and metrics
4. Apply professional formatting

### Phase 4: Output
1. Save both files to tmp/
2. Display summary to user
3. Provide file locations

## Examples

### Generate current quarter insights
```bash
/dr-insights --env app
```

Output:
```
📊 Generating insights for 2026-Q1...
  📊 Fetching P&L trends...
  📈 Fetching KPI metrics...
  💡 Calculating insights...
  📄 Generating PowerPoint presentation...
  📋 Generating Excel data book...

✅ Insights generated successfully

==================================================
INSIGHTS GENERATED
==================================================
Period: 2026-Q1
Key Findings: 5

Outputs:
  PowerPoint: tmp/Insights_2026-02-03_143022.pptx
  Excel: tmp/Insights_Data_2026-02-03_143022.xlsx
==================================================
```

### Generate specific quarter
```bash
/dr-insights --year 2025 --quarter Q4 --env app
```

### Generate previous month
```bash
/dr-insights --period 2026-01 --env app
```

### Save to custom location
```bash
/dr-insights --year 2025 --quarter Q4 \
  --output-pptx reports/Q4_2025_Insights.pptx \
  --output-xlsx reports/Q4_2025_Data.xlsx
```

## Use Cases

### Board Presentations
```bash
/dr-insights --quarter Q4 --year 2025 --env app
# Use PowerPoint for board meeting
```

### Executive Dashboard Updates
```bash
# Weekly insights
/dr-insights --env app
```

### Quarterly Business Reviews
```bash
# Comprehensive analysis for stakeholders
/dr-insights --year 2025 --quarter Q4 --env app
```

### Investor Communications
```bash
# Professional presentation for investors
/dr-insights --quarter Q4 --year 2025
```

### Department Reviews
```bash
# Share with teams for transparency
/dr-insights --env app
```

## Key Metrics Included

**Growth Metrics**:
- Revenue MoM/QoQ/YoY growth
- ARR trends
- Net New ARR

**Profitability Metrics**:
- Gross profit and margin
- Operating expense ratio
- EBITDA

**Unit Economics**:
- CAC (Customer Acquisition Cost)
- LTV (Lifetime Value)
- LTV/CAC ratio
- Payback period

**Cash Metrics**:
- Monthly burn rate
- Runway (months of cash)
- Burn multiple (burn rate / revenue)

**Churn & Retention**:
- Dollar churn
- Percentage churn
- Net revenue retention

## Performance

- Small datasets (1-2 years): ~1-2 minutes
- Large datasets (3+ years): ~3-5 minutes

Fast processing via efficient MCP aggregation tools.

## Error Handling

**"Not authenticated" error**
- Run `/dr-auth --env app` first

**"No KPI data found" warning**
- Agent adapts and focuses on P&L trends
- Recommendations still generated

**"Incomplete data for period" warning**
- Agent includes available data
- Highlights gaps in report

## Related Skills

- `/dr-anomalies-report` - Data quality assessment
- `/dr-reconcile` - P&L vs KPI validation
- `/dr-dashboard` - Executive KPI monitoring
- `/dr-extract` - Full financial data extraction

## Advanced Usage

### Automated Insights
```bash
# Schedule weekly insights
0 8 * * 1 /dr-insights --env app --output-pptx tmp/weekly_insights.pptx
```

### Comparative Analysis
```bash
# Generate for multiple quarters
/dr-insights --year 2025 --quarter Q1 --output-pptx tmp/Q1.pptx
/dr-insights --year 2025 --quarter Q2 --output-pptx tmp/Q2.pptx
# Compare side-by-side
```

### Custom Reporting
```bash
# Export data in custom location
/dr-insights --env app \
  --output-xlsx /shared/reports/latest_analysis.xlsx \
  --output-pptx /shared/reports/latest_presentation.pptx
```

## Customization

Insights adapt to client profiles at `config/client-profiles/{env}.json`:
- Different account hierarchies
- Custom KPI definitions
- Department structures
- Business rules

Modify profile to customize insights.

## Data Freshness

Reports include generation timestamp. Data reflects:
- Latest available P&L (typically current month)
- Latest available KPIs (typically current quarter)
- Calculations performed at generation time

For historical comparison, generate reports for multiple periods.
