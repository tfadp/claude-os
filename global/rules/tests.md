---
globs: ["**/test_*.py", "**/*_test.py", "**/tests/**", "**/*.test.*", "**/*.spec.*"]
---
# Test Rules

## TDD Protocol (enforced here)
- Write the failing test FIRST. Run it. Confirm RED before writing any implementation.
- Write minimum code to pass. Confirm GREEN.
- Refactor only after GREEN. Confirm still GREEN.
- "I'll add tests later" is not acceptable — no test = not done.

## Test Quality
- One assertion focus per test — test one behavior, not multiple
- Test names must describe the scenario: `test_login_fails_with_wrong_password` not `test_login`
- No `time.sleep()` in tests — use mocks or fixtures for async/timing
- Never assert on implementation details — assert on observable behavior

## Coverage
- Every function that handles user input or external data needs at least one sad-path test
- Every bug fix needs a regression test added before the fix is written
