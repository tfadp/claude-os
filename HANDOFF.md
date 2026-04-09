# Session Handoff — Claude OS + Managed Agents Assessment

**Date:** 2026-04-09
**Branch:** `claude/assess-managed-agents-Q3LiY`
**Repo:** `tfadp/claude-os`
**Status:** Assessment complete, implementation artifacts pushed, PR not yet created.

---

## What This Repo Is

**Claude OS** is a global configuration layer for Claude Code (Anthropic's CLI). It is not a
standalone app — it is scaffolding: rules, agents, slash commands, security hooks, and memory
files that live in `~/.claude/` and apply to every project on your machine.

Key idea: instead of copy-pasting the same prompts and guardrails into every project, you encode
them once here and they apply everywhere.

```
global/
├── CLAUDE.md          ← global rules (non-negotiables, TDD, debugging protocol, etc.)
├── agents/            ← subagent definitions (reader, builder, reviewer)
├── commands/          ← slash commands (/review, /qa, /genesis, /morning, /sync, etc.)
├── hooks/             ← shell scripts that run before every bash/write (security)
├── rules/             ← language-specific rules (python, shell, sql, tests)
└── memory/            ← cross-project knowledge base (patterns, debugging, architecture)
```

The files in `global/` mirror to `~/.claude/` on your machine. That's how Claude Code picks
them up. See `GUIDE.md` for the full install walkthrough.

---

## What Happened This Session

### Trigger
You shared the Anthropic tweet announcing **Claude Managed Agents** (public beta) and asked
for an assessment of whether/how it fits Claude OS.

### What We Assessed
Managed Agents is a new Anthropic service where:
- You define an **Agent** config (model, system prompt, tools) once via `POST /v1/agents`
- Each run creates a **Session** — Anthropic provisions a container, runs the agent loop,
  streams events back to your app
- The agent can use bash, file ops, web search, GitHub repos, MCP servers — all server-side

### Core Finding
Managed Agents and Claude Code are complementary, not competing:

| Use case | Use this |
|---|---|
| Interactive coding session | Claude Code + Claude OS (as before) |
| Autonomous PR review bot | Managed Agents |
| Nightly QA run / CI pipeline | Managed Agents |
| Long task that could exhaust context | Managed Agents (has built-in compaction) |
| Anything needing a human in the loop | Claude Code + Claude OS (as before) |

The `/review` and `/qa` commands already ask Claude to "work autonomously" — Managed
Agents just does that with better infrastructure (versioned configs, container isolation,
event streaming) and without needing you at the keyboard.

---

## What Was Built This Session

All new files live in `global/managed-agents/` on branch `claude/assess-managed-agents-Q3LiY`.

### `global/managed-agents/ASSESSMENT.md`
Full fit/gap analysis. Covers:
- Where Managed Agents fits well (autonomous QA, PR review bot, versioned agent configs, Skills)
- Where it doesn't (interactive work, hooks-based security, per-project sidecars)
- Architecture diagram showing how the two systems work together
- 4-phase adoption roadmap (Phase 1: reviewer bot → Phase 4: full CI/CD automation)
- Cost considerations and third-party provider limitations (not available on Bedrock/Vertex)

### `global/managed-agents/agents/reviewer.yaml`
Anthropic CLI config for the **reviewer agent** — the Managed Agents equivalent of
`global/agents/reviewer.md`. Write tools disabled; bash enabled for running tests and
git diff. Deploy with:
```bash
ant beta agents create --file global/managed-agents/agents/reviewer.yaml
```

### `global/managed-agents/agents/qa-runner.yaml`
Anthropic CLI config for the **QA runner agent** — the Managed Agents equivalent of
the `/qa` slash command. Full toolset enabled; writes a health report to
`/mnt/session/outputs/qa-report.md` which you can download afterward. Deploy with:
```bash
ant beta agents create --file global/managed-agents/agents/qa-runner.yaml
```

### `global/managed-agents/examples/pr-review-bot.py`
Working Python script. Two modes:
1. **Direct call:** `python pr-review-bot.py owner/repo 42 feature-branch`
   Creates a session, mounts the PR branch, streams review to terminal, posts as PR comment.
2. **Webhook server:** `python pr-review-bot.py` — Flask app that handles GitHub PR events.

### `global/managed-agents/examples/async-qa.py`
Working Python script for async QA runs:
- `python async-qa.py --github owner/repo --branch main` (clean state, recommended)
- `python async-qa.py --local ./my-project` (uploads local files)
Downloads `qa-report.md` when done.

---

## Current Git State

```
branch:   claude/assess-managed-agents-Q3LiY
ahead of: main by 1 commit (dd4f3ad)
pushed:   yes — origin is up to date
PR:       not created yet
```

Commit message: `feat: assess Claude Managed Agents for Claude OS`

---

## What Still Needs to Be Done

### Immediate (to complete this work item)

1. **Open a PR** — branch is pushed, PR not yet created.
   Title: `feat: assess Managed Agents for Claude OS`
   Base: `main`

2. **Verify the Anthropic CLI syntax** — the YAML agent configs use
   `ant beta agents create --file <path>`. Confirm this is the correct CLI command
   (check `platform.claude.com/docs/en/api/sdks/cli.md`). If the flag is different,
   update the YAML file headers and the ASSESSMENT.md deploy instructions.

3. **Test the reviewer bot end-to-end** — needs:
   - `ANTHROPIC_API_KEY` with Managed Agents beta access
   - `CLAUDE_OS_REVIEWER_AGENT_ID` (from step 2 above)
   - `CLAUDE_OS_ENV_ID` (from `ant beta environments create`)
   - `GITHUB_TOKEN` with repo + PR comment permissions
   Run: `python global/managed-agents/examples/pr-review-bot.py owner/repo 1 main`

### Medium term (Phase 2 of the roadmap)

4. **Test async-qa.py** — same env vars plus `CLAUDE_OS_QA_AGENT_ID`.
   Try: `python global/managed-agents/examples/async-qa.py --github owner/repo --branch main`

5. **Skills migration** — package `global/rules/python.md`, `tests.md`, `shell.md` as
   Managed Agents Skills so they load on-demand rather than sitting in every system prompt.
   This requires the Skills API (`POST /v1/skills`).

### Longer term (Phase 3–4)

6. **GitHub Actions integration** — add a workflow file that calls `pr-review-bot.py`
   on PR open/synchronize events. The script already supports direct invocation.

7. **Permission policies** — the current YAML configs use `always_allow` for bash.
   Consider switching dangerous operations (git push, rm) to `always_ask` and handling
   the `user.tool_confirmation` event in the example scripts.

---

## How to Reconstruct This Context on a New Machine

```bash
# 1. Clone and switch to the feature branch
git clone https://github.com/tfadp/claude-os
cd claude-os
git checkout claude/assess-managed-agents-Q3LiY

# 2. Read the assessment
cat global/managed-agents/ASSESSMENT.md

# 3. Read this file
cat HANDOFF.md

# 4. The three key things to do next (in order):
#    a) Open the PR (branch is already pushed)
#    b) Verify CLI syntax for agent creation
#    c) Do a live end-to-end test of pr-review-bot.py
```

Tell Claude: *"Read HANDOFF.md and global/managed-agents/ASSESSMENT.md, then help me
complete the next steps."* That is enough context to resume without losing anything.

---

## Key Decisions Made (for future reference)

- **Managed Agents is an addition, not a replacement.** Interactive Claude Code sessions
  stay as-is. No changes to `global/CLAUDE.md`, slash commands, or hooks.
- **Python chosen for examples** because Claude OS has an existing Python project
  (the daily-email project referenced in CLAUDE.md anti-patterns). TypeScript versions
  would follow the same shape using `@anthropic-ai/sdk`.
- **reviewer.yaml disables write tools** to match the intent of `global/agents/reviewer.md`
  (strict code review, no modifications).
- **qa-runner.yaml writes the report to `/mnt/session/outputs/`** so it survives the session
  and can be downloaded via the Files API. This is the Managed Agents equivalent of
  Claude Code writing to `.claude/tasks/`.
- **Stream-first pattern** is used in both example scripts: stream opens before the kickoff
  message is sent, to avoid missing early events.
