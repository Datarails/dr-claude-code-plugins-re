"""
Generate JWT Token dynamically from Session ID and CSRF Token

This eliminates the need to manually refresh tokens every 5 minutes.
The JWT is generated server-side and cached automatically.
"""

import sys
sys.path.insert(0, "/Users/stasg/DataRails-dev/dr-claude-code-plugins-re/mcp-server/src")

import asyncio
import httpx
from datarails_mcp.auth import get_auth

async def get_dynamic_credentials():
    """
    Get JWT token and CSRF token dynamically from session

    This method:
    1. Reads session cookies from browser/keyring
    2. Exchanges them for a fresh JWT token
    3. Returns both JWT and CSRF for API calls
    """

    print("="*80)
    print("GENERATING DYNAMIC CREDENTIALS")
    print("="*80)
    print()

    # Get auth object which handles session/JWT management
    auth = get_auth("app")

    # Ensure token is valid (auto-refreshes if needed)
    await auth.ensure_valid_token()

    # Get headers with JWT
    headers = auth.get_headers()

    jwt_token = headers.get('Authorization', '').replace('Bearer ', '')
    csrf_token = headers.get('X-CSRFToken', '')

    print("✓ Credentials generated from session")
    print()
    print(f"JWT Token (valid ~5 min):")
    print(f"  {jwt_token[:60]}...")
    print()
    print(f"CSRF Token:")
    print(f"  {csrf_token[:60]}...")
    print()

    # Create CONFIG dict
    config = {
        "base_url": "https://app.datarails.com",
        "jwt_token": jwt_token,
        "csrf_token": csrf_token,
        "table_id": "16528",
    }

    print("✓ CONFIG ready to use in notebook:")
    print()
    print("CONFIG = {")
    print(f'    "base_url": "{config["base_url"]}",')
    print(f'    "jwt_token": "{jwt_token}",')
    print(f'    "csrf_token": "{csrf_token}",')
    print(f'    "table_id": "{config["table_id"]}",')
    print("}")

    return config

# Run it - handle both terminal and Jupyter contexts
try:
    loop = asyncio.get_running_loop()
    # Already in async context (e.g., Jupyter notebook)
    print("⚠️  Running in async context (Jupyter?)")
    print("    Use the notebook cell instead of running this as a script")
    import sys
    sys.exit(1)
except RuntimeError:
    # No loop running - safe to use asyncio.run()
    config = asyncio.run(get_dynamic_credentials())


# TEST IT
print()
print("="*80)
print("TESTING THE CREDENTIALS")
print("="*80)
print()

async def test_creds(config):
    """Test that credentials work"""

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{config['base_url']}/finance-os/api/tables/v1/{config['table_id']}/data",
            json={
                "filters": [
                    {"name": "Scenario", "values": ["Actuals"], "is_excluded": False},
                    {"name": "System_Year", "values": ["2025"], "is_excluded": False},
                    {"name": "DR_ACC_L0", "values": ["P&L"], "is_excluded": False},
                ],
                "limit": 1,
                "offset": 0
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {config['jwt_token']}",
                "X-CSRFToken": config['csrf_token']
            },
            timeout=30
        )

    if response.status_code == 200:
        print("✓ Credentials work! API returned 200 OK")
        print("✓ Ready to use in notebook")
    else:
        print(f"✗ Failed with status {response.status_code}")
        print(f"  Error: {response.text[:100]}")

asyncio.run(test_creds(config))
