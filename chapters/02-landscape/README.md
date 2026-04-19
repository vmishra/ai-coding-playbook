# Chapter 2 — The Agentic Coding Landscape

> A candid, opinionated map of the tools. Enough to make a decision, not enough to become obsolete in six weeks.

---

## The categories that actually matter

Forget feature-by-feature matrices. There are four axes that matter for a working engineer:

1. **Surface area:** terminal CLI, IDE, or web.
2. **Control granularity:** per-call confirmation vs autonomous bursts.
3. **Ecosystem fit:** what does it compose with (your cloud, your stack, your tools)?
4. **Model strategy:** locked to one vendor, multi-model, or BYO.

Almost every product choice you'll make reduces to those four. The rest is UX polish.

## The current landscape, honestly

As of April 2026. Expect this section to drift; the chapter concepts above won't.

### [Gemini CLI](https://github.com/google-gemini/gemini-cli) — the default if you're in or near Google

- **Surface:** Terminal.
- **Control:** Per-call by default; Plan Mode (since [v0.34.0](https://github.com/google-gemini/gemini-cli/releases), March 2026) for review-then-execute.
- **Ecosystem:** Native to Google Cloud (Vertex AI, BigQuery, Cloud Functions, Cloud Workstations, Firebase Studio). [Docs](https://geminicli.com/docs/).
- **Model:** Gemini 3 Pro / Flash by default. Model Garden unlocks Gemma, Qwen, DeepSeek, Llama via Vertex.
- **What it's best at:** Anything that composes with Google Cloud, shell-heavy workflows, free-tier exploration.
- **Where it still lags:** Multi-file refactor finesse is slightly behind Claude Code on complex codebases. Hook ergonomics are lighter.

### [Claude Code](https://www.anthropic.com/claude-code) — the reference-quality agentic CLI

- **Surface:** Terminal (plus [VS Code extension](https://code.claude.com/docs/en/ides)).
- **Control:** Per-call by default; `--permission-mode plan | acceptEdits | bypassPermissions`. Fine-grained `allow`/`ask`/`deny` lists. [Docs](https://code.claude.com/docs/en/settings).
- **Ecosystem:** MCP-native, large and growing skills/commands library, Vertex AI availability via the [Anthropic partnership on GCP](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- **Model:** Claude Opus / Sonnet / Haiku. No BYO model.
- **What it's best at:** Long-horizon refactors, reproducible workflows (hooks, skills, subagents), teams that value strict permissions.
- **Where it lags:** Not as tightly wired to Google Cloud as Gemini CLI. No free tier worth planning around.

### [Google Antigravity](https://antigravity.google/) — the agentic IDE

- **Surface:** GUI IDE (VS Code fork). Dual view: **Editor** + **Manager** ("Mission Control") for parallel agents.
- **Control:** Higher-autonomy by default; you orchestrate multiple agents at once.
- **Ecosystem:** Gemini 3 native, Claude Sonnet 4.5 and GPT-OSS also selectable. As of April 2026, **MCP support is still missing** — this is the main gap versus Claude Code and Cursor. [Docs](https://antigravity.google/docs/home) • [Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity).
- **What it's best at:** Parallel agent work when you want a visual control surface, not a terminal.
- **Where it lags:** No MCP (yet), earlier in maturity than Gemini CLI, paid tier rate limits have been bumpy.

Chapter 19 goes deeper on Antigravity specifically.

### [Cursor](https://cursor.com) — the popular VS Code fork

- **Surface:** GUI IDE.
- **Control:** Granular; Composer + agent modes.
- **Ecosystem:** Multi-model (OpenAI, Anthropic, Google). Active MCP marketplace.
- **What it's best at:** Mainstream IDE users who want a single polished product.
- **Where it lags:** Vendor lock on the Cursor platform; pricing can be surprising at scale.

### [Aider](https://aider.chat) — the git-native CLI

- **Surface:** Terminal, git-centric.
- **Control:** Very explicit — every change becomes a commit.
- **Model:** Any OpenAI-compatible endpoint. Strong local-model support.
- **What it's best at:** Small teams that value the git-as-truth discipline; pairs nicely with local models (Ch. 18).

### [Cline](https://cline.bot), [Continue.dev](https://continue.dev), [Windsurf](https://codeium.com/windsurf)

VS Code-resident alternatives that each trade off differently. Continue is the most model-agnostic (good with Ollama); Cline is popular for autonomous tasks in-IDE; Windsurf leans into multi-file refactor UX.

## Choosing between them

Real answers, not hedges:

**"I work in a Google Cloud shop."** Gemini CLI, with Antigravity for IDE-heavy days. Claude Code as a secondary for work where its refactor quality matters.

**"I'm a solo founder shipping a SaaS."** Claude Code for depth, Gemini CLI's free tier for exploratory grunt work, Stitch (Ch. 17) for UI generation, Firebase Studio for deploy.

**"I'm a senior engineer at a non-Google bigtech."** Claude Code primary — the permissions model and hooks survive a security review more easily than most alternatives. Gemini CLI for anything touching BigQuery or GCP.

**"I want one IDE, not a terminal."** Cursor or Antigravity. Antigravity if you want Gemini 3 and a generous free tier; Cursor if MCP marketplace maturity matters more than Google-native integration.

**"I want to run models locally for privacy."** Aider or Continue.dev with Ollama running Qwen3-Coder or Gemma. See Ch. 18.

## The durable cut

Strip the product names, and you get four durable decisions every team will make for as long as this category exists:

1. **How much control do you want per step?** (Confirm-each vs autonomous.) There's no universally right answer — it's a function of the task's blast radius and how much you trust the model on it.
2. **Where does your code, data, and cloud live?** Choose tools that compose with that. Fighting your cloud is a tax you pay forever.
3. **Who owns the model?** First-party (Anthropic, Google) means you get the best version of that vendor's model; BYO (Vertex Model Garden, Ollama, OpenAI-compatible) means flexibility but you own more of the integration.
4. **How do you extend the agent?** Skills, MCP, extensions, custom commands, hooks. Every tool has some form of this; the one with the cleanest primitives wins as your team grows.

Every product in the category is a particular set of answers to those four.

## What to ignore

- **Benchmarks.** SWE-bench numbers move a few points each quarter; your productivity doesn't track them closely.
- **Twitter threads claiming Tool X "killed" Tool Y.** Nobody kills anything; the space is compounding, not zero-sum.
- **"Which one writes better code."** They all write the same code when given the same context. Context is your job. The tool's job is to make it easy.

## What to read next

- [Chapter 3 — Effective Prompting](../03-prompting/README.md)
- [Chapter 4 — Memory](../04-memory/README.md)
- [Chapter 19 — Antigravity Deep-Dive](../19-antigravity/README.md) once you've read Parts II–III.

## References

- Gemini CLI repo: [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
- Gemini CLI docs: [geminicli.com/docs](https://geminicli.com/docs/)
- Claude Code docs: [code.claude.com/docs](https://code.claude.com/docs/en/overview)
- Antigravity: [antigravity.google](https://antigravity.google/)
- Vertex AI Model Garden: [cloud.google.com/vertex-ai/generative-ai/docs/model-garden](https://cloud.google.com/vertex-ai/generative-ai/docs/model-garden)
- Anthropic Vertex partnership: [docs.cloud.google.com/vertex-ai/…/use-claude](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude)
