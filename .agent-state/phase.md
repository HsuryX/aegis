<!-- SCHEMA:
file_type: state
top_level_fields:
  - "Current phase: 0-audit | 1-design | 2-spec | 3-implement"
  - "Terminal phase: 0-audit | 1-design | 2-spec | 3-implement"
  - "Lifecycle mode: finite-delivery | steady-state"
  - "Last updated: YYYY-MM-DD"
  - "Scope classification: micro | small | standard | large"
  - "Project type: {free-form}"
phase_table_format: |
  | Phase | Status | Gate Met | Date Entered |
  |-------|--------|----------|--------------|
  | N. Name | not-started | in-progress | completed | not-applicable | yes (YYYY-MM-DD) | no | N/A | YYYY-MM-DD |
sections:
  - "Integrity Invariants"
  - "Handoff Context"
  - "Feature Slices (if applicable)"
  - "Session Log"
handoff_blocks:
  - "**Exit audit (from prior agent):** {populated by the exiting agent per playbooks/principles-conditional.md Multi-Agent Handoff Protocol — phase state summary, open items, known risks, evidence pointer. Single-agent projects may record 'single-agent continuation' here.}"
  - "**In progress:** {current session state — update before ending a session}"
  - "**Entry acknowledgment (by receiving agent):** {populated when a session picks up another agent's work — re-read confirmation, discrepancies found, accepted scope. Single-agent projects may record 'same agent, continuous session' here.}"
  - "**Previous context ({label}, historical):** {demoted prior In progress blocks}"
  - "**Next:** {next session pointer with full plan}"
session_log_format: |
  | Date | Phase | Duration | Work Done | Decisions Made | Gaps Found | Lessons Learned |
  | YYYY-MM-DD | {phase-slug} | {N sessions} | {summary} | {D-{n} list or "(none)"} | {G-{n} list or "(none)"} | {lessons or "(none new)"} |
reference: AGENTS.md Session Start Protocol + playbooks/principles-conditional.md Multi-Agent Handoff Protocol
-->

# Phase Status

**Current phase:** 0-audit
**Terminal phase:** 3-implement
**Lifecycle mode:** steady-state
**Last updated:** 2026-04-25
**Scope classification:** standard
**Project type:** governance framework

| Phase | Status | Gate Met | Date Entered |
|-------|--------|----------|--------------|
| 0. Audit | in-progress | no | 2026-04-25 |
| 1. Design | not-started | no | |
| 2. Spec | not-started | no | |
| 3. Implement | not-started | no | |

## Integrity Invariants

- (none yet — first session should record the initial integrity check in Handoff Context.)

## Handoff Context

Update before ending a session — this is the primary handoff mechanism between sessions or collaborators.

**Exit audit (from prior agent):** (none — clean framework state)

**In progress:** *(Clean framework template state. The Handoff Context is intentionally empty — no project session has been recorded. The first real session in a downstream adoption MUST replace this paragraph with an Integrity check block citing verifiable counts and the `validate.py` exit code per `AGENTS.md` Session Start Protocol Step 3.)*

**Entry acknowledgment (by receiving agent):** (none — clean framework state)

**Next:** start Phase 0 surface audit or classify the next material work item.

## Feature Slices (if applicable)

(Applies only when Phase 1 invokes the Decomposition Rule in `playbooks/01-design.md`. For monolithic projects, leave this section as the placeholder.)

## Session Log

| Date | Phase | Duration | Work Done | Decisions Made | Gaps Found | Lessons Learned |
|------|-------|----------|-----------|----------------|------------|-----------------|
