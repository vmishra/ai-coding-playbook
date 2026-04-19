# Chapter 14 — IDE Integration

> When the terminal wins, when the IDE wins, and the Google-specific answers (Firebase Studio, Cloud Workstations) that most content undersells.

---

## The durable question

For any piece of work, you're choosing between:

- **Terminal-first**: CLI has focus; editor is a window you switch to for reading. Keystrokes go to the agent.
- **IDE-first**: editor has focus; agent is a side panel. Keystrokes go to your code; you prompt the agent when you need to.
- **Agent-first IDE**: the agent is the primary surface, with the editor as one of several views. Antigravity (Ch. 19) is the current canonical example.

Different tasks call for different modes. Pick deliberately.

## When terminal wins

- Long exploratory sessions where you'll have the agent read broadly.
- Headless runs (CI, scheduled tasks, scripted workflows).
- Anything where you want to compose the agent with shell tooling (pipes, direnv, tmux).
- When you already live in tmux and switching to an IDE would be friction.

Terminal CLIs (Gemini CLI, Claude Code) assume you're comfortable at the shell. If you are, they're the most powerful surface.

## When IDE wins

- Heavy in-file editing where you want diffs reviewed inline.
- Quick targeted changes where you don't need a full session's context.
- Pairing humans and agents on the same file — you type, it suggests, you accept or reject.
- Cross-referencing agent output with surrounding code visually.

## VS Code integration

Both tools ship first-party VS Code integration. This is the right default for most engineers.

### Gemini CLI in VS Code

Native terminal + the official Gemini Code Assist extension (which pairs tightly with Gemini CLI). [Docs](https://developers.google.com/gemini-code-assist).

Good pattern: keep `gemini` open in the integrated terminal for sessions; use Gemini Code Assist in-editor for inline suggestions and quick targeted changes.

### Claude Code in VS Code

Native terminal + the [Claude Code VS Code extension](https://code.claude.com/docs/en/ides). The extension picks up your `~/.claude/` config, shows sessions in a side panel, and lets you trigger commands and skills from the palette.

Same pattern: `claude` in the integrated terminal for agentic sessions, extension for in-editor quick actions.

## JetBrains integration

- Gemini Code Assist has a JetBrains plugin.
- Claude Code has a JetBrains plugin ([docs](https://code.claude.com/docs/en/ides)).

Same logic as VS Code — terminal for sessions, plugin for targeted work.

## Firebase Studio (Google's agentic cloud IDE)

The answer when someone asks "what's Google's cloud IDE?" Firebase Studio ([firebase.google.com/docs/studio](https://firebase.google.com/docs/studio)) is a browser-based, agentic full-stack dev environment built on Cloud Workstations infrastructure. It's the current canonical Google offering for browser-first development, and it subsumes the old Project IDX product (which was renamed to Firebase Studio on April 15, 2025 — IDX no longer exists as a separate product).

**What it gives you:**

- Full VS Code-compatible editor in the browser.
- Gemini-powered agent baked in.
- First-party Firebase, Cloud Run, App Hosting integration.
- Fast spin-up from a template or from an existing repo.
- No local setup — any laptop with a browser works.

**When to reach for it:**

- Prototyping or early-stage work where local setup friction isn't worth paying.
- Full-stack apps where Firebase is in the picture.
- Demos and codelabs.
- Teaching — no "but my Mac has a broken Node install" problem.

**When not to:**

- Latency-sensitive work where round-tripping to a remote host is painful.
- Heavy offline work.
- Codebases with tooling that's hard to run in the browser environment.

## Cloud Workstations

[Cloud Workstations](https://cloud.google.com/workstations/docs) is the underlying VM-based dev environment service. Firebase Studio sits on top; Cloud Workstations is the lower-level offering you'd use for:

- Large monorepos that don't fit in browser-native tooling.
- Teams that need customized base images (pre-installed tools, proprietary SDKs, specific language toolchains).
- Compliance / data-residency requirements that make a managed VM with VPC-SC controls the right answer.
- Persistent dev environments that survive disconnects and last days.

Pre-installed tooling typically includes Gemini CLI. You SSH in (or use the web IDE), open a Gemini CLI session, and work exactly as you would locally.

**The big win:** a new engineer gets a fully configured environment in minutes instead of days. Add "agent pre-installed with the team's extension and CLAUDE.md" and you have a radically lower onboarding bar.

## Agent-first IDEs (Antigravity, Cursor)

Different enough to get their own chapter. See:

- [Chapter 19 — Google Antigravity](../19-antigravity/README.md) for the Google agent-first IDE.
- Cursor is discussed in Ch. 2; it's a reasonable non-Google option.

The short version: agent-first IDEs trade granular control for higher-autonomy workflows. Right choice for some work, wrong for others. Try them; don't marry them.

## The mixed setup that actually works

Most senior engineers end up running a mixed setup:

- **Terminal** (tmux + CLI) for deep sessions, exploration, and anything that benefits from shell composition.
- **VS Code or JetBrains** with the appropriate extension for targeted in-editor work, quick fixes, inline suggestions.
- **Firebase Studio or Cloud Workstations** for full-stack prototypes and for onboarding new teammates fast.
- **Antigravity / Cursor** occasionally for work that fits the agent-first flow — tried, kept in the rotation, not the only tool.

Pick the mode that fits the task. Treat the surfaces as interchangeable runtimes over the same underlying concepts — memory, commands, skills, MCP, hooks — which you've already built once.

## References

- [Firebase Studio docs](https://firebase.google.com/docs/studio)
- [Cloud Workstations docs](https://cloud.google.com/workstations/docs)
- [Gemini Code Assist](https://developers.google.com/gemini-code-assist)
- [Claude Code IDE integrations](https://code.claude.com/docs/en/ides)
- IDX → Firebase Studio migration note: [firebase.google.com/docs/studio/idx-is-firebase-studio](https://firebase.google.com/docs/studio/idx-is-firebase-studio)
