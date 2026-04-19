# Chapter 19 — Google Antigravity

> Google's agentic IDE. A fundamentally different shape from the terminal CLIs — not better, not worse, different. This chapter is what to actually do with it.

---

## What it is

[Google Antigravity](https://antigravity.google/) is Google's agentic development platform, announced November 18, 2025 alongside Gemini 3. It is *not* a CLI and it is *not* exactly a traditional IDE. It's an agent-first development environment built on a VS Code fork, organized around parallel agent orchestration rather than keystroke-level editing.

Two views you'll use constantly:

- **Editor** — a familiar VS Code-style editor for inspecting and refining code.
- **Manager** (also called "Mission Control") — a surface for spawning and monitoring multiple autonomous agents, each working in its own workspace on its own task.

Official docs: [antigravity.google/docs/home](https://antigravity.google/docs/home). Getting-started codelab: [codelabs.developers.google.com/getting-started-google-antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity).

## The mental model shift

With Gemini CLI or Claude Code, you're running *a session*. You prompt, the agent works, you review, you prompt again.

With Antigravity, you're running *a queue of agents*. You describe work; Antigravity spawns an agent in its own workspace; it produces artifacts; you review. While that's happening, you're briefing the next task. Parallelism is the default, not the exception.

If you're coming from CLIs, the analogy that helps: Antigravity is to agentic coding what CI is to local testing. The work happens somewhere else; you watch outcomes, not keystrokes.

This is great for some tasks and bad for others:

- **Great for:** independent tasks (several unrelated bugs, several isolated refactors), exploratory work where you want the agent to go figure things out while you do something else, anything that benefits from Gemini 3 out of the box.
- **Bad for:** tight, iterative, keystroke-level work; scenarios where you need to supervise every tool call; anything where MCP is core to your workflow (see current-state note below).

## What you actually interact with

### Artifacts

The agent's work surfaces as named outputs:

- **Task List** — structured to-do the agent is working through.
- **Implementation Plan** — before-the-diff plan of what it's about to change.
- **Code Diffs** — proposed file changes, reviewable and approveable.
- **Screenshots** — visual evidence of browser-based work.
- **Browser Recordings** — the agent's Browser subagent (below) recorded while it drove Chrome.
- **Walkthroughs** — post-implementation summary + verification steps.

Artifacts replace the CLI's transcript as your primary reviewable surface.

### Browser subagent

A dedicated subagent that drives Chrome. It navigates, inspects, takes screenshots, and can record sequences. Used for:

- Verifying a UI change actually renders as intended.
- Investigating web-app bugs that only show up in the browser.
- Recording reproductions and walkthroughs.

### Rules, Workflows, Skills

The customization layer:

- **Rules** — policies the agent must respect (think: hooks + allowlists).
- **Workflows** — reusable multi-step procedures.
- **Skills** — named capabilities, similar in spirit to the skills in Ch. 6.

### Allowlists

Terminal commands and browser URLs have allowlists. A sane default that mirrors the permissions discipline from Ch. 8.

## Models

As of April 2026, Antigravity supports, selectable per task:

- **Gemini 3.1 Pro** (High / Low effort)
- **Gemini 3 Flash**
- **Claude Sonnet 4.6** and **Claude Opus 4.6**
- **GPT-OSS 120B**

Default is Gemini 3. Verify the current lineup in-product — [models page](https://antigravity.google/docs/models) — as it's updated regularly.

## Parallel agent orchestration

The standout feature. Up to **5 parallel agents** at the time of writing, each in a separate workspace:

- Spawn each with its own task description.
- Monitor all of them from Mission Control.
- Approve / reject each one's diff independently.
- Useful when you have four unrelated bugs or four isolated refactors — four agents work in parallel while you triage a fifth.

The constraint is the same as Ch. 11 on CLI subagents: parallelism works when the tasks are genuinely independent. If they aren't, merges conflict, decisions drift, and you spend more time reconciling than you saved by parallelizing.

## Pricing (April 2026)

- **Free preview** — rate-limited, useful for trying it on real work.
- **Pro $20/mo** — ~1,000 monthly AI credits, weekly caps on premium models.
- **Ultra $249.99/mo** — ~25,000 credits, priority queue, no weekly caps.
- **Credit packs** — $25 for 2,500 credits.

Credit-to-token conversion isn't officially published. Budget from observed usage, not from announced numbers.

## The current gaps you should know about

As of April 2026, a few rough edges:

1. **MCP support.** Antigravity's initial launch did not ship with MCP support. Signals in early 2026 indicate MCP has landed in recent builds — **verify in-product**. If MCP is core to your workflow, check before you invest heavily.
2. **Pro-tier rate limits.** Pro subscribers have reported lockouts on premium Claude models extending beyond documented refresh windows. Ultra is rate-limited less aggressively.
3. **Preview status.** Antigravity is a public preview, not GA. Expect breaking changes.

Pair these with its strengths — and Gemini 3 performance is genuinely strong, ~parity with Claude Opus on SWE-bench Verified — and the current calculus is: use it where parallel agent orchestration or Gemini 3 specifically matter; fall back to Gemini CLI or Claude Code for the rest.

## Getting started — the actual first-hour walkthrough

1. **Download** from [antigravity.google](https://antigravity.google/). macOS, Windows, or Linux native installer. Gmail login + Chrome required.
2. **Connect a repo** — open an existing local project or clone one into a new workspace.
3. **Run the [codelab](https://codelabs.developers.google.com/getting-started-google-antigravity)** for a guided first task. It's 20–30 minutes and walks you through Editor, Manager, Artifacts, and the Browser subagent.
4. **Set Rules** for the repo — at minimum, disallow `rm -rf`, disallow pushing to main, allowlist the commands your project uses for test/build/run.
5. **Spawn your first non-trivial task** in Mission Control. Something well-scoped: "Add a loading spinner to the profile page, respecting our existing design tokens. Don't change any other page."
6. **Review the Implementation Plan** artifact before the diff. Approve, redirect, or cut scope.
7. **Review the diff.** Approve, request changes, or reject.
8. **Run the Walkthrough** artifact to verify behavior.

## When to choose Antigravity vs Gemini CLI

| Situation | Choose |
|---|---|
| Parallel independent tasks you want to fan out | Antigravity |
| Tight iterative loop on a single problem | Gemini CLI |
| GUI-friendly onboarding for a less terminal-heavy teammate | Antigravity |
| CI-like automation and scripting | Gemini CLI |
| Heavy MCP ecosystem usage | Gemini CLI (until Antigravity MCP matures) |
| You want to see the agent drive a browser | Antigravity |

Both, for most serious users.

## Antigravity and the rest of your stack

The durable concepts from earlier chapters still apply:

- **Memory** — the `GEMINI.md` / team-convention docs you've written still work.
- **Context discipline** — same signal-vs-noise problem, different surface.
- **Spec-first briefing** — even more important here, because the agent works longer without your input.
- **Hooks / Rules** — the concept is identical; Antigravity's realization is Rules + Allowlists.
- **Skills** — same idea, different surface.

You're not re-learning anything. You're applying what you know to a new surface.

## References

- [Antigravity product site](https://antigravity.google/)
- [Antigravity docs](https://antigravity.google/docs/home)
- [Antigravity models](https://antigravity.google/docs/models)
- [Google codelab — Getting Started](https://codelabs.developers.google.com/getting-started-google-antigravity)
- [Google Developers blog announcement](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
