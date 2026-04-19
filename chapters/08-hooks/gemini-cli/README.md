# Gemini CLI — Hooks Walkthrough

Verified against [Gemini CLI hooks docs](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md) and [reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/reference.md).

## The event list

Gemini CLI's events are a near-superset of what you'll want. Grouped:

**Session lifecycle**
- `SessionStart`, `SessionEnd`

**Agent loop**
- `BeforeAgent`, `AfterAgent`
- `BeforeModel`, `AfterModel`

**Tool selection and execution**
- `BeforeToolSelection`
- `BeforeTool`, `AfterTool`

**Compression / notifications**
- `PreCompress`
- `Notification`

The protocol and output conventions mirror Claude's — unsurprising, since the tools share lineage through the emerging hook-as-policy pattern.

## Where hooks are configured

Three places, merged with more-specific winning:

- **System:** `/etc/gemini-cli/settings.json`
- **User:** `~/.gemini/settings.json`
- **Workspace:** `.gemini/settings.json`
- **Extension-bundled:** `<extension>/hooks/hooks.json` (note: not the manifest).

## Config shape

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "write_file|replace",
        "hooks": [
          {
            "name": "security-check",
            "type": "command",
            "command": "${GEMINI_PROJECT_DIR}/.gemini/hooks/security.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

- **`matcher`**: regex on tool events; exact string on lifecycle events.
- **`name`**: human label, surfaced in logs.
- **`type`**: `command` is the most common.
- **`timeout`**: milliseconds.

## Output protocol

Identical pattern to Claude Code:

- **Exit 0 + JSON on stdout** — fine-grained control, e.g. `{"decision": "deny", "reason": "..."}`.
- **Exit 2** — hard block, stderr goes to the agent.
- **Other nonzero exit** — non-blocking warning.

Environment variables the hook can rely on: `GEMINI_PROJECT_DIR`, `GEMINI_SESSION_ID`. A `CLAUDE_PROJECT_DIR` alias is also set for script portability — handy if you want a hook script that works under both CLIs.

## Working example — block `rm -rf`

`~/.gemini/settings.json`:

```json
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {
            "name": "block-rm-rf",
            "type": "command",
            "command": "${GEMINI_PROJECT_DIR}/.gemini/hooks/block-rm-rf.sh",
            "timeout": 5000
          }
        ]
      }
    ]
  }
}
```

`~/.gemini/hooks/block-rm-rf.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

payload="$(cat)"
cmd="$(printf '%s' "$payload" | jq -r '.tool_args.command // .tool_input.command // ""')"

if printf '%s' "$cmd" | grep -Eq '(rm[[:space:]]+([^#]*-[a-z]*r[a-z]*f|[^#]*-[a-z]*f[a-z]*r|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive)|rm[[:space:]]+-rf?[[:space:]]+/(\s|$))'; then
  cat <<EOF
{"decision":"deny","reason":"Destructive rm blocked by hook: $cmd"}
EOF
  exit 0
fi

exit 0
```

Make it executable:

```bash
chmod +x ~/.gemini/hooks/block-rm-rf.sh
```

## Working example — auto-format on write

`BeforeTool` would be too early (you'd be formatting the intent, not the file). Use `AfterTool` on `write_file`/`replace`:

```json
{
  "hooks": {
    "AfterTool": [
      {
        "matcher": "write_file|replace",
        "hooks": [
          {
            "name": "format-after-write",
            "type": "command",
            "command": "${GEMINI_PROJECT_DIR}/.gemini/hooks/format-after-write.sh",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

`~/.gemini/hooks/format-after-write.sh` — same body as the Claude Code version; both tools expose the target file path in the event payload.

## Coarse filtering without hooks

For simpler guardrails, Gemini CLI also supports `excludeTools` in settings or extension manifests:

```json
{
  "excludeTools": [
    "run_shell_command(rm -rf)",
    "run_shell_command(sudo *)"
  ]
}
```

This is regex-less, rule-based blocking. It covers a lot of cases with zero scripting. For anything more nuanced — logging, conditional logic, path scoping by directory — hooks remain the right primitive.

## Debugging

- Restart Gemini CLI after editing hook settings.
- Run the hook with a representative stdin JSON payload to verify behavior.
- Check the session log (shown by `/bug` or via `--log-level debug`) for hook invocation traces.

## Script portability tip

If you want a single hook script to work under both Claude Code and Gemini CLI:

```bash
project_dir="${CLAUDE_PROJECT_DIR:-${GEMINI_PROJECT_DIR:-$PWD}}"
```

Gemini CLI sets `CLAUDE_PROJECT_DIR` as an alias, so the above degrades cleanly.

## References

- [Hooks index](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md)
- [Hooks reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/reference.md)
- [Writing hooks](https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/writing-hooks.md)
