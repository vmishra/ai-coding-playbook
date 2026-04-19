# Gemini CLI settings examples

## Files

- [`settings.example.json`](./settings.example.json) — a starter `~/.gemini/settings.json` with sensible defaults, basic `excludeTools` safety, a filesystem MCP server, and the two Gemini hook assets wired in.
- [`mcp-example.json`](./mcp-example.json) — just the `mcpServers` block if you want to add MCP without touching other settings.

## Install

**Do not wholesale replace your existing `~/.gemini/settings.json`.** Merge selectively.

If you don't have a settings file yet:

```bash
mkdir -p ~/.gemini
cp settings.example.json ~/.gemini/settings.json
```

Then install the referenced hooks and MCP servers from [the hook assets](../hooks/) and [Chapter 7's MCP walkthrough](../../../chapters/07-mcp/gemini-cli/README.md).

## What each section is for

- **`context.fileName`**: The list of filenames the CLI loads as context files. Including `AGENTS.md` supports the emerging cross-tool convention.
- **`excludeTools`**: Coarse safety rails without hook scripts — blocks known-dangerous shell patterns.
- **`mcpServers`**: MCP server wiring.
- **`hooks`**: Hook wiring.

See [Chapter 4](../../../chapters/04-memory/README.md) (memory), [Chapter 7](../../../chapters/07-mcp/gemini-cli/README.md) (MCP), and [Chapter 8](../../../chapters/08-hooks/gemini-cli/README.md) (hooks).
