# Changelog

## [Unreleased]

## [3.3.1] — 2026-08-09

### Fixed
- Removed the retired `version:` key from `datarails-excel-agent__internal`'s
  frontmatter (gatekeeper rubric F6) — the plugin version lives in
  `.claude-plugin/plugin.json` only. The add-in compatibility keys
  (`addinSchemaVersion`, `matchedAddinVersions`) are unaffected.
- **Adopted the post-fix aggregation contract — v3.3.0 referenced a response row that no longer exists, 35 times across 15 files.** [DR-51604](https://datarailsteam.atlassian.net/browse/DR-51604) was fixed server-side on 2026-08-06 (the FinanceOS gateway had been sending `include_totals: True`, inherited from a captured dashboards-UI request; it now sends `False`). Aggregate responses therefore return **exactly one row per requested group** — no subtotal levels, and **no keyless grand-total row either**. **Verified live 2026-08-09** across `_by_id` at 1, 2 and 3 dimensions and `_by_alias` at 2 dimensions — each probe using a **fresh cache key**, since `include_totals` is not part of the server's widget-editor cache key and re-running the original repro would have returned the pre-fix shape and produced a confident false negative. The shared data-scope preamble (item 4, byte-identical in all 14 carriers) now states that contract: every row is a real group, a total is obtained by **summing the rows**, and `[null]` is a real group rather than a total.
- **Repaired three checks that depended on the removed grand-total row** — these broke the moment the platform deployed, and were live in shipped v3.3.0. `reconciliation` Check 4 instructed comparing *"the two keyless rows"* across two slicings, which cannot run at all now; it compares summed totals of the two slicings instead, which preserves the independence (it came from slicing the same window two ways, never from a server-provided total). `anomalies` used the keyless row as its total-rows denominator for the rare-value threshold, and `anomalies-report` for its null rate — both now sum the group counts client-side. The other 30 references, which merely told skills to *drop* a row that is no longer returned, were rewritten to the new contract rather than left as confusing no-ops.
- **Told the multi-dimensional pulls to aggregate to their intended grain before time-series math** (`financial-summary`, `intelligence`). Both fetch with two dimensions — `[date, account]` and `[account_l1, month]` respectively — so a returned row is a *(month × account)* group, not a time-series point. Neither skill said to sum by month first, so the trend step could pick a single account as the "peak month", repeat months in MoM/YoY deltas, and compare different accounts as adjacent periods. Both now aggregate to the intended grain (month for company-level trends, group + month for per-account/per-department) before computing direction, peak, deltas, or the σ anomaly rule, keeping the `[null]` date bucket separate.
- **Both anomaly skills normalize GROUP BY rows once, up front.** `anomalies` builds a single `valid_rows` collection (every requested dimension key present, genuine `[null]` preserved) that all recipes then run on, and `anomalies-report` does the same before applying the borrowed recipes — otherwise a stale roll-up row inflates the missing-value denominator, always satisfies `COUNT > 1` for duplicate detection, and shifts rare-category thresholds.
- **Kept the defensive row filter, but time-boxed and explained it.** `include_totals` is not part of the server's widget-editor cache key and entries live ~7 days, so a query cached before the fix can still return the legacy shape. The preamble keeps "retain only rows in which every requested dimension key is present" as a **transitional guard through ~2026-08-13**, noting it is a no-op on a correct response — a roll-up row *omits* keys, whereas a genuine null is *present* as `[null]`.
- **Corrected the DR-48411 guidance and its attribution.** Three skills had been instructing users to *expect wrong numbers*: `metric-drilldown__internal` treated a 0.500 drill/headline ratio as normal, `financial-summary-v2__internal` appended a blanket "absolute dollar values may be 2× the truth" caveat, and `cross-layer-reconcile__internal` read "exactly 2.000×" as a confirmed engine doubling. DR-48411 is **fixed and closed**, and its cause was duplicate `Posting Date` field ids on one template inflating `/metrics/v1/data` — *not* the roll-up rows, as this plugin previously speculated. DR-48411 itself was confirmed non-reproducing on **2026-08-05** — that probe predates the 2026-08-06 aggregate fix and is unaffected by it, because the metrics endpoints run on a different engine (`/internal/insights/v2/*`) which DR-51604 explicitly did not touch. Expectation is now ~1.000, with the three false-alarm modes documented from live probes: a scenario-scope mismatch reads **0.537**, a truncated drill response reads arbitrarily low (a CALC probe returned 130 of 2,472 rows → **0.168**), and an aggregation leg retaining legacy roll-up rows reads exactly **2.000×**. Carries DR-51604's triage rule verbatim: *a 2× on a 2-dimension aggregate was roll-up rows; a 2× on `/metrics/v1/data` was the duplicate-field join — same number, different causes.*

## [3.3.0] — 2026-08-05

### Changed (duplication-audit identity & routing sweep)
- **Every `*__internal` component's frontmatter `name:` now carries the `__internal` marker, and every description opens with a `Dev-only … (stripped at publish)` clause** (audit M14/H7/H9/M30 + RELEASING.md policy reversal). The publish pipeline strips by directory, but three real egress paths (account-level skill uploads, local directory marketplaces, desktop-app uploads) discard the folder name and keep only the frontmatter `name:` — under the old "name stays clean" rule that distributed dev-only skills under production-looking identities. Renamed: `dr-financial-summary-v2`→`financial-summary-v2__internal`, `dr-metric-drilldown`→`metric-drilldown__internal`, `dr-metric-explorer`→`metric-explorer__internal`, `dr-org-context`→`org-context__internal`, `dr-excel-context`→`excel-context__internal`, `dr-cross-layer-reconcile`→`cross-layer-reconcile__internal`, `datarails-excel-agent`→`datarails-excel-agent__internal`. `financial-summary-v2`'s description no longer opens "Same shape as /dr-financial-summary" (an instruction to the selector to treat a 2×-caveated dev harness as interchangeable with production); `metric-drilldown` now states it starts from a catalog metric, not a workbook cell; `excel-context` is now `user-invocable: false` and describes itself as a connector other skills delegate to (it advertised direct invocation for an operation whose `--rows` parameter only a calling skill could fill). `commands/reconcile__internal.md` renamed to `layer-drift__internal.md` so the bare "reconcile" stem stops fanning out.
- **The four report generators' descriptions now lead with artifact + period scope** (audit H8) — previously three of four said "executive"+"Generate"+mixed deliverables while their period scopes silently differed by 12×: `dashboard` = ONE-MONTH KPI snapshot (Excel + 1-slide PPT); `insights` = FULL-FISCAL-YEAR narrative deck; `intelligence` = FULL-FISCAL-YEAR 10-sheet Excel workbook, no PowerPoint (superlative "most powerful" deleted — pure selection bias); `extract` = RAW FULL-YEAR 4-sheet export, no analysis. Each names the right sibling for the other jobs.
- **`tables` vs `profile` vs `anomalies` vs `anomalies-report` split on the question asked, and every baseline is now declared** (audit H10/M10/M11): `tables` = SCHEMA, and its quick-overview bullet now requires an explicit business-dimension `fields` list for `profile_categorical_fields` (called bare, the tool profiles upload/mapping metadata columns and silently drops fields beyond 5 — `tables` was the one call site missing the guard); `profile` = whole-history STATISTICS, with a new note that its outlier bands are unscoped while `anomalies` scopes the same band to the latest fiscal year; `anomalies` = chat-only, fiscal-year-scoped; `anomalies-report` = Excel workbook over an ALL-TIME baseline **by design**, now stated in the description, at the borrowed-recipes pointer, and in the period-scope note, so its counts are never expected to match `/dr-anomalies`.
- **`audit`'s reconciliation/mapping contradiction resolved** (audit M12): check family 2 runs `/dr-reconcile`'s four checks as specified there (single method source) and owns the roll-up pass/fail; family 3 explicitly reuses the roll-up mechanics with the same parameters/tolerance but reports only the unmapped-account exception list — the file no longer simultaneously forbids and performs an inline re-derivation.
- **`reconciliation` vs `cross-layer-reconcile__internal` carry reciprocal negative scope clauses** (audit M30/M31): whole-period four-family workbook vs single-metric three-layer engine-drift guard.
- **The Step-0 catalog fan-out no longer instructs an impossible call** (audit L3): `financial-summary-v2__internal`, `metric-explorer__internal`, and the CLAUDE.md discovery recipe all listed bare `list_aliased_fields` in a parallel fan-out — `alias` is a required argument, so that call fails validation every time. All three now fan out `list_data_models(has_alias=true)` + `list_business_metrics` and defer `list_aliased_fields` until a table's alias is known.
- **The four command launchers hand off by addressable slug** (audit L9) — `datarails-financeos:forecast-variance` / `:anomalies` / `:tables` / `:test` instead of `dr-*` display names (which are not invocation handles and, for near-prefix pairs like `dr-anomalies`/`dr-anomalies-report`, ambiguous).

### Removed
- **Deleted all 8 agents (`agents/*.md`) — they were 1:1 mirrors of same-named skills, and the agents were the weaker copies** (duplication-audit findings H12/H13/H14/M13/L10). Five shared a byte-identical 21-tool allowlist and restated their skill's description in permuted word order with no discriminator; `reconciliation` promised an Excel report with no `Bash` (openpyxl could never run); `forecast` had no `execute_office_js`, so it structurally couldn't honor the Excel-context contract, and defined its own variance bands the maintained skill deliberately doesn't; `anomaly-detector` copied the anomalies skills' scoring while dropping the two numeric severity thresholds — same weighted formula, different Data Quality Score run to run. The skills remain the single source of every workflow's guards; autonomous sweeps delegate to a general-purpose agent that runs the skill. The one unique agent behavior worth keeping (nothing else was) was dropped deliberately: the forecast agent's variance bands, which the runtime-discovering skill never defined.
- **Deleted `commands/metric-explorer__internal.md`** — it claimed the same `datarails-financeos:metric-explorer__internal` handle as the skill directory and shadowed it, and its only instruction pointed at a non-addressable handle, making the skill's 130-line workflow unreachable (audit H11). Its one unique bit — the `--category` fallback guess — moved into the skill's Workflow. The skill is `user-invocable: true`, so nothing is lost.
- **Deleted `skills/semantic-query__internal/`** — `dr-query` already prefers the alias path and subsumes it, and its body mandated a by-id fallback its own alias-only `allowed-tools` forbade, so on thin-alias orgs it had to either violate its own instruction or stall (audit M9).

### Changed
- **`excel-context__internal` aligned with the excel-agent bootstrap design — the static command catalog is gone.** The skill predates the `f3d5b2c` dynamic-bootstrap redesign (both were authored 2026-05-27/28, but only the excel-agent was migrated) and still carried a May-era static snapshot of the command catalog: per-command parameter tables, hardcoded `timeoutMs` values, the `list_functions` pagination contract with pseudocode, and per-platform notes — exactly the drift class the bootstrap eliminated by fetching the operating manual from the running add-in (`agent.get_skill`), and the skill never even mentioned `get_skill` (its only staleness defense was `agent.list_commands`, an existence check that can't catch a changed parameter or timeout). Slimmed to what the bootstrap deliberately doesn't cover: context detection (guard), the four integration patterns/anchors, and a **financial-intent → command-NAME routing table** — with an explicit doctrine block: fetch the manual via `agent.get_skill` before issuing commands, and on any disagreement the manual wins. The mutating-command confirmation rule stays (the known five as a minimum set, the manual's marking authoritative); the misleading "reference implementation" pointer at `forecast-variance` (which inlines rather than delegates — audit L12, still open) is replaced by naming the Anchor blocks as the reference integration.

## [3.2.0] — 2026-08-03

### Changed
- **DR-51147: documented the to-go `aggregation_type` values (`MTG`/`QTG`/`YTG`) + DR-50860 dynamic-metric flags across the metrics-layer surface, and aligned the docs with the DR-51364 aggregation guardrails.** The Call-Shape Matrix (`docs/internal/FINANCE_OS_API_ISSUES_REPORT.md`) now covers all 7 `aggregation_type` values with a new "To-go semantics" section settled from engine source: to-go is a **window-bounded reverse running total inclusive of the row's own bucket** (NOT the arithmetic complement of to-date — `YTD(M) + YTG(M) = full-year + value(M)`), so for "remaining to period end" the `date_end` must be the **fiscal period END** — the exact opposite of the to-date `end_of_month(today)` rounding rule; day-grain `MTG` collapses to one row per month; `get_business_metric_table_rows` honors the knob for CALC metrics only; to-go rows keep bucket-end stamps like to-date. `metric-drilldown__internal` and `financial-summary-v2__internal` now **actually wire `aggregation_type` into their `get_business_metric_data` calls** (both previously asked MTD/QTD/YTD disambiguation questions but never passed the parameter — a silent no-op), add to-go intent rows ("remaining"/"left to spend" → plan-scenario confirmation + period-end window), and enforce the dynamic-metric flags from `list_business_metrics` (`unsupported_grains[]` → never request a listed grain as `aggregation_period`, the platform rejects with `INVALID_PARAMS`; `uses_dynamic_time_units: true` → values are window-dependent, never reuse/compare across windows, always label the window). `CLAUDE.md`'s aggregation notes and the report's raw-aggregation section now state the DR-51364 server-enforced guardrails: dates in ordered filter conditions (`gt`/`gte`/`lt`/`lte`/`range`/`total_range`) must be **epoch seconds** (calendar strings are rejected), a field may not appear in both `dimensions` and `metrics`, one aggregation per field per call, and SUM/AVG are rejected on Text fields — with each guardrail's **observed** failure mode recorded, since the 422-vs-500 split turns out to be per guardrail rather than per build generation. **Live-verified 2026-08-03** against org `datarails-financials.com`: the engine-source to-go model reproduced exactly (window-bounding, inclusive-of-own-bucket, and `YTD(M) + YTG(M) = full-year + value(M)` to the cent), and three findings were added that the engine read alone did not surface — to-go payloads arrive in **descending** date order (so pick a bucket by matching its `date`, never by position); day-grain `MTG` collapses to a row stamped at the month's **earliest in-window day** carrying the whole-month total (it looks like an ordinary daily row); and **`time_aggregation: EOP` metrics ignore `aggregation_type` entirely and silently**, returning plain `DEFAULT` values for `YTD`/`YTG` alike — which both skills now guard: `financial-summary-v2__internal` **partitions the lineup by `time_aggregation` before fetching** (flow metrics carry the requested type; `EOP` metrics go out in a separate `DEFAULT` call, labelled "period-end balance"), so a mixed batch — where one `EOP` line is visually indistinguishable from the running totals around it — never goes out at all. `metric-drilldown__internal` additionally scopes its **drilldown window to the reported to-go bucket** (bucket start → fiscal period end) rather than the Step-2 request window, since a to-go headline covers only one bucket forward while the request window spans every earlier bucket too; the cross-layer sanity ratio now states that both legs must share a span and says to omit the ratio rather than show a mismatched one. Relatedly, the retired `/tables/v1` polling snapshot in the report is now explicitly marked historical (headings, code docstring, and a pointer to the current `start_aggregation_by_*` / `get_aggregation_result_by_*` contract) so its example can no longer be mistaken for current guidance. Still unexercised: the `unsupported_grains` → `INVALID_PARAMS` rejection (all 70 metrics in the org report no dynamic time units and no unsupported grains), so that rule is documented from the tool contract rather than observed. The report's fiscal-year note is deliberately untouched pending the open fiscal-threading question.
- **`datarails-excel-agent` bootstrap listener-liveness is now transport-generic (COM + Flex).** `checkListenerAlive` previously assumed Excel-for-web / a task pane and treated a heartbeat cell that exists but was never stamped as "detached" — a false negative on the COM/desktop add-in before the first command (COM only heartbeats a workbook it is actively driving, so `dr_agent_listener_heartbeat` is present-but-empty until then), which told users to "reopen the task pane" that desktop has none of. The check now returns a discriminated `state` (`unsupported` / `unstamped` / `stale` / `alive`) instead of booleans, and the rules **defer** the fail-fast rather than removing it: `unstamped` proceeds before the first command (COM-normal) but, if a row is still `queued`/empty and still `unstamped` past ~6 s, escalates to the stalled-listener message — so a genuinely dead/not-loaded add-in (never stamps H1) can no longer trigger an unbounded blind wait. `stale` blocks; `running` rows never re-check liveness (a long single-threaded command legitimately shows a stale heartbeat). Stalled-listener message reworded transport-agnostically (web → reopen task pane; desktop → ensure the add-in is enabled / Excel isn't on a modal dialog). Skill version 2.0 → 2.1. Pairs with sync-server's COM agent-bridge hardening.

## [3.1.0] — 2026-07-13

### Changed
- **`datarails-excel-agent` dynamic bootstrap + Excel-context routing + listener-liveness heartbeat now actually ship.** These landed on `main` via #272 **after** `v3.0.6` was cut, so no released tag carried them yet — the `[3.0.4]` entry below was written ahead of the merge. This release is the one that ships: the dynamic `__internal` bootstrap (command catalog loaded at runtime from the add-in's live `agent.get_skill`, so it can't drift from the shipped add-in), the bridge-vs-connector **route-by-target** fix, and the heartbeat guard that fails fast when the add-in's bridge listener detaches. Requires an add-in build with the `agent.get_skill` handler + `dr_agent_listener_heartbeat` cell; older add-ins fall back to the compact static catalog + legacy waits (no regression). Stays `__internal` (internal marketplace only). Wire schema unchanged (`1.0`, additive).

## [3.0.6] — 2026-07-13

### Changed
- **README rewrite — corrected the skill invocation format (was broken) + external-view cleanup.** The README told users to invoke skills as `/dr-<name>` (the frontmatter `name`), but Claude Code invokes a plugin skill/command by **`/<plugin>:<folder-or-filename>`** and ignores the frontmatter `name` (confirmed against the Claude Code Skills/Plugins docs). So every documented `/dr-*` command was non-resolving — e.g. it's `/datarails-financeos:tables`, not `/dr-tables`, and `/datarails-financeos:reconciliation` (folder), not `/dr-reconcile` (name). Rewrote the whole README to use the correct namespaced form throughout, led usage with natural-language invocation (Claude auto-selects the skill/agent), added a `datarails-financeos:` + Tab autocomplete tip, and made the skill list exhaustive (all 19, grouped) and consistent with the shipped honest-scoping (audit = not-SOX, reconcile = pipeline-consistency, forecast-variance = runtime-discovered scenarios, query = advanced filters, drilldown = no-file mode). Also removed the "For Maintainers" section (it named the internal repo `dr-internal-plugins` and `RELEASING.md` in the public mirror), refreshed `--year` examples to 2026, corrected the intelligence output label to "up to 10 sheets", and added an Agents section. Shipped to the public mirror as an out-of-band README hotfix (same content), so the next promotion supersedes it cleanly.
- **Applied the same invocation fix to `SETUP.md` and `docs/guides/GETTING_STARTED.md`** — every `/dr-*` command → the correct `/datarails-financeos:<folder>` form (folder names, so `reconcile`→`reconciliation`, etc.), `--year 2025` examples → `2026`, and the SETUP audit row's "(SOX-oriented reports)" → "(not a SOX certification)". The public repo README already carries the fix via hotfix; SETUP/GETTING_STARTED reach public on the next promotion.
- **Removed four redundant command launchers that collided with same-named skills.** `commands/{drilldown,financial-summary,expense-analysis,revenue-trends}.md` shared a folder/filename with a skill, so both registered the *same* slash (e.g. `/datarails-financeos:drilldown`) — an ambiguous double-registration left over from the S11 launcher consolidation. Deleted them; the identically-named skills remain the sole resolvers (same slash, full recipe). The four distinct launchers that map to a differently-named skill stay: `explore-tables`→`tables`, `data-check`→`anomalies`, `budget-comparison`→`forecast-variance`, `test-api`→`test`.

## [3.0.5] — 2026-07-12

### Changed
- **Migrated every skill/agent to the DR-50141 async fetch tools + truncation-envelope handling (DR-50494).** The MCP server replaced the four blocking fetch tools with async start→poll pairs (`start_aggregation_by_id`/`_by_alias` → `get_aggregation_result_by_id`/`_by_alias`; `start_distinct_values_by_id`/`_by_alias` → `get_distinct_values_result_by_id`/`_by_alias`) and hid the blocking tools from the tool list (still callable). This release aligns the whole plugin surface (~130 call sites across 19 public skills, 8 agents, 3 internal skills, 1 internal command, and `CLAUDE.md`):
  - **New canonical "Async fetch — start → poll" block** in `CLAUDE.md`, inlined verbatim into every fetching skill/agent (29 files): `start_*` takes the same arguments as its blocking twin and returns `{status: "pending", handle}`; echo the handle to the matching result tool; `status: "running"` + `retry_after_seconds` means poll again (not an error); distinct-values `limit` moves to the result tool; expired-handle errors restart with `start_*`. Includes a **transitional fallback** — if the `start_*` tools aren't on the connector yet (older server), the blocking twins still work with the same arguments — so the plugin behaves correctly on both sides of the MCP prod deploy, whichever lands first. The deprecated tool names stay in each frontmatter allow-list (after the new pairs) for the same reason.
  - **Data-scope preamble v2** (13 files, byte-verbatim): item 1 now names the async distinct-values pair, and a new **item 5 — Truncated results** teaches the `{data, truncated: true, total_rows, returned_rows, guidance}` envelope (server caps serialized results at ~100 KB): the `data` prefix is incomplete — never compute totals/shares/trends from it; follow the `guidance` (narrow the query or use a business metric) and re-fetch. Standalone truncation blockquotes added to `profile`, `get-formula`, and `anomalies-report` (no full preamble there), and row-fetch truncation sentences to `query`/`extract`/`drilldown`/`tables` (whose `get_data_by_*` reads can also return the envelope).
  - **`CLAUDE.md`** data-access-layer table, aggregation-vs-pagination note, discovery recipe steps 3–4, and distinct-values API note rewritten to the async pairs; a "Deprecated blocking tools (v3.1, async migration)" mapping table added to the backward-compat section so references to the old names are silently mapped, never reported as missing.
  - `reconciliation`'s cross-endpoint agreement check now runs both legs as start→poll (aliased vs by-id families — the independence argument is unchanged); `test`'s per-field probes and `cross-layer-reconcile__internal`'s aliased/raw legs migrated the same way. Tools that didn't change (`get_data_by_*`, `get_fields_by_id`, `list_*`, `profile_*`, `get_business_metric_*`) were left untouched.

## [3.0.4] — 2026-07-05

### Changed
- **`datarails-excel-agent` converted to a dynamic bootstrap — the command catalog now loads from the add-in at runtime.** The skill was a ~380-line static file whose hand-maintained §5 catalog had drifted from the shipped Flex add-in: it listed commands Flex never implements (`agent.evaluate_drget`, `agent.get_connection_info`, `create_dynamic_range`, `agent.list_dynamic_ranges`/`_schemas` → wasted `unknown_command` cycles), was missing `agent.list_function_definitions` (which Flex does implement), and its send snippet required `dr_agent_seq` (F1) — a named range Flex never creates, so the documented first send threw `ItemNotFound` on a Flex-fresh workbook. It is now a ~110-line bootstrap: transport essentials (sheet layout, F1-tolerant send snippet, poll rules, cancel) + a "first action: fetch `agent.get_skill`, cache, follow" step. The full operating manual (catalog generated from the add-in's live capability descriptor + rules) ships **inside the add-in** and is served over the bridge, so it can never drift again. Fallback path (compact union catalog + the four always-apply safety rules) triggers deterministically on `unknown_command` for older Flex builds and the COM/desktop track until they implement `agent.get_skill`. Requires add-in build with the `agent.get_skill` handler; wire schema unchanged (`1.0`, additive).
- **Bridge listener-liveness (heartbeat) guard added to the `datarails-excel-agent` bootstrap.** On Excel-for-web the add-in's bridge listener can silently detach mid-session (task-pane suspend / co-authoring recovery) and stop draining the bridge — every request then sits at `queued` and the caller busy-waits its whole ~90 s execution budget blind, with no signal (the single worst failure mode observed in live testing). Paired with a new add-in-side heartbeat (the listener writes `dr_agent_listener_heartbeat`!H1 roughly every 2 s), the bootstrap now reads it before the first command and re-checks during the outbox poll: a **present-but-stale** heartbeat (> ~6 s old) means the listener detached → the skill stops and tells the user to reopen the Datarails add-in task pane instead of hanging; an **absent** cell means an older add-in without the feature → the skill falls back to the legacy §3 waits (no regression). Requires the add-in build that writes the heartbeat; wire schema unchanged (`1.0`, additive).
- **Excel-context routing fix — bridge vs MCP connector split by target, not by whether Excel is open.** In a live Excel session, org-data questions ("list my dr models", aggregations, distinct values) were being routed to the `__dr_agent` bridge — which only exposes workbook-scoped commands — instead of the `datarails-finance-os` MCP connector, forcing users to explicitly ask for the connector. The `CLAUDE.md` Excel Context Contract said the connector was "only for server-side data pulls when there is no Excel context"; that sentence is replaced with a **route-by-target** rule (bridge acts on the open workbook; connector answers org-data questions **even while a workbook is open**), backed by a decision table + tie-breakers (near-miss pair called out: "list functions in this workbook" = bridge `agent.list_functions` vs "list my Datarails models" = connector `list_data_models`). Over-correction guardrail added so refresh/drill/insert/publish/connect/submit never leak to the connector. The `datarails-excel-agent__internal` description clause and the `dr-tables` / `explore-tables` descriptions were updated to match. Also: the send-request snippet now sets `clientTimestamp` via `new Date().toISOString()` (was a literal) so round-trip latency is measurable.
- **Documentation refresh — aligned all docs to the shipped v3.0.3 reality.** A doc audit found most docs lagged the v3.0.x tool migration, honest-scoping, and launcher-consolidation passes; several stale claims shipped in the public release. Fixes:
  - **Public front door (`README.md`, `docs/guides/GETTING_STARTED.md`, `SETUP.md`):** `/dr-audit` re-described as an audit-support evidence package (was "SOX compliance audit"); `/dr-intelligence` SaaS/vendor/sales sheets marked conditional (only when the org's data sources them); `/dr-reconcile` re-described as independent-source pipeline-consistency checks; `/dr-query` noted to support advanced filters; `/dr-drilldown` noted to support no-file intake; the bundled-connector flow replaced the wrong `claude mcp add datarails-mcp` instruction everywhere; GETTING_STARTED's ~13 wrong `/datarails-finance-os:*` command namespaces corrected to `/datarails-financeos:*`, its "environment profile" Step 4 reframed as an optional compatibility check (no profiles exist), and its Claude Code examples pointed at the real dedicated skills; example-org timing figures generalized.
  - **`RELEASING.md`:** documented the current release endgame — the public auto-tag GitHub App is not installed (auto-tag has failed on v3.0.1/v3.0.2/v3.0.3), so the maintainer must manually create the `v<version>` tag on the merge commit (exact `gh api` command included); bootstrap items 1–2 marked OUTSTANDING; the public hotfix Version-bump path flagged as blocked by the same App gap; `__internal` naming added to the strip convention.
  - **`CONTRIBUTING.internal.md` / `DEV_MCP.internal.md`:** promotion described as an explicit two-stage flow pointing at RELEASING.md (was "tag push auto-syncs"); "don't self-bump plugin.json" note added; the two MCP servers described as one codebase differing by feature flags; "dev users" audience wording corrected to external/marketplace.
  - **`docs/internal/FINANCE_OS_API_ISSUES_REPORT.md`:** added a status header separating the historical Feb-2026 raw-API snapshot from the current-canonical Call-Shape Matrix; corrected the **`wrapper_warning` clipping-hint claim** (no such hint exists on the live surface — callers detect bucket-end clipping themselves) and propagated that fix into the `financial-summary-v2__internal` and `metric-drilldown__internal` skills that repeated it; marked distinct-values RESOLVED, token expiry MITIGATED, async-polling/field-name request shape retired, and the single-org field list flagged.
  - **Deleted four obsolete internal docs** (`FPA_IMPLEMENTATION_SUMMARY`, `COMPREHENSIVE_FPA_REPORT_GUIDE`, `DATA_EXTRACTION_STRATEGY`, `TABLE_STRUCTURE_ANALYSIS`) — Feb-2026 artifacts describing a removed MCP tool, a nonexistent script, and the retired client-profile system, and holding real example-org financials; nothing referenced them and git history preserves them.

## [3.0.3] — 2026-07-05

### Changed
- **Analytical-fidelity (P0) pass across the public surface** — driven by the 45-item live-prod audit (2026-07-02): tool references were clean, but a handful of data-model assumptions recurred across skills and produced misleading or empty output. All fixes are runtime-discovery based (nothing org-specific is hardcoded):
  - **Canonical "Data-scope preamble" added to `CLAUDE.md`** and inlined verbatim into every aggregating skill (`financial-summary`, `expense-analysis`, `revenue-trends`, `insights`, `intelligence`, `extract`, `anomalies`, `forecast-variance`, `departments`, `dashboard`, `audit`, `reconciliation`): (1) discover the scenario domain — never assume a `Budget` scenario exists; route budget/plan asks to a discovered planning-version-like field; (2) discover the account grain — pick the hierarchy level whose values partition P&L flows (the top level is often the balance-sheet equation, so binding P&L categories there misclassifies — e.g. expense-analysis previously reported ASSET/LIABILITY/EQUITY as "top expenses"); (3) default every P&L question to the latest complete fiscal year / trailing 12 closed months and **label every output with period + scenario** (previously unscoped all-time totals over multi-year stock+flow tables); (4) read GROUP BY responses correctly — nulls arrive as an explicit `[null]` bucket and every response appends a keyless grand-total row that must be excluded from sums/trends/shares (previously computed ~100% null rates and phantom trend periods).
  - **Canonical "KPI honesty" rule added to `CLAUDE.md`** and inlined into the KPI-rendering skills/agents (`dashboard`, `insights`, `extract`, `intelligence`, revenue-trends' KPI context, dashboard/insights agents): render only KPIs sourceable from the discovered metric catalog or derivable from the P&L grain; SaaS metrics (ARR/MRR/churn/LTV/CAC/burn/runway/NRR) are not derivable from a P&L table and are omitted rather than fabricated or left as placeholders.
  - **`reconciliation` engine replaced** (was circular — both "sides" derived from the same aggregate, so every line reconciled to 0% by construction). Now four **independent-source** checks: cross-endpoint agreement (aliased vs by-id API families, skipped honestly when per-field alias coverage is thin), balance-sheet identity (|A| vs |L+E| per period at the discovered balance-sheet grain, sign convention discovered), cross-grain roll-up (P&L-grain buckets must sum to their parent bucket), and scenario/period integrity (group rows vs the keyless grand-total checksum). Reframed honestly as data-pipeline & mapping consistency checks, not source-system reconciliation; `reconciliation` agent aligned.
  - **`forecast-variance` de-hardcoded**: scenario list resolved from the discovered scenario domain (was `Actuals,Budget,Forecast` literals); plan side falls back to a discovered planning-version field with graceful degradation (adapted from budget-comparison's missing-budget prose); `forecast`/`departments` agents aligned.
  - **Live-verified recipe bugs fixed**: same-field COUNT of a grouped dimension 500s — COUNT now targets a different dense field (`anomalies`, data-check command); `explore-tables`' presentation templates dropped the un-derivable `~[count]` row-count columns (no tool returns row counts — the template invited fabrication); wrong `/datarails-finance-os:*` cross-command namespaces corrected to `/datarails-financeos:*` (9 occurrences across commands).
- **Audit skill re-scoped to honest, data-evidencable checks (audit finding S8).** The `audit` skill/agent promised SOX control tests — Access Control, Change Management, system-log/access-report "evidence" — that no MCP tool can substantiate (there is no audit-log/access-history endpoint), producing fabricated compliance assurance. Reframed as an **audit-support evidence package**: four data-evidencable check families (completeness & period integrity via grand-total checksums, consistency via `/dr-reconcile`'s independent-source checks, account-mapping integrity via cross-grain roll-ups with `[null]`-bucket flagging, and substantive sampling of material buckets), with a mandatory "Out of scope — requires external evidence" section in every deliverable naming the control families (access control, change management, ITGC) this tool cannot test.
- **Profiling response-shape documented; bare categorical profiling forbidden (audit finding S9).** `profile`, `anomalies`, and the `anomaly-detector` agent now state that `profile_numeric_fields` relays the backend-native `DR_Values`/`col_keys`/`row_keys` layout (values duplicated per stat, no per-value aggregator labels) and require key-mapping every value to its statistic — with a one-field `get_aggregated_data_by_*` cross-check anchor when ambiguous — before labeling anything MIN/MAX/AVG/COUNT or deriving outlier bands. `profile_categorical_fields` must always receive an explicit business-dimension `fields` list — called bare it profiles upload/mapping metadata columns, not business data. Also fixed `anomaly-detector`'s frequency recipe, which still COUNTed the same field it grouped by (500s live) and didn't exclude the grand-total row.
- **Command layer consolidated to thin launchers (audit finding S11).** All 8 public commands were full duplicate recipes of same-intent skills, frozen at older fix generations — every correction had to land twice, and the stale copy competed for the same user intent. Each is now a ~15-line launcher that delegates to its skill (`test-api`→`dr-test`, `financial-summary`→`dr-financial-summary`, `revenue-trends`→`dr-revenue-trends`, `expense-analysis`→`dr-expense-analysis`, `explore-tables`→`dr-tables`, `data-check`→`dr-anomalies`, `budget-comparison`→`dr-forecast-variance`, `drilldown`→`dr-drilldown`), matching the pattern the two `__internal` launchers already used. All slash-command entry points and trigger descriptions are unchanged (backward compatible); each recipe now exists in exactly one place. The one capability that lived only in a command — `drilldown`'s no-file intake (paste a DR.GET formula / describe the data point / structured filters, no workbook needed) — was ported into the `drilldown` skill as an explicit **no-file mode** before the command was reduced.
- **Generalization pass — nothing example-org-specific remains in any skill/agent/command.** The plugin is developed against one example org but ships to many clients; a 46-file audit removed everything that had leaked from the example org and made every remaining specific clearly illustrative: real dollar figures from live runs replaced with obviously-invented round figures (keeping the pedagogy, e.g. the 2× ratio example); real table/field/metric ids replaced with placeholders or clearly-fake ids; real dimension values (reporting units) and org-peculiar field names (the example org's `DR_ACC_L1.5` in-between level, `Report_Field`) genericized to "a sibling account-level field from the discovered schema" phrasing; remaining hardcoded `"Actuals"`/`"Budget"` filter literals in call templates replaced with `<scenario_value>`-style placeholders bound to the discovered scenario domain; org-specific "expected metric lineups" and errored-metric examples reframed as illustrative; mock outputs labeled "(illustrative — your org's values will differ)"; `tables`' example output dropped its un-derivable Rows/Last-Updated columns. Sanctioned runtime-discovery heuristics (regex matchers, name-priority fallback chains, platform conventions like DR.GET grammar and scenario-cycle notation) were explicitly preserved.

## [3.0.2] — 2026-07-01

### Changed
- **Made the Excel Add-In bridge internal.** `datarails-excel-agent` (bridge protocol) and `excel-context` (`dr-excel-context`, the orchestrator) are dev/desktop-only — the Add-In bridge is unusable in the public Cowork target — yet they were being carried into the public promotion as regular skills. Renamed both to `*__internal` so the publish pipeline strips them from the public mirror. The explicit cross-references in the public `drilldown` / `get-formula` / `forecast-variance` skills were repointed to the **Excel Context Contract in `CLAUDE.md`** (retained) so no public skill hard-points at a stripped skill; that contract now carries a one-line note that the bridge is internal/desktop-only and dormant in the public target. `drilldown` stays public (it degrades to its MCP/openpyxl path when no Excel bridge is present).

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
