#!/usr/bin/env bash
# Scans command or file content for secrets before execution/write.
# Called by Claude Code PreToolUse hook for Bash and Write tools.

INPUT="$1"

# Patterns that indicate potential secrets
SECRET_PATTERNS=(
  "sk-[a-zA-Z0-9]{20,}"
  "AKIA[0-9A-Z]{16}"
  "ghp_[a-zA-Z0-9]{36}"
  "ghs_[a-zA-Z0-9]{36}"
  "github_pat_"
  "Bearer [a-zA-Z0-9._\-]{20,}"
  "password\s*=\s*['\"][^'\"]{6,}"
  "passwd\s*=\s*['\"][^'\"]{6,}"
  "secret\s*=\s*['\"][^'\"]{6,}"
  "api_key\s*=\s*['\"][^'\"]{6,}"
  "private_key"
  "-----BEGIN RSA PRIVATE KEY-----"
  "-----BEGIN OPENSSH PRIVATE KEY-----"
  "-----BEGIN EC PRIVATE KEY-----"
)

for pattern in "${SECRET_PATTERNS[@]}"; do
  if echo "$INPUT" | grep -qE "$pattern"; then
    echo "WARNING: Potential secret detected matching pattern: $pattern"
    echo "Review before proceeding. Ensure no credentials are being exposed."
    exit 2
  fi
done

exit 0
