# Slash Commands — Installation & Usage Guide

## What You've Got

| Command | What it does | Replaces |
|---------|-------------|----------|
| `/morning` | Loads all context, picks up yesterday's cliffhanger | Your morning copy-paste prompt |
| `/sync` | End-of-day state save: todos, lessons, CLAUDE.md refinement, GitHub push | Your evening copy-paste prompt |
| `/review` | Runs tests, then critically reviews last 24hrs of code | Your "/review" prompt |
| `/post-review` | Logs findings to todo, saves lesson, presents Path A vs B for fixes | Your "I've read your review" prompt |
| `/genesis` | Full new-project bootstrap with Claude OS sidecar | Your "starting a brand-new project" prompt |
| `/audit` | Strict Auditor mode — full checklist, no fixes, just findings | Your `REVIEW_MODE=ON` trigger |

---

## How to Install

### Option A: Per-Project (recommended — gets committed to Git so your setup travels with the repo)

```bash
# From your project root:
mkdir -p .claude/commands

# Copy all command files into the project:
cp /path/to/these/commands/*.md .claude/commands/

# Commit them:
git add .claude/commands/
git commit -m "Add Claude slash commands for workflow automation"
git push
```

### Option B: Global (available in every project, but not shared via Git)

```bash
# Create the global commands directory:
mkdir -p ~/.claude/commands

# Copy all command files:
cp /path/to/these/commands/*.md ~/.claude/commands/
```

**Which to choose?** Put them in the project (Option A) so they're version-controlled and always travel with your repo. If you want them available even outside any project, do both.

---

## How to Use

In Claude Code, just type the slash and the name:

```
/morning          → starts your day
/review           → end-of-day code review
/post-review      → after reading the review, plan fixes
/sync             → end-of-day session save
/audit            → weekly deep audit
/genesis          → new project from scratch
```

Type `/help` to see all available commands including these.

---

## How to Add to Existing Projects

For any project that already has your `.claude/` sidecar set up:

```bash
cd your-project
mkdir -p .claude/commands
cp ~/your-commands-source/*.md .claude/commands/
git add .claude/commands/
git commit -m "Add slash commands"
```

Your existing `CLAUDE.md`, `SOUL.md`, `SPECS.md`, and `tasks/` folder stay untouched.

---

## How to Keep Them Updated

When you improve a command (say you tweak `/review` to also check for accessibility issues), you need to propagate it to your other projects. Two approaches:

### Manual (simple, fine for a few projects)
Edit the command in one project, then copy the updated `.md` file to your other projects and commit.

### Script (better if you have 3+ projects)

Create a small sync script. Save this as `~/sync-claude-commands.sh`:

```bash
#!/bin/bash
# Update slash commands across all your projects
SOURCE=~/.claude/commands  # keep your "master" copies here

PROJECTS=(
  ~/code/project-one
  ~/code/project-two
  ~/code/project-three
)

for proj in "${PROJECTS[@]}"; do
  if [ -d "$proj/.claude" ]; then
    mkdir -p "$proj/.claude/commands"
    cp "$SOURCE"/*.md "$proj/.claude/commands/"
    echo "✅ Updated: $proj"
  else
    echo "⚠️  No .claude/ found in $proj — skipping"
  fi
done
```

```bash
chmod +x ~/sync-claude-commands.sh
```

Run it whenever you update a command. Commit the changes in each project afterward.

---

## Your Daily Workflow (Now Simplified)

**Morning:**
```
/morning
```

**During the day:** Build stuff with Claude as usual.

**Before wrapping up:**
```
/review
```
Read the findings, then:
```
/post-review
```
Choose Path A or B, fix things.

**End of day:**
```
/sync
```

**Once or twice a week:**
```
/audit
```
Then take findings to Codex for a second opinion.

**New project:**
```
/genesis
```
