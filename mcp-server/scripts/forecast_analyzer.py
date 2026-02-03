#!/usr/bin/env python3
"""
Datarails Forecast Analyzer

Analyzes variances between Actuals, Budget, and Forecast scenarios.
Identifies trends and provides variance analysis.

Usage:
    uv --directory mcp-server run python scripts/forecast_analyzer.py --year 2025
    uv --directory mcp-server run python scripts/forecast_analyzer.py --year 2025 --env app
    uv --directory mcp-server run python scripts/forecast_analyzer.py --year 2025 --scenarios Actuals,Budget,Forecast
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
)
from datarails_mcp.chart_builder import waterfall_chart
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
        "scenario": "Scenario",
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


async def analyze_forecasts(
    env: str,
    year: int,
    scenarios: list = None,
    period: str = None,
    output_xlsx: str = None,
    output_pptx: str = None,
) -> dict:
    """Analyze forecast vs actual variances."""
    if not year:
        year = datetime.now().year

    if not scenarios:
        scenarios = ["Actuals", "Budget", "Forecast"]

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
        print(f"\n📊 Analyzing forecast variance for {year}...")

        # Fetch data for each scenario
        scenario_data = {}
        for scenario in scenarios:
            print(f"  📋 Fetching {scenario} data...")
            scenario_data[scenario] = await fetch_scenario_data(client, profile, year, scenario)

        # Analyze variances
        print("  ⚖️  Analyzing variances...")
        variance_analysis = analyze_variances(scenario_data, profile)

        # Generate outputs
        print("  📄 Generating Excel report...")
        xlsx_path = generate_variance_report(
            scenario_data=scenario_data,
            variance_analysis=variance_analysis,
            year=year,
            output_file=output_xlsx
        )

        print("  📊 Generating PowerPoint summary...")
        pptx_path = generate_forecast_presentation(
            scenario_data=scenario_data,
            variance_analysis=variance_analysis,
            year=year,
            output_file=output_pptx
        )

        print(f"\n✅ Forecast analysis complete")

        return {
            "success": True,
            "year": year,
            "scenarios_analyzed": len(scenarios),
            "variances_found": len(variance_analysis),
            "excel": xlsx_path,
            "powerpoint": pptx_path,
        }

    finally:
        await client.close()


async def fetch_scenario_data(
    client: DatarailsClient,
    profile: dict,
    year: int,
    scenario: str
) -> dict:
    """Fetch data for a specific scenario."""
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

        scenario_dict = defaultdict(float)

        if data and isinstance(data, list):
            for row in data:
                account = row.get(account_field, "Unknown")
                amount = float(row.get(amount_field, 0))
                scenario_dict[account] += amount

        return dict(scenario_dict)

    except Exception as e:
        print(f"    ⚠ Error fetching {scenario} data: {e}")
        return {}


def analyze_variances(scenario_data: dict, profile: dict) -> dict:
    """Analyze variances between scenarios."""
    variances = {}

    # Get Actuals as baseline
    actuals = scenario_data.get("Actuals", {})
    budget = scenario_data.get("Budget", {})
    forecast = scenario_data.get("Forecast", {})

    account_hierarchy = profile.get("account_hierarchy", {})

    # Analyze each major account
    for account_key, account_name in account_hierarchy.items():
        if account_key.endswith("_filter"):
            continue

        actual_amount = actuals.get(account_name, 0)
        budget_amount = budget.get(account_name, 0)
        forecast_amount = forecast.get(account_name, 0)

        if budget_amount != 0 or actual_amount != 0:
            variance_budget = calculate_variance(actual_amount, budget_amount)
            variance_forecast = calculate_variance(actual_amount, forecast_amount)

            variances[account_name] = {
                "actual": actual_amount,
                "budget": budget_amount,
                "forecast": forecast_amount,
                "variance_budget": variance_budget,
                "variance_forecast": variance_forecast,
            }

    return variances


def generate_variance_report(
    scenario_data: dict,
    variance_analysis: dict,
    year: int,
    output_file: str = None,
) -> str:
    """Generate Excel variance report."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Forecast_Variance_{year}_{timestamp}.xlsx")

    report = ExcelReport(title="Forecast Variance Analysis")

    # Summary sheet
    report.add_title(f"Forecast Variance Analysis - {year}")

    # Add variance data
    variance_data = []
    for account, variances in variance_analysis.items():
        variance_data.append({
            "Account": account,
            "Actual": format_currency(variances["actual"]),
            "Budget": format_currency(variances["budget"]),
            "Forecast": format_currency(variances["forecast"]),
            "Budget Variance": format_percentage(variances["variance_budget"]["percentage"]),
            "Forecast Variance": format_percentage(variances["variance_forecast"]["percentage"]),
        })

    if variance_data:
        report.add_data_table(variance_data, start_row=3)

    # Add scenario totals
    report.add_sheet("Scenario Totals")
    report.add_title("Total by Scenario")

    totals_data = []
    for scenario, data in scenario_data.items():
        total = sum(data.values())
        totals_data.append({
            "Scenario": scenario,
            "Total": format_currency(total),
        })

    if totals_data:
        report.add_data_table(totals_data, start_row=3)

    report.save(output_file)
    return output_file


def generate_forecast_presentation(
    scenario_data: dict,
    variance_analysis: dict,
    year: int,
    output_file: str = None,
) -> str:
    """Generate PowerPoint presentation."""
    if not output_file:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_dir = Path(__file__).parent.parent.parent / "tmp"
        output_dir.mkdir(exist_ok=True)
        output_file = str(output_dir / f"Forecast_Summary_{year}_{timestamp}.pptx")

    report = PowerPointReport(title=f"Forecast Analysis - {year}")

    # Slide: Overview
    slide = report.add_slide("Overview")

    scenario_totals = {}
    for scenario, data in scenario_data.items():
        total = sum(data.values())
        scenario_totals[scenario] = format_currency(total)

    if scenario_totals:
        report.add_metrics_boxes(slide, scenario_totals, columns=3)

    # Slide: Key Variances
    slide = report.add_slide("Variance Summary")

    variance_summary = {}
    for account, variances in list(variance_analysis.items())[:6]:
        budget_var = variances["variance_budget"]["percentage"]
        variance_summary[f"{account} (Budget)"] = format_percentage(budget_var)

    if variance_summary:
        report.add_metrics_boxes(slide, variance_summary, columns=2)

    report.save(output_file)
    return output_file


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze forecast variances"
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
        help="Calendar year to analyze"
    )
    parser.add_argument(
        "--scenarios",
        default="Actuals,Budget,Forecast",
        help="Comma-separated scenarios (default: Actuals,Budget,Forecast)"
    )
    parser.add_argument(
        "--period",
        default=None,
        help="Specific period to analyze"
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

    scenarios = [s.strip() for s in args.scenarios.split(",")]

    try:
        result = asyncio.run(
            analyze_forecasts(
                env=args.env,
                year=args.year,
                scenarios=scenarios,
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
        print(f"FORECAST ANALYSIS")
        print(f"{'='*50}")
        print(f"Year: {result['year']}")
        print(f"Scenarios: {result['scenarios_analyzed']}")
        print(f"Variances Found: {result['variances_found']}")
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
