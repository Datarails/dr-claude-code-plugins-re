# chatgpt-stable — load-bearing branch

This branch is the plugin bundle served to **ChatGPT** by the remote MCP server
(`datarails-finance-os-mcp`), which clones it into `plugin_content/` at Docker
build time (`PLUGIN_BRANCH=chatgpt-stable`).

It is frozen on the **deprecated** tool set (seeded from `v2.6.4`) because the
official ChatGPT app has not yet upgraded to the new tools. Claude installs
`main` directly and is unaffected.

**Rules:**
- Land ChatGPT fixes here only; keep skills compatible with the deprecated tools.
- Do **not** merge `main` into this branch (it carries the new tool surface).
- Retire by pointing the MCP `PLUGIN_BRANCH` back to `main` once ChatGPT upgrades.

Tracking: DR-50140.
