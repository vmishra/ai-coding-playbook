# Chapter 12 — Research and Web Integration

> Turning the open web into an always-available primitive. The research habit that separates senior agentic-coding practitioners from novices.

---

## The concept

Most problems you hit have been solved, discussed, or at least encountered by someone else on the open web. For a long time, using that fact during coding meant context-switching to a browser, skimming, copying back, cleaning up. Agents can collapse that loop: search, fetch, summarize, cite — in the same context where you're writing code.

Both major tools expose two primitives:

- **Web search** — returns ranked URLs + snippets for a query.
- **Web fetch** — retrieves and processes a specific URL's content.

The durable idea: **research is a context-shaped activity**, not a capability you bolt onto coding. Treat it as a first-class mode, with its own briefing, its own verification, and — critically — its own subagent.

## The research anti-pattern

Asking the agent to "research X and then implement Y" in a single session. The research burns context; the implementation then happens in a polluted context; edits suffer.

The fix: make research a distinct turn or, better, a distinct subagent. Research output goes to a file or a summary in the primary. Implementation runs in a separate session or subagent that reads the research output rather than conducting the research itself.

This is the same pattern as Ch. 11's subagent discipline, applied to a specific recurring activity.

## Good research looks like this

A useful research output has five things:

1. **A scoped question.** Not "tell me about Rust async." Rather: "What's the idiomatic way to cancel a long-running Tokio task from outside, as of stable 1.75+?"
2. **A summary** — 5-10 bullets, neutral, no marketing.
3. **Sources with URLs**, primary first. Official docs beat blog posts, which beat Stack Overflow, which beats Reddit.
4. **Dates** on each source where discoverable. In this space, 18 months old is often obsolete.
5. **Open questions** or contested claims worth flagging. "Sources disagree on whether X is required — the official docs say yes, a popular blog post says no."

The `/research` slash command asset in this playbook (Ch. 5) enforces this shape.

## Design principles

### 1. Search before you fetch

Web fetch is expensive — a random article can easily be 4-8k tokens. Search-first lets you pick which few URLs are worth fetching, and skip the rest.

### 2. Fetch the primary source

Official docs, RFCs, GitHub release notes, vendor blog posts from the vendor itself. If you're going to pay for one fetch, make it a primary.

### 3. Cache when practical

Both tools cache recent fetches for a few minutes. Use this: if you're iterating on a research question, you're often re-fetching the same URL three times in a row. The cache hit is free.

### 4. Do research in a subagent when it's heavy

Three-or-more fetches likely to produce 10-20k of content combined = subagent. Get back the summary; keep your primary context clean.

### 5. Write it down

Ephemeral research is a cost you pay over and over. If the research mattered enough to conduct, it matters enough to commit to `docs/research/<topic>.md` with a date. Next time the question comes up, the agent reads that file instead of re-running the searches.

## A two-tier research workflow

The pattern a senior practitioner uses:

### Tier 1 — Quick lookup in-session

"What's the current Gemini CLI flag for X?" — one `/research` invocation, answer lands in the session, you move on.

### Tier 2 — Durable research document

"Compare vector databases for our RAG layer." — subagent-delegated, produces a file in `docs/research/`, gets linked from the relevant spec, becomes a team artifact.

The crime is using Tier 1 habits for Tier 2 work. You ask a deep question in one turn, get a shallow answer, repeat in a week, same shallow answer.

## The canonical research command

See [`assets/claude-code/commands/research.md`](../../assets/claude-code/commands/research.md) and [`assets/gemini-cli/commands/research.toml`](../../assets/gemini-cli/commands/research.toml). Both enforce:

- A 5-bullet factual summary (no marketing language).
- Sources with URLs, primary first.
- Open questions flagged.
- No fabrication — "if you can't verify a claim, say so."

Use this command before touching any unfamiliar library. It's a 20-second habit that saves hours of dead-end exploration.

## When research output is wrong

The agent will sometimes confidently cite a URL that doesn't exist or paraphrase a doc in a way that inverts the meaning. You don't catch this by reading more carefully; you catch it by *verifying at least one claim per research output*.

Open one URL. Does the page actually say what the summary says? If yes, trust the rest more. If no, the whole output is suspect — redo it with tighter constraints.

This is the same "click through to verify" habit from Ch. 1, just applied to research rather than file reads.

## Web research for specific use cases

### Debugging a runtime error

The error message itself is usually the query. Search → fetch the most-cited issue → summarize. The agent is great at synthesizing across GitHub issues and Stack Overflow.

### Learning a new library

Fetch the official quickstart. Ask for the 5-bullet mental model. Use that as the spec for your first integration.

### Reviewing a design choice

"I'm considering X vs Y for Z. Find current comparisons with cited pros/cons, and surface anyone who regretted picking one." The "regretted picking" framing finds critical content that pure comparison articles miss.

### Staying current

"What's new in Gemini CLI since version N?" Fetch the releases page, summarize by category, flag breaking changes.

## What's next

- [Chapter 13 — Tool Connectivity](../13-connectivity/README.md) — going from open-web research to private, authenticated data.
- [Chapter 17 — UI Generation](../17-ui-generation/README.md) — where research + design + code generation compose.

## References

- [Anthropic on context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Gemini CLI tool reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/index.md)
