---
name: sync
description: End-of-session sync — saves state, lessons, and sets up tomorrow's cliffhanger
---
Current branch and uncommitted state:
!`git status --short 2>/dev/null || echo "(no git repo)"`

Recent commits this session:
!`git log --since="6 hours ago" --oneline 2>/dev/null || echo "(no recent commits)"`

---

## Why This Matters
Running /sync and ending the session is a token cost control measure. Leaving Claude Code 
idle for 5+ minutes causes the prompt cache to expire. When you return, the full conversation 
context is reprocessed from scratch at full price (~10x cost spike). Always /sync and close 
rather than leaving a session idle.

We are finishing this session. Please perform a "Session Sync" to preserve our state:

1. **Update tasks/todo.md**: Mark everything we finished today as complete. Move any "In Progress" items to the top of the "Active Tasks" list.

2. **Update tasks/lessons.md**: Reflect on today's work. If we hit any errors, bugs, or if you had to explain a complex concept to me, record that "Lesson" so we don't repeat the struggle later.

3. **Refine CLAUDE.md**: If I had to correct your behavior or remind you of a rule today, update the "Protocols" in CLAUDE.md to make those rules more clear for the future.

4. **The Cliffhanger**: Give me a 3-sentence summary of our progress and tell me exactly what the first step is for when I return.

5. **Update Session State**: Update the Session State block in tasks/todo.md: record current branch, last test result, any blockers, and pending decisions.

6. **Promote Anti-Patterns**: Check tasks/lessons.md. If any lesson has appeared 3+ times, move it to Anti-Patterns in the global CLAUDE.md and remove duplicates from lessons.md.

7. **Review Exceptions**: Review tasks/exceptions.md. Summarize any unresolved exceptions that need attention next session.

8. **GITHUB**: Confirm that everything is pushed to GitHub and let me know if there is anything else more for me to do.

Once the files are updated, give me a final confirmation of our current project status.
