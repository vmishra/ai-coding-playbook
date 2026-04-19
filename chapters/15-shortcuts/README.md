# Chapter 15 — Keybindings and Shortcuts

> The shortcuts that pay for themselves in the first week. Short chapter by design — don't memorize what you won't use.

---

## The rule

Learn four keybindings today. Add one when it hurts not to have it. Don't sit down with a 60-item cheat sheet — you'll retain none of it.

## Gemini CLI — core bindings

In-session (active prompt):

| Binding | What it does |
|---|---|
| `Ctrl+C` (2x) | Cancel the current turn / exit |
| `Ctrl+L` | Clear the terminal view (history preserved) |
| `Ctrl+D` | Exit the session |
| `Ctrl+R` | Reverse-search through your input history |
| `Tab` | Autocomplete command / path / file mention |
| `Esc` | Interrupt the model mid-response |
| `↑` / `↓` | Navigate previous inputs |
| `/` | Open the slash-command menu |
| `@` | Start a file reference |
| `!` | Run a shell command without full tool execution |

Slash commands worth memorizing first (they save the most time):

| Command | Use |
|---|---|
| `/help` | List every command. Start here. |
| `/memory show` | Show the concatenated GEMINI.md currently in context |
| `/memory reload` | Reload memory files after edits |
| `/commands reload` | Reload custom commands after edits |
| `/mcp` | List active MCP servers |
| `/bug` | Submit a bug report with session log attached |
| `/compress` | Compact the current context (version-dependent name) |
| `/chat save <name>` | Checkpoint the session |
| `/chat resume <name>` | Restore a checkpoint |

Full reference: [Gemini CLI commands](https://geminicli.com/docs/reference/commands/).

## Claude Code — core bindings

In-session:

| Binding | What it does |
|---|---|
| `Ctrl+C` | Cancel the current turn |
| `Ctrl+D` | Exit the session |
| `Esc` | Interrupt the model mid-response |
| `↑` / `↓` | Navigate previous inputs |
| `Tab` | Autocomplete |
| `/` | Slash-command menu |
| `@` | File reference |
| `!` | Bash command without full tool routing (in some versions) |

Slash commands worth memorizing first:

| Command | Use |
|---|---|
| `/help` | List every command |
| `/context` | Show current context usage |
| `/compact [hint]` | Compact with optional focus hint |
| `/clear` | Reset conversation (keeps config) |
| `/model` | Switch models mid-session |
| `/permission-mode` | Change permission mode live |
| `/memory` | List loaded memory files |
| `/skills` | List loaded skills |
| `/agents` | List subagents |
| `/mcp` | List MCP servers |
| `/continue` | Resume the previous session |
| `/exit` | End the session |

Full reference: [Claude Code commands](https://code.claude.com/docs/en/cli-reference).

## The four to start with

Regardless of tool, these four earn their keep in the first day:

1. **The context-view command** — `/context` (Claude) or `/memory show` (Gemini). Check it between sub-tasks to catch bloat early.
2. **The compaction command** — `/compact` (Claude), `/compress` (Gemini). Run it the moment signal-to-noise drops.
3. **`Esc` to interrupt.** The model heads in the wrong direction, cut it off immediately — don't wait for it to finish.
4. **The file-reference `@` syntax.** Inline files into your prompt instead of copy-pasting. `@src/auth/middleware.ts` is immediate.

## IDE-mode shortcuts

For the VS Code and JetBrains integrations, refer to each extension's keybinding panel — they evolve too fast to document durably. The pattern to expect:

- A keybinding to open the agent panel.
- A keybinding to send the current selection as context.
- A keybinding to accept / reject suggested edits.

Rebind to something you'll remember. `Cmd+L` / `Ctrl+L` is a common convention for "send to agent."

## Antigravity

Its own shortcut surface — see [Ch. 19](../19-antigravity/README.md) or the [Antigravity docs](https://antigravity.google/docs/home).

## What not to bother with

- Exotic bindings you'll use once a quarter. Learn them when you need them.
- Remapping for aesthetics. Muscle memory is load-bearing; don't retrain it without a reason.
- Multi-keystroke chords that add no speed over typing `/command`.

## References

- Gemini CLI — [Commands reference](https://geminicli.com/docs/reference/commands/)
- Claude Code — [CLI reference](https://code.claude.com/docs/en/cli-reference)
