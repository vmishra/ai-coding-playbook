# Claude Code settings examples

## Files

- [`settings.example.json`](./settings.example.json) — a reasonable starter `~/.claude/settings.json`. Permissions block defaults to "ask for anything that edits or runs code." Hooks wired to the three Claude Code hook assets (block-rm-rf, format-after-edit, audit-log).

## Install

**Do not wholesale replace your existing `~/.claude/settings.json`.** Open both files side-by-side and copy the pieces that fit.

If you don't have a settings file yet:

```bash
mkdir -p ~/.claude
cp settings.example.json ~/.claude/settings.json
```

Then verify the hook script paths exist (see [hook assets](../hooks/)).

## What each section is for

- **`permissions`**: Which tools run without prompting vs which ones ask. The starter here errs on the side of ask-before-edit. Loosen over time as you build trust in the agent on a particular project.
- **`hooks`**: Wire in the three starter hooks. Comment or remove entries for hooks you haven't installed yet.

See [Chapter 8](../../../chapters/08-hooks/claude-code/README.md) for the hook walkthrough.
