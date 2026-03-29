---
name: dr-auth
description: Authenticate with Datarails Finance OS and store credentials for SDK usage
allowed-tools:
  - Bash
  - Read
  - Write
argument-hint: "[--env production]"
---

# Datarails Authentication

Authenticate with Datarails Finance OS via OAuth and store tokens for SDK usage.

## Execution

Write the following script to a temp file and run it with `python3`. It has **zero external dependencies** — uses only Python stdlib.

```python
import base64
import hashlib
import http.server
import json
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser
from pathlib import Path

AUTH_SERVER = "https://auth.datarails.com"
CALLBACK_PORT = 9876
CALLBACK_URL = f"http://localhost:{CALLBACK_PORT}/callback"
CLIENT_ID = "claude-code"
CREDS_DIR = Path.home() / ".datarails"
CREDS_PATH = CREDS_DIR / "credentials.json"


def create_auth_request():
    state = secrets.token_hex(32)
    code_verifier = secrets.token_urlsafe(32)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

    auth_url = (
        f"{AUTH_SERVER}/"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={urllib.parse.quote(CALLBACK_URL)}"
        f"&state={state}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
        f"#/authorize"
    )
    return auth_url, state


def exchange_token(session_token, env_url):
    exchange_url = f"{env_url}/jwt/api/external/token/"
    data = json.dumps({"session_token": session_token}).encode()
    req = urllib.request.Request(exchange_url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        tokens = json.loads(resp.read())
    return tokens["access"], tokens["refresh"]


def main():
    auth_url, expected_state = create_auth_request()
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == "/callback":
                params = urllib.parse.parse_qs(parsed.query)
                result["token"] = params.get("session_token", params.get("token", [None]))[0]
                result["env_url"] = params.get("env_url", [None])[0]
                result["state"] = params.get("state", [None])[0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Authenticated! You can close this tab.</h1>")
        def log_message(self, *args):
            pass

    server = http.server.HTTPServer(("localhost", CALLBACK_PORT), Handler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.start()

    print(f"Opening browser for Datarails login...")
    webbrowser.open(auth_url)

    server_thread.join(timeout=120)
    server.server_close()

    if not result.get("token"):
        print("ERROR: Authentication timed out or failed.")
        return

    if result["state"] != expected_state:
        print("ERROR: State mismatch — possible CSRF attack.")
        return

    print("Exchanging token...")
    access, refresh = exchange_token(result["token"], result["env_url"])

    CREDS_DIR.mkdir(parents=True, exist_ok=True)
    CREDS_PATH.write_text(json.dumps({
        "access": access,
        "refresh": refresh,
        "env_url": result["env_url"],
    }, indent=2))

    print(f"Authenticated successfully!")
    print(f"Environment: {result['env_url']}")
    print(f"Credentials saved to: {CREDS_PATH}")


main()
```

## After Authentication

Credentials are stored at `~/.datarails/credentials.json` (persists across sessions and working directories).

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Browser doesn't open | Copy the URL from terminal and open manually |
| Port 9876 in use | Kill the process using the port and retry |
| Token expired | Run `/dr-auth` again |
