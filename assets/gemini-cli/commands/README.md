# Gemini CLI slash command assets

Drop-in `.toml` commands. Copy the ones you want into `~/.gemini/commands/` (or `.gemini/commands/` in your repo for team-shared commands) and run `/commands reload` in an existing session.

## What's here

| File | Command | What it does |
|---|---|---|
| `research.toml` | `/research <topic>` | Web-research a topic and produce a structured summary with sources. |
| `commit.toml` | `/commit` | Inspect the staged diff, propose a conventional commit message, commit. |
| `review.toml` | `/review` | Review branch changes vs `main` with severity-classified comments. |

## Install

```bash
mkdir -p ~/.gemini/commands
cp research.toml commit.toml review.toml ~/.gemini/commands/
```

In an open Gemini CLI session:

```
/commands reload
```

## Notes

- `/commit` uses `!{git commit …}` — Gemini will prompt for confirmation the first time.
- `/review` assumes your default branch is `main`. Adjust the `git diff` target if yours differs.
- `/research` is the most useful of the three on day one — make a habit of it before editing unfamiliar code.

See [Chapter 5](../../../chapters/05-slash-commands/gemini-cli/README.md) for the full walkthrough.
