# CLAUDE.md

This repo contains **two Datarails Finance OS plugins** for different environments:

## Repo Structure

```
cowork/          Cowork plugin (MCP-based)
  skills/        MCP-based skills that call tools directly
  commands/      Cowork-friendly commands
  agents/        Agent definitions
  .claude-plugin/plugin.json   (configures MCP server)

code/            Claude Code plugin (SDK-based)
  skills/        SDK-based skills (/dr-auth)
  agents/        datarails-sdk agent (Claude generates and runs code)
  hooks/         SessionStart hook to verify SDK is available
  settings.json  Sets datarails-sdk as default agent
  .claude-plugin/plugin.json   (no MCP server)

shared/          Shared by both plugins
  config/        environments.json, profile-schema.json, client-profiles/
  docs/          Analysis reports, operational guides
```

## Install

**Cowork:** `/plugin install Datarails-FinanceOS@datarails-marketplace`

**Claude Code:**
```bash
PYTHONPATH=~/dev/dr-datarails-sdk/python:$PYTHONPATH claude --plugin-dir ./code
```

**Local dev (Cowork):** `claude --plugin-dir ./cowork`

## Critical Rules

- **Never generate reports with fake data.** Always fetch fresh data first.
- **Never commit client-specific data.** Table IDs, field names, profiles go in `shared/config/client-profiles/` (gitignored).

## Authentication

- **Cowork plugin:** OAuth via MCP transport (automatic when connector is connected)
- **Code plugin:** `/dr-auth` skill (SDK OAuth flow, saves tokens to `~/.datarails/credentials.json`)

## Data Access

| Tier | Method | Speed | Use When |
|------|--------|-------|----------|
| 1 | Aggregation | ~5 seconds | Summaries, totals, grouped data |
| 2 | Pagination (500/page) | ~10 min for 50K rows | Raw data extraction |

**Date fields must be dimensions, never filters** (silently returns empty). See `shared/docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md`.
