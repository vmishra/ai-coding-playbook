# Gemini CLI — Custom Slash Commands

Step-by-step. Every command here is runnable; copy into `~/.gemini/commands/<name>.toml` and reload with `/commands reload`.

Primary source: [custom-commands.md in the gemini-cli repo](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md).

## The format in 60 seconds

- **File:** TOML, extension `.toml`, one command per file.
- **Locations:** user-global at `~/.gemini/commands/<name>.toml`, project at `.gemini/commands/<name>.toml`. Project wins on collisions.
- **Namespacing:** subdirectories become `:`-separated names. `~/.gemini/commands/git/commit.toml` → `/git:commit`.
- **Minimum viable file:** a single `prompt` field. That's it.

## Step 1 — Make your commands directory

```bash
mkdir -p ~/.gemini/commands
```

## Step 2 — Write your first command

Create `~/.gemini/commands/research.toml`:

```toml
description = "Research a topic and summarize findings with sources."

prompt = """
You are a thorough research assistant. For the topic below, produce:

1. A 5-bullet summary of the state of the art.
2. Key sources with URLs (primary/official first, then high-quality secondary).
3. Open questions that would be worth investigating further.

Topic: {{args}}

Respect any conventions defined in GEMINI.md. Cite specific URLs inline.
"""
```

## Step 3 — Reload without restarting

In a running Gemini CLI session:

```
/commands reload
```

Now `/research vector databases for RAG` is a valid command.

## The three injection primitives

Inside a `prompt = "..."` block you get three kinds of substitution.

### Arguments — `{{args}}`

Expands to whatever the user typed after the command name. If your prompt doesn't include `{{args}}`, the raw tail is appended at the end of the prompt.

### Shell execution — `!{command}`

Runs a shell command at invocation time; its stdout/stderr is substituted into the prompt. Gemini CLI prompts before running (unless you've pre-approved the command in settings). Braces must be balanced.

```toml
prompt = """
Summarize the staged changes and propose a conventional-commit message.

Staged diff:
!{git diff --staged}

Repo context:
!{git log --oneline -10}
"""
```

### File embedding — `@{path}`

Embeds the file's contents (or a directory listing). Processed before `!{}` and `{{args}}`.

```toml
prompt = """
Using the team style guide below, review the file the user is asking about.

Style guide:
@{./docs/style-guide.md}

File to review: {{args}}
"""
```

## A full example — `/commit`

Save as `~/.gemini/commands/commit.toml`:

```toml
description = "Inspect staged changes, write a conventional-commit message, commit."

prompt = """
Read the staged diff below and produce a conventional-commit message.

Staged diff:
!{git diff --staged}

Recent commit style (match this tone):
!{git log --pretty=format:'%s' -10}

Rules:
- Subject line under 72 characters, imperative mood.
- Body explains the *why*, not the *what* — the diff already shows what.
- No trailing period on the subject.
- If the diff touches multiple concerns, split into multiple commits and propose the split instead of committing.

When you have the message, run:
!{git commit -m "<your subject>" -m "<your body>"}

If the diff is empty, tell me and stop.
"""
```

Invoke with `/commit`.

## A full example — `/review`

Save as `~/.gemini/commands/review.toml`:

```toml
description = "Review the branch's changes against our review checklist."

prompt = """
Review the changes on the current branch (against main) using the checklist below.

Checklist:
@{./.gemini/review-checklist.md}

Branch diff:
!{git diff main...HEAD}

Produce output in this shape:
## Summary
<2-3 sentences>

## Concerns (by severity)
- **Critical:** <or 'none'>
- **Should fix:** <or 'none'>
- **Nit:** <or 'none'>

## Specific comments
- `path/to/file.ts:L123` — <comment>

Be specific about line numbers and quote the relevant diff. Don't hedge.
"""
```

## Namespaced commands

Create `~/.gemini/commands/git/commit.toml` and `~/.gemini/commands/git/push.toml` — they become `/git:commit` and `/git:push`. Useful once you have more than ~10 commands.

```bash
mkdir -p ~/.gemini/commands/git
# move commit.toml into ~/.gemini/commands/git/
```

## Extensions can ship commands

If you're packaging commands for a team, put them in a Gemini CLI extension: an extension directory with `gemini-extension.json` and a `commands/` subdirectory. Users install with `gemini extensions install <github-url>`. Covered in Ch. 6.

## Debugging commands

- **`/commands list`** — shows every command and its source (user, project, extension).
- **`/commands reload`** — re-reads after you edit a file.
- **If `/foo` doesn't show up,** check the filename is `foo.toml` (not `foo.md`, not `foo`).
- **If `{{args}}` seems empty,** you forgot to pass arguments or you have a typo (`{args}` is wrong).
- **If `!{...}` isn't running,** you probably have unbalanced braces inside the command. Quote or escape as needed.

## Project vs user

Commit `.gemini/commands/*.toml` to the repo when the command is team-wide (like `/review`). Keep `~/.gemini/commands/*.toml` for personal shortcuts.

## Things this format doesn't have (yet, as of April 2026)

- No typed/named argument schema. You get `{{args}}` as a raw string and parse it in the prompt. If you need structure, ask for it in the prompt text.
- No conditional logic in the TOML itself. If your command has branches, it's probably a skill (Ch. 6).

## References

- [Official custom-commands docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)
- [Gemini CLI reference commands](https://geminicli.com/docs/reference/commands/)
- [Extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
