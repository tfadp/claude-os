---
name: trim
description: Audit CLAUDE.md and memory files — flags rules and entries that have gone stale or redundant
---

Current global CLAUDE.md:
!`cat ~/.claude/CLAUDE.md 2>/dev/null || echo "(not found)"`

Current memory files:
!`cat ~/.claude/memory/preferences.md 2>/dev/null || echo "(not found)"`
!`cat ~/.claude/memory/patterns.md 2>/dev/null || echo "(not found)"`
!`cat ~/.claude/memory/debugging.md 2>/dev/null || echo "(not found)"`

Project CLAUDE.md (if present):
!`cat .claude/CLAUDE.md 2>/dev/null || echo "(no project-level CLAUDE.md)"`

---

Run a trim audit on the files above. For each rule, preference, pattern, or log entry, apply these 5 diagnostic questions:

1. **Still true?** Is this rule still accurate given the current codebase and tools?
2. **Still relevant?** Does this project still do the thing this rule protects against?
3. **Duplicate?** Does another rule or entry already cover this?
4. **Overconstrained?** Does this rule block reasonable behavior more often than it prevents real mistakes?
5. **Graduated?** Was this a temporary lesson that is now obvious and no longer needs to be stated?
6. **Tool/MCP audit**: List every MCP server and tool registered in `settings.json`.
   For each one: when was it last used this week? If it hasn't been used in 7+ days,
   flag it for removal with: `[TRIM CANDIDATE - tool: {name}]`

For each candidate, output:
- **Rule/entry** (quote it exactly)
- **File and line** where it lives
- **Diagnosis**: which question it failed and why
- **Recommendation**: DELETE / MERGE WITH [other rule] / REWRITE TO [shorter version]

Do NOT make any changes. Return the list of candidates only. I will decide what to cut.

End with a count: X rules reviewed, Y flagged for removal, Z flagged for rewrite.
