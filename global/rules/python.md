---
globs: ["**/*.py"]
---
# Python Rules

## Style
- Always type hint function signatures — parameters and return type
- Use `pathlib.Path` not `os.path` for file operations
- Use f-strings not `.format()` or `%` formatting
- snake_case for all variables, functions, and modules

## Quality
- After any code change, run `ruff check` on the changed file before declaring done
- Never use bare `except:` — always catch a specific exception type
- Do not use `print()` for debugging — use `logging` or remove before commit
- Use list/dict comprehensions over map/filter for readability

## Dependencies
- Pin versions in requirements.txt or pyproject.toml — never use unpinned `package`
- Prefer stdlib over third-party for simple tasks (e.g. use `json` not `simplejson`)

## Deployment check (anti-pattern — graduated from lessons)
- After ANY code change: (1) run `ruff check` on changed files, (2) deploy to server, (3) verify server has the new code
- Git push is NOT deployment
