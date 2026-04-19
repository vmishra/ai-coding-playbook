# Claude Code — Hooks Walkthrough

Verified against [Claude Code hooks docs](https://docs.claude.com/en/docs/claude-code/hooks). Current hook event list was sourced from the hooks reference on 2026-04-19; Anthropic occasionally adds events — check the docs if one seems missing.

## The event list

All events that can fire a hook:

**Session lifecycle**
- `SessionStart`, `SessionEnd`, `InstructionsLoaded`, `CwdChanged`

**User interaction**
- `UserPromptSubmit`, `Notification`, `Elicitation`, `ElicitationResult`

**Tool use**
- `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`

**Subagents and tasks**
- `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`

**Stop and continuation**
- `Stop`, `StopFailure`, `TeammateIdle`

**Environment**
- `ConfigChange`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`

**Compaction**
- `PreCompact`, `PostCompact`

## Where hooks are configured

In `settings.json` under the `hooks` key. Supports user, project, and local scopes, same as other settings.

## Config shape

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh",
            "timeout": 10000
          }
        ]
      }
    ]
  }
}
```

- **`matcher`**: `"*"` or omitted = all tools. A plain tool name or pipe-alternation = exact match (`"Bash|Edit"`). Anything else is a JS regex.
- **`if`** (tool events only): a permission-rule expression that further filters. The hook runs only if the matcher passes *and* `if` evaluates true.
- **`type`**: `command` (stdin JSON / stdout JSON), `http` (POST body / response JSON), `prompt`, or `agent`.
- **`command`**: the shell command. `$CLAUDE_PROJECT_DIR` is set by the CLI.
- **`timeout`**: milliseconds.

## Output protocol

Three ways a hook communicates back:

1. **Exit 0 + JSON on stdout** → fine-grained control.
2. **Exit 2** → hard block. stderr is surfaced to Claude as an error message.
3. **Other nonzero exit** → non-blocking warning.

### Universal JSON fields

```json
{
  "continue": true,
  "stopReason": "optional message to show"
}
```

### For `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop`, `ConfigChange`, `PreCompact`

Top-level `decision: "block"` + `reason` blocks the event:

```json
{ "decision": "block", "reason": "Reason surfaced to Claude." }
```

### For `PreToolUse` — nested `hookSpecificOutput`

```json
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive command blocked by hook"
  }
}
```

`permissionDecision` values: `allow`, `deny`, `ask`, `defer`.

## Working example — block `rm -rf`

### Register the hook

`~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm-rf.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

### The script

`~/.claude/hooks/block-rm-rf.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Read the event payload from stdin
payload="$(cat)"

# Extract the Bash command from the payload (jq is robust; fall back if missing)
cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"

# Block anything resembling rm -rf, rm -fr, rm -r --force, or rm of root-like paths
if printf '%s' "$cmd" | grep -Eq '(rm[[:space:]]+([^#]*-[a-z]*r[a-z]*f|[^#]*-[a-z]*f[a-z]*r|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive)|rm[[:space:]]+-rf?[[:space:]]+/(\s|$))'; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive rm command blocked by hook: $cmd"
  }
}
EOF
  exit 0
fi

# Allow by emitting no decision (empty stdout, exit 0)
exit 0
```

Make it executable:

```bash
chmod +x ~/.claude/hooks/block-rm-rf.sh
```

Test it out-of-band before trusting it:

```bash
echo '{"tool_input":{"command":"rm -rf /tmp/test"}}' | ~/.claude/hooks/block-rm-rf.sh
# Expect: JSON with permissionDecision: "deny"
```

```bash
echo '{"tool_input":{"command":"ls -la"}}' | ~/.claude/hooks/block-rm-rf.sh
# Expect: no output, exit 0
```

## Working example — auto-format on edit

`PostToolUse` on the `Edit` and `Write` tools, running your formatter and surfacing errors back to the agent.

`~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format-after-edit.sh",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

`~/.claude/hooks/format-after-edit.sh`:

```bash
#!/usr/bin/env bash
set -uo pipefail

payload="$(cat)"
path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // ""')"

# Bail quietly if we can't identify the file
[[ -z "$path" ]] && exit 0
[[ ! -f "$path" ]] && exit 0

# Prettier for JS/TS/JSON/MD, gofmt for Go, black for Python, rustfmt for Rust.
case "$path" in
  *.js|*.jsx|*.ts|*.tsx|*.json|*.md|*.yml|*.yaml)
    if command -v prettier >/dev/null 2>&1; then
      prettier --write "$path" >/dev/null 2>&1 || true
    fi
    ;;
  *.go)
    command -v gofmt >/dev/null 2>&1 && gofmt -w "$path" || true
    ;;
  *.py)
    command -v black >/dev/null 2>&1 && black --quiet "$path" || true
    ;;
  *.rs)
    command -v rustfmt >/dev/null 2>&1 && rustfmt "$path" || true
    ;;
esac

exit 0
```

This is a "fail-open" hook — if the formatter isn't installed, we silently skip it. The edit still succeeds.

## Working example — audit log

`PostToolUse` on every tool, appending a JSONL line:

```bash
#!/usr/bin/env bash
set -uo pipefail

payload="$(cat)"
log="${CLAUDE_PROJECT_DIR}/.claude/audit.log"
mkdir -p "$(dirname "$log")"

# Timestamp + compact payload; strip anything sensitive upstream if needed
printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$payload" >> "$log"
exit 0
```

`grep` through `audit.log` when something weird happened and you need to reconstruct what the agent did.

## Debugging

- **Nothing happens.** Restart Claude Code; hooks are read at session start.
- **Hook fires but decision is ignored.** Check your JSON shape — `PreToolUse` needs nested `hookSpecificOutput`; other events use top-level `decision`.
- **Hook silently crashes.** Run the command manually with a representative stdin payload. Check `~/.claude/logs/` for hook errors.

## Scoping hooks with `if`

The `if` field is powerful. It accepts the same permission-rule syntax as `allowed-tools` on commands and skills:

```json
{ "matcher": "Edit|Write", "if": "Edit(src/billing/**)", "hooks": [ ... ] }
```

Only fires when Edit/Write touches files under `src/billing/`. This is how you get path-scoped enforcement without writing path logic into every script.

## References

- [Hooks reference](https://docs.claude.com/en/docs/claude-code/hooks)
- [Settings + permissions](https://code.claude.com/docs/en/settings)
