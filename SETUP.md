# Datarails Finance OS Plugin - Setup Guide

## Cowork Setup (Claude Desktop)

### Option 1: Upload ZIP (Recommended)

1. Download the plugin ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest)
2. Open Claude Desktop → Browse plugins → **Personal** tab
3. Click **+** → **Upload plugin**
4. Select the downloaded ZIP
5. Restart Claude Desktop

### Option 2: Marketplace (GitHub)

```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install Datarails-FinanceOS@datarails-marketplace
```

### After Installation

```
What can you do with Datarails?
```

### Authentication

OAuth via MCP transport — automatic when the connector is connected. Click "+" > Connectors > Datarails > Connect.

---

## Claude Code Setup

### Prerequisites

- [Claude Code](https://docs.anthropic.com/claude-code) installed
- Python 3.11+ with `uv` package manager
- A Datarails account with access to Finance OS
- JFrog (datarails.jfrog.io) credentials for installing the SDK

### Step 1: Configure JFrog

```bash
uv auth login https://datarails.jfrog.io/artifactory/api/pypi/dr-pypi \
  --username YOUR_EMAIL --password YOUR_JFROG_TOKEN
```

Add to `~/.config/uv/uv.toml`:
```toml
[[index]]
name = "dr-pypi"
url = "https://datarails.jfrog.io/artifactory/api/pypi/dr-pypi/simple"
default = true

[[index]]
name = "pypi"
url = "https://pypi.org/simple"
```

### Step 2: Install SDK

```bash
uv venv
source .venv/bin/activate
uv pip install dr-datarails-sdk
```

### Step 3: Install Plugin

**From marketplace:**
```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install Datarails-FinanceOS-Code@datarails-marketplace
```

**Local dev:**
```bash
source .venv/bin/activate
claude --plugin-dir /path/to/dr-claude-code-plugins-re/code
```

### Step 4: Authenticate

In Claude Code, run:
```
/dr-auth
```

A browser opens for Datarails login. Credentials are saved to `~/.datarails/credentials.json`.

### Step 5: Test

```
list my datarails tables
ask the datarails AI: what is 2+2?
```

---

## API Performance

| Approach | Speed | Use Case |
|----------|-------|----------|
| Aggregation API | ~5 seconds | Summaries, totals, grouped data |
| Pagination | ~10 minutes (50K+ rows) | Raw data extraction, full exports |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Cowork:** Tools not available | Connect via Connectors UI ("+" > Connectors > Datarails > Connect) |
| **Cowork:** "Not authenticated" | Disconnect and reconnect |
| **Code:** "No credentials" | Run `/dr-auth` |
| **Code:** SDK import error | Activate venv: `source .venv/bin/activate` |
| **Code:** JFrog 401 | Re-run `uv auth login` with correct credentials |
| "No profile found" | Run `/dr-learn` (Cowork) or ask "learn my tables" (Code) |
| Slow extraction | Normal for raw data. Use aggregation for summaries. |

---

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
