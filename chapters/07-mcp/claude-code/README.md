# Claude Code — Configuring MCP Servers

Step-by-step. Verified against [Claude Code MCP docs](https://docs.claude.com/en/docs/claude-code/mcp).

## Two ways to configure

1. **`claude mcp add` (recommended for everyday use)** — an interactive CLI that writes to the right file at the right scope.
2. **Edit JSON directly** — for scripting, or when you want to commit a `.mcp.json` to share with the team.

## Scopes

- **Local / user:** `~/.claude.json` under `mcpServers` — applies to you across projects.
- **Project (committed):** `.mcp.json` at the repo root — shared with everyone who clones.
- **Project (not committed):** `.claude/settings.local.json` — your personal override for this project.

`claude mcp add --scope project …` writes to `.mcp.json`. `--scope user` writes to `~/.claude.json`. Default is user.

## The server config shape

```json
{
  "mcpServers": {
    "<server-name>": {
      "type": "stdio",
      "command": "<for stdio>",
      "args": ["..."],
      "url": "<for http / sse>",
      "env": { "VAR": "value" },
      "headers": { "Authorization": "Bearer ${TOKEN}" }
    }
  }
}
```

`type` is `stdio`, `http`, or `sse`. Env-var expansion (`${VAR}`, `${VAR:-default}`) works in `command`, `args`, `env`, `url`, `headers`.

## Step 1 — Add the Filesystem server (CLI way)

```bash
claude mcp add \
  --transport stdio \
  --scope user \
  filesystem \
  -- \
  npx -y @modelcontextprotocol/server-filesystem ~/projects/your-repo
```

The `--` separates Claude's arguments from the server's. Restart the session and verify:

```
/mcp
```

The `filesystem` server should show connected.

## Step 2 — Add a remote HTTP server (CLI way)

```bash
claude mcp add \
  --transport http \
  --scope user \
  notion \
  https://mcp.notion.com/mcp
```

Some servers require an auth header:

```bash
claude mcp add \
  --transport http \
  --scope user \
  --header "Authorization: Bearer ${MCP_NOTION_TOKEN}" \
  notion \
  https://mcp.notion.com/mcp
```

`${MCP_NOTION_TOKEN}` is resolved from your environment at session start, not baked in.

## Step 3 — Commit a shared `.mcp.json` for your team

At the repo root, `.mcp.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${CLAUDE_PROJECT_DIR}"]
    },
    "billing-db": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "${BILLING_DATABASE_URL}"]
    }
  }
}
```

`${CLAUDE_PROJECT_DIR}` is set by the CLI; `${BILLING_DATABASE_URL}` comes from each engineer's shell. Secrets stay out of the repo.

## Step 4 — Figma Dev Mode MCP

Figma ships an MCP server for the Dev Mode design handoff (see Ch. 17). Once enabled in the desktop app:

```bash
claude mcp add --transport http figma http://127.0.0.1:3845/mcp
```

Or the hosted variant:

```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

## Step 5 — Narrowing tool exposure

Claude Code supports filtering which of a server's tools enter context. Edit the relevant `mcpServers` entry:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com/mcp",
      "toolFilters": { "include": ["search_issues", "get_pr"] }
    }
  }
}
```

(Field name has varied across versions — check the [current docs](https://docs.claude.com/en/docs/claude-code/mcp) for the exact key. The intent is the same.)

## Inspecting and debugging

- **`/mcp`** — list every configured server, status, tools exposed.
- **`/mcp restart <server>`** — restart a specific server.
- Logs: `~/.claude/logs/mcp-*.log` or similar, depending on version.

## Permissions interact with MCP

MCP tools obey the same `permissions` model as built-in tools. You can allow, ask, or deny per tool:

```json
{
  "permissions": {
    "allow": ["mcp__filesystem__read_file", "mcp__filesystem__list_directory"],
    "ask":   ["mcp__filesystem__write_file"],
    "deny":  ["mcp__filesystem__delete_file"]
  }
}
```

The tool name pattern is `mcp__<server>__<tool>`. This is how you harden an MCP server's surface without modifying the server itself.

## Security checklist

- **Filesystem server: scope to the project**, never `/` or `$HOME`.
- **Secrets live in env vars**, not in `.mcp.json`. The file is committed.
- **Pair write/execute tools with `ask` permission** rather than `allow`.
- **Audit `/mcp`** monthly. Remove servers you haven't used.

## Troubleshooting

- **Server won't connect.** Run the command manually in a shell. If it fails there, fix the command.
- **Tools don't appear.** Run `/mcp tools <server>`; servers occasionally declare capabilities only as `resources`, which don't show in the tool list.
- **Too many tokens spent on tool descriptions.** Use `toolFilters` (or the server's native filter), or disconnect servers you rarely use.

## References

- [Claude Code MCP docs](https://docs.claude.com/en/docs/claude-code/mcp)
- [MCP spec](https://modelcontextprotocol.io)
- [MCP server catalog](https://github.com/modelcontextprotocol/servers)
- [Settings + permissions](https://code.claude.com/docs/en/settings)
