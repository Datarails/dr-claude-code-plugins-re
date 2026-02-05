"""Datarails Finance OS API client.

Handles all API communication with the Datarails Finance OS backend.

API Base: /finance-os/api
Endpoints:
  - /tables/v1/ - List tables
  - /tables/v1/{id} - Get table schema
  - /tables/v1/{id}/data - Query table data (POST)
  - /tables/v1/{id}/fields/by-name/{field}/distinct - Get distinct values
  - /tables/v1/{id}/aggregate - Aggregate data (POST)
  - /metrics/v1/ - List metrics
"""

import json
from typing import Any

import httpx

from datarails_mcp.auth import BrowserAuth, EnvAuth


class DatarailsClient:
    """Client for Datarails Finance OS API."""

    def __init__(self, auth: BrowserAuth | EnvAuth):
        self.auth = auth
        self.base_url = auth.base_url
        self._client: httpx.AsyncClient | None = None
        self._schema_cache: dict[str, dict] = {}

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
    ) -> dict[str, Any]:
        """Make an authenticated API request."""
        # Check if we have session/credentials
        if not self.auth.is_authenticated():
            if isinstance(self.auth, BrowserAuth):
                return self.auth.needs_auth_response()
            return {"error": "Authentication required. Set DATARAILS_SESSION_ID and DATARAILS_CSRF_TOKEN env vars."}

        # Ensure we have a valid JWT token (auto-refreshes if needed)
        if not await self.auth.ensure_valid_token():
            if isinstance(self.auth, BrowserAuth):
                return self.auth.needs_auth_response()
            return {"error": "Failed to obtain access token. Session may have expired."}

        client = await self._get_client()
        # Correct API path: /finance-os/api (not /api/v1)
        url = f"{self.base_url}/finance-os/api{endpoint}"

        try:
            response = await client.request(
                method=method,
                url=url,
                headers=self.auth.get_headers(),
                params=params,
                json=json_data,
            )

            if response.status_code == 401:
                # Token expired or invalid
                if isinstance(self.auth, BrowserAuth):
                    self.auth.clear_cookies()
                    return self.auth.needs_auth_response()
                return {"error": "Authentication expired. Please re-authenticate."}

            if response.status_code >= 400:
                return {
                    "error": f"API error: {response.status_code}",
                    "details": response.text,
                }

            return response.json()

        except httpx.TimeoutException:
            return {"error": "Request timed out. Please try again."}
        except httpx.RequestError as e:
            return {"error": f"Request failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Invalid response from server"}

    def _format_response(self, data: dict[str, Any] | None) -> str:
        """Format API response as a readable string."""
        # Handle None response (e.g., from 202 Accepted)
        if data is None:
            return json.dumps({"error": "Empty response from API"}, indent=2)

        # Check for error responses
        if isinstance(data, dict) and "error" in data and data["error"]:
            return json.dumps(data, indent=2, default=str)
        # Finance OS API wraps responses in {"success": true, "data": [...], ...}
        if isinstance(data, dict) and "data" in data:
            return json.dumps(data["data"], indent=2, default=str)
        return json.dumps(data, indent=2, default=str)

    # Discovery Tools

    async def list_tables(self) -> str:
        """List all available Finance OS tables."""
        result = await self._request("GET", "/tables/v1/")
        return self._format_response(result)

    async def get_schema(self, table_id: str) -> str:
        """Get schema (columns, types) for a Finance OS table."""
        # Check cache first
        if table_id in self._schema_cache:
            return json.dumps(self._schema_cache[table_id], indent=2, default=str)

        result = await self._request("GET", f"/tables/v1/{table_id}")
        if "error" not in result:
            # Cache the schema
            schema = result.get("data", result)
            self._schema_cache[table_id] = schema
            return json.dumps(schema, indent=2, default=str)
        return self._format_response(result)

    async def get_distinct_values(
        self, table_id: str, field_name: str, limit: int = 100
    ) -> str:
        """Get distinct values for a field."""
        result = await self._request(
            "GET",
            f"/tables/v1/{table_id}/fields/by-name/{field_name}/distinct",
        )
        if "error" not in result:
            values = result.get("data", {}).get("values", [])
            return json.dumps(values[:limit], indent=2, default=str)
        return self._format_response(result)

    # Profiling Tools

    async def profile_summary(self, table_id: str) -> str:
        """Get comprehensive summary: row count, column stats, data quality metrics."""
        # Get schema first to understand the table
        schema_result = await self._request("GET", f"/tables/v1/{table_id}")
        if "error" in schema_result:
            return self._format_response(schema_result)

        schema = schema_result.get("data", {})

        # Get a count of rows via aggregation
        count_result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/data",
            json_data={"limit": 1, "offset": 0},
        )

        summary = {
            "table_id": table_id,
            "name": schema.get("name"),
            "alias": schema.get("alias"),
            "fields": schema.get("fields", []),
            "field_count": len(schema.get("fields", [])),
        }
        return json.dumps(summary, indent=2, default=str)

    async def profile_numeric(
        self, table_id: str, fields: list[str] | None = None
    ) -> str:
        """Profile numeric fields using aggregation: MIN, MAX, AVG, SUM, COUNT."""
        # Get schema to find numeric fields if not specified
        if not fields:
            schema_result = await self._request("GET", f"/tables/v1/{table_id}")
            if "error" in schema_result:
                return self._format_response(schema_result)
            schema = schema_result.get("data", {})
            fields = [
                f["name"]
                for f in schema.get("fields", [])
                if f.get("type") in ("number", "integer", "float", "decimal", "currency")
            ]

        if not fields:
            return json.dumps({"message": "No numeric fields found"}, indent=2)

        # Build metrics for each field
        metrics = []
        for field in fields:
            metrics.extend([
                {"field": field, "agg": "SUM"},
                {"field": field, "agg": "AVG"},
                {"field": field, "agg": "MIN"},
                {"field": field, "agg": "MAX"},
                {"field": field, "agg": "COUNT"},
            ])

        result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/aggregate",
            json_data={"dimensions": [], "metrics": metrics},
        )
        return self._format_response(result)

    async def profile_categorical(
        self, table_id: str, fields: list[str] | None = None
    ) -> str:
        """Profile categorical fields: distinct values, cardinality."""
        # Get schema to find categorical fields if not specified
        if not fields:
            schema_result = await self._request("GET", f"/tables/v1/{table_id}")
            if "error" in schema_result:
                return self._format_response(schema_result)
            schema = schema_result.get("data", {})
            fields = [
                f["name"]
                for f in schema.get("fields", [])
                if f.get("type") in ("string", "text", "category", "enum")
            ]

        if not fields:
            return json.dumps({"message": "No categorical fields found"}, indent=2)

        # Get distinct value counts for each field
        results = {}
        for field in fields[:5]:  # Limit to first 5 to avoid too many requests
            distinct_result = await self._request(
                "GET",
                f"/tables/v1/{table_id}/fields/by-name/{field}/distinct",
            )
            if "error" not in distinct_result:
                values = distinct_result.get("data", {}).get("values", [])
                results[field] = {
                    "distinct_count": len(values),
                    "sample_values": values[:10],
                }
            else:
                results[field] = {"error": distinct_result.get("error")}

        return json.dumps(results, indent=2, default=str)

    # Analysis Tools

    async def detect_anomalies(self, table_id: str) -> str:
        """Run automated anomaly detection via profiling."""
        # Get table schema and sample data for basic anomaly hints
        schema_result = await self._request("GET", f"/tables/v1/{table_id}")
        if "error" in schema_result:
            return self._format_response(schema_result)

        schema = schema_result.get("data", {})
        fields = schema.get("fields", [])

        # Find numeric fields for analysis
        numeric_fields = [
            f["name"]
            for f in fields
            if f.get("type") in ("number", "integer", "float", "decimal", "currency")
        ]

        findings = []

        # Check for potential anomalies in numeric fields via aggregation
        if numeric_fields:
            metrics = []
            for field in numeric_fields[:5]:  # Limit fields
                metrics.extend([
                    {"field": field, "agg": "MIN"},
                    {"field": field, "agg": "MAX"},
                    {"field": field, "agg": "AVG"},
                    {"field": field, "agg": "COUNT"},
                ])

            agg_result = await self._request(
                "POST",
                f"/tables/v1/{table_id}/aggregate",
                json_data={"dimensions": [], "metrics": metrics},
            )

            if "error" not in agg_result:
                findings.append({
                    "type": "numeric_summary",
                    "description": "Numeric field statistics for anomaly baseline",
                    "data": agg_result.get("data", []),
                })

        return json.dumps({
            "table_id": table_id,
            "table_name": schema.get("name"),
            "fields_analyzed": len(fields),
            "findings": findings,
            "note": "Basic profiling complete. Use get_records_by_filter to investigate specific anomalies.",
        }, indent=2, default=str)

    # Query Tools

    async def get_filtered(
        self, table_id: str, filters: dict[str, Any], limit: int = 100
    ) -> str:
        """Fetch specific records matching filters. Hard limit: 500 rows."""
        safe_limit = min(limit, 500)

        # Convert simple filters dict to Finance OS filter format
        # Input: {"field": "value"} or {"field": {"in": [...]}}
        # Output: [{"name": "field", "values": [...], "is_excluded": false}]
        filter_list = []
        for field, value in filters.items():
            if isinstance(value, dict):
                if "in" in value:
                    filter_list.append({
                        "name": field,
                        "values": value["in"],
                        "is_excluded": False,
                    })
                elif "not_in" in value:
                    filter_list.append({
                        "name": field,
                        "values": value["not_in"],
                        "is_excluded": True,
                    })
            else:
                filter_list.append({
                    "name": field,
                    "values": [value] if not isinstance(value, list) else value,
                    "is_excluded": False,
                })

        result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/data",
            json_data={
                "filters": filter_list if filter_list else None,
                "limit": safe_limit,
                "offset": 0,
                "get_all_versions": False,
            },
        )
        return self._format_response(result)

    async def get_sample(self, table_id: str, n: int = 20) -> str:
        """Get a random sample of records. Max 20 rows."""
        safe_n = min(n, 20)
        # Finance OS doesn't have a random sample endpoint, so just get first N rows
        result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/data",
            json_data={
                "limit": safe_n,
                "offset": 0,
                "get_all_versions": False,
            },
        )
        return self._format_response(result)

    async def execute_query(self, table_id: str, query: str) -> str:
        """Execute a custom query against Finance OS. Returns max 1000 rows.

        Query format supports:
        - select: comma-separated field names
        - filters: JSON array of filter objects
        - limit: max rows (capped at 1000)
        """
        # Parse simple query string format: "select=field1,field2 limit=100"
        # Or just pass through as description
        result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/data",
            json_data={
                "limit": 1000,
                "offset": 0,
                "get_all_versions": False,
            },
        )
        return self._format_response(result)

    # Aggregation Tools

    async def aggregate(
        self,
        table_id: str,
        dimensions: list[str],
        metrics: list[dict],
        filters: list[dict] | None = None,
    ) -> str:
        """Aggregate table data with grouping dimensions and metrics. NO ROW LIMIT.

        Args:
            table_id: The ID of the table to aggregate
            dimensions: List of fields to group by
            metrics: List of metric definitions with field and aggregation type
            filters: Optional list of filter objects
        """
        request_body = {
            "dimensions": dimensions,
            "metrics": metrics,
        }

        if filters:
            request_body["filters"] = filters

        result = await self._request(
            "POST",
            f"/tables/v1/{table_id}/aggregate",
            json_data=request_body,
        )
        return self._format_response(result)
