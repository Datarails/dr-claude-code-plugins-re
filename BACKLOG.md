# Backlog

- [ ] **Eliminate MCP code duplication** — refactor `dr-datarails-mcp-remote` to use `datarails_sdk` internally instead of its own `DatarailsClient`. The MCP becomes a thin transport layer wrapping this SDK.
- [ ] **CI/CD for dr-datarails-sdk** — set up automated publishing to JFrog on merge (similar to `dr-finance-os/sdk-publish.yml`). Currently published manually.
