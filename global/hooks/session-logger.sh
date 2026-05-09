#!/usr/bin/env bash
# Logs Claude Code session lifecycle events to ~/.claude/logs/sessions.log.
# Wired to SessionStart, SessionEnd, and PreCompact hooks via settings.json.
# Hook event name is passed as $1; remaining args are forwarded for context.

set -euo pipefail

EVENT="${1:-unknown}"
TS="$(date '+%Y-%m-%d %H:%M:%S')"
CWD="$(pwd)"
LOG_FILE="$HOME/.claude/logs/sessions.log"

mkdir -p "$(dirname "$LOG_FILE")"
printf '%s | %-13s | %s\n' "$TS" "$EVENT" "$CWD" >> "$LOG_FILE"

exit 0
