# Changelog

## [Unreleased]

## [3.0.1] — 2026-07-01

### Changed
- **Strengthened the alias→by-id fallback in every discovery-bearing skill (+ the canonical `CLAUDE.md` recipe).** A full skill-by-skill test against the live production org surfaced that a *table* alias does **not** imply its *fields* are aliased — the mapped `financials` table exposes only ~5 aliased fields out of ~185, and none of the load-bearing ones (`amount`, `scenario`, account groups, dates). The v3.0.0 "alias-first" framing is kept, but each skill's field-binding step now states explicitly that the alias/by-id choice is **per field**: resolve any un-aliased field via `get_fields_by_id` + the `*_by_id` tools (which always work), and never abandon a query because the aliased set is thin. Behavior-preserving clarification — the by-id fallback already existed; this makes it unmissable so a literal reader can't get stuck on a sparse alias surface.
- **Added a backward-compatibility "retired tool names (old → new)" mapping to `CLAUDE.md`.** So references to the previous MCP's tool names (`list_finance_tables`, `aggregate_table_data`, `get_metric_data`, `semantic_*`, …) from old workflows or user muscle memory are silently mapped to the current tools instead of being reported as missing. `/dr-*` skill/command names are unchanged, so existing invocations keep working.

## [3.0.0] — 2026-06-23

### Changed
- **Migrated every skill, agent, command, and `CLAUDE.md` to the refactored MCP tool surface.** The server consolidated to a 3-layer model and renamed/removed many tools; the plugin was calling tool names that no longer exist. Renames applied in frontmatter and prose: `list_finance_tables`→`list_data_models`, `get_table_schema`→`get_fields_by_id`, `aggregate_table_data`→`get_aggregated_data_by_alias`/`_by_id`, `get_records_by_filter`/`get_sample_records`→`get_data_by_alias`/`_by_id`, `get_field_distinct_values`→`get_distinct_values_by_alias`/`_by_id`; the dev-layer families `semantic_*`→aliased (`get_data_by_alias`, `get_aggregated_data_by_alias`, `get_distinct_values_by_alias`, `list_aliased_fields`) and `get_metric_*`/`drill_down_metric`→`get_business_metric_*` (`list_business_metrics`, `get_business_metric_details`/`_data`/`_drilled_down_data`/`_table_rows`). Removed the now-deleted `profile_table_summary` and `detect_anomalies` (anomaly/profile findings were already computed client-side from `profile_*` + aggregates) and `execute_query` (superseded by `get_data_by_*` advanced filters). The `list_metrics_by_category`/`_by_dimension`/`get_metric_dimension_matrix` helpers have no server replacement and are now done client-side over the `list_business_metrics` flat list.
- **Adopted the aliased layer as the preferred raw-data path.** Discovery is now alias-first (`list_data_models` → `list_aliased_fields` + the `*_by_alias` tools when a table has an alias, else `get_fields_by_id` + the by-id tools) — friendlier field names and ~95% fewer tokens, with a reliable by-id fallback. KPI questions start at the ungated `list_business_metrics` for discovery and compute values via aggregation. Public-facing skills/agents use only **ungated** tools; the gated `get_business_metric_*` data tools, `sql_query`, and managed-agents tools live in the `__internal` dev skills, which target the dev MCP (flags on).
- **Corrected obsolete API guidance in skill prose.** Date ranges now filter directly via **advanced** filters (`total_range`/`gte`/`lte` with epoch-second strings) — dropped the "dates must be dimensions / epoch ints rejected" workaround. Comparisons, ranges, text matching, and null checks are supported via advanced filters — dropped the "filter API is value-list only" guidance. Distinct values come from `get_distinct_values_by_*` (sample-row fallback only on error) — dropped the "distinct-values API 409s, use samples" claim.
- **`tools/public-stripped-tools.txt` rewritten to the flag-gated surface** (strips `get_business_metric_*` data, `sql_query`, managed-agents; keeps the ungated aliased layer + `list_business_metrics`), with `RELEASING.md`'s scrub section updated to the flag-based (not endpoint-based) model. A staged promotion dry-run removes 0 entries from the migrated public skills — they're already prod-safe.

## [2.9.2] — 2026-06-14

### Added
- Privacy policy reference, required by Anthropic's Software Directory Policy for any plugin that connects to a remote service or handles user data (a homepage link doesn't satisfy it). The plugin connects to the remote Datarails Finance OS MCP, so the already-published policy is now referenced in the two required spots: a `privacy` field in `.claude-plugin/plugin.json` and a **Privacy** section in `README.md`, both linking https://www.datarails.com/privacy-policy/. Shipped to the public mirror as an out-of-band hotfix (public PR #19); the change here is byte-identical, so the next promotion supersedes it cleanly.

### Fixed
- `get-formula`: generated workbooks broke in Excel because the bare `Value` token in `=DR.GET(Value, …)` resolved to nothing and Excel autocorrected it to the built-in `VALUE()` function. The skill now creates a workbook-scoped defined name `Value` (= the string constant `"Value"`) in every generated workbook, asserts it post-save along with the exact `=DR.GET(Value,` form of every formula, and documents the failure mode in Troubleshooting. Shipped to the public mirror as an out-of-band hotfix (public PR #16); the change here is byte-identical, so the next promotion supersedes it cleanly.
- Invented DR.GET dialects in non-formula skills: a client workbook generated in the field (2026-06-01) carried "live" formulas transliterated from the MCP aggregation call — `=DR.GET(Value,"financials","Amount","SUM",…)` with hardcoded filter values and raw epoch timestamps as date headers — improvised in a session where get-formula's syntax reference wasn't loaded; DR.GET authoring rules existed only inside that one skill. All nine Excel-writing skills (`extract`, `intelligence`, `insights`, `dashboard`, `departments`, `audit`, `reconciliation`, `forecast-variance`, `anomalies-report`) now inline a compact **"DR.GET Formulas — Authoring Contract"** (canonical `"[Dimension]", CellRef` pair syntax, no API-call transliteration, values via cell references, calendar EOM date serials, the `Value` defined name, bare formulas only), per the repo's inline-not-handoff doctrine. `get-formula`'s Common Mistakes table now names the transliterated-API and epoch-date-header anti-patterns. Shipped to the public mirror byte-identically (stacked on public PR #16). The block is single-sourced: canonical copy in `docs/internal/drget-authoring-contract.md`, `tools/sync-drget-authoring-contract.py --write` re-stamps every inlined copy, and CI fails the advisory job on drift.

### Changed
- Public mirror gains a one-click **Version bump** action (`tools/public-workflows/version-bump.yml`, installed on `Datarails/dr-claude-code-plugins-re`): it bumps the root `plugin.json`, commits to `main`, and pushes a `v<version>` tag via the GitHub App token, which fires the public `release.yml` to build the ZIP and publish the GitHub Release. This is the public-side equivalent of the internal `version-bump.yml`, and the release path for out-of-band hotfixes (e.g. the privacy-policy public PR #19) that the promotion-only auto-tag does not cover. Release-infra only — no change to plugin behavior.

## [2.9.1] — 2026-06-01

### Changed
- Public-promotion pipeline now strips dev-only (semantic/metrics-layer) MCP tools from each promoted skill's `allowed-tools:` and agent's `tools:` frontmatter, so the published plugin only references tools the production MCP serves. No change to plugin behavior on either surface.
- Internal-only analysis docs moved from `docs/analysis/` (and the stale `docs/guides/COMPREHENSIVE_FPA_REPORT_GUIDE.md`) into `docs/internal/`, which the publish pipeline strips — they no longer reach the public mirror. These were stale Feb-2026 dev artifacts that referenced a removed `generate_intelligence_workbook` "MCP tool", an internal production API-issues report, and real client financials. Dangling references in `CLAUDE.md`, `docs/guides/GETTING_STARTED.md`, and the two metric `__internal` skills were repointed; the bucket-end-clipping guidance in `CLAUDE.md` is now inline. `docs/guides/GETTING_STARTED.md` (the user-facing guide) stays public.

## [2.9.0] — 2026-05-27

### Changed — inline discovery replaces the profile / learn / hook machinery (BREAKING for setup flow)

Cowork (the production target for Finance OS users) runs in an isolated sandbox:
the cwd is an ephemeral per-session home, the workspace is mounted separately,
plugin command hooks don't dispatch, and cross-skill handoffs get skipped by the
planner. The centralized `./.datarails/profile.json` + `/dr-learn-v2` +
profile-gate hook approach cannot work there. Every skill and agent now
**discovers the client's financials table, fields, and account categories
inline** — self-contained, once per conversation, with no profile file and no
setup step.

**Removed:**
- `/dr-learn` and `/dr-learn-v2` skills (deleted).
- The profile-gate hook (`hooks/`) — confirmed it never executes in Cowork.
- The `./.datarails/profile.json` cache, `config/profile-schema.json`, and
  `config/client-profiles/`.

**Migrated to inline discovery:**
- Raw-tables skills: `financial-summary`, `revenue-trends`, `expense-analysis`,
  `extract`, `intelligence`, `insights`, `anomalies-report`, `get-formula`,
  `drilldown`, `test`. Each discovers the financials table (name-match, else
  largest), binds the fields it uses from the schema, and reads account-category
  values from sample records. Aggregation-field failures are handled reactively
  (retry a schema sibling) instead of a pre-probe sweep. `anomalies-report` still
  honors `--table-id` (zero discovery); `test` now **reports** the field-
  compatibility map in-conversation instead of writing it to a profile.
- Metric-v1 `__internal` skills (`financial-summary-v2`, `metric-explorer`,
  `metric-drilldown`, `semantic-query`, `cross-layer-reconcile`): Step 0 reduced
  to the silent 3-call catalog bootstrap, session-cached; disk-read + learn
  fallback dropped. `org-context` had no profile dependency (unchanged).
- Agents `anomaly-detector` and `insights`: same inline-discovery treatment.

**Docs:** `CLAUDE.md` "Client Profile Lookup Contract" → "Client Data Discovery"
standard (canonical recipes + the sandbox/hook/planner-skip rationale). `README`,
`SETUP`, `GETTING_STARTED`, `COMPREHENSIVE_FPA_REPORT_GUIDE`, and the `test-api`
command no longer instruct users to run `/dr-learn` or mention a client profile.

## [2.8.3] — 2026-05-25

### Fixed (financial-summary cold-start, take 3 — structural)

- `financial-summary` SKILL.md restructured so the profile prerequisite
  lives **above the `## Workflow` section**, not inside it. Take 2
  (v2.8.2) put the prerequisite as Step 2 inside Workflow and Claude
  still bypassed it — the planner appears to squeeze out housekeeping
  steps from the Workflow plan, leaving only data-producing steps.
- New structure:
  - `## ⚠️ Prerequisite — read before anything else` (H2 above
    Workflow): mandatory `.v1` resolution + slash-invoke of
    `/dr-learn-v2` if missing + the `.v1` field bindings.
  - `## What this skill does`: brief description (was the opening
    paragraph).
  - `## Workflow`: only 3 data-producing steps (Aggregate, Monthly
    trend, Present) — all reference the field bindings established in
    the Prerequisite section. Workflow opens with a guard:
    *"The Workflow below ASSUMES the prerequisite above completed."*
- Frontmatter `description` reworded to lead with "REQUIRES the v1
  client profile from /dr-learn-v2 (auto-invoked when missing)" so the
  catalog surface also signals the dependency loudly.

Pilot — `financial-summary` only. If this finally works in Cowork,
the same structural lift propagates to the other 9 non-metric-v1
skills.

## [2.8.2] — 2026-05-25

### Fixed (financial-summary cold-start, take 2)

- `financial-summary` Step 2 now **invokes `/dr-learn-v2` as a
  slash command** (sub-skill invocation) rather than inlining its
  workflow steps. The previous inline approach (v2.8.1) was ignored
  by Claude — the long Step 0 housekeeping block got skipped during
  initial planning, and the skill jumped straight to its old
  `Discover the schema` step, falling back to auto-discovery.
  Sub-skill invocation is a clearer, harder-to-skip imperative;
  `/dr-learn-v2` now also appears in the right-pane Skills panel
  alongside `financial-summary` (matching user expectation).
- `financial-summary` Step 3 (`Discover the schema`) **removed**.
  Replaced with `Resolve field bindings from the profile`, which
  binds `<financials_table_id>`, `<amount_field>`, `<account_field>`,
  `<scenario_field>`, `<date_field>`, and the account-hierarchy
  values from `.v1.*` — with an explicit *"Do NOT call
  get_table_schema or list_finance_tables — Step 2 guaranteed these
  values."* This removes the auto-discovery escape hatch completely.
- Steps 4–6 updated to reference the `.v1` bindings directly instead
  of abstract `<placeholder>` field names. Step 6 now uses
  `.v1.account_hierarchy.revenue` / `.cogs` / `.opex` for category
  filtering.

This is a pilot on `financial-summary` only. If user testing confirms
Claude invokes `/dr-learn-v2` and the panel shows both skills, the
same pattern (slash-invoke + removed discovery) propagates to the
other 9 non-metric-v1 skills in a follow-up.

## [2.8.1] — 2026-05-25

### Changed (legacy/production silent auto-fire)

- All ten non-metric-v1 profile-aware skills switched from
  **confirm-then-auto-fire** (or confirm-or-fallback) to **silent
  auto-fire**. Previously, when `.v1` was missing they would prompt
  *"Build via /dr-learn-v2 (~30s)? [Y/n]"* and either fire learn on
  confirmation or fall back to auto-discovery / STOP. The prompt
  let Claude legitimately skip learn, so users saw skills running
  auto-discovery without learn ever firing.
  
  New behavior: if `.v1` is missing, the skill runs the full
  `/dr-learn-v2` workflow inline without asking, surfacing only a
  brief progress note (*"Building client profile (~30s)…"*). Learn
  is now mandatory on cold-start. No fallback to auto-discovery
  without learn for these skills.
  
  Affected (10 skills):
  - **3 production user-facing:** `financial-summary`,
    `revenue-trends`, `expense-analysis`
  - **7 legacy raw-tables:** `extract`, `intelligence`, `insights`,
    `anomalies-report`, `get-formula`, `drilldown`, `test`
  
  `anomalies-report` previously had an auto-discovery fallback
  ("lone exception" in the contract); that fallback is removed for
  the profile-missing case. The skill still supports the
  `--table-id` case for non-financial tables, where v1 may not apply.
- "Client Profile Lookup Contract" in `plugins/datarails-financeos/
  CLAUDE.md` updated to describe the unified silent-auto-fire
  behavior. Both consumer families (metric-v1 silent bootstrap, v1
  silent auto-fire) are now invisible to the user on cold-start
  apart from the one-line progress note for the slower v1 path.

## [2.8.0] — 2026-05-24

### Changed (v1 unification)

- **Session-memory caching is now explicit** in the lookup contract:
  every consumer skill's Step 0 / profile-lookup first checks whether
  the profile was loaded earlier in the conversation. If yes, use it
  directly — no disk read, no bootstrap. Once loaded (from disk or
  from a fresh bootstrap), the profile stays in session context for
  the rest of the conversation.
- **Legacy consumer skills switched from STOP-on-miss to
  confirm-then-auto-fire**: when `.v1` is missing, they now prompt
  *"Build it now via /dr-learn-v2 (~30s)? [Y/n]"* and run the full
  learn-v2 workflow inline on confirmation. Previously they STOPped
  and required the user to manually run /dr-learn-v2 then re-issue
  their original command. `anomalies-report` is the lone exception:
  declining the prompt falls back to auto-discovery mode (it has a
  working profile-less path).
- All seven legacy skill `allowed-tools` widened to include the full
  learn-v2 surface so inline execution works
  (`list_semantic_tables`, `get_metric_definitions`, `get_metric_data`,
  `get_field_distinct_values`, `get_sample_records`, `Write` added
  where missing).
- Three production user-facing skills also gain the contract — they
  were initially missed because they referenced "client profile" in
  prose without hardcoding the legacy `${CLAUDE_PLUGIN_DATA}` path,
  so the initial grep skipped them:
  - `financial-summary` (production)
  - `revenue-trends`
  - `expense-analysis`
  
  These three follow the `anomalies-report` variant — **confirm-or-
  fallback** rather than confirm-or-STOP, since they all have working
  auto-discovery paths today. Declining the profile-build prompt
  proceeds in auto-discovery mode (existing behavior); confirming
  runs `/dr-learn-v2` inline. `allowed-tools` widened the same way.

- `/dr-learn-v2` expanded with a non-interactive **Phase 2 (v1 schema
  discovery)**: heuristic financials-table identification, semantic
  field-name mapping (amount/scenario/year/date/account_l0..l2/
  department), account hierarchy walking (revenue / cogs / opex via
  distinct-value sniffing), and per-field aggregation compatibility
  probes. Per-mapping `confidence` flags (`exact` / `pattern` / `guess`)
  surface heuristic uncertainty so consumer skills can warn.
- `/dr-learn-v2` now **saves by default**; pass `--no-save` to skip the
  disk write for diagnostics-only runs. The previous `--save` flag is
  the new default behavior.
- Unified profile shape: `./.datarails/profile.json` now contains both
  `.v2` (catalog) and `.v1` (heuristic schema) blocks under a single
  root with shared `captured_at`. Consumer skills reference their block.
- "Client Profile Lookup Contract" in `plugins/datarails-financeos/
  CLAUDE.md` expanded to document both family behaviors: metric-v1
  consumers do silent bootstrap (3 catalog calls); legacy v1 consumers
  ask-first with a "Run /dr-learn-v2" message on miss.
- All seven legacy raw-tables consumer skills updated to read the `.v1`
  block of `./.datarails/profile.json` (was the sandboxed
  `${CLAUDE_PLUGIN_DATA}/client-profiles/<env>.json`):
  - `extract`, `intelligence`, `insights`, `anomalies-report`,
    `get-formula`, `drilldown`, `test`
  
  Each now prompts the user to run `/dr-learn-v2` if v1 metadata is
  missing. `anomalies-report` is the lone skill that can still run
  without a profile (auto-discovery fallback) — it surfaces the gap
  once and proceeds.
- All five metric-v1 `__internal` consumer skills' Step 0 updated to
  check the `.v2` block (was `schema_version == "v2"` at root).
- Legacy `/dr-learn` skill gets a **deprecation banner** pointing at
  `/dr-learn-v2`. The body remains for users on the interactive
  field-confirmation workflow; physical removal is a follow-up.

### Changed

- **Profile cache path moved to workspace** (`./.datarails/profile.json`)
  in `skills/learn-v2__internal/`. The previous `${CLAUDE_PLUGIN_DATA}`
  location was sandboxed away from Cowork's `Write` tool, so `--save`
  silently fell back to writing the profile into the user's workspace
  with an ad-hoc filename. The new path works identically in Cowork and
  Claude Code; org-slug discovery is no longer needed.
- New **"Client Profile Lookup Contract (v2)"** section in
  `plugins/datarails-financeos/CLAUDE.md` documenting the
  read-or-silently-bootstrap pattern that every metric-v1 `__internal`
  consumer skill follows.
- All five metric-v1 `__internal` consumer skills gain a **Step 0:
  Profile lookup** housekeeping step before their workflow:
  - `metric-drilldown__internal`
  - `financial-summary-v2__internal`
  - `metric-explorer__internal`
  - `semantic-query__internal`
  - `cross-layer-reconcile__internal`

  Each silently reads the v2 profile from disk; on miss, runs the three
  learn-v2 catalog calls inline and stashes in session memory. No disk
  writes — only an explicit `/dr-learn-v2` invocation persists. Each skill's
  `allowed-tools` frontmatter widened to include the catalog tools and
  `Read`.
- Legacy `/dr-learn` (v1 schema) is **not** updated — it's slated for
  replacement by `/dr-learn-v2`. Unmigrated raw-tables skills
  (`extract`, `intelligence`, `insights`, `anomalies-report`,
  `get-formula`, `drilldown`, `test`) continue to consume the v1
  profile at `${CLAUDE_PLUGIN_DATA}/client-profiles/<env>.json` until
  they migrate.

## [2.7.0] — 2026-05-20

### Changed
- Plugin source-of-truth moved to `dr-internal-plugins` under `plugins/datarails-financeos/`. The public repo `Datarails/dr-claude-code-plugins-re` is now a published mirror — install URLs and the user-facing marketplace stay unchanged.

### Changed (MCP-alignment)

- Skills and agents updated to match the current MCP server tool
  surface (29 tools; the 12 semantic/metric tools may be flag-gated
  per org via Unleash `mcp__semantic_tools` / `mcp__metrics_tools`).
  No user-facing skill or agent depends on the gated tool groups —
  all production workflows stay end-to-end on the 15 always-available
  raw-tables tools, so flag-off orgs see no quality regression.
- `skills/query/SKILL.md` — full rewrite for the new filter API.
  Drops `>`, `<`, `IS NULL`, `LIKE`, and `--sql` mode advertising;
  documents the rejected operators explicitly with workarounds
  (aggregate-bucketing for ranges, `get_field_distinct_values` +
  IN-list for substring matches).
- `skills/anomalies/SKILL.md`, `skills/profile/SKILL.md`,
  `skills/anomalies-report/SKILL.md` — rewritten to compute outlier
  flags, severity buckets, duplicate counts, null rates,
  percentiles, and the Data Quality Score client-side from baseline
  MCP aggregates. The MCP `detect_anomalies` / `profile_*` tools
  return baseline numbers only; the skills attribute every derived
  number to its source so users can re-derive it.
- `skills/intelligence/SKILL.md` — small honesty patches: outlier
  classification is computed in-skill from the monthly P&L series,
  not returned by `detect_anomalies`.
- Broken `/dr-query` examples removed from `skills/anomalies/`,
  `skills/profile/`, `docs/guides/GETTING_STARTED.md`.
- `agents/anomaly-detector.md`, `agents/finance-analyst.md` — full
  body rewrites. Both now document the client-side compute model
  explicitly, drop `execute_query` SQL claims (the `query` arg is
  ignored by the server), and add `Bash` to anomaly-detector's tool
  list so it can actually generate Excel via openpyxl.
- `agents/insights.md`, `agents/audit.md` — light touch-ups to
  attribute outlier/exception detection to client-side computation.
- The dev-only `kpi-catalog` skill renamed to `metric-explorer`
  ("KPI" is a reserved noun inside Datarails; this skill explores
  the metrics catalog). Now lives at
  `skills/metric-explorer__internal/`.
- `__internal/` (double-underscore) convention adopted for all
  dev-only skill folders and command/agent files; `.internal/`
  (dot) was invisible in Claude Code's `/` slash menu. Skill/command
  bodies updated to self-reference the new path.

### Added

- `skills/financial-summary/`, `skills/revenue-trends/`,
  `skills/expense-analysis/` — three user-facing workflows ported
  from the legacy `commands/` files into proper skills with
  `user-invocable: true`. Each uses only raw-tables tools (backward
  compatible) and adopts the current filter API (no comparison
  operators, no date-field filters). Commands removal is deferred
  to a separate PR.
- Metric-query UX guardrails: call-shape matrix in
  `docs/analysis/FINANCE_OS_API_ISSUES_REPORT.md` (bucket-end
  clipping recipe + empty-result triage), disambiguation gate in
  `skills/metric-drilldown__internal/` and
  `skills/financial-summary-v2__internal/`, and a `CLAUDE.md`
  Critical Rule preferring the engine over client-side derivation
  (companion to MCP wrapper PR #37 on `dr-datarails-mcp-remote`).

### Added (internal-only, stripped at publish)
- Internal-surface conventions documented in `CONTRIBUTING.internal.md`:
  - `*__internal/` for dev-only skill folders, `*__internal.md` for dev-only commands/agents — double underscore so Claude Code's skill/command loader (which treats `.` as an extension separator) still discovers them on developer machines.
  - `*.internal.md` for internal-only docs (never user-invocable, dot is fine).
  Excludes added to `tools/publish-datarails-financeos.sh` cover both shapes.
- Seven dev-only skills exercising the new MCP surface (metrics-v1, semantictables-v1, utility endpoints):
  - `skills/learn-v2__internal/` — three-call profile build, replacement for the legacy 22-step `/dr-learn` ceremony
  - `skills/metric-explorer__internal/` — full metrics catalog explorer
  - `skills/metric-drilldown__internal/` — `get_metric_data` + `drill_down_metric` flow
  - `skills/financial-summary-v2__internal/` — metric-first P&L summary, A/B against legacy
  - `skills/semantic-query__internal/` — semantictables-v1 aliased queries
  - `skills/org-context__internal/` — users / FX / filebox / workflow guide
  - `skills/cross-layer-reconcile__internal/` — triangulation regression guard
- Two dev-only commands: `commands/metric-explorer__internal.md`, `commands/reconcile__internal.md`

## [2.6.1]

Imported from `Datarails/dr-claude-code-plugins-re@main`. See [GitHub Releases](https://github.com/Datarails/dr-claude-code-plugins-re/releases) on the public repo for the pre-internal-mirror history.
