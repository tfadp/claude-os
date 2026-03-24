---
name: morning
description: Start a new daily session — loads context and picks up where we left off
---

Start a new session. Please read `.claude/CLAUDE.md`, `SOUL.md`, `SPECS.md`, and the `tasks/` folder.

What changed in git since yesterday:
!`git log --since="yesterday" --oneline 2>/dev/null || echo "(no git repo or no overnight commits)"`

Current branch and status:
!`git status --short 2>/dev/null || echo "(no git repo)"`

---

Acknowledge our "Patient Mentor" workflow and tell me what our first "Cliffhanger" task is from yesterday's sync.

If there is no previous sync or cliffhanger, summarize the current state of the project and suggest what we should work on first.

Check tasks/exceptions.md for any unresolved flags from the previous session.
Report the current Session State from todo.md.
