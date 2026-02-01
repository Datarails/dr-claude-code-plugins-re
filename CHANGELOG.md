# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-20

### Added

- Initial release of Datarails Finance OS plugin for Claude Code
- **Skills**
  - `/dr-auth` - Authentication with Datarails (browser cookie extraction)
  - `/dr-tables` - Table discovery and schema exploration
  - `/dr-profile` - Numeric and categorical field profiling
  - `/dr-anomalies` - Automated anomaly detection
  - `/dr-query` - Record filtering and custom queries
- **Agents**
  - Finance Analyst agent for comprehensive data analysis
- **Documentation**
  - Full README with installation and usage instructions
  - Each skill documented with examples
- MCP server integration via `.mcp.json`
- Plugin manifest for distribution

### Technical Details

- Bundled MCP server: `datarails-finance-os`
- Requires Python package: `datarails-finance-os-mcp`
- Supports dev and prod environments
- Secure credential storage via system keychain
