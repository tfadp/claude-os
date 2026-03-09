# /qa — Quality Assurance Pass

You are now in QA Mode. Work autonomously through all four phases below.
Do not stop to ask questions unless you hit a blocker that cannot be resolved without my input.
Report findings as you go. When all four phases are complete, give me a summary report.

---

## Phase 1 — Test Suite
Run the full test suite using the test command in CLAUDE.md.
- If all tests pass: note it and move to Phase 2.
- If any tests fail: fix each failure before moving on.
  - Show the error, your diagnosis, and the fix as a before/after diff.
  - Re-run the suite after each fix to confirm it passes.
- Do not move to Phase 2 until the test suite is fully green.

## Phase 2 — Lint
Run the lint command from CLAUDE.md.
- Fix all errors. Warnings are noted but do n
cat > ~/claude-os/global/commands/qa.md << 'EOF'
# /qa — Quality Assurance Pass

You are now in QA Mode. Work autonomously through all four phases below.
Do not stop to ask questions unless you hit a blocker that cannot be resolved without my input.
Report findings as you go. When all four phases are complete, give me a summary report.

---

## Phase 1 — Test Suite
Run the full test suite using the test command in CLAUDE.md.
- If all tests pass: note it and move to Phase 2.
- If any tests fail: fix each failure before moving on.
  - Show the error, your diagnosis, and the fix as a before/after diff.
  - Re-run the suite after each fix to confirm it passes.
- Do not move to Phase 2 until the test suite is fully green.

## Phase 2 — Lint
Run the lint command from CLAUDE.md.
- Fix all errors. Warnings are noted but do not block progress.
- Show a summary of what was fixed.
- Re-run lint to confirm clean.

## Phase 3 — Performance Bottlenecks
Analyze the codebase and identify the top 3 performance bottlenecks.
For each one:
- Where it is (file + function)
- What the problem is
- Estimated impact (high / medium / low)
- Path A (quick fix) and Path B (proper fix)

Do not implement fixes yet. Present the findings and wait for my direction.

## Phase 4 — QA Report
Produce a summary with:
- Test suite: pass/fail count, list of fixes made
- Lint: errors fixed, warnings noted
- Top 3 bottlenecks with your Path A/B for each
- Any spec violations or naming drift caught during the pass
- Log all exceptions found to tasks/exceptions.md

Score the overall codebase health 1–10 and explain the score.
