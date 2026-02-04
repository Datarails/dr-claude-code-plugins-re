#!/usr/bin/env python3
"""Generate live financial reports from real Datarails data."""

import asyncio
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datarails_mcp.auth import get_auth
from datarails_mcp.client import DatarailsClient
from datarails_mcp.excel_builder import ExcelReport
from datarails_mcp.report_utils import format_currency


async def generate_anomaly_report():
    """Generate anomaly detection report from real data."""
    print("\n🔴 GENERATING ANOMALY DETECTION REPORT")
    print("=" * 60)

    auth = get_auth()
    client = DatarailsClient(auth)

    # Load profile
    profile_path = Path(__file__).parent.parent.parent / "config" / "client-profiles" / "app.json"
    with open(profile_path) as f:
        profile = json.load(f)

    table_id = profile["tables"]["financials"]["id"]
    print(f"✓ Using table: {table_id}")

    # Get anomalies
    print("🔍 Detecting anomalies...")
    anomalies_str = await client.detect_anomalies(table_id)
    anomalies = json.loads(anomalies_str)

    print(f"✓ Found {len(anomalies.get('findings', []))} findings")

    # Create Excel report
    print("📊 Generating Excel report...")
    excel = ExcelReport()

    # Summary sheet
    findings = anomalies.get("findings", [])
    critical = [f for f in findings if f.get("severity") == "critical"]
    high = [f for f in findings if f.get("severity") == "high"]
    medium = [f for f in findings if f.get("severity") == "medium"]
    low = [f for f in findings if f.get("severity") == "low"]

    score = anomalies.get("quality_score", 0)

    excel.add_sheet("Summary")
    excel.add_heading("Data Quality Report")
    excel.add_data([
        ["Data Quality Score", f"{score}/100"],
        ["Total Findings", len(findings)],
        ["Critical", len(critical)],
        ["High", len(high)],
        ["Medium", len(medium)],
        ["Low", len(low)],
    ])

    # Critical findings
    if critical:
        excel.add_sheet("Critical")
        excel.add_heading("Critical Findings")
        for finding in critical:
            excel.add_data([
                ["Issue", finding.get("issue_type")],
                ["Description", finding.get("description")],
                ["Records Affected", finding.get("record_count", 0)],
                [""]
            ])

    # High findings
    if high:
        excel.add_sheet("High Priority")
        excel.add_heading("High Priority Findings")
        for finding in high[:5]:  # First 5
            excel.add_data([
                ["Issue", finding.get("issue_type")],
                ["Description", finding.get("description")],
            ])

    # Save
    output_path = Path(__file__).parent.parent.parent / "tmp" / "Anomaly_Report_Live.xlsx"
    excel.save(str(output_path))
    print(f"✅ Report saved: {output_path}")

    return str(output_path)


async def generate_dashboard_data():
    """Generate dashboard data from real KPIs."""
    print("\n📈 GENERATING EXECUTIVE DASHBOARD")
    print("=" * 60)

    auth = get_auth()
    client = DatarailsClient(auth)

    # Load profile
    profile_path = Path(__file__).parent.parent.parent / "config" / "client-profiles" / "app.json"
    with open(profile_path) as f:
        profile = json.load(f)

    kpi_table_id = profile["tables"]["kpis"]["id"]
    print(f"✓ Using KPI table: {kpi_table_id}")

    # Get sample data
    print("📊 Fetching KPI data...")
    sample_str = await client.get_sample(kpi_table_id, n=20)
    sample_data = json.loads(sample_str)

    records = sample_data.get("records", [])
    print(f"✓ Got {len(records)} KPI records")

    # Create Excel dashboard
    print("📊 Generating Excel dashboard...")
    excel = ExcelReport()

    excel.add_sheet("Dashboard")
    excel.add_heading("Executive KPI Dashboard")

    # Add KPI data
    if records:
        excel.add_data([["KPI Name", "Value", "Status"]])
        for i, record in enumerate(records[:10]):
            metric_name = record.get("metric", "Unknown")
            value = record.get("value", 0)
            status = "✓"

            if isinstance(value, (int, float)):
                formatted_value = format_currency(value) if value > 1000 else f"{value:.2f}%"
            else:
                formatted_value = str(value)

            excel.add_data([[metric_name, formatted_value, status]])

    # Save
    output_path = Path(__file__).parent.parent.parent / "tmp" / "Dashboard_Live.xlsx"
    excel.save(str(output_path))
    print(f"✅ Dashboard saved: {output_path}")

    return str(output_path)


async def main():
    """Generate all reports."""
    try:
        print("\n" + "=" * 60)
        print("🚀 GENERATING LIVE REPORTS FROM YOUR DATA")
        print("=" * 60)

        # Generate reports
        anomaly_path = await generate_anomaly_report()
        dashboard_path = await generate_dashboard_data()

        print("\n" + "=" * 60)
        print("✅ ALL REPORTS GENERATED")
        print("=" * 60)
        print(f"\n📄 Reports created in tmp/:")
        print(f"  • {Path(anomaly_path).name}")
        print(f"  • {Path(dashboard_path).name}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
