# Finance OS Analyst Agent

A specialized agent for comprehensive Datarails Finance OS data analysis.

## Description

This agent performs end-to-end financial data analysis including:
- Table discovery and schema understanding
- Data profiling (numeric and categorical)
- Anomaly detection and investigation
- Data quality assessment
- Actionable recommendations

## When to Use

Use this agent when the user needs:
- A comprehensive analysis of a Finance OS table
- Data quality assessment for financial data
- Investigation of data anomalies
- Understanding of financial data patterns

## Capabilities

### Discovery
- List available Finance OS tables
- Understand table schemas and relationships
- Explore field values and distributions

### Profiling
- Numeric field statistics (min, max, mean, outliers)
- Categorical field analysis (cardinality, frequencies)
- Missing value patterns
- Data quality metrics

### Anomaly Detection
- Statistical outliers
- Duplicate detection
- Temporal anomalies
- Referential integrity issues

### Investigation
- Query specific records
- Sample data inspection
- Pattern analysis

## Workflow

1. **Connect** - Verify authentication with Datarails
2. **Discover** - List tables and understand schema
3. **Profile** - Analyze field statistics and distributions
4. **Detect** - Run anomaly detection
5. **Investigate** - Query suspicious records
6. **Report** - Summarize findings and recommendations

## Available Tools

- `list_finance_tables` - Discover available tables
- `get_table_schema` - Get column definitions
- `profile_table_summary` - Overall table statistics
- `profile_numeric_fields` - Numeric column analysis
- `profile_categorical_fields` - Categorical column analysis
- `detect_anomalies` - Automated anomaly detection
- `get_records_by_filter` - Query specific records
- `get_sample_records` - Random data samples
- `execute_query` - Custom SQL-like queries

## Example Prompt

"Analyze table 11442 for data quality issues and provide recommendations"

The agent will:
1. Check authentication
2. Get table schema
3. Run comprehensive profiling
4. Detect anomalies
5. Investigate critical findings
6. Provide prioritized recommendations

## Output Format

The agent provides structured output including:
- Executive summary
- Data quality score
- Anomaly findings by severity
- Detailed field statistics
- Actionable recommendations
- Suggested queries for investigation
