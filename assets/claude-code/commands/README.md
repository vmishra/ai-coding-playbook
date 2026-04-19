# Claude Code slash command assets

Drop-in `.md` commands. Copy the ones you want into `~/.claude/commands/` (or `.claude/commands/` in your repo for team-shared commands). They become available on session start; existing sessions pick them up after a restart.

## What's here

| File | Command | What it does |
|---|---|---|
| `research.md` | `/research <topic>` | Web-research a topic with structured summary and sourced citations. |
| `commit.md` | `/commit` | Inspect staged diff, propose conventional-commit message, commit. |
| `review.md` | `/review [base]` | Review branch changes against `main` (or given base) with severity classifications. |
| `plan.md` | `/plan <task>` | Produce an implementation plan without writing any code. High-leverage before any non-trivial edit. |

## Install

```bash
mkdir -p ~/.claude/commands
cp *.md ~/.claude/commands/
```

Then start (or restart) `claude`.

## Notes

- The `allowed-tools` field on each command scopes what can run without additional permission prompts. `/commit` pre-approves `Bash(git commit:*)` but would still flag `Bash(rm:*)`.
- `/plan` has tight `Read Grep Glob` scope by design — it's a read-only planning step. Pair it with a separate session where you paste the plan back and ask for the implementation.
- All four commands read CLAUDE.md context at invocation.

See [Chapter 5](../../../chapters/05-slash-commands/claude-code/README.md) for the walkthrough and permission-scoping notes.
