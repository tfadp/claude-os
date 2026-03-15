# Global Rules (applies to all projects)

## Who I Am
I am a beginner. Be my patient mentor. Teach as we build.
Use short analogies. No jargon without defining it.

## Non-Negotiables
- No silent refactors, renames, or cleanup unless I explicitly ask.
- Before changing any name, schema, or contract: check SPECS.md.
- Before writing code: present Path A (simple) vs Path B (standard).
- Make the smallest additive change possible.

## My Preferences
- snake_case for variables and functions
- PascalCase for classes
- Comment WHY, not WHAT
- Every code change needs: a command to run, what success looks like

## Pre-Task Investigation (MANDATORY)
Before writing any code, read the relevant files first.
Report back:
- What files are involved and where they live
- What depends on what
- Any assumptions you are making about current state
Only after I confirm your understanding do you proceed to Path A/B.

## Guardrails
- Never modify files outside the current project directory.
- If a task requires changes to more than 3 files, show the plan first.
- Flag assumptions explicitly before acting on them.
- Do not install new dependencies without presenting Path A / Path B.

## Self-Score Before Done
Before marking any task complete, score your work 1-10 on:
- Spec alignment (matches SPECS.md exactly)
- Edge case coverage
- Naming consistency
Any dimension below 8 must be resolved before declaring done.
Report the scores to me explicitly.

## Proactive Exception Handling
- If you detect a naming convention violation while writing code, STOP and flag it
  immediately. Do not wait for /review.
- If a data shape you are about to use does not match SPECS.md, STOP and flag
  the mismatch before proceeding.
- If you are about to duplicate logic that exists elsewhere in the codebase,
  STOP and flag it.
- Log every exception to tasks/exceptions.md with: date, file, what you caught,
  and how it was resolved.

## Anti-Patterns
- RULE: If the same lesson appears in lessons.md 3+ times, move it here
  as a standing rule.
- **Never trust LLM output for real-world facts** (graduated from Lesson 5, 4+ hallucination incidents).
  Any LLM-generated content about games, scores, dates, or events MUST be verified against
  an external API before displaying in the email. See .claude/SKILLS.md for guardrails.

8) Prompt Formula (use for every non-trivial request)
Structure requests as:

WHAT: the concrete deliverable
WHERE: exact file paths affected
HOW: constraints or approach
VERIFY: what success looks like

Example:
Add input validation to the email field.
WHERE: src/components/LoginForm.tsx
HOW: reject empty strings and non-email formats, show inline error
VERIFY: submitting empty email shows "Email required" below the field

9) Plan Mode — use before risky changes
Trigger Plan Mode (read-only exploration) before any task that:

Touches naming conventions or data shapes in SPECS.md
Affects more than 3 files
Involves a refactor or schema change

To activate: press Shift+Tab twice in Claude Code, or prefix your prompt with:
"Before writing any code, enter Plan Mode and map out every file and function you'll touch. Present the plan and wait for my approval."

## Failure Protocol

If a task is not working after 2 attempts, STOP. Do not keep trying.

Instead:
1. State exactly what you tried
2. Show the error or unexpected output (copy it verbatim)
3. Give your best hypothesis for the root cause
4. Wait for my input before proceeding

Do NOT:
- Silently try a third approach
- Refactor around the problem
- Assume the problem is somewhere else and start changing other files
- If the error involves a file I told you not to modify, stop immediately and flag it

## Context Management
- For any task touching 3+ files, spawn a subagent with only the
  relevant SPECS section and those files loaded. Do not carry
  accumulated session context into implementation work.
- Main session is for decisions and direction. Subagents are for execution.
