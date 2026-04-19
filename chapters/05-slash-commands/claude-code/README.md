# Claude Code — Custom Slash Commands

Step-by-step. Every command here is runnable; copy into `~/.claude/commands/<name>.md` and the command becomes available on the next session start.

Primary sources: [Claude Code slash commands / skills docs](https://code.claude.com/docs/en/skills), [Best Practices](https://code.claude.com/docs/en/best-practices).

## The format in 60 seconds

- **File:** Markdown with optional YAML frontmatter. Extension `.md`, one command per file.
- **Locations:** personal at `~/.claude/commands/<name>.md`, project at `.claude/commands/<name>.md` (commit to share). Project wins on collisions.
- **Namespacing:** subdirectories become `:`-separated names. `.claude/commands/git/commit.md` → `/git:commit`.
- **Minimum viable file:** a single line of body. No frontmatter required.

## Step 1 — Make your commands directory

```bash
mkdir -p ~/.claude/commands
```

## Step 2 — Write your first command

Create `~/.claude/commands/research.md`:

```markdown
---
description: Research a topic and summarize findings with sources.
argument-hint: [topic]
allowed-tools: WebSearch WebFetch
---

You are a thorough research assistant. For the topic: **$ARGUMENTS**

Produce:
1. A 5-bullet summary of the state of the art.
2. Key sources with URLs (primary / official first, then high-quality secondary).
3. Open questions that would be worth investigating further.

Respect anything set in CLAUDE.md. Cite specific URLs inline.
```

Restart the session (or run `/agents reload` if your build supports it), then `/research` is available and `/research vector databases for RAG` runs it.

## Frontmatter fields

All optional. These are the ones you'll actually use (verified against [the docs](https://code.claude.com/docs/en/skills)):

| Field | Purpose |
|---|---|
| `description` | One-line summary shown in the `/` menu. |
| `argument-hint` | Autocomplete hint, e.g. `[issue-number]`, `[topic]`. |
| `allowed-tools` | Pre-approved tools — space-separated or YAML list. Fine-grained: `Bash(git add *) Bash(git commit *)`. |
| `model` | Force a specific model while the command runs (e.g. `opus`). |
| `disable-model-invocation` | `true` means only you can invoke it — the model can't. Use for dangerous commands. |

## The three injection primitives

Same pattern as Gemini, different syntax.

### Arguments — `$ARGUMENTS`, `$1`, `$2`

- `$ARGUMENTS` — the full argument string.
- `$1`, `$2`, … — positional args, shell-quoted. `"hello world"` counts as one arg.
- If the body omits `$ARGUMENTS` but args are passed, Claude Code appends `ARGUMENTS: <value>`.

### Shell execution — `` !`command` `` (inline) or a fenced `!` block

```markdown
---
description: Summarize the staged diff and propose a conventional-commit message.
allowed-tools: Bash(git diff:*) Bash(git commit:*) Bash(git log:*)
---

Staged diff:
!`git diff --staged`

Recent commit style:
!`git log --pretty=format:'%s' -10`

Produce a conventional-commit message. Subject under 72 chars, imperative mood.
Body explains the *why* — diff already shows what. No trailing period on subject.

If the diff is empty, say so and stop.
```

For multiline or interactive blocks, use a fenced `!` block:

    ```!
    pnpm typecheck
    pnpm test -- users
    ```

Output is substituted *before* Claude sees the prompt. Governed by `allowed-tools` + the session's permission rules.

### File references — `@path/to/file`

Same as anywhere in Claude Code — the file's contents are inlined.

```markdown
Team style guide:
@./docs/style-guide.md

File under review: @$1
```

## A full example — `/commit`

`.claude/commands/commit.md` (project-scoped, team-shared):

```markdown
---
description: Inspect staged changes and commit with a conventional-commit message.
allowed-tools: Bash(git diff:*) Bash(git log:*) Bash(git commit:*) Bash(git status:*)
---

## Context

Current status:
!`git status --short`

Staged diff:
!`git diff --staged`

Recent commit style:
!`git log --pretty=format:'%s' -10`

## Task

Produce a conventional-commit message that matches the style above.

Rules:
- Subject under 72 chars, imperative mood, no trailing period.
- Body explains the *why* — the diff already shows what.
- If the diff mixes concerns, propose the split instead of committing.
- If the diff is empty, say so and stop.

Once the message is correct, run:
```!
git commit -m "<subject>" -m "<body>"
```
```

## A full example — `/review`

`.claude/commands/review.md`:

```markdown
---
description: Review branch changes against our checklist.
argument-hint: [optional: base branch, default main]
allowed-tools: Bash(git diff:*) Bash(git log:*) Bash(git status:*)
---

Base branch: ${1:-main}

Checklist:
@./.claude/review-checklist.md

Diff vs base:
!`git diff ${1:-main}...HEAD`

Produce output in this shape:

## Summary
<2–3 sentences, factual, no fluff>

## Concerns (by severity)
- **Critical:** <or 'none'>
- **Should fix:** <or 'none'>
- **Nit:** <or 'none'>

## Specific comments
- `path/to/file.ts:L123` — <comment>

Quote the relevant diff in specific comments. Don't hedge. Name the real problem.
```

## Namespaced commands

Group by subdirectory:

```
.claude/commands/
├── git/
│   ├── commit.md     → /git:commit
│   ├── amend.md      → /git:amend
│   └── pr.md         → /git:pr
├── review/
│   ├── diff.md       → /review:diff
│   └── security.md   → /review:security
└── triage.md         → /triage
```

The `/` menu respects this and shows the hierarchy. Useful once you have more than ~10 commands.

## Listing, inspecting, editing

- `/` at the prompt — menu of all commands with descriptions.
- `/mycommand --help` — not universal, but many commands include their own help.
- `/agents`, `/skills` — list subagents and skills (Ch. 6 and Ch. 11).

## Security — pre-approving shell with `allowed-tools`

The `allowed-tools` field is fine-grained and uses the same permission-rule syntax as the global `permissions.allow`. Pre-approving `Bash(git commit:*)` means *only* `git commit ...` subcommands run without a prompt from inside this command; `Bash(rm:*)` would still get flagged.

Use this instead of globally allowlisting shell. A command with a scoped allowlist is safer than a liberal global permission that stays on for the whole session.

## Project vs personal

- Commit `.claude/commands/*.md` when the command is team-wide.
- Keep `~/.claude/commands/*.md` for your own shortcuts.

If a command ends up useful in three different repos, graduate it from project to user.

## Things this format does have that Gemini's doesn't (yet)

- Declarative `allowed-tools` with precise permission patterns.
- `disable-model-invocation` — hard-scopes a command to human-only invocation.
- `model` override per-command.

## References

- [Slash commands / skills reference](https://code.claude.com/docs/en/skills)
- [Best practices](https://code.claude.com/docs/en/best-practices)
- [Settings + permissions](https://code.claude.com/docs/en/settings)
