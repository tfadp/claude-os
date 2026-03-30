---
name: genesis
description: Bootstrap a brand-new project with the full Claude OS sidecar
---
Project name: $ARGUMENTS

We are starting a brand-new project. I am a beginner. You are my "Patient Mentor" and you will teach as we build.

GOAL: Install the repo sidecar "Claude Operating System" that prevents drift, keeps a Source of Truth, and makes changes testable.

**STEP 1 — CREATE THE SIDECAR DIRECTORY**
Create the `.claude/` folder at the repo root with these files:

1) `.claude/CLAUDE.md` — The Brain (lean project facts only, 20-40 lines)
```
# [Project Name]
[One sentence: what this project does]

## Tech Stack
[language/framework, database, key libraries]

## Commands
[command]    # [what it does]

## Key Files
[path/to/file]    — [what it does]

## Project Rules
- Check .claude/SPECS.md only when modifying naming, schemas, or contracts.
  Do NOT load SPECS.md at session start.
- [any project-specific rules not in global config]
```
# exceptions.md — Proactive Catches

## Format
- [DATE] | [FILE] | [WHAT WAS CAUGHT] | [RESOLUTION]

## Log
-
2) `.claude/SPECS.md` — Source of Truth
```
# SPECS.md — Source of Truth (Contracts + Decisions)

## A) Naming Conventions (LOCKED)
- Variables: snake_case
- Functions: snake_case
- Classes: PascalCase
- Files: lowercase-with-dashes OR snake_case (choose ONE and enforce)
- Folders: lowercase
RULE: Do not change unless you follow Change Control in CLAUDE.md.

## B) Data Shapes / Schemas (LOCKED)
(Empty at start. Fill in once we define objects.)
RULE: Any schema change requires before/after + impact + tests.

## C) Invariants (LOCKED)
(Examples: IDs are strings; timestamps are ISO 8601; etc.)
RULE: Add invariants early and treat them like law.

## D) Domain Rules (LOCKED)
(Empty at start. Add business logic rules here — things that govern
app behavior but aren't schemas or naming conventions.)
Examples: currency display, formatting rules, API rate limits, etc.
RULE: Treat like invariants. Do not change without Change Control.

## E) Decisions Log (editable)
- [DATE]: Project initialized; Claude OS installed.
```

3) `.claude/tasks/todo.md` — Roadmap
```
# todo.md — Roadmap

## Session State
- branch: (current git branch)
- last_test: (pass/fail + command)
- blocked: (any blockers)
- pending_decisions: (any open questions)

## Next 3 Steps
1)
2)
3)

## Backlog
-
```

4) `.claude/tasks/lessons.md` — What We Learned
```
# lessons.md — What We Learned
-
```

5) `.claude/tasks/exceptions.md` — Proactive Catches
```
# exceptions.md — Proactive Catches

## Format
- [DATE] | [FILE] | [WHAT WAS CAUGHT] | [RESOLUTION]

## Log
-
```

**STEP 2 — PROJECT GENESIS**
1. Ask me what we are building today.
2. Recommend the simplest stack/tools for a beginner for that goal.
3. Propose a professional folder structure and create a "Hello World" or minimal runnable entrypoint.
4. Add a minimal test or smoke test command (even if basic).
5. Update `.claude/SPECS.md` with chosen stack + any initial data shapes once defined.
6. Update `.claude/tasks/todo.md` with the next 3 concrete steps.
7. Update SPECS.md Domain Rules with any business logic we discuss.

Before presenting Path A vs Path B, jot 3–5 rough notes on:
- key constraints or unknowns for this project
- the biggest risk in each path
- any assumptions you're making about the stack or scope
Keep each note under 5 words. Then present the paths.

**IMPORTANT**: Do not write any code until after you present Path A vs Path B for Genesis.

If a project name was provided in `$ARGUMENTS`, use it to pre-fill the `.claude/CLAUDE.md` header and ask "What are we building with [name]?" instead of the generic question.

Start now by creating the sidecar files, then ask: "What are we building today?"
