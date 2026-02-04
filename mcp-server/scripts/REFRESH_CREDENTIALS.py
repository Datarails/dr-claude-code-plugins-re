"""
Quick script to refresh credentials when they expire

Run this in the notebook when you get 401 errors:
"""

import sys
sys.path.insert(0, "/Users/stasg/DataRails-dev/dr-claude-code-plugins-re/mcp-server/src")

import asyncio
from datarails_mcp.auth import get_auth

print("="*80)
print("REFRESHING CREDENTIALS")
print("="*80)

async def refresh_creds():
    auth = get_auth("app")
    await auth.ensure_valid_token()
    headers = auth.get_headers()

    jwt_token = headers.get('Authorization', '').replace('Bearer ', '')
    csrf_token = headers.get('X-CSRFToken', '')

    print(f"\n✓ Credentials refreshed!")
    print(f"\nUpdate the CONFIG dict above with these values:\n")
    print(f'CONFIG = {{')
    print(f'    "base_url": "https://app.datarails.com",')
    print(f'    "jwt_token": "{jwt_token}",')
    print(f'    "csrf_token": "{csrf_token}",')
    print(f'    "table_id": "16528",')
    print(f'}}')
    print(f"\nThen run this cell again to reinitialize the API client:")
    print(f"api = DatarailsAPI(CONFIG)")
    print(f"print('✓ API client reinitialized with new credentials')")

    return jwt_token, csrf_token

jwt, csrf = asyncio.run(refresh_creds())
