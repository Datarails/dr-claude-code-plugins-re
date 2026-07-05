---
description: Explore what data is available in your Datarails account
---

# Explore Your Data

This command is a thin launcher — the single maintained table-exploration
recipe lives in the `dr-tables` skill. Do not improvise workflow steps here.

Invoke the **`dr-tables`** skill with whatever the user passed:

- no args → list all available tables (id, name, alias)
- `<table_id>` → schema and summary for one table
- `--schema` → detailed schema view
- `--field <name>` → distinct values for a specific field
