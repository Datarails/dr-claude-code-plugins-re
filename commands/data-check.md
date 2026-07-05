---
description: Check your financial data for quality issues - missing values, anomalies, and inconsistencies
---

# Data Quality Check

This command is a thin launcher — the single maintained data-quality recipe
lives in the `dr-anomalies` skill. Do not improvise workflow steps here.

Invoke the **`dr-anomalies`** skill with the user's arguments (a table name or
id if they gave one; otherwise the skill discovers the financials table itself).

Related skills for the handoff:

- Field-level statistical profiling (ranges, null rates, cardinality) →
  `dr-profile`.
- A full data-quality Excel workbook deliverable → `dr-anomalies-report`.
