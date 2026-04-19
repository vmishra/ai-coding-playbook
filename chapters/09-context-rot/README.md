# Chapter 9 — Preventing Context Rot

> Why long sessions get dumber. The symptoms, the mechanism, and the handful of habits that push the problem out by 10x.

---

## What context rot is

You start a session. The agent is sharp — answers are precise, edits are clean, it respects your constraints. Three hours in, it's confidently inventing function names, "forgetting" decisions you made an hour ago, and circling on a simple bug.

The model hasn't gotten dumber. Your context has gotten dirtier.

The mechanism is simple. The context window is finite. Every tool call, every file read, every intermediate thought, every "let me try" that didn't pan out — all of it stays in the window. The more stuff you pile in, the more the model has to attend across, and the harder it is to find the signal. The symptoms look like forgetfulness; the actual problem is attention dilution.

## The four symptoms

Learn to spot these early. They're your cue to take corrective action *before* you waste another hour.

### 1. Repetition

The agent suggests a change it already made. Reads a file it already read in full. Proposes an approach you already rejected. The correction is in the context, but it's buried.

### 2. Confident invention

A function name appears that doesn't exist. An import path it "remembers" is wrong. This is the model's prior leaking through because the real data got crowded out.

### 3. Drift

You asked it to fix one thing; its diff now touches seven files and includes "cleanups" you didn't ask for. The original brief's boundaries have faded.

### 4. Hedging

"This *should* work," "usually this pattern…", "in most cases this is safe." The model is noticing its own uncertainty without being able to locate the concrete thing it's uncertain about. The signal-to-noise in its context has dropped below the threshold where it can reason crisply.

If you see two of these in the same session, stop. Do not push through. Push through is the most expensive thing you can do here.

## The mental model: signal vs noise

Treat your context window as having two populations of content:

- **Signal.** The current goal, the files that matter, the decisions you've reached, the constraints you've set.
- **Noise.** Files read and no longer relevant. Aborted approaches. Verbose tool output that was summarized in one line you read ten messages ago. The agent's own "let me also check…" exploration tangents.

Long sessions accumulate noise faster than they accumulate signal. The ratio flips silently, and the model's performance tracks it. Every technique below is about shifting that ratio back.

## The durable habits

### 1. End sessions at task boundaries

The single highest-leverage thing. When the task is done, close the session. Open a new one for the next task.

This feels wrong if you're used to keeping a terminal open all day. It isn't. A fresh context is not a cost; it's a feature. The agent gets the best conditions for the new task — nothing leaking in from the last one.

"But I need the previous context for this next task" is almost never true. If there's something load-bearing, put it in memory (Ch. 4) where it'll be available to every session, not just this one.

### 2. Compact aggressively

Both tools offer compaction: replace the long conversation history with a short summary, free the context. Don't wait until you're near the limit — the reason to compact is not "I'm out of space," it's "my signal-to-noise has dropped."

Good compaction triggers:
- Just finished a sub-phase (explored, now implementing).
- Changed approach — the old approach is now irrelevant.
- Ran a long tool call that flooded the window.

Gemini CLI: `/compress` (or whatever your version calls it — check `/help`).
Claude Code: `/compact`. Accepts an optional hint — "focus on the spec and the current implementation; drop the exploration."

### 3. Checkpoint decisions into durable stores

When you and the agent agree on something load-bearing, don't leave it floating in the conversation. Move it to a file the next session will see:

- **Decisions and rationale** → `docs/decisions/<topic>.md`, or append to `CLAUDE.md` / `GEMINI.md`.
- **The spec you converged on** → `specs/<feature>.md`.
- **A plan you want to continue tomorrow** → a file the agent will read when the next session starts.

Then when you compact or start fresh, nothing load-bearing is lost.

### 4. Read narrowly

The single biggest noise-generator is the agent reading 40 files "to be thorough." Explicit instructions keep this in check:

- "Use Grep to locate the 3 files most relevant to X. Then read only those in full."
- "Don't read a file in full unless you've decided you need to change it."
- "If you need to see more of a file, read a specific line range, not the whole thing."

This is a habit; drill it until it's automatic. Every unnecessary full-file read is a context tax.

### 5. Delegate exploration to subagents

For anything that requires reading many files or investigating broadly, spawn a subagent (Ch. 11). The subagent burns its own context; yours stays clean. What comes back is the subagent's summary — a 200-word answer instead of 40 file reads.

This is the biggest single lever for long-horizon work. Your primary context becomes a project coordinator; subagents do the heavy reading.

### 6. Watch the meter

Both CLIs expose their context usage:

- Gemini: a badge in the footer; `/memory show` for what's loaded.
- Claude: `/context` for a full breakdown.

Glance at it between sub-tasks. If usage is past 50% of the window and you haven't made meaningful progress, stop. Compact, checkpoint, or start fresh.

### 7. One concern at a time

Scope creep is a context killer. "While you're in there, also fix the linting in that other file" doubles the effective noise by doubling the live targets. Resist. Finish the one thing; new session for the next.

## When to start fresh instead of compacting

Compaction preserves the thread of the conversation in summarized form. Fresh sessions throw it out. Prefer fresh when:

- The previous direction was wrong and you want the agent to approach the task without its baggage.
- You're shifting to a task that doesn't share much signal with the previous one.
- The session ran long and compaction keeps producing summaries that feel stale.

Prefer compaction when:

- You're genuinely continuing the same work.
- There's a handful of concrete decisions you don't want to lose.
- The session isn't that long yet and the signal-to-noise is recoverable.

Default to fresh. You'll rarely regret it.

## The anti-pattern gallery

Watch for these — you'll do them, everyone does:

### "Just one more fix"

You've been at this for three hours. Output has degraded. Instead of starting fresh, you add another correction. The correction lands in a polluted context. It doesn't stick. You add another. Compounding waste.

Response: it is always faster to close the session, spend 30 seconds writing down where you are, and start fresh.

### "Let me give you more context"

The agent drifted, so you paste 200 lines of additional context in. You just *added* to the problem. The signal-to-noise got worse, not better.

Response: pasting context is sometimes the right move, but usually what you want is to *remove* the noise, not add more signal to drown it out. Compact first.

### "Keep this session alive because it understands the codebase"

No it doesn't — the codebase understanding, such as it is, came from files the agent read, which are still there but now buried. A fresh session with a good `CLAUDE.md` / `GEMINI.md` pointing at the right files will re-orient in a few turns.

### "I'll just ask it to forget the earlier stuff"

Models don't forget on command. They'll *say* they'll focus on the new thing, but the earlier stuff is still in the window, still contributing to their outputs. Compaction is the real mechanism; verbal instructions aren't.

## A concrete workflow

The pattern that works on long-horizon work:

1. **Start of session:** memory files loaded, narrow goal, minimal brief.
2. **Explore:** subagent-delegated exploration. You get back a summary, not the reads.
3. **Plan:** agent produces a plan (in plan mode). You review. Checkpoint the plan to a file.
4. **Implement phase 1:** do one logical chunk. Run the tests. Commit.
5. **Compact or restart:** if the implementation phase generated a lot of tool output, compact with a hint: "Keep the plan and the commit summary; drop the tool output."
6. **Repeat** for phases 2, 3, ...
7. **End of session:** commit anything uncommitted, record the remaining plan in `specs/` or `docs/decisions/`, close.

Under this pattern, a 4-hour task never produces a 4-hour-long single session. It produces 3–5 short, clean sessions chained through durable files.

## What's next

- [Chapter 10 — Saving Tokens](../10-saving-tokens/README.md) — the economics angle on the same discipline.
- [Chapter 11 — Subagents and Parallelization](../11-subagents/README.md) — the heaviest lever for keeping context clean.
