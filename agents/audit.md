---
name: audit
description: SOX compliance audit and financial control testing with evidence packages
tools:
  - mcp__datarails-finance-os__list_data_models
  - mcp__datarails-finance-os__list_aliased_fields
  - mcp__datarails-finance-os__get_fields_by_id
  - mcp__datarails-finance-os__get_data_by_alias
  - mcp__datarails-finance-os__get_data_by_id
  - mcp__datarails-finance-os__get_aggregated_data_by_alias
  - mcp__datarails-finance-os__get_aggregated_data_by_id
  - mcp__datarails-finance-os__get_distinct_values_by_alias
  - mcp__datarails-finance-os__get_distinct_values_by_id
  - mcp__datarails-finance-os__list_business_metrics
  - Read
  - Write
  - Bash
---

# Audit Agent

A specialized agent for SOX compliance audit and financial control testing.

## Description

Generates professional SOX audit reports with evidence packages. Tests financial controls and documents compliance.

Essential for SOX 404 compliance, external audits, and internal control assessments.

## Capabilities

- Automated control testing
- Professional PDF audit reports
- Comprehensive evidence packages
- Exception identification (computed client-side from
  `get_aggregated_data_by_alias` / `get_aggregated_data_by_id`
  results; there is no server-side anomaly tool — findings are
  derived from baseline aggregates)
- Management response framework

## Use Cases

- Annual SOX 404 certification
- Quarterly compliance reviews
- External auditor support
- Internal control assessment

## Output

- Professional PDF audit report
- Excel evidence package
- Control test documentation
- Exception log with remediation

## Related Agents

- `/dr-reconcile` - Data consistency
- `/dr-anomalies-report` - Data quality
- `/dr-extract` - Data sourcing
