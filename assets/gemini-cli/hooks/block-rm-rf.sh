#!/usr/bin/env bash
#
# BeforeTool hook for Gemini CLI — blocks destructive rm commands.
#
# Install:
#   cp block-rm-rf.sh ~/.gemini/hooks/
#   chmod +x ~/.gemini/hooks/block-rm-rf.sh
#
# Register in ~/.gemini/settings.json:
#   {
#     "hooks": {
#       "BeforeTool": [{
#         "matcher": "run_shell_command",
#         "hooks": [{
#           "name": "block-rm-rf",
#           "type": "command",
#           "command": "${GEMINI_PROJECT_DIR}/.gemini/hooks/block-rm-rf.sh",
#           "timeout": 5000
#         }]
#       }]
#     }
#   }
#
# Test:
#   echo '{"tool_args":{"command":"rm -rf /tmp/x"}}' | ./block-rm-rf.sh
#   # Expect: {"decision":"deny", ...}
#
#   echo '{"tool_args":{"command":"ls -la"}}' | ./block-rm-rf.sh
#   # Expect: no output, exit 0

set -euo pipefail

payload="$(cat)"

if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$payload" | jq -r '.tool_args.command // .tool_input.command // ""')"
else
  cmd="$(printf '%s' "$payload" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]*)"/\1/')"
fi

if printf '%s' "$cmd" | grep -Eiq '(rm[[:space:]]+([^#]*-[a-z]*r[a-z]*f|[^#]*-[a-z]*f[a-z]*r|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive)|rm[[:space:]]+-rf?[[:space:]]+/(\s|$|\*))'; then
  cat <<EOF
{"decision":"deny","reason":"Destructive rm command blocked by hook: ${cmd}"}
EOF
  exit 0
fi

exit 0
