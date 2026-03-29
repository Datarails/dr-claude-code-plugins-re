# Datarails Finance OS Plugin for Claude

Analyze financial data, detect anomalies, and generate insights directly from Claude.

This repo contains **two plugins** for different environments:

| Plugin | For | How it works |
|--------|-----|-------------|
| **Datarails-FinanceOS** | Cowork (Claude Desktop) | MCP-based — Claude calls tools directly |
| **Datarails-FinanceOS-Code** | Claude Code (terminal) | SDK-based — Claude writes and runs code |

## Install

### Cowork (Claude Desktop)

**Option 1: Upload ZIP (Recommended)**

1. Download the plugin ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest)
2. Open Claude Desktop → Browse plugins → **Personal** tab
3. Click **+** → **Upload plugin**
4. Select the downloaded ZIP
5. Install the **Datarails FinanceOS** plugin

**Option 2: Add from GitHub**

```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install Datarails-FinanceOS@datarails-marketplace
```

### Claude Code (Terminal)

**From marketplace:**
```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install Datarails-FinanceOS-Code@datarails-marketplace
```

**Local dev:**
```bash
# Requires: uv venv with dr-datarails-sdk installed, or PYTHONPATH set
claude --plugin-dir ./code
```

---

## Getting Started

### Cowork
Once the Datarails connector is connected, start with:
```
/dr-tables                             # List available tables
/dr-learn                              # Create client profile (first time)
/dr-intelligence --year 2025           # Generate FP&A intelligence workbook
```

### Claude Code
```
/dr-auth                               # Authenticate (first time)
list my datarails tables               # Then ask anything naturally
```

---

## Cowork Skills

| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-learn` | Discover table structure and create client profile | Profile JSON |
| `/dr-tables` | List and explore tables | Table metadata |
| `/dr-profile` | Profile field statistics | Stats |
| `/dr-query` | Query and filter records | Data |
| `/dr-extract` | Extract financial data to Excel | Excel |
| `/dr-intelligence` | FP&A intelligence workbook with auto-insights | 10-sheet Excel |
| `/dr-anomalies-report` | Data quality assessment | Excel report |
| `/dr-insights` | Trend analysis and executive insights | PowerPoint + Excel |
| `/dr-reconcile` | P&L vs KPI consistency validation | Excel report |
| `/dr-dashboard` | Executive KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Budget vs actual variance analysis | Excel + PowerPoint |
| `/dr-audit` | SOX compliance audit reporting | PDF + Excel |
| `/dr-departments` | Department P&L analysis | Excel + PowerPoint |
| `/dr-get-formula` | Generate Excel with DR.GET formulas | Excel workbook |
| `/dr-drilldown` | Drill into DR.GET cells | Breakdown data |
| `/dr-test` | Test API field compatibility | Diagnostic report |
| `/dr-anomalies` | Detect data anomalies | Quality findings |

## Claude Code Capabilities

The SDK agent handles all the above dynamically — no individual skills needed. It knows all SDK methods and domain knowledge (aggregation rules, DR.GET syntax, variance logic, audit framework, etc.).

Additionally available:
- `ask_ai` — freeform AI assistant (not available in Cowork)

---

## Repo Structure

```
cowork/              Cowork plugin (MCP-based)
  skills/            17 MCP-based skills
  commands/          8 Cowork commands
  agents/            8 agent definitions
  .claude-plugin/    Plugin manifest with MCP server

code/                Claude Code plugin (SDK-based)
  agents/            datarails-sdk agent (all domain knowledge embedded)
  skills/auth/       /dr-auth OAuth flow
  hooks/             SessionStart SDK verification
  settings.json      Default agent config
  .claude-plugin/    Plugin manifest (no MCP)

shared/              Shared by both
  config/            environments.json, profile-schema.json, client-profiles/
  docs/              Analysis reports, guides
```

---

## For Maintainers

### Building Cowork ZIP
```bash
cd cowork && ./build-cowork-zip.sh
```

### Keep Plugins in Sync
When adding a new capability to one plugin, consider whether it should be available in the other:
- **New Cowork skill** → check if the domain knowledge should be added to `code/agents/datarails-sdk.md`
- **New SDK method or domain rule** → check if a corresponding Cowork skill or skill update is needed
- **New shared config/docs** → put in `shared/`

---

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
