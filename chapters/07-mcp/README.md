# Chapter 7 — MCP Servers

> The protocol that lets your agent talk to the rest of your software. An introduction that takes the mystery out, and a warning about the sharp edges.

---

## The concept

An agent is useful in proportion to what it can *do*. Out of the box, an agentic CLI can read files, edit files, run shell commands, and hit the open web. That covers a lot, but not: your issue tracker, your CRM, your internal APIs, your design system, your databases, your feature flags, your cloud resources.

MCP — the **Model Context Protocol** ([modelcontextprotocol.io](https://modelcontextprotocol.io)) — is the standard that closes that gap. An **MCP server** exposes a set of tools and (optionally) resources over a simple JSON-RPC protocol. An **MCP client** (your CLI) connects to that server and the server's tools become available to the agent in its tool-call loop.

It's the USB of agentic coding. One protocol, many servers, many clients. Anthropic introduced it; Google adopted it in Gemini CLI and the Agent Development Kit; Cursor, Windsurf, VS Code agent modes, and most serious agentic tools support it. If you learn MCP once, you can wire capability into any of them.

## What an MCP server actually is

A process that speaks JSON-RPC and advertises:

- **Tools** — named, typed operations the agent can call. (`search_issues`, `create_branch`, `query_bigquery_table`.)
- **Resources** — optional; named read-only data sources.
- **Prompts** — optional; named, pre-packaged prompt templates.

Connection happens over one of three transports:

- **stdio** — the server is a subprocess, you talk over stdin/stdout. Most local servers.
- **streamable http** — the server is a remote HTTP endpoint. Most hosted servers.
- **SSE** — server-sent events over HTTP. Older pattern, still common.

The transport is configuration; from the agent's perspective, all three look the same.

## When to add an MCP server

When all three are true:

1. The agent needs to do something it can't do with file edits + shell.
2. There's already an MCP server for it (either official, or one you can write in a few hours).
3. The benefit outweighs the cost — because MCP servers have a cost, and it's usually context.

### The cost you're paying

Every connected MCP server contributes, at session start, a description of every tool it exposes. If you wire up six servers each exposing ten tools, you've committed a few thousand tokens of tool descriptions to every single turn. On a long session that's real money — and more importantly, it crowds out room for the actual work.

The single most common MCP mistake is connecting everything you can think of "just in case." A server you use once a week should not be loaded every session.

Both CLIs support scoping servers per-project (so `.mcp.json` in a billing repo loads the Stripe server, while your CRM repo loads the Salesforce server, and neither loads when you're in a different project). Use this.

## When to write your own MCP server

When an internal system is important enough that your team uses it daily, wrapping it in an MCP server is usually worth the afternoon. The spec is small; the tooling is good; the payoff is "every new engineer's agent can talk to this system the day they onboard."

Watch for:

- **Don't expose destructive operations without confirmation.** Your MCP server controls what the agent *can* do; pair risky tools with tight permissions in the client.
- **Be careful with secrets.** Servers see whatever inputs the agent gives. Never have the agent pass secrets through tool call inputs — use environment variables on the server side.
- **Version your tool signatures.** Once a tool is in production use, its name and schema are a public API. Break it carefully.

## Useful servers to know about

A non-exhaustive list of MCP servers that pay for themselves fast (see the [MCP servers index](https://github.com/modelcontextprotocol/servers) for the full catalog):

- **Filesystem** (`@modelcontextprotocol/server-filesystem`) — scoped file access; useful when you want the agent to read/write in a specific directory without exposing the whole machine.
- **Git** (`@modelcontextprotocol/server-git`) — richer git operations than shell `git`, including history queries.
- **Fetch** — disciplined URL fetching with caching.
- **Postgres / SQLite** — parameterized queries against a database. Read-only recommended.
- **Figma Dev Mode** — discussed in detail in Ch. 17.
- **Stripe, Notion, Linear, Asana, Slack, Sentry** — most SaaS vendors now ship official or community servers.
- **Google / Cloud** — official servers for Google Drive, Calendar, Gmail; for GCP services, prefer the [Agent Development Kit's](https://google.github.io/adk-docs/) direct Google Cloud integrations covered in Ch. 20.

Before adding a third-party server, read its source or docs. You're giving it access to your agent's session.

## The permissions principle

Every MCP server is a capability you're granting the agent. Apply the principle of least privilege:

- **Prefer scoped servers.** The filesystem server should be pointed at the project root, not `/`.
- **Prefer read-only where possible.** A `query` tool is less dangerous than an `execute` tool.
- **Prefer per-project scoping over global.** If only the billing repo needs Stripe, only the billing repo should have Stripe loaded.
- **Audit what you've loaded.** Both tools let you list active servers. Do it occasionally.

## Realizations

- [Claude Code — configuring MCP](./claude-code/README.md) — `claude mcp add`, transports, per-scope configuration, filesystem + Figma examples.
- [Gemini CLI — configuring MCP](./gemini-cli/README.md) — `mcpServers` in settings and in extensions, examples.

## A note on the converging standard

MCP is now the de facto standard — Anthropic, Google, Microsoft (via VS Code's Copilot agent mode), Cursor, and most independent tool vendors support it. A capability you expose as an MCP server is portable across every agent you're likely to use. That's the bet worth making.

The one current hole: **Google Antigravity does not support MCP as of April 2026** in its initial releases; Google has signaled it's landing, and some sources report it has landed in recent builds — verify in-product. For anything Antigravity-specific, see Ch. 19.

## References

- [Model Context Protocol — introduction](https://modelcontextprotocol.io/introduction)
- [MCP server catalog](https://github.com/modelcontextprotocol/servers)
- [Claude Code MCP docs](https://docs.claude.com/en/docs/claude-code/mcp)
- [Gemini CLI MCP server docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md)

## What's next

- [Chapter 8 — Hooks and Automation](../08-hooks/README.md) — the other side of capability: constraints.
- [Chapter 17 — UI Generation](../17-ui-generation/README.md) — where Figma Dev Mode MCP pulls its weight.
