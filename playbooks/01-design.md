<!--
SYNC-IMPACT
- version: 1.1.0 → 1.2.0
- bump: MINOR
- date: 2026-04-25
- rationale: Framework support-scope release; see CHANGELOG.md#v120 for the evidence and migration summary.
- downstream_review_required:
  - CHANGELOG.md
-->
---
id: playbooks/01-design
title: Phase 1: Design
version: 1.2.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 1-design
severity: normative
mechanical_items: 4
judgment_items: 28
mixed_items: 1
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/identifiers.md
  - playbooks/standards.md
  - playbooks/security-threat-model.md
  - playbooks/00-audit.md
  - playbooks/02-spec.md
supersedes: null
---

# Phase 1: Design

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **artifact**, **canonical**, **gap**, **review**, **significant decision**, **surface**, **trust boundary**. "Significant decision" is the threshold that triggers the full Quality Seeking protocol — see the glossary for the criteria.

## Objective

The agent MUST close all major architectural decisions. The target system shape MUST be specific enough that implementation requires no further architectural discovery.

## Required Decisions

Ordered by dependency — earlier decisions constrain later ones. Each MUST be recorded in `.agent-state/decisions.md` with a unique ID. The agent MUST apply the Quality Seeking protocol to every decision.

1. **Architecture** — subsystems, boundaries, dependency direction
2. **Authority model** — what owns truth for each domain concept. For **micro and small scope** projects, D-2 MAY be simplified to a single-paragraph owner-per-concept statement without a formal authority-map diagram, provided Authority Discipline (no duplicate truth) is still respected. For **standard and large scope**, D-2 REQUIRES the full authority map — one entry per durable concept with owner, dependencies, and invariants; the map MUST be consulted by the Whole-System Composition Check.
3. **Public contracts** — exact interfaces, not vague descriptions; include field ordering conventions. When the project exposes any cross-trust-boundary interface, the contract MUST have both a **prose contract** (markdown `Contract` section in the spec) AND a **machine-readable contract** in one of the canonical forms listed in `standards.md` Contract Formats (the sole canonical menu — do not re-enumerate here). The D-13+ Contract Format candidate decision (see below) resolves which form. Internal-only interfaces MAY record `schema: N/A — internal only` with a one-line justification. Operator-facing prose contracts that D-13 explicitly classifies as `schema: N/A — operator-facing prose contract` are also exempt from the machine-readable requirement.
4. **Data model** — canonical object shapes, persistence format, wire format; include field and column ordering conventions
5. **Security model** — trust boundaries, secret management, authentication, authorization, input validation strategy. When any `playbooks/security-threat-model.md` applicability condition is met, D-5 MUST link to a full STRIDE threat model artifact at `specs/threat-model.md`. Projects qualifying for the N/A escape record `threat model: N/A — {justification}` in D-5 and must state why none of the four applicability conditions are present.
6. **Error and recovery model** — failure semantics, degraded states, recovery order and preconditions
7. **Naming model** — canonical term for each durable concept; populate the Naming Table (depends on concepts from 1–6 being identified)
8. **Configuration model** — what is configurable, what is not, where configuration lives, environment parity
9. **Observability model** — logging strategy (structured format, standard fields, levels), metrics, tracing, alert conditions. When the project emits distributed traces, cross-service metrics, or structured logs consumed by a third-party platform, D-9 SHOULD cite OpenTelemetry semantic conventions (https://opentelemetry.io/docs/specs/semconv/) as the target convention unless an alternative is explicitly justified. SHOULD, not MUST — projects using non-OTel stacks (bespoke log schemas, platform-native metrics) MAY document their own conventions, provided each span/metric/log field has a stated canonical name and no two fields carry the same meaning under different names
10. **Test strategy** — test framework and runner, test types, coverage targets, what is tested at which level, test data approach. For **standard and large scope**, D-10 MUST populate: (a) **test pyramid** ratio (target % of unit : integration : e2e — default 70:20:10 per `standards.md` Testing → Test pyramid; override with justification), (b) **per-layer coverage floor** (unit ≥ 80%, integration ≥ 70%, e2e ≥ critical-flow count per `standards.md` Testing → Per-layer coverage), (c) **mechanical enforcement command** per layer (e.g., `pytest tests/unit --cov-fail-under=80`), (d) **trust-boundary coverage floor** (95% line coverage + 70% branch coverage per `standards.md` Testing).
11. **Repository structure** — directory layout reflecting architecture, not history (depends on all above). REQUIRED for standard and large scope; MAY be `not-applicable` for small scope per `00-audit.md` Project Scope Classification (small scope projects with an established layout need not re-decide it as a formal D-11 entry)
12. **Documentation structure** — what documents exist (including README), what each one owns, what format (depends on all above). REQUIRED for standard and large scope; MAY be `not-applicable` for small scope per `00-audit.md` Project Scope Classification

### Canonical Dependency Edges

The "ordered by dependency" claim above is concrete: the canonical edges below hold for every project. They seed the `Downstream impact` graph that the Whole-System Composition Check at the bottom of this playbook toposorts. D-13+ decisions extend this graph by populating their own `Downstream impact:` field per the Decision Entry Format.

| From | Constrains (target decisions) | Reason |
|---|---|---|
| D-1 Architecture | D-2, D-3, D-4, D-5, D-6, D-10, D-11 | Subsystems and dependency direction define the targets every later decision binds to |
| D-3 Public contracts | D-4, D-7, D-10 | Wire format constrains data model; contract names enter the Naming Table; contract tests anchor the test strategy |
| D-4 Data model | D-7, D-11 | Data-shape names enter the Naming Table; persistence layout enters repository structure |
| D-5 Security model | D-6, D-7, D-9, D-10 | Trust boundaries inform error semantics; security terms enter the Naming Table; audit logging shapes observability; trust-boundary coverage floor (95%) drives the test strategy |
| D-6 Error / recovery | D-7, D-9, D-10 | Error names enter the Naming Table; observable error events enter observability; recovery paths drive test coverage |
| D-1..D-6 (collectively) | D-7 Naming model | Per the inline annotation on D-7 — concepts to name are gathered from the earlier decisions |
| D-1..D-10 (collectively) | D-11 Repository structure | Per the inline annotation on D-11 — directory layout reflects the full architecture |
| D-1..D-11 (collectively) | D-12 Documentation structure | Per the inline annotation on D-12 — what documents exist depends on the entire architecture |

D-8 (Configuration) and D-9 (Observability) are largely peers and MAY be opened after D-1 is settled. D-9 SHOULD follow D-5 when audit logging is in scope (security events drive observability targets). Both feed into D-11 and D-12 via the collective edges above.

The agent MUST settle decisions in dependency order per these edges; the agent MUST NOT open a downstream decision while its upstream dependency is still open, unless parallel evaluation is necessary to resolve a circular dependency. When invoking the parallel-evaluation exception, the agent MUST record (a) which two or more decisions form the cycle (cite IDs), (b) why neither side can be settled first, and (c) the resolution criterion that closes the cycle. The record MUST appear in the **Unresolved concerns** field of every involved decision entry; without that record, parallel evaluation is silent deferral and the gate fails.

Additional project-specific decisions SHOULD be added as D-13+ when the project scope demands them. Common candidates include:

- **Contract Format** — selects which machine-readable form (from the canonical menu in `standards.md` Contract Formats) is authoritative for the project's external interfaces. REQUIRED when the project exposes any cross-trust-boundary interface; MAY be omitted for purely internal tools. Links back to D-3 and to `standards.md` Contract Formats (the single source of truth for the format list).
- **Subsystem Ownership** — for projects meeting ALL of the `principles-conditional.md` Multi-Agent Handoff Protocol conditions — scope ∈ {`standard`, `large`}, ≥ 2 subsystems, and ≥ 3 distinct agents or team members across the project's lifetime — D-13+ MUST declare which owner (person, team, or agent) is responsible for each subsystem boundary (derived from D-1 Architecture). Ownership determines review assignment and gate approval in the Multi-Agent Handoff Protocol (`principles-conditional.md`). Exempt projects MAY omit this decision. When scope is `standard` or `large`, exempt projects SHOULD use the local `.agent-state/phase.md` note described in `principles-conditional.md`; for `micro` and `small`, that note is OPTIONAL.
- **Accessibility Model** — REQUIRED when the system has any user-facing interface (web, mobile, desktop, CLI) per `standards.md` Accessibility. The decision MUST specify: (a) target compliance level per interface class (WCAG 2.2 AA for web; platform-native + WCAG where applicable for mobile/desktop; the CLI checklist for terminal apps), (b) testing approach per `standards.md` Accessibility → Testing approach (automated scans, manual audit cadence, AT target, CI integration), (c) assistive-technology support target. Projects with no user-facing interface MAY record `accessibility: N/A — no user interface` with justification.
- **Deployment model, caching strategy, internationalization, API versioning, deployment safety strategy** (feature flags, progressive rollout)

The agent MUST apply the same Quality Seeking protocol and decision entry format to every D-13+ decision.

## Prototyping Protocol

When a design decision cannot be moved to `Accepted` with available evidence (documented in the decision entry's Alternatives considered analysis as "insufficient evidence to evaluate"), a time-boxed prototype (spike) MAY be authorized:

1. The agent MUST record the spike as a gap entry with type `evidence`, specifying: the question being answered, the maximum effort budget, the success criteria, and which decision it informs
2. Spike code is disposable — it MUST go in a temporary branch or directory, MUST NOT be placed in the canonical codebase, and MUST NOT be held to implementation standards
3. The spike's outcome MUST be recorded in the gap entry's Resolution field and used to move the blocked decision toward `Accepted` (or toward `Rejected` if the spike invalidates the approach)
4. A spike that exceeds its budget without clear results is evidence that the approach is too risky — the agent MUST record this finding
5. Maximum 2 spikes per design cycle; more indicates the project scope needs decomposition per the Decomposition Rule. If a third spike appears genuinely necessary — i.e., the underlying decision cannot be moved to `Accepted` without further empirical evidence AND the Decomposition Rule does not resolve the problem — the agent MUST NOT self-authorize it. The agent MUST stop and propose the third spike to the user, citing: (a) the concrete evidence gathered from the first two spikes, (b) why decomposition is not a viable alternative in this specific case, (c) the single question the third spike would answer, and (d) its bounded effort budget. The user MAY approve, modify, or reject. If approved, the agent MUST record the approval in the session log in `phase.md` AND as an "Unresolved concerns" note in the decision entry the spike serves (referencing the approval date). Recurrent third-spike requests across sessions are evidence that the scope itself needs decomposition — the agent MUST surface this pattern to the user rather than continue requesting exceptions

## Decision Entry Format

Identifiers follow the rules in [`identifiers.md`](./identifiers.md): `D-1` through `D-12` are reserved for the Required Decisions enumerated above, `D-13` and above are project-specific, IDs are monotonic and MUST NOT be reused. When a decision is revised, the original ID persists with `Status: Superseded (by D-{new})`; the replacement receives a new ID, goes through the normal `Draft` → `Proposed` → `Accepted` → `Final` lifecycle, and MUST populate its `Supersedes:` field with the old ID.

Fields ordered per ADR convention: identification → status → context → prior art → substance → analysis → confirmation → impact.

```markdown
### D-{number}: {title}

**Status:** Draft | Proposed | Accepted | Final | Superseded (by D-{new}) | Rejected | Deferred | not-applicable | emergency
**Date opened:** YYYY-MM-DD
**Date accepted:** YYYY-MM-DD
**Date final:** YYYY-MM-DD
**Surface:** {audit surface this addresses}
**Supersedes:** {D-{old} if this decision replaces an earlier one; omit otherwise}

**Context:** {what forces, constraints, or conditions make this decision necessary — not what was chosen, but why a choice is needed}
**Prior art:** {1–3 sentences on how similar problems have been solved elsewhere — related frameworks, published ADRs, well-known patterns. REQUIRED for significant decisions per `principles.md` Quality Seeking. For non-significant decisions (those failing the "more than one file OR two reasonable engineers could disagree" test), this field MAY be left with the literal rationale "not significant"}
**Decision:** {what was decided}
**Alternatives considered:** {at least 2 structurally different options with their strengths}
**Why this option wins:** {compare each alternative against simplicity, correctness, maintainability, extensibility — a one-sentence dismissal is not genuine analysis}
**Confirmation:** {how compliance with this decision is mechanically or judgmentally verified — examples: "verified by `specs/auth.md:SC-7` conformance test", "enforced by PreToolUse hook in `harness/claude-code/settings.json`", "audited at Phase 3 gate via Post-Change Verification item N", "grep check against the Naming Table in `decisions.md`". REQUIRED when Status is `Accepted`, `Final`, or `emergency`. MAY be refined as the mechanism matures (e.g., "will be verified by `specs/auth.md:SC-7`" at `Accepted` → "verified by `specs/auth.md:SC-7`, passing as of 2026-MM-DD" at `Final`)}
**Unresolved concerns:** {risks or objections acknowledged but accepted — record why they are acceptable; leave blank if none}
**Downstream impact:** {what this decision affects — decision IDs that depend on it, spec files, or subsystem names}
```

**Field-by-field requirements:**

- **Date opened** MUST be populated on entry creation (any Status).
- **Date accepted** MUST be populated when Status transitions to `Accepted`.
- **Date final** MUST be populated when Status transitions to `Final`.
- **Supersedes** MUST be populated on any entry that replaces a prior decision; omitted otherwise.
- **Prior art** MUST be populated for significant decisions before Status can leave `Draft`.
- **Confirmation** MUST be populated before Status can transition to `Accepted`. It MAY be refined when Status transitions to `Final`.
- **Unresolved concerns** MAY be left blank only when none exist; the agent MUST NOT omit the field.

When a decision is revised to a new entry, the agent MUST update the original entry's Status to `Superseded (by D-{new})` and MUST keep it in the Terminal Decisions section for traceability; the replacement entry receives a new ID and MUST populate its `Supersedes:` field with the old ID.

## Decision Lifecycle

Decisions move through a sequence of states. Each state imposes different obligations. Legitimate transitions form the following directed graph:

| State | Meaning | Required fields beyond the base (Date opened + Surface + Context) | Valid next states |
|---|---|---|---|
| **Draft** | Being written; not ready for review. | (none beyond base) | `Proposed`, `Rejected`, `Deferred`, `not-applicable` |
| **Proposed** | Author believes it is ready for review. | Decision + Alternatives considered + Why this option wins + Prior art (if significant) + Unresolved concerns + Downstream impact | `Accepted`, `Draft` (rework), `Rejected` |
| **Accepted** | Reviewed and approved; implementation not yet complete. This state replaces the prior vocabulary's `settled` value. | All `Proposed` fields + Confirmation + Date accepted | `Final`, `Superseded`, `Rejected` |
| **Final** | Implemented in code, verified by the Confirmation mechanism, and authoritative in current use. Later cycles MAY supersede it through the normal revision path. | All `Accepted` fields + Date final + Confirmation refined with evidence | `Superseded`, `Rejected` (terminal rollback only, under Rollback Protocol) |
| **Superseded (by D-{n})** | Replaced by a later decision. Retained for traceability. | `Status: Superseded (by D-{n})` reference | None — terminal |
| **Rejected** | Considered and not chosen. Retained to prevent re-deliberation and to support future alternatives analysis. | All `Proposed` fields + Why this option wins explaining the rejection | None — terminal |
| **Deferred** | Postponed with an explicit trigger condition that will resume analysis. | Explicit trigger condition in Unresolved concerns | `Draft` (when trigger fires), `Rejected` |
| **not-applicable** | Required slot (D-1..D-12) skipped because project scope does not require it. | Scope classification justification | None — terminal unless scope reclassifies upward |
| **emergency** | Hotfix recorded under the Hotfix Workflow in `03-implement.md`. MUST be reconciled within 48 hours. | Same required fields as `Accepted` + emergency reconciliation gap reference | `Accepted` (ratified) or `Rejected` (reverted) |

Any transition not listed above is prohibited. If the agent needs a transition that is not in the table, the agent MUST escalate via the Amendment Protocol in `principles-gates.md` rather than self-authorize.

**State counts at each phase gate:**

- **Phase 1 Design Closure Gate**: every Required Decision (D-1..D-12 for standard/large, D-1..D-10 for small) MUST be in `Accepted` or `not-applicable` state. No `Draft`, `Proposed`, or `Deferred` decisions MAY remain for Required slots.
- **Phase 2 Spec Gate**: every spec MUST trace to decisions in `Accepted` or `Final` state. `Draft`, `Proposed`, or `Deferred` decisions MUST NOT be used as spec traceability targets.
- **Phase 3 Completion**: every decision cited by implementation MUST be in `Final` state. `Superseded`, `Rejected`, and `not-applicable` decisions are retained in `decisions.md` for traceability but MUST NOT be cited as `Implements:` trailers on live code. `Deferred` decisions MUST have fired their trigger by Phase 3 completion (and moved to `Final` or `Rejected`), or be explicitly acknowledged as out-of-scope deferrals in the Phase 3 Completion Criteria. In `steady-state` mode, this check applies at cycle completion rather than implying end-of-history finality.

## Naming Table

The agent MUST maintain the Naming Table in `decisions.md` under a dedicated section. Entries MUST be ordered alphabetically by Canonical Term for lookup.

| Concept | Canonical Term | Owner | Forbidden Aliases |
|---------|---------------|-------|-------------------|
| (concept) | (the one name) | (which subsystem/spec) | (old, ambiguous, or colliding names) |

One concept, one name, used identically across code, documentation, and specifications. After populating the naming table, the agent MUST retroactively update all prior decisions (D-1 through D-6) to use canonical terms. Working names from earlier decisions MUST NOT persist. This terminological update does not constitute a substantive revision and does not trigger the cascade rule — unless the old and new terms were used with different intended meanings across decisions, indicating a semantic conflict that requires resolution.

## Whole-System Composition Check

Ordered from concrete to abstract: structural → authority → semantic → cross-cutting → global synthesis. Every item MUST be verified. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**Tally:** 1 `[M]` · 1 `[M+J]` · 8 `[J]`.

- [ ] **[J]** Boundary definitions MUST be consistent end-to-end (A→B and B→C MUST agree on what B is)
- [ ] **[J]** Repository structure MUST reflect the decided architecture
- [ ] **[J]** Authority model MUST NOT have duplicate truth owners
- [ ] **[J]** No subsystem MAY have silently become authoritative over another's domain
- [ ] **[M]** Naming MUST NOT collide across subsystems. Mechanical: the Naming Table in `decisions.md` MUST have no duplicate Canonical Term rows.
- [ ] **[J]** Public contracts, runtime behavior, and documentation MUST describe the same system — no contract MAY promise behavior the runtime will not implement, no runtime behavior MAY exist without a corresponding contract, and documentation MUST accurately describe both
- [ ] **[J]** Error/recovery paths MUST be coherent across subsystem boundaries
- [ ] **[J]** Concurrency model MUST be addressed for all shared mutable state (or declared single-threaded with justification)
- [ ] **[J]** When all decisions are composed, no decision's assumptions MAY be violated by another — the agent MUST trace each decision's Downstream impact to verify affected decisions still hold
- [ ] **[M+J]** Downstream impact references MUST form a DAG (no circular dependencies). Mechanical: a toposort of `Downstream impact` edges MUST complete without a cycle. Judgment: if D-X lists D-Y and D-Y lists D-X, the agent MUST resolve the cycle by clarifying which decision truly constrains the other.

## Decomposition Rule

If the project is too large for one coherent design pass, the agent MUST say so explicitly, MUST identify sub-projects (feature slices or bounded contexts) with dependency order, and MUST drive the highest-value sub-project through the full phase sequence first. Remaining sub-projects MUST wait — they begin their own phase sequence after the preceding sub-project completes or reaches a defined integration point (decided and recorded as a milestone). Each sub-project MUST share the same `decisions.md` and `gaps.md` but MUST track its own phase in `phase.md` (the agent MUST add a per-sub-project phase table below the main table). The agent MUST NOT simulate completeness.

**Feature-sliced delivery:** When requirements evolve or the project benefits from iterative delivery, feature slices MAY independently traverse the phase sequence. Feature A MAY be in Phase 3 (implementing) while Feature B is in Phase 1 (designing). Requirements for this model:
- Shared decisions in `decisions.md` serve as the integration backbone — all feature slices MUST read and respect `Accepted` or `Final` decisions
- When a feature slice's design reveals that a shared decision must change, ALL feature slices at Phase 2 or Phase 3 MUST evaluate the impact via the Cascade Rule and the Revision Impact Protocol in `02-spec.md`
- Cross-cutting concerns (security model, error model, naming model) MUST be `Accepted` globally before any feature slice enters Phase 2 — these MUST NOT be sliced
- The agent MUST record each feature slice's phase status in `phase.md`

## Design Closure Gate

Apply the shared gate procedure from `AGENTS.md` Phase Gates and `principles-gates.md` (Gate Outcome Vocabulary, Three-Tier Gate Criteria, Multi-Perspective Verification, Verification Coverage Matrix). Run the Adversarial Review Protocol per its Per-phase timing hooks table in `principles-gates.md` before scoring this checklist. This checklist records the Phase 1-specific criteria only.

**Tally:** 3 `[M]` · 0 `[M+J]` · 13 `[J]`. **Tiers:** 12 `[must-meet]` · 4 `[should-meet]` · 0 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** All required decisions MUST be recorded as `Accepted` (or explicitly marked `not-applicable` with justification) in `decisions.md` — for standard/large scope all 12 are REQUIRED; for small scope D-1 through D-10 are REQUIRED and D-11, D-12 MAY be marked `not-applicable` per the scope classification in `00-audit.md`. `Final` is also acceptable (and expected when a required decision is re-entered from a later phase). Mechanical: `grep -A2 -E '^### D-([1-9]|1[0-2]):' .agent-state/decisions.md | grep -E '^\*\*Status:\*\* (Draft|Proposed|Deferred)$'` MUST return zero hits for Required Decision IDs (D-1..D-12 are Required; D-13+ project-specific decisions MAY still be `Draft`/`Proposed`/`Deferred` at Phase 1 gate if they are not cross-cutting).
- [ ] **[J]** **[must-meet]** Product boundary MUST be explicit (what is in, what is out)
- [ ] **[J]** **[must-meet]** All subsystem boundaries MUST be defined
- [ ] **[J]** **[must-meet]** Authority model MUST have no gaps (every durable concept MUST have one owner)
- [ ] **[J]** **[should-meet]** Public contracts MUST be defined (or explicitly deferred with documented reason — deferred contracts MUST be recorded as `conditional` gap entries)
- [ ] **[J]** **[must-meet]** Data model MUST be fully specified (objects, persistence format, wire format)
- [ ] **[J]** **[must-meet]** Security model MUST cover trust boundaries, authentication, authorization, and input validation
- [ ] **[J]** **[must-meet]** Threat model MUST be complete OR explicit N/A recorded. For projects meeting the `playbooks/security-threat-model.md` applicability conditions (secrets, user data, cross-trust-boundary communication, or input from an external source that could be adversarial), the full STRIDE matrix MUST be populated per trust boundary with every STRIDE letter mitigated, structurally marked `N/A`, or carrying a cited `residual risk tracked in G-{n}` reference. The matrix artifact MUST exist at the path D-5 names (`specs/threat-model.md` is the default; D-5 MAY name another path with justification). For projects not meeting applicability, D-5 MUST record `threat model: N/A — {one-sentence justification}` referencing which of the four applicability conditions is absent. Mechanical: when applicability is met, `grep -c '^### Boundary:' {threat-model path}` MUST match the D-5 declared boundary count; AND `grep -cE '^- \*\*(Spoofing|Tampering|Repudiation|Information disclosure|Denial of service|Elevation of privilege):' {threat-model path}` MUST equal 6 × boundary count. Missing artifact when applicability is met fails the gate.
- [ ] **[M]** **[must-meet]** Naming table MUST be populated with no unresolved collisions. Mechanical: no duplicate Canonical Term rows in the Naming Table within `decisions.md`.
- [ ] **[J]** **[must-meet]** Critical failure and recovery semantics MUST be decided
- [ ] **[J]** **[should-meet]** Configuration and observability models MUST be decided
- [ ] **[J]** **[must-meet]** Test strategy MUST be decided
- [ ] **[J]** **[should-meet]** Repository structure MUST be decided
- [ ] **[J]** **[should-meet]** Documentation structure MUST be decided
- [ ] **[J]** **[must-meet]** Whole-system composition check MUST pass (delegates to the Composition Check section above)
- [ ] **[M]** **[must-meet]** No stale placeholders in authored artifacts. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b|\((forthcoming|pending)\)' .agent-state/decisions.md` MUST return zero hits.

If ANY `[must-meet]` item is NO, the gate outcome is `Hold` or `Recycle`. If only `[should-meet]` items are NO, the gate outcome is `Conditional Go` per the Gate Outcome Vocabulary in `principles-gates.md`.

## Pre-Closure Certainty Check

After every Design Closure Gate item is checked YES, the agent MUST answer these questions honestly before advancing. All seven are `[J]` (judgment) — no mechanical check can substitute for honest self-interrogation here.

**Tally:** 0 `[M]` · 0 `[M+J]` · 7 `[J]`. **Tiers:** 7 `[must-meet]` · 0 `[should-meet]` · 0 `[nice-to-have]`.

- **[J]** **[must-meet]** Did any decision move to `Accepted` based on the first reasonable answer instead of the genuinely best answer?
- **[J]** **[must-meet]** Are there interactions between decisions that have not been fully thought through?
- **[J]** **[must-meet]** Are there failure modes, edge cases, or concurrency scenarios not explicitly addressed?
- **[J]** **[must-meet]** Would a skeptical senior reviewer find gaps in any decision's rationale or alternatives analysis?
- **[J]** **[must-meet]** Is any decision vague enough that two competent engineers could design the affected subsystem differently? (Implementation detail ambiguity is resolved by specifications in Phase 2, not here.)
- **[J]** **[must-meet]** Are there any perspectives from Multi-Perspective Verification (see `principles-gates.md` Multi-Perspective Verification for the canonical perspective list) that have NOT been verified or did NOT produce clean results?
- **[J]** **[must-meet]** **Ideal Final Result (TRIZ):** For each decision, imagine the no-drawback version — the version that delivers the decision's benefit with zero cost, zero complexity, zero operational overhead. If the no-drawback version is different from what was chosen, why was it not chosen? If the answer is **"cost or effort only"**, the agent MUST revisit the decision — cost and effort alone do not justify the gap between ideal and chosen when the project is still in Phase 1. If the answer is an inherent constraint (physical, legal, contractual, external dependency), the agent MUST record the constraint in the decision's Context or Alternatives section so future revisions do not re-traverse the same ground.

If ANY answer is yes, the gate is NOT passed. The agent MUST return to the relevant decision, close the gap, re-run the composition check, and re-evaluate. The answers also MUST NOT conflict with the current fresh-context design/adversarial review artifacts or the recorded Verification Coverage Matrix; unsupported or contradicted "no" answers fail the gate. At standard/large scope, the current fresh-context gate review artifact is required evidence for these answers — the author alone is not the sole judge, and the gate review may reject any self-assessment it does not find supported. Thoroughness here prevents costly rework during implementation.

Answering "no" REQUIRES concrete evidence — the agent MUST cite the specific decisions, sections, or gap entries that address each concern. An unsupported "no" MUST be treated as "yes" (gate fails).

**Cascade rule:** When revising an `Accepted` or `Final` decision, the agent MUST re-evaluate every decision listed in the revised decision's own "Downstream impact" field (these are the decisions that depend on it). Revision follows the decision lifecycle: the original entry's Status transitions to `Superseded (by D-{new})` and a new entry is created starting in `Draft` — the new entry's `Supersedes:` field points to the old ID, and the new entry proceeds through the normal `Draft` → `Proposed` → `Accepted` → `Final` progression. If a downstream decision changes as a result, the agent MUST transitively re-evaluate its own downstream decisions through the same Supersede + new-entry mechanism. Cascade stops at any decision that does not change after re-evaluation — unchanged decisions MUST NOT propagate further. After all cascading is complete, the agent MUST re-run the Whole-System Composition Check. When an `Accepted` or `Final` decision requires revision during a later phase (Phase 2 or 3), the agent MUST regress to Phase 1 before revising — applying the standard phase regression procedure from `AGENTS.md`. The agent MUST NOT revise decisions in-place during later phases; the cascade rule and composition check MUST be satisfied within Phase 1 before re-advancing.

## Escalation Triggers

The agent MUST return to Phase 0 (Audit) if:
- A surface was missed during audit and its absence blocks a decision
- An audit verdict turns out to be wrong under deeper analysis (e.g., something marked `keep` cannot actually be kept without structural change)
- The strategy decision (in-place vs. clean-room vs. hybrid vs. new-build) proves wrong given what design has revealed
- The product boundary or goals must change based on design discoveries — the agent MUST surface this to the user first and MUST NOT silently redefine product scope
