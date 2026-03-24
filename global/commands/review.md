---
name: review
description: Critical review of recent code changes — runs tests first, then audits
---
Focus or time window (if specified): $ARGUMENTS

Current git log:
!`git log --since="24 hours ago" --oneline 2>/dev/null || echo "(no git repo or no recent commits)"`

Recent diff stat:
!`git diff HEAD~5 --stat 2>/dev/null || echo "(no diff available)"`

---

For each task completed in this session, score it 1-10 on:
- Spec alignment
- Edge case coverage
- Naming consistency
Any dimension below 8: flag it and resolve before we close the session.

First, run the project's test suite (if one exists). Report the results.

Then review the code shown in the git log and diff above. If `$ARGUMENTS` specifies a focus area or time window (e.g. "last 48 hours", "auth module"), use that to narrow or extend the scope. Be critical.

For each issue found, report:
- **File and line**: Where is the problem?
- **Severity**: 🔴 Critical / 🟡 Warning / 🔵 Suggestion
- **What's wrong**: Plain-language explanation
- **Fix**: What the corrected code or approach should look like

Also check for:
- Naming consistency against `.claude/SPECS.md`
- Contracts respected (data shapes, invariants)
- Error handling and edge cases
- Missing or broken tests
- "Lazy logic" shortcuts

End with a summary: total issues by severity, and your single biggest recommendation.
