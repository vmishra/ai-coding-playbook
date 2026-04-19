<h1 align="center">The AI Coding Playbook</h1>

<p align="center">
  <em>Everything useful I've learned running agents against real codebases.<br/>
  21 chapters. Both Gemini CLI and Claude Code. Every example is runnable.</em>
</p>

<p align="center">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <img src="https://img.shields.io/badge/chapters-21-brightgreen.svg" alt="21 chapters">
  <img src="https://img.shields.io/badge/tools-Gemini%20CLI%20%2B%20Claude%20Code-orange.svg" alt="Gemini CLI + Claude Code">
  <img src="https://img.shields.io/badge/verified-April%202026-lightgrey.svg" alt="Verified April 2026">
  <a href="https://github.com/vmishra/ai-coding-playbook/stargazers"><img src="https://img.shields.io/github/stars/vmishra/ai-coding-playbook?style=social" alt="Stars"></a>
</p>

---

Every post about "AI coding" is one of three things: a marketing page for a tool you already know exists, a three-minute YouTube demo that doesn't survive a real codebase, or a tutorial from six months ago — which in this space is ancient.

This is the reference I wish existed when `gemini` and `claude` went from "neat demo" to the thing I reach for before I start typing. It covers both CLIs (Gemini first because of Google-native integration; Claude a close second because its primitives are still the most mature), plus Antigravity, Stitch, Claude Design, Firebase Studio, Vertex AI Model Garden, Google ADK, the Claude Agent SDK, and the current state of local coding models.

Written by [Vikas Mishra](https://github.com/vmishra), a working engineer at Google, from actual usage — not transcripts of someone else's tutorials.

## What's inside

|     |     |
| :-- | :-- |
| **21 chapters** | Concept first, tool-specific realization second — so the chapters don't rot every time a vendor ships a release |
| **4 slash commands × 2 tools** | `/research`, `/commit`, `/review`, `/plan` — tightly scoped `allowed-tools`, team-shareable |
| **2 skills × 2 tools** | `pr-description` and `test-gen`, written to avoid the "tests pass while the feature is broken" failure mode |
| **5 hook scripts** | `block-rm-rf`, `format-after-edit`, `audit-log`, plus the Gemini CLI mirrors — each ships with a test payload in the header |
| **Config starters** | `settings.json` for both CLIs, a committable `.mcp.json`, `GEMINI.md` / `CLAUDE.md` templates |
| **Six end-to-end playbooks** | Bug triage, multi-file migration, spec-to-shipped, on-call, research-driven decisions, PR triage at scale |
| **Primary sources throughout** | Every claim links to an official doc. Broken claim → filed issue → fixed in a week. |

## The mental model this whole book depends on

```
┌─────────────────────────────────────────────────────────────┐
│                      The Context Window                     │
│                                                             │
│   [ system prompt ][ your brief ][ files the agent read ]   │
│   [ tool results ][ the agent's own plans and notes ]       │
│   [ intermediate outputs ][ your follow-up messages ]       │
│                                                             │
│                  Everything the model sees                  │
└─────────────────────────────────────────────────────────────┘
```

The agent has exactly one input: this window. Most "the agent is confused" complaints reduce to "the relevant thing isn't in the window" or "the window is so full the relevant thing got crowded out." Every technique in this book is about controlling what lives there, for how long, at what position.

Chapter 1 opens with this diagram. Everything else is the consequence.

## Install the assets in 60 seconds

```bash
git clone https://github.com/vmishra/ai-coding-playbook.git
cd ai-coding-playbook

# Gemini CLI
mkdir -p ~/.gemini/{commands,skills,hooks}
cp -r assets/gemini-cli/commands/* ~/.gemini/commands/
cp -r assets/gemini-cli/skills/*   ~/.gemini/skills/
cp    assets/gemini-cli/hooks/*.sh ~/.gemini/hooks/ && chmod +x ~/.gemini/hooks/*.sh

# Claude Code
mkdir -p ~/.claude/{commands,skills,hooks}
cp -r assets/claude-code/commands/* ~/.claude/commands/
cp -r assets/claude-code/skills/*   ~/.claude/skills/
cp    assets/claude-code/hooks/*.sh ~/.claude/hooks/ && chmod +x ~/.claude/hooks/*.sh
```

Hooks and MCP servers need a line in `settings.json` before they fire — snippets live in each asset's README, copy exactly the ones you want. **Read what you're loading.** An MCP server you don't trust is still a capability you just gave an agent.

## Table of contents

```
Part I · Foundations
  01  Getting Started with Agentic Coding
  02  The Agentic Coding Landscape
  03  Effective Prompting for Agents

Part II · Giving the Agent Context
  04  Memory Systems               GEMINI.md, CLAUDE.md, path-scoped rules
  05  Custom Slash Commands        TOML + Markdown walkthroughs
  06  Agent Skills                 Discovery model, context:fork, extensions

Part III · Connecting to the World
  07  MCP Servers                  Concept + both-tool config recipes
  08  Hooks and Automation         Policy as code, with scripts
  13  Tool Connectivity            GCP, BigQuery, Firebase, internal APIs

Part IV · Context Economics
  09  Preventing Context Rot       Four symptoms, seven habits
  10  Saving Tokens                Where the money goes, and the seven levers
  11  Subagents and Parallelization

Part V · Wider Ecosystem
  12  Research and Web Integration
  14  IDE Integration              VS Code, JetBrains, Firebase Studio, Cloud Workstations
  15  Keybindings and Shortcuts
  16  Test Generation and Automation
  17  UI Generation                Stitch, Claude Design, v0, Figma Dev Mode MCP
  18  Local Models for Coding      Qwen3-Coder, Gemma 4, DeepSeek, Ollama, Vertex

Part VI · Advanced
  19  Google Antigravity
  20  Agent SDKs                   Google ADK + Claude Agent SDK
  21  Advanced Workflows           Six end-to-end recipes
```

Annotated TOC with descriptions: [`docs/TABLE_OF_CONTENTS.md`](./docs/TABLE_OF_CONTENTS.md).

## Pick a path

**You've got 90 minutes.** Chapters 1, 3, 4, 9, 10. You'll be measurably better by dinner.

**Solo dev shipping a SaaS.** 1, 3, 4, 5, 6, 9, 12, 17, 19, 21.

**Rolling this out to a team.** 1, 2, 6, 7, 8, 10, 11, 13, 14, 20, 21.

**Just curious what's here.** Read Chapter 2, skim the TOC, come back.

## Three things that make it different

**1 · Concepts first, realizations second.** Chapter 4 is about memory as a problem. `GEMINI.md` and `CLAUDE.md` are two realizations. When filenames change (and they will), the chapter still holds. Every concept chapter is built this way deliberately.

**2 · Every asset actually runs.** No theoretical "here's how you'd write one" examples. If it's in `assets/`, it's tested against real input — every hook script ships with a test payload in its own header. Dry-run it before trusting it.

**3 · Opinions, not hedging.** Where one approach is better for a task, the text says so and explains why. Where it's "it depends," it says what it depends on. You're allowed to disagree — [file an issue](https://github.com/vmishra/ai-coding-playbook/issues) with a specific counterexample.

## Tested against

- Gemini CLI v0.34+ (Plan Mode, native skills, `save_memory` tool)
- Claude Code v2.1.59+ (auto-memory, skills with `context: fork`, full hook event list)
- Google Antigravity (April 2026 preview build; MCP status evolving)
- Firebase Studio, Cloud Workstations, Vertex AI Model Garden (current as of April 2026)

When a tool ships a breaking change, [file an issue](https://github.com/vmishra/ai-coding-playbook/issues) with the version and what broke. The [CHANGELOG](./CHANGELOG.md) records every material update.

## Repository layout

```
ai-coding-playbook/
├── chapters/                  The book
│   ├── 01-getting-started/
│   │   ├── README.md          ← concept chapter
│   │   ├── gemini-cli/        ← Gemini-specific walkthrough
│   │   └── claude-code/       ← Claude-specific walkthrough
│   └── ... (21 chapters)
├── assets/                    Runnable, copy-pasteable resources
│   ├── gemini-cli/
│   │   ├── commands/   skills/   hooks/   settings/
│   └── claude-code/
│       ├── commands/   skills/   hooks/   mcp/   settings/
├── docs/                      Cross-chapter reference
│   ├── TABLE_OF_CONTENTS.md
│   ├── GLOSSARY.md
│   ├── FAQ.md
│   ├── ROADMAP.md
│   └── MANIFESTO.md           ← why this exists, how it stays fresh
├── AGENTS.md                  The repo's own memory file
├── CLAUDE.md → AGENTS.md
└── GEMINI.md → AGENTS.md
```

## Contributing

Read [`CONTRIBUTING.md`](./CONTRIBUTING.md). Short version: small PRs, real examples, no AI-generated filler, if you ship an asset it has to actually run on a fresh install.

If you tried something from the book on a real codebase and it did (or didn't) work the way the chapter claimed, **please open a field-report issue**. Those are the best feedback loop this repo has.

## License

[MIT](./LICENSE). Fork it, remix it, turn it into a paid course, point a tool at it, translate it — just don't claim you wrote it.

---

<p align="center">
  <sub>Star the repo if it earned it. File an issue if it didn't.</sub>
</p>
