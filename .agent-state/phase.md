<!-- SCHEMA:
file_type: state
top_level_fields:
  - "Current phase: 0-audit | 1-design | 2-spec | 3-implement"
  - "Terminal phase: 0-audit | 1-design | 2-spec | 3-implement"
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
  - "**Exit audit (from prior agent):** {populated by the exiting agent per AGENTS.md Multi-Agent Handoff Protocol — phase state summary, open items, known risks, evidence pointer. Single-agent projects may record 'single-agent continuation' here.}"
  - "**In progress:** {current session state — update before ending a session}"
  - "**Entry acknowledgment (by receiving agent):** {populated when a session picks up another agent's work — re-read confirmation, discrepancies found, accepted scope. Single-agent projects may record 'same agent, continuous session' here.}"
  - "**Previous context ({label}, historical):** {demoted prior In progress blocks}"
  - "**Next:** {next session pointer with full plan}"
session_log_format: |
  | Date | Phase | Duration | Work Done | Decisions Made | Gaps Found | Lessons Learned |
  | YYYY-MM-DD | {phase-slug} | {N sessions} | {summary} | {D-{n} list or "(none)"} | {G-{n} list or "(none)"} | {lessons or "(none new)"} |
reference: AGENTS.md Session Start Protocol + Handoff Context
-->

# Phase Status

**Current phase:** 0-audit
**Terminal phase:** 3-implement
**Last updated:** YYYY-MM-DD
**Scope classification:** (to be determined in Phase 0 per `playbooks/00-audit.md` Project Scope Classification)
**Project type:** (free-form — e.g., "TypeScript REST API", "Python CLI", "governance framework")

| Phase | Status | Gate Met | Date Entered |
|-------|--------|----------|--------------|
| 0. Audit | in-progress | no | YYYY-MM-DD |
| 1. Design | not-started | no | — |
| 2. Spec | not-started | no | — |
| 3. Implement | not-started | no | — |

## Integrity Invariants

(None recorded yet. Session Start Protocol step 3 in `AGENTS.md` requires each session to append a concrete `Integrity check {YYYY-MM-DD HH:MM UTC}: ...` block to the current session's Handoff Context; this section is a quick-reference index of those blocks.)

## Handoff Context

**Exit audit (from prior agent):** (populate at session end per `AGENTS.md` Multi-Agent Handoff Protocol — phase state summary, open items, known risks, evidence pointer. Single-agent projects may record "single-agent continuation" here.)

**In progress:** (current session state — update before ending a session.)

**Entry acknowledgment (by receiving agent):** (populate when a session picks up another agent's work — re-read confirmation, discrepancies found, accepted scope. Single-agent projects may record "same agent, continuous session" here.)

**Next:** (next session pointer with full plan.)

## Feature Slices (if applicable)

(Applies only when Phase 1 invokes the Decomposition Rule in `playbooks/01-design.md`. For monolithic projects, leave this section as the placeholder.)

## Session Log

| Date | Phase | Duration | Work Done | Decisions Made | Gaps Found | Lessons Learned |
|------|-------|----------|-----------|----------------|------------|-----------------|
| YYYY-MM-DD | 0-audit | 0 sessions | (template — no work yet) | (none) | (none) | (none new) |
