# Chapter 3 — Effective Prompting for Agents

> Briefing is not the same as prompting. This is the skill shift that explains most of the variance between "the agent is magic" and "the agent is useless."

---

## The shift from prompt to brief

Prompting a chat model is a single-turn transaction. You type a question; it answers; you judge.

Briefing an agent is a multi-turn commitment. You describe an outcome; the agent reads, plans, edits, runs, observes, iterates; you supervise and redirect. The input isn't a prompt — it's a *working agreement* that the agent will come back to across dozens of turns. Two things follow from that:

1. **Clarity compounds.** A vague brief produces a vague plan, which guides dozens of tool calls, each adding context that will be judged against the vague brief. The drift is exponential.
2. **What you leave out matters as much as what you put in.** Anything not said is either filled in by the model's prior (usually wrong) or decided by the agent on the fly (sometimes right). Both are worse than being explicit.

Anthropic's internal observation, worth internalizing: **intelligence is not the bottleneck, context is.** ([Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). Google's Gemini 3 prompting guide converges on the same lesson from the other side: direct, structured briefs with clearly separated sections outperform loose natural language ([Gemini 3 prompting guide, Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)).

## The four parts of a good brief

Every brief that works — regardless of the model or tool — has the same four parts. You can skip them on trivial tasks. Skip them on a non-trivial task and you'll pay in turns.

### 1. Outcome

What does "done" look like? Concretely, in terms the model can verify or at least restate.

> "The `/users/:id` endpoint returns `404` instead of `500` when the user doesn't exist, and the existing tests still pass."

Compare to:

> "Fix the user endpoint."

The first can be verified against. The second cannot.

### 2. Scope

What the agent should touch — and, more importantly, what it shouldn't. Agents are eager. Without bounds they will "helpfully" refactor, rename, reformat, and upgrade dependencies, and now you have a 40-file diff for what should have been a 3-line fix.

> "Only touch files in `src/routes/users/` and `src/__tests__/routes/users/`. Don't change logging, don't change other endpoints, don't touch the database layer."

### 3. Constraints

Non-goals. Conventions to respect. Things that are out of bounds for reasons the agent can't derive from the code.

> "We're migrating off this file next quarter, so minimize diffs — don't introduce new abstractions. Keep the existing logging format even though it's inconsistent with the rest of the repo."

### 4. Verification

How will you or the agent know it's actually done?

> "Run `pnpm test -- users` and show me the output. If any new test fails, stop and ask before rewriting."

A brief with all four parts tends to be 4–8 sentences. That's the right size. More is overhead; less, and you're letting the model fill in blanks.

## The spec-first habit

For any task bigger than "rename this variable," write the brief *in a file* before you paste it. This is sometimes called **spec-first development**, and it's the single most impactful habit you can adopt. It forces you to think through the four parts above before you're watching the agent work (where you'll tolerate ambiguity because it's already moving).

Keep specs under version control in `specs/` or similar. A spec is a few paragraphs — goal, scope, non-goals, acceptance criteria. It is *not* a design doc; don't over-engineer it. Teams that do this ship with markedly lower rollback rates than teams that freestyle every session.

(If you're on a Google stack, [Google Docs or internal go/ links can be a fine home for specs too](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies) — what matters is that the spec exists before the agent runs.)

## Durable patterns

These hold across tools and across model generations. Treat them as rules until you have a specific reason to break one.

### Plan before edit

For any non-trivial task, ask for a plan first, edit second.

> "Before changing any file, tell me the plan: which files you'll touch, what you'll change in each, and how you'll verify. Don't edit anything yet."

This turns the session into a series of tiny, reviewable checkpoints. Reject plans that propose too much. Cut scope, re-ask. It is much cheaper to fix a plan than to fix a diff.

Both CLIs support this at the flag level: `gemini --plan` and `claude --permission-mode plan`. Use them on first sessions for any repo.

### Explore first, read narrowly

Ask the agent to *explore* before it reads deeply. "Use Grep and Glob to find the three files most relevant to X. Then read only those." This keeps the context tight. The failure mode to avoid: the agent reads 40 files "to be thorough," the window fills, and now the actual edit is happening in a cluttered context.

(See Ch. 10 for why this works — the short version: tokens near the end of the window are attended to more strongly than tokens near the middle.)

### Use structure: delimiters and headings

Gemini 3 and Claude both respond better to structured briefs. Pick one scheme — XML tags or Markdown headings — and use it consistently within a brief.

```
## Outcome
The /users/:id endpoint returns 404 for missing users, not 500.

## Scope
Only src/routes/users/ and its tests.

## Constraints
- No new abstractions.
- Don't touch logging.

## Verification
Run `pnpm test -- users`. All existing tests must still pass.
```

This is not ceremony. It's how the model finds each part during tool calls 30 turns later, when your brief has scrolled up.

### Name the unit of work

Every session is about one thing. Say what it is, at the top.

> "In this session we are only fixing the 500-on-missing-user bug. Any other issue you notice, flag it and keep going — don't fix it inline."

Agents respect scope when you set it. They drift when you don't.

### Refer to things by their real names

The agent can grep. Use file paths, function names, and line numbers if you have them. "Update the session validator in `auth/middleware.ts:validateSession`" beats "fix the thing that checks sessions."

### Demand citations for non-trivial claims

If the agent says "this change is safe because X," ask it to point to where in the code X is established. If it can't, its reasoning is post-hoc — push back.

## Anti-patterns

These show up constantly. They're easy to spot once you're looking.

### "Please and thank you" bloat

Polite padding burns tokens and doesn't make the model cooperate more. "Please could you kindly, when you get a chance, take a look at…" costs you context and reads as noise. Be direct. The model is not offended.

### Stacked asks

> "Fix the 500 bug, add retries, and while you're there clean up the logging, and update the README."

This is four tasks. The agent will do some subset of them badly. Split them into four sessions. Each one will be faster and better than the combined attempt.

### "Do whatever you think is best"

You are delegating judgment to the agent. The agent does not have your context. You will be unhappy with the result. If you genuinely don't care, say "I don't care about X, pick anything reasonable" — that scopes the latitude. Open-ended "whatever you think" is always a mistake.

### "Make it better"

"Better" is undefined. Faster? Smaller diff? More tests? Less dependency surface? Define it.

### Correcting by piling on

When the agent does something wrong, resist the instinct to add a new instruction on top. Instead, scroll back mentally: what was missing from the original brief that let the wrong thing happen? Fix the brief. Start fresh. You'll spend less total time than you would accumulating corrections on top of a compromised context.

## A worked example

**Bad brief** (one sentence, no structure):

> "The API is too slow on the users endpoint, make it faster."

**Good brief** (four-part, structured):

```
## Outcome
GET /users/:id p95 latency drops below 100ms in our staging benchmark.

## Scope
- src/routes/users/get.ts
- src/lib/db/users.ts (if needed)
- New tests allowed in src/__tests__/routes/users/

## Constraints
- Don't add caching yet — that's a separate project and involves a product decision.
- Don't change the response shape. Downstream clients depend on it.
- Keep the existing transaction boundary; we need read-after-write consistency.

## Verification
- Run `pnpm bench -- users-get` and include p50/p95/p99.
- Run `pnpm test -- users` and show output.
- If the only improvement you can find is adding caching, stop and tell me, don't work around the constraint.

## Starting approach
Before editing, explain what you think the hotspot is and cite the file/line. If you're not confident, tell me and we'll profile first.
```

Same task. Radically different trajectory. The good brief is the entire difference between a 30-minute focused session and a 3-hour drift.

## Prompting vs context engineering

A lot of "prompting tricks" from the chat-model era — chain-of-thought incantations, role-play setups, token-level manipulations — are less useful for agents than they were for single-turn chats. The modern models already do chain-of-thought when it helps; they don't need you to ask them to.

What *does* still matter is **context engineering**: deciding what belongs in the window, at which position, for how long. Everything in Parts IV and V of this book is context engineering. Everything in this chapter is the narrow subset of context engineering that happens at the moment you type your brief.

See Anthropic's [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) and Google's [Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) for the vendor takes. They agree on more than they disagree.

## References

- Google: [Gemini 3 prompting guide (Vertex AI)](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gemini-3-prompting-guide)
- Google: [Prompt design strategies, Gemini API](https://ai.google.dev/gemini-api/docs/prompting-strategies)
- Google: [Overview of prompting strategies, Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/prompts/prompt-design-strategies)
- Anthropic: [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices)
- Anthropic: [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)
- Anthropic: [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## What's next

- [Chapter 4 — Memory Systems](../04-memory/README.md) — moving durable context out of your brief and into a file the agent always sees.
- [Chapter 9 — Preventing Context Rot](../09-context-rot/README.md) — what to do when a briefed session still drifts.
- [Chapter 10 — Saving Tokens](../10-saving-tokens/README.md) — the economics of context discipline.
