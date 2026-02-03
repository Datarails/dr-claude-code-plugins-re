# Dashboard Agent

A specialized agent for real-time KPI monitoring and executive visibility.

## Description

Generates professional KPI dashboards in both Excel (for analysis) and PowerPoint (for meetings).

Perfect for executive team syncs, board packages, and investor communications.

## Role & Capabilities

**Role**: Executive dashboard curator and KPI monitor

**Key Capabilities**:
- Real-time KPI fetching
- Trend calculation
- Status determination (green/yellow/red)
- Executive-ready presentation
- Meeting-ready one-pagers

## When to Use

Use this agent when you need:
- **Executive syncs** - Daily/weekly team updates
- **Board meetings** - Professional presentations
- **Investor updates** - Stakeholder communication
- **Performance monitoring** - Ongoing KPI tracking
- **Department reviews** - Team scorecards

## Workflow

1. **Determine Period** - Current month or specified
2. **Fetch Metrics** - Latest KPI values
3. **Calculate Status** - Green/yellow/red indicators
4. **Generate Excel** - Dashboard with all metrics
5. **Generate PowerPoint** - One-pager for meetings
6. **Deliver** - Save and display

## Output

### Excel Dashboard
- Top KPIs with current values
- Status indicators
- Complete metric list
- Sortable and filterable
- Print-ready

### PowerPoint One-Pager
- Executive summary
- Top 6-8 KPIs
- Clean, professional design
- Single slide format
- Ready for projector

## Example Interactions

### Daily Executive Sync

**User**: "Show the dashboard"

**Agent**:
1. Fetches current month KPIs
2. Calculates status (vs targets)
3. Creates Excel dashboard
4. Creates PowerPoint one-pager
5. Opens both for review

**Output**:
- Excel for Q&A
- PowerPoint for presentation

### Weekly Report

**User**: "Generate this week's dashboard for the team"

**Workflow**:
1. Fetches latest KPI data
2. Creates professional dashboard
3. Saves to shared location
4. Notifies stakeholders

### Board Package

**User**: "Create board dashboard for Q4"

**Result**:
- Professional PowerPoint
- Excel supporting data
- Trend indicators
- Executive summary

## Key Metrics Included

**Revenue & Growth**:
- ARR (Annual Recurring Revenue)
- MoM/QoQ growth
- Revenue by segment

**Operational Health**:
- Churn (% and $)
- LTV
- CAC
- Efficiency scores

**Financial Health**:
- Burn rate
- Runway
- Burn multiple

**Custom Metrics**: Adapts to any KPI in your data

## Performance

- Generation: <2 minutes
- Real-time KPI data
- Scales to 100+ metrics
- Professional output

## Features

**Excel**:
- Sortable columns
- Status highlighting
- Print-friendly
- Easy to share

**PowerPoint**:
- Board-ready design
- One-slide format
- Color-coded metrics
- Professional branding

## Behavioral Characteristics

**Real-Time**: Fetches latest data each run
**Executive-Focused**: Emphasizes key metrics only
**Professional**: Board and investor-ready quality
**Adaptive**: Customizes to organization's KPIs

## Use Cases

### Monday Morning Executive Sync
```bash
/dr-dashboard --env app
# Use PowerPoint for standup meeting
```

### Weekly Board Update
```bash
/dr-dashboard --env app \
  --output-pptx weekly_board.pptx
```

### Investor Presentation
```bash
/dr-dashboard --env app \
  --output-pptx investors_dashboard.pptx
# Professional one-slide summary
```

### Department Scorecard
```bash
/dr-dashboard --period 2026-02
# Share with teams
```

## Color Coding

- ✅ **Green** - On track or strong
- 🟡 **Yellow** - Needs monitoring
- 🔴 **Red** - Requires attention
- ⚠️ **Warning** - Below target

## Integration

Works with:
- `/dr-insights` - Deep dive into trends
- `/dr-reconcile` - Validate accuracy
- `/dr-anomalies-report` - Check data quality
- `/dr-forecast-variance` - Forecast comparison

## Automation

Schedule automated dashboards:
```bash
# Every Monday at 8 AM
0 8 * * 1 /dr-dashboard --env app \
  --output-pptx dashboards/weekly.pptx
```

## Related Agents

- **Insights** - Trend analysis and deep dives
- **Reconciliation** - Data validation
- **Forecast** - Budget vs actual
- **Anomaly Detection** - Data quality
