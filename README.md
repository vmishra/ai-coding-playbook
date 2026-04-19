# The AI Coding Playbook

> Durable, opinionated guidance for shipping real software with agentic coding tools — concepts first, tool-specific recipes second. Runnable slash commands, skills, hooks, and MCP configs included.

Maintained by [Vikas Mishra](https://github.com/vmishra). Contributions welcome.

---

## The problem this solves

The agentic coding space is moving faster than anyone can document. Tools ship breaking changes quarterly. Blog posts written in spring are obsolete by autumn. Vendors publish setup guides but not judgment.

Most content in this space is one of three things: a marketing page, a 3-minute demo that doesn't survive a real codebase, or a tutorial that's six months stale — which, in this field, is ancient.

This playbook is designed to age well. Every chapter is organized around a **durable concept** — something that was true in 2023, is true now, and will still be true when today's CLIs are footnotes. The tool-specific sections are the *realization* of those concepts, not the substance. Memory is a concept; `GEMINI.md` is a realization. Context hygiene is a concept; prompt caching and compaction are realizations. When the tools change, the concept chapters stay; the recipes get updated.

The assets — slash commands, agent skills, MCP configs, hooks — are built to be cloned, customized, and kept.

## Tool coverage and stance

**Primary: [Gemini CLI](https://github.com/google-gemini/gemini-cli).** It's open source, ships from Google, integrates cleanly with Vertex AI, Cloud Workstations, and the rest of the Google developer stack, and is the right default if you want your tooling to compose with a Google cloud footprint.

**Secondary: [Claude Code](https://www.anthropic.com/claude-code).** Included because its abstractions — skills, subagents, hook events, permissions — are currently the most mature in the category, and the concepts generalize. If you understand Claude Code's hook model, you understand hooks in general.

**Covered where relevant:** [Google Antigravity](https://antigravity.google) (the agentic IDE), [Stitch](https://stitch.withgoogle.com) (UI generation), [Firebase Studio](https://firebase.studio) and Cloud Workstations (cloud dev env), [Google ADK](https://google.github.io/adk-docs/) (Agent Development Kit), Claude Agent SDK, and the open-model ecosystem (Gemma, Qwen3-Coder, Ollama, vLLM).

This playbook does not pretend to be neutral. Where one tool is clearly better for a task, it says so. Where the answer is "it depends," it says what it depends on.

## Who this is for

Working software engineers. You know what a shell is, you've shipped code, you've debugged something at 2 AM. You don't need "what is the terminal" or "save your file before running it." You want the things that take months to learn on your own, compressed into something you can read in a weekend.

If you've never written code, start with a language fundamentals course and come back when you have something to build.

## How to read it

Three paths through the material:

**Fast track (about 90 minutes):**
[Ch. 1 → Ch. 3 → Ch. 4 → Ch. 9 → Ch. 10](./docs/TABLE_OF_CONTENTS.md). Gets you 80% of the lift.

**Solo / indie path:**
1, 3, 4, 5, 6, 9, 12, 17, 19, 21. Heavy on skills, research, and UI generation.

**Team / platform engineer path:**
1, 2, 6, 7, 8, 10, 11, 13, 14, 20, 21. Heavy on MCP, hooks, subagents, integration.

Full TOC: [`docs/TABLE_OF_CONTENTS.md`](./docs/TABLE_OF_CONTENTS.md).

## Repository layout

```
ai-coding-playbook/
├── README.md                    # You are here
├── docs/                        # Cross-chapter reference
│   ├── TABLE_OF_CONTENTS.md
│   ├── GLOSSARY.md
│   ├── FAQ.md
│   └── ROADMAP.md
├── chapters/
│   ├── 01-getting-started/
│   │   ├── README.md            # The concept chapter
│   │   ├── gemini-cli/          # Gemini CLI realization
│   │   └── claude-code/         # Claude Code realization
│   └── …
└── assets/                      # Drop-in, copy-pasteable resources
    ├── gemini-cli/
    │   ├── commands/            # Custom slash commands (TOML)
    │   ├── extensions/          # Extensions with MCP + context
    │   └── settings/            # settings.json snippets
    └── claude-code/
        ├── commands/            # Slash commands (.md)
        ├── skills/              # Skills (SKILL.md + support files)
        ├── hooks/               # Hook scripts
        ├── mcp/                 # MCP server configs
        └── settings/            # settings.json snippets
```

## Installing the assets

```bash
# Gemini CLI — primary
mkdir -p ~/.gemini/commands ~/.gemini/extensions
cp -r assets/gemini-cli/commands/*   ~/.gemini/commands/
cp -r assets/gemini-cli/extensions/* ~/.gemini/extensions/

# Claude Code
mkdir -p ~/.claude/{commands,skills,hooks}
cp -r assets/claude-code/commands/* ~/.claude/commands/
cp -r assets/claude-code/skills/*   ~/.claude/skills/
cp -r assets/claude-code/hooks/*    ~/.claude/hooks/

# Or cherry-pick one
cp assets/gemini-cli/commands/research.toml ~/.gemini/commands/
```

Every asset has its own README explaining what it does, when to reach for it, and what it costs in tokens or latency.

## How this stays fresh

Two mechanisms:

1. **Concept / realization split.** Concept chapters describe invariants ("you need a way to give the agent durable context"). Realization sections describe the current tool-specific way to do that, and get updated when vendors change things.
2. **Versioned tags.** Tool behavior references the version I tested. When a claim breaks, it's filed as an issue and patched. The [CHANGELOG](./CHANGELOG.md) records every material update.

If you hit something that no longer works, open an issue. Include the tool version.

## On style

This guide is written by a human with opinions. Where I think one approach is clearly better than another, I say so and explain why. You're welcome to disagree.

The two failure modes I've tried hardest to avoid: the breathless "unlock the power of" tone, and the hedged "there are many ways to approach this" non-answer. If you find either of these in here, file a bug.

## Contributing

Read [`CONTRIBUTING.md`](./CONTRIBUTING.md). Short version: small PRs, real examples, no slop, if you ship an asset it has to run.

## License

[MIT](./LICENSE). Use it, fork it, build a course on it — just don't claim you wrote it.
