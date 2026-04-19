# Changelog

All notable changes to the AI Coding Playbook will be noted here.

The format loosely follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Dates are ISO (YYYY-MM-DD).

## [0.1.0] — 2026-04-19

First public version. Complete TOC (21 chapters) and initial asset coverage.

### Added

**Foundations (Part I):**
- Ch 01 — Getting Started with Agentic Coding (mental model, install, first session; Gemini CLI and Claude Code walkthroughs).
- Ch 02 — The Agentic Coding Landscape (Gemini CLI, Claude Code, Antigravity, Cursor, Aider, Cline, Continue.dev, Windsurf).
- Ch 03 — Effective Prompting for Agents (the four-part brief, spec-first habit, anti-patterns).

**Giving the Agent Context (Part II):**
- Ch 04 — Memory Systems (`GEMINI.md`, `CLAUDE.md`, three-tier hierarchy, path-scoped rules).
- Ch 05 — Custom Slash Commands (concept + Gemini TOML walkthrough + Claude Markdown walkthrough).
- Ch 06 — Agent Skills (concept + Claude Code walkthrough + Gemini CLI skills + extensions).

**Connecting to the World (Part III):**
- Ch 07 — MCP Servers (concept + both-tool config walkthroughs).
- Ch 08 — Hooks and Automation (concept + both-tool walkthroughs with runnable examples).
- Ch 13 — Tool Connectivity (Google Cloud, BigQuery, Firebase, internal APIs; auth patterns).

**Context Economics (Part IV):**
- Ch 09 — Preventing Context Rot (four symptoms, seven durable habits).
- Ch 10 — Saving Tokens (economics, seven levers, worked cost example).
- Ch 11 — Subagents and Parallelization.

**Wider Ecosystem (Part V):**
- Ch 12 — Research and Web Integration.
- Ch 14 — IDE Integration (VS Code, JetBrains, Firebase Studio, Cloud Workstations).
- Ch 15 — Keybindings and Shortcuts.
- Ch 16 — Test Generation and Automation.
- Ch 17 — UI Generation (Stitch, Claude Design, v0, Figma Dev Mode MCP).
- Ch 18 — Local Models for Coding (Qwen3-Coder, DeepSeek, Gemma 4, Ollama, vLLM, Vertex Model Garden).

**Advanced Platforms (Part VI):**
- Ch 19 — Google Antigravity (deep-dive on Google's agentic IDE).
- Ch 20 — Agent SDKs (Google ADK and Claude Agent SDK).
- Ch 21 — Advanced Workflows and Playbooks (six end-to-end worked examples).

**Assets:**
- Slash commands for both tools (`research`, `commit`, `review`, `plan`).
- Skills for both tools (`pr-description`, `test-gen`).
- Hook scripts (`block-rm-rf`, `format-after-edit`, `audit-log`) for both tools.
- MCP configs (starter `.mcp.json`, `mcpServers` settings).
- `settings.json` starters for both CLIs.

**Reference:**
- `README.md`, `CONTRIBUTING.md`, `LICENSE` (MIT), `.gitignore`, `AGENTS.md` (with `CLAUDE.md` and `GEMINI.md` symlinks).
- `docs/TABLE_OF_CONTENTS.md`, `docs/GLOSSARY.md`, `docs/FAQ.md`, `docs/ROADMAP.md`.

---

Older entries will appear here as the playbook evolves.
