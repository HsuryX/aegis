---
name: audit-surface
description: Record a Phase 0 surface audit entry in .agent-state/audit.md
---

# audit-surface

Use during Phase 0 to record one audited surface using the Per-Surface Entry
Format in `playbooks/00-audit.md`.

Required surfaces are scope-dependent:

- `micro`: Product, Security
- `small`: Product, Architecture, Security, Quality
- `standard` / `large`: Product, Architecture, Runtime, Operations, Security, Quality, Organization

For each surface, record:

- `Exists`: factual current state
- `Strong`: specific elements worth preserving
- `Wrong`: stale, contradictory, misleading, accidental, or missing elements
- `Reference`: file paths, URLs, or sources examined
- `Verdict`: `keep`, `keep-with-conditions`, `redesign`, or `delete`
- `Conditions`: only for `keep-with-conditions`, each linked to a `conditional` gap
- `Design notes`: constraints and risks for Phase 1

Every existing element must receive exactly one verdict. Do not treat existence,
age, tests, or downstream dependents as acceptance evidence.
