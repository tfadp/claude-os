---
globs: ["**/*.sh", "**/*.bash", "**/Makefile", "**/Dockerfile*"]
---
# Shell / Infra Rules

## Safety
- Always quote variables: `"$VAR"` not `$VAR`
- Use `set -euo pipefail` at the top of every bash script
- Never `rm -rf` without first echoing what would be deleted
- Test scripts locally before deploying — never run untested shell on a production server

## Style
- Use `[[ ]]` not `[ ]` for conditionals in bash
- Functions should have a comment describing what they do and what they return
- Constants in UPPER_SNAKE_CASE

## Deployment
- SCP transfers: always verify the file exists on the remote after transfer
- After any script change that runs on the server: SSH in and confirm the process is using the new version
