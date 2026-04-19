# Claude Code — Setup and First Session

## Install

Claude Code ships as an npm package. Node ≥ 18.

```bash
npm install -g @anthropic-ai/claude-code
claude --version
```

Official page: [anthropic.com/claude-code](https://www.anthropic.com/claude-code). Docs: [code.claude.com/docs](https://code.claude.com/docs).

If your `npm -g` install wants sudo, fix your Node setup (nvm, fnm, volta). Don't sudo it.

## Auth: two modes

### 1. Claude.ai subscription (easiest)

Run `claude`, approve the browser login, done. Your Claude Pro/Team/Enterprise subscription governs usage.

### 2. Anthropic API key

For programmatic use or per-token billing.

```bash
# From https://console.anthropic.com/
export ANTHROPIC_API_KEY="sk-ant-..."
claude
```

Put the key in a per-project `.envrc` (direnv), not in your shell rc. You do not want keys leaking across projects.

If you're at Google and this is your secondary tool, the Vertex AI partnership also makes Claude models available via Vertex; auth flows through GCP. See the [Vertex AI Claude docs](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude) for current instructions.

## Config files

- **User config:** `~/.claude/settings.json` — your personal preferences, applies everywhere.
- **Project config:** `.claude/settings.json` — shared, checked in.
- **Local project config:** `.claude/settings.local.json` — not checked in, for personal per-project overrides.

Minimal user config:

```json
{
  "theme": "dark",
  "permissions": {
    "allow": ["Read", "Grep", "Glob"],
    "ask":   ["Edit", "Write", "Bash"],
    "deny":  []
  }
}
```

The permission split above means: reads and searches run without asking, but any edit, write, or shell command requires your approval. This is the right default for your first week. Loosen later (Ch. 8).

## Directory layout for assets

```
~/.claude/
├── settings.json        # config
├── CLAUDE.md            # personal preferences the agent always sees
├── commands/            # your custom slash commands (one .md per command)
├── agents/              # custom subagents
├── skills/              # custom skills (folders with SKILL.md)
├── hooks/               # hook scripts
└── projects/            # transcripts (auto-managed)
```

Per-project, `.claude/` in the repo root does the same but is team-shared.

## First session flags

```bash
# Use a specific model
claude --model opus
claude --model sonnet

# Plan mode — propose before acting
claude --permission-mode plan

# Accept edits automatically (fast iteration, use carefully)
claude --permission-mode acceptEdits

# Headless / scripted
claude -p "Summarize changes since main"

# Continue your last session
claude --continue
```

The flag that pays for itself fastest is `--permission-mode plan`. Start every non-trivial session with it until you've built intuition for when the agent's judgment is reliable.

## First-session checklist

```bash
cd ~/projects/your-repo
claude --permission-mode plan
```

At the prompt:

```
> Walk me through how auth works here. Read only.
```

When it answers:

1. Click through one cited file path. Is the code really there?
2. Check `/context` to see what it's loaded.
3. Ask one follow-up. Notice context growth.
4. `/exit` and `/clear` so you don't carry state into the next task.

## Useful built-in commands

- `/context` — show current context window usage.
- `/compact` — summarize and compress history (Ch. 9).
- `/clear` — reset conversation, keeps config.
- `/model` — switch models mid-session.
- `/permission-mode` — change permission mode live.
- `/agents`, `/skills` — list loaded custom agents/skills.
- `/mcp` — list MCP servers and status.

## Common first-run problems

- **"Browser auth won't complete."** Multiple logged-in accounts. Log out, try again, or use an incognito window.
- **"It runs my commands without asking."** Your permission mode is `acceptEdits` or `bypassPermissions`. Switch to `default` or `plan`.
- **"Rate limited immediately."** You're probably on a Claude.ai account with heavy prior usage — wait for the window reset or switch to API auth.
- **"Can't find files."** Started `claude` outside the repo. Close, `cd`, relaunch.

## What to read next

- [Chapter 3 — Effective Prompting](../../03-prompting/README.md)
- [Chapter 4 — Memory](../../04-memory/README.md) — set up a `CLAUDE.md` for your project.
