# Chapter 5 — Custom Slash Commands

> The first thing you build when you notice you're typing the same 40 words more than twice. Cheap to create, cheap to share, high leverage.

---

## The concept

A slash command is a named, reusable prompt. You type `/foo`, the CLI expands it into whatever the file behind `foo` says, and the expanded text is what the model sees. That's it. No magic.

Three things make them disproportionately valuable:

1. **Anything you type routinely becomes a file in a repo.** The best prompts on your team eventually belong in version control. Slash commands are the mechanism.
2. **They can include live context.** Both tools let a command embed the output of a shell command or the contents of a file. So `/commit` can run `git diff --staged` and incorporate the real diff every time you use it — no copy-paste.
3. **They're composable with the rest of the system.** Commands can reference memory (Ch. 4), invoke subagents (Ch. 11), call tools with pre-approved permissions. Once you know the primitives, you stop writing throwaway prompts and start writing durable ones.

## When to make one

Rule of thumb: **the third time you type something that's more than two sentences long, stop and make a command.** Less than that, the overhead isn't worth it. More than that, you'll type it a hundred times this quarter.

Common candidates:
- `/research <topic>` — run web search + summarize, with your preferred output format.
- `/commit` — inspect staged changes, write a conventional commit message, commit.
- `/review` — run your team's code review checklist against the current diff.
- `/triage <issue-number>` — fetch the issue, summarize, propose next step.
- `/spec <feature>` — stub out a spec file using your team's template.
- `/migrate <from> <to>` — boilerplate a migration with your team's conventions.

Anti-candidates — things that *look* like they should be commands but shouldn't:
- Anything you do once a quarter. Write it down, don't commandify.
- Anything so complex it spans multiple steps with decisions in between. That's a *skill* (Ch. 6) or a *subagent* (Ch. 11), not a command.
- Anything that requires secret inputs. Use env vars.

## The durable design principles

These hold across both tools.

### 1. Bake the context in

A great command doesn't just replay your prompt — it pulls in *fresh* context every time. `/commit` should read the current diff. `/research` should read your `GEMINI.md` / `CLAUDE.md` so it respects your conventions. `/review` should see the branch's changes, not a stale copy.

### 2. Structure the output

Commands tend to get re-used by humans and by subsequent agent turns. If a command's output has a consistent structure (heading, bullets, sources), that structure becomes usable — you can grep it, show it in a PR, feed it into another command.

### 3. Declare what the command can and can't touch

Both tools let you scope tool access per-command. Use it. A `/commit` command doesn't need network access. A `/research` command doesn't need `git push`. Tightening scope at the command level means you don't have to think about it mid-session.

### 4. One command, one job

If your command has three modes, it's three commands. Name them. `/commit:fix` and `/commit:feat` beat a `/commit` that asks "which type?" every time.

### 5. Namespace as you grow

Group related commands under a subdirectory (which both tools turn into a namespace prefix). `git/commit.md` becomes `/git:commit`. Keeps `/` menu navigable.

## Where this sits in the stack

- **Memory** (Ch. 4) is what's always true about your world.
- **Slash commands** are discrete operations you invoke on demand.
- **Skills** (Ch. 6) are capabilities the agent decides to use when relevant.
- **Hooks** (Ch. 8) are policy the agent can't opt out of.

A command that keeps growing "if conditions" is trying to become a skill. A skill that must always run is trying to be a hook. Each primitive has a sweet spot.

## Realizations

- [Gemini CLI — custom commands (TOML)](./gemini-cli/README.md) — step-by-step walkthrough, working example.
- [Claude Code — custom commands (Markdown + YAML frontmatter)](./claude-code/README.md) — step-by-step walkthrough, working example.

## References

- Gemini CLI — [Custom commands docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)
- Claude Code — [Slash commands / skills docs](https://code.claude.com/docs/en/skills)
- Anthropic — [Best Practices for Claude Code](https://code.claude.com/docs/en/best-practices)

## What's next

- [Chapter 6 — Agent Skills](../06-skills/README.md) — when commands aren't enough.
- [Chapter 7 — MCP Servers](../07-mcp/README.md) — connecting commands to real systems.
