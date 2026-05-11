# /trace — Harness-Level Failure Analysis

You are auditing the harness, not the code. Treat this session as evidence about
where the scaffolding failed, not where the implementation failed.

## Procedure

1. **Reconstruct the friction points.** Walk back through the session and list
   moments where:
   - You asked me to clarify something a rule should have made unambiguous
   - You took a wrong path and had to backtrack
   - A protocol fired late (e.g., Plan Mode triggered after code was already written)
   - A protocol didn't fire when it should have
   - Context filled with noise that a truncation or offload rule could have caught
   - You repeated work that memory should have surfaced
   - A tool was used that a sharper tool would have replaced
   - I corrected your behavior in a way a rule would have pre-empted

   For each: one-line description, the turn or approximate point it happened, and
   the proximate cause.

2. **Classify each friction point.** Tag with one of:
   - `[RULE-GAP]` — no rule covered this; one should
   - `[RULE-LATE]` — rule exists but fires too late in the protocol order
   - `[RULE-WEAK]` — rule exists but is too vague to act on
   - `[RULE-MISSING-TRIGGER]` — rule exists but nothing surfaces it at the right moment
   - `[TOOL-GAP]` — a tool or hook would have prevented this, no rule alone fixes it
   - `[MEMORY-GAP]` — durable knowledge that should be in `~/.claude/memory/` wasn't

3. **Propose harness changes.** For each friction point worth fixing, write:
   - The exact rule, hook, or memory entry to add/modify
   - Which file it goes in (`CLAUDE.md`, a specific memory file, a hook script, a command)
   - The historical failure trace (this session, this turn, this symptom) — so the
     rule's origin is documented per the "every rule traces to a failure" principle

4. **Apply the simplicity ceiling.** Before recommending, ask: would tightening an
   existing rule beat adding a new one? Prefer edits over additions. Flag any
   proposal that pushes the rule count up rather than the rule precision up.

5. **Output format.** A single markdown block I can paste into the relevant file,
   plus a one-line commit message in conventional format for the `tfadp/claude-os`
   sync.

## Anti-patterns to avoid

- Do not propose rules for things that happened once and are unlikely to recur.
  Friction must be plausibly recurring to earn a rule.
- Do not propose rules the current model handles natively. Cross-check against
  the `/trim` mindset: if a capable model wouldn't need this rule, don't add it.
- Do not critique the code in this command. That is `/review`'s job. If you find
  yourself describing what the code does wrong, stop — wrong command.
- Do not invent friction. If the session went smoothly, say so and exit. A clean
  `/trace` is a valid output.

## When to run

- At session end, before `/sync`, when something felt slower or rougher than it
  should have
- After a session where I corrected your behavior more than once
- After a `/review` that surfaced issues your protocols should have caught earlier
- Periodically, even on smooth sessions, to catch silent friction I didn't flag
