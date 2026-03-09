# Claude OS — The Human Guide

I consume every podcast, video, article, and tweet I can find about Claude Code. I have a
dedicated Claude project called "Make Claude Better" — every time I see something interesting,
I run it against my setup. A lot of the time it comes back: not useful, skip it. But sometimes
it's genuinely additive, and when it is, it goes into this system. Basically I use Claude to
make Claude better. I probably update this once a week as new ideas, models, and techniques
come out.

A lot of my progress has come from structures, guardrails, and formats — most of which are
about optimizing how AI writes and maintains code. This repo is the accumulated result of that
process. Not a grand design. An evolving operating system built one insight at a time.

If you're moving to Claude Code from another AI coding tool or from coding without AI assistance,
this is the setup I wish I'd had on day one.

---

## What This Repo Is

A global configuration layer that sits on top of Claude Code and makes it consistent, safe,
and predictable across every project. The files here are the rules, habits, and guardrails
that prevent Claude from making the mistakes it makes by default — renaming things you didn't
ask it to rename, declaring things done when they aren't, making assumptions instead of asking.

The key insight: **Claude Code is only as good as its instructions.** The model is remarkable,
but the scaffolding around it determines whether you get great output or frustrating output.
This repo is the scaffolding.

There are two levels of configuration in Claude Code:

- **Global** (~/.claude/CLAUDE.md) — rules that apply to every project, every session
- **Project-level** (.claude/CLAUDE.md inside each repo) — facts specific to that project

This repo stores and documents your global layer. Each project manages its own project-level files.
The distinction matters: **behavioral rules live globally, project facts live locally.**

---

## The File Structure

global/
├── CLAUDE.md        — Global rules loaded at the start of every session
├── settings.json    — Hooks and permissions (security layer)
└── commands/        — Slash commands (/morning, /sync, /review, /qa, /audit, /genesis, /post-review)

These mirror ~/.claude/ on your machine. This repo is the source of truth — ~/.claude/
is the deployed version. Edit here, copy there to apply.

---

## global/CLAUDE.md — The Brain

Claude reads this at the start of every session and follows it for the duration. Here's what's
in it and why each section exists:

**Non-Negotiables** — No silent refactors, no renaming, no "cleanup" you didn't ask for.
Claude has a habit of tidying things up in ways that break other things. This stops that.

**Path A / Path B** — Before writing any code, Claude presents two approaches: simple and robust.
Forces a planning step before execution and surfaces tradeoffs you might not have considered.

**Pre-Task Investigation** — Before coding, Claude reads the relevant files and reports back
what it found: what files are involved, what depends on what, what assumptions it's making.
You confirm its understanding before it starts. Eliminates Claude's most common mistake class:
building on a wrong mental model of what already exists.

**Change Control** — Anything touching naming conventions or data shapes requires a before/after
diff and an impact summary before Claude proceeds.

**Definition of Done** — Claude cannot say "done" unless the code runs, a test command was
executed, docs are updated if behavior changed, and SPECS are updated if any contract changed.

**Self-Score Before Done** — Before declaring anything complete, Claude scores itself 1-10 on
spec alignment, edge case coverage, and naming consistency. Any dimension below 8 gets flagged
before you see it.

**Context Management** — Claude's context window fills during long sessions. At 70% it starts
losing precision. Run /compact at 70%, /clear at 90%. Run /status to check where you are.

**Guardrails** — Claude cannot touch files outside the current project, cannot change more than
3 files without showing a plan first, cannot install dependencies without a Path A/B discussion.

**Proactive Exception Handling** — Claude flags naming violations, spec mismatches, and logic
duplication in real time as it writes. Everything it catches gets logged to tasks/exceptions.md.

**Anti-Patterns** — If the same lesson appears in lessons.md three or more times, it graduates
here as a permanent standing rule.

**Prompt Formula** — Structure for individual requests: WHAT (deliverable) → WHERE (file paths)
→ HOW (constraints/approach) → VERIFY (what success looks like).

**Plan Mode** — For risky tasks (more than 3 files, refactors, schema changes), Claude enters
read-only exploration before writing anything. Maps every file and function, presents the plan,
waits for approval.

---

## global/settings.json — The Security Layer

Two hooks that run automatically before Claude executes anything. Set once, forget about them.

**Dangerous Actions Blocker** — Watches every terminal command Claude tries to run. If it
matches patterns that could cause irreversible damage, it is blocked. Claude tells you to run
it manually if you actually intended it.

**Secrets Scanner** — Watches every command Claude runs and every file Claude writes. If it
detects API keys, passwords, or credentials, it blocks the action. Secrets live in .env files —
never in code, never in commits.

---

## global/commands/ — Slash Commands

Custom commands typed during a session, prefixed with /. Markdown files Claude reads and
executes as a prompt.

**/morning** — Start a new session. Claude reads the sidecar files and surfaces the first
task from yesterday's cliffhanger.

**/review** — Critical review of everything written in the session. Claude scores completed
tasks, flags issues, and proposes fixes via Path A/B.

**/post-review** — After reading review findings, picks the most important lesson, saves it
to lessons.md, and structures the first fix.

**/sync** — End of day. Marks completed tasks, updates session state, checks for lessons
ready to graduate to Anti-Patterns, writes the cliffhanger for tomorrow, confirms GitHub push.

**/qa** — Quality assurance pass. Runs autonomously through four phases: full test suite
(fixes any failures before moving on), lint (fixes all errors), performance analysis
(identifies top 3 bottlenecks with Path A/B for each), and a final QA report with an
overall codebase health score. Run before any major deploy or after a heavy coding session.

**/audit** — Weekly. Reviews the full codebase, surfaces structural issues, produces findings
to take to an external review session.

**/genesis** — New project setup. Creates the full .claude/ sidecar, asks what you are
building, walks through Path A/B for initial stack and structure.

---

## Per-Project Structure

Every project gets a .claude/ sidecar:

.claude/
├── CLAUDE.md          — Project facts only: stack, commands, key files (20-40 lines max)
├── SPECS.md           — Source of truth: naming conventions, schemas, invariants, domain rules
└── tasks/
    ├── todo.md        — Roadmap + session state (branch, last test result, blockers)
    ├── lessons.md     — What we learned
    └── exceptions.md  — Proactive catches log

**CLAUDE.md** is facts only. No behavioral rules — those live globally and inherit automatically.

**SPECS.md** is the contract layer. Naming conventions, data shapes, and domain rules (business
logic that governs behavior — things like "all currency displayed in USD" or "negative returns
use red"). Treat everything in SPECS like law. Change Control required to modify any of it.

---

## Setup — Start Here

### Step 1: Install your global config

cp global/CLAUDE.md ~/.claude/CLAUDE.md
cp global/settings.json ~/.claude/settings.json
cp -r global/commands/ ~/.claude/commands/

mkdir -p ~/.claude/hooks
cp global/hooks/dangerous-actions-blocker.sh ~/.claude/hooks/
cp global/hooks/secrets-scanner.sh ~/.claude/hooks/
chmod +x ~/.claude/hooks/dangerous-actions-blocker.sh
chmod +x ~/.claude/hooks/secrets-scanner.sh

### Step 2: New projects

Run /genesis at the start of any new project. It creates the full .claude/ sidecar,
asks what you are building, and walks you through the initial stack decision via Path A/B.
Do not write any code before running genesis on a new project.

### Step 3: Existing projects

For any existing project where you want to drop this system in, paste this into Claude Code:

I'm adding new structure to this project. Do NOT rewrite or remove anything that exists.
Only ADD what I specify. Show me a diff before making any changes.

1. Create .claude/CLAUDE.md with: project name, tech stack, key commands, key files.
2. Create .claude/SPECS.md with sections: Naming Conventions, Data Shapes, Invariants,
   Domain Rules, Decisions Log.
3. Create .claude/tasks/todo.md with a Session State block at the top
   (branch, last_test, blocked, pending_decisions) and a Next 3 Steps section.
4. Create .claude/tasks/lessons.md (empty).
5. Create .claude/tasks/exceptions.md (empty, with Format header).

After making changes, show me the updated files and confirm nothing existing was modified.

---

## The Routine

**Every morning:**
/morning
Claude reads the sidecar, tells you where you left off, and surfaces the first task.

**During the day:**
Work normally. Claude investigates before coding, presents Path A/B, flags exceptions in
real time, and self-scores before declaring anything done.

**End of session:**
/review → read findings → /post-review → /sync

**Before a major deploy or after a heavy coding session:**
/qa
Runs autonomously — tests, lint, performance bottlenecks, health score. Review the report
and decide which bottleneck fixes to action.

**Weekly:**
/audit
Take the findings to an external model (we use Codex) for a second-opinion review.
Bring Codex's suggestions back to Claude and work through them.

---

## Changelog

Every change to this system goes in changelog.md with a date and a one-line reason.
Six months from now you will look at a rule and wonder if it is still necessary.
The changelog tells you what problem it was solving.
