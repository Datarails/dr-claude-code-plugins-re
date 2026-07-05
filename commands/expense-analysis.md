---
description: Analyze your expenses - find top spending categories, trends, and potential issues using complete aggregated data
---

# Expense Analysis

This command is a thin launcher — the single maintained expense recipe lives in
the `dr-expense-analysis` skill. Do not improvise workflow steps here.

Invoke the **`dr-expense-analysis`** skill with whatever arguments the user
passed (`--year`, `--scenario`, `--breakdown`, a category focus, …).

The skill discovers the account grain at runtime and builds the expense set as
an include-list of discovered P&L buckets (never "everything except revenue"),
period-scoped and labeled.
