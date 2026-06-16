---
description: Hand off the current branch to bar-ai-coder. Opens a PR labeled auto-coder/managed; the review loop iterates on CI + bot comments, then either auto-merges (with --auto-approve) or pings you on Slack for manual approval. Args optional — PR title inferred from commits if omitted. Use --auto-approve anywhere in args to skip manual approval and let the loop merge when CI is green.
argument-hint: [--auto-approve] [PR title]
---

# How to run this command

**Run the entire workflow below as a subagent** to keep verbose tool
output out of the main conversation. The user can expand the Agent
call if they want to see the details.

**First do Step 0 below** (commit this session's work, in the main
conversation), then invoke the `Agent` tool with:

- `subagent_type`: `general-purpose`
- `description`: `ship-it: open auto-coder PR`
- `prompt`: the ENTIRE block of text below the `===== SUBAGENT PROMPT =====`
  marker, with the user's argument substituted in for `$ARGUMENTS` where
  it appears.

## Step 0 — Commit this session's work (main conversation, before handoff)

**This step runs in the main conversation, NOT in the subagent** — the
subagent can't pause to collect interactive input, so the commit decision
has to happen here, before the Agent is invoked. Doing it here also keeps
unrelated leftover files out of the PR, which matters: extra files inflate
the diff and can trip the review-loop's size gate into a forced manual
approval even when `--auto-approve` was passed.

1. Run ONE Bash call: `git status --porcelain`. If the output is empty the
   working tree is clean — skip the rest of this step and go straight to the
   handoff line below.
2. If the tree is dirty, categorize **every** dirty file using **this
   session's conversation history**:
   - **Related** — files this session created, edited, or discussed.
   - **Possibly unrelated** — everything else (e.g. leftover files from a
     previous session, or something the user edited earlier and forgot).

   **List every single dirty file from `git status` — never omit, collapse,
   or summarize.** Each file must appear in exactly one of the two lists. The
   point is that the user always sees what's in their tree before anything is
   committed or shipped, especially files they may have forgotten about.
3. Auto-generate a commit message from the session's work — imperative mood,
   present tense, 5-12 words, names the change not the file (same style as
   Step 1.5's title rules below). **Do not ask the user to type a message.**
4. Show the user the full breakdown and proposed message, then ask
   `yes` / `no` / `cancel`:

   ```
   Checking working tree before handoff…
   Cross-referencing dirty files with this session's work…

   Related to our work this session (recommend committing):
     <related files — list every one>

   Auto-generated commit message:
     "<inferred message>"

   Possibly unrelated (NOT from this session — will leave uncommitted):
     <unrelated files, each on its own line, or "- (none)">

   Commit the related files with that message and ship?
     [yes]     commit related + ship   (leaves unrelated files alone)
     [no]      ship only already-committed work
     [cancel]  stop — don't ship; I'll go deal with those files first
   ```

   - `yes` →
     - **First check the current branch.** If you are on a protected/base
       branch (`main`, `master`, `dev`, `prod`, `develop`, `release`), create
       the ship branch **before committing** so the commit never lands on the
       protected branch: `git checkout -b ship/<slug>`, where `<slug>` is the
       inferred commit message run through the same slugify rules the script
       uses (lowercase, non-alphanumerics → `-`, trimmed, ≤60 chars). If that
       branch already exists locally **or on `origin`** (check both, since a
       push would fail on a remote collision too), truncate the slug enough to
       make room and append a short unique suffix (e.g. `ship/<slug>-2`),
       keeping the whole name ≤60 chars, then retry — never fall back to
       committing onto the base branch. The subagent's script detects it's
       already on a feature branch and won't re-create it. If you are already
       on a feature branch, skip this and commit in place.
     - Then `git add <related files>` (only the related paths, NOT
       `git add -A`) and `git commit -m "<inferred message>"`. Leave the
       unrelated files uncommitted in the working tree.
     - **Why branch-first on a base branch:** `git checkout -b` then commit
       puts the commit only on the new `ship/` branch. Committing first and
       letting the script branch afterward would leave the commit on the base
       branch too — the local base branch ends up 1 commit ahead of its
       upstream even though nothing was pushed. Branching first avoids that
       entirely.
   - `no` → commit nothing. Proceed to ship only already-committed work;
     leave all dirty files untouched.
   - `cancel` → **stop entirely. Do NOT invoke the Agent.** Make no commits
     and no changes; the user wants to inspect/handle the files first.
     Acknowledge briefly (e.g. "Cancelled — nothing shipped. Your files are
     untouched.") and end the turn.

   If there are no "possibly unrelated" files, this is a simple confirm —
   still show it so the user sees what's about to be committed.

**Before invoking the Agent**, tell the user one short line: e.g.
`Handing off to ship-it subagent…` so they know what's happening.

**After the Agent returns**, output its final summary verbatim to the
user. Do NOT add your own commentary, summary, or follow-up unless the
agent's output indicates the user needs to act.

===== SUBAGENT PROMPT =====

You are running the `/ship-it` slash command — bar-ai-coder Plug 2.
The user has been coding locally and wants to hand the branch off to
the review loop. Your job is to do the **minimum LLM work** required,
then delegate all git/gh ceremony to a single bash script invocation.
The script handles: sync with main, branch creation, commit, push,
label setup, gist upload, PR creation, label routing. **Don't** run
those steps yourself one by one — that's the slow path the script
exists to replace.

`$ARGUMENTS` is the user-supplied argument string (may be empty).

---

## Step 1 — Parse `$ARGUMENTS` (no tool calls)

Extract:

- `AUTO_APPROVE`: `true` if `$ARGUMENTS` contains the flag
  `--auto-approve` anywhere in the string, else `false`. Strip the
  flag from the title.
- `TITLE`: the remaining `$ARGUMENTS` text with `--auto-approve`
  removed and surrounding whitespace trimmed. May be empty.

---

## Step 1.5 — Infer a meaningful title from the diff (only if TITLE is empty)

**Skip this step if `TITLE` is non-empty** — the user gave us their
own title, use it verbatim.

Otherwise, generate a real PR title from what's being shipped. This is
the difference between a PR showing up to reviewers as
`ship: conversation.controller.ts edits` versus `Add Slack ID lookup
fallback chain for Plug 2 PRs`. The title also becomes the `ship/<slug>`
branch name.

By now Step 0 (main conversation) has already committed this session's
work, so the strongest signal is the commit log; any files still
uncommitted are the leftovers Step 0 intentionally left out and won't be
shipped.

1. ONE Bash call to gather the diff signal — the commits ahead of the
   repo's default branch (resolved dynamically into `$BASE` — usually
   `main`, but `master` / a custom default branch will work the same way)
   that haven't been pushed yet, plus any still-uncommitted edits for
   context:

   ```sh
   BASE=$(GITHUB_TOKEN="" gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
   {
     echo '=== Uncommitted changes (git diff HEAD --stat) ==='
     git diff HEAD --stat 2>/dev/null
     echo
     echo '=== Uncommitted diff (first 100 lines) ==='
     git diff HEAD 2>/dev/null | head -100
     echo
     echo "=== Local commits ahead of origin/$BASE (subjects) ==="
     git fetch --quiet origin "$BASE" 2>/dev/null
     git log --oneline "origin/$BASE..HEAD" 2>/dev/null
   }
   ```

2. Generate a single-line PR title (no LLM thinking needed beyond
   reading what changed):

   - 5-12 words.
   - Imperative mood, present tense (matches the project's commit
     style): `Add ...`, `Fix ...`, `Refactor ...`, `Drop ...`.
   - Names the *change*, not the file. Bad: `Edit cfoTuner.ts`.
     Good: `Cap CFO tuner retries at 3 attempts`.
   - No `ship:` prefix — that's only for the auto-commit fallback
     pattern, not for human-readable PR titles.

3. Set `TITLE = <the inferred line>`.

This `TITLE` is used only for the `gh pr create` title and the
`ship/<slug>` branch name. It is independent of Step 0's commit
message — the two are generated separately and may differ slightly in
wording; that's fine (the commit subject and PR title don't have to be
byte-identical).

Time cost: ~5-8s end-to-end — ~3-5s of subagent reasoning plus
~1-3s of network for `gh repo view` (default-branch lookup) and
`git fetch`. Worth it — PR titles are how reviewers triage what's
worth looking at.

---

## Step 2 — Generate the Context block (one LLM step, the only heavy thinking)

### Step 2a — Detect pre-existing commits on the branch (no extra LLM step)

Before generating the Context block, surface any commits the user
already made on this branch *before* the current Claude Code session
started. The Context block normally describes only the session's
intent ("Decisions made", "Files of interest" come from the chat
history). Pre-existing commits would otherwise silently ship in the
PR with no mention in the description — review hazard, also blinds
the auto-coder review loop's iteration agent.

(Heading says "no extra LLM step" rather than "no LLM" — the
categorization below still uses LLM reasoning to compare commit
subjects against the conversation, but it folds into Step 2's
single LLM turn and doesn't add a new model round-trip.)

Step 1.5's bash output already shows the commit *subjects* but not
the per-commit file lists, so Step 2a always runs its own bash for
the file mapping. The cost is one additional `git log --name-status`
(local-only, no network — `git fetch` was already done by Step 1.5
in the common path):

```sh
BASE=$(GITHUB_TOKEN="" gh repo view --json defaultBranchRef --jq .defaultBranchRef.name)
git fetch --quiet origin "$BASE" 2>/dev/null   # skip if Step 1.5 already fetched
echo '=== Per-commit files (sha, subject, files touched) ==='
# --name-status under git log gives one section per commit with the
# file list immediately after the subject. This is per-commit
# accuracy, NOT the branch-vs-base net diff (a commit that touches a
# file and is later reverted would disappear from a net diff).
git log --name-status --pretty=format:'%n--- %h %s' "origin/$BASE..HEAD" 2>/dev/null
```

Categorize each commit as either:
- **From this session** — commit subject matches the conversation
  (names of files the chat discussed, or the commit Step 0 just made
  with its auto-generated message).
- **Pre-existing** — anything else. User-authored commits made
  before the session opened (e.g. a `test/` branch the user
  hand-prepped before invoking /ship-it).

If there are pre-existing commits, set `PRE_EXISTING_BLOCK` to a
markdown list of them; otherwise set `PRE_EXISTING_BLOCK=""`. Include
the per-commit file list **only if** the bash output gave you the
mapping (it should — see above):

```
**Pre-existing commits on this branch (not from this session)**:
- `abc1234` <commit subject> — touches `path/to/file.ts`
- `def5678` <commit subject> — touches `other/file.ts`
```

If for any reason the per-commit file mapping isn't available, omit
the `— touches ...` portion rather than fabricate it:

```
**Pre-existing commits on this branch (not from this session)**:
- `abc1234` <commit subject>
- `def5678` <commit subject>
```

### Step 2b — Build the Context block

Build a `CONTEXT_BLOCK` string with this exact shape:

```markdown
<!-- BAR_AI_CODER_CONTEXT -->
## Context

**Source**: /ship-it from local Claude Code

**Objective**: <one-line: what is this PR trying to accomplish?>

**Decisions made**:
- <important choice + brief reason>
- <another>

**Constraints / gotchas**:
- <e.g., "the `Snapshot` type is being renamed in PR #1248 — don't conflict">

**Files of interest**:
- `path/to/file.ts`

**Out of scope**:
- <e.g., "error retry logic — separate ticket">

<!-- if PRE_EXISTING_BLOCK is non-empty, inject it here verbatim, e.g.: -->
**Pre-existing commits on this branch (not from this session)**:
- `abc1234` <subject> — touches `path/to/file.ts`
<!-- /BAR_AI_CODER_CONTEXT -->
```

Target ≤3000 chars. Use `- (none)` for fields with nothing to say —
keeps the shape predictable for the extractor.

**If there's no meaningful prior conversation** (first-turn /ship-it
with no chat history) AND `PRE_EXISTING_BLOCK` is empty: skip this
step entirely and let the script synthesize a minimal block from
`TITLE`. Set `CONTEXT_BLOCK=""`.

**If chat history is empty but `PRE_EXISTING_BLOCK` is non-empty**:
still build the Context block — even with `- (none)` for all the
session-specific fields — so the pre-existing commits get surfaced
in the PR description.

---

## Step 2.5 — Committing is handled before handoff (do NOT prompt here)

Committing this session's work happens in the **main conversation** in
**Step 0**, before this subagent is ever invoked. That's where an
interactive confirmation can actually work — a subagent can't pause to
collect a reply, so prompting here would hang or surface broken questions.

**Do not run `git status` and prompt for commits in this subagent.** Any
files still dirty by the time the script runs are intentional (Step 0 left
them out on purpose). The script is invoked with `NO_AUTO_COMMIT=true`
(Step 4), so it will **not** `git add -A` them — they stay in the working
tree and only already-committed work is shipped.

---

## Step 3 — (No work) Transcript handled by the script

The script auto-extracts the last 40 conversation turns directly
from the Claude Code session log on disk
(`~/.claude/projects/<encoded-cwd>/<session>.jsonl`) using `jq` —
**you do not need to write a transcript file**.

This was the single biggest speedup vs. the original /ship-it: the
old flow had the LLM emit ~5000-10000 tokens of raw transcript text
via the Write tool, which took ~30-60s of streaming time. The
script does the same job in ~200ms with `jq` + array slicing.

If you want to skip the transcript / gist entirely (e.g. for a tiny
no-conversation /ship-it), pass `NO_TRANSCRIPT=true`. The script
will create the PR with the Context block only, no gist.

---

## Step 4 — Single Bash invocation: run the script

Execute the script in ONE Bash tool call. Pass parsed inputs as env
vars:

```sh
TITLE="<step 1 TITLE>" \
AUTO_APPROVE="<step 1 AUTO_APPROVE>" \
NO_AUTO_COMMIT=true \
CONTEXT_BLOCK=$'<step 2 CONTEXT_BLOCK, $-quoted so literal newlines pass through>' \
bash "${CLAUDE_PLUGIN_ROOT}/scripts/ship-it.sh"
```

(`${CLAUDE_PLUGIN_ROOT}` is set by Claude Code to this plugin's install
directory, so the script is found regardless of which repo you run
`/ship-it` in.)

`NO_AUTO_COMMIT=true` is always passed: committing is owned by Step 0 in
the main conversation, so the script must not `git add -A` whatever is
still dirty (those files were intentionally left out). `COMMIT_MSG` is no
longer needed and is omitted.

The script handles ALL git/gh work (sync with main, branch creation,
commit, push, transcript extraction from session log, gist upload,
PR creation, label routing) and emits a structured `SCRIPT_RESULT`
block at the end. On any abort, it exits 1 with an `ABORT:` line on
stderr — surface that to the user verbatim if it happens.

When passing `CONTEXT_BLOCK`, use `$'...'` ANSI-C quoting so embedded
newlines in the block are preserved. Escape `'` characters in the
block as `\'`. If escaping is fiddly, write the block to a temp file
and `export CONTEXT_BLOCK="$(cat /tmp/ctx.md)"` instead.

For debugging perf, run with `DEBUG_TIMING=1` — the script will emit
phase-by-phase wall-clock timings to stderr.

---

## Step 5 — Parse the script output and print the hand-off

The script's stdout ends with:

```
SCRIPT_RESULT
status=<opened|already-shipped|label-added>
branch=<BRANCH>
base=<BASE>
repo=<REPO>
pr_number=<N>
pr_url=<URL>
auto_approve=<true|false>
gist_url=<URL or empty>
local_main_ahead=<true|false>
END_RESULT
```

Parse those fields. Then print the structured hand-off output below,
substituting values:

```
Your ship has departed 🧑‍🚀
  ├─ Branch:  <BRANCH>
  ├─ PR:      <PR_URL>
  └─ Loop:    auto-coder review loop engaged

What happens next: checks run → iterate on failures → merge
(or escalate after 3 iterations).

Controls:
  · Pause:   post any comment on the PR (human comment = pause)
  · Cancel:  remove the `auto-coder/managed` label
  · Watch:   open the PR URL in your browser

Approval mode: <auto-approve if AUTO_APPROVE=true, else manual-approval (default)>
  · auto-approve   = review-loop merges when ready
  · manual-approval = you get a Slack ping when ready to merge
```

If `status=already-shipped`: replace the first line with
`Your ship has already departed — see PR below.`

If `status=label-added`: replace the first line with
`Your ship has departed (label added) — review loop will pick this up shortly.`

---

## Step 6 — Optional: offer local-main cleanup

This step **only applies** if `local_main_ahead=true` in the script
output. It means the user ran `/ship-it` while sitting on local
`main` with unpushed commits, and those commits were carried onto
the new ship/ branch. Local main is now ahead of origin/main with
work-in-progress that's safely captured on the new branch.

Ask the user, after printing the Shipped! summary:

> Your local main still has those commits ahead of origin/main (your
> work is preserved on the ship/ branch). Want me to clean up local
> main with `git checkout main && git reset --hard origin/main`? (yes/no)

If yes: run those two commands via Bash, then checkout back to the
ship/ branch.

If no or no response: do nothing.

---

## Error handling

- If the script exits non-zero with an `ABORT:` line, print the abort
  message to the user verbatim and stop. Do NOT try alternate flows.
- If the Bash tool itself errors before the script runs (file not
  found, permission denied), print the error and stop — likely the
  `ship-it` plugin isn't installed or `${CLAUDE_PLUGIN_ROOT}` is unset;
  tell them to install/enable it (`/plugin install ship-it@datarails-marketplace`)
  and retry.
- **Never push to a branch named** `main`, `master`, `dev`, `prod`,
  `develop`, or `release`. The script enforces this; don't try to
  bypass.
