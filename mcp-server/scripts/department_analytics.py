#!/usr/bin/env python3
"""
Datarails Department Analytics

Analyzes P&L and performance metrics by department.
Creates departmental reports and comparative analysis.

Usage:
    uv --directory mcp-server run python scripts/department_analytics.py --year 2025
    uv --directory mcp-server run python scripts/department_analytics.py --year 2025 --department Engineering
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
from datarails_mcp.report_utils import format_currency, format_percentage
from datarails_mcp.excel_builder import ExcelReport
from datarails_mcp.pptx_builder import PowerPointReport


# Default profile
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
        "account_l1": "DR_ACC_L1",
        "department": "Department",
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


async def analyze_departments(
    env: str,
    year: int,
    department: str = None,
    output_xlsx: str = None,
    output_pptx: str = None,
) -> dict:
    """Analyze department P&L and performance."""
    if not year:
        year = datetime.now().year

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
        print(f"\n📊 Analyzing departments for {year}...")

        # Fetch department data
        print("  📋 Fetching department P&L...")
        dept_data = await fetch_department_data(client, profile, year)

        # Generate outputs
        print("  📄 Generating Excel report...")
        xlsx_path = generate_department_excel(
            dept_data=dept_data,
            year=year,
            output_file=output_xlsx
        )

        print("  📊 Generating PowerPoint review...")
        pptx_path = generate_department_pptx(
            dept_data=dept_data,
            year=year,
            output_file=output_pptx
        )

        print(f"\n✅ Department analysis complete")

        return {
            "success": True,
            "year": year,
            "departments": len(dept_data),
            "excel": xlsx_path,
            "powerpoint": pptx_path,
        }

    finally:
        await client.close()


async def fetch_department_data(client: DatarailsClient, profile: dict, year: int) -> dict:
    """Fetch P&L data by department."""
    table_id = profile.get("tables", {}).get("financials", {}).get("id", "16528")
    amount_field = profile.get("field_mappings", {}).get("amount", "Amount")
    dept_field = profile.get("field_mappings", {}).get("department", "Department")
    account_field = profile.get("field_mappings", {}).get("account_l1", "DR_ACC_L1")

    try:
        # Fetch data by department and account
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[dept_field, account_field],
            metrics=[{"field": amount_field, "agg": "SUM"}]
        )

        dept_summary = defaultdict(lambda: defaultdict(float))

        if data and isinstance(data, list):
            for row in data:
                dept = row.get(dept_field, "Unknown")
                account = row.get(account_field, "Unknown")
                amount = float(row.get(amount_field, 0))
                dept_summary[dept][account] += amount

        return dict(dept_summary)

    except Exception as e:
        print(f"    ⚠ Error fetching department data: {e}")
        return {}


def generate_department_excel(
    dept_data: dict,
    year: int,
    output_file: str = None,
) -> str:
    """Generate Excel department analysis."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Department_Analysis_{year}_{timestamp}.xlsx")

    report = ExcelReport(title="Department Analysis")

    # Summary sheet
    report.add_title(f"Department P&L Analysis - {year}")

    # Add department summary
    summary_data = []
    for dept_name, accounts in dept_data.items():
        total = sum(accounts.values())
        revenue = accounts.get("REVENUE", 0)
        expenses = sum([v for k, v in accounts.items() if "Expense" in k or "COGS" in k])

        summary_data.append({
            "Department": dept_name,
            "Revenue": format_currency(revenue),
            "Expenses": format_currency(abs(expenses)),
            "Total": format_currency(total),
        })

    if summary_data:
        report.add_data_table(summary_data, start_row=3)

    # Per-department sheets
    for dept_name, accounts in dept_data.items():
        report.add_sheet(dept_name[:31])  # Excel sheet name limit
        report.add_title(f"{dept_name} P&L - {year}")

        dept_data_detail = []
        for account, amount in accounts.items():
            dept_data_detail.append({
                "Account": account,
                "Amount": format_currency(amount),
            })

        if dept_data_detail:
            report.add_data_table(dept_data_detail, start_row=3)

    report.save(output_file)
    return output_file


def generate_department_pptx(
    dept_data: dict,
    year: int,
    output_file: str = None,
) -> str:
    """Generate PowerPoint department review."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Department_Review_{year}_{timestamp}.pptx")

    report = PowerPointReport(title=f"Department Analysis - {year}")

    # Create slide for each department
    for dept_name, accounts in list(dept_data.items())[:6]:  # First 6 departments
        slide = report.add_slide(f"{dept_name}")

        # Department metrics
        total = sum(accounts.values())
        revenue = accounts.get("REVENUE", 0)
        expenses = sum([v for k, v in accounts.items() if "Expense" in k or "COGS" in k])

        metrics = {
            "Revenue": format_currency(revenue),
            "Expenses": format_currency(abs(expenses)),
            "Total": format_currency(total),
        }

        if metrics:
            report.add_metrics_boxes(slide, metrics, columns=3)

    report.save(output_file)
    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze P&L by department"
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
        required=True,
        help="Calendar year"
    )
    parser.add_argument(
        "--department",
        default=None,
        help="Specific department (optional)"
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
            analyze_departments(
                env=args.env,
                year=args.year,
                department=args.department,
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
        print(f"DEPARTMENT ANALYSIS")
        print(f"{'='*50}")
        print(f"Year: {result['year']}")
        print(f"Departments: {result['departments']}")
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
