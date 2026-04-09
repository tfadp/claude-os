# Claude Managed Agents — Assessment for Claude OS

> **TL;DR:** Managed Agents is the right choice for autonomous, async, and CI/CD workloads.
> It is **not** a replacement for interactive Claude Code sessions — those stay as-is.
> The `/review`, `/qa`, and PR-feedback loops are the highest-value entry points.

---

## What Managed Agents Is

Anthropic runs the agent loop. You supply the config; they provision the container,
handle context compaction, run the tools, and stream events back to your app.

```
Your App
  │
  ├── POST /v1/agents      ← create once, store the ID
  │
  └── POST /v1/sessions    ← every run
          │
          ├── agent config (model, system, tools, skills)
          └── container (bash, file ops, code execution)
                  │
                  └── resources: GitHub repo, uploaded files
```

Two mandatory steps: **agent first, session every run.** The agent is a versioned,
persistent config object — never call `agents.create()` on every run.

---

## How Claude OS Maps to This

| Claude OS concept        | Managed Agents equivalent                        |
|--------------------------|--------------------------------------------------|
| `agents/builder.md`      | `POST /v1/agents` with system + toolset config   |
| `agents/reviewer.md`     | Same, with write tools disabled                  |
| `global/rules/*.md`      | Skills — loaded on demand, not in the system prompt |
| `/qa` slash command      | Managed Agent session triggered by script        |
| `/review` slash command  | Managed Agent session with GitHub repo mounted   |
| `hooks/dangerous-actions-blocker.sh` | Permission policies (`always_ask`) |
| `git worktree` per task  | Per-session container (stronger isolation)       |
| File-based session state | `/mnt/session/outputs/` + Files API              |

---

## Where Managed Agents Fits Well

### 1. Autonomous QA and Review Runs

`/qa` already asks Claude to "work autonomously through all four phases."
That is exactly what a Managed Agent session is for:

- Mount the project repo via `github_repository` resource
- Agent runs bash, reads files, executes tests — all inside a clean container
- Stream events to your terminal or a Slack webhook
- Download the QA report at the end via the Files API

No human needs to watch. No context accumulation from previous work. Reproducible.

### 2. CI/CD Integration — PR Review Bot

The `reviewer` agent is a perfect fit for a GitHub-triggered review bot:

```
GitHub PR opened
    → webhook → your script → sessions.create()
    → agent reads diff, runs tests, applies reviewer.md rubric
    → streams findings → post as PR comment
    → session archived
```

This is something Claude Code cannot do today (it needs a human at the keyboard).
Managed Agents handles the infrastructure; your app just handles the event and
reads the output.

See `examples/pr-review-bot.py` for a working implementation.

### 3. Versioned Agent Configs

Currently `agents/builder.md`, `reviewer.md`, and `reader.md` are unversioned
markdown files. A typo in production is silent.

As Managed Agent configs:
- Every `agents.update()` creates an immutable version number
- Sessions pin to a version: `{type: "agent", id: agent_id, version: 42}`
- Roll back safely: existing sessions keep their pinned version
- A/B test prompts: run version 41 and 42 in parallel on the same input

### 4. Long-Running Tasks That Would Exhaust Context

A full `/qa` pass on a large codebase can accumulate thousands of tokens of
tool output. Managed Agent sessions have built-in context compaction — when the
session approaches its limit, Anthropic summarises earlier history automatically
and continues without losing important decisions.

Claude Code sessions do not have this; you hit the limit and restart.

### 5. Skills — Reusable Rules Without Prompt Bloat

Today `global/rules/python.md`, `shell.md`, `tests.md` are referenced manually
or loaded into every session. In Managed Agents, you package them as **Skills**:

- Stored server-side as versioned objects
- Loaded on-demand by the agent when the task is relevant
- No extra tokens in the system prompt for every session

This is the Managed Agents equivalent of Claude OS's lazy-load rule
("do not load SPECS.md at session start").

---

## Where Managed Agents Does NOT Fit

### Interactive Claude Code Sessions (the main use case)

You are typing. Claude responds. You refine. Container provisioning takes
10–30 seconds — unacceptable latency for interactive work.

**Keep using Claude Code + Claude OS for interactive development.**
Managed Agents is for the autonomous legs of your workflow.

### Per-Project `.claude/` Sidecars

The `.claude/CLAUDE.md`, `SPECS.md`, `tasks/todo.md` files are designed for
Claude Code's context loading. They still belong there.

For Managed Agent sessions, pass SPECS content via the system prompt or as a
file resource at session create time.

### Hooks-Based Security (Pre-Execution Shell Scripts)

`dangerous-actions-blocker.sh` intercepts every bash command before it runs.
In Managed Agents, the equivalent is **permission policies**:

```yaml
tools:
  - type: agent_toolset_20260401
    configs:
      - name: bash
        permission_policy:
          type: always_ask   # session goes idle; your app must confirm
```

This requires your app to handle `agent.tool_use` events with
`evaluated_permission: "ask"` and respond with `user.tool_confirmation`.
More work than a shell script, but also more auditable.

For autonomous sessions where you trust the agent's bash usage, `always_allow`
(the default) is fine. Apply `always_ask` only for sensitive operations like
`git push` or anything touching credentials.

---

## Recommended Adoption Roadmap

### Phase 1 — Start Here (low risk, high value)

1. Deploy the `reviewer` agent (see `agents/reviewer.yaml`)
2. Run `examples/pr-review-bot.py` manually on your next PR
3. Verify the output quality matches your `/review` command
4. Wire it to a GitHub webhook if you are happy

### Phase 2 — Async QA

1. Deploy the `qa-runner` agent (see `agents/qa-runner.yaml`)
2. Run `examples/async-qa.py` after your next feature branch is done
3. Compare the report to a manual `/qa` pass
4. Schedule it as a nightly cron once you trust it

### Phase 3 — Skills Migration

1. Publish `global/rules/python.md` as a Managed Agents Skill
2. Reference it in both the reviewer and qa-runner agent configs
3. Stop embedding rule text in system prompts; let the skill load it

### Phase 4 — CI/CD Automation

1. GitHub Actions trigger on PR open → call `pr-review-bot.py`
2. Post review as PR comment using `GITHUB_TOKEN`
3. Block merge if reviewer scores below 7/10 on spec alignment

---

## Architecture: Claude OS + Managed Agents (Combined)

```
Interactive Work (Claude Code)          Autonomous Work (Managed Agents)
────────────────────────────────        ─────────────────────────────────────
Human types → Claude Code               GitHub PR event → your webhook
  CLAUDE.md global rules loaded           sessions.create(agent=reviewer_id)
  /review, /qa slash commands              resources: [github_repository]
  hooks: secrets-scanner.sh              agent streams findings
  subagents: reader, builder              your app posts PR comment
  per-project .claude/ sidecar           session archived → Files API
```

They are complementary. Interactive for building; autonomous for auditing.

---

## Cost Considerations

Managed Agent sessions have container costs separate from token costs.
For a 5-minute QA run at current rates, container time is negligible vs
the token cost of a thorough review. The main cost driver is model tokens.

The reviewer agent is read-only (no writes, no deployments), so the cost
of an accidental session left running is low. Still: always `archive()`
sessions when done.

---

## Not Available on Third-Party Providers

Managed Agents is first-party Anthropic only — not on Bedrock, Vertex, or
Foundry. If you are proxying through any of those, stay with Claude API +
tool use for agent loops.
