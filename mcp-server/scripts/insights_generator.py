#!/usr/bin/env python3
"""
Datarails Insights Agent

Generates executive-ready insights with visualizations and trend analysis.
Creates professional PowerPoint presentations and Excel data books.

Usage:
    uv --directory mcp-server run python scripts/insights_generator.py --year 2025
    uv --directory mcp-server run python scripts/insights_generator.py --quarter Q4 --year 2025 --env app
    uv --directory mcp-server run python scripts/insights_generator.py --period 2025-Q4 --output-pptx tmp/insights.pptx
"""

import argparse
import json
import sys
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# Add mcp-server/src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datarails_mcp.auth import get_auth
from datarails_mcp.client import DatarailsClient
from datarails_mcp.report_utils import (
    format_currency,
    format_percentage,
    format_ratio,
    calculate_growth_rate,
    safe_divide,
)
from datarails_mcp.chart_builder import line_chart, bar_chart, waterfall_chart
from datarails_mcp.excel_builder import ExcelReport
from datarails_mcp.pptx_builder import PowerPointReport


# Default profile
DEFAULT_PROFILE = {
    "tables": {
        "financials": {
            "id": "16528",
            "name": "Financials Cube",
        },
        "kpis": {
            "id": "34298",
            "name": "KPI Metrics",
        }
    },
    "field_mappings": {
        "amount": "Amount",
        "date": "Reporting Date",
        "account_l1": "DR_ACC_L1",
        "scenario": "Scenario",
        "kpi_name": "KPI",
        "kpi_value": "value",
        "quarter": "Quarter & Year",
    },
    "account_hierarchy": {
        "revenue": "REVENUE",
        "cogs": "Cost of Good sold",
        "opex": "Operating Expense",
    },
}


def load_profile(env: str) -> dict:
    """Load client profile for environment."""
    profile_path = Path(__file__).parent.parent.parent / "config" / "client-profiles" / f"{env}.json"

    if profile_path.exists():
        try:
            with open(profile_path) as f:
                profile = json.load(f)
            print(f"✓ Loaded profile: {env}")
            return profile
        except Exception as e:
            print(f"⚠ Error loading profile {env}: {e}")
            return DEFAULT_PROFILE
    else:
        print(f"ℹ Using default profile structure")
        return DEFAULT_PROFILE


async def fetch_pl_trends(
    client: DatarailsClient,
    profile: dict,
    months: int = 12,
    scenario: str = "Actuals"
) -> dict:
    """Fetch P&L trend data over specified months."""
    print("  📊 Fetching P&L trends...")

    table_id = profile.get("tables", {}).get("financials", {}).get("id", "16528")
    amount_field = profile.get("field_mappings", {}).get("amount", "Amount")
    date_field = profile.get("field_mappings", {}).get("date", "Reporting Date")
    account_field = profile.get("field_mappings", {}).get("account_l1", "DR_ACC_L1")
    scenario_field = profile.get("field_mappings", {}).get("scenario", "Scenario")

    account_hierarchy = profile.get("account_hierarchy", {})

    try:
        # Fetch aggregated P&L data by month and account
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[date_field, account_field],
            metrics=[{"field": amount_field, "agg": "SUM"}],
            filters=[
                {"name": scenario_field, "values": [scenario], "is_excluded": False}
            ]
        )

        # Organize data by account
        pl_data = defaultdict(lambda: defaultdict(float))

        if data and isinstance(data, list):
            for row in data:
                date = row.get(date_field, "")
                account = row.get(account_field, "Unknown")
                amount = float(row.get(amount_field, 0))
                pl_data[account][date] = amount

        return {
            "raw_data": dict(pl_data),
            "accounts": list(pl_data.keys()),
            "dates": sorted(set(d for account_data in pl_data.values() for d in account_data.keys()))
        }

    except Exception as e:
        print(f"    ⚠ Error fetching P&L trends: {e}")
        return {"raw_data": {}, "accounts": [], "dates": []}


async def fetch_kpi_metrics(
    client: DatarailsClient,
    profile: dict,
    quarters: int = 4,
    scenario: str = "Actuals"
) -> dict:
    """Fetch KPI metrics for specified quarters."""
    print("  📈 Fetching KPI metrics...")

    table_id = profile.get("tables", {}).get("kpis", {}).get("id", "34298")
    kpi_name_field = profile.get("field_mappings", {}).get("kpi_name", "KPI")
    kpi_value_field = profile.get("field_mappings", {}).get("kpi_value", "value")
    quarter_field = profile.get("field_mappings", {}).get("quarter", "Quarter & Year")
    scenario_field = profile.get("field_mappings", {}).get("scenario", "Scenario")

    try:
        # Fetch KPI data
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[quarter_field, kpi_name_field],
            metrics=[{
                "field": kpi_value_field,
                "agg": "MAX"  # KPIs are typically already aggregated
            }],
            filters=[
                {"name": scenario_field, "values": [scenario], "is_excluded": False}
            ]
        )

        kpi_data = defaultdict(lambda: defaultdict(float))

        if data and isinstance(data, list):
            for row in data:
                quarter = row.get(quarter_field, "")
                kpi_name = row.get(kpi_name_field, "Unknown")
                value = float(row.get(kpi_value_field, 0))
                kpi_data[kpi_name][quarter] = value

        return {
            "raw_data": dict(kpi_data),
            "kpis": list(kpi_data.keys()),
            "quarters": sorted(set(q for kpi_metrics in kpi_data.values() for q in kpi_metrics.keys()))
        }

    except Exception as e:
        print(f"    ⚠ Error fetching KPI metrics: {e}")
        return {"raw_data": {}, "kpis": [], "quarters": []}


async def generate_insights(
    env: str,
    period: str = None,
    year: int = None,
    quarter: str = None,
    output_pptx: str = None,
    output_xlsx: str = None,
) -> dict:
    """Generate insights with trends and metrics."""
    # Parse period parameter
    if period:
        # Format: YYYY-QX or YYYY-MM
        parts = period.split("-")
        if len(parts) == 2:
            year = int(parts[0])
            quarter = parts[1].upper()

    if not year:
        year = datetime.now().year

    if not quarter:
        # Determine current quarter
        month = datetime.now().month
        quarter = f"Q{(month - 1) // 3 + 1}"

    # Load profile
    profile = load_profile(env)

    # Authenticate
    print(f"🔐 Authenticating with {env}...")
    auth = get_auth()

    if not auth.is_authenticated():
        return {
            "error": "NOT_AUTHENTICATED",
            "message": "Not authenticated with Datarails",
            "action": f"Run '/dr-auth --env {env}' to authenticate",
        }

    client = DatarailsClient(auth)

    try:
        print(f"\n📊 Generating insights for {year}-{quarter}...")

        # Fetch data
        pl_trends = await fetch_pl_trends(client, profile)
        kpi_metrics = await fetch_kpi_metrics(client, profile)

        # Calculate insights
        print("  💡 Calculating insights...")
        insights = calculate_business_insights(
            pl_trends=pl_trends,
            kpi_metrics=kpi_metrics,
            profile=profile
        )

        # Generate outputs
        print("  📄 Generating PowerPoint presentation...")
        pptx_path = generate_powerpoint_report(
            title=f"Financial Insights - {year}-{quarter}",
            insights=insights,
            pl_trends=pl_trends,
            kpi_metrics=kpi_metrics,
            profile=profile,
            output_file=output_pptx
        )

        print("  📋 Generating Excel data book...")
        xlsx_path = generate_excel_databook(
            insights=insights,
            pl_trends=pl_trends,
            kpi_metrics=kpi_metrics,
            year=year,
            quarter=quarter,
            output_file=output_xlsx
        )

        print(f"\n✅ Insights generated successfully")

        return {
            "success": True,
            "year": year,
            "quarter": quarter,
            "powerpoint": pptx_path,
            "excel": xlsx_path,
            "insights": insights,
        }

    finally:
        await client.close()


def calculate_business_insights(pl_trends: dict, kpi_metrics: dict, profile: dict) -> dict:
    """Calculate business insights from data."""
    insights = {
        "growth_metrics": {},
        "efficiency_metrics": {},
        "key_findings": [],
        "recommendations": [],
    }

    # Calculate growth rates
    raw_data = pl_trends.get("raw_data", {})
    if raw_data:
        # Get revenue trend
        revenue_account = profile.get("account_hierarchy", {}).get("revenue", "REVENUE")
        if revenue_account in raw_data:
            revenue_data = raw_data[revenue_account]
            dates = sorted(revenue_data.keys())

            if len(dates) >= 2:
                current_revenue = revenue_data.get(dates[-1], 0)
                previous_revenue = revenue_data.get(dates[-2], 0)

                growth_rate = calculate_growth_rate(current_revenue, previous_revenue)
                insights["growth_metrics"]["revenue_mom"] = growth_rate
                insights["growth_metrics"]["revenue_current"] = current_revenue

                # Add finding
                if growth_rate > 0.15:
                    insights["key_findings"].append({
                        "title": "Strong Revenue Growth",
                        "value": format_percentage(growth_rate),
                        "severity": "success"
                    })
                elif growth_rate < -0.10:
                    insights["key_findings"].append({
                        "title": "Revenue Decline",
                        "value": format_percentage(growth_rate),
                        "severity": "warning"
                    })

    # Calculate efficiency metrics
    kpi_data = kpi_metrics.get("raw_data", {})
    if kpi_data:
        # Look for key KPIs
        for kpi_name, kpi_values in kpi_data.items():
            if kpi_values:
                latest_value = list(kpi_values.values())[-1]
                insights["efficiency_metrics"][kpi_name] = latest_value

                # Add findings based on KPIs
                if "ARR" in kpi_name:
                    insights["key_findings"].append({
                        "title": "Annual Recurring Revenue",
                        "value": format_currency(latest_value),
                        "severity": "info"
                    })
                elif "Churn" in kpi_name and latest_value > 0:
                    severity = "warning" if latest_value > 0.10 else "info"
                    insights["key_findings"].append({
                        "title": "Customer Churn Rate",
                        "value": format_percentage(latest_value),
                        "severity": severity
                    })

    # Add recommendations
    if len(insights["key_findings"]) > 0:
        insights["recommendations"].append("Monitor key metrics regularly")
        insights["recommendations"].append("Compare against industry benchmarks")
        insights["recommendations"].append("Review departmental performance")

    return insights


def generate_powerpoint_report(
    title: str,
    insights: dict,
    pl_trends: dict,
    kpi_metrics: dict,
    profile: dict,
    output_file: str = None,
) -> str:
    """Generate PowerPoint presentation."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Insights_{timestamp}.pptx")

    report = PowerPointReport(title=title)

    # Slide 2: Executive Summary
    slide = report.add_slide("Executive Summary")

    summary_metrics = {}
    growth = insights.get("growth_metrics", {})
    if "revenue_mom" in growth:
        summary_metrics["Revenue Growth (MoM)"] = format_percentage(growth["revenue_mom"])
    if "revenue_current" in growth:
        summary_metrics["Current Revenue"] = format_currency(growth["revenue_current"])

    efficiency = insights.get("efficiency_metrics", {})
    metric_keys = list(efficiency.keys())[:2]
    for key in metric_keys:
        summary_metrics[key] = format_currency(efficiency[key])

    if summary_metrics:
        report.add_metrics_boxes(slide, summary_metrics, columns=2)

    # Slide 3: Key Findings
    slide = report.add_slide("Key Findings & Insights")
    findings = insights.get("key_findings", [])
    if findings:
        for idx, finding in enumerate(findings[:5]):
            y_pos = 1.5 + (idx * 1.0)
            title = finding.get("title", "Finding")
            value = finding.get("value", "—")
            report.add_text_box(slide, 0.5, y_pos, 4, 0.8, f"{title}: {value}", font_size=14)

    # Slide 4: Recommendations
    slide = report.add_slide("Recommendations")
    recommendations = insights.get("recommendations", [])
    if recommendations:
        report.add_bullet_points(slide, recommendations)

    # Slide 5: Data Summary
    slide = report.add_slide("Data Summary")
    data_summary = {
        "P&L Accounts": str(len(pl_trends.get("accounts", []))),
        "KPI Metrics": str(len(kpi_metrics.get("kpis", []))),
        "Date Range": f"{len(pl_trends.get('dates', []))} periods",
        "Data Freshness": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    report.add_metrics_boxes(slide, data_summary, columns=2)

    report.save(output_file)
    return output_file


def generate_excel_databook(
    insights: dict,
    pl_trends: dict,
    kpi_metrics: dict,
    year: int,
    quarter: str,
    output_file: str = None,
) -> str:
    """Generate Excel data book with supporting details."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Insights_Data_{timestamp}.xlsx")

    report = ExcelReport(title="Financial Insights Data Book")

    # Summary sheet
    report.add_title(f"Financial Insights - {year}-{quarter}")

    # Add key findings
    summary_data = []
    for finding in insights.get("key_findings", []):
        summary_data.append({
            "Finding": finding.get("title", ""),
            "Value": finding.get("value", "—"),
            "Category": finding.get("severity", "info").upper(),
        })

    if summary_data:
        report.add_data_table(summary_data, start_row=3)

    # Add recommendations sheet
    if insights.get("recommendations"):
        report.add_sheet("Recommendations")
        report.add_title("Recommendations & Action Items")

        rec_data = []
        for idx, rec in enumerate(insights.get("recommendations", []), 1):
            rec_data.append({
                "Item": str(idx),
                "Recommendation": rec,
                "Priority": "High" if idx <= 2 else "Medium",
            })

        report.add_data_table(rec_data, start_row=3)

    # Add metrics sheet
    if insights.get("efficiency_metrics"):
        report.add_sheet("Metrics")
        report.add_title("Key Performance Indicators")

        metrics_data = []
        for kpi_name, kpi_value in insights.get("efficiency_metrics", {}).items():
            metrics_data.append({
                "KPI": kpi_name,
                "Value": format_currency(kpi_value) if isinstance(kpi_value, (int, float)) else str(kpi_value),
            })

        if metrics_data:
            report.add_data_table(metrics_data, start_row=3)

    # Add data sources sheet
    report.add_sheet("Data Sources")
    report.add_title("Data Sources & Methodology")

    sources = []
    sources.append({
        "Source": "P&L Trends",
        "Accounts": str(len(pl_trends.get("accounts", []))),
        "Periods": str(len(pl_trends.get("dates", []))),
    })
    sources.append({
        "Source": "KPI Metrics",
        "Accounts": str(len(kpi_metrics.get("kpis", []))),
        "Periods": str(len(kpi_metrics.get("quarters", []))),
    })
    sources.append({
        "Source": "Analysis",
        "Accounts": "Growth rates, efficiency metrics",
        "Periods": f"Generated: {datetime.now().strftime('%Y-%m-%d')}",
    })

    report.add_data_table(sources, start_row=3)

    report.save(output_file)
    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate financial insights with trends and analysis"
    )
    parser.add_argument(
        "--env",
        default="app",
        choices=["app", "dev", "demo", "testapp"],
        help="Environment (default: app)"
    )
    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Calendar year (default: current year)"
    )
    parser.add_argument(
        "--quarter",
        default=None,
        choices=["Q1", "Q2", "Q3", "Q4"],
        help="Quarter (default: current quarter)"
    )
    parser.add_argument(
        "--period",
        default=None,
        help="Period as YYYY-QX (e.g., 2025-Q4) or YYYY-MM"
    )
    parser.add_argument(
        "--output-pptx",
        default=None,
        help="PowerPoint output file path"
    )
    parser.add_argument(
        "--output-xlsx",
        default=None,
        help="Excel output file path"
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(
            generate_insights(
                env=args.env,
                period=args.period,
                year=args.year,
                quarter=args.quarter,
                output_pptx=args.output_pptx,
                output_xlsx=args.output_xlsx,
            )
        )

        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            print(f"   {result.get('message', '')}")
            if "action" in result:
                print(f"   Action: {result['action']}")
            return 1

        print(f"\n{'='*50}")
        print(f"INSIGHTS GENERATED")
        print(f"{'='*50}")
        print(f"Period: {result['year']}-{result['quarter']}")
        print(f"Key Findings: {len(result['insights'].get('key_findings', []))}")
        print(f"\nOutputs:")
        print(f"  PowerPoint: {result['powerpoint']}")
        print(f"  Excel: {result['excel']}")
        print(f"{'='*50}\n")

        return 0

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
