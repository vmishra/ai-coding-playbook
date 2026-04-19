# Gemini CLI — Setup and First Session

## Install

Gemini CLI ships as an npm package. You need Node.js ≥ 20.

```bash
# Global install (recommended)
npm install -g @google/gemini-cli

# Or run once without installing
npx https://github.com/google-gemini/gemini-cli
```

Verify:

```bash
gemini --version
```

If you're on macOS and `npm install -g` wants sudo, stop and fix your Node setup first (use `nvm`, `fnm`, or `volta`). Don't sudo-install Node packages — you'll regret it.

Official repo: [github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli).

## Auth: three modes, pick one

The first time you run `gemini`, it prompts for auth. There are three modes, in roughly increasing order of how serious your usage is:

### 1. Personal Google account (free tier)

Easiest. The CLI opens a browser, you log in with a Google account, and you're done. Your free quota is tied to that account. Good for learning and side projects.

### 2. Gemini API key (`GEMINI_API_KEY`)

For programmatic use or when you want to pay per token instead of being throttled by free quota.

```bash
# Get a key from https://aistudio.google.com/apikey
export GEMINI_API_KEY="your-key-here"
gemini
```

Put the export in your shell profile or, better, in a per-project `.envrc` managed by [direnv](https://direnv.net/) so you don't leak keys across projects.

### 3. Vertex AI (Google Cloud project)

For enterprise work, teams, or anything touching Google Cloud. Ties usage to a GCP project, uses IAM, bills to your project, and enables the larger quotas.

```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GOOGLE_GENAI_USE_VERTEXAI=true
gemini
```

This is the right default if you work at Google, if your employer uses Google Cloud, or if you plan to run at scale. It also unlocks Model Garden models (Ch. 18).

## Config file

After first run, config lives at:

- **User:** `~/.gemini/settings.json` — applies to every project.
- **Project:** `.gemini/settings.json` — checked into the repo, shared with the team.

A reasonable starting `~/.gemini/settings.json`:

```json
{
  "contextFileName": "GEMINI.md",
  "theme": "Default",
  "coreTools": ["ShellTool", "EditFileTool", "ReadFileTool"],
  "telemetry": { "enabled": false }
}
```

We'll cover `contextFileName` in Ch. 4 (memory). For now, the default is fine.

## First session flags worth knowing

```bash
# Start with a specific model
gemini -m gemini-3-pro

# Headless / scripted mode — no interactive prompts
gemini -p "Summarize the changes since main"

# Plan mode — propose a plan, don't execute until approved
gemini --plan

# Sandbox (runs in a container — safer for untrusted code)
gemini --sandbox
```

`--plan` is the single most useful flag for learning. It makes the agent tell you what it's about to do before it does anything. Start every session with it until you trust the agent's judgment for a given repo.

## First-session checklist

In the repo you picked:

```bash
cd ~/projects/your-repo
gemini --plan
```

Then at the prompt:

```
> Walk me through how auth works in this codebase. Read only — don't edit.
```

When it responds:

1. Click through one file path it cites. Is it real? Is the code it quoted actually there?
2. Note how many files it read. (The session badge or `/context` shows this.)
3. Ask one follow-up. Notice how quickly the context grows.

You're now past the tutorial barrier. The rest of the playbook is about doing this well.

## Common first-run problems

- **"Auth keeps looping."** Your Google account probably needs Workspace permissions, or you're logged into multiple Google accounts in the browser. Log out of all of them, then retry.
- **"It can't find my project files."** You started `gemini` from the wrong directory. It treats the current directory as the project root.
- **"Quotas exhausted."** You're on the free tier and it's been a busy day. Either wait, or switch to `GEMINI_API_KEY` / Vertex AI auth.
- **"Node version error."** You're on an old Node. `nvm install 20` (or later) and retry.

## What to read next

- [Chapter 3 — Effective Prompting](../../03-prompting/README.md) — how to brief the agent.
- [Chapter 4 — Memory](../../04-memory/README.md) — set up `GEMINI.md` for your project.
