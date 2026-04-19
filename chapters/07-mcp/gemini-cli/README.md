# Gemini CLI — Configuring MCP Servers

Step-by-step. Verified against [Gemini CLI MCP server docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md).

## Where servers are configured

Three places; they merge, with later (more specific) winning on collisions:

1. **User:** `~/.gemini/settings.json` under `mcpServers`.
2. **Workspace:** `.gemini/settings.json` under `mcpServers`.
3. **Extensions:** each installed extension's `gemini-extension.json` can declare `mcpServers`.

## The server config shape

Each server is a named entry with a transport (`command`, `url`, or `httpUrl`) plus options:

```json
{
  "mcpServers": {
    "<server-name>": {
      "command": "<for stdio>",
      "args": ["..."],
      "url": "<for SSE>",
      "httpUrl": "<for streamable HTTP>",
      "env": { "VAR": "value" },
      "cwd": "<optional working dir>",
      "headers": { "Authorization": "..." },
      "timeout": 600000,
      "trust": false,
      "includeTools": ["tool_name"],
      "excludeTools": ["tool_name"]
    }
  }
}
```

Use exactly one of `command` / `url` / `httpUrl`. Env-var expansion (`$VAR`, `${VAR}`, Windows `%VAR%`) works inside `command`, `args`, `env`, `url`, `headers`.

`includeTools` and `excludeTools` let you filter *which* of the server's tools actually reach the agent — a key lever for keeping context small.

## Step 1 — A concrete example (Filesystem)

Edit `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/projects/your-repo"
      ]
    }
  }
}
```

Restart Gemini CLI. Verify:

```
/mcp
```

The `filesystem` server should be listed as connected, and its tools (`read_file`, `write_file`, `list_directory`, etc.) should be available.

## Step 2 — Scoping to a single project

Put the same server under `.gemini/settings.json` in the project:

```json
{
  "mcpServers": {
    "billing-db": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres",
        "${DATABASE_URL}"]
    }
  }
}
```

`${DATABASE_URL}` is read from your env. This server loads only when you open Gemini CLI inside this repo.

## Step 3 — A remote HTTP server (Figma Dev Mode)

```json
{
  "mcpServers": {
    "figma": {
      "httpUrl": "http://127.0.0.1:3845/mcp",
      "timeout": 30000
    }
  }
}
```

This assumes you've enabled the Figma Dev Mode MCP server in the Figma desktop app ([Figma docs](https://developers.figma.com/docs/figma-mcp-server/)). The remote hosted variant is:

```json
{
  "mcpServers": {
    "figma": { "httpUrl": "https://mcp.figma.com/mcp" }
  }
}
```

Covered in detail in Ch. 17.

## Step 4 — Shipping MCP servers in an extension

Inside `gemini-extension.json`:

```json
{
  "name": "my-team-toolkit",
  "version": "0.1.0",
  "mcpServers": {
    "internal-api": {
      "command": "node",
      "args": ["${GEMINI_EXTENSION_DIR}/bin/mcp-server.js"],
      "env": { "API_BASE_URL": "https://internal.example.com" }
    }
  },
  "settings": [
    {
      "name": "API_TOKEN",
      "envVar": "INTERNAL_API_TOKEN",
      "sensitive": true
    }
  ]
}
```

Team installs with `gemini extensions install <git-url>`, gets the MCP server and any required config prompts in one step.

## Inspecting active servers

- **`/mcp`** — list servers, their status, and tools exposed.
- **`/mcp restart <name>`** — restart a misbehaving server.
- **`/mcp logs <name>`** — recent server output.

## Narrowing tool exposure

If a server exposes 30 tools but you only use 3, set `includeTools` to drop the rest from context:

```json
{
  "mcpServers": {
    "github": {
      "httpUrl": "https://mcp.github.com/mcp",
      "includeTools": ["search_issues", "get_pr", "create_comment"]
    }
  }
}
```

Same idea with `excludeTools` when you want to block specific destructive operations.

## Security checklist

- **Scope filesystem servers.** Point at a specific directory, not `/`.
- **Use env vars for secrets**, never inline in settings.
- **Mark `"trust": false`** (the default) unless you genuinely trust the server; with `trust: false` the CLI prompts before risky tool calls.
- **Audit your installed servers** periodically. `/mcp` is free.

## Troubleshooting

- **Server shows as "failed."** Run its `command` manually in a shell; it should print a JSON-RPC handshake on stdin. If it crashes, fix the command or missing dependency.
- **Tools don't show up.** The server might have declared them under `resources` or `prompts`; only `tools` show in the tool list.
- **Agent keeps ignoring the server.** The server's tool descriptions might be uninformative. The model picks tools by description.

## References

- [MCP server docs (Gemini CLI)](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)
- [Extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
- [MCP spec](https://modelcontextprotocol.io)
- [Community MCP server catalog](https://github.com/modelcontextprotocol/servers)
