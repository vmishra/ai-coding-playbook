# Chapter 1 — Getting Started with Agentic Coding

> The mental model. Install. First session. Everything that comes later assumes you have this.

---

## What's actually new

Every generation of programming tool — the IDE, the debugger, the LSP, the language model autocomplete — sat *next to* your code. You held the pen; the tool helped. Agentic coding is categorically different: the agent reads your code, makes a plan, edits files, runs commands, observes output, and iterates. You're no longer typing; you're briefing. The skill shifts from "how do I write the code" to "how do I describe the outcome, scope the work, and verify the result."

This is not a productivity multiplier on the old skill. It's a different skill. People who are 10x faster with an agent are usually not typing faster; they're briefing better, scoping tighter, and catching the agent's failure modes earlier. The people who are underwhelmed usually haven't shifted modes — they're still typing, with the agent as a fancy autocomplete.

The rest of this book is about making that shift.

## The mental model

Hold this picture in your head whenever you're working with an agent:

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

The model has exactly one input: this window. It has no memory of prior sessions (unless you give it one — Chapter 4). It cannot "just know" anything about your codebase that isn't either (a) in the window or (b) fetchable by a tool.

This single fact explains most of what will go wrong:

- **"The agent forgot what we decided earlier."** It didn't forget. The decision either wasn't in the window, or got crowded out by later content.
- **"It keeps making the same mistake."** The correction is in the window, but it's buried under 40k tokens of file reads. It's no longer near the front of attention.
- **"It invented a function that doesn't exist."** The real function is in a file the agent never read. From the model's perspective, inventing was the only option.

Every technique in this book is, at the root, a technique for controlling what's in the window, for how long, and at what position. If you internalize that, the rest is details.

## What "agentic" actually means

An agent is an LLM in a loop. Each turn:

1. The model sees the current context window.
2. It decides: respond with text, call a tool, or stop.
3. If it called a tool, the tool runs and appends its result to the window.
4. Go to 1.

"Tools" here includes file reads, file edits, shell commands, web searches, MCP calls, subagent spawns — anything the runtime exposes. The model chooses which to call based on instructions and what's in the window. You influence those choices by controlling both.

When people say an agent is "smart" or "dumb," they're usually describing how well the model makes that loop converge on a useful outcome. The raw model capability matters, but the runtime — tool selection, permissions, context discipline, memory, hooks — matters at least as much. A strong model with a weak runtime underperforms a weak model with a strong runtime on almost any real task.

## Installing Gemini CLI (primary)

See the full walkthrough at [`gemini-cli/setup.md`](./gemini-cli/setup.md). Short version:

```bash
npm install -g @google/gemini-cli
gemini          # first run — auth flow opens
```

It needs Node ≥ 20, authenticates against your Google account by default (free tier), and drops its config at `~/.gemini/settings.json`. If you're at Google or have a Google Cloud project, authenticating against Vertex AI unlocks higher quotas and enterprise auth.

## Installing Claude Code (secondary)

See [`claude-code/setup.md`](./claude-code/setup.md) for the walkthrough. Short version:

```bash
npm install -g @anthropic-ai/claude-code
claude          # first run — auth flow opens
```

Needs Node ≥ 18, authenticates against Claude.ai (subscription) or an API key, config at `~/.claude/settings.json`.

## Your first useful session

Pick a repo you know well. Don't pick something you've never seen — you won't be able to tell if the agent is right. Open the CLI *inside* the repo (both tools use the working directory as the project root).

Now, instead of asking the agent to write something, ask it to **explain** something:

> "Walk me through how authentication works in this codebase. Start with the request entering the system and trace what touches the user record. Don't modify anything — I just want to understand."

Read its answer. Do two things:

1. **Verify at least one claim** by clicking through to the file. If the agent says "the session token is validated in `auth/middleware.ts:42`," open that file. Is it? If not, the agent is hallucinating, and you have just learned the most important lesson of this book: *verify before you trust*.
2. **Notice the context cost.** The agent probably read 10–30 files to answer. Those reads are now in the window. Your next message will be evaluated against all of them, plus everything you add. This is why you start shorter sessions for each discrete task instead of one mega-session — Ch. 9 and Ch. 10 have the full discipline, but the instinct starts here.

Once the explanation is accurate, ask for a small edit:

> "Add a structured log line at the point where the token is rejected, including the reason code. Don't change behavior — just add the log."

Watch it:

- Does it re-read the file, or rely on its earlier read?
- Does it run the tests, or just claim the change is safe?
- Does its diff match what you asked for, or does it also "clean up" unrelated code?

Whatever it does wrong on this first edit tells you more than any tutorial can. The best way to learn an agent is to watch one fail, diagnose why, and add the missing guardrail. Most of the rest of this book is a catalogue of those guardrails.

## Three habits to start with

1. **Ask for a plan before the edit.** "Tell me what you'd change, don't change anything yet." Read the plan; push back; approve. This turns the session into a series of tiny, reviewable steps instead of one giant "it did a thing."
2. **Name your work unit.** "For this session, we're only touching auth. If you need to change logging, stop and ask me first." Agents respect scope when you set it explicitly. They ignore it when you don't.
3. **End a session when the task ends.** Don't keep the CLI open for the entire day. A fresh session for each task costs nothing and saves you from Ch. 9's problems. Context is cheap to create; it's not cheap to keep clean.

## What to skip (for now)

Beginners often reach for advanced features too early and get burned:

- **Don't wire up MCP servers yet.** (Ch. 7.) They're the single fastest way to balloon context and confuse the agent if you haven't built intuition first.
- **Don't install dozens of skills or extensions.** (Ch. 6.) Each one is context cost at startup. Build your own when you know what you actually repeat.
- **Don't hand the agent destructive commands.** (Ch. 8.) Start with the default permission prompts. Loosen them only when you've seen the agent behave correctly on read-heavy work first.
- **Don't use autonomous/headless modes yet.** Watch the agent's every step for your first few sessions. You can't supervise what you haven't learned to read.

## What's next

- [Chapter 2 — The Agentic Coding Landscape](../02-landscape/README.md): Gemini CLI, Claude Code, Antigravity, Cursor — what each one actually gives you.
- [Chapter 3 — Effective Prompting for Agents](../03-prompting/README.md): how to brief without writing an essay.
- [Chapter 4 — Memory Systems](../04-memory/README.md): how to make the agent remember across sessions.

## Tool-specific setup

- [Gemini CLI setup](./gemini-cli/setup.md) — install, auth modes, first-session flags.
- [Claude Code setup](./claude-code/setup.md) — install, auth, permission model, first-session flags.
