# Claude Code skill assets

Drop-in skill directories. Each subdirectory is a runnable skill. Copy into `~/.claude/skills/` (personal) or `.claude/skills/` (project, team-shared).

## What's here

| Skill | Triggers when... | What it produces |
|---|---|---|
| [`pr-description/`](./pr-description/) | User asks for a PR description or branch summary | A structured PR description using the team template (or the default shape) |
| [`test-gen/`](./test-gen/) | User asks to write tests or add coverage for a file/function | A test plan first, then tests matching the repo's existing conventions |

## Install

```bash
# Personal
cp -r pr-description test-gen ~/.claude/skills/

# Or project-scoped (shared with the team)
mkdir -p .claude/skills
cp -r pr-description test-gen .claude/skills/
```

Restart (or start) a Claude Code session. Verify with `/skills`.

## Design notes

Both skills share a discipline worth stealing:

1. **Read first, decide second.** The skill's body walks the agent through gathering context before producing output. This avoids confident hallucination.
2. **Pause-for-approval checkpoint.** `test-gen` outputs the plan first and waits. You can approve, redirect, or cut scope before any test file exists.
3. **Tight `allowed-tools`.** Neither skill opens general shell — each is scoped to only the commands it genuinely needs. Safe to share.

See [Chapter 6](../../../chapters/06-skills/claude-code/README.md) for the full walkthrough and frontmatter reference.
