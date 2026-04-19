---
name: audit-surface
description: Use during Phase 0 when auditing a surface to record findings and verdicts in audit.md
---

# /audit-surface

Creates a new audit surface entry in `.agent-state/audit.md` following the Per-Surface Entry Format defined in `playbooks/00-audit.md`.

## Surfaces

The framework audits seven surfaces, ordered by the constraint chain — earlier surfaces constrain later ones:

1. **Product** — boundary, scope, goals, non-goals (REQUIRES `SC-{n}` and `NG-{n}` labels per `playbooks/identifiers.md`)
2. **Architecture** — subsystems, dependency direction, public contracts, data model, versioning
3. **Runtime** — behavior, state, errors, recovery, configuration
4. **Operations** — build, CI/CD, deployment, observability
5. **Security** — trust boundaries, secrets, authentication, authorization
6. **Quality** — tests, dependency health, code quality, accessibility
7. **Organization** — naming consistency, documentation accuracy, repository structure

## Per-surface entry format

See `playbooks/00-audit.md` "Per-Surface Entry Format" for the canonical field layout. The skill writes entries with these fields:

- **Exists:** factual description of current state
- **Strong:** genuinely good elements worth preserving — be specific
- **Wrong:** stale, contradictory, misleading, accidental, or missing — be specific
- **Reference:** file paths, URLs, or sources examined
- **Verdict:** `keep` | `keep-with-conditions` | `redesign` | `delete`
- **Conditions:** (required only when Verdict is `keep-with-conditions` — list each condition as a reference to a gap entry `G-{n}` of type `conditional`; omit for other verdicts)
- **Design notes:** considerations, risks, or constraints for the design phase

Every existing element MUST receive exactly one of the four verdicts above. There MUST NOT be an implicit fifth state. `keep-with-conditions` requires every condition to be tracked as a `conditional` gap entry in `gaps.md` with an explicit trigger for when the condition MUST be met — an unmet condition at gate time reverts the verdict to `redesign`. Existence, age, test coverage, and downstream dependents MUST NOT be used as justification for a verdict.

## Scope-driven surface count

The Project Scope Classification in `playbooks/00-audit.md` determines which surfaces MUST be audited:

- **Micro**: Product + Security
- **Small**: Product + Architecture + Security + Quality
- **Standard / Large**: all seven

If the scope is uncertain, the framework prefers over-auditing to under-auditing — under-governing costs more than over-governing.

## When to invoke

- At Phase 0 for each surface required by the scope classification
- When reclassifying scope upward during a later phase (previously skipped surfaces become required) — this triggers the Phase Regression Procedure in `AGENTS.md` to the earliest phase whose gate criteria are no longer met
- When a surface was missed and its absence blocks a design decision (escalate to Phase 0 regression)

## Label references (Product surface only)

- `SC-{n}` — product success criteria (testable, binary pass/fail)
- `NG-{n}` — product non-goals (explicit exclusions to prevent silent scope creep)

These labels are mirrored in spec files under `specs/` during Phase 2.
