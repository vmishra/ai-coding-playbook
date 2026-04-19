#!/usr/bin/env bash
#
# PostToolUse hook for Claude Code — runs the project's formatter after edits.
# Fail-open by design: if the formatter isn't installed, the edit still succeeds.
#
# Install:
#   cp format-after-edit.sh ~/.claude/hooks/
#   chmod +x ~/.claude/hooks/format-after-edit.sh
#
# Register in ~/.claude/settings.json:
#   {
#     "hooks": {
#       "PostToolUse": [{
#         "matcher": "Edit|Write",
#         "hooks": [{
#           "type": "command",
#           "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/format-after-edit.sh",
#           "timeout": 30000
#         }]
#       }]
#     }
#   }

set -uo pipefail

payload="$(cat)"

if command -v jq >/dev/null 2>&1; then
  path="$(printf '%s' "$payload" | jq -r '.tool_input.file_path // .tool_input.path // ""')"
else
  path="$(printf '%s' "$payload" | grep -oE '"(file_path|path)"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | sed -E 's/.*"(file_path|path)"[[:space:]]*:[[:space:]]*"([^"]*)"/\2/')"
fi

[[ -z "$path" ]] && exit 0
[[ ! -f "$path" ]] && exit 0

case "$path" in
  *.js|*.jsx|*.ts|*.tsx|*.json|*.md|*.yml|*.yaml|*.css|*.scss)
    command -v prettier >/dev/null 2>&1 && prettier --write "$path" >/dev/null 2>&1 || true
    ;;
  *.go)
    command -v gofmt >/dev/null 2>&1 && gofmt -w "$path" >/dev/null 2>&1 || true
    ;;
  *.py)
    command -v ruff >/dev/null 2>&1 && ruff format --quiet "$path" >/dev/null 2>&1 \
      || (command -v black >/dev/null 2>&1 && black --quiet "$path" >/dev/null 2>&1) \
      || true
    ;;
  *.rs)
    command -v rustfmt >/dev/null 2>&1 && rustfmt "$path" >/dev/null 2>&1 || true
    ;;
  *.java)
    command -v google-java-format >/dev/null 2>&1 && google-java-format -i "$path" >/dev/null 2>&1 || true
    ;;
esac

exit 0
