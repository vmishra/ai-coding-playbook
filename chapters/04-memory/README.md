# Chapter 4 — Memory Systems

> How to give the agent durable context without re-briefing it every session. The single highest-leverage thing you can do after learning to prompt well.

---

## The concept

The model has no persistent state. Every new session starts with an empty context window. If you don't do something about that, you will re-explain your codebase, your conventions, and your constraints every single time. That's not a prompt problem — it's a memory problem.

Memory in an agentic CLI is a set of **files the tool reads into context automatically**. That's it. There's no clever vector store, no embedding search running in the background, no AI trying to remember what you said last Tuesday. A few text files, loaded at session start or on demand, assembled in a defined order, and visible to the model on the first turn.

The trick is knowing:

1. **What belongs in those files** (and what doesn't).
2. **Where to put them** so the tool finds them at the right scope — personal, project, or sub-directory.
3. **How to keep them small and current** so they're load-bearing, not dead weight.

## The three-tier hierarchy

Both CLIs implement the same conceptual hierarchy, with different filenames. The concept is durable. The filenames are realizations.

| Tier | What it's for | Who sees it |
|---|---|---|
| **User / global** | Your personal preferences, tool prefs, how you like diffs formatted | You, on every project |
| **Project (shared)** | Build commands, test commands, architecture facts, team conventions, "read this file before touching X" | Everyone on the team, checked into git |
| **Project (local)** | Your personal overrides for this repo only — sandbox URLs, local cred paths, machine-specific stuff | You, on this project, not checked in |
| **Nested / subsystem** | Rules that only apply to a specific directory — load on demand when the agent reads files there | The agent, when relevant |

You can get by with just the middle two (project shared + user global). Most teams never need the local or nested tiers at first. But when you do need them, they're the thing that prevents "please stop editing the legacy directory" from being a thing you type.

## What to put in a memory file (and what not to)

**Put in:**

- **Build/test/run commands** with their real names. `pnpm test -- path/filter` beats "run the tests." The agent will copy-paste what you wrote.
- **Architecture one-liners.** "Requests enter at `api/server.ts`, are auth'd by `auth/middleware.ts`, and routed via the router registered in `api/router.ts`." Three sentences of architecture save fifty tool calls of exploration.
- **Conventions the agent won't infer.** "We use tabs. We use `snake_case` for DB columns, `camelCase` for TS fields, and a `@ColumnMap` decorator bridges them." These are exactly the things the model gets wrong by default.
- **Non-goals.** "Do not use `any`. Do not use `// @ts-ignore`. Do not add dependencies without asking."
- **Pointers to where to look.** "For anything about billing, start from `billing/README.md`."

**Don't put in:**

- **Secrets, API keys, personal tokens.** Memory files are often committed. They're also loaded every session, which means they're in every log and every debug dump. Secrets don't belong anywhere near memory.
- **Bulk documentation.** If your memory file is 2,000 lines, it's eating context on every single turn. Slim it down. Move detail into files and reference them with imports.
- **Contradictory rules.** "We prefer X" in one place and "don't do X" in another means the model will pick whichever it saw last. Reconcile before committing.
- **Transient state.** "Currently working on feature X, due Friday." This goes stale, and stale context is worse than no context — it actively misleads.

Think of a memory file the way you'd think of an onboarding doc for a senior engineer joining next week. Specific. Terse. Load-bearing. Not a novel.

## Gemini CLI — `GEMINI.md`

### The file hierarchy

Gemini CLI loads context files from (verified against [the official spec](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)):

1. `~/.gemini/GEMINI.md` — user-global
2. `./GEMINI.md` at the project root, plus a walk up the parent directory tree
3. `./<any-subdir>/GEMINI.md` — loaded on demand when tools touch that subdirectory

All discovered files are **concatenated** into the context. The footer UI shows how many context files were loaded. You can change the filename(s) in `~/.gemini/settings.json`:

```json
{
  "context": { "fileName": ["AGENTS.md", "GEMINI.md"] }
}
```

### The `/memory` command

Three subcommands you'll use often ([docs](https://geminicli.com/docs/reference/commands/)):

- `/memory show` — print the exact concatenated context the model is seeing. Run this first time you set up a project — it surfaces bugs like accidentally double-loaded files.
- `/memory reload` — reload all `GEMINI.md` files after an edit.
- `/memory add <text>` — append a line to your user-global `GEMINI.md`. Handy mid-session.

### The `save_memory` tool

Gemini CLI ships a built-in `save_memory` tool that the agent can call to persist a fact — it appends the string to a `## Gemini Added Memories` section of `~/.gemini/GEMINI.md` ([docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md)). Treat this as a convenience, not a pattern. If the agent is saving things on its own, review them: the long-term value of a memory file drops fast once it contains agent-auto-generated filler.

### Imports — `@path/to/file`

Split large memory into topic files and import them:

```markdown
# GEMINI.md

## Project
This is the billing service. Handles subscriptions, invoices, proration.

## Build and test
- Install: `pnpm install`
- Run: `pnpm dev`
- Test: `pnpm test`
- Typecheck: `pnpm typecheck`

## Conventions
@./docs/conventions.md

## Subsystems
- Billing: see `./billing/GEMINI.md`
- Invoicing: see `./invoicing/GEMINI.md`
```

Imports are resolved by the Memory Import Processor ([docs](https://geminicli.com/docs/cli/gemini-md/)) and can be relative or absolute paths.

### A starter `GEMINI.md`

```markdown
# <Project Name>

One paragraph: what this repo is, who uses it, what it talks to.

## Run / test / build
- Install: `<cmd>`
- Dev: `<cmd>`
- Test: `<cmd>` (add `-- <filter>` to scope)
- Typecheck / lint: `<cmd>`
- Deploy: `<cmd>` (or "ask before deploying")

## Architecture in three sentences
Requests enter at `<file>`, are handled by `<system>`, persist to `<store>`.
Dependencies we own: <list>. Dependencies we don't: <list>.

## Conventions
- Indent: <tabs / 2 spaces / 4 spaces>
- Naming: <TS/Python/etc.>
- Error handling: <return Result / throw / etc.>
- Logging: <module, format>
- Never: add deps without asking, use `any`, commit secrets, skip tests.

## Where to look
- Auth: `./auth/README.md`
- Data model: `./db/README.md`
- API contracts: `./api/README.md`

## Known traps
- `<file>` has a subtle invariant about <thing>. Read the comments first.
- `<subsystem>` is scheduled for deprecation — minimize changes there.
```

Keep it under 200 lines. When it starts creeping up, extract into `./docs/*.md` and use `@` imports.

## Claude Code — `CLAUDE.md`

### The file hierarchy

Claude Code's [memory docs](https://code.claude.com/docs/en/memory) specify this precedence (more specific wins, all are concatenated):

1. **Managed policy** (org-wide): `/etc/claude-code/CLAUDE.md` (Linux/WSL), `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS), `C:\Program Files\ClaudeCode\CLAUDE.md` (Windows).
2. **Project shared**: `./CLAUDE.md` or `./.claude/CLAUDE.md`.
3. **Project local**: `./CLAUDE.local.md` (gitignored).
4. **User global**: `~/.claude/CLAUDE.md`.
5. **Nested**: `./<subdir>/CLAUDE.md`, loaded on demand when Claude reads files in that subdir.

### The `/memory` slash command

`/memory` lists every file loaded in the current session, lets you open them in your editor, and toggles auto-memory. Run it whenever you're about to debug "why is the agent ignoring what I told it?" — usually the answer is that the file you think is loaded isn't.

### Auto-memory (Claude Code ≥ v2.1.59)

Claude Code can write its own persistent notes to `~/.claude/projects/<project>/memory/`, indexed by a `MEMORY.md` file plus topic files. Only the first 200 lines of `MEMORY.md` load per session; topic files load on demand. Toggle with `autoMemoryEnabled` in `settings.json` or `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

This is powerful and dangerous. Review what the agent is writing periodically. A memory file you don't own quickly becomes noise.

### Imports — `@path/to/file`

Same syntax as Gemini's, up to 5 recursive hops. First-time import of an external path triggers a one-time approval dialog.

### Rules files — `.claude/rules/*.md`

More granular than `CLAUDE.md`: each rule file can include `paths:` glob frontmatter so it only loads when files matching those globs are touched.

```markdown
---
paths:
  - "src/billing/**"
---
# Billing module rules
- Money is stored in cents as integers, never floats.
- Currency codes are ISO 4217 uppercase.
- All mutations go through `billing/api.ts` — never write directly.
```

### A starter `CLAUDE.md`

Use the same template structure as the Gemini starter above — the content is identical; only the filename differs. Key differences:

- Use `.claude/rules/*.md` with `paths:` frontmatter for path-scoped rules instead of nested `CLAUDE.md` files (more explicit).
- Rely on `CLAUDE.local.md` for your personal, uncommitted overrides.

## A working pattern: the three-file setup

For a real team project, this is a good default layout:

```
~/.claude/CLAUDE.md          # (or GEMINI.md) — your personal preferences
./CLAUDE.md                  # project shared — build/test/arch, committed
./CLAUDE.local.md            # your overrides, in .gitignore
./.claude/rules/
  billing.md                 # path-scoped to billing/**
  auth.md                    # path-scoped to auth/**
  migrations.md              # path-scoped to db/migrations/**
```

If you're on Gemini CLI, swap `CLAUDE.md` → `GEMINI.md`, and use nested `GEMINI.md` files (`./billing/GEMINI.md`, etc.) for path-scoped rules.

## Keeping memory current

A stale memory file is worse than no memory file. Two lightweight practices that prevent rot:

1. **Memory PRs are small and specific.** "Add: `pnpm migrate` invocation." Not "I updated a bunch of stuff in `CLAUDE.md`." Reviewable, revertable.
2. **Review quarterly.** A 15-minute pass through `CLAUDE.md` / `GEMINI.md` every quarter. Delete anything that hasn't been true in three months.

If your team is already using an `AGENTS.md` convention (common in 2026), both tools can be pointed at it — Gemini via `context.fileName`, Claude via an `@./AGENTS.md` import from `CLAUDE.md`. Pick one source of truth; don't maintain two.

## Common mistakes

- **Putting your whole style guide in.** It'll be 4,000 lines and eat context. Link to it; don't inline it.
- **Copy-pasting the team spec.** Specs are for humans; memory files are for agents. The shape is different. A memory file tells the agent what *not* to do; a spec tells a human *what* to do.
- **Forgetting `CLAUDE.local.md` / machine-specific Gemini overrides exist.** You end up committing your local DB URL into the shared `CLAUDE.md`, and now your coworker is hitting your laptop. Use the local tier.
- **Over-reliance on nested memory.** If `src/**/GEMINI.md` files contradict the root, the agent will oscillate. Root sets the invariants; nested files only add specifics.

## When memory isn't the right answer

Not every recurring instruction belongs in memory.

- **If it's a workflow, make it a slash command** (Ch. 5). "Always run the linter after edits" is a hook (Ch. 8), not a memory entry.
- **If it's a capability, make it a skill or extension** (Ch. 6). "When the user asks for a PR description, generate this format" is a skill.
- **If it's secret configuration, make it an env var.** Never a memory file.

Memory is for the things the agent needs to know are *always* true about your world. Workflows, capabilities, and secrets each have a better home.

## References

- Gemini CLI — [GEMINI.md spec](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md), [memory tool](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md), [commands](https://geminicli.com/docs/reference/commands/)
- Claude Code — [Memory docs](https://code.claude.com/docs/en/memory), [Best practices](https://code.claude.com/docs/en/best-practices)
- Anthropic — [Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

## What's next

- [Chapter 5 — Custom Slash Commands](../05-slash-commands/README.md) — for workflows that don't belong in memory.
- [Chapter 9 — Preventing Context Rot](../09-context-rot/README.md) — what to do when even a good memory file isn't enough.
