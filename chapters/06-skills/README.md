# Chapter 6 — Agent Skills

> Capabilities the agent discovers and reaches for on its own. The primitive you need when a slash command has grown branches.

---

## The concept

A slash command is invoked by you; a *skill* is invoked by the agent.

A skill is a named capability, stored as a directory with a description, optional body, and optional support files (templates, helpers, examples). The agent sees the *description* up-front — enough to know a skill exists and what it's for — and loads the full body only when it decides to use it. That "discover-but-don't-load" property is the whole point. You can ship twenty skills and pay only for the descriptions in idle context; the detail is loaded lazily.

If that sounds like a plugin model from any IDE you've used, it is. The difference is the agent picks *when* to reach for the skill, the same way you or a colleague would reach for the right tool in a toolbox. That's the durable idea. The filenames and frontmatter fields will drift over time; the discovery pattern won't.

## When to prefer a skill over a command

| Question | Answer |
|---|---|
| Do I want to invoke this myself? | **Slash command** (Ch. 5). |
| Do I want the agent to notice when it's relevant? | **Skill.** |
| Does it must-always-run regardless of what the agent thinks? | **Hook** (Ch. 8). |
| Is it so involved it should run in its own subagent with its own context? | **Subagent** (Ch. 11). |

Some real examples to calibrate:

- **"When the user asks to generate a PR description, produce it in our team's format."** → Skill. The agent should reach for it automatically on matching intent.
- **"When any edit happens in `src/billing/`, enforce the currency-code rule."** → Path-scoped rule or hook, not a skill.
- **"Look up an issue, summarize it, propose next step."** → Command. You invoke this.
- **"Migrate this entire subsystem from library X to library Y across dozens of files."** → Subagent with its own plan, or a skill that *delegates* to a subagent.

## What a skill contains

A skill is a folder:

```
skills/<skill-name>/
├── SKILL.md         # required entrypoint (description + instructions)
├── examples/        # optional: reference outputs
├── templates/       # optional: files to adapt or copy
└── helpers/         # optional: scripts the skill invokes
```

The `SKILL.md` usually has:

1. **YAML frontmatter** with at minimum a `description` — enough to tell the agent when to reach for the skill.
2. **Body** — the instructions the agent follows once invoked. Loaded on demand.

Best-in-class skill descriptions are short, specific, and name the trigger. "Use when the user asks for a PR description on a branch" beats "helps with PRs."

## Design principles

### 1. One skill, one clear trigger

A skill that's "helpful in many situations" is a skill the agent will reach for badly. Name the trigger explicitly in the description so the model's self-selection is tight.

### 2. The description is load-bearing

The agent sees the description at session start and decides whether to load the skill. The description is how the skill gets picked. Spend time on it.

### 3. Keep the body focused

When the body loads, it becomes context. If it's 2,000 lines, you're paying full token cost every time the skill fires. Break helper material into files the skill references, not inlines.

### 4. Scope with paths when you can

If a skill only applies to certain paths, say so. Both tools support path-scoped activation in some form. This prevents the agent from reaching for "currency rule" logic when editing unrelated code.

### 5. Skills can spawn subagents

For anything heavy — a multi-file refactor, a deep investigation — the skill's body can offload into a subagent so the primary context stays clean. See Ch. 11.

## The difference between a great skill and mediocre skill

A great skill:

- Has a one-sentence description that *only* matches its actual use case.
- Loads a short, focused body that tells the agent *exactly* what to do and what to avoid.
- Produces consistent output every time — same section headers, same tone, same structure.
- References existing team artifacts (`docs/style-guide.md`) instead of duplicating them.

A mediocre skill:

- Has a vague description, matches too broadly, fires when you don't want it to.
- Has a 1,500-line body that's really a small book on the topic.
- Produces different-shaped output each time because the instructions are aspirational, not precise.
- Duplicates whatever's in `CLAUDE.md` / `GEMINI.md` because the author didn't check.

## Realizations

- [Claude Code Skills](./claude-code/README.md) — step-by-step, frontmatter reference, working `pr-description` skill.
- [Gemini CLI Skills and Extensions](./gemini-cli/README.md) — skills vs extensions, manifest, example extension that bundles MCP + commands + skill.

## Standards worth watching

Anthropic has published the skill format under the **open [Agent Skills](https://agentskills.io) standard**. Gemini CLI's skills follow a similar pattern. If this converges — and the signals as of April 2026 suggest it will — you'll be able to author a skill once and use it across tools. Worth betting on, worth checking on before you go deep.

## References

- Claude Code — [Skills docs](https://code.claude.com/docs/en/skills)
- Gemini CLI — [Skills docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md), [Extensions reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
- Open standard — [agentskills.io](https://agentskills.io)
