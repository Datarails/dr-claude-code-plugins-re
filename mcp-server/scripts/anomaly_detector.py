#!/usr/bin/env python3
"""
Datarails Anomaly Detection Agent

Detects data quality issues in Finance OS tables and generates comprehensive Excel report.
Automatically adapts to client-specific table structures and field names.

Usage:
    uv --directory mcp-server run python scripts/anomaly_detector.py --env app
    uv --directory mcp-server run python scripts/anomaly_detector.py --env app --table-id 16528
    uv --directory mcp-server run python scripts/anomaly_detector.py --env app --severity critical
    uv --directory mcp-server run python scripts/anomaly_detector.py --env app --output tmp/custom_report.xlsx
"""

import argparse
import json
import sys
import asyncio
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add mcp-server/src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from datarails_mcp.auth import get_auth
from datarails_mcp.client import DatarailsClient
from datarails_mcp.report_utils import (
    summarize_anomalies,
    format_currency,
    get_severity_color,
    safe_divide,
    export_json,
)
from datarails_mcp.excel_builder import ExcelReport


# Default profile (falls back to this structure if profile doesn't exist)
DEFAULT_PROFILE = {
    "tables": {
        "financials": {
            "id": "16528",
            "name": "Financials Cube",
        }
    },
    "field_mappings": {
        "amount": "Amount",
        "date": "Reporting Date",
        "account": "DR_ACC_L1",
    },
}


def load_profile(env: str) -> dict:
    """Load client profile for environment.

    Args:
        env: Environment name (app, dev, demo, testapp)

    Returns:
        Profile dictionary
    """
    profile_path = Path(__file__).parent.parent.parent / "config" / "client-profiles" / f"{env}.json"

    if profile_path.exists():
        try:
            with open(profile_path) as f:
                profile = json.load(f)
            print(f"✓ Loaded profile: {env}")
            return profile
        except Exception as e:
            print(f"⚠ Error loading profile {env}: {e}")
            print("  Using default profile structure")
            return DEFAULT_PROFILE
    else:
        print(f"ℹ No profile found for '{env}', using default structure")
        return DEFAULT_PROFILE


async def discover_financials_table(client: DatarailsClient, profile: dict) -> str:
    """Discover financials table if not specified in profile.

    Args:
        client: DatarailsClient instance
        profile: Client profile

    Returns:
        Table ID
    """
    # Check if table ID is in profile
    table_id = profile.get("tables", {}).get("financials", {}).get("id")
    if table_id:
        return table_id

    # Discover from API
    print("🔍 Discovering financials table...")
    tables = await client.list_finance_tables()

    if not tables:
        raise Exception("No tables found. Authentication may have failed.")

    # Use first table (typically the financials table)
    table_id = tables[0]["id"]
    print(f"✓ Found financials table: {table_id}")

    return table_id


async def run_anomaly_detection(
    env: str,
    table_id: str = None,
    severity_filter: str = None,
    output_file: str = None,
) -> dict:
    """Run anomaly detection on a Finance OS table.

    Args:
        env: Environment (app, dev, demo, testapp)
        table_id: Optional table ID override
        severity_filter: Optional severity filter (critical, high, medium, low)
        output_file: Optional output file path

    Returns:
        Dictionary with results and file path
    """
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

    # Create client
    client = DatarailsClient(auth)

    try:
        # Determine table ID
        if not table_id:
            table_id = await discover_financials_table(client, profile)

        print(f"\n📊 Analyzing table {table_id}...")

        # Run anomaly detection
        print("  🔬 Running anomaly detection...")
        anomalies = await client.detect_anomalies(table_id)

        # Profile numeric and categorical fields
        print("  📈 Profiling numeric fields...")
        numeric_profile = await client.profile_numeric_fields(table_id)

        print("  📝 Profiling categorical fields...")
        categorical_profile = await client.profile_categorical_fields(table_id)

        # Get table schema
        print("  📋 Retrieving schema...")
        schema = await client.get_table_schema(table_id)

        # Fetch sample records for top anomalies
        print("  🔍 Fetching sample records...")
        samples = {}
        if anomalies:
            # Get up to 3 samples from top anomalies
            for idx, anomaly in enumerate(anomalies[:5]):
                try:
                    # Try to fetch samples for this anomaly type
                    if "field" in anomaly:
                        field = anomaly["field"]
                        sample_data = await client.get_records_by_filter(
                            table_id=table_id,
                            filters={},
                            limit=5
                        )
                        if sample_data:
                            samples[field] = sample_data
                except Exception as e:
                    pass  # Continue if sample retrieval fails

        # Summarize results
        print("  📊 Summarizing results...")
        summary = summarize_anomalies(anomalies)

        # Filter by severity if requested
        filtered_anomalies = anomalies
        if severity_filter:
            filtered_anomalies = [
                a for a in anomalies
                if a.get("severity", "").lower() == severity_filter.lower()
            ]

        # Generate Excel report
        print("  📄 Generating Excel report...")
        output_path = generate_excel_report(
            profile=profile,
            table_id=table_id,
            anomalies=filtered_anomalies,
            summary=summary,
            numeric_profile=numeric_profile,
            categorical_profile=categorical_profile,
            samples=samples,
            output_file=output_file
        )

        print(f"\n✅ Report generated: {output_path}")

        # Return results
        return {
            "success": True,
            "table_id": table_id,
            "total_anomalies": summary["total"],
            "by_severity": summary["by_severity"],
            "data_quality_score": summary["data_quality_score"],
            "output_file": output_path,
            "summary": summary,
        }

    finally:
        await client.close()


def generate_excel_report(
    profile: dict,
    table_id: str,
    anomalies: list,
    summary: dict,
    numeric_profile: dict,
    categorical_profile: dict,
    samples: dict,
    output_file: str = None,
) -> str:
    """Generate Excel report with anomaly findings.

    Args:
        profile: Client profile
        table_id: Table ID
        anomalies: List of anomalies
        summary: Summary statistics
        numeric_profile: Numeric field profiles
        categorical_profile: Categorical field profiles
        samples: Sample records
        output_file: Optional output file path

    Returns:
        Output file path
    """
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Anomaly_Report_{timestamp}.xlsx")

    # Create Excel report
    report = ExcelReport(title="Anomaly Detection Report")

    # ===== SUMMARY SHEET =====
    report.ws.title = "Summary"
    report.add_title("Data Quality Assessment")

    # Add metadata
    metadata_row = 3
    metadata = [
        ("Table ID", table_id),
        ("Analyzed", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ("Total Anomalies", str(summary["total"])),
    ]

    for label, value in metadata:
        cell = report.ws[f"A{metadata_row}"]
        cell.value = label
        cell.font = report.styles["metric_label"]

        cell = report.ws[f"B{metadata_row}"]
        cell.value = value
        cell.font = report.styles["metric_value"]

        metadata_row += 1

    # Add data quality score
    score = summary["data_quality_score"]
    score_display = f"{score:.0f}/100"
    score_status = summary["health_status"]

    score_row = metadata_row + 1
    report.ws.merge_cells(f"A{score_row}:B{score_row}")
    cell = report.ws[f"A{score_row}"]
    cell.value = "Data Quality Score"
    cell.font = report.styles["metric_label"]

    score_row += 1
    report.ws.merge_cells(f"A{score_row}:B{score_row}")
    cell = report.ws[f"A{score_row}"]
    cell.value = score_display
    cell.font = report.styles["metric_value"]

    score_row += 1
    report.ws.merge_cells(f"A{score_row}:B{score_row}")
    cell = report.ws[f"A{score_row}"]
    cell.value = score_status
    cell.font = report.styles["metric_value"]

    # Add severity summary
    report.add_severity_summary(summary["by_severity"])

    # ===== CRITICAL SHEET =====
    if summary["by_severity"]["critical"] > 0:
        critical_anomalies = [a for a in anomalies if a.get("severity") == "critical"]
        report.add_sheet("Critical")
        report.add_title("Critical Findings - Immediate Action Required")

        critical_data = []
        for anomaly in critical_anomalies[:20]:  # Limit to 20 rows
            critical_data.append({
                "Finding": anomaly.get("type", "Unknown"),
                "Field": anomaly.get("field", "—"),
                "Details": anomaly.get("description", ""),
                "Count": str(anomaly.get("count", 1)),
            })

        if critical_data:
            report.add_data_table(critical_data, start_row=3)

    # ===== HIGH PRIORITY SHEET =====
    if summary["by_severity"]["high"] > 0:
        high_anomalies = [a for a in anomalies if a.get("severity") == "high"]
        report.add_sheet("High Priority")
        report.add_title("High Priority Findings")

        high_data = []
        for anomaly in high_anomalies[:20]:
            high_data.append({
                "Finding": anomaly.get("type", "Unknown"),
                "Field": anomaly.get("field", "—"),
                "Details": anomaly.get("description", ""),
                "Count": str(anomaly.get("count", 1)),
            })

        if high_data:
            report.add_data_table(high_data, start_row=3)

    # ===== NUMERIC PROFILE SHEET =====
    if numeric_profile:
        report.add_sheet("Numeric Analysis")
        report.add_title("Numeric Field Statistics")

        numeric_data = []
        for field_name, stats in numeric_profile.items():
            if isinstance(stats, dict):
                numeric_data.append({
                    "Field": field_name,
                    "Min": format_currency(stats.get("min", 0)),
                    "Max": format_currency(stats.get("max", 0)),
                    "Mean": format_currency(stats.get("mean", 0)),
                    "Std Dev": format_currency(stats.get("std_dev", 0)),
                    "Null %": f"{stats.get('null_pct', 0):.1f}%",
                })

        if numeric_data:
            report.add_data_table(numeric_data, start_row=3)

    # ===== CATEGORICAL PROFILE SHEET =====
    if categorical_profile:
        report.add_sheet("Categorical Analysis")
        report.add_title("Categorical Field Analysis")

        categorical_data = []
        for field_name, stats in categorical_profile.items():
            if isinstance(stats, dict):
                categorical_data.append({
                    "Field": field_name,
                    "Distinct Values": str(stats.get("distinct_count", 0)),
                    "Top Value": stats.get("top_value", "—"),
                    "Top Value %": f"{stats.get('top_value_pct', 0):.1f}%",
                    "Null %": f"{stats.get('null_pct', 0):.1f}%",
                })

        if categorical_data:
            report.add_data_table(categorical_data, start_row=3)

    # ===== SAMPLES SHEET =====
    if samples:
        report.add_sheet("Samples")
        report.add_title("Sample Records for Investigation")

        row = 3
        for field_name, sample_records in samples.items():
            report.ws.merge_cells(f"A{row}:H{row}")
            cell = report.ws[f"A{row}"]
            cell.value = f"Samples from field: {field_name}"
            cell.font = report.styles["subheader"]
            cell.fill = report.styles["subheader_fill"]
            row += 1

            if sample_records and len(sample_records) > 0:
                # Convert records to list of dicts if needed
                if isinstance(sample_records, list) and len(sample_records) > 0:
                    report.add_data_table(sample_records, start_row=row)
                    row += len(sample_records) + 3

    # Add footer
    report.add_footer(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Save report
    report.save(output_file)

    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Detect data quality anomalies in Datarails Finance OS tables"
    )
    parser.add_argument(
        "--env",
        default="app",
        choices=["app", "dev", "demo", "testapp"],
        help="Environment (default: app)"
    )
    parser.add_argument(
        "--table-id",
        default=None,
        help="Table ID (optional, uses profile if not specified)"
    )
    parser.add_argument(
        "--severity",
        default=None,
        choices=["critical", "high", "medium", "low"],
        help="Filter results by severity"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path (default: tmp/Anomaly_Report_TIMESTAMP.xlsx)"
    )

    args = parser.parse_args()

    try:
        # Run detection
        result = asyncio.run(
            run_anomaly_detection(
                env=args.env,
                table_id=args.table_id,
                severity_filter=args.severity,
                output_file=args.output,
            )
        )

        # Print results
        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            print(f"   {result.get('message', '')}")
            if "action" in result:
                print(f"   Action: {result['action']}")
            return 1

        print(f"\n{'='*50}")
        print(f"ANOMALY DETECTION SUMMARY")
        print(f"{'='*50}")
        print(f"Table: {result['table_id']}")
        print(f"Total Anomalies: {result['total_anomalies']}")
        print(f"Data Quality Score: {result['data_quality_score']:.0f}/100")
        print(f"\nBy Severity:")
        for severity, count in result["by_severity"].items():
            print(f"  {severity.capitalize()}: {count}")
        print(f"\nReport: {result['output_file']}")
        print(f"{'='*50}\n")

        return 0

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
