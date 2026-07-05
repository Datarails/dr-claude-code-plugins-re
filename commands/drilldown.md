---
description: Drill down on a Datarails DR.GET value - paste a formula or describe what you want to break down and see the underlying detail
---

# DR.GET Drill-Down

This command is a thin launcher — the full drill-down workflow lives in the
`dr-drilldown` skill. Do not improvise workflow steps here.

Invoke the **`dr-drilldown`** skill with whatever the user provided. No workbook
is needed — the skill's **no-file mode** accepts exactly what this command used
to take directly:

- a pasted `DR.GET` formula,
- a plain-language description ("Break down January 2026 Actuals Revenue"), or
- structured filters ("Scenario=..., Account Group=..., Reporting Date=...").

With an open Excel workbook (add-in bridge) or an `.xlsx` path, the skill's
Excel-context / file paths take over instead.
