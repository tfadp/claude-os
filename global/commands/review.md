---
name: review
description: Critical review of recent code changes — runs tests first, then audits
---
For each task completed in this session, score it 1-10 on:
- Spec alignment
- Edge case coverage
- Naming consistency
Any dimension below 8: flag it and resolve before we close the session.
First, run the project's test suite (if one exists). Report the results.

Then review the code written or changed in the last 24 hours (use `git log --since="24 hours ago" --oneline` and `git diff HEAD~5` or similar to identify recent changes). Be critical.

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
