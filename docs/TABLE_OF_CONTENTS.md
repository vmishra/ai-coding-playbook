# Table of Contents

Chapters are organized around a durable concept first, tool-specific realizations second. Read in order for a complete path, or skip around using the recommended paths in the [main README](../README.md).

## Part I — Foundations

1. **[Getting Started with Agentic Coding](../chapters/01-getting-started/README.md)** — Installing Gemini CLI and Claude Code. First-session mechanics. The mental model that everything else in this book depends on.
2. **[The Agentic Coding Landscape](../chapters/02-landscape/README.md)** — Gemini CLI, Claude Code, Antigravity, Cursor, Aider. How they differ, where each wins, and what stays true across all of them.
3. **[Effective Prompting for Agents](../chapters/03-prompting/README.md)** — Briefing an agent is not the same as prompting a chat model. Task framing, goal-vs-steps, what to leave out.

## Part II — Giving the Agent Context

4. **[Memory Systems](../chapters/04-memory/README.md)** — `GEMINI.md`, `CLAUDE.md`, project-level vs personal memory, file-based memory patterns, what belongs there and what doesn't.
5. **[Custom Slash Commands](../chapters/05-slash-commands/README.md)** — Turning prompts you've typed more than three times into permanent, shareable commands. TOML vs Markdown formats. Arg handling.
6. **[Agent Skills](../chapters/06-skills/README.md)** — Skills as composable capabilities. When to prefer a skill over a slash command over a subagent. Skill design patterns.

## Part III — Connecting the Agent to the World

7. **[MCP Servers](../chapters/07-mcp/README.md)** — Model Context Protocol, what it actually solves, how to configure servers in both tools, building your own, and when you shouldn't.
8. **[Hooks and Automation](../chapters/08-hooks/README.md)** — Policy as code. Blocking bad commits, routing sensitive reads, auto-running formatters. The hook event model.
9. **[Tool Connectivity — Google Cloud, BigQuery, Firebase, APIs](../chapters/13-connectivity/README.md)** — Wiring agents into real infrastructure. Auth patterns. Principle of least privilege for agents.

## Part IV — Context Economics

10. **[Preventing Context Rot](../chapters/09-context-rot/README.md)** — Why long sessions degrade. Compaction, checkpointing, and when to start fresh (the answer is "sooner than you think").
11. **[Saving Tokens — The Economics Chapter](../chapters/10-saving-tokens/README.md)** — The one most people want first. Prompt caching, explore-first-read-narrowly, subagent offloading, model routing, the ratio that predicts whether a session will succeed, and a concrete cost playbook.
12. **[Subagents and Parallelization](../chapters/11-subagents/README.md)** — When to delegate. How to brief a subagent. Failure modes of parallel agent work.

## Part V — Working with the Wider Ecosystem

13. **[Research and Web Integration](../chapters/12-research/README.md)** — Using `WebSearch` and `WebFetch` as real research primitives. Citations. Caching. A research slash command you'll actually use.
14. **[IDE Integration](../chapters/14-ide/README.md)** — VS Code, JetBrains, Firebase Studio, Cloud Workstations. When the CLI wins, when the IDE wins.
15. **[Keybindings and Shortcuts](../chapters/15-shortcuts/README.md)** — The shortcuts that pay for themselves in the first week.
16. **[Test Generation and Automation](../chapters/16-testing/README.md)** — Generating tests that are actually useful. Running them in-loop. Preventing the "tests pass, feature broken" failure.
17. **[UI Generation — Stitch, v0, Figma Dev Mode](../chapters/17-ui-generation/README.md)** — From a sketch to a working component. Figma Dev Mode MCP. How to bring generated UI back into a real codebase.
18. **[Local Models for Coding](../chapters/18-local-models/README.md)** — Gemma, Qwen3-Coder, DeepSeek. Ollama, LM Studio, vLLM. Where local wins, where it doesn't.

## Part VI — Advanced Platforms and Frameworks

19. **[Google Antigravity](../chapters/19-antigravity/README.md)** — Google's agentic IDE. What's genuinely new versus what's a repackaging. When to reach for it over Gemini CLI alone.
20. **[Agent SDKs — Google ADK and Claude Agent SDK](../chapters/20-agent-sdks/README.md)** — Moving past the CLI. Building custom agents programmatically. Multi-agent systems on Vertex AI.
21. **[Advanced Workflows and Playbooks](../chapters/21-workflows/README.md)** — End-to-end recipes: bug triage, large migrations, feature shipping, oncall triage, code review at scale.

## Appendices

- [Glossary](./GLOSSARY.md)
- [FAQ](./FAQ.md)
- [Roadmap](./ROADMAP.md)
- [Changelog](../CHANGELOG.md)
