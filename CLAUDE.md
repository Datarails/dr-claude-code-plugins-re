# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code plugin for Datarails Finance OS. It provides skills (`skills/*/SKILL.md`), commands (`commands/*.md`), and agents (`agents/*.md`) that connect to a remote MCP server at `https://mcp.datarails.com/mcp` (configured in `.claude-plugin/plugin.json`). There is no local server code — the MCP server is hosted remotely.

## Critical Rules

**NEVER generate reports, Excel files, or any artifacts without first fetching fresh data from the live Datarails API.** Reports with fake/placeholder data have zero value.

**NEVER hardcode client-specific information in skills or committed files.** Table IDs, field names, and account hierarchies differ per client — every skill **discovers them inline at runtime** (see "Client Data Discovery" below). Never bake them into a skill, a committed config, or a persisted profile file.

**Prefer the engine over local computation for metric values.** When `get_metric_data` returns empty for a CALC metric whose `health == "ready"`, sweep parameters (`date_end`, `aggregation_period`, `scenario`) before deriving the value from base metrics yourself. The most common cause of an empty response is bucket-end clipping — see `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` "Metrics-v1 Call-Shape Matrix" and honor the MCP `wrapper_warning` text when present. If after the sweep you still need to compute client-side as a fallback, **label it explicitly** in the user-facing output: *"derived from <bases> client-side because get_metric_data returned empty for these parameters — not the canonical engine value."* Never present a derived number as if it came from the metrics layer.

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

### Client Data Discovery

Every Datarails environment names its financials table and fields differently, so skills can't hardcode them. Each profile-aware skill **discovers what it needs inline, as the first step of its own workflow** — self-contained, with no shared profile file, no separate learn/setup command, and no hooks.

**Why inline — and not a cached profile, a `/dr-learn` dependency, or a hook (all tried, all failed):**

- **Cowork runs in an isolated sandbox** with an ephemeral per-session home (`/sessions/<name>`); the user's workspace folder is mounted but is *not* the cwd. A profile written to `./.datarails/profile.json` lands in the throwaway home and does **not** survive between sessions — a disk cache can't be relied on.
- **Plugin command hooks do not dispatch in Cowork** (confirmed across multiple builds — pure-shell probe left no trace), so harness-level enforcement of a setup step isn't available.
- **Cross-skill / cross-file handoffs get skipped** — "invoke `/dr-learn-v2` first" or "read this shared reference, then proceed" are planning steps Claude routinely optimizes away (PRs #41-44 chronicle four failed prose variants). Inlining the critical discovery in the skill's own workflow is the only reliably-executed form.

Re-discovering on each cold session is also *more correct* than risking a stale cache.

**Session-memory caching (within one conversation):** the first skill that discovers the table/fields/categories carries them forward; later skills in the same conversation reuse them. Each skill's discovery step opens with *"if you already discovered these this conversation, reuse them."*

#### Canonical inline-discovery recipes (maintainer source of truth)

When writing or updating a skill, copy the relevant recipe so heuristics stay consistent. **This doc is the source of truth; the skill inlines the recipe — do NOT make skills `Read` this file at runtime** (that's a handoff the planner skips).

**Raw-tables skills (P&L / financials):**
1. `list_finance_tables` → financials table = name matches `/financial|cube|p&?l|ledger|gl/i`, else largest by row count.
2. `get_table_schema(<id>)` → bind by case-insensitive name match: `amount` (numeric: `^amount$`→`transaction_amount`→`value`), `scenario` (`^scenario$`→`^version$`), `date` (`reporting_date`→`posting_date`→`^date$`), `account_l1` (`dr_acc_l1`→`account_l1`→`account_group_l1`). Ask the user if `amount`/`scenario` is unclear.
3. Account categories via `get_sample_records(<id>, limit=500)` (distinct-values API 409s) → `revenue` `/revenue|sales|income/i`, `cogs` `/cogs|cost of goods|cost of sales|direct cost/i`, `opex` `/operating|opex|expense|sg&a/i`.
4. **Aggregation field failures are handled reactively, not pre-probed:** if `aggregate_table_data` 500s on a dimension field, re-inspect the schema for a sibling (e.g. `DR_ACC_L1.5`) and retry. (Replaces learn-v2's slow pre-probe sweep.)

**Metric-v1 skills (`__internal`, metrics/semantic layer):**
Run the three catalog calls in parallel — `list_finance_tables`, `list_semantic_tables`, `get_metric_definitions` (~5s) — and use the result directly; cache in session. (These skills already do this; the only change is dropping the disk-read/learn fallback.)

#### Status: migration complete

Every profile-aware skill and agent now discovers inline. `/dr-learn`, `/dr-learn-v2`, the `./.datarails/profile.json` cache, and `config/profile-schema.json` have all been **removed**. There is no profile file anywhere — do not add one or reintroduce a learn/setup command. When writing a new skill, inline the recipe above; never depend on a saved profile or a sibling skill to discover for you (Cowork skips those handoffs).

### Excel Context Contract

Any skill that offers Excel-context behavior (in-sheet enrichment, agent refresh,
drill-down) **must delegate to `/dr-excel-context`** rather than implementing
Excel context detection inline. This contract applies globally; it overrides
inline logic in individual skill files.

**Three mandatory delegation points:**

| Point | When | Delegate to |
|-------|------|-------------|
| Guard | Step 0 — before any data pull | `/dr-excel-context guard` |
| Refresh | Step 0b — after guard confirms connection | `/dr-excel-context refresh` |
| Drill-down | Final step — after analysis written to sheet | `/dr-excel-context drilldown` |

**Rules enforced by the connector:**

- `agent.get_session` success is the **only** authoritative Excel context signal.
  Never infer context from user wording.
- `agent.connect_file` requires explicit user confirmation — never called
  automatically.
- `agent.refresh` is offered once per invocation and only when Excel context
  is confirmed.
- `agent.drill_down` fires only in enrichment mode (DR.GET formula cells exist).
  Cold-question mode (raw API values from `aggregate_table_data`) always skips
  drill-down.

Skills with existing inline logic: the inline logic remains valid for the demo
period. Migrate to delegation anchors during the next batch skill edit.

### Plugin Content Types

- **Skills** (`skills/*/SKILL.md`): Full-featured workflows for Claude Code. Each has frontmatter with `allowed-tools` listing which MCP tools it can use. Reference: `skills/intelligence/SKILL.md`.
- **Commands** (`commands/*.md`): Lightweight Cowork-friendly commands (no CLI dependencies).
- **Agents** (`agents/*.md`): Specialized agent definitions (finance-analyst, dashboard, audit, etc.).

### Adding a New Skill

1. Create `skills/<name>/SKILL.md` with frontmatter (name, description, allowed-tools, argument-hint)
2. Include: inline Client Data Discovery as the workflow's first data step (copy the canonical recipe above), Workflow phases, Execution Instructions, Troubleshooting
3. No registration step needed — skills are auto-discovered from the `skills/` directory

## Git Guidelines

**Commit:** Skills, commands, agents, plugin config, schemas, docs (`docs/analysis/`, `docs/guides/`), notebooks.

**Never commit:** output files (`tmp/`), credentials, `.env.local`.

## Output Files

All generated artifacts (Excel, PowerPoint, CSV, diagnostics) go to `tmp/` (gitignored).

## Authentication

OAuth 2.0 + PKCE at the MCP transport layer. No `/dr-auth` command exists — auth happens when the connector is first connected.

- **Cowork:** Install the plugin via Browse plugins > Personal tab. Auth happens automatically when the connector is first used.
- **Claude Code:** `/plugin marketplace add Datarails/dr-claude-code-plugins-re` then `/plugin install datarails-financeos@datarails-marketplace`

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Tools not available | Connect via Connectors UI. Do NOT suggest bash workarounds or mention "MCP" to Cowork users. |
| "Not authenticated" | Disconnect and reconnect via Connectors UI |
| Skill picked the wrong table/field | Skills discover the financials table + fields inline; if it guesses wrong, tell it which to use and it continues. There is no profile to build. |
| Field fails in aggregation | Skills retry a schema sibling automatically (reactive fallback). `/dr-test` reports the full field-compatibility map if you want it up front. |
| Slow extraction | Normal for pagination (~90 rec/sec). Use aggregation for summaries (~5s). |
