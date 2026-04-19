#!/usr/bin/env bash
#
# PreToolUse hook for Claude Code — blocks destructive rm commands.
#
# Install:
#   cp block-rm-rf.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/block-rm-rf.sh
#
# Register in ~/.claude/settings.json:
#   {
#     "hooks": {
#       "PreToolUse": [{
#         "matcher": "Bash",
#         "hooks": [{
#           "type": "command",
#           "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm-rf.sh",
#           "timeout": 5000
#         }]
#       }]
#     }
#   }
#
# Test:
#   echo '{"tool_input":{"command":"rm -rf /tmp/x"}}' | ./block-rm-rf.sh
#   # Expect: JSON with permissionDecision: "deny"
#
#   echo '{"tool_input":{"command":"ls -la"}}' | ./block-rm-rf.sh
#   # Expect: no output, exit 0

set -euo pipefail

payload="$(cat)"

if command -v jq >/dev/null 2>&1; then
  cmd="$(printf '%s' "$payload" | jq -r '.tool_input.command // ""')"
else
  # Fallback: crude grep if jq is unavailable. Not robust for quoted commands.
  cmd="$(printf '%s' "$payload" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*"command"[[:space:]]*:[[:space:]]*"([^"]*)"/\1/')"
fi

# Match:
#   rm -rf, rm -fr, rm -Rf, rm --recursive --force, rm with -r + -f as separate flags
#   rm -rf / or rm -rf /* (extra dangerous)
if printf '%s' "$cmd" | grep -Eiq '(rm[[:space:]]+([^#]*-[a-z]*r[a-z]*f|[^#]*-[a-z]*f[a-z]*r|--recursive[[:space:]]+--force|--force[[:space:]]+--recursive)|rm[[:space:]]+-rf?[[:space:]]+/(\s|$|\*))'; then
  cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Destructive rm command blocked by hook: ${cmd}"
  }
}
EOF
  exit 0
fi

exit 0
