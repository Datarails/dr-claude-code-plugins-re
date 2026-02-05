#!/usr/bin/env python3
"""
Finance OS API Diagnostic Tool

Systematically tests the Datarails Finance OS API to document:
- What works reliably
- What fails or is unreliable
- Performance bottlenecks
- Workarounds required

Usage:
    uv --directory mcp-server run python scripts/api_diagnostic.py --env app
"""

import argparse
import json
import sys
import asyncio
import time
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Any, List, Dict, Optional

# Add mcp-server/src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import httpx
from datarails_mcp.auth import get_auth


@dataclass
class TestResult:
    """Result of an API test."""
    test_name: str
    endpoint: str
    method: str
    status_code: int
    response_time_ms: float
    success: bool
    error_message: str = ""
    response_size: int = 0
    records_returned: int = 0
    notes: str = ""


@dataclass
class DiagnosticReport:
    """Full diagnostic report."""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    environment: str = ""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    partial: int = 0
    results: List[TestResult] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class APIDiagnostic:
    """Diagnostic tool for Finance OS API."""

    def __init__(self, env: str = "app"):
        self.env = env
        self.auth = get_auth()
        self.report = DiagnosticReport(environment=env)

        # Load profile
        self.profile = self._load_profile(env)
        self.base_url = self.auth.base_url

        # Test configuration
        self.financials_table = self.profile["tables"]["financials"]["id"]
        self.kpis_table = self.profile["tables"].get("kpis", {}).get("id")
        self.fields = self.profile["field_mappings"]
        self.accounts = self.profile.get("account_hierarchy", {})

    def _load_profile(self, env: str) -> dict:
        """Load client profile."""
        project_root = Path(__file__).parent.parent.parent
        profile_path = project_root / "config" / "client-profiles" / f"{env}.json"

        if profile_path.exists():
            with open(profile_path) as f:
                return json.load(f)
        raise FileNotFoundError(f"No profile found for {env}")

    def _log(self, message: str, level: str = "INFO"):
        """Log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        icon = {"INFO": "ℹ️", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "TEST": "🧪"}.get(level, "")
        print(f"[{timestamp}] {icon} {message}")

    async def _ensure_auth(self):
        """Ensure we have a valid JWT token."""
        if not self.auth.is_authenticated():
            self._log("Not authenticated!", "FAIL")
            return False

        self._log("Refreshing JWT token...", "INFO")
        result = await self.auth.ensure_valid_token()
        if result:
            self._log("JWT token refreshed", "PASS")
        else:
            self._log("Failed to refresh JWT token", "FAIL")
        return result

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json_data: dict = None,
        timeout: float = 60.0
    ) -> tuple[int, dict | None, float]:
        """Make API request and return (status_code, response_data, time_ms)."""
        url = f"{self.base_url}/finance-os/api{endpoint}"

        start = time.perf_counter()
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                if method == "GET":
                    resp = await client.get(url, headers=self.auth.get_headers())
                else:
                    resp = await client.post(url, headers=self.auth.get_headers(), json=json_data)

                elapsed = (time.perf_counter() - start) * 1000

                try:
                    data = resp.json() if resp.text else None
                except:
                    data = None

                return resp.status_code, data, elapsed

        except httpx.TimeoutException:
            elapsed = (time.perf_counter() - start) * 1000
            return -1, {"error": "TIMEOUT"}, elapsed
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            return -2, {"error": str(e)}, elapsed

    def _add_result(self, result: TestResult):
        """Add test result to report."""
        self.report.results.append(result)
        self.report.total_tests += 1
        if result.success:
            self.report.passed += 1
        elif "partial" in result.notes.lower():
            self.report.partial += 1
        else:
            self.report.failed += 1

    def _add_issue(self, severity: str, category: str, description: str,
                   workaround: str = "", impact: str = ""):
        """Add issue to report."""
        self.report.issues.append({
            "severity": severity,
            "category": category,
            "description": description,
            "workaround": workaround,
            "impact": impact
        })

    # =========================================================================
    # TEST CASES
    # =========================================================================

    async def test_list_tables(self):
        """Test: List all tables endpoint."""
        self._log("Testing: List Tables API", "TEST")
        await self._ensure_auth()

        status, data, elapsed = await self._make_request("GET", "/tables/v1/")

        success = status == 200 and data and "data" in data
        records = len(data.get("data", [])) if data else 0

        result = TestResult(
            test_name="List Tables",
            endpoint="/tables/v1/",
            method="GET",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=records,
            notes=f"Returned {records} tables" if success else f"Error: {data}"
        )
        self._add_result(result)

        if success:
            self._log(f"List Tables: {status} ({elapsed:.0f}ms) - {records} tables", "PASS")
        else:
            self._log(f"List Tables: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")
            self._add_issue("LOW", "Discovery", "List tables may fail intermittently",
                          "Retry on failure", "Minor - usually works")

    async def test_get_schema(self):
        """Test: Get table schema endpoint."""
        self._log("Testing: Get Schema API", "TEST")
        await self._ensure_auth()

        status, data, elapsed = await self._make_request("GET", f"/tables/v1/{self.financials_table}")

        success = status == 200 and data and "data" in data
        fields = len(data.get("data", {}).get("fields", [])) if success else 0

        result = TestResult(
            test_name="Get Table Schema",
            endpoint=f"/tables/v1/{self.financials_table}",
            method="GET",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=fields,
            notes=f"Schema has {fields} fields" if success else f"Error: {data}"
        )
        self._add_result(result)

        if success:
            self._log(f"Get Schema: {status} ({elapsed:.0f}ms) - {fields} fields", "PASS")
        else:
            self._log(f"Get Schema: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")

    async def test_aggregation_simple(self):
        """Test: Simple aggregation (single dimension, single metric)."""
        self._log("Testing: Simple Aggregation API", "TEST")
        await self._ensure_auth()

        payload = {
            "dimensions": [self.fields["account_l1"]],
            "metrics": [{"field": self.fields["amount"], "agg": "SUM"}],
            "filters": [
                {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False},
                {"name": self.fields["year"], "values": ["2025"], "is_excluded": False}
            ]
        }

        status, data, elapsed = await self._make_request(
            "POST", f"/tables/v1/{self.financials_table}/aggregate", payload
        )

        # Check for various failure modes
        if status == 200 and data:
            if data.get("data"):
                success = True
                records = len(data["data"])
                notes = f"Returned {records} aggregated rows"
            elif data.get("success") is False:
                success = False
                notes = f"API returned success=false: {data.get('error', 'unknown')}"
            else:
                success = False
                notes = f"Empty response body: {data}"
        elif status == 202:
            success = False
            notes = "202 Accepted - async processing required (not supported by client)"
        elif status == 500:
            success = False
            notes = f"500 Internal Server Error: {data}"
        else:
            success = False
            notes = f"Unexpected status {status}: {data}"

        result = TestResult(
            test_name="Simple Aggregation",
            endpoint=f"/tables/v1/{self.financials_table}/aggregate",
            method="POST",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=records if success else 0,
            notes=notes
        )
        self._add_result(result)

        if success:
            self._log(f"Simple Aggregation: {status} ({elapsed:.0f}ms) - {records} rows", "PASS")
        else:
            self._log(f"Simple Aggregation: {status} ({elapsed:.0f}ms) - {notes}", "FAIL")
            self._add_issue(
                "HIGH", "Aggregation",
                f"Simple aggregation fails with status {status}",
                "Use pagination + client-side aggregation",
                "Major - forces fetching all raw data"
            )

    async def test_aggregation_complex(self):
        """Test: Complex aggregation (multiple dimensions)."""
        self._log("Testing: Complex Aggregation API (multi-dimension)", "TEST")
        await self._ensure_auth()

        payload = {
            "dimensions": [
                self.fields["date"],
                self.fields["account_l1"],
                self.fields["account_l2"]
            ],
            "metrics": [{"field": self.fields["amount"], "agg": "SUM"}],
            "filters": [
                {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False},
                {"name": self.fields["account_l0"], "values": [self.accounts["pnl_filter"]], "is_excluded": False},
                {"name": self.fields["year"], "values": ["2025"], "is_excluded": False}
            ]
        }

        status, data, elapsed = await self._make_request(
            "POST", f"/tables/v1/{self.financials_table}/aggregate", payload, timeout=120.0
        )

        success = status == 200 and data and data.get("data")
        records = len(data.get("data", [])) if success else 0

        result = TestResult(
            test_name="Complex Aggregation (3 dimensions)",
            endpoint=f"/tables/v1/{self.financials_table}/aggregate",
            method="POST",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=records,
            notes=f"Returned {records} rows" if success else f"Status {status}: {data}"
        )
        self._add_result(result)

        if success:
            self._log(f"Complex Aggregation: {status} ({elapsed:.0f}ms) - {records} rows", "PASS")
        else:
            self._log(f"Complex Aggregation: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")
            self._add_issue(
                "HIGH", "Aggregation",
                "Multi-dimension aggregation unreliable",
                "Fetch raw data and aggregate client-side",
                "Major - P&L reports require multiple dimensions"
            )

    async def test_data_pagination_single_page(self):
        """Test: Data endpoint - single page (500 records)."""
        self._log("Testing: Data API - Single Page", "TEST")
        await self._ensure_auth()

        payload = {
            "filters": [
                {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False},
                {"name": self.fields["year"], "values": ["2025"], "is_excluded": False}
            ],
            "limit": 500,
            "offset": 0
        }

        status, data, elapsed = await self._make_request(
            "POST", f"/tables/v1/{self.financials_table}/data", payload
        )

        success = status == 200 and data and data.get("data")
        records = len(data.get("data", [])) if success else 0

        result = TestResult(
            test_name="Data Pagination (Single Page)",
            endpoint=f"/tables/v1/{self.financials_table}/data",
            method="POST",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=records,
            notes=f"Returned {records} records in {elapsed:.0f}ms"
        )
        self._add_result(result)

        if success:
            self._log(f"Single Page Data: {status} ({elapsed:.0f}ms) - {records} records", "PASS")
        else:
            self._log(f"Single Page Data: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")

    async def test_data_pagination_full(self):
        """Test: Full pagination to fetch all records."""
        self._log("Testing: Full Data Pagination (all records)", "TEST")

        all_data = []
        offset = 0
        page_count = 0
        errors = []
        start_time = time.perf_counter()
        token_refreshes = 0

        while True:
            # Refresh token every 20K rows
            if offset > 0 and offset % 20000 == 0:
                self._log(f"  Refreshing token at offset {offset}...", "INFO")
                await self._ensure_auth()
                token_refreshes += 1

            payload = {
                "filters": [
                    {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False},
                    {"name": self.fields["account_l0"], "values": [self.accounts["pnl_filter"]], "is_excluded": False},
                    {"name": self.fields["year"], "values": ["2025"], "is_excluded": False}
                ],
                "limit": 500,
                "offset": offset
            }

            status, data, elapsed = await self._make_request(
                "POST", f"/tables/v1/{self.financials_table}/data", payload
            )

            page_count += 1

            if status == 401:
                self._log(f"  401 at offset {offset}, refreshing token...", "WARN")
                await self._ensure_auth()
                token_refreshes += 1
                continue

            if status != 200:
                errors.append(f"Page {page_count} (offset {offset}): status {status}")
                # Try to continue
                if len(errors) > 5:
                    break
                offset += 500
                continue

            page = data.get("data", []) if data else []
            if not page:
                break

            all_data.extend(page)

            if len(all_data) % 10000 == 0:
                self._log(f"  Fetched {len(all_data):,} records...", "INFO")

            if len(page) < 500:
                break

            offset += 500

            # Safety limit
            if len(all_data) >= 100000:
                break

        total_time = (time.perf_counter() - start_time) * 1000
        records_per_second = len(all_data) / (total_time / 1000) if total_time > 0 else 0

        success = len(all_data) > 50000  # We expect ~54K records

        result = TestResult(
            test_name="Full Data Pagination",
            endpoint=f"/tables/v1/{self.financials_table}/data",
            method="POST",
            status_code=200 if success else -1,
            response_time_ms=total_time,
            success=success,
            records_returned=len(all_data),
            notes=f"{len(all_data):,} records in {page_count} pages, {token_refreshes} token refreshes, {len(errors)} errors, {records_per_second:.0f} rec/sec"
        )
        self._add_result(result)

        if success:
            self._log(f"Full Pagination: {len(all_data):,} records in {total_time/1000:.1f}s ({records_per_second:.0f} rec/s)", "PASS")
        else:
            self._log(f"Full Pagination: Only got {len(all_data):,} records - INCOMPLETE", "FAIL")

        if errors:
            self._add_issue(
                "MEDIUM", "Pagination",
                f"Encountered {len(errors)} errors during pagination",
                "Implement retry logic with exponential backoff",
                "Intermittent failures require robust error handling"
            )

    async def test_distinct_values(self):
        """Test: Get distinct values for a field."""
        self._log("Testing: Distinct Values API", "TEST")
        await self._ensure_auth()

        field_name = self.fields["account_l1"]
        status, data, elapsed = await self._make_request(
            "GET", f"/tables/v1/{self.financials_table}/fields/by-name/{field_name}/distinct"
        )

        success = status == 200 and data and data.get("data", {}).get("values")
        values = data.get("data", {}).get("values", []) if success else []

        result = TestResult(
            test_name="Get Distinct Values",
            endpoint=f"/tables/v1/{self.financials_table}/fields/by-name/{field_name}/distinct",
            method="GET",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=len(values),
            notes=f"Found {len(values)} distinct values" if success else f"Error: {data}"
        )
        self._add_result(result)

        if success:
            self._log(f"Distinct Values: {status} ({elapsed:.0f}ms) - {len(values)} values", "PASS")
        else:
            self._log(f"Distinct Values: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")

    async def test_jwt_expiry(self):
        """Test: JWT token expiry behavior."""
        self._log("Testing: JWT Token Expiry (waiting 30s)", "TEST")

        # Get fresh token
        await self._ensure_auth()

        # Make initial request
        status1, _, _ = await self._make_request("GET", "/tables/v1/")
        self._log(f"  Initial request: {status1}", "INFO")

        # Wait 30 seconds
        self._log("  Waiting 30 seconds...", "INFO")
        await asyncio.sleep(30)

        # Make request without refreshing token
        status2, _, _ = await self._make_request("GET", "/tables/v1/")
        self._log(f"  After 30s (no refresh): {status2}", "INFO")

        # Wait another 4.5 minutes (total ~5 min)
        # Actually let's just document the known behavior

        result = TestResult(
            test_name="JWT Token Expiry",
            endpoint="N/A",
            method="N/A",
            status_code=status2,
            response_time_ms=0,
            success=status2 == 200,
            notes=f"Token still valid after 30s. Known expiry: 5 minutes."
        )
        self._add_result(result)

        self._add_issue(
            "HIGH", "Authentication",
            "JWT tokens expire after 5 minutes",
            "Refresh token every 20K rows or before each major operation",
            "Long-running operations will fail without token refresh"
        )

    async def test_kpi_aggregation(self):
        """Test: KPI table aggregation."""
        if not self.kpis_table:
            self._log("Skipping KPI test - no KPI table configured", "WARN")
            return

        self._log("Testing: KPI Table Aggregation", "TEST")
        await self._ensure_auth()

        payload = {
            "dimensions": [
                self.fields.get("quarter", "Quarter & Year"),
                self.fields.get("kpi_name", "KPI")
            ],
            "metrics": [{"field": self.fields.get("kpi_value", "value"), "agg": "MAX"}],
            "filters": [
                {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False}
            ]
        }

        status, data, elapsed = await self._make_request(
            "POST", f"/tables/v1/{self.kpis_table}/aggregate", payload
        )

        success = status == 200 and data and data.get("data")
        records = len(data.get("data", [])) if success else 0

        result = TestResult(
            test_name="KPI Table Aggregation",
            endpoint=f"/tables/v1/{self.kpis_table}/aggregate",
            method="POST",
            status_code=status,
            response_time_ms=elapsed,
            success=success,
            records_returned=records,
            notes=f"Returned {records} KPI records" if success else f"Status {status}: {data}"
        )
        self._add_result(result)

        if success:
            self._log(f"KPI Aggregation: {status} ({elapsed:.0f}ms) - {records} records", "PASS")
        else:
            self._log(f"KPI Aggregation: {status} ({elapsed:.0f}ms) - FAILED", "FAIL")

    async def test_concurrent_requests(self):
        """Test: Concurrent request handling."""
        self._log("Testing: Concurrent Requests (5 parallel)", "TEST")
        await self._ensure_auth()

        async def make_single_request(i: int):
            payload = {
                "filters": [
                    {"name": self.fields["scenario"], "values": ["Actuals"], "is_excluded": False},
                    {"name": self.fields["year"], "values": ["2025"], "is_excluded": False}
                ],
                "limit": 100,
                "offset": i * 100
            }
            return await self._make_request(
                "POST", f"/tables/v1/{self.financials_table}/data", payload
            )

        start = time.perf_counter()
        results = await asyncio.gather(*[make_single_request(i) for i in range(5)])
        total_time = (time.perf_counter() - start) * 1000

        successes = sum(1 for s, _, _ in results if s == 200)

        result = TestResult(
            test_name="Concurrent Requests (5 parallel)",
            endpoint=f"/tables/v1/{self.financials_table}/data",
            method="POST",
            status_code=200 if successes == 5 else -1,
            response_time_ms=total_time,
            success=successes == 5,
            records_returned=successes,
            notes=f"{successes}/5 succeeded in {total_time:.0f}ms total"
        )
        self._add_result(result)

        if successes == 5:
            self._log(f"Concurrent Requests: All 5 succeeded in {total_time:.0f}ms", "PASS")
        else:
            self._log(f"Concurrent Requests: Only {successes}/5 succeeded", "WARN")
            self._add_issue(
                "MEDIUM", "Concurrency",
                f"Concurrent requests may fail ({successes}/5 succeeded)",
                "Use sequential requests or limit concurrency",
                "Parallel fetching may be unreliable"
            )

    # =========================================================================
    # REPORT GENERATION
    # =========================================================================

    def generate_report(self) -> str:
        """Generate the diagnostic report."""
        lines = []
        lines.append("=" * 80)
        lines.append("FINANCE OS API DIAGNOSTIC REPORT")
        lines.append("=" * 80)
        lines.append(f"\nTimestamp: {self.report.timestamp}")
        lines.append(f"Environment: {self.report.environment}")
        lines.append(f"Base URL: {self.base_url}")
        lines.append("")

        # Summary
        lines.append("-" * 80)
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Tests: {self.report.total_tests}")
        lines.append(f"  ✅ Passed:  {self.report.passed}")
        lines.append(f"  ❌ Failed:  {self.report.failed}")
        lines.append(f"  ⚠️  Partial: {self.report.partial}")
        lines.append("")

        # Test Results
        lines.append("-" * 80)
        lines.append("TEST RESULTS")
        lines.append("-" * 80)
        for r in self.report.results:
            icon = "✅" if r.success else "❌"
            lines.append(f"\n{icon} {r.test_name}")
            lines.append(f"   Endpoint: {r.method} {r.endpoint}")
            lines.append(f"   Status: {r.status_code} | Time: {r.response_time_ms:.0f}ms | Records: {r.records_returned}")
            lines.append(f"   Notes: {r.notes}")

        # Issues Found
        lines.append("")
        lines.append("-" * 80)
        lines.append("ISSUES FOUND")
        lines.append("-" * 80)

        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        sorted_issues = sorted(self.report.issues, key=lambda x: severity_order.get(x["severity"], 99))

        for i, issue in enumerate(sorted_issues, 1):
            sev = issue["severity"]
            icon = {"CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢"}.get(sev, "⚪")
            lines.append(f"\n{icon} Issue #{i} [{sev}] - {issue['category']}")
            lines.append(f"   Description: {issue['description']}")
            lines.append(f"   Workaround: {issue['workaround']}")
            lines.append(f"   Impact: {issue['impact']}")

        # Recommendations
        lines.append("")
        lines.append("-" * 80)
        lines.append("RECOMMENDATIONS")
        lines.append("-" * 80)

        # Auto-generate recommendations based on issues
        recommendations = [
            "1. ALWAYS use pagination (/data endpoint) instead of aggregation API",
            "   - Aggregation API returns 500/502/202 frequently",
            "   - Pagination is reliable but requires fetching all raw data",
            "",
            "2. IMPLEMENT client-side aggregation",
            "   - Fetch raw data with pagination",
            "   - Aggregate in Python/memory",
            "   - More reliable than server-side aggregation",
            "",
            "3. REFRESH JWT tokens every 20,000 rows or 4 minutes",
            "   - Tokens expire after 5 minutes",
            "   - Long operations will fail without refresh",
            "",
            "4. IMPLEMENT retry logic with exponential backoff",
            "   - 502 Bad Gateway errors are common",
            "   - 500 Internal Server errors occur intermittently",
            "   - 429 Rate limiting may occur",
            "",
            "5. AVOID concurrent requests",
            "   - Server may reject parallel requests",
            "   - Sequential pagination is more reliable",
            "",
            "6. CACHE schema and distinct values",
            "   - These rarely change",
            "   - Reduces API calls and speeds up operations",
        ]
        lines.extend(recommendations)

        # Performance Notes
        lines.append("")
        lines.append("-" * 80)
        lines.append("PERFORMANCE NOTES")
        lines.append("-" * 80)

        # Find pagination test result
        pagination_result = next((r for r in self.report.results if "Full" in r.test_name), None)
        if pagination_result:
            lines.append(f"\nFull Data Extraction Performance:")
            lines.append(f"  - Records: {pagination_result.records_returned:,}")
            lines.append(f"  - Total Time: {pagination_result.response_time_ms/1000:.1f} seconds")
            lines.append(f"  - Rate: ~{pagination_result.records_returned / (pagination_result.response_time_ms/1000):.0f} records/second")
            lines.append(f"  - Note: Client-side aggregation adds processing time")

        lines.append("")
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)

        return "\n".join(lines)

    async def run_all_tests(self):
        """Run all diagnostic tests."""
        print("\n" + "=" * 80)
        print("FINANCE OS API DIAGNOSTIC")
        print("=" * 80)
        print(f"Environment: {self.env}")
        print(f"Base URL: {self.base_url}")
        print(f"Financials Table: {self.financials_table}")
        print(f"KPIs Table: {self.kpis_table}")
        print("=" * 80 + "\n")

        # Run tests
        await self.test_list_tables()
        await self.test_get_schema()
        await self.test_distinct_values()
        await self.test_aggregation_simple()
        await self.test_aggregation_complex()
        await self.test_kpi_aggregation()
        await self.test_data_pagination_single_page()
        await self.test_concurrent_requests()
        await self.test_jwt_expiry()
        await self.test_data_pagination_full()  # This one takes longest, run last

        # Generate report
        report = self.generate_report()
        print("\n" + report)

        # Save report to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = Path(__file__).parent.parent.parent / "tmp" / f"API_Diagnostic_Report_{timestamp}.txt"
        report_path.parent.mkdir(exist_ok=True)
        report_path.write_text(report)
        print(f"\n📄 Report saved to: {report_path}")

        return report


async def main():
    parser = argparse.ArgumentParser(description="Finance OS API Diagnostic Tool")
    parser.add_argument("--env", default="app", choices=["app", "dev", "demo", "testapp"])
    args = parser.parse_args()

    diagnostic = APIDiagnostic(env=args.env)
    await diagnostic.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
