# Claude Code — MCP assets

## Files

- [`team-mcp.json`](./team-mcp.json) — a starter `.mcp.json` to commit at a project root. Engineers cloning the repo automatically get the same MCP servers on `claude` startup.

## Install

```bash
cp team-mcp.json <your-repo-root>/.mcp.json
```

Edit server entries to fit the project. Keep secret values out — reference them with `${ENV_VAR}` instead.

## Companion reading

[Chapter 7 — MCP Servers](../../../chapters/07-mcp/README.md) has the concept framing; [the Claude Code realization](../../../chapters/07-mcp/claude-code/README.md) has the step-by-step `claude mcp add` walkthrough and the permissions-model integration.
