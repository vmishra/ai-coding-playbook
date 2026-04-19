# Chapter 10 — Saving Tokens

> The economics chapter. Most people's actual top question. Where the money goes, why, and the seven levers that matter.

---

## Why this matters

At individual-developer scale, an agentic CLI is maybe $20–$200 a month. Not a problem.

At team scale — 50, 100, 500 engineers running agents against real codebases — the number stops being a rounding error. A poorly-disciplined team can burn five figures a month on tokens that produced nothing useful. The difference between a team that runs agents profitably and a team that doesn't is not "which model" or "which tool." It's context discipline, and it's learnable.

This chapter is the concrete tactics. Chapter 9 covers the session-level symptoms; this chapter covers the cost side.

## Where tokens actually go

Run any reasonably complex session and the token breakdown roughly looks like this, in rough order:

1. **File reads.** By far the dominant contributor. Reading a single 1,000-line source file is usually 3–8k tokens. Do that twenty times in a session and you have 100k+ tokens of file content.
2. **Tool descriptions.** Every MCP server, every skill description, every slash command, every built-in tool contributes to the header of every turn. Easy to blow 5–10k tokens before a single byte of your work enters.
3. **Intermediate agent thinking.** Modern models produce substantial reasoning that gets appended to context across turns. You can't always see it; you're paying for it.
4. **Tool output.** `git log`, test output, shell command output. Often verbose, often useful for three turns and then dead weight.
5. **Memory files.** `CLAUDE.md` / `GEMINI.md` load every session. Necessary, but they compound with everything else.
6. **Your prompts and the model's replies.** Usually the smallest slice.

Notice what's *not* on this list: the actual code changes. Writing a file is cheap. Reading files is expensive. That asymmetry is the core economic insight of this chapter.

## The seven levers

In roughly decreasing order of impact.

### 1. Explore first, read narrowly

The dominant optimization. Almost every session reads three to five times more than it needs to. Forcing yourself to pre-locate the relevant files costs 10 seconds; the savings are enormous.

```
❌ "Understand the auth system."
→ agent reads 30 files, 80k tokens

✅ "Grep/glob to find the three files most relevant to auth.
    Then read only those."
→ agent reads 3 files, 12k tokens, same understanding.
```

This is a prompting habit. Make it automatic.

### 2. Offload reads to subagents

When a task *genuinely* requires reading a lot (understanding a subsystem, migrating across many files), spawn a subagent. Its reads land in its context, not yours. You get back a 200-word summary. See Ch. 11 for the patterns.

The math is striking. A subagent that reads 40 files and returns a 500-token summary saves you ~60k tokens of your primary context. Do this five times in a session and you've pulled 300k tokens out of the primary.

### 3. Use prompt caching

Both vendors support prompt caching: the first N bytes of every request are cached, and subsequent requests that share that prefix pay cache-hit rates (~10% of normal) instead of full rates.

The prefix is the system prompt + your memory files + tool descriptions — everything stable across turns. That's often 20–40k tokens. At cache-hit pricing, those 20–40k tokens effectively cost nothing.

The discipline this imposes: **put stable stuff at the top, volatile stuff at the bottom.** Don't edit `CLAUDE.md` / `GEMINI.md` in the middle of a session — you invalidate the cache for everything after the edit. Don't shuffle tool registration. The moment the prefix shifts, cache hit rate drops.

- Anthropic prompt caching — [docs](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- Google Vertex AI context caching — [docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)

If you're building on the SDKs directly (Ch. 20), caching is something you wire in explicitly. In the CLIs, it's mostly automatic — but you can sabotage it with editing habits.

### 4. Compact at the right moment

Compaction isn't free — the summary model call has its own cost — but it pays for itself as soon as the saved context would have otherwise been re-attended for several more turns.

Rules of thumb:
- Compact when usage exceeds ~60% of the window and the session has more to do.
- Compact after a heavy exploration phase and before the implementation phase.
- **Compact with a hint.** "Keep the plan and the chosen approach. Drop the exploration details and tool output." A targeted compact produces a more useful summary than a generic one.

### 5. Route to cheaper models for cheap work

Haiku / Gemini Flash are 80-90% cheaper than Opus / Gemini Pro and are completely adequate for large fractions of the work: reading and summarizing files, running a format check, drafting commit messages, answering simple questions, exploring an unfamiliar directory.

- Claude Code: `/model haiku` for a session, or set `model: haiku` frontmatter on specific skills/commands.
- Gemini CLI: `gemini -m gemini-3-flash` or a per-skill model override.

The pattern: small / fast model for exploration and summarization; premium model for the actual reasoning and code edits. Most sessions could safely do half the work on the cheap tier without losing quality.

### 6. Scope MCP tool exposure

Connected MCP servers contribute tool descriptions to every turn. If you're not actively using a tool, dropping it from context is free money.

- Disconnect servers you rarely use. (`/mcp` to list.)
- Use `includeTools` / `excludeTools` (Gemini) or tool filters (Claude) to expose only the specific tools you need.
- Prefer project-scoped `.mcp.json` over global — your billing repo's Stripe server shouldn't load when you open an unrelated repo.

### 7. Trim the memory files

`CLAUDE.md` / `GEMINI.md` loads every session. A 3,000-line memory file costs you 3,000 lines of tokens on every cold start. It also hurts cache invalidation because editing it invalidates the cached prefix.

Trim it. Link to detail files with `@import` (Ch. 4) instead of inlining. Target under 200 lines for the main file.

## A concrete cost exercise

Here's a worked example on a typical mid-size task (add a new endpoint with tests, ~4 files touched).

**Undisciplined run:**

| Phase | Tokens | Notes |
|---|---|---|
| Session init (memory + tool descriptions) | 15k | CLAUDE.md at 600 lines, 6 MCP servers loaded |
| Exploration reads | 80k | Agent read 22 files, most unnecessary |
| Implementation reads + edits | 30k | Fine |
| Test iterations | 25k | Two failed runs, verbose jest output |
| Agent reasoning across 40+ turns | 40k | Normal |
| **Total input tokens** | **~190k** | ~$1.50 on Opus pricing |
| Output tokens | 15k | |

**Disciplined run (same task):**

| Phase | Tokens | Notes |
|---|---|---|
| Session init (trimmed memory, scoped MCP) | 6k | CLAUDE.md at 150 lines, 2 MCP servers |
| Subagent explores, returns summary | 4k (primary) + 30k (subagent) | Subagent reads 22 files; summary returned |
| Implementation reads + edits | 30k | Same |
| Test iterations | 10k | Compact between runs drops verbose output |
| Agent reasoning | 20k | Shorter session overall |
| **Total primary input tokens** | **~70k** + 30k (subagent on cheaper model) | ~$0.50 on Opus + cheap tier |

Rough 3× cost reduction, same output quality. This is not a contrived example; it's the standard gap between a well-run and poorly-run session.

## The ratio that predicts success

In day-to-day practice, the best predictor of whether a session will produce clean output is this ratio:

```
useful_edits / total_tokens
```

Sessions where this ratio is healthy feel snappy and produce clean diffs. Sessions where it collapses feel mushy and produce drift. When you feel the session going bad, this ratio is usually what changed — more tokens flowing, fewer edits landing.

You don't literally measure this; you develop a feel for it. The feel is "are we actually making edits commensurate with the context we're burning?"

## Observability

If you're running agents at team scale, you need cost visibility. A few strategies:

- **Audit log hook** (Ch. 8 asset). Every tool call timestamped; easy to post-process for token cost per session.
- **Vendor dashboards.** Anthropic Console and Google Cloud Billing both break down usage by model and (with effort) by project/tag.
- **A team-scoped wrapper.** Some teams wrap the CLI in a small shell script that tags each invocation with a work item ID, making cost attributable to stories/tickets.

This is a Ch. 21 / Ch. 20 topic in depth. The point here is: you can't fix what you can't see.

## The discipline in one sentence

**Fewer files in context, more work out per token.**

Every specific tactic is a way of moving one of those two dials. The durable skill is noticing which one is slipping and doing the right thing before the session curdles.

## References

- Anthropic — [Prompt caching](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)
- Anthropic — [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- Google — [Vertex AI context caching](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview)
- Claude Code — [Best Practices](https://code.claude.com/docs/en/best-practices)

## What's next

- [Chapter 11 — Subagents and Parallelization](../11-subagents/README.md) — the biggest single lever described here, with the full patterns.
- [Chapter 12 — Research and Web Integration](../12-research/README.md) — subagent-delegated research as a default primitive.
