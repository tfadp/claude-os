---
name: audit
description: Activate Strict Auditor mode — full checklist review of the codebase
---

REVIEW_MODE=ON

You are now a **Strict Auditor**. Run through this checklist against the entire codebase:

- [ ] **Naming consistency**: All names match `.claude/SPECS.md` conventions
- [ ] **Contracts respected**: Data shapes and schemas match SPECS
- [ ] **Invariants honored**: IDs, timestamps, types all follow declared rules
- [ ] **Error handling**: Every function that can fail has proper error handling
- [ ] **Edge cases**: Empty inputs, nulls, boundary values are handled
- [ ] **Tests exist**: Every public function has at least one test
- [ ] **Verification commands**: Every feature has a terminal command to prove it works
- [ ] **No "lazy logic"**: No TODOs, no placeholder code, no shortcuts
- [ ] **Comments**: WHY-comments and docstrings on public functions
- [ ] **Docs current**: README and SPECS reflect actual behavior

Report findings as a numbered list with severity. Do not fix anything — just report.
