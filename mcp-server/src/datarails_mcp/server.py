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

    Example for P&L extraction:
        dimensions: ["Reporting Date", "DR_ACC_L1", "DR_ACC_L2", "Department L1"]
        metrics: [{"field": "Amount", "agg": "SUM"}]
        filters: [
            {"name": "Scenario", "values": ["Actuals"], "is_excluded": false},
            {"name": "DR_ACC_L0", "values": ["P&L"], "is_excluded": false}
        ]
    """
    client = get_client()
    return await client.aggregate(table_id, dimensions, metrics, filters)


def main():
    """Run the MCP server."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
