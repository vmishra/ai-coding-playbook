#!/usr/bin/env bash
#
# AfterTool hook for Gemini CLI — appends every tool call to an audit log.
#
# Install:
#   cp audit-log.sh ~/.gemini/hooks/
#   chmod +x ~/.gemini/hooks/audit-log.sh
#
# Register in ~/.gemini/settings.json:
#   {
#     "hooks": {
#       "AfterTool": [{
#         "hooks": [{
#           "name": "audit-log",
#           "type": "command",
#           "command": "${GEMINI_PROJECT_DIR}/.gemini/hooks/audit-log.sh",
#           "timeout": 2000
#         }]
#       }]
#     }
#   }

set -uo pipefail

payload="$(cat)"
project_dir="${GEMINI_PROJECT_DIR:-${CLAUDE_PROJECT_DIR:-$PWD}}"
log="${project_dir}/.gemini/audit.log"

mkdir -p "$(dirname "$log")"

ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
if command -v jq >/dev/null 2>&1; then
  compact="$(printf '%s' "$payload" | jq -c .)"
else
  compact="$(printf '%s' "$payload" | tr -d '\n')"
fi

printf '%s %s\n' "$ts" "$compact" >> "$log"
exit 0
