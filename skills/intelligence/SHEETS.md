# 10-Sheet Workbook Specification

Order matters — the dashboard is sheet 1, raw data is sheet 10. Each sheet must include a generation timestamp footer and the year analyzed.

## Sheet Definitions

1. **Insights Dashboard** — Top 5 findings with severity color, current period KPIs (Revenue, Gross Margin, OpEx, Burn, Runway), and the ranked recommendations list.
2. **Expense Deep Dive** — Top 20 expense accounts: amount, % of total OpEx, MoM change %, YoY change %. Color the % cells with a green-to-red color scale.
3. **Variance Waterfall** — Current period vs. prior period: contribution to total variance line by line. Use a bar chart.
4. **Trend Analysis** — 12-month rolling P&L: Revenue, COGS, Gross Profit, OpEx, Net Income. One line per metric, secondary axis for margin %.
5. **Anomaly Report** — Auto-detected outliers from `detect_anomalies` plus the sigma-based rule. Severity column, drill-down hint per row.
6. **Vendor Analysis** — Top 20 vendors: spend, % of OpEx, MoM change. Concentration risk flag column. Pie chart for top 10.
7. **SaaS Metrics** — ARR, Net New ARR, NRR, GRR, CAC, LTV, LTV/CAC, Magic Number, Burn Multiple, CAC Payback. Quarterly columns; YoY column at right.
8. **Sales Performance** — Rep-level: bookings, win rate, ACV, ramp status. Cohort table by hire quarter.
9. **Cost Center P&L** — Department by month grid with totals row and YoY column. Conditional formatting on change %.
10. **Raw Data** — Long-form pivot-ready dataset (the monthly L1 by L2 frame). No formatting — just headers and data.
