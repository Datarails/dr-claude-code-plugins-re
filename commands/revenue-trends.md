---
description: See your revenue trends over time - growth rates, patterns, and insights using complete aggregated data
---

# Revenue Trends

This command is a thin launcher — the single maintained revenue-trends recipe
lives in the `dr-revenue-trends` skill. Do not improvise workflow steps here.

Invoke the **`dr-revenue-trends`** skill with whatever arguments the user
passed (period, scenario, composition focus, …).

The skill matches revenue at the discovered P&L grain, excludes the trailing
grand-total row from trend math, and labels output with period + scenario.
