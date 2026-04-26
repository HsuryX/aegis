---
name: gap
description: Record missing information, blockers, deviations, or framework issues in .agent-state/gaps.md
---

# gap

Use when information is missing, a rule cannot be followed, scope is being
deferred, or a framework problem is discovered.

Choose the next monotonic `G-{n}` ID and follow `.agent-state/gaps.md` plus
`playbooks/gaps.md`.

Gap types:

- `evidence`
- `analysis`
- `decision`
- `framework`
- `deviation`
- `conditional`
- `scope-reduction`
- `failure-pattern`
- `grandfathered`

Severity:

- `critical`: blocks phase advancement
- `non-critical`: tracked but does not block, with justification

Type-specific rules:

- `deviation` and `grandfathered` require an expiry condition.
- `conditional` and `scope-reduction` require a trigger condition.
- `grandfathered` requires the initial artifact set.
- `conditional` gaps from `keep-with-conditions` must link the audit verdict.

Never silently defer a requirement; record an explicit `scope-reduction` gap.
