# Gemini CLI — Skills and Extensions

Step-by-step for both Gemini CLI **Skills** (newer, close analogue to Claude's skills) and **Extensions** (the broader package format that can bundle skills, commands, MCP servers, and hooks).

Primary sources:
- [Skills reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
- [Extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)

## Skills in 60 seconds

- **A skill is a directory.** `~/.gemini/skills/<name>/SKILL.md` (user), `.gemini/skills/<name>/SKILL.md` (workspace), `.agents/skills/<name>/SKILL.md` (alias). Workspace wins on collisions.
- **Format** is Markdown with YAML frontmatter, same open-standard shape as Claude's. Description loads up-front; body loads via the `activate_skill` tool when the model decides the skill is relevant.
- **Invoke** with `activate_skill` automatically, or force from the user side with the skill name.

## Step 1 — Create the skill directory

```bash
mkdir -p ~/.gemini/skills/pr-description
```

For workspace-scoped:

```bash
mkdir -p .gemini/skills/pr-description
```

## Step 2 — Write `SKILL.md`

```markdown
---
description: Generate a PR description in our team format. Use when the user asks for a PR description, draft, or summary of branch changes for a pull request.
---

You are generating a pull-request description for the current branch.

## 1. Gather context

Changes on the current branch vs main:
!{git diff main...HEAD}

Commits on this branch:
!{git log main..HEAD --pretty=format:'%s%n%b%n---'}

If `CONTRIBUTING.md` exists, read it — it may define our PR description template.

## 2. Produce the description

Output in exactly this shape:

## Summary
<1-3 sentences. What and why. No implementation details.>

## Changes
- <bullet per logical change, grouped by area>

## Test plan
- [ ] <concrete, verifiable check>
- [ ] <concrete, verifiable check>

## Risk and rollback
<What could break, how to roll back.>

## 3. Rules

- No marketing language ("streamlines", "unlocks", "supercharges"). Factual only.
- If the branch touches multiple concerns, say so and recommend splitting.
- If there are no tests and the change is non-trivial, list "add tests for X" in the Test plan.
```

## Step 3 — Verify

```bash
gemini
```

Then ask:

> "Generate a PR description for this branch."

Gemini should pick the skill via `activate_skill`. If it doesn't, tighten the description's trigger phrasing and retry.

## Extensions — the broader package

A skill is one artifact. An *extension* is the package format that can bundle many: MCP servers, custom slash commands, context files, skills, sub-agents, hooks, and policy rules — installed and updated as one unit.

Extensions live at `~/.gemini/extensions/<name>/` with a `gemini-extension.json` manifest.

### Install and manage

```bash
# Install from a git repo
gemini extensions install https://github.com/you/my-extension

# Install from a local directory
gemini extensions install ./path/to/extension

# Pin to a ref
gemini extensions install https://github.com/you/my-extension --ref v1.2.0

# Opt into auto-updates
gemini extensions install https://github.com/you/my-extension --auto-update

# Other lifecycle
gemini extensions list
gemini extensions enable <name>
gemini extensions disable <name>
gemini extensions update <name>
gemini extensions uninstall <name>
gemini extensions new <name>          # scaffold a new extension locally
gemini extensions link <path>         # develop against a local dir
```

Updates require a restart to take effect.

### The manifest — `gemini-extension.json`

Verified fields from the [extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md):

```json
{
  "name": "my-team-toolkit",
  "version": "0.1.0",
  "description": "Team-standard skills, commands, and integrations.",

  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${GEMINI_PROJECT_DIR}"]
    }
  },

  "contextFileName": "GEMINI.md",

  "excludeTools": [
    "run_shell_command(rm -rf)"
  ],

  "settings": [
    {
      "name": "TEAM_API_KEY",
      "description": "API key for the team internal service.",
      "envVar": "TEAM_API_KEY",
      "sensitive": true
    }
  ]
}
```

### Directory layout

An extension can bundle multiple asset types alongside the manifest:

```
my-team-toolkit/
├── gemini-extension.json       # manifest
├── commands/                   # custom slash commands (TOML)
│   └── gcp/
│       └── deploy.toml         # becomes /gcp:deploy
├── skills/
│   └── pr-description/
│       └── SKILL.md
├── agents/                     # sub-agents (*.md)
├── hooks/
│   └── hooks.json              # hook config (see Ch. 8)
├── GEMINI.md                   # optional context loaded when the extension is active
└── README.md
```

This is how you ship a cohesive "team developer platform" — one install, every engineer gets the same skills, commands, MCP wiring, and guardrails.

## Choosing: skill vs command vs extension

| You have... | Ship as... |
|---|---|
| One reusable capability the agent should reach for on its own | Skill |
| One prompt I invoke myself | Command |
| A bundle of several of the above, plus MCP and hooks, that travels together | Extension |

Most teams end up with a single internal extension repo that evolves over time.

## Settings and secrets

The `settings` array in `gemini-extension.json` collects config values at install time and writes them into a per-extension `.env`. Mark anything secret (`"sensitive": true`) so it doesn't echo to the terminal.

Don't put secrets in `SKILL.md`, in `GEMINI.md`, or in any committed file. The extension settings mechanism is the correct home.

## Discovery debugging

- `gemini extensions list` — installed extensions with their state.
- `/memory show` — also shows extension-provided context files.
- **"Why didn't my skill fire?"** — same answer as Claude: description isn't specific. Name the trigger.

## References

- [Skills reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md)
- [Extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
- [Custom commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md)
