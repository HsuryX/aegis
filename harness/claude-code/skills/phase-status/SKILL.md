---
name: phase-status
description: Use at session start, after phase transitions, or when uncertain about the current governance state
---

# /phase-status

Displays a one-screen overview of the project's current governance state, read from `.agent-state/phase.md`, `decisions.md`, and `gaps.md`. Enforces the Session Start Protocol requirement to verify state integrity before acting.

## What it displays

1. **Current phase** and gate status (from `phase.md` phase table)
2. **Terminal phase** (if set — e.g., spec-only projects)
3. **Scope classification** (micro / small / standard / large from `audit.md`)
4. **Handoff context** (in-progress work, blockers, next step)
5. **Open decisions** — count and list of titles
6. **Critical gaps** — count and list (blocks phase advancement per the `critical` severity rule)
7. **Non-critical gaps** — count only
8. **Active deviations** — list with expiry conditions; flags any that have outlived their expiry

## Integrity checks

The skill MUST verify all six sub-checks from the Session Start Protocol in `AGENTS.md` step 3 ("Verify state integrity"):

1. `phase.md` exists and is parseable — if not, report Phase 0 with no prior progress
2. Phase N marked `completed` has supporting evidence in the relevant state files (e.g., Phase 1 completed requires all Required Decisions to be in `Accepted` or `Final` state in `decisions.md`, with the count matching the scope classification)
3. If a state file contains only its template with no entries, the project is treated as if that phase's work has not begun — regardless of what `phase.md` claims
4. State files are mutually consistent — contradictions are reported as NEEDS_CONTEXT per the Completion Status Protocol in `playbooks/principles.md`
5. Archive files (`decisions-archive.md`, `gaps-archive.md`, `phase-archive.md`) are read when they exist — contradictions between archive and active entries are surfaced to the user before proceeding (see `playbooks/principles.md` Required Behaviors #8 "Archive consultation")
6. SYNC-IMPACT HTML comments at the top of `AGENTS.md` and each `playbooks/*.md` file are checked — if any comment's `date` is after the agent's last-read date and its `downstream_review_required` list includes a file not yet re-read, the agent MUST re-read that file before proceeding (see `playbooks/principles.md` Sync Impact Reports)
7. No deviation in `gaps.md` has outlived its expiry condition — expired deviations MUST be flagged to the user for re-evaluation

## When to invoke

- At the start of every session, before any other work (Session Start Protocol step 1 delegates here)
- After updating phase status (e.g., advancing a phase gate)
- Any time the agent is uncertain about current phase or gate status
- Before creating new decisions or gaps (to confirm the current phase allows them)
- Before ending a session (as a final check that the Handoff Context is up to date)

## Output format

A concise table plus a handoff summary — designed to fit in one screen without scrolling. No verbose prose. The agent SHOULD paste the output into the session log when reporting status to the user.

## Example output

```
Phase: 3-implement (in progress; gate not met)
Terminal: 3-implement
Scope: standard
Decisions: 3 Final, 1 Accepted, 0 active
Critical gaps: 0
Non-critical gaps: 1 (deviation, expires at Phase 2 close)
Deviations past expiry: 0
Handoff: feature slice X in progress — second subsystem
Next: feature slice Y — integration tests
```
