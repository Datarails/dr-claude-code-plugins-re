---
description: Drill down on a Datarails DR.GET value - paste a formula or describe what you want to break down and see the underlying detail
---

# DR.GET Drill-Down

Help the user drill into a Datarails financial number to see the underlying line-item detail. The user provides a DR.GET formula or describes the data point, and you query Datarails for the breakdown.

## Step 1: Verify Connection

Start by calling `list_finance_tables` to verify the connection is active.

**If the tool call fails:** The Datarails connector isn't connected. Tell the user to click the **"+"** button next to the prompt, select **Connectors**, find **Datarails**, and click **Connect**. Then STOP.

## Step 2: Get the DR.GET Parameters

Ask the user what they want to drill into. They can provide:

**Option A - Paste a DR.GET formula:**
The user pastes something like:
```
=DR.GET(Value, "[DR_ACC_L1.5]", "Revenues", "[Scenario]", "Actuals", "[Reporting Date]", 46053)
```

Parse the dimension/value pairs from the formula. A DR.GET formula has the pattern:
`=DR.GET(Value, "[Dim1]", Value1, "[Dim2]", Value2, ...)`

Extract each `"[DimensionName]"` and its corresponding value (the next argument). Values may be strings or numbers.

**Option B - Describe the data point:**
The user says something like: "Break down January 2026 Actuals Revenue"

Map their description to dimension filters:
- Use `get_table_schema` to find the correct field names
- Common mappings: "Revenue" → account field, "Actuals" → Scenario field, "January 2026" → Reporting Date field
- Ask clarifying questions if the description is ambiguous

**Option C - Provide filters directly:**
The user provides structured filters: "Scenario=Actuals, DR_ACC_L1.5=Revenues, Reporting Date=2026-01"

## Step 3: Ask About Global Filters

Ask the user if they have any global filters set in their Datarails Excel Add-in (e.g., Reporting Unit, Entity, Department). These filters affect what data DR.GET returns.

If they provide filter values, add them to the query filters. If they're unsure, proceed without them but warn that totals may not match their Excel if filters are active.

## Step 4: Choose Drill-Down Fields

Ask the user what they want to break down by. Suggest useful options:

> What would you like to break the data down by? Common options:
> - **Account detail** (e.g., Account Full, Account Name)
> - **Department** (e.g., Department L1, Department L2)
> - **Vendor**
> - **Entity / Reporting Unit**
>
> Or tell me the specific field names if you know them.

Use `get_table_schema` to validate that the chosen fields exist.

## Step 5: Run the Aggregation

**Aggregation rules:**
- Date fields (`Reporting Date`, `Reporting Month`, etc.) must ALWAYS go in `dimensions`, never in `filters`. Date filters silently return empty results.
- To limit to a specific period, include the date as a dimension and filter the results client-side after the response.
- Only text fields (`Scenario`, `Account Group L0`, etc.) go in `filters`.

```
Use: mcp__datarails-finance-os__aggregate_table_data
Parameters:
  table_id: <financials_table_id from list_finance_tables>
  dimensions: [<chosen drill-down fields>]
  metrics: [{"field": "Amount", "agg": "SUM"}]
  filters: [<DR.GET dimension filters + any global filters>]
```

**Important:** Use `aggregate_table_data` (not `get_records_by_filter`) because it has no row limit and returns properly computed totals.

## Step 6: Validate and Present

1. **Validate:** If the user provided an expected total (from their Excel cell), compare the aggregation total to it. If they match (within $1), proceed. If not, warn the user and explain the difference may be due to global filters not accounted for.

2. **Present the breakdown:**

> ### Drill-Down: Revenues, Actuals, Jan-26
>
> | Account Name | Amount |
> |---|---|
> | Subscription Revenue | $1,100,000 |
> | Implementation Revenue | $134,567 |
> | **Total** | **$1,234,567** |
>
> Sorted by absolute amount. Total validated against source.

**Formatting rules:**
- Format numbers with commas and dollar signs
- Sort rows by absolute amount descending
- If more than 30 rows, show top 20 and summarize rest as "Other (N items)"
- Always show the total row at the bottom

## Step 7: Offer Follow-ups

After presenting results, offer:
- "Want me to break this down further by another field?"
- "Should I compare this to Budget or another scenario?"
- "Want to drill into one of these line items?"

## Examples

**User:** "Break down my January 2026 Actuals revenue by account"
1. Map to filters: Scenario=Actuals, Reporting Date=Jan 2026, Account L1=Revenue
2. Ask about global filters
3. Aggregate by Account Name/Account Full
4. Present breakdown table

**User:** "Here's my formula: =DR.GET(Value, "[DR_ACC_L1.5]", $A6, "[Scenario]", $B$1, "[Reporting Date]", B$5) - the values are Revenues, Actuals, and Jan 2026. Break it down."
1. Parse: DR_ACC_L1.5=Revenues, Scenario=Actuals, Reporting Date=Jan 2026
2. Ask about global filters
3. Ask which field to break down by
4. Present breakdown table
