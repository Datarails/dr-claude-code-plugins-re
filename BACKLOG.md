# Backlog — Must Haves for Production

- [ ] **Register OAuth client_id** — register `claude-code` (or similar) with auth.datarails.com so `/dr-auth` works. Blocked on team (see QUESTIONS_FOR_TEAM.md).
- [ ] **Publish `dr-datarails-sdk`** — set up CI/CD to publish Python + TypeScript packages so the plugin hook can `pip install` / `npm install` instead of requiring local PYTHONPATH. Blocked on team (see QUESTIONS_FOR_TEAM.md).
- [ ] **Update hook for production** — once SDK is published, change `hooks.json` from PYTHONPATH check to `pip install dr-datarails-sdk`.
- [ ] **Eliminate MCP code duplication** — refactor `dr-datarails-mcp-remote` to use `datarails_sdk` internally instead of its own `DatarailsClient`.
