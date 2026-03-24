---
globs: ["**/*.sql", "**/*_query.py", "**/queries/**", "**/migrations/**"]
---
# SQL Rules

## Safety
- Never use string concatenation to build queries — always use parameterized queries
- Every DELETE or UPDATE must have a WHERE clause — no unbounded mutations
- Before running a migration: check for a rollback path

## Style
- Keywords in UPPERCASE: SELECT, FROM, WHERE, JOIN, etc.
- One clause per line for readability in multi-condition queries
- Table aliases should be meaningful (not single letters like `a`, `b`)

## Schema changes
- Every schema change requires: before state, after state, impact assessment, and a migration test
- Document schema changes in `.claude/SPECS.md` under "Data Shapes / Schemas"
