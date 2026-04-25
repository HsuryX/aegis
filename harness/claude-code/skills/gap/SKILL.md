---
name: gap
description: Use when information is missing, unclear, or blocking, or when a framework rule deviation needs tracking
---

# /gap

Creates a new gap entry following the Entry Template in `.agent-state/gaps.md` and the identifier rules in `playbooks/identifiers.md`.

## What it does

1. Reads `.agent-state/gaps.md` to determine the next monotonic `G-{n}` ID
   - IDs are assigned in creation order across the entire project lifetime
   - Resolved gaps retain their ID even when archived to `gaps-archive.md`
2. Prompts for severity, type, description, resolution path, and any required trigger / expiry / linked-verdict fields for the chosen type
3. Writes a new entry in the appropriate section (Critical Gaps or Non-Critical Gaps)

## Gap types

Nine types, ordered by how they arise in the workflow (see `playbooks/gaps.md` for the full taxonomy with resolution rules — that section is canonical; update this enum when the canonical list changes):

- **evidence** — empirical data needed; usually triggers a time-boxed spike (see `playbooks/01-design.md` Prototyping Protocol)
- **analysis** — deeper thinking on an existing question
- **decision** — a new decision entry is required (the gap is the trigger; the decision is the resolution)
- **framework** — the framework itself has a rule that needs amendment (see `playbooks/principles-gates.md` Amendment Protocol)
- **deviation** — a framework-rule exception with an explicit expiry condition
- **conditional** — a verdict/gate carry-forward obligation; created by `keep-with-conditions` or `Conditional Go`, and MUST be met before its trigger fires
- **scope-reduction** — an explicit, tracked deferral of a specified requirement; the permitted alternative to silent scope reduction (see `playbooks/03-implement.md` Hard Rule 3)
- **failure-pattern** — a named failure mode from `playbooks/failure-patterns.md` detected during work; resolved when the pattern's counter is applied and verified
- **grandfathered** — a pre-adoption artifact preserved under explicit expiry; used at adoption time when aegis is applied to an existing project with pre-existing artifacts that would otherwise fail traceability or coverage rules (see `playbooks/gaps.md` grandfathered definition)

## Severity

- **critical** — blocks phase advancement; MUST be resolved before the next phase gate
- **non-critical** — tracked but does not block; MAY remain open past phase gates with justification

When in doubt, classify as critical — false positives cost less than false negatives.

## When to invoke

- When information is missing, unclear, or contradictory
- When a framework rule cannot be followed for a specific reason (use type `deviation` with explicit expiry)
- When an architectural discovery during implementation reveals a design-phase gap
- When the agent is tempted to make an on-the-fly judgment call that would affect more than one file — the temptation itself is evidence that a gap exists

## Expiry, triggers, and re-evaluation

Four gap types carry time-sensitive conditions (see `playbooks/gaps.md` for the full lifecycle):

- **deviation** — MUST have an **Expiry condition** (e.g., "until Phase 2 completes", "until D-{n} is revised"). At session start, the agent MUST flag deviations that have outlived their expiry per the Session Start Protocol in `AGENTS.md`. If more than 3 active deviations exist simultaneously, the agent MUST report degraded governance status.
- **conditional** — MUST have a **Trigger condition** (the specific event that MUST cause the condition to be met). If it comes from a `keep-with-conditions` verdict, it MUST also carry a **Linked verdict** naming the audit surface. When its trigger fires while still open, the carry-forward fails: audit-linked conditionals revert the verdict to `redesign`; gate-linked conditionals block the named next gate.
- **scope-reduction** — MUST have a **Trigger condition** (when the deferred requirement MUST be restored). For `critical`-severity scope-reduction gaps, user confirmation is REQUIRED before the code change that relies on the deferral. An unmet trigger at gate time produces `Hold` and escalates to the user per `playbooks/gaps.md` Scope-reduction gaps and gate timing.
- **grandfathered** — MUST have an **Expiry condition** (typically "when 100% of originally-grandfathered artifacts have been edited, superseded, or deleted") and an **Initial artifact set** listing the legacy artifacts covered (file paths or a `git log` anchor). MUST NOT be invoked retroactively on artifacts modified after adoption.

## Label references

- `G-{n}` identifies the gap itself
- `Closes: G-{n}` in commit trailers identifies commits that resolve the gap
- Gaps reference decisions by ID when the gap is a decision gap (e.g., "Blocks: D-5")
