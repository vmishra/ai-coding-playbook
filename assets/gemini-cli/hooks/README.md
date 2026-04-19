# Gemini CLI hook assets

Mirrors the Claude Code hook discipline. Both files use `GEMINI_PROJECT_DIR` with a `CLAUDE_PROJECT_DIR` fallback so the scripts are portable.

## What's here

| Script | Event | What it does |
|---|---|---|
| [`block-rm-rf.sh`](./block-rm-rf.sh) | `BeforeTool` on `run_shell_command` | Blocks destructive `rm -rf` variants. |
| [`audit-log.sh`](./audit-log.sh) | `AfterTool` on any tool | Appends every tool call to `.gemini/audit.log` as JSONL. |

## Install

```bash
mkdir -p ~/.gemini/hooks
cp *.sh ~/.gemini/hooks/
chmod +x ~/.gemini/hooks/*.sh
```

Register via `~/.gemini/settings.json` under the `hooks` key. Each script's header has the exact snippet.

## Test

```bash
echo '{"tool_args":{"command":"rm -rf /tmp/x"}}' | ~/.gemini/hooks/block-rm-rf.sh
# Expect: {"decision":"deny","reason":"..."}

echo '{"tool_args":{"command":"ls -la"}}' | ~/.gemini/hooks/block-rm-rf.sh
# Expect: no output, exit 0
```

See [Chapter 8](../../../chapters/08-hooks/gemini-cli/README.md) for the walkthrough.
