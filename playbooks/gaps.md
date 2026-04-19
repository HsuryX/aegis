<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/gaps
title: Gap Playbook
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: all
severity: normative
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/failure-patterns.md
  - playbooks/03-implement.md
supersedes: null
---

# Gap Playbook

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **artifact**, **gap**, **review**, **significant decision**, **verify**. A "gap" is missing, unclear, or blocking information — distinct from a decision (resolved information). See the glossary for the full definition.

## Purpose

Gaps track unresolved information that the framework cannot yet act on. They are the framework's mechanism for acknowledging uncertainty without either ignoring it or blocking all progress. Every gap has a severity (determines whether it blocks phase advancement), a type (determines how to resolve it), and a lifecycle (determines when it expires or MUST be acted upon).

Gap entries live in `.agent-state/gaps.md`. Identifiers follow the rules in [`identifiers.md`](./identifiers.md): `G-{n}` IDs are monotonic across the entire project lifetime and MUST NOT be reused after resolution. Resolved gaps retain their original ID for historical traceability.

## Gap Type Taxonomy

Nine types, ordered by how they arise in the workflow:

| Type | Meaning | When to use | Resolution |
|---|---|---|---|
| **evidence** | Empirical data needed — a spike or prototype is required to answer a specific question. | A design decision cannot be moved to `Accepted` without experimental data. | Spike outcome recorded in the gap's Resolution field; blocked decision moves toward `Accepted` or `Rejected`. See `01-design.md` Prototyping Protocol. |
| **analysis** | Deeper thinking needed on an existing question — no spike required, but the answer is not yet clear. | A design decision has multiple viable alternatives and the current analysis is insufficient to choose. | Extended analysis recorded; decision moves forward or the gap is converted to `evidence` if a spike is needed. |
| **decision** | A new design decision is required — a concept arose that has no decision entry. | Implementation or specification work reveals an architectural choice that was not anticipated during Phase 1. | A new `D-{n}` entry is created in `decisions.md`; the agent regresses to Phase 1 if the decision is cross-cutting. |
| **framework** | A framework rule itself is wrong or inadequate. | A playbook rule produces a bad outcome per the Spirit = Letter threshold in `principles.md`, or a rule is ambiguous enough to produce inconsistent behavior across sessions. | Proposed amendment via the Amendment Protocol in `AGENTS.md`. The user decides. |
| **deviation** | A recorded departure from a framework rule, approved by the user, with an explicit expiry condition. | The user authorizes a temporary exception to a framework rule. | The expiry condition fires; the deviation is either converted to a framework amendment or the original rule is restored. Expired deviations MUST be flagged at session start per `AGENTS.md` Session Start Protocol step 3. |
| **conditional** | A condition attached to a `keep-with-conditions` verdict in `audit.md`. MUST be met before the next phase gate fires. | An audit surface element is correct in substance but requires specific follow-up work. See `AGENTS.md` Verdict Discipline. | The condition is met (code change, decision, or verification); the linked verdict is confirmed as `keep`. An unmet condition at gate time reverts the verdict to `redesign`. |
| **scope-reduction** | An explicit, tracked deferral of a specified requirement — the permitted alternative to silent scope reduction. | A specified requirement cannot be implemented in the current phase but the deferral is deliberate, bounded, and user-confirmed when critical. See `03-implement.md` Hard Rule 3. | The trigger condition fires and the requirement is restored; or the requirement is renegotiated with the user and the gap is converted to a decision. |
| **failure-pattern** | A named failure mode detected during work — matches a pattern in `failure-patterns.md`. | The agent recognizes a known anti-pattern (e.g., "kitchen-sink-session", "wrapper-preservation", "rationalization-cascade") during a session. | The pattern's documented counter is applied; the gap is resolved when the counter is verified. See `failure-patterns.md` for the 12-pattern registry with Symptom / Counter / Cross-reference for each. |
| **grandfathered** | Pre-adoption artifact preserved under explicit expiry — legacy tests, specs, or decisions that existed before aegis was adopted and cannot be retrofitted at once. | At adoption time, when aegis is applied to an existing project with pre-existing artifacts that would otherwise fail traceability or coverage rules. Prevents the adoption cliff from blocking adoption. See `03-implement.md` Legacy-test grandfathering for the canonical pattern. | Expires when 100% of the originally-grandfathered artifacts have been edited, superseded, or deleted. The entry MUST list the initial set (or a `git log` anchor) so the expiry is verifiable. Grandfathering MUST NOT be invoked retroactively on artifacts modified after adoption — any touched artifact reverts to the normal traceability requirement. |

## Severity Criteria

Two levels:

- **Critical** — the gap makes it impossible to produce a correct result in the current phase. Missing information that prevents a decision, unresolved contradiction between decisions, security or correctness concern, or ambiguity that would cause two competent agents to produce incompatible outputs. **Blocks phase advancement** — the phase gate MUST NOT pass with any open critical gap. Gate outcome: `Hold` or `Recycle` per the Gate Outcome Vocabulary in `principles.md`.
- **Non-critical** — the gap SHOULD be addressed but the current phase can produce a correct (if incomplete) result without it. Optimization opportunities, edge cases with known workarounds, style or naming refinements, low-risk assumptions with documented fallback. **Does NOT block phase advancement** — the gate MAY pass with tracked non-critical gaps.

When uncertain, classify as critical — false positives cost less than false negatives.

## Quick Capture

When the agent discovers a side-finding during work and the full 9-field gap entry format would disrupt flow, the agent MAY use the Quick Capture shorthand — a 3-field entry that records the finding with minimal friction, then MUST be triaged to a full entry before the next phase gate.

```markdown
### G-{n}: {title}
**Status:** captured
**Quick note:** {one-line description of the finding}
**Severity guess:** critical | non-critical
**Date captured:** YYYY-MM-DD
```

**Lifecycle:** `captured` entries MUST be triaged to full entries (with all required fields per the Entry Format below) before the next phase gate evaluates. The agent MUST either expand the captured entry in-place (adding the missing fields and changing `Status:` to `open`) or discard it with a one-line justification in the session log. Untriaged `captured` entries block the gate — mechanically, `grep -c 'Status:\*\* captured' .agent-state/gaps.md` MUST return zero at gate time.

Quick Capture exists to prevent a common failure mode: gap entries written under time pressure skip required SCHEMA fields. By legitimizing a lightweight capture format, the framework channels the "write it down fast" impulse into a structured path rather than fighting it. The triage step ensures completeness before the entry can influence gate outcomes.

## Gap Lifecycle

All gaps start as `open` (or `captured` via Quick Capture, then triaged to `open`). Resolution depends on the type:

- **evidence, analysis, decision**: resolved when the information is obtained and recorded in the Resolution field. For `decision` type, a corresponding `D-{n}` entry MUST exist in `decisions.md`.
- **framework**: resolved when the user approves, modifies, or rejects the proposed amendment per the Amendment Protocol.
- **deviation**: resolved when the expiry condition fires AND either the original rule is restored or a framework amendment is approved. Expired deviations that remain unresolved MUST be flagged at every session start.
- **conditional**: resolved when the condition is met. An unmet condition at gate time reverts the linked `keep-with-conditions` verdict to `redesign` — the gap transitions to "resolved (unmet — verdict reverted)" and the affected surface MUST be re-audited.
- **scope-reduction**: resolved when the trigger fires and the deferred requirement is restored, or when the user explicitly renegotiates the requirement into a decision.
- **failure-pattern**: resolved when the pattern's documented counter is applied and verified effective.
- **grandfathered**: resolved when the expiry condition fires — either 100% of originally-grandfathered artifacts have been edited/superseded/deleted, or the user explicitly retires the grandfathering convention via the Amendment Protocol. Partial resolution (some artifacts retrofitted) does NOT close the gap; the gap tracks the full set.

**Archival:** per `principles.md` Required Behaviors #6 (state-file hygiene) and #7 (archive consultation), resolved gaps are archived to `gaps-archive.md` when `.agent-state/gaps.md` exceeds 300 lines. Archived entries retain their original `G-{n}` ID. The agent MUST read the archive when creating new gaps to check for conflicts or recurrences.

## Entry Format

The canonical working template lives in `.agent-state/gaps.md`. Required fields for all types: Status, Severity, Type, Blocks, Description, Resolution path, Resolution, Date opened, Date resolved.

Additional fields by type:

| Field | Required for | Purpose |
|---|---|---|
| **Expiry condition** | `deviation`, `conditional`, `scope-reduction`, `grandfathered` | When the entry expires or its trigger fires |
| **Trigger condition** | `conditional`, `scope-reduction` | The specific event that MUST cause action |
| **Linked verdict** | `conditional` | The `keep-with-conditions` audit surface this condition belongs to |
| **Initial artifact set** | `grandfathered` | List of file paths or a `git log` anchor identifying the legacy artifacts covered — required for expiry verification |
| **Severity history** | any type whose Severity has changed since opening | Append-only record of each severity change (see Severity history rule below) |

All other type-specific fields leave blank or omit when not applicable. **Severity history** applies to all types but is required only when the Severity value has actually changed.

**Severity history (append-only, all types).** Any entry whose `Severity` value has changed since the gap was first opened MUST carry a `**Severity history:**` field listing each change as `{YYYY-MM-DD}: {old} → {new} — {justification}`. A severity **downgrade** (critical → non-critical) is a known abuse vector: an unresolved critical gap can be made to pass the phase gate by mechanical severity change rather than actual resolution. Downgrades MUST cite: (a) what specific evidence justifies the reduced severity, OR (b) a named user approval recorded in the session log (for critical → non-critical, user approval is RECOMMENDED). Upgrades (non-critical → critical) require no justification beyond "new evidence" and MAY be applied by the agent unilaterally — erring on the side of critical is consistent with the Severity Criteria principle. A `validate.py` check cross-references `gaps-archive.md` against the current `gaps.md` severity values; any silent downgrade of an archived-critical gap is a check failure.

## Phase-Gate Interaction

| Severity | Gate behavior |
|---|---|
| **Critical** | Blocks advancement. Gate outcome MUST be `Hold` or `Recycle` until all critical gaps are resolved. Mechanical check: `grep -A1 '^### G-' .agent-state/gaps.md \| grep -B1 'Severity:\*\* critical' \| grep 'Status:\*\* open'` MUST return zero hits. |
| **Non-critical** | Does NOT block advancement. The gate MAY pass. The agent MUST list open non-critical gaps in the gate report so the user is aware of the tracked debt. |

**Conditional gaps and gate timing:** a `conditional` gap's `Trigger condition` defines WHEN the condition MUST be met. If the trigger fires and the gap is still open, the linked `keep-with-conditions` verdict reverts to `redesign` and the gap becomes critical (blocks the gate until the reverted verdict is addressed).

**Scope-reduction gaps and gate timing:** a `scope-reduction` gap's `Trigger condition` defines WHEN the deferred requirement MUST be restored or renegotiated. If the trigger fires and the gap is still open (the requirement is neither restored nor explicitly renegotiated into a decision), the gap becomes critical — gate outcome MUST be `Hold` per the Gate Outcome Vocabulary in `principles-gates.md`. The agent MUST escalate to the user with three explicit options: (a) restore the deferred requirement immediately, (b) renegotiate the scope with the user and convert the gap to a new decision (`D-{n}`) that captures the renegotiated scope, or (c) extend the trigger with explicit user approval, recorded as a `deviation`-type gap with its own expiry condition. The agent MUST NOT silently extend the trigger — that converts an explicit deferral back into the silent scope reduction the rule exists to prevent (per `zen.md` aphorism #17).

## Cross-References

- Gap identifiers: [`identifiers.md`](./identifiers.md) `G-{n}` rules
- Gap entry working template: `.agent-state/gaps.md`
- Archival rules: `principles.md` Required Behaviors #6 (state-file hygiene) and #7 (archive consultation)
- Framework amendment flow: `AGENTS.md` Amendment Protocol
- Deviation tracking: `AGENTS.md` Amendment Protocol (temporary deviations)
- Verdict conditions: `AGENTS.md` Verdict Discipline (`keep-with-conditions`)
- Scope deferral: `03-implement.md` Hard Rule 3 (silent vs. explicit deferral)
- Prototyping: `01-design.md` Prototyping Protocol (evidence type)
- Failure patterns: `failure-patterns.md` (12 named failure modes with counter rules)
