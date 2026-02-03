#!/usr/bin/env python3
"""
Datarails Reconciliation Engine

Validates consistency between P&L and KPI data sources.
Identifies discrepancies and explains variances.

Usage:
    uv --directory mcp-server run python scripts/reconciliation_engine.py --year 2025
    uv --directory mcp-server run python scripts/reconciliation_engine.py --year 2025 --env app
    uv --directory mcp-server run python scripts/reconciliation_engine.py --year 2025 --tolerance-pct 5
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
    format_currency,
    format_percentage,
    calculate_variance,
    safe_divide,
)
from datarails_mcp.excel_builder import ExcelReport


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


async def reconcile_data(
    env: str,
    year: int,
    scenario: str = "Actuals",
    tolerance_pct: float = 5.0,
    output_file: str = None,
) -> dict:
    """Reconcile P&L vs KPI data."""
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
        print(f"\n📊 Reconciling P&L vs KPI data for {year}...")

        # Fetch P&L data
        print("  📋 Fetching P&L data...")
        pl_data = await fetch_pl_data(client, profile, year, scenario)

        # Fetch KPI data
        print("  📊 Fetching KPI data...")
        kpi_data = await fetch_kpi_data(client, profile, year, scenario)

        # Perform reconciliation
        print("  ⚖️  Performing reconciliation...")
        reconciliation = perform_reconciliation(pl_data, kpi_data, tolerance_pct, profile)

        # Generate Excel report
        print("  📄 Generating Excel report...")
        output_path = generate_reconciliation_report(
            reconciliation=reconciliation,
            pl_data=pl_data,
            kpi_data=kpi_data,
            year=year,
            output_file=output_file
        )

        print(f"\n✅ Reconciliation complete: {output_path}")

        return {
            "success": True,
            "year": year,
            "total_checks": reconciliation["total_checks"],
            "passed": reconciliation["passed"],
            "failed": reconciliation["failed"],
            "exceptions": len(reconciliation["exceptions"]),
            "output_file": output_path,
        }

    finally:
        await client.close()


async def fetch_pl_data(client: DatarailsClient, profile: dict, year: int, scenario: str) -> dict:
    """Fetch P&L data by account and month."""
    table_id = profile.get("tables", {}).get("financials", {}).get("id", "16528")
    amount_field = profile.get("field_mappings", {}).get("amount", "Amount")
    date_field = profile.get("field_mappings", {}).get("date", "Reporting Date")
    account_field = profile.get("field_mappings", {}).get("account_l1", "DR_ACC_L1")
    scenario_field = profile.get("field_mappings", {}).get("scenario", "Scenario")

    try:
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[date_field, account_field],
            metrics=[{"field": amount_field, "agg": "SUM"}],
            filters=[
                {"name": scenario_field, "values": [scenario], "is_excluded": False}
            ]
        )

        pl_by_account = defaultdict(float)
        pl_by_month = defaultdict(lambda: defaultdict(float))

        if data and isinstance(data, list):
            for row in data:
                date = row.get(date_field, "")
                account = row.get(account_field, "Unknown")
                amount = float(row.get(amount_field, 0))

                pl_by_account[account] += amount
                pl_by_month[account][date] = amount

        return {
            "by_account": dict(pl_by_account),
            "by_month": dict(pl_by_month),
        }

    except Exception as e:
        print(f"    ⚠ Error fetching P&L data: {e}")
        return {"by_account": {}, "by_month": {}}


async def fetch_kpi_data(client: DatarailsClient, profile: dict, year: int, scenario: str) -> dict:
    """Fetch KPI data by metric and period."""
    table_id = profile.get("tables", {}).get("kpis", {}).get("id", "34298")
    kpi_name_field = profile.get("field_mappings", {}).get("kpi_name", "KPI")
    kpi_value_field = profile.get("field_mappings", {}).get("kpi_value", "value")
    quarter_field = profile.get("field_mappings", {}).get("quarter", "Quarter & Year")
    scenario_field = profile.get("field_mappings", {}).get("scenario", "Scenario")

    try:
        data = await client.aggregate_table_data(
            table_id=table_id,
            dimensions=[quarter_field, kpi_name_field],
            metrics=[{"field": kpi_value_field, "agg": "MAX"}],
            filters=[
                {"name": scenario_field, "values": [scenario], "is_excluded": False}
            ]
        )

        kpi_by_metric = defaultdict(float)
        kpi_by_quarter = defaultdict(lambda: defaultdict(float))

        if data and isinstance(data, list):
            for row in data:
                quarter = row.get(quarter_field, "")
                kpi_name = row.get(kpi_name_field, "Unknown")
                value = float(row.get(kpi_value_field, 0))

                kpi_by_metric[kpi_name] = value
                kpi_by_quarter[kpi_name][quarter] = value

        return {
            "by_metric": dict(kpi_by_metric),
            "by_quarter": dict(kpi_by_quarter),
        }

    except Exception as e:
        print(f"    ⚠ Error fetching KPI data: {e}")
        return {"by_metric": {}, "by_quarter": {}}


def perform_reconciliation(pl_data: dict, kpi_data: dict, tolerance_pct: float, profile: dict) -> dict:
    """Perform reconciliation checks."""
    reconciliation = {
        "total_checks": 0,
        "passed": 0,
        "failed": 0,
        "exceptions": [],
        "validation_rules": [],
    }

    # Check 1: Revenue consistency
    reconciliation["total_checks"] += 1
    pl_revenue = pl_data.get("by_account", {}).get(profile.get("account_hierarchy", {}).get("revenue", "REVENUE"), 0)

    if "Revenue" in kpi_data.get("by_metric", {}):
        kpi_revenue = kpi_data["by_metric"]["Revenue"]
        variance = calculate_variance(pl_revenue, kpi_revenue)
        variance_pct = abs(variance["percentage"])

        reconciliation["validation_rules"].append({
            "rule": "Revenue P&L vs KPI",
            "pl_value": pl_revenue,
            "kpi_value": kpi_revenue,
            "variance": variance_pct,
            "tolerance": tolerance_pct,
            "status": "PASS" if variance_pct <= tolerance_pct else "FAIL"
        })

        if variance_pct <= tolerance_pct:
            reconciliation["passed"] += 1
        else:
            reconciliation["failed"] += 1
            reconciliation["exceptions"].append({
                "type": "Revenue Variance",
                "description": f"Revenue variance exceeds tolerance: {variance_pct:.1f}%",
                "pl_amount": pl_revenue,
                "kpi_amount": kpi_revenue,
                "variance_pct": variance_pct,
            })

    # Check 2: Expense consistency
    reconciliation["total_checks"] += 1
    pl_cogs = pl_data.get("by_account", {}).get(profile.get("account_hierarchy", {}).get("cogs", "Cost of Good sold"), 0)
    pl_opex = pl_data.get("by_account", {}).get(profile.get("account_hierarchy", {}).get("opex", "Operating Expense"), 0)
    pl_total_expense = abs(pl_cogs) + abs(pl_opex)

    reconciliation["validation_rules"].append({
        "rule": "Total Expense Completeness",
        "pl_value": pl_total_expense,
        "status": "PASS" if pl_total_expense > 0 else "WARN"
    })

    if pl_total_expense > 0:
        reconciliation["passed"] += 1
    else:
        reconciliation["failed"] += 1

    # Check 3: Data completeness
    reconciliation["total_checks"] += 1
    pl_accounts = len(pl_data.get("by_account", {}))
    kpi_metrics = len(kpi_data.get("by_metric", {}))

    if pl_accounts > 0 and kpi_metrics > 0:
        reconciliation["passed"] += 1
        status = "PASS"
    else:
        reconciliation["failed"] += 1
        status = "FAIL"

    reconciliation["validation_rules"].append({
        "rule": "Data Completeness",
        "pl_accounts": pl_accounts,
        "kpi_metrics": kpi_metrics,
        "status": status
    })

    return reconciliation


def generate_reconciliation_report(
    reconciliation: dict,
    pl_data: dict,
    kpi_data: dict,
    year: int,
    output_file: str = None,
) -> str:
    """Generate Excel reconciliation report."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Reconciliation_{year}_{timestamp}.xlsx")

    report = ExcelReport(title="Reconciliation Report")

    # Summary sheet
    report.add_title(f"P&L vs KPI Reconciliation - {year}")

    # Add summary metrics
    total = reconciliation["total_checks"]
    passed = reconciliation["passed"]
    failed = reconciliation["failed"]
    pass_pct = (passed / total * 100) if total > 0 else 0

    summary_data = [
        {"Metric": "Total Checks", "Value": str(total)},
        {"Metric": "Passed", "Value": str(passed)},
        {"Metric": "Failed", "Value": str(failed)},
        {"Metric": "Pass Rate", "Value": f"{pass_pct:.1f}%"},
    ]

    report.add_data_table(summary_data, start_row=3)

    # Add validation rules
    report.add_sheet("Validation Rules")
    report.add_title("Reconciliation Validation Rules")

    rules_data = []
    for rule in reconciliation.get("validation_rules", []):
        rules_data.append({
            "Rule": rule.get("rule", ""),
            "Status": rule.get("status", ""),
            "Details": json.dumps(rule, default=str),
        })

    if rules_data:
        report.add_data_table(rules_data, start_row=3)

    # Add exceptions sheet
    if reconciliation["exceptions"]:
        report.add_sheet("Exceptions")
        report.add_title("Reconciliation Exceptions")

        exceptions_data = []
        for exc in reconciliation["exceptions"]:
            exceptions_data.append({
                "Type": exc.get("type", ""),
                "Description": exc.get("description", ""),
                "P&L Amount": format_currency(exc.get("pl_amount", 0)),
                "KPI Amount": format_currency(exc.get("kpi_amount", 0)),
                "Variance %": format_percentage(exc.get("variance_pct", 0)),
            })

        if exceptions_data:
            report.add_data_table(exceptions_data, start_row=3)

    # Add P&L summary
    report.add_sheet("P&L Summary")
    report.add_title("P&L Data by Account")

    pl_summary = []
    for account, amount in pl_data.get("by_account", {}).items():
        pl_summary.append({
            "Account": account,
            "Total Amount": format_currency(amount),
        })

    if pl_summary:
        report.add_data_table(pl_summary, start_row=3)

    # Add KPI summary
    report.add_sheet("KPI Summary")
    report.add_title("KPI Data Summary")

    kpi_summary = []
    for metric, value in kpi_data.get("by_metric", {}).items():
        kpi_summary.append({
            "KPI": metric,
            "Value": format_currency(value) if isinstance(value, (int, float)) else str(value),
        })

    if kpi_summary:
        report.add_data_table(kpi_summary, start_row=3)

    report.save(output_file)
    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Reconcile P&L vs KPI data"
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
        help="Calendar year to reconcile"
    )
    parser.add_argument(
        "--scenario",
        default="Actuals",
        help="Scenario to reconcile (default: Actuals)"
    )
    parser.add_argument(
        "--tolerance-pct",
        type=float,
        default=5.0,
        help="Variance tolerance percentage (default: 5.0)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output file path"
    )

    args = parser.parse_args()

    try:
        result = asyncio.run(
            reconcile_data(
                env=args.env,
                year=args.year,
                scenario=args.scenario,
                tolerance_pct=args.tolerance_pct,
                output_file=args.output,
            )
        )

        if result.get("error"):
            print(f"\n❌ Error: {result['error']}")
            print(f"   {result.get('message', '')}")
            if "action" in result:
                print(f"   Action: {result['action']}")
            return 1

        print(f"\n{'='*50}")
        print(f"RECONCILIATION REPORT")
        print(f"{'='*50}")
        print(f"Year: {result['year']}")
        print(f"Checks: {result['total_checks']} total")
        print(f"  Passed: {result['passed']}")
        print(f"  Failed: {result['failed']}")
        if result['exceptions'] > 0:
            print(f"Exceptions: {result['exceptions']} issues found")
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
