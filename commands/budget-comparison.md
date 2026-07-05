---
description: Compare actual results to budget - see where you're over or under plan using complete aggregated data
---

# Budget vs Actual Comparison

This command is a thin launcher — the single maintained recipe for plan-vs-actual
analysis lives in the `dr-forecast-variance` skill. Do not improvise workflow
steps here.

Invoke the **`dr-forecast-variance`** skill with the user's request framed as a
budget-vs-actual comparison, passing through any period (`--year`), scenario, or
category focus they named.

Notes for the handoff:

- The skill discovers the scenario domain at runtime. If no budget-like scenario
  exists (common — many orgs carry only actuals/forecast scenarios), it uses the
  discovered planning-version-like field as the plan side, and degrades
  gracefully to comparing the scenarios that do exist.
- All variance math is period-scoped and labeled with period + scenario.
