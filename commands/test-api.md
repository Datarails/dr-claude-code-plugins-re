---
description: Test API field compatibility and performance - discover which fields work with aggregation and report the compatibility map
---

# API Diagnostic Test

This command is a thin launcher — the single maintained diagnostic lives in the
`dr-test` skill. Do not improvise workflow steps here.

Invoke the **`dr-test`** skill with whatever arguments the user passed.

Notes for the handoff:

- Results are **session-only** — nothing is persisted, and other skills handle
  field failures reactively on their own; this diagnostic is for when the user
  wants the compatibility map up front.
- An all-PASS result is the norm on healthy orgs.
