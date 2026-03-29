# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin for Datarails Finance OS. It provides skills (`skills/*/SKILL.md`), commands (`commands/*.md`), and agents (`agents/*.md`) that connect to a remote MCP server at `https://mcp.datarails.com/mcp` (configured in `.claude-plugin/plugin.json`). There is no local server code — the MCP server is hosted remotely.

## Critical Rules

**NEVER generate reports, Excel files, or any artifacts without first fetching fresh data from the live Datarails API.** Reports with fake/placeholder data have zero value.

**NEVER put client-specific information in CLAUDE.md or committed files.** Table IDs, field names, account hierarchies, and business logic go in `config/client-profiles/<env>.json` (gitignored). See `config/profile-schema.json` for the schema.

## Build & Release

```bash
# Bump version in plugin.json (single source of truth)
#   .claude-plugin/plugin.json  →  "version": "X.Y.Z"

# Publish release — GitHub Actions builds the ZIP automatically
git tag vX.Y.Z && git push origin main --tags
```

## Installation

**Cowork (Claude Desktop):** Browse plugins > Personal > **+** > Add marketplace from GitHub > `Datarails/dr-claude-code-plugins-re`

**Claude Code:** `/plugin marketplace add Datarails/dr-claude-code-plugins-re`

## Architecture

### Two-Tier Data Access

Read `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` before building new features.

| Tier | Method | Speed | Use When |
|------|--------|-------|----------|
| 1 | Aggregation API (async polling) | ~5 seconds | Summaries, totals, grouped data |
| 2 | Pagination (500/page) | ~10 min for 50K rows | Raw data extraction, full exports |

**Always prefer aggregation.** Fall back to pagination only when aggregation fails or raw records are needed.

### Aggregation API Gotchas

- **Date fields must be dimensions, never filters.** Date filters silently return empty results (API stores dates as epoch timestamps). Include dates as dimensions, then filter client-side.
- **Some fields fail per-client** (500 errors). The client profile tracks these in `aggregation.failed_fields` and provides alternatives in `aggregation.field_alternatives`. Run `/dr-test` to discover compatibility.
- **Distinct values API is broken** (returns 409). Use sample data instead.
- **JWT tokens expire in 5 minutes.** Auto-refreshes for aggregation; manual refresh every 20K rows for pagination.

### Client Profiles

Located at `${CLAUDE_PLUGIN_DATA}/client-profiles/<env>.json` (persistent across plugin updates). Created by `/dr-learn`, tested by `/dr-test`. Contains table IDs, field mappings, account hierarchies, and aggregation compatibility hints. Legacy profiles at `config/client-profiles/<env>.json` are also supported as fallback.

### Plugin Content Types

- **Skills** (`skills/*/SKILL.md`): Full-featured workflows for Claude Code. Each has frontmatter with `allowed-tools` listing which MCP tools it can use. Reference: `skills/intelligence/SKILL.md`.
- **Commands** (`commands/*.md`): Lightweight Cowork-friendly commands (no CLI dependencies).
- **Agents** (`agents/*.md`): Specialized agent definitions (finance-analyst, dashboard, audit, etc.).

### Adding a New Skill

1. Create `skills/<name>/SKILL.md` with frontmatter (name, description, allowed-tools, argument-hint)
2. Include: Client Profile System section, Workflow phases, Execution Instructions, Troubleshooting
3. No registration step needed — skills are auto-discovered from the `skills/` directory

## Git Guidelines

**Commit:** Skills, commands, agents, plugin config, schemas, docs (`docs/analysis/`, `docs/guides/`), notebooks.

**Never commit:** Client profiles (`config/client-profiles/*.json`), output files (`tmp/`), credentials, `.env.local`.

## Output Files

All generated artifacts (Excel, PowerPoint, CSV, diagnostics) go to `tmp/` (gitignored).

## Authentication

OAuth 2.0 + PKCE at the MCP transport layer. No `/dr-auth` command exists — auth happens when the connector is first connected.

- **Cowork:** Install the plugin via Browse plugins > Personal tab. Auth happens automatically when the connector is first used.
- **Claude Code:** `/plugin marketplace add Datarails/dr-claude-code-plugins-re` then `/plugin install Datarails-FinanceOS@datarails-marketplace`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Tools not available | Connect via Connectors UI. Do NOT suggest bash workarounds or mention "MCP" to Cowork users. |
| "Not authenticated" | Disconnect and reconnect via Connectors UI |
| "No profile found" | Run `/dr-learn` |
| Field fails in aggregation | Run `/dr-test`, check `aggregation.field_alternatives` in profile |
| Slow extraction | Normal for pagination (~90 rec/sec). Use aggregation for summaries (~5s). |
