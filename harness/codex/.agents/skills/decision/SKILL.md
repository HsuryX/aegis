---
name: decision
description: Record a design decision in .agent-state/decisions.md
---

# decision

Use when a significant design decision is needed. Follow the Decision Entry
Format in `playbooks/01-design.md` and the identifier rules in
`playbooks/identifiers.md`.

Workflow:

1. Read `.agent-state/decisions.md` and choose the next monotonic `D-{n}` ID.
2. Use `D-1` through `D-12` only for Required Decisions; use `D-13+` for project-specific decisions.
3. Record context, prior art, at least two structurally different alternatives, the chosen decision, why it wins, confirmation method, unresolved concerns, and downstream impact.
4. Start as `Draft` unless the decision has already passed review.
5. For `Accepted`, `Final`, or `emergency`, include a concrete confirmation mechanism.

Do not make significant architecture choices only in prose or code comments.
If discovery during implementation reveals a new decision need, regress to the
appropriate earlier phase per `AGENTS.md`.
