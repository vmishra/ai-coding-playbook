# Gemini CLI skill assets

Drop-in skills. Copy into `~/.gemini/skills/` (user) or `.gemini/skills/` (workspace-shared).

## What's here

| Skill | Triggers when... | What it produces |
|---|---|---|
| [`pr-description/`](./pr-description/) | User asks for a PR description or branch summary | Structured PR description using the team template (or default shape) |

## Install

```bash
# User
mkdir -p ~/.gemini/skills
cp -r pr-description ~/.gemini/skills/

# Or workspace (shared with team)
mkdir -p .gemini/skills
cp -r pr-description .gemini/skills/
```

Restart Gemini CLI.

See [Chapter 6](../../../chapters/06-skills/gemini-cli/README.md) for the walkthrough and extension-packaging guidance.
