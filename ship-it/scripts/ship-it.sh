#!/usr/bin/env bash
#
# ship-it.sh — deterministic git/gh work for the /ship-it slash command
# (bar-ai-coder Plug 2). Called by .claude/commands/ship-it.md.
#
# Why a script: collapsing all the gh/git ceremony into one shell
# invocation removes ~15 Claude LLM round-trips (one per Bash tool call
# in the prior pure-LLM version), bringing /ship-it from ~4.5 min down
# to ~30-45s.
#
# Inputs (env vars, all optional unless noted):
#   TITLE              PR title. If empty, auto-inferred from the latest
#                      commit subject or the dirty file list.
#   AUTO_APPROVE       "true" → add auto-coder/auto-approve label so the
#                      review loop self-merges. Default: "false".
#   CONTEXT_BLOCK      The <!-- BAR_AI_CODER_CONTEXT --> markdown block
#                      the calling agent generated from the conversation.
#                      Used verbatim as the head of the PR body. If empty,
#                      we synthesize a minimal one from $TITLE.
#   COMMIT_MSG         If set, used as the commit message for dirty
#                      changes (the calling agent confirmed this with
#                      the user). If unset, fall back to TITLE or the
#                      auto-inferred "ship: <basename> edits" pattern.
#                      Ignored when NO_AUTO_COMMIT=true (no commit runs).
#   NO_AUTO_COMMIT     "true" → never auto-commit dirty changes. The
#                      caller (Step 0 of the /ship-it command) already
#                      committed this session's work in the main
#                      conversation, so any remaining dirty files are
#                      intentional and must be left in the working tree.
#                      Only already-committed work is pushed/shipped.
#   TRANSCRIPT_PATH    [legacy] Path to a markdown file with raw last-N
#                      user/assistant messages. If set + non-empty file
#                      exists, used as the gist content. If unset, we
#                      auto-extract from the current Claude session log
#                      at ~/.claude/projects/<encoded-cwd>/*.jsonl
#                      (see TRANSCRIPT_AUTO_TURNS for the cap).
#   TRANSCRIPT_AUTO_TURNS  Max user/assistant turns to pull from the
#                          auto-extracted session log. Default: 40.
#   NO_TRANSCRIPT      "true" → skip the gist entirely (no transcript).
#   GH_PREFIX          Prefix prepended to every `gh` call. Datarails uses
#                      `GITHUB_TOKEN=""` because the env GITHUB_TOKEN
#                      lacks org access; keyring has the right scopes.
#                      Defaults to `GITHUB_TOKEN=""`.
#   DEBUG_TIMING       "1" → emit phase timings to stderr.
#   DRY_RUN            "1" → run all checks + local git work but SKIP
#                      destructive remote operations (push, gist create,
#                      PR create, label create). Useful for benchmarking.
#
# Output: prints a structured "SCRIPT_RESULT" block at the end with
#   status=<opened|already-shipped|label-added>
#   branch=<BRANCH>
#   pr_url=<URL>
#   pr_number=<N>
#   auto_approve=<true|false>
#   local_main_ahead=<true|false>   ← caller can offer cleanup prompt
# On abort: exits 1 with an "ABORT:" line on stderr.

set -euo pipefail

GH_PREFIX="${GH_PREFIX:-GITHUB_TOKEN=\"\"}"
gh_() {
  # Run gh with the configured prefix. eval is fine — GH_PREFIX is
  # operator-controlled, not user input.
  eval "$GH_PREFIX gh \"\$@\""
}

abort() {
  echo "ABORT: $*" >&2
  exit 1
}

# Phase timing: when DEBUG_TIMING=1, log wall-clock from script start
# to each named phase. Uses $EPOCHREALTIME (bash 5+, includes µs).
T_BOOT=${EPOCHREALTIME:-$(date +%s.%N)}
phase() {
  [ "${DEBUG_TIMING:-}" = "1" ] || return 0
  local now=${EPOCHREALTIME:-$(date +%s.%N)}
  # Print elapsed (seconds, 3 decimals) and phase name to stderr.
  awk -v t0="$T_BOOT" -v t1="$now" -v name="$1" \
    'BEGIN { printf "::timing:: t=%6.3fs phase=%s\n", t1-t0, name }' >&2
}
phase BOOT

# ─────────────────────────────────────────────────────────────────────
# 1. Pre-flight + repo context — gh repo view ‖ git fetch in parallel
# ─────────────────────────────────────────────────────────────────────

git rev-parse --git-dir >/dev/null 2>&1 || abort "not a git repo"

CURRENT=$(git rev-parse --abbrev-ref HEAD)
DIRTY=$(git status --porcelain || true)
case "$CURRENT" in
  ""|HEAD) abort "detached HEAD — checkout a branch first" ;;
esac
phase PREFLIGHT

# Kick off `gh repo view` and `git fetch` concurrently — they're
# both network-bound and independent. We can't fetch a specific base
# branch until we know the default branch ref, but in practice the
# default is overwhelmingly `main` so we speculatively fetch `main`;
# if the actual default turns out to be different we fetch it too.
TMP_REPO_JSON=$(mktemp)
TMP_FETCH_ERR=$(mktemp)
trap 'rm -f "$TMP_REPO_JSON" "$TMP_FETCH_ERR" "${TRANSCRIPT_AUTO_PATH:-}"' EXIT

(gh_ repo view --json defaultBranchRef,nameWithOwner > "$TMP_REPO_JSON" 2>&1) &
PID_GH_REPO=$!
(git fetch --quiet origin main 2>"$TMP_FETCH_ERR" || true) &
PID_FETCH_SPEC=$!

wait $PID_GH_REPO || abort "gh repo view failed: $(cat "$TMP_REPO_JSON")"
REPO_JSON=$(cat "$TMP_REPO_JSON")
REPO=$(printf '%s' "$REPO_JSON" | jq -r .nameWithOwner)
BASE=$(printf '%s' "$REPO_JSON" | jq -r .defaultBranchRef.name)

wait $PID_FETCH_SPEC || true
# If the speculative `main` fetch failed (e.g. base isn't main, or
# network blip), retry the actual base branch synchronously.
if [ "$BASE" != "main" ] || ! git rev-parse --verify "origin/$BASE" >/dev/null 2>&1; then
  git fetch --quiet origin "$BASE" 2>&1 || abort "git fetch origin $BASE failed"
fi
phase REPO_VIEW_AND_FETCH

AHEAD=0
if git rev-parse --verify "origin/$BASE" >/dev/null 2>&1; then
  AHEAD=$(git rev-list --count "origin/$BASE..HEAD" 2>/dev/null || echo 0)
fi

# Detect "user is on local main with unpushed commits" — we don't
# auto-reset (left to the caller to offer as an optional cleanup
# prompt), but we surface it in the structured output.
LOCAL_MAIN_AHEAD=false
if [ "$CURRENT" = "$BASE" ] && [ "$AHEAD" -gt 0 ]; then
  LOCAL_MAIN_AHEAD=true
fi

# Abort if there's literally nothing to ship.
if [ "$CURRENT" = "$BASE" ] && [ -z "$DIRTY" ] && [ "$AHEAD" -eq 0 ]; then
  abort "nothing to ship — no commits ahead of $BASE and no uncommitted changes"
fi

# With NO_AUTO_COMMIT, dirty files are never committed/pushed by this
# script (committing is owned by Step 0 of /ship-it, in the main
# conversation). So if there are no commits ahead of base either, there
# is genuinely nothing to ship — on ANY branch. This catches the
# "declined Step 0 with no prior commits" path, which would otherwise
# push an empty branch and fail with a confusing `gh pr create` error.
if [ "${NO_AUTO_COMMIT:-}" = "true" ] && [ "$AHEAD" -eq 0 ]; then
  abort "nothing to ship — no commits ahead of $BASE (uncommitted changes are left untouched; commit the work you want to ship, then re-run /ship-it)"
fi

# ─────────────────────────────────────────────────────────────────────
# 2. Sync with main (merge — least risky strategy)
# ─────────────────────────────────────────────────────────────────────

if [ "$CURRENT" != "$BASE" ]; then
  BEHIND=$(git rev-list --count "HEAD..origin/$BASE" 2>/dev/null || echo 0)
  if [ "$BEHIND" -gt 0 ]; then
    if ! git merge --no-edit "origin/$BASE" >/dev/null 2>&1; then
      CONFLICTS=$(git status --porcelain | awk '/^(UU|AA|DD|AU|UA|DU|UD)/ {print $2}')
      git merge --abort
      {
        echo "merge with origin/$BASE has conflicts. Resolve locally and re-run /ship-it."
        echo "Conflicting files:"
        printf '  - %s\n' $CONFLICTS
      } >&2
      exit 1
    fi
  fi
fi

# ─────────────────────────────────────────────────────────────────────
# 3. Branch handling (deterministic — no interactive prompt)
# ─────────────────────────────────────────────────────────────────────

slugify() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g; s/-+/-/g' \
    | cut -c1-60
}

# Infer a commit message for uncommitted changes. Priority:
#   1. COMMIT_MSG (caller-confirmed by the user)
#   2. TITLE (user-supplied $ARGUMENTS)
#   3. "ship: <first-file-basename> edits" (deterministic fallback)
infer_commit_msg() {
  if [ -n "${COMMIT_MSG:-}" ]; then
    printf '%s' "$COMMIT_MSG"
    return
  fi
  if [ -n "${TITLE:-}" ]; then
    printf '%s' "$TITLE"
    return
  fi
  local first
  first=$(printf '%s' "$DIRTY" | awk '{ $1=""; sub(/^[ \t]+/, ""); print; exit }')
  if [ -n "$first" ]; then
    printf 'ship: %s edits' "$(basename "$first")"
  else
    printf 'ship: edits'
  fi
}

PROTECTED='^(main|master|dev|prod|develop|release)$'

if [ "$CURRENT" = "$BASE" ]; then
  # Case B: on default branch → create ship/<slug>
  if [ -n "${TITLE:-}" ]; then
    SLUG=$(slugify "$TITLE")
  elif [ "$AHEAD" -gt 0 ]; then
    SLUG=$(slugify "$(git log -1 --format=%s)")
  elif [ -n "$DIRTY" ]; then
    FIRST_DIRTY=$(printf '%s' "$DIRTY" | awk '{ $1=""; sub(/^[ \t]+/, ""); print; exit }')
    SLUG=$(slugify "$(basename "${FIRST_DIRTY%.*}")")
  else
    SLUG=""
  fi
  [ -z "$SLUG" ] && SLUG="update-$(date +%s | tail -c 5)"

  if printf '%s' "$SLUG" | grep -Eq "$PROTECTED"; then
    abort "refuse to use protected branch name as slug: $SLUG"
  fi

  BRANCH="ship/$SLUG"
  if [ "${DRY_RUN:-}" = "1" ]; then
    if [ "${NO_AUTO_COMMIT:-}" = "true" ]; then
      echo "[dry-run] would: git checkout -b $BRANCH (NO_AUTO_COMMIT=true → leave dirty changes uncommitted)" >&2
    else
      echo "[dry-run] would: git checkout -b $BRANCH; commit dirty changes" >&2
    fi
  else
    git checkout -b "$BRANCH"
    if [ "${NO_AUTO_COMMIT:-}" != "true" ] && [ -n "$DIRTY" ]; then
      git add -A
      git commit -m "$(infer_commit_msg)" >/dev/null
    fi
  fi
else
  # Case A: already on a feature branch
  if printf '%s' "$CURRENT" | grep -Eq "$PROTECTED"; then
    abort "refuse to ship from protected branch: $CURRENT"
  fi
  BRANCH="$CURRENT"

  if [ "${NO_AUTO_COMMIT:-}" != "true" ] && [ -n "$DIRTY" ]; then
    if [ "${DRY_RUN:-}" = "1" ]; then
      echo "[dry-run] would: git add -A && git commit -m '<inferred>'" >&2
    else
      git add -A
      git commit -m "$(infer_commit_msg)" >/dev/null
    fi
  fi
fi
phase BRANCH_AND_COMMIT

# ─────────────────────────────────────────────────────────────────────
# 4. Idempotent label creation (parallel)
# ─────────────────────────────────────────────────────────────────────

if [ "${DRY_RUN:-}" = "1" ]; then
  echo "[dry-run] would create 6 auto-coder/* labels in parallel" >&2
else
  {
    gh_ label create "auto-coder/managed" --color "1f883d" --description "owned by auto-coder review loop" 2>/dev/null &
    gh_ label create "auto-coder/paused-for-human" --color "fbca04" --description "paused: human comment present" 2>/dev/null &
    gh_ label create "auto-coder/abandoned" --color "d73a4a" --description "auto-coder gave up; PR closed" 2>/dev/null &
    gh_ label create "auto-coder/auto-approve" --color "0e8a16" --description "auto-coder may approve + merge without human gate" 2>/dev/null &
    gh_ label create "auto-coder/awaiting-manual-approval" --color "0075ca" --description "ready for opener to approve + merge" 2>/dev/null &
    gh_ label create "auto-coder/local-ship" --color "8a2be2" --description "PR from local /ship-it (Plug 2) — exempt from size gate" 2>/dev/null &
    wait
  } || true
fi
phase LABELS

# ─────────────────────────────────────────────────────────────────────
# 5+6. Build the transcript file from the Claude session log, then
#      push branch ‖ create gist in parallel.
#
# Reading the session JSONL eliminates the prior LLM-emits-transcript
# step (which used to take 30-60s for substantive conversations).
# Bash + jq does it in ~1s with full fidelity.
# ─────────────────────────────────────────────────────────────────────

# Resolve $PWD → encoded project dir: /Users/foo/bar → -Users-foo-bar
ENCODED_CWD=$(printf '%s' "$PWD" | sed 's|/|-|g')
SESSION_DIR="$HOME/.claude/projects/$ENCODED_CWD"

# Reason the transcript ended up unavailable — used in the PR body
# note if no gist is uploaded. Empty string = transcript present.
TRANSCRIPT_SKIP_REASON=""
TRANSCRIPT_AUTO_PATH=""
if [ "${NO_TRANSCRIPT:-}" = "true" ]; then
  TRANSCRIPT_SKIP_REASON="NO_TRANSCRIPT=true (caller opted out)"
elif [ -n "${TRANSCRIPT_PATH:-}" ] && [ -s "${TRANSCRIPT_PATH:-/dev/null}" ]; then
  # Legacy path: caller already wrote the transcript file
  TRANSCRIPT_AUTO_PATH="$TRANSCRIPT_PATH"
elif [ ! -d "$SESSION_DIR" ]; then
  TRANSCRIPT_SKIP_REASON="session log dir not found at $SESSION_DIR (Claude Code may use a different layout in this version)"
  echo "WARN: $TRANSCRIPT_SKIP_REASON" >&2
elif [ -d "$SESSION_DIR" ]; then
  # Identify the MAIN session's JSONL.
  #
  # Two signals combined for robust selection:
  #
  #   (a) $CLAUDE_SESSION_ID env var — Claude Code exposes the current
  #       process's session ID. When /ship-it runs inside a subagent,
  #       this is the subagent's own session ID (NOT the user's main).
  #
  #   (b) "fresh-subagent fingerprint" check — a subagent's session
  #       log is brand new (mtime < 60s) AND small (< 200KB). The
  #       user's main session log is established (mtime stretches
  #       further back) AND larger.
  #
  # We only exclude $CLAUDE_SESSION_ID.jsonl from candidates when BOTH
  # (a) it matches our env, AND (b) the log file looks like a fresh
  # subagent (recent + small). This way:
  #
  #   - In production subagent path: self's log is fresh+small →
  #     excluded → picks the user's main from the remaining.
  #   - In direct-bash path: self's log is the user's main (older
  #     and bigger) → kept → picked.
  #
  # Among remaining candidates we pick the most-recently-modified —
  # that's the session where the user just typed something.
  SELF_SESSION_ID="${CLAUDE_SESSION_ID:-${CLAUDE_CODE_SESSION_ID:-}}"
  SELF_LOG_PATH=""
  EXCLUDE_SELF=false
  if [ -n "$SELF_SESSION_ID" ]; then
    SELF_LOG_PATH="$SESSION_DIR/$SELF_SESSION_ID.jsonl"
    if [ -f "$SELF_LOG_PATH" ]; then
      # stat -f for BSD/macOS, -c for GNU/Linux
      SELF_SIZE=$(stat -f '%z' "$SELF_LOG_PATH" 2>/dev/null \
        || stat -c '%s' "$SELF_LOG_PATH" 2>/dev/null \
        || echo 0)
      # find -mmin -1 returns the file if modified in the last 1 min
      IS_FRESH=$(find "$SELF_LOG_PATH" -mmin -1 -print 2>/dev/null)
      # Subagent fingerprint: brand-new file (< 1 min old) AND small
      # (< 200KB). The 200KB threshold cleanly separates subagents
      # (typically <100KB during execution) from main sessions
      # (typically >>200KB even for short conversations).
      if [ -n "$IS_FRESH" ] && [ "$SELF_SIZE" -lt 204800 ]; then
        EXCLUDE_SELF=true
      fi
    fi
  fi

  # Sorted by mtime desc, restricted to last 10 min (excludes idle
  # old sessions that aren't part of the current activity).
  ALL_CANDIDATES=$(
    find "$SESSION_DIR" -maxdepth 1 -name '*.jsonl' -type f -mmin -10 -print0 2>/dev/null \
      | xargs -0 ls -1t 2>/dev/null
    true
  )

  MAIN_LOG=""
  if [ -n "$ALL_CANDIDATES" ]; then
    while IFS= read -r f; do
      [ -z "$f" ] && continue
      if [ "$EXCLUDE_SELF" = "true" ] && [ "$f" = "$SELF_LOG_PATH" ]; then
        continue   # self is fingerprinted as the subagent's own — skip
      fi
      MAIN_LOG="$f"
      break
    done <<EOF
$ALL_CANDIDATES
EOF
  fi

  # Fallback A: if exclusion threw away everything (rare — would mean
  # ONLY the subagent's session was active in the last 10 min), still
  # use self so the gist gets built. Better than nothing.
  if [ -z "$MAIN_LOG" ] && [ -n "$ALL_CANDIDATES" ]; then
    MAIN_LOG=$(printf '%s\n' "$ALL_CANDIDATES" | head -1)
  fi

  if [ -n "$MAIN_LOG" ] && [ "${DEBUG_TIMING:-}" = "1" ]; then
    REASON="kept self (not fresh-subagent)"
    [ "$EXCLUDE_SELF" = "true" ] && REASON="excluded self ($(basename "$SELF_LOG_PATH"): fresh+small)"
    echo "::info:: picked session log: $(basename "$MAIN_LOG") — $REASON" >&2
  fi

  if [ -z "$MAIN_LOG" ]; then
    TRANSCRIPT_SKIP_REASON="no .jsonl session log found in $SESSION_DIR modified in the last 60 min"
    echo "WARN: $TRANSCRIPT_SKIP_REASON" >&2
  elif [ ! -s "$MAIN_LOG" ]; then
    TRANSCRIPT_SKIP_REASON="session log $MAIN_LOG is empty"
    echo "WARN: $TRANSCRIPT_SKIP_REASON" >&2
  else
    TRANSCRIPT_AUTO_PATH=$(mktemp -t auto-coder-transcript.XXXXXX).md
    CAP=${TRANSCRIPT_AUTO_TURNS:-40}
    {
      echo "# auto-coder /ship-it transcript"
      echo
      echo "Captured: $(date -u +'%Y-%m-%dT%H:%M:%SZ')"
      echo "Source: $(basename "$MAIN_LOG")"
      echo
      echo "---"
      echo
      # Extract real conversation turns:
      #  - type=user with string content (skip array-only entries that
      #    are tool_result chains).
      #  - type=assistant text blocks (skip thinking, tool_use,
      #    tool_result blocks — they bloat without helping).
      # Slurp all into an array, slice last $CAP turns, then emit each
      # turn block separated by a blank line. Using jq's array slicing
      # (vs awk's RS="") because the content itself contains blank
      # lines, which would confuse paragraph-based record splitting.
      # Noise patterns: Claude Code system-injected blocks that bloat
      # the transcript without helping the iteration agent.
      jq -s -r --argjson cap "$CAP" '
        def is_noise(s):
          (s | test("^<local-command-")) or
          (s | test("^<command-(name|message|args|stdout|stderr)>")) or
          (s | test("^<system-reminder>")) or
          (s | test("^<bash-stdout>")) or
          (s | test("^<bash-stderr>")) or
          (s | test("^Caveat: The messages below"));
        [
          .[]
          | select(.type == "user" or .type == "assistant")
          | if .type == "user" then
              (.message.content | if type == "string" then . else empty end) as $c
              | if ($c | length) > 0 and (is_noise($c) | not) then
                  "## User\n" + $c
                else empty end
            elif .type == "assistant" then
              (.message.content | map(select(.type == "text") | .text) | join("\n")) as $text
              | if ($text | length) > 0 then "## Assistant\n" + $text else empty end
            else empty end
        ]
        | .[-($cap):]
        | .[]
        | . + "\n"
      ' "$MAIN_LOG" 2>/dev/null
    } > "$TRANSCRIPT_AUTO_PATH"
    # Cap at 100KB just in case (gists allow 1MB but iteration agent
    # doesn't need megabytes of chat).
    if [ "$(wc -c < "$TRANSCRIPT_AUTO_PATH")" -gt 102400 ]; then
      head -c 100000 "$TRANSCRIPT_AUTO_PATH" > "$TRANSCRIPT_AUTO_PATH.cut"
      mv "$TRANSCRIPT_AUTO_PATH.cut" "$TRANSCRIPT_AUTO_PATH"
      echo >> "$TRANSCRIPT_AUTO_PATH"
      echo "...[transcript truncated at 100KB — earlier turns omitted]..." >> "$TRANSCRIPT_AUTO_PATH"
    fi
  fi
fi
phase TRANSCRIPT_BUILD

GIST_URL=""
if [ "${DRY_RUN:-}" = "1" ]; then
  echo "[dry-run] would push branch $BRANCH" >&2
  echo "[dry-run] would upload gist (size=$(wc -c < "${TRANSCRIPT_AUTO_PATH:-/dev/null}" 2>/dev/null || echo 0))" >&2
  GIST_URL="https://gist.github.com/EXAMPLE/dryrun"
else
  # Push branch ‖ upload gist (both network-bound and independent).
  TMP_PUSH=$(mktemp)
  TMP_GIST=$(mktemp)
  trap 'rm -f "$TMP_REPO_JSON" "$TMP_FETCH_ERR" "$TMP_PUSH" "$TMP_GIST" "${TRANSCRIPT_AUTO_PATH:-}"' EXIT

  (git push -u origin "$BRANCH" > "$TMP_PUSH" 2>&1) &
  PID_PUSH=$!

  PID_GIST=""
  if [ -n "$TRANSCRIPT_AUTO_PATH" ] && [ -s "$TRANSCRIPT_AUTO_PATH" ]; then
    (gh_ gist create "$TRANSCRIPT_AUTO_PATH" \
       --desc "auto-coder context for $REPO/$BRANCH" > "$TMP_GIST" 2>&1) &
    PID_GIST=$!
  fi

  if ! wait $PID_PUSH; then
    tail -10 "$TMP_PUSH" >&2
    abort "git push failed for branch $BRANCH"
  fi
  tail -3 "$TMP_PUSH" >&2

  if [ -n "$PID_GIST" ]; then
    wait $PID_GIST || true
    CANDIDATE=$(tail -1 "$TMP_GIST")
    if printf '%s' "$CANDIDATE" | grep -qE '^https://gist\.github\.com/'; then
      GIST_URL="$CANDIDATE"
    else
      echo "WARN: gist upload failed (continuing without it): $(tail -3 "$TMP_GIST")" >&2
    fi
  fi
fi
phase PUSH_AND_GIST

# ─────────────────────────────────────────────────────────────────────
# 7. Compose PR body
# ─────────────────────────────────────────────────────────────────────

# If the caller didn't supply a Context block (e.g. cold run with no
# conversation), synthesize a minimal one so the iteration agent's
# extractor still finds it.
if [ -z "${CONTEXT_BLOCK:-}" ]; then
  CONTEXT_BLOCK=$(cat <<EOF
<!-- BAR_AI_CODER_CONTEXT -->
## Context

**Source**: /ship-it from local Claude Code

**Objective**: ${TITLE:-$(git log -1 --format=%s)}

**Decisions made**:
- (none documented)

**Constraints / gotchas**:
- (none documented)

**Files of interest**:
- (auto-coder will discover from the diff)

**Out of scope**:
- (none documented)
<!-- /BAR_AI_CODER_CONTEXT -->
EOF
)
fi

# Inject the gist URL (or a "transcript unavailable" note) just before
# the closing CONTEXT tag. We always emit a "Full conversation
# transcript:" line so reviewers can see at a glance whether a gist
# was attached — and if not, why.
TRANSCRIPT_LINE=""
if [ -n "$GIST_URL" ]; then
  TRANSCRIPT_LINE="**Full conversation transcript**: $GIST_URL"
elif [ -n "$TRANSCRIPT_SKIP_REASON" ]; then
  TRANSCRIPT_LINE="**Full conversation transcript**: (unavailable — $TRANSCRIPT_SKIP_REASON)"
fi

if [ -n "$TRANSCRIPT_LINE" ]; then
  CONTEXT_BLOCK=$(printf '%s' "$CONTEXT_BLOCK" | awk -v line="$TRANSCRIPT_LINE" '
    /<!-- \/BAR_AI_CODER_CONTEXT -->/ && !p {
      print line
      p = 1
    }
    { print }
  ')
fi

FINAL_TITLE="${TITLE:-$(git log -1 --format=%s)}"

PR_BODY=$(cat <<EOF
$CONTEXT_BLOCK

---

Opened by /ship-it from local Claude Code. Branch \`$BRANCH\` → base \`$BASE\`.

bar-ai-coder review-loop will iterate on CI failures and bot
comments, then self-approve + merge. Post any comment to pause
for human review. Remove the \`auto-coder/managed\` label to cancel.

Architecture: https://github.com/barpg2802/bar-ai-coder/blob/main/ARCHITECTURE.md
EOF
)

# ─────────────────────────────────────────────────────────────────────
# 8. PR create / label-add / already-shipped
# ─────────────────────────────────────────────────────────────────────

PR_URL=""
PR_NUM=""
PR_STATUS=""

if [ "${DRY_RUN:-}" = "1" ]; then
  PR_URL="https://github.com/$REPO/pull/0"
  PR_NUM="0"
  PR_STATUS="dry-run"
  echo "[dry-run] would lookup/create PR for branch $BRANCH" >&2
else
  EXISTING_JSON=$(gh_ pr list --head "$BRANCH" --json number,url,labels --jq '.[0]' 2>/dev/null || echo "")
  if [ -n "$EXISTING_JSON" ] && [ "$EXISTING_JSON" != "null" ]; then
    PR_NUM=$(printf '%s' "$EXISTING_JSON" | jq -r .number)
    PR_URL=$(printf '%s' "$EXISTING_JSON" | jq -r .url)
    HAS_LABEL=$(printf '%s' "$EXISTING_JSON" | jq -r '[.labels[].name] | any(. == "auto-coder/managed")')
    if [ "$HAS_LABEL" = "true" ]; then
      PR_STATUS="already-shipped"
    else
      gh_ pr edit "$PR_NUM" --add-label "auto-coder/managed" --add-label "auto-coder/local-ship" --body "$PR_BODY" >/dev/null
      PR_STATUS="label-added"
    fi
  else
    PR_URL=$(gh_ pr create \
      --base "$BASE" \
      --head "$BRANCH" \
      --title "$FINAL_TITLE" \
      --body "$PR_BODY" \
      --label "auto-coder/managed" \
      --label "auto-coder/local-ship")
    PR_NUM=$(printf '%s' "$PR_URL" | grep -oE '[0-9]+$')
    PR_STATUS="opened"
  fi

  # Auto-approve label if requested
  if [ "${AUTO_APPROVE:-false}" = "true" ] && [ -n "$PR_NUM" ]; then
    gh_ pr edit "$PR_NUM" --add-label "auto-coder/auto-approve" >/dev/null
  fi
fi
phase PR_CREATE

# ─────────────────────────────────────────────────────────────────────
# 9. Structured output for the calling agent to consume
# ─────────────────────────────────────────────────────────────────────

cat <<EOF
SCRIPT_RESULT
status=$PR_STATUS
branch=$BRANCH
base=$BASE
repo=$REPO
pr_number=$PR_NUM
pr_url=$PR_URL
auto_approve=${AUTO_APPROVE:-false}
gist_url=$GIST_URL
local_main_ahead=$LOCAL_MAIN_AHEAD
END_RESULT
EOF
