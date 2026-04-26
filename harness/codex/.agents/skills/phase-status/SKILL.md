---
name: phase-status
description: Inspect current aegis phase, lifecycle mode, gate status, decisions, and gaps
---

# phase-status

Use at session start, before phase transitions, and whenever current governance
state is uncertain.

Read:

- `.agent-state/phase.md`
- `.agent-state/audit.md`
- `.agent-state/decisions.md`
- `.agent-state/gaps.md`
- archive files when required by `AGENTS.md`

Report a concise status:

- Current phase and gate status
- Terminal phase
- Lifecycle mode
- Scope classification
- Open decisions
- Critical gaps
- Non-critical gaps count
- Active deviations and expired deviations
- Handoff context and next action

Before acting, verify ledger integrity with a countable or tool-checkable
evidence block. Prose-only "verified" statements are not valid evidence.
