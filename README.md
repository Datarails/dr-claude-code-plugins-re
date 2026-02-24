# Datarails Finance OS Plugin for Claude

Analyze financial data, detect anomalies, and generate insights directly from Claude.

## Install

### Cowork (Claude Desktop)

**Option 1: Upload ZIP (Recommended)**

1. Download the plugin ZIP from the [latest release](https://github.com/Datarails/dr-claude-code-plugins-re/releases/latest)
2. Open Claude Desktop → Cowork → Browse plugins → **Personal** tab
3. Click **+** → **Upload plugin**
4. Select the downloaded ZIP
5. Install the **Datarails Finance OS** plugin

**Option 2: Add from GitHub**

1. Open Claude Desktop → Browse plugins → **Personal** tab
2. Click **+** → **Add marketplace from GitHub**
3. Enter: `Datarails/dr-claude-code-plugins-re`
4. Install the **Datarails Finance OS** plugin

> **Note:** Option 2 may fail on some machines due to a [known SSH issue](https://github.com/anthropics/claude-code/issues/26588) in Claude Desktop. If installation fails, use Option 1 (ZIP upload) instead.

### Claude Code (Terminal)

**Option A: Install from GitHub (Recommended)**

Open Claude Code in any project and run:
```
/plugin marketplace add https://github.com/Datarails/dr-claude-code-plugins-re.git
/plugin install datarails-finance-os@datarails-marketplace
```

> **Important:** Use the full HTTPS URL (not `Datarails/dr-claude-code-plugins-re`). The shorthand format triggers SSH cloning which may fail without SSH keys configured.

This installs the plugin globally — skills are available from any project.

**Option B: Load from local directory (Development)**

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
claude --plugin-dir ./dr-claude-code-plugins-re
```

This loads the plugin for the current session only — useful for development and testing.

**Option C: Run from the plugin directory**

```bash
git clone https://github.com/Datarails/dr-claude-code-plugins-re.git
cd dr-claude-code-plugins-re
claude
```

Skills are auto-discovered from the `skills/` directory when running inside the repo.

**Managing the plugin:**
```
/plugin                    # View installed plugins, enable/disable
/plugin update             # Update to latest version
/plugin uninstall          # Remove the plugin
```

---

## Getting Started

Once installed, authenticate and explore:

```
/dr-auth                               # Connect via OAuth (opens browser)
/dr-tables                             # List available tables
/dr-learn                              # Create client profile (first time)
/dr-intelligence --year 2025           # Generate FP&A intelligence workbook
```

New here? Follow the **[Getting Started Guide](docs/guides/GETTING_STARTED.md)** for a hands-on walkthrough (~15 minutes).

---

## Skills

### Data Access & Setup
| Skill | Description |
|-------|-------------|
| `/dr-auth` | Authenticate with Datarails |
| `/dr-learn` | Discover table structure and create client profile |
| `/dr-tables` | List and explore tables |
| `/dr-profile` | Profile field statistics |
| `/dr-query` | Query and filter records |
| `/dr-extract` | Extract financial data to Excel |

### Financial Analysis
| Skill | Description | Output |
|-------|-------------|--------|
| `/dr-intelligence` | **Most powerful** - FP&A intelligence workbook with auto-insights | 10-sheet Excel |
| `/dr-anomalies-report` | Data quality assessment with anomaly detection | Excel report |
| `/dr-insights` | Trend analysis and executive insights | PowerPoint + Excel |
| `/dr-reconcile` | P&L vs KPI consistency validation | Excel report |
| `/dr-dashboard` | Executive KPI monitoring | Excel + PowerPoint |
| `/dr-forecast-variance` | Budget vs actual variance analysis | Excel + PowerPoint |
| `/dr-audit` | SOX compliance audit reporting | PDF + Excel |
| `/dr-departments` | Department P&L analysis | Excel + PowerPoint |
| `/dr-get-formula` | Generate Excel with DR.GET formulas | Excel workbook |

### /dr-intelligence (Most Powerful)

```
/dr-intelligence --year 2025                    # Full intelligence workbook
```

**10 Sheets Generated:**
1. Insights Dashboard - Top 5 findings with severity
2. Expense Deep Dive - Top 20 accounts, % of total
3. Variance Waterfall - What changed and why
4. Trend Analysis - 12-month trends
5. Anomaly Report - Auto-detected outliers
6. Vendor Analysis - Top vendors, concentration risk
7. SaaS Metrics - ARR, LTV, CAC, Efficiency
8. Sales Performance - Rep leaderboard
9. Cost Center P&L - Department detail
10. Raw Data - Pivot-ready for analysis

---

## Authentication

Uses **OAuth 2.0 + PKCE** — a browser window opens automatically for secure login. Environment is selected during login.

```
/dr-auth                    # Connect (opens browser)
/dr-auth --env dev          # Connect to dev auth server
/dr-auth --disable          # Disconnect
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Not authenticated" | Run `/dr-auth` (opens browser for OAuth login) |
| Need different environment | `/dr-auth --disable` then `/dr-auth --env <env>` |
| "No profile found" | Run `/dr-learn` first |
| Skills not showing | Restart Claude Desktop / Claude Code |
| Slow extraction | Normal for raw data (~90 rec/sec). Summaries use aggregation (~5s) |

See [SETUP.md](SETUP.md) for detailed setup and troubleshooting.

---

## For Maintainers

### Publishing Updates

```bash
git tag v1.4.0
git push origin main --tags
# GitHub Actions builds the release ZIP automatically
```

### Building Cowork ZIP Manually

```bash
./build-cowork-zip.sh
# Upload via Cowork → Browse plugins → Upload plugin
```

---

## License

MIT License - see LICENSE file.

## Support

- GitHub Issues: https://github.com/Datarails/dr-claude-code-plugins-re/issues
- Datarails Support: support@datarails.com
