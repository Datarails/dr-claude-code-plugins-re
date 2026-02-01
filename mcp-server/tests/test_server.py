"""Tests for the Datarails MCP server."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


@pytest.fixture
def mock_env_auth():
    """Create a mock environment auth with session cookies."""
    with patch.dict(
        "os.environ",
        {
            "DATARAILS_SESSION_ID": "test-session-id",
            "DATARAILS_CSRF_TOKEN": "test-csrf-token",
            "DATARAILS_ENV": "dev",
        },
    ):
        yield


@pytest.fixture
def mock_no_env():
    """Mock environment with no auth configured."""
    with patch.dict("os.environ", {}, clear=True):
        with patch("datarails_mcp.auth.keyring") as mock_keyring:
            mock_keyring.get_password.return_value = None
            yield mock_keyring


class TestEnvAuth:
    """Tests for environment variable authentication."""

    def test_env_auth_configured(self, mock_env_auth):
        from datarails_mcp.auth import EnvAuth

        auth = EnvAuth()
        assert auth.is_configured()
        assert auth._session_id == "test-session-id"
        assert auth._csrf_token == "test-csrf-token"

    def test_env_auth_headers(self, mock_env_auth):
        from datarails_mcp.auth import EnvAuth

        auth = EnvAuth()
        # Simulate having fetched a token
        auth._access_token = "test-jwt-token"
        headers = auth.get_headers()

        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test-jwt-token"
        assert headers["X-CSRFToken"] == "test-csrf-token"

    def test_env_auth_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            from datarails_mcp.auth import EnvAuth

            auth = EnvAuth()
            assert not auth.is_configured()

    def test_env_auth_with_direct_jwt(self):
        """Test direct JWT token without session cookies."""
        with patch.dict("os.environ", {"DATARAILS_JWT_TOKEN": "direct-jwt"}, clear=True):
            from datarails_mcp.auth import EnvAuth

            auth = EnvAuth()
            assert auth.is_configured()
            assert auth._access_token == "direct-jwt"


class TestBrowserAuth:
    """Tests for browser-based session authentication."""

    def test_browser_auth_not_authenticated_initially(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        assert not auth.is_authenticated()
        assert not auth.has_session()

    def test_browser_auth_set_session_cookies(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        auth.set_session_cookies(
            session_id="my-session-id",
            csrf_token="my-csrf-token",
        )

        assert auth.is_authenticated()
        assert auth.has_session()
        assert auth._session_id == "my-session-id"
        assert auth._csrf_token == "my-csrf-token"

    def test_browser_auth_headers_with_token(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        auth.set_session_cookies("my-session", "my-csrf")
        # Simulate having fetched a token
        auth._access_token = "my-jwt-token"

        headers = auth.get_headers()
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer my-jwt-token"
        assert headers["X-CSRFToken"] == "my-csrf"

    def test_browser_auth_needs_auth_response(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        response = auth.needs_auth_response()

        assert response["error"] == "authentication_required"
        assert "login_url" in response
        assert "extraction_js" in response
        assert "instructions" in response

    def test_browser_auth_extraction_js(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        js = auth.get_session_extraction_js()

        assert "sessionid" in js
        assert "csrftoken" in js

    def test_browser_auth_clear_session(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        auth.set_session_cookies("my-session", "my-csrf")
        auth._access_token = "my-jwt"
        assert auth.is_authenticated()

        auth.clear_session()
        assert not auth.is_authenticated()
        assert auth._session_id is None
        assert auth._access_token is None

    def test_browser_auth_token_info(self, mock_no_env):
        from datarails_mcp.auth import BrowserAuth

        auth = BrowserAuth()
        auth.set_session_cookies("my-session", "my-csrf")

        info = auth.token_info
        assert info["has_session"] is True
        assert info["has_access_token"] is False
        assert info["needs_refresh"] is True


class TestGetAuth:
    """Tests for auth selection logic."""

    def test_uses_env_auth_when_configured(self, mock_env_auth):
        from datarails_mcp.auth import get_auth, EnvAuth

        auth = get_auth()
        assert isinstance(auth, EnvAuth)

    def test_uses_browser_auth_when_env_not_configured(self, mock_no_env):
        from datarails_mcp.auth import get_auth, BrowserAuth

        auth = get_auth()
        assert isinstance(auth, BrowserAuth)


class TestDatarailsClient:
    """Tests for the Datarails API client."""

    @pytest.fixture
    def client(self, mock_env_auth):
        from datarails_mcp.auth import EnvAuth
        from datarails_mcp.client import DatarailsClient

        auth = EnvAuth()
        # Pre-set a token to avoid token fetch in tests
        auth._access_token = "test-jwt-token"
        auth._access_exp = 9999999999  # Far future
        return DatarailsClient(auth)

    async def test_list_tables(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "data": [
                    {"id": "1", "name": "Revenue"},
                    {"id": "2", "name": "Expenses"},
                ]
            }

            result = await client.list_tables()

            mock_request.assert_called_once_with("GET", "/tables/v1/")
            assert "Revenue" in result
            assert "Expenses" in result

    async def test_get_schema(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {
                "data": {
                    "id": "123",
                    "name": "Test Table",
                    "fields": [
                        {"name": "id", "type": "integer"},
                        {"name": "amount", "type": "decimal"},
                    ]
                }
            }

            result = await client.get_schema("123")

            mock_request.assert_called_once_with("GET", "/tables/v1/123")
            assert "id" in result
            assert "amount" in result

    async def test_profile_numeric(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            # First call returns schema, second returns aggregation
            mock_request.side_effect = [
                {"data": {"fields": [{"name": "amount", "type": "number"}]}},
                {"data": [{"amount_SUM": 10000, "amount_AVG": 500}]}
            ]

            result = await client.profile_numeric("123", ["amount"])

            # Should call aggregate endpoint
            assert mock_request.call_count == 1
            call_args = mock_request.call_args
            assert call_args[0][0] == "POST"
            assert "/aggregate" in call_args[0][1]

    async def test_get_filtered_respects_limit(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": []}

            # Request more than max allowed
            await client.get_filtered("123", {"status": "active"}, limit=1000)

            # Should cap at 500
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["json_data"]["limit"] == 500

    async def test_get_sample_respects_limit(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"data": []}

            # Request more than max allowed
            await client.get_sample("123", n=50)

            # Should cap at 20
            mock_request.assert_called_once()
            call_args = mock_request.call_args
            assert call_args[1]["json_data"]["limit"] == 20

    async def test_error_handling(self, client):
        with patch.object(client, "_request", new_callable=AsyncMock) as mock_request:
            mock_request.return_value = {"error": "Not found"}

            result = await client.list_tables()

            assert "error" in result
            assert "Not found" in result


class TestMCPServerAuthTools:
    """Tests for the MCP server authentication tools."""

    async def test_check_auth_status_authenticated(self, mock_env_auth):
        # Reset the client to pick up new auth
        import datarails_mcp.server as server_module
        server_module._client = None

        from datarails_mcp.server import check_auth_status

        result = await check_auth_status()
        data = json.loads(result)

        assert data["authenticated"] is True

    async def test_check_auth_status_not_authenticated(self, mock_no_env):
        import datarails_mcp.server as server_module
        server_module._client = None

        from datarails_mcp.server import check_auth_status

        result = await check_auth_status()
        data = json.loads(result)

        # When not authenticated, returns auth-needed response
        assert data["error"] == "authentication_required"
        assert "login_url" in data
        assert "instructions" in data

    async def test_set_auth_cookies(self, mock_no_env):
        import datarails_mcp.server as server_module
        server_module._client = None

        from datarails_mcp.server import set_auth_cookies

        result = await set_auth_cookies(
            session_id="new-session-id",
            csrf_token="new-csrf-token",
        )
        data = json.loads(result)

        assert data["success"] is True
        assert data["session_set"]["session_id"] is True
        assert data["session_set"]["csrf_token"] is True

    async def test_get_cookie_extraction_script(self, mock_no_env):
        from datarails_mcp.server import get_cookie_extraction_script

        result = await get_cookie_extraction_script()
        data = json.loads(result)

        assert "login_url" in data
        assert "javascript" in data
        assert "instructions" in data
        assert "sessionid" in data["javascript"]
        assert "csrftoken" in data["javascript"]


class TestMCPServerDataTools:
    """Tests for the MCP server data tools."""

    @pytest.fixture
    def mock_client(self, mock_env_auth):
        with patch("datarails_mcp.server._client", None):
            with patch("datarails_mcp.server.get_client") as mock_get:
                mock_instance = MagicMock()
                mock_get.return_value = mock_instance
                yield mock_instance

    async def test_list_finance_tables(self, mock_client):
        from datarails_mcp.server import list_finance_tables

        mock_client.list_tables = AsyncMock(return_value='{"tables": []}')

        result = await list_finance_tables()

        mock_client.list_tables.assert_called_once()
        assert "tables" in result

    async def test_get_table_schema(self, mock_client):
        from datarails_mcp.server import get_table_schema

        mock_client.get_schema = AsyncMock(return_value='{"columns": []}')

        result = await get_table_schema("123")

        mock_client.get_schema.assert_called_once_with("123")
        assert "columns" in result

    async def test_detect_anomalies(self, mock_client):
        from datarails_mcp.server import detect_anomalies

        mock_client.detect_anomalies = AsyncMock(
            return_value='{"anomalies": [], "severity": "low"}'
        )

        result = await detect_anomalies("123")

        mock_client.detect_anomalies.assert_called_once_with("123")
        assert "anomalies" in result

    async def test_get_records_by_filter_caps_limit(self, mock_client):
        from datarails_mcp.server import get_records_by_filter

        mock_client.get_filtered = AsyncMock(return_value='{"records": []}')

        await get_records_by_filter("123", {"status": "active"}, limit=1000)

        # Should be capped at 500
        mock_client.get_filtered.assert_called_once_with(
            "123", {"status": "active"}, 500
        )

    async def test_get_sample_records_caps_limit(self, mock_client):
        from datarails_mcp.server import get_sample_records

        mock_client.get_sample = AsyncMock(return_value='{"records": []}')

        await get_sample_records("123", n=100)

        # Should be capped at 20
        mock_client.get_sample.assert_called_once_with("123", 20)
