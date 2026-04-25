---
name: decision
description: Use when a significant design decision needs to be recorded during Phase 1 or when architectural discovery surfaces a new decision need
---

# /decision

Creates a new decision entry following the Decision Entry Format in `playbooks/01-design.md` and the identifier rules in `playbooks/identifiers.md`.

## What it does

1. Reads `.agent-state/decisions.md` to determine the next monotonic `D-{n}` ID
   - `D-1` through `D-12` are reserved for Required Decisions in `01-design.md`
   - `D-13` and above are project-specific
   - IDs are monotonic and MUST NOT be reused
2. Prompts the agent for the decision title, context, alternatives, and rationale
3. Writes a new entry in the Active Decisions section using the canonical template:
   - `Status` (Draft | Proposed | Accepted | Final | Superseded (by D-{new}) | Rejected | Deferred | not-applicable | emergency) — mirrors `01-design.md` Decision Lifecycle; that section is canonical. Update this enum when the canonical list changes.
   - `Date opened`, `Date accepted`, `Date final`
   - `Surface` (which audit surface this addresses)
   - `Supersedes` (D-{old} if this decision replaces an earlier one; omit otherwise)
   - `Context` (what forces the decision — not what was chosen, but why a choice is needed)
   - `Prior art` (1–3 sentences on how similar problems have been solved elsewhere — REQUIRED for significant decisions per `principles.md` Quality Seeking)
   - `Decision` (what was chosen)
   - `Alternatives considered` (at least 2 structurally different options with their strengths)
   - `Why this option wins` (compare each alternative against simplicity, correctness, maintainability, extensibility)
   - `Confirmation` (how compliance is verified — REQUIRED when Status is Accepted, Final, or emergency)
   - `Unresolved concerns`
   - `Downstream impact`
4. Applies the Quality Seeking protocol for significant decisions (generate alternatives, argue against your preference, then decide)

## Canonical template

See `playbooks/01-design.md` "Decision Entry Format" for the exact field layout. The skill enforces:

- **At least 2 alternatives** — a decision with fewer alternatives is rejected until more are considered
- **Why this option wins** MUST compare against simplicity, correctness, maintainability, extensibility — a one-sentence dismissal of an alternative is not genuine analysis
- **Status** starts as `Draft` while being written; transitions to `Proposed` when ready for review; becomes `Accepted` after review passes; transitions to `Final` when the Confirmation mechanism demonstrably fires (e.g., the spec's `specs/<spec>.md:SC-{n}` test passes, the hook is wired and firing, the audit check returns clean). Terminal states (`Superseded (by D-{new})`, `Rejected`, `not-applicable`) retain the entry for traceability and MUST NOT be cited as `Implements:` trailers on live code. `Deferred` is a non-terminal pause state that can return to `Draft` when its trigger fires.

## When to invoke

- Any time a significant decision is needed (a decision where changing it later would require modifying more than one file OR two reasonable engineers could disagree on the answer — see `playbooks/glossary.md` significant decision)
- At Phase 1 Design when working through the 12 Required Decisions
- When opening D-13+ project-specific decisions. Common candidates include **Contract Format** (REQUIRED for cross-trust-boundary interfaces; see `playbooks/standards.md` Contract Formats and `02-spec.md`), **Subsystem Ownership** (REQUIRED only when the project meets ALL `principles-conditional.md` Multi-Agent Handoff Protocol conditions: scope `standard|large`, ≥ 2 subsystems, and ≥ 3 distinct agents or team members across the project lifetime), **Accessibility Model** (REQUIRED when UI is present — target WCAG level, testing approach, AT support per `standards.md`), deployment model, caching strategy, internationalization, API versioning, deployment safety
- During implementation if architectural discovery reveals a gap — in which case the agent MUST first regress to Phase 1 per the Phase Regression Procedure in `AGENTS.md`

## D-10 Test strategy expansion

For standard/large scope, D-10 MUST populate four fields beyond framework + runner: (a) **test pyramid ratio** (default 70:20:10), (b) **per-layer coverage floor** (unit ≥ 80%, integration ≥ 70%, e2e ≥ critical-flow count), (c) **mechanical enforcement command per layer** (e.g., `pytest tests/unit --cov-fail-under=80`), (d) **trust-boundary coverage floor** (95% line + 70% branch per `standards.md`).

## Label references

- `D-{n}` identifies the decision itself
- `Implements: D-{n}` in commit trailers identifies commits that realize the decision
- `Closes: G-{n}` in commit trailers identifies commits that resolve a tracked gap as part of the decision
