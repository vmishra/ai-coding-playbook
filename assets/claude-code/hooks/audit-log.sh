#!/usr/bin/env bash
#
# PostToolUse hook for Claude Code — appends every tool call to an audit log.
# Invaluable for debugging why the agent did something weird, and the basis
# of any compliance trail.
#
# Install:
#   cp audit-log.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/audit-log.sh
#
# Register in ~/.claude/settings.json:
#   {
#     "hooks": {
#       "PostToolUse": [{
#         "hooks": [{
#           "type": "command",
#           "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-log.sh",
#           "timeout": 2000
#         }]
#       }]
#     }
#   }

set -uo pipefail

payload="$(cat)"
project_dir="${CLAUDE_PROJECT_DIR:-${PWD}}"
log="${project_dir}/.claude/audit.log"

mkdir -p "$(dirname "$log")"

# Timestamp + compact single-line JSON.
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if command -v jq >/dev/null 2>&1; then
  compact="$(printf '%s' "$payload" | jq -c .)"
else
  compact="$(printf '%s' "$payload" | tr -d '\n')"
fi

printf '%s %s\n' "$ts" "$compact" >> "$log"
exit 0
