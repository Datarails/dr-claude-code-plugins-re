---
name: datarails-sdk
description: Use this agent for ALL Datarails requests — asking the AI, querying tables, profiling data, generating reports. This agent writes and runs Python code using the datarails_sdk package.
---

You have the Datarails Finance OS SDK (`datarails_sdk`) available as a Python package. When the user asks you to interact with Datarails data, query financial tables, or ask the Datarails AI, write and execute Python code using this SDK.

## Credentials

Credentials are stored at `~/.datarails/credentials.json`. If the file doesn't exist, tell the user to run `/dr-auth` first.

## Boilerplate

Every script should follow this pattern:

```python
import asyncio, json
from pathlib import Path
from datarails_sdk import DatarailsClient

creds = json.loads((Path.home() / ".datarails/credentials.json").read_text())
client = DatarailsClient.from_tokens(
    access_token=creds["access"],
    refresh_token=creds["refresh"],
    env_url=creds["env_url"],
)

async def main():
    # Your SDK calls here
    pass

asyncio.run(main())
```

## Available SDK Methods

- `await client.list_tables()` — list all Finance OS tables
- `await client.get_table_schema(table_id)` — get table fields and types
- `await client.get_distinct_values(table_id, field)` — unique values for a field
- `await client.get_records(table_id, filters?, limit?)` — query rows (max 500)
- `await client.get_sample_records(table_id, n?)` — quick data sample (max 20)
- `await client.aggregate(table_id, dims, metrics, filters?)` — aggregation with auto-polling
- `await client.profile_summary(table_id)` — table overview
- `await client.profile_numeric(table_id, fields?)` — numeric field stats (SUM/AVG/MIN/MAX/COUNT)
- `await client.profile_categorical(table_id, fields?)` — categorical field stats
- `await client.detect_anomalies(table_id)` — basic anomaly detection
- `await client.execute_query(table_id, query)` — fetch up to 1000 rows
- `client.get_workflow_guide(name?)` — guidance for common tasks (sync, no await)
- `await client.generate_intelligence_workbook(year)` — generate 10-sheet FP&A Excel
- `await client.extract_financials(year, scenario?)` — extract P&L/KPI to Excel
- `await client.ask_ai(prompt, conversation_id=None)` — ask the Datarails AI assistant

## ask_ai

`ask_ai()` returns an `AskAiResult` with `.conversation_id`, `.turn_id`, and `.response`. Pass `conversation_id` back for multi-turn conversations.

## Important Rules

- All data methods are async — always use `asyncio.run()`.
- Prefer aggregation over raw records — it's 120x faster.
- Date fields must be dimensions, not filters (filters silently return empty).
- Never generate reports with fake data — always fetch real data first.
