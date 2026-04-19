<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/02-spec
title: Phase 2: Spec
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: 2-spec
severity: normative
mechanical_items: 11
judgment_items: 12
mixed_items: 2
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/identifiers.md
  - playbooks/standards.md
  - playbooks/01-design.md
  - playbooks/03-implement.md
supersedes: null
---

# Phase 2: Spec

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **canonical**, **contract**, **review**, **spec**, **trust boundary**, **verify**. "Contract" means a single section of a specification (one interface's invariants), not the whole spec document — see the glossary.

## Objective

The agent MUST draft canonical specifications describing the steady-state final system. Not migration plans. Not history. Not roadmap. The final contract.

## Spec Location and Format

Specifications MUST live in the location and format decided by D-12 (Documentation structure). If D-12 has not prescribed a specific structure, the default is a `specs/` directory in the project root with one markdown file per public contract. For machine-readable contracts (APIs, schemas, wire formats), the agent MUST use the canonical format for the technology (e.g., OpenAPI for REST APIs, protobuf for RPC, JSON Schema for data validation) alongside a markdown companion that covers the non-machine-readable sections below.

## Spec Rules

1. **Final system only** — specs MUST NOT use "currently X, will become Y" language
2. **Decision-traced** — every spec section MUST trace to a decision in `decisions.md`
3. **Unambiguous** — if a behavior can be interpreted two ways, the spec is incomplete and MUST be tightened
4. **Written fresh** — the agent MUST NOT edit copies of existing documentation; the agent MUST write from the decided design
5. **Test-derivable** — conformance criteria MUST be concrete enough to produce specific test cases with expected inputs and outputs
6. **No production code** — conformance examples MUST use pseudocode, test vectors, or input/output pairs, NOT implementation-ready code

## Spec Section Structure

Ordered from context to substance to cross-cutting concerns. Labeled artifacts follow the rules in [`identifiers.md`](./identifiers.md):

- **Scope** — what this spec covers, and what it excludes. Exclusions MUST be enumerated as `NG-{n}` Non-Goal labels (see `identifiers.md`). The Non-Goals section MUST NOT be empty — if no exclusions apply, the author MUST write `NG-none: {one-sentence justification}`. The Scope section MUST also declare the interface's trust-boundary class: cross-trust-boundary (public API, third-party webhook, user input) OR internal-only (private function, internal queue). Internal-only interfaces MAY record `schema: N/A — internal only` and skip the Machine-readable Contract subsection below.
- **Definitions** — canonical terms used (referencing the naming table)
- **Contract** — the specification itself: formats, behaviors, invariants, constraints. Every significant behavior MUST carry an `FR-{n}` (functional) or `NFR-{n}` (non-functional) label. Trivial inline prose MAY remain unlabeled.
- **Machine-readable Contract** — REQUIRED for every spec whose Scope section declares a cross-trust-boundary interface. The machine-readable artifact MUST be one of the canonical forms enumerated in `standards.md` Contract Formats (that subsection is the sole canonical list; this playbook intentionally does not re-enumerate it). The artifact MUST be checked into `specs/schemas/{spec-name}.{ext}` (unless D-13+ Contract Format specifies otherwise) and this subsection MUST contain a one-line pointer: `**schema:** specs/schemas/bookmarks-api.openapi.yaml` (or equivalent). Each `FR-{n}` / `NFR-{n}` that corresponds to a field, endpoint, or validation rule in the machine-readable artifact MUST include a trailing pointer: `(schema: path#/component/ref)`. The prose Contract above is authoritative for intent; the machine-readable contract is authoritative for format. A conflict between the two MUST halt the Phase 2 gate.
- **Error semantics** — what failures look like, what guarantees hold during failure, how clients should handle errors
- **Security considerations** — applicable trust, validation, and capability rules
- **Conformance criteria** — verifiable conditions that determine compliance. Every criterion MUST carry an `SC-{n}` label and MUST reference the `FR-{n}` or `NFR-{n}` it validates (format: `SC-3: validates FR-7, FR-9 — {concrete criterion}`). Each criterion MUST include concrete examples with specific inputs and expected outputs.

## Conformance Proof

Each critical specification MUST declare its proof class:
- **Machine-checked** — automated tests verify compliance
- **Fixture-backed** — test vectors or reference data verify compliance
- **Human-audited** — explicit review process with stated criteria and reviewer qualifications

The agent MUST NOT accept self-certifying claims, hardcoded success assertions, or empty evidence artifacts as proof. For spec-only projects (Phase 2 terminal), machine-checked proof REQUIRES test vectors or reference implementations provided as specification artifacts, not production code — the agent MUST declare the proof class as fixture-backed if executable verification is not feasible within the spec phase.

## Completeness Mandate

Specifications MUST cover ALL paths, not just the happy path. Each item below MUST have specification coverage or MUST be explicitly declared out of scope with justification:

- Every error condition in the error and recovery model
- Every input variation at system boundaries (including malformed, empty, oversized, adversarial, and timeout/resource exhaustion scenarios)
- Every state transition, including transitions under concurrent access
- Edge cases identified during audit

A specification that covers only the common case is incomplete. The agent MUST NOT advance to implementation with incomplete specifications. The cost of discovering unspecified behavior during implementation is far higher than the cost of specifying it now.

## Excluded from Specs

These MUST NOT appear in canonical specifications — they belong elsewhere:
- Migration plans or transition notes
- Historical context or rationale (→ `decisions.md`)
- Implementation guidance (→ developer documentation or code comments)
- Rejected alternatives (→ `decisions.md`)
- Progress tracking or roadmap items
- Tutorials, how-to guides, or onboarding material (→ developer documentation)

## Quality Checks

Ordered by severity: correctness → testability → completeness → consistency → readability. Every check MUST pass before advancing. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**Tally:** 6 `[M]` · 1 `[M+J]` · 10 `[J]`.

**`[J]` evidence-location discipline.** Every `[J]` item checked off in a Specification Review MUST be accompanied — in the session log or the Adversarial Review archive at `.agent-state/reviews/` — by a citation of the form `passed — verified via {file:line | subagent:name | tool_output_ref}`. A bare checkmark without a citation is self-attestation and is NOT sufficient per `principles-gates.md` Adversarial Review Protocol `[J]` disposition classes. The evidence-location format makes a `[J]` check falsifiable by a later reviewer; checkmark-only dispositions hide the judgment behind opaque prose. Exception: for `micro` or `small` scope projects, author self-review suffices, but the self-review MUST still cite evidence locations — the checklist is a tool for the author's own discipline, not a ceremony to complete.

- [ ] **[J]** Specs MUST NOT contradict other specifications
- [ ] **[J]** Error semantics MUST cover all failure modes, not just the happy path
- [ ] **[J]** Conformance criteria MUST be concrete enough to write tests from, not vague aspirations
- [ ] **[M]** Each critical behavior MUST have a declared proof class. Mechanical: `grep -cE '^\*\*Proof class:\*\*' specs/<spec>.md` MUST be non-zero.
- [ ] **[M]** No unresolved placeholders (TBD, TODO) MAY remain in critical paths. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b' specs/` MUST return zero hits.
- [ ] **[M]** No `[NEEDS CLARIFICATION: ...]` markers MAY remain in the spec. Mechanical: `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits. This is the canonical scope defined in [`identifiers.md`](./identifiers.md) — playbook files are intentionally excluded because they document the marker convention itself.
- [ ] **[M]** Every significant behavior in the Contract section MUST carry an `FR-{n}` or `NFR-{n}` label per [`identifiers.md`](./identifiers.md); trivial inline prose MAY remain unlabeled. Mechanical: `grep -cE '\b(FR|NFR)-\d+\b' specs/<spec>.md` MUST be non-zero (or the spec MUST declare `FR-none` with justification).
- [ ] **[M+J]** Every conformance criterion MUST carry an `SC-{n}` label and MUST reference the `FR-` or `NFR-` it validates. Mechanical: every `SC-\d+:` line MUST contain an `FR-` or `NFR-` reference on the same line. Judgment: the cross-reference MUST be correct (the cited FR/NFR is actually what the SC validates).
- [ ] **[M]** The Non-Goals section MUST NOT be empty — every exclusion MUST carry an `NG-{n}` label, or the section MUST declare `NG-none` with justification. Mechanical: `grep -cE '\bNG-(\d+|none)\b' specs/<spec>.md` MUST be non-zero.
- [ ] **[J]** Factual claims (API signatures, library behaviors, file paths, function names, data formats, configuration options) MUST be verified using tools (grep, LSP, documentation lookup, package registry) — LLM memory alone is not evidence. When review is delegated to a subagent, the reviewer MUST have tool access and MUST use it for factual verification
- [ ] **[J]** Each specification's behaviors MUST align bidirectionally with its traced decisions — no behaviors beyond what decisions require (scope creep), no decided behaviors omitted (scope reduction). The agent MUST compare the spec's Contract and Conformance criteria against the decision's substance
- [ ] **[M]** Every MUST / SHOULD / MAY sentence in the Contract section MUST cite an `FR-{n}` or `NFR-{n}` label (or be explicitly demoted to non-normative prose — the explicit demotion is itself a scope statement). Orphan normatives in the Contract section are spec creep indicators (behavior is being specified without a corresponding requirement anchor). Mechanical: `awk '/^## Contract/,/^## [^#]/' specs/<spec>.md | grep -E '\b(MUST|SHOULD|MAY)\b' | grep -vE '\b(FR|NFR)-[0-9]+\b'` MUST return zero hits unless the line is inside a demoted-prose paragraph annotated `<!-- non-normative -->`.
- [ ] **[M]** When the spec's Scope declares a cross-trust-boundary interface, the Machine-readable Contract subsection MUST be non-empty. Mechanical: `grep -cE '^\*\*schema:\*\*' specs/<spec>.md` MUST return ≥ 1 for every cross-trust-boundary spec. Internal-only specs MUST explicitly record `**schema:** N/A — internal only` with justification; a missing schema subsection is a spec-completeness failure.
- [ ] **[J]** Every term MUST match the canonical naming table exactly
- [ ] **[J]** Concurrent access behavior MUST be specified for all shared mutable state (or declared out of scope with justification)
- [ ] **[J]** A reader with no project history MUST be able to understand the spec fully
- [ ] **[J]** Multi-Perspective Verification MUST produce clean results from every perspective listed in `principles-gates.md` Multi-Perspective Verification

## Specification Review

Specifications are more consequential than code — a wrong spec produces systematically wrong implementation. After quality checks pass, the agent MUST request a review from a separate agent in a fresh context (mirroring the Code Review protocol in `03-implement.md`):

1. **Reviewer receives:** (a) the specification under review, (b) the decision ID(s) it traces to with the full text of each decision's Context, Decision, and Alternatives considered sections (not just the IDs), (c) the relevant audit surface entries, and (d) the quality checks above. The reviewer MAY request additional context for specific ambiguities encountered during review — the agent MUST provide the requested context as a targeted excerpt, not the whole project. The reviewer MUST NOT receive: an implementation plan, unrelated specifications, the main session's context, or any code. The reviewer MUST operate in a fresh context with only the items listed above
2. **Review focus:** ambiguities that allow two different implementations, contradictions with other specs, unstated assumptions, conformance criteria that do not actually test the stated behavior, and scope drift from the traced decisions
3. **Review outcomes:**
   - `approve` — specification is ready for the Phase Gate
   - `request-changes` — the author MUST address feedback, re-run quality checks, and re-request review
   - `escalate` — a design gap was identified; the agent MUST return to Design phase
4. **Lightweight exception:** for micro and small scope projects (see `00-audit.md`), self-review against the quality checks suffices — the author MUST record the scope classification as justification

## Escalation Triggers

The agent MUST return to Design phase if:
- Writing a spec reveals that a design decision is ambiguous or contradictory
- Two specifications require incompatible behavior from the same subsystem
- A concept cannot be precisely specified with the current naming model
- Conformance criteria cannot be made concrete enough to test — indicating the design is underspecified

## Revision Impact Protocol

When a design decision is revised after specifications have been written:

1. Each specification MUST declare which decision ID(s) it derives from in its Scope section (enforced by the "Decision-traced" rule above)
2. When a decision is revised to a new ID (`D-{old}` → `D-{new}`), all specifications referencing the old ID MUST be marked **stale** via a gap entry
3. Stale specifications MUST be re-evaluated: either confirmed still valid under the new decision, revised to match, or deleted
4. Implementation against a stale specification is prohibited — the agent MUST treat it the same as implementing without a specification

## Adversarial Gate Check

Before evaluating the Phase Gate below, the agent MUST run an adversarial review subagent per `principles-gates.md` Adversarial Review Protocol. This review is distinct from the Specification Review above: Specification Review validates each spec's content fidelity against its traced decisions; adversarial review catches completeness gaps across all specs — unspecified error semantics, conformance criteria that don't actually test the stated behavior, `[NEEDS CLARIFICATION]` markers, Non-Goals that still say "TBD", `FR-{n}`/`NFR-{n}` without concrete thresholds, or `SC-{n}` that references `FR-{n}` but the FR itself is vague.

**Scope:** required for standard and large scope projects; optional for micro and small. **Input:** all spec files under `specs/`, the Quality Checks section above, and the relevant audit surface entries. **Output:** a list of `file:line` findings. The agent MUST address every finding before the Phase Gate evaluates. The adversarial review runs AFTER Specification Review and BEFORE the Phase Gate — spec fidelity is checked first (correctness), completeness is checked second.

## Phase Gate

Ordered by prerequisite progression: existence → individual quality → cross-spec consistency → testability → gap resolution. Every item MUST be satisfied before advancing. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**HALT AND REPORT.** Evaluate each item below against the Gate Outcome Vocabulary and Three-Tier Gate Criteria in `principles-gates.md`. Report the gate outcome (`Go`, `Conditional Go`, `Hold`, `Recycle`, or `Kill`) using the Completion Status Protocol — include evidence for each `[M]` item and a rendered judgment for each `[J]` item. For `Conditional Go`, record each unmet `[should-meet]` item as a `conditional` gap entry. For `Hold` or `Recycle`, list the specific `[must-meet]` items that fail.

**Tally:** 4 `[M]` · 1 `[M+J]` · 3 `[J]`. **Tiers:** 8 `[must-meet]` · 0 `[should-meet]` · 0 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** All public contracts MUST have specifications. Mechanical: every public contract identified during Phase 0 audit MUST have a corresponding file under `specs/`.
- [ ] **[J]** **[must-meet]** All specifications MUST pass the quality checks above (delegates to the Quality Checks section above)
- [ ] **[M]** **[must-meet]** Specification review MUST be completed (separate-agent review for standard/large scope; self-review for micro/small). Mechanical: a review outcome is recorded in the session log in `phase.md`.
- [ ] **[J]** **[must-meet]** Specifications MUST be cross-referenced and mutually consistent
- [ ] **[J]** **[must-meet]** Conformance criteria MUST cover all critical behaviors with declared proof classes
- [ ] **[M]** **[must-meet]** All CRITICAL gaps in `gaps.md` MUST be resolved (non-critical MAY remain tracked). Mechanical: same grep as Phase 1 — `grep -A1 '^### G-' .agent-state/gaps.md | grep -B1 'Severity:\*\* critical' | grep 'Status:\*\* open'` MUST return zero hits.
- [ ] **[M]** **[must-meet]** No stale placeholders in authored artifacts. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b|\((forthcoming|pending)\)' .agent-state/decisions.md specs/` MUST return zero hits.
- [ ] **[M+J]** **[must-meet]** Verification Coverage Matrix complete: all 5 perspectives exercised with clean results. Mechanical: the session log contains a filled matrix with no `no` or `findings` entries. Judgment: the evidence cited for each perspective is genuine. See `principles-gates.md` Verification Coverage Matrix.

## Terminal Phase (Spec-Only Projects)

For projects where Phase 2 is the terminal phase (specification-only repositories, governance documents, as declared in `phase.md`), the Phase Gate above doubles as the **Project Completion Gate**. When all gate criteria pass, the agent MUST:

1. Mark Phase 2 status as `completed` in `phase.md`
2. Mark Phase 3 as `not-applicable` in `phase.md`
3. Run Multi-Perspective Verification from `principles-gates.md` as the final quality check
4. Record project completion in the session log
