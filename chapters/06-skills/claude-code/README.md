# Claude Code — Skills

Step-by-step. Verified against the [official Skills docs](https://code.claude.com/docs/en/skills) and the [Agent Skills](https://agentskills.io) open standard.

## The format in 60 seconds

- **A skill is a directory.** `~/.claude/skills/<name>/SKILL.md` (personal), `.claude/skills/<name>/SKILL.md` (project). The directory can include support files.
- **`SKILL.md`** is Markdown with YAML frontmatter. Only `description` is strictly recommended; the rest are optional.
- **Discovery is two-stage.** At session start, Claude loads every skill's *description* (the frontmatter + first line or two). The *body* is loaded lazily when the model (or you) invokes the skill.

This two-stage design is why skills are cheap to have sitting around and expensive to load. Treat descriptions as your attention budget.

## Step 1 — Create the skill directory

```bash
mkdir -p ~/.claude/skills/pr-description
```

(If this skill should travel with the repo instead of your user config, create `.claude/skills/pr-description/` in the repo root.)

## Step 2 — Write `SKILL.md`

```markdown
---
description: Generate a PR description in our team format. Use when the user asks for a PR description, draft, or summary of branch changes for a pull request.
argument-hint: [optional: target-branch, default main]
allowed-tools: Bash(git diff:*) Bash(git log:*) Bash(gh pr:*) Read
---

You are generating a pull-request description for the current branch.

## 1. Gather context

Branch changes vs ${1:-main}:
!`git diff ${1:-main}...HEAD`

Commits on this branch:
!`git log ${1:-main}..HEAD --pretty=format:'%s%n%b%n---'`

If CONTRIBUTING.md exists, read it — it may define our PR description template.

## 2. Produce the description

Output in exactly this shape:

## Summary
<1-3 sentences. What and why. No implementation details.>

## Changes
- <bullet per logical change, grouped by area>

## Test plan
- [ ] <concrete verifiable check>
- [ ] <concrete verifiable check>

## Risk and rollback
<What could break, how to roll back.>

## 3. Rules

- No marketing language ("streamlines", "unlocks", "supercharges"). Factual only.
- If the branch touches more than one concern, say so and recommend splitting.
- If there are no tests and the change is non-trivial, list "add tests for X" in the Test plan.
```

## Step 3 — Verify

Start a fresh Claude Code session in the repo. Ask:

> "Generate a PR description for this branch."

The agent should recognize the intent and invoke the `pr-description` skill. You'll see it referenced in the transcript. If it doesn't fire, your description probably isn't specific enough (see "The description is load-bearing" in the concept chapter).

Alternatively, force it: `/pr-description` (some builds auto-expose skill directories as slash commands).

## Frontmatter reference

Verified from the [Skills docs](https://code.claude.com/docs/en/skills). All fields optional.

| Field | Purpose |
|---|---|
| `name` | Override the directory name. Usually leave blank. |
| `description` | What the skill is for. This is what the model sees up-front — spend real time on it. |
| `when_to_use` | Additional description-space budget for trigger guidance. |
| `argument-hint` | Autocomplete hint string. |
| `disable-model-invocation` | If `true`, only you (human) can invoke. Good for dangerous skills. |
| `user-invocable` | If `false`, only the model invokes it — never you. |
| `allowed-tools` | Pre-approved tools with fine-grained permission patterns. |
| `model` | Override the active model for this skill. |
| `effort` | `low` / `medium` / `high` / `xhigh` / `max`. For coding/agentic tasks, `xhigh` is a sensible default. |
| `context` | Set to `fork` to run the skill in a subagent with its own context. |
| `agent` | Which subagent type to spawn when `context: fork`. |
| `hooks` | Skill-scoped hooks. |
| `paths` | Glob patterns that scope auto-activation to certain files. |
| `shell` | `bash` or `powershell`. |

There is no `trigger` field. Triggering comes from `description` + optional `when_to_use` + optional `paths`.

## The description budget

Claude Code's combined cap per skill listing entry (description + when_to_use) is ~1,536 characters, and the total skill-description budget per session is ~1% of context (default floor 8,000 chars; overridable via `SLASH_COMMAND_TOOL_CHAR_BUDGET`). Don't write novels in descriptions.

## Path-scoping with `paths`

Scope a skill to specific files so it only enters the attention pool when relevant:

```yaml
---
description: Enforce billing-module invariants when editing billing code.
paths:
  - "src/billing/**"
  - "src/__tests__/billing/**"
---
```

This is often a better fit than a broad description. The model ignores the skill entirely until the work touches matching files.

## Running a skill in its own context

For expensive skills — long investigation, multi-file refactor — set `context: fork` so the body runs in a subagent with its own context window. Your primary context stays clean.

```yaml
---
description: Migrate a file from lodash to vanilla ES. Use when the user asks to remove lodash from a file.
context: fork
agent: refactor
allowed-tools: Read Edit Grep
effort: xhigh
---
```

The subagent gets a fresh context scoped to the task, runs to completion, and returns a summary — the tens of thousands of tokens it consumed do not pollute your primary session.

## A second example — `/pr-summary-for-slack`

A short, tightly-scoped skill:

```markdown
---
description: Summarize a merged PR for a Slack release channel. Use when asked for a Slack-ready release note.
argument-hint: [pr-number]
allowed-tools: Bash(gh pr view:*)
disable-model-invocation: false
---

PR details:
!`gh pr view $1 --json title,body,author,url,files`

Produce a 3-line Slack message:
- Line 1: emoji + one-sentence user-facing description.
- Line 2: `@author` and PR link.
- Line 3: blast radius — which areas it touches.

No marketing language. Keep under 300 characters total.
```

## Discovery debugging

- `/skills` — list loaded skills with their sources.
- `/context` — see how much of your budget is spent on skill descriptions.
- **"Why didn't my skill fire?"** Usually the description isn't specific enough. Add explicit trigger language ("Use when the user asks for…").
- **"Why did my skill fire when I didn't want it to?"** Tighten the description or add `paths`.

## Installing the bundled asset

See [`assets/claude-code/skills/pr-description/`](../../../assets/claude-code/skills/pr-description/) for the complete, runnable version of the first skill above.

## References

- [Skills docs](https://code.claude.com/docs/en/skills)
- [Best Practices](https://code.claude.com/docs/en/best-practices)
- [Agent Skills open standard](https://agentskills.io)
