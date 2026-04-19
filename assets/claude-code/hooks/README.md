# Claude Code hook assets

Three drop-in hook scripts covering the highest-leverage patterns.

## What's here

| Script | Event | What it does |
|---|---|---|
| [`block-rm-rf.sh`](./block-rm-rf.sh) | `PreToolUse` on `Bash` | Blocks destructive `rm -rf` variants before they execute. |
| [`format-after-edit.sh`](./format-after-edit.sh) | `PostToolUse` on `Edit\|Write` | Runs the project's formatter on the edited file. Fail-open. |
| [`audit-log.sh`](./audit-log.sh) | `PostToolUse` on any tool | Appends every tool call to `.claude/audit.log` as JSONL. |

## Install

```bash
mkdir -p ~/.claude/hooks
cp *.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/*.sh
```

Then register them in `~/.claude/settings.json`. Each script's header includes the exact settings snippet.

## Test each hook out-of-band

```bash
# block-rm-rf: should emit a deny decision
echo '{"tool_input":{"command":"rm -rf /tmp/x"}}' | ~/.claude/hooks/block-rm-rf.sh

# block-rm-rf: should pass
echo '{"tool_input":{"command":"ls -la"}}' | ~/.claude/hooks/block-rm-rf.sh

# format-after-edit: should be a no-op if the file doesn't match
echo '{"tool_input":{"file_path":"/tmp/doesnotexist"}}' | ~/.claude/hooks/format-after-edit.sh

# audit-log: writes a line to CLAUDE_PROJECT_DIR/.claude/audit.log
CLAUDE_PROJECT_DIR=/tmp echo '{"tool":"Edit"}' | ~/.claude/hooks/audit-log.sh
cat /tmp/.claude/audit.log
```

## Notes

- All three scripts use `jq` when available and degrade to `grep`/`sed` when it isn't. Still worth installing `jq` — `brew install jq`, `apt install jq`, `dnf install jq`.
- `audit-log.sh` is the single most useful hook to have running at all times. Disk is cheap; being able to replay "what the agent actually did" is priceless.
- These scripts are fail-open for convenience (formatter) and fail-closed for safety (block-rm-rf). Read each header before customizing.

See [Chapter 8](../../../chapters/08-hooks/claude-code/README.md) for the walkthrough, event list, and output protocol.
