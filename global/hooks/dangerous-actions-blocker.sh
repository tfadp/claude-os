#!/usr/bin/env bash
# Blocks irreversible or destructive shell commands before execution.
# Called by Claude Code PreToolUse hook for Bash tool.

INPUT="$1"

# Patterns to block
BLOCKED_PATTERNS=(
  "rm -rf /"
  "rm -rf ~"
  "rm -rf \$HOME"
  "dd if="
  "mkfs"
  ":(){:|:&};:"
  "chmod -R 777 /"
  "chown -R"
  "git push --force"
  "git push -f"
  "git reset --hard HEAD~"
  "git clean -fd"
  "DROP TABLE"
  "DROP DATABASE"
  "TRUNCATE TABLE"
  "format c:"
  "> /dev/sda"
  "shred"
  "wipefs"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if echo "$INPUT" | grep -qi "$pattern"; then
    echo "BLOCKED: Dangerous command detected matching pattern: $pattern"
    echo "If this is intentional, confirm with the user before proceeding."
    exit 2
  fi
done

exit 0
