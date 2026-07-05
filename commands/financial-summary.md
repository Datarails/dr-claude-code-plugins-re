---
description: Get a quick summary of your financial data - revenue, expenses, and key metrics using real aggregated totals
---

# Financial Summary

This command is a thin launcher — the single maintained summary recipe lives in
the `dr-financial-summary` skill. Do not improvise workflow steps here.

Invoke the **`dr-financial-summary`** skill with whatever arguments the user
passed (`--year`, `--scenario`).

The skill computes every figure from aggregated totals (never sampled rows),
defaults to the latest complete fiscal year, and labels all output with the
period + scenario it covers.
