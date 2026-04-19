# Chapter 11 — Subagents and Parallelization

> The heaviest single lever for keeping context clean and running work at human scale. Also the primitive people abuse the fastest.

---

## The concept

A subagent is a second instance of the agent, spawned by the primary, running in its own context window, and given its own narrow task. When it finishes, it returns a summary to the primary. Everything the subagent read, explored, and reasoned through lives and dies in *its* context — not in yours.

Two things make subagents powerful:

1. **Context isolation.** Heavy reads happen elsewhere. Your primary session stays sharp.
2. **Parallelism.** Several subagents can work simultaneously on independent pieces of a larger task.

Two things make them dangerous:

1. **They still cost tokens.** A subagent that reads 40 files isn't free just because you don't see the reads. You just moved the cost off your screen.
2. **Parallelism magnifies mistakes.** A misbriefed subagent burns through tokens solving the wrong problem — fast, and four at a time.

The discipline is the same one that makes delegation work with humans: give them a scoped goal, trust them to execute, verify the output.

## When to spawn a subagent

Three clear use cases:

1. **Exploration that produces a summary.** "Tell me how the auth system works" — delegate this; get back a 300-word summary, not 40 files of reads.
2. **Independent, parallelizable work.** "Generate tests for these four unrelated functions" — four subagents in parallel, each with its own file to write.
3. **Isolated, possibly failing investigation.** "Figure out why this test is flaky" — the subagent can go deep without polluting your primary context if it comes up empty.

And the cases where *not* to:

1. **Work that needs the primary context.** If the subagent will need knowledge from the current session to do its job, spawning it means briefing it from scratch — usually worse than just doing the work in the primary.
2. **Trivial tasks.** Spawning has overhead. If the task is three tool calls, just do it.
3. **When you can't verify the output.** A subagent that produces code you don't read is a future bug you're choosing to own.

## Briefing a subagent

Everything Chapter 3 said about briefing applies, doubly. The subagent doesn't have your context; it has *only* what you give it. A bad brief produces bad work in isolation, and you pay for it regardless.

The four parts — outcome, scope, constraints, verification — become mandatory, not optional. And one more part matters more for subagents than for the primary:

**Tell the subagent what *not* to return.** If you only want a summary, say so. "Return a 300-word summary. Do not quote code unless the specific line is load-bearing." Otherwise you'll get the full transcript back and the whole point of the subagent evaporates.

## The two modes

### Fire-and-forget

Spawn, wait for result, integrate. The simplest mode, and the right default. Good for research, exploration, single-target refactors.

### Parallel

Spawn several subagents at once. Right for work that's genuinely independent — tests for four unrelated functions, migrations of four isolated files, independent lookups against four data sources.

Parallelism fails when the tasks aren't as independent as you thought. If subagent A's changes would affect what subagent B should do, you have ordering you aren't enforcing. Result: B redoes work, or creates conflicts. When in doubt, run serially.

## Realization: Claude Code

Claude Code exposes subagents directly in the `Agent` tool. Skills can also fork into a subagent via `context: fork` in frontmatter.

Direct spawn from the primary:

> "Use the Agent tool with subagent_type=Explore to research how authentication works in this codebase. Give me back a summary under 300 words and the file paths that matter."

Skill-defined subagent (from Ch. 6):

```yaml
---
description: Migrate a file from lodash to vanilla ES. Use when the user asks to remove lodash from a file.
context: fork
agent: refactor
allowed-tools: Read Edit Grep
effort: xhigh
---
```

You can also define custom subagent types in `~/.claude/agents/<name>.md` with their own system prompt and tool allowlist. Useful when a particular kind of investigation recurs.

## Realization: Gemini CLI

Gemini CLI supports sub-agents via skills and extensions; a skill can be invoked via `activate_skill` and run in an isolated context. Multi-agent system patterns — orchestrator plus workers — are first-class in Google's [Agent Development Kit](https://google.github.io/adk-docs/), covered in Ch. 20. For lightweight parallelization inside a single Gemini CLI session, see [the skills reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md).

For serious multi-agent work with Gemini models — more than the CLI's session-scoped subagent use — ADK is the right tool. Think of the CLI's subagents as "a way to keep context clean" and ADK's multi-agent systems as "a way to build production agent systems."

## Parallelism patterns that work

### Map-reduce

Independent work followed by a synthesis pass. "Research these five libraries; return a 100-word comparison on dimension X" → five subagents in parallel → one synthesis pass in the primary that compares their outputs.

### Pipeline

Sequential stages where each subagent hands off to the next. Rarely worth the complexity unless each stage is expensive.

### Explore-then-execute

One subagent explores the problem space and returns a plan; the primary (or another subagent) executes the plan. This is the dominant pattern for anything harder than trivial.

## Parallelism patterns that don't

- **"Divide and conquer" when the divisions are fictional.** If you can't clearly state what each subagent owns and doesn't own, they'll step on each other.
- **"Let the subagents decide the scope."** Scoping is your job. Subagents are bad at carving work.
- **"More subagents = faster."** Each one is context cost. Over-parallelization burns more tokens than it saves.

## Observability

- **Claude Code:** the transcript shows subagent invocations inline; the `Task` object tracks them. `/context` shows primary context use; subagent usage is tracked separately.
- **Gemini CLI:** skill invocations surface in the log; `gemini extensions list` + `/memory show` for what's loaded.

If you're debugging "why did my subagent do X," ask for its transcript. Don't try to infer from the summary it returned.

## Cost math, briefly

A rough mental model:

- A subagent's *cost* is its own input + output tokens, on whatever model you route it to.
- The subagent's *gift to you* is the difference between "those tokens in your primary context" and "a short summary in your primary context."
- If the subagent's work would have taken 20k tokens of reads in your primary but returns a 500-token summary, you've saved ~19.5k tokens of future compounding context cost.

Route subagent work to a cheaper model where you can (Flash, Haiku). They're usually great at "read and summarize."

## The discipline

- Delegate reading and exploration.
- Keep planning and final judgment in the primary.
- Brief subagents like you're briefing a contractor: outcome, scope, constraints, verification, and *what not to return*.
- Verify their output — particularly code edits.

## References

- Claude Code — [Skills / context:fork](https://code.claude.com/docs/en/skills)
- Gemini CLI — [Skills](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
- Google — [ADK — Multi-agent systems](https://google.github.io/adk-docs/agents/multi-agents/)

## What's next

- [Chapter 12 — Research and Web Integration](../12-research/README.md) — research, the canonical "subagent-shaped" task.
- [Chapter 20 — Agent SDKs](../20-agent-sdks/README.md) — when CLI subagents aren't enough.
