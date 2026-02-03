#!/usr/bin/env python3
"""
Datarails Executive Dashboard

Generates real-time KPI monitoring dashboard with visualizations.
Creates Excel dashboards and PowerPoint one-pagers.

Usage:
    uv --directory mcp-server run python scripts/executive_dashboard.py --period 2026-02
    uv --directory mcp-server run python scripts/executive_dashboard.py --period 2026-02 --env app
    uv --directory mcp-server run python scripts/executive_dashboard.py --period 2026-02 --output-xlsx tmp/dashboard.xlsx
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
    calculate_growth_rate,
)
from datarails_mcp.excel_builder import ExcelReport
from datarails_mcp.pptx_builder import PowerPointReport


# Default profile
DEFAULT_PROFILE = {
    "tables": {
        "kpis": {
            "id": "34298",
            "name": "KPI Metrics",
        }
    },
    "field_mappings": {
        "kpi_name": "KPI",
        "kpi_value": "value",
        "quarter": "Quarter & Year",
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


async def generate_dashboard(
    env: str,
    period: str = None,
    output_xlsx: str = None,
    output_pptx: str = None,
) -> dict:
    """Generate executive dashboard."""
    # Parse period
    if not period:
        period = datetime.now().strftime("%Y-%m")

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
        print(f"\n📊 Generating dashboard for {period}...")

        # Fetch KPI data
        print("  📈 Fetching KPI metrics...")
        kpi_data = await fetch_kpi_data(client, profile)

        # Calculate trends
        print("  📊 Calculating trends...")
        dashboard_metrics = calculate_dashboard_metrics(kpi_data)

        # Generate outputs
        print("  📋 Generating Excel dashboard...")
        xlsx_path = generate_excel_dashboard(
            metrics=dashboard_metrics,
            kpi_data=kpi_data,
            period=period,
            output_file=output_xlsx
        )

        print("  🎯 Generating PowerPoint one-pager...")
        pptx_path = generate_pptx_onepager(
            metrics=dashboard_metrics,
            period=period,
            output_file=output_pptx
        )

        print(f"\n✅ Dashboard generated successfully")

        return {
            "success": True,
            "period": period,
            "metrics_count": len(dashboard_metrics),
            "excel": xlsx_path,
            "powerpoint": pptx_path,
            "metrics": dashboard_metrics,
        }

    finally:
        await client.close()


async def fetch_kpi_data(client: DatarailsClient, profile: dict) -> dict:
    """Fetch latest KPI data."""
    table_id = profile.get("tables", {}).get("kpis", {}).get("id", "34298")
    kpi_name_field = profile.get("field_mappings", {}).get("kpi_name", "KPI")
    kpi_value_field = profile.get("field_mappings", {}).get("kpi_value", "value")

    try:
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[kpi_name_field],
            metrics=[{"field": kpi_value_field, "agg": "MAX"}]
        )

        kpi_dict = {}
        if data and isinstance(data, list):
            for row in data:
                kpi_name = row.get(kpi_name_field, "Unknown")
                value = float(row.get(kpi_value_field, 0))
                kpi_dict[kpi_name] = value

        return kpi_dict

    except Exception as e:
        print(f"    ⚠ Error fetching KPI data: {e}")
        return {}


def calculate_dashboard_metrics(kpi_data: dict) -> dict:
    """Calculate metrics for dashboard."""
    metrics = {}

    # Key metrics
    key_kpis = [
        "ARR",
        "Revenue",
        "Churn %",
        "LTV",
        "CAC",
        "Burn Rate",
        "Runway",
    ]

    for kpi in key_kpis:
        for kpi_name, value in kpi_data.items():
            if kpi.lower() in kpi_name.lower():
                metrics[kpi] = value
                break

    return metrics


def generate_excel_dashboard(
    metrics: dict,
    kpi_data: dict,
    period: str,
    output_file: str = None,
) -> str:
    """Generate Excel dashboard."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Executive_Dashboard_{timestamp}.xlsx")

    report = ExcelReport(title="Executive Dashboard")

    # Summary sheet
    report.add_title(f"Executive KPI Dashboard - {period}")

    # Add top metrics
    summary_data = []
    for metric_name, value in metrics.items():
        if isinstance(value, float):
            if "%" in metric_name or "Churn" in metric_name:
                formatted_value = format_percentage(value)
            else:
                formatted_value = format_currency(value)
        else:
            formatted_value = str(value)

        summary_data.append({
            "KPI": metric_name,
            "Value": formatted_value,
            "Status": "✅" if value > 0 else "⚠️",
        })

    if summary_data:
        report.add_data_table(summary_data, start_row=3)

    # Add all KPIs sheet
    report.add_sheet("All Metrics")
    report.add_title("Complete KPI List")

    all_kpis_data = []
    for kpi_name, value in kpi_data.items():
        if isinstance(value, float):
            if "%" in kpi_name or "Churn" in kpi_name:
                formatted_value = format_percentage(value)
            else:
                formatted_value = format_currency(value)
        else:
            formatted_value = str(value)

        all_kpis_data.append({
            "KPI": kpi_name,
            "Current Value": formatted_value,
        })

    if all_kpis_data:
        report.add_data_table(all_kpis_data, start_row=3)

    report.save(output_file)
    return output_file


def generate_pptx_onepager(
    metrics: dict,
    period: str,
    output_file: str = None,
) -> str:
    """Generate PowerPoint one-pager."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Dashboard_OnePager_{timestamp}.pptx")

    report = PowerPointReport(title=f"Executive Dashboard - {period}")

    # Slide: KPI Summary
    slide = report.add_slide("KPI Summary")

    # Format metrics for display
    display_metrics = {}
    for metric_name, value in metrics.items():
        if isinstance(value, float):
            if "%" in metric_name or "Churn" in metric_name:
                display_metrics[metric_name] = format_percentage(value)
            elif "Runway" in metric_name or "Burn" in metric_name:
                display_metrics[metric_name] = f"{value:.1f}"
            else:
                display_metrics[metric_name] = format_currency(value)
        else:
            display_metrics[metric_name] = str(value)

    # Add metrics boxes (color-coded)
    if display_metrics:
        report.add_metrics_boxes(slide, display_metrics, columns=3)

    # Slide: Data Timestamp
    slide = report.add_slide("Dashboard Information")

    info = {
        "Report Period": period,
        "Generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Total Metrics": str(len(metrics)),
        "Data Source": "Finance OS KPI Table",
    }
    report.add_metrics_boxes(slide, info, columns=2)

    report.save(output_file)
    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate executive KPI dashboard"
    )
    parser.add_argument(
        "--env",
        default="app",
        choices=["app", "dev", "demo", "testapp"],
        help="Environment (default: app)"
    )
    parser.add_argument(
        "--period",
        default=None,
        help="Period YYYY-MM (default: current month)"
    )
    parser.add_argument(
        "--output-xlsx",
        default=None,
        help="Excel output file path"
    )
    parser.add_argument(
        "--output-pptx",
        default=None,
        help="PowerPoint output file path"
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(
            generate_dashboard(
                env=args.env,
                period=args.period,
                output_xlsx=args.output_xlsx,
                output_pptx=args.output_pptx,
            )
        )

        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            print(f"   {result.get('message', '')}")
            if "action" in result:
                print(f"   Action: {result['action']}")
            return 1

        print(f"\n{'='*50}")
        print(f"EXECUTIVE DASHBOARD")
        print(f"{'='*50}")
        print(f"Period: {result['period']}")
        print(f"Metrics: {result['metrics_count']}")
        print(f"\nOutputs:")
        print(f"  Excel: {result['excel']}")
        print(f"  PowerPoint: {result['powerpoint']}")
        print(f"{'='*50}\n")

        return 0

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
