"""Datarails Finance OS MCP Server.

Provides Claude Code with tools to interact with Datarails Finance OS API
for data discovery, profiling, anomaly detection, and querying.
"""

import json

from mcp.server.fastmcp import FastMCP

from datarails_mcp.auth import BrowserAuth, get_auth, set_session_cookies, clear_auth
from datarails_mcp.client import DatarailsClient

# Initialize MCP server
mcp = FastMCP("datarails-finance-os")

# Initialize auth and client (lazy, will authenticate on first use)
_client: DatarailsClient | None = None


def get_client() -> DatarailsClient:
    """Get or create the Datarails client."""
    global _client
    if _client is None:
        auth = get_auth()
        _client = DatarailsClient(auth)
    else:
        # Check if credentials changed (e.g., CLI saved new cookies)
        fresh_auth = get_auth()
        if fresh_auth.has_session() and not _client.auth.has_session():
            # Credentials were added externally, recreate client
            _client = DatarailsClient(fresh_auth)
    return _client


def reset_client() -> None:
    """Reset the client (e.g., after setting new auth cookies)."""
    global _client
    _client = None


# =============================================================================
# Authentication Tools
# =============================================================================


@mcp.tool()
async def check_auth_status() -> str:
    """Check if authenticated with Datarails.

    Returns authentication status and login URL if not authenticated.
    Use this before making API calls to ensure valid credentials.

    If not authenticated, returns instructions for browser-based login.
    """
    auth = get_auth()

    if auth.is_authenticated():
        return json.dumps({
            "authenticated": True,
            "message": "Authenticated with Datarails",
            "environment": auth.env if hasattr(auth, 'env') else "unknown",
        })
    else:
        # Return auth-needed response for BrowserAuth
        if isinstance(auth, BrowserAuth):
            return json.dumps(auth.needs_auth_response())
        else:
            return json.dumps({
                "authenticated": False,
                "error": "authentication_required",
                "message": "Set DATARAILS_ACCESS_TOKEN environment variable",
            })


@mcp.tool()
async def set_auth_cookies(
    session_id: str,
    csrf_token: str,
) -> str:
    """Store session cookies extracted from browser.

    Call this after user completes browser login and you've extracted
    the session cookies (sessionid, csrftoken). These cookies are persistent
    and will be used to automatically fetch/refresh JWT tokens as needed.

    Args:
        session_id: The sessionid cookie value from browser
        csrf_token: The csrftoken cookie value from browser

    Returns confirmation of stored session.

    Note: Unlike JWT tokens that expire in 5 minutes, session cookies
    are long-lived (days/weeks). The user won't need to re-authenticate
    frequently.
    """
    set_session_cookies(session_id, csrf_token)
    reset_client()  # Force client recreation with new auth

    return json.dumps({
        "success": True,
        "message": "Session cookies stored successfully. JWT tokens will be fetched automatically.",
        "session_set": {
            "session_id": bool(session_id),
            "csrf_token": bool(csrf_token),
        }
    })


@mcp.tool()
async def clear_auth_cookies() -> str:
    """Clear stored authentication cookies.

    Use this to log out or reset authentication state.
    """
    clear_auth()
    reset_client()

    return json.dumps({
        "success": True,
        "message": "Authentication cookies cleared",
    })


@mcp.tool()
async def get_cookie_extraction_script() -> str:
    """Get JavaScript code to extract session cookies from browser.

    Run this script in the browser console (after logging into Datarails)
    to get the session cookies (sessionid, csrftoken).

    These cookies are persistent and will be used to automatically
    fetch/refresh JWT tokens as needed.
    """
    auth = BrowserAuth()
    return json.dumps({
        "login_url": auth.get_login_url(),
        "target_domain": auth.base_url,
        "javascript": auth.get_session_extraction_js(),
        "instructions": [
            f"1. Navigate to {auth.get_login_url()} and complete login",
            f"2. After login, you'll be redirected to {auth.base_url}",
            "3. Execute the JavaScript code on that page to extract session cookies",
            "4. Pass session_id and csrf_token to set_auth_cookies tool",
            "5. Session cookies are persistent - no frequent re-authentication needed!",
        ],
    })


# =============================================================================
# Discovery Tools
# =============================================================================


@mcp.tool()
async def list_finance_tables() -> str:
    """List all available Finance OS tables.

    Returns a list of tables with their IDs, names, and basic metadata.
    Use this to discover what data is available for analysis.
    """
    client = get_client()
    return await client.list_tables()


@mcp.tool()
async def get_table_schema(table_id: str) -> str:
    """Get schema (columns, types) for a Finance OS table.

    Args:
        table_id: The ID of the table to get schema for

    Returns detailed column information including:
    - Column names and data types
    - Nullable flags
    - Primary key information
    - Foreign key relationships
    """
    client = get_client()
    return await client.get_schema(table_id)


@mcp.tool()
async def get_field_distinct_values(
    table_id: str, field_name: str, limit: int = 100
) -> str:
    """Get distinct values for a field. Useful for understanding categorical data.

    Args:
        table_id: The ID of the table
        field_name: The name of the field to get distinct values for
        limit: Maximum number of distinct values to return (default 100)

    Returns a list of unique values found in the specified field,
    along with their counts.
    """
    client = get_client()
    return await client.get_distinct_values(table_id, field_name, limit)


# =============================================================================
# Profiling Tools
# =============================================================================


@mcp.tool()
async def profile_table_summary(table_id: str) -> str:
    """Get comprehensive summary: row count, column stats, data quality metrics.

    Args:
        table_id: The ID of the table to profile

    Returns:
    - Total row count
    - Column count and types breakdown
    - Missing value statistics
    - Data quality score
    - Memory usage estimate
    """
    client = get_client()
    return await client.profile_summary(table_id)


@mcp.tool()
async def profile_numeric_fields(
    table_id: str, fields: list[str] | None = None
) -> str:
    """Profile numeric fields: MIN, MAX, AVG, SUM, COUNT, outliers.

    Args:
        table_id: The ID of the table to profile
        fields: Optional list of specific fields to profile. If None, profiles all numeric fields.

    Returns for each numeric field:
    - Min, max, mean, median, std deviation
    - Sum and count
    - Null count and percentage
    - Outlier detection (values beyond 3 standard deviations)
    - Distribution percentiles (25th, 50th, 75th, 95th, 99th)
    """
    client = get_client()
    return await client.profile_numeric(table_id, fields)


@mcp.tool()
async def profile_categorical_fields(
    table_id: str, fields: list[str] | None = None
) -> str:
    """Profile categorical fields: distinct values, NULL counts, cardinality.

    Args:
        table_id: The ID of the table to profile
        fields: Optional list of specific fields to profile. If None, profiles all categorical fields.

    Returns for each categorical field:
    - Distinct value count (cardinality)
    - Most frequent values with counts
    - Null count and percentage
    - Uniqueness ratio
    """
    client = get_client()
    return await client.profile_categorical(table_id, fields)


# =============================================================================
# Analysis Tools
# =============================================================================


@mcp.tool()
async def detect_anomalies(table_id: str) -> str:
    """Run automated anomaly detection via profiling (no raw data fetch).

    Args:
        table_id: The ID of the table to analyze

    Detects various anomaly types:
    - Numeric outliers (statistical)
    - Missing value patterns
    - Duplicate detection
    - Temporal anomalies (gaps, future dates)
    - Categorical anomalies (rare values, unexpected nulls)
    - Referential integrity issues

    Returns findings with severity levels (critical, high, medium, low)
    and recommendations for remediation.
    """
    client = get_client()
    return await client.detect_anomalies(table_id)


# =============================================================================
# Query Tools
# =============================================================================


@mcp.tool()
async def get_records_by_filter(
    table_id: str, filters: dict, limit: int = 100
) -> str:
    """Fetch specific records matching filters. Hard limit: 500 rows.

    Args:
        table_id: The ID of the table to query
        filters: Dictionary of field names to filter values.
                 Example: {"status": "active", "amount": {">": 1000}}
        limit: Maximum rows to return (default 100, max 500)

    Filter operators supported:
    - Equality: {"field": "value"}
    - Comparison: {"field": {">": 100, "<": 1000}}
    - In list: {"field": {"in": ["a", "b", "c"]}}
    - Null check: {"field": {"is_null": true}}
    - Like pattern: {"field": {"like": "%pattern%"}}
    """
    client = get_client()
    safe_limit = min(limit, 500)
    return await client.get_filtered(table_id, filters, safe_limit)


@mcp.tool()
async def get_sample_records(table_id: str, n: int = 20) -> str:
    """Get a random sample of records for quick inspection. Max 20 rows.

    Args:
        table_id: The ID of the table to sample
        n: Number of sample records to return (default 20, max 20)

    Useful for:
    - Quick data exploration
    - Understanding data format and content
    - Validating assumptions about the data
    """
    client = get_client()
    safe_n = min(n, 20)
    return await client.get_sample(table_id, safe_n)


@mcp.tool()
async def execute_query(table_id: str, query: str) -> str:
    """Execute a custom query against Finance OS. Returns max 1000 rows.

    Args:
        table_id: The ID of the table to query (used for authorization)
        query: SQL-like query string to execute

    Supports:
    - SELECT with column selection
    - WHERE clauses with conditions
    - ORDER BY for sorting
    - GROUP BY with aggregations
    - LIMIT (automatically capped at 1000)

    Note: Some operations may be restricted based on user permissions.
    """
    client = get_client()
    return await client.execute_query(table_id, query)


# =============================================================================
# Aggregation Tools
# =============================================================================

# Known dimension field alternatives for aggregation compatibility.
# Some fields cause HTTP 500 errors in certain Datarails environments when used
# as aggregation dimensions. This map provides alternatives in priority order.
_AGGREGATION_FIELD_ALTERNATIVES = {
    "DR_ACC_L1": ["DR_ACC_L1.5", "DR_ACC_L0.5"],
    "DR_ACC_L2": ["DR_ACC_L1.5", "DR_ACC_L0.5"],
    "Department L1": ["Cost Center"],
    "Department L2": ["Cost Center"],
}


def _format_aggregation_error(original_error: dict, dimensions: list[str]) -> str:
    """Format aggregation error with helpful retry guidance."""
    suggestions = []
    for dim in dimensions:
        if dim in _AGGREGATION_FIELD_ALTERNATIVES:
            alts = _AGGREGATION_FIELD_ALTERNATIVES[dim]
            suggestions.append(
                f"Instead of '{dim}', try: {', '.join(repr(a) for a in alts)}"
            )

    error_response = {
        "error": original_error.get("error", "Aggregation failed"),
        "details": original_error.get("details", ""),
        "dimensions_used": dimensions,
        "recommendation": (
            "Aggregation failed, likely due to an incompatible dimension field. "
            "IMPORTANT: Do NOT fall back to execute_query or get_records_by_filter — "
            "they are limited to 500-1000 rows and will give INCOMPLETE data. "
            "Instead, retry aggregate_table_data with different dimension fields."
        ),
    }
    if suggestions:
        error_response["suggested_alternatives"] = suggestions

    return json.dumps(error_response, indent=2, default=str)


@mcp.tool()
async def aggregate_table_data(
    table_id: str,
    dimensions: list[str],
    metrics: list[dict],
    filters: list[dict] | None = None,
) -> str:
    """Aggregate table data with grouping dimensions and metrics. NO ROW LIMIT.

    This is the correct way to extract financial totals - use aggregation
    instead of raw queries which are limited to 500-1000 rows.

    Args:
        table_id: The ID of the table to aggregate
        dimensions: List of fields to group by (e.g., ["Reporting Date", "DR_ACC_L1", "Department L1"])
        metrics: List of metric definitions with field and aggregation type.
                 Example: [{"field": "Amount", "agg": "SUM"}, {"field": "Amount", "agg": "COUNT"}]
        filters: Optional list of filter objects to narrow the data.
                 Example: [{"name": "Scenario", "values": ["Actuals"], "is_excluded": false}]

    Aggregation types supported:
    - SUM: Sum of values
    - AVG: Average of values
    - MIN: Minimum value
    - MAX: Maximum value
    - COUNT: Count of records
    - COUNT_DISTINCT: Count of distinct values

    Returns aggregated data grouped by the specified dimensions.
    Unlike get_records_by_filter (500 rows) or execute_query (1000 rows),
    aggregation has NO row limit and returns properly computed totals.

    If a dimension field causes a server error, this tool automatically retries
    with compatible alternative fields (e.g., DR_ACC_L1.5 instead of DR_ACC_L1).
    The response will note any field substitutions that were made.

    IMPORTANT: Never fall back to execute_query or get_records_by_filter for
    financial totals. Those tools have row limits and will return incomplete data.
    Always use this tool and retry with different dimension fields if needed.

    Example for P&L extraction:
        dimensions: ["Reporting Date", "DR_ACC_L1", "DR_ACC_L2", "Department L1"]
        metrics: [{"field": "Amount", "agg": "SUM"}]
        filters: [
            {"name": "Scenario", "values": ["Actuals"], "is_excluded": false},
            {"name": "DR_ACC_L0", "values": ["P&L"], "is_excluded": false}
        ]
    """
    client = get_client()

    # Try original request
    result = await client.aggregate_raw(table_id, dimensions, metrics, filters)

    if "error" not in result:
        return client._format_response(result)

    # Only auto-retry on 500 errors (likely field compatibility issue)
    if "500" not in str(result.get("error", "")):
        return client._format_response(result)

    # Identify dimensions that have known alternatives
    retryable = {
        dim: _AGGREGATION_FIELD_ALTERNATIVES[dim]
        for dim in dimensions
        if dim in _AGGREGATION_FIELD_ALTERNATIVES
    }

    if not retryable:
        return _format_aggregation_error(result, dimensions)

    # Try alternatives in priority order (max 2 attempts)
    max_attempts = max(len(alts) for alts in retryable.values())
    for attempt in range(max_attempts):
        new_dims = []
        subs = {}
        for dim in dimensions:
            if dim in retryable and attempt < len(retryable[dim]):
                alt = retryable[dim][attempt]
                new_dims.append(alt)
                subs[dim] = alt
            elif dim in retryable:
                # Use last available alternative
                alt = retryable[dim][-1]
                new_dims.append(alt)
                subs[dim] = alt
            else:
                new_dims.append(dim)

        retry_result = await client.aggregate_raw(
            table_id, new_dims, metrics, filters
        )

        if "error" not in retry_result:
            # Success with alternatives — return data with substitution note
            data = retry_result.get("data", retry_result)
            return json.dumps({
                "data": data,
                "_auto_substitutions": subs,
                "_note": (
                    "Some dimension fields were automatically substituted for "
                    "compatibility: "
                    + ", ".join(f"'{k}' -> '{v}'" for k, v in subs.items())
                    + ". Data is grouped by the substitute fields."
                ),
            }, indent=2, default=str)

    # All retries exhausted
    return _format_aggregation_error(result, dimensions)


# =============================================================================
# Workflow Guide
# =============================================================================

_WORKFLOWS = {
    "getting-started": {
        "description": "First time? Start here - authenticate and explore your data",
        "when_to_use": [
            "help", "get started", "connect", "what can you do",
            "how do I start", "new user", "setup",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Check if already authenticated",
                "tool": "check_auth_status",
                "on_error": "If not authenticated, guide user through browser login (see tips below)",
            },
            {
                "step": 2,
                "action": "Discover available tables",
                "tool": "list_finance_tables",
                "guidance": "Look for tables with P&L, Financials, or Income Statement in the name",
            },
            {
                "step": 3,
                "action": "Explore the main table structure",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id from step 2>"},
                "guidance": "Identify key fields: Amount, Account hierarchy (DR_ACC_L0/L1/L2), Scenario, Reporting Date",
            },
            {
                "step": 4,
                "action": "Preview sample data",
                "tool": "get_sample_records",
                "parameters_guidance": {"table_id": "<financials_table_id>", "n": 10},
            },
        ],
        "tips": [
            "If not authenticated: user must log into Datarails at https://app.datarails.com, then extract session cookies via browser console (F12 > Console) and provide session_id + csrf_token",
            "Use set_auth_cookies tool to store the extracted cookies",
            "After authentication, session cookies persist for days/weeks - no frequent re-auth needed",
        ],
        "next_workflows": ["financial-summary", "explore-data"],
    },
    "financial-summary": {
        "description": "Quick overview of revenue, expenses, and profit with real aggregated totals",
        "when_to_use": [
            "financial summary", "overview", "snapshot", "how are we doing",
            "P&L summary", "income statement", "financial overview",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find the financials table",
                "tool": "list_finance_tables",
                "guidance": "Look for tables with P&L, Financials, or Income Statement in the name",
            },
            {
                "step": 3,
                "action": "Get table schema to discover field names",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Identify: Amount field, Account hierarchy field (DR_ACC_L1 or similar), Scenario field, Date field",
            },
            {
                "step": 4,
                "action": "Get totals by account category",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<account_l1_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [{"name": "Scenario", "values": ["Actuals"], "is_excluded": False}],
                },
                "on_error": "The tool auto-retries with alternative fields if one fails (e.g., DR_ACC_L1.5 instead of DR_ACC_L1)",
            },
            {
                "step": 5,
                "action": "Get monthly trend data",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<date_field>", "<account_l1_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [{"name": "Scenario", "values": ["Actuals"], "is_excluded": False}],
                },
            },
            {
                "step": 6,
                "action": "Present summary with real numbers",
                "tool": None,
                "guidance": "Show totals by category (Revenue, COGS, OpEx), calculate gross profit and margins, show monthly trend direction",
            },
        ],
        "presentation_guide": "Show totals by category, calculate gross profit = Revenue - COGS, gross margin %, and indicate monthly trend direction (growing/stable/declining)",
        "tips": [
            "Aggregation returns complete totals in ~5 seconds - never fall back to sample-based estimates",
            "If a dimension field fails, the tool automatically retries with compatible alternatives",
            "Check for KPI tables too - they may have ARR, MRR, and other SaaS metrics",
        ],
        "next_workflows": ["expense-analysis", "revenue-trends", "budget-comparison"],
    },
    "expense-analysis": {
        "description": "Detailed expense breakdown - top spending categories, trends, and potential issues",
        "when_to_use": [
            "expense", "spending", "costs", "where is money going",
            "cost analysis", "expense breakdown", "operating expenses",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find the financials table",
                "tool": "list_finance_tables",
            },
            {
                "step": 3,
                "action": "Get table schema",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Identify account hierarchy fields and amount field",
            },
            {
                "step": 4,
                "action": "Get expense totals by category (excluding revenue)",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<account_l1_field>", "<account_l2_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [
                        {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
                        {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": True},
                    ],
                },
                "on_error": "If L2 field fails, retry with just L1 for a higher-level breakdown",
            },
            {
                "step": 5,
                "action": "Get monthly expense trend",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<date_field>", "<account_l1_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [
                        {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
                        {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": True},
                    ],
                },
            },
            {
                "step": 6,
                "action": "Present expense analysis",
                "tool": None,
                "guidance": "Show top expense categories with amounts and % of total, monthly trend, key findings, and recommendations",
            },
        ],
        "tips": [
            "Exclude revenue from expense analysis using is_excluded: true filter",
            "If DR_ACC_L2 fails, try DR_ACC_L1.5 or just use L1 for higher-level view",
            "Look for categories with unusually high concentration (>50% of total)",
        ],
        "next_workflows": ["budget-comparison", "data-quality"],
    },
    "revenue-trends": {
        "description": "Revenue patterns over time - growth rates, seasonal patterns, and composition",
        "when_to_use": [
            "revenue", "growth", "sales trends", "revenue trends",
            "top line", "ARR", "MRR", "revenue growth",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find financials and KPI tables",
                "tool": "list_finance_tables",
                "guidance": "Identify both the main P&L table and any KPI/metrics table",
            },
            {
                "step": 3,
                "action": "Get table schema",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
            },
            {
                "step": 4,
                "action": "Get monthly revenue totals",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<date_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [
                        {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": False},
                        {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
                    ],
                },
            },
            {
                "step": 5,
                "action": "Get revenue by sub-category",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<account_l2_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [
                        {"name": "<account_l1_field>", "values": ["<revenue_category>"], "is_excluded": False},
                        {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
                    ],
                },
                "on_error": "If L2 field fails, skip this step and show only top-level revenue",
            },
            {
                "step": 6,
                "action": "Check KPI metrics if KPI table exists",
                "tool": "get_sample_records",
                "parameters_guidance": {"table_id": "<kpi_table_id>", "n": 20},
                "guidance": "Look for ARR, MRR, Net New ARR, Churn metrics. Skip if no KPI table.",
            },
            {
                "step": 7,
                "action": "Present revenue analysis",
                "tool": None,
                "guidance": "Show monthly trend table with MoM change %, overall direction, peak month, growth rate, revenue composition, and KPI metrics if available",
            },
        ],
        "tips": [
            "Calculate MoM growth rate for each month",
            "If only one period of data exists, show breakdown instead of trends",
            "KPI tables often have ARR/MRR - check for them separately",
        ],
        "next_workflows": ["expense-analysis", "budget-comparison"],
    },
    "budget-comparison": {
        "description": "Compare actual results to budget - see where you're over or under plan",
        "when_to_use": [
            "budget", "variance", "actual vs budget", "over budget",
            "under budget", "budget comparison", "plan vs actual",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find financials table",
                "tool": "list_finance_tables",
            },
            {
                "step": 3,
                "action": "Get table schema",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Confirm Scenario field exists with Actuals and Budget values",
            },
            {
                "step": 4,
                "action": "Get Actuals totals by category",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<account_l1_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [{"name": "Scenario", "values": ["Actuals"], "is_excluded": False}],
                },
            },
            {
                "step": 5,
                "action": "Get Budget totals by category",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<account_l1_field>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [{"name": "Scenario", "values": ["Budget"], "is_excluded": False}],
                },
                "on_error": "If no Budget scenario exists, check what scenarios are available and offer to compare against Forecast or another scenario",
            },
            {
                "step": 6,
                "action": "Calculate and present variance analysis",
                "tool": None,
                "guidance": "Calculate dollar variance (Actual - Budget) and % variance for each category. Flag variances: >20% critical, 10-20% warning, 5-10% watch, <5% normal. Show favorable and unfavorable variances separately.",
            },
        ],
        "tips": [
            "Both Actuals and Budget queries complete in ~5 seconds each",
            "If no Budget scenario, offer to compare against Forecast or other available scenarios",
            "For revenue, over-budget is favorable; for expenses, under-budget is favorable",
            "Can add department-level breakdown by adding department field to dimensions",
        ],
        "next_workflows": ["expense-analysis", "revenue-trends"],
    },
    "data-quality": {
        "description": "Check your financial data for quality issues - missing values, anomalies, and inconsistencies",
        "when_to_use": [
            "data quality", "data check", "anomalies", "missing data",
            "data issues", "data health", "validate data",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find all tables",
                "tool": "list_finance_tables",
            },
            {
                "step": 3,
                "action": "Run anomaly detection on main table",
                "tool": "detect_anomalies",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Checks for outliers, missing data, duplicates, date anomalies, and referential integrity",
            },
            {
                "step": 4,
                "action": "Get table summary profile",
                "tool": "profile_table_summary",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Gets row counts, missing value percentages, data quality score",
            },
            {
                "step": 5,
                "action": "Profile numeric fields",
                "tool": "profile_numeric_fields",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Checks min/max values, statistical outliers, unexpected nulls",
            },
            {
                "step": 6,
                "action": "Profile categorical fields",
                "tool": "profile_categorical_fields",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Checks for unexpected values, high cardinality, inconsistent naming",
            },
            {
                "step": 7,
                "action": "Present data quality report",
                "tool": None,
                "guidance": "Show overall health score, issues by severity (critical/high/medium/low), specific findings for missing data/outliers/duplicates, and recommended actions",
            },
        ],
        "tips": [
            "Run anomaly detection on each important table, not just the main one",
            "High cardinality in category fields may indicate inconsistent naming",
            "Outliers in Amount field could be legitimate large transactions or data entry errors",
        ],
        "next_workflows": ["explore-data", "financial-summary"],
    },
    "explore-data": {
        "description": "Discover what tables and data are available in your Datarails account",
        "when_to_use": [
            "explore", "what data", "tables", "discover",
            "what's available", "show me my data", "browse",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "List all available tables",
                "tool": "list_finance_tables",
            },
            {
                "step": 3,
                "action": "Present table overview",
                "tool": None,
                "guidance": "Categorize tables (Financial, KPI, Master Data) based on column names. Show table name, ID, and inferred purpose.",
            },
            {
                "step": 4,
                "action": "Explore a specific table (on user request)",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<requested_table_id>"},
                "guidance": "Show columns with types and inferred meaning",
            },
            {
                "step": 5,
                "action": "Show sample data (on user request)",
                "tool": "get_sample_records",
                "parameters_guidance": {"table_id": "<requested_table_id>", "n": 10},
            },
        ],
        "tips": [
            "Financial tables typically have: Amount, Account hierarchy, Scenario, Date fields",
            "KPI tables typically have: Metric names, Quarter/Period, Calculated ratios",
            "Master data tables typically have: Names, Codes, IDs (no amount fields)",
            "Steps 4-5 are interactive - run them when the user asks about a specific table",
        ],
        "next_workflows": ["financial-summary", "data-quality"],
    },
    "api-test": {
        "description": "Test which fields work with aggregation in your environment and measure performance",
        "when_to_use": [
            "test api", "field compatibility", "diagnostic",
            "which fields work", "aggregation test", "troubleshoot",
        ],
        "steps": [
            {
                "step": 1,
                "action": "Verify authentication",
                "tool": "check_auth_status",
                "on_error": "Guide user through getting-started workflow",
            },
            {
                "step": 2,
                "action": "Find the financials table",
                "tool": "list_finance_tables",
            },
            {
                "step": 3,
                "action": "Get table schema to identify testable fields",
                "tool": "get_table_schema",
                "parameters_guidance": {"table_id": "<financials_table_id>"},
                "guidance": "Identify account hierarchy fields (L0, L1, L1.5, L2), date, scenario, department/cost center fields",
            },
            {
                "step": 4,
                "action": "Test each field individually with aggregation",
                "tool": "aggregate_table_data",
                "parameters_guidance": {
                    "table_id": "<financials_table_id>",
                    "dimensions": ["<field_to_test>"],
                    "metrics": [{"field": "Amount", "agg": "SUM"}],
                    "filters": [{"name": "Scenario", "values": ["Actuals"], "is_excluded": False}],
                },
                "guidance": "Test fields one at a time in this order: Scenario, Date, Account L0, L1, L2, L1.5, Department, Cost Center. Record PASS/FAIL for each.",
            },
            {
                "step": 5,
                "action": "Present diagnostic results",
                "tool": None,
                "guidance": "Show a table of fields with PASS/FAIL status, group count, and timing. Summarize which alternatives to use for failed fields. Each test takes ~5 seconds.",
            },
        ],
        "tips": [
            "Each field test takes about 5 seconds",
            "Testing 8 fields takes about 40 seconds total",
            "If ALL fields fail, the aggregation API may not work in this environment",
            "Results help optimize all other workflows for speed",
            "Run /dr-learn skill (in Claude Code) to auto-save results to client profile",
        ],
        "next_workflows": ["financial-summary", "explore-data"],
    },
}


@mcp.tool()
async def get_workflow_guide(workflow_name: str | None = None) -> str:
    """Get guided workflows for common financial analysis tasks.

    Call without arguments to see all available workflows.
    Call with a workflow name to get step-by-step guidance.

    Use this tool when:
    - A user is new and wants to know what they can do
    - A user asks for help or says "what can you do?"
    - You need guidance on which tools to use for a specific task
    - A user wants a financial summary, expense analysis, revenue trends, etc.

    Args:
        workflow_name: Optional. One of: getting-started, financial-summary,
                       expense-analysis, revenue-trends, budget-comparison,
                       data-quality, explore-data, api-test
    """
    if workflow_name is None:
        # List mode
        available = []
        for name, wf in _WORKFLOWS.items():
            available.append({
                "name": name,
                "description": wf["description"],
                "triggers": wf["when_to_use"],
            })
        return json.dumps({
            "available_workflows": available,
            "usage": "Call get_workflow_guide with a workflow name for step-by-step guidance",
            "tip": "Users can also just describe what they want in plain language and you can use the appropriate tools directly. These workflows provide structured guidance for common tasks.",
        }, indent=2)

    # Detail mode
    wf = _WORKFLOWS.get(workflow_name)
    if wf is None:
        return json.dumps({
            "error": f"Unknown workflow: {workflow_name}",
            "available_workflows": list(_WORKFLOWS.keys()),
        })

    return json.dumps({
        "workflow": workflow_name,
        "description": wf["description"],
        "steps": wf["steps"],
        "tips": wf.get("tips", []),
        "presentation_guide": wf.get("presentation_guide", ""),
        "next_workflows": wf.get("next_workflows", []),
    }, indent=2, default=str)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
