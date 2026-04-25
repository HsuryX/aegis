<!--
SYNC-IMPACT
- version: 1.0.0 → 1.1.0
- bump: MINOR
- date: 2026-04-25
- rationale: Framework refinement release. Adds the bounded-change 0 -> 3 path for already-governed work (`00-audit.md`); the harness security-claim model with explicit control-class (`Executable` / `Backstop` / `Advisory`) and activation-state (`Active now` / `Shipped but inactive` / `Not available here`) classification (`harness/capability-matrix.md`); the Canonical Dependency Edges DAG seeding the Whole-System Composition Check (`01-design.md`); the Adversarial Review Protocol Per-phase timing-hooks table (`principles-gates.md`); the Scope-Proportional gate-protocol mini-matrix (`principles-gates.md` Scope-Proportional Ceremony); the `phase regression` glossary entry; and `validate.py check_traceability` — a file-level `Implements:`/`Covers:` rollup (warning-only, vacuous on the framework repo itself). Extends Required Behaviors #7 with an archive-decay re-evaluation rule for consulted archive entries >= 12 months old (`principles.md`). Expands the existing Cold Read perspective with a concrete protocol (`principles-gates.md`). Adds a date-only UTC variant to the scope-reduction sign-off format for `micro`/`small` projects (`00-audit.md` ceremony matrix + `release-readiness.md` checklist); the full git-email anchored form remains for `standard`/`large`. Relaxes Session Start Protocol Step 3 — the integrity block now accepts any form that cites countable or tool-checkable evidence; the prior templated form is preserved as a reference example. Promotes the implementation-boundary rule to a dedicated `## Implementation Boundary` section in `AGENTS.md` (v1.0.0 carried the rule as a paragraph below the Phase Gates table); the new section's bounded-change summary paragraph points at `00-audit.md` for the full Bounded-Change Rule; surfaces additional Phase 1 gate items (Authority model, Whole-System Composition Check, threat-model applicability) and Phase 2 Proof-class declaration in the `AGENTS.md` Phase Gates table; decouples the Phase 1 threat-model gate from `specs/threat-model.md` artifact-existence (binds to whichever path D-5 declares); reformats the `AGENTS.md` Workspace Discipline second paragraph from a single run-on into a 6-bullet list (preserving v1.0.0 content and adding a Bash-subprocess-gap caveat); trims the scope-reduction marker phrase list (`validate.py` `_DEFERRAL_PHRASES`, mirrored in `standards.md` / `03-implement.md` / `harness/cursor/.cursor/rules/phase-3.mdc`) to unambiguous multi-word forms only, dropping false-positive-prone tokens. De-duplicates the Verdict Discipline definition (`AGENTS.md` is sole canonical owner; glossary holds a one-paragraph redirect); removes the four per-phase `## Adversarial Gate Check` stanzas (replaced by the new Per-phase timing-hooks table); removes the redundant placeholder grep at `02-spec.md` Quality Checks (the Phase Gate scan is a strict superset). Compresses Codex and Cursor harness READMEs by deferring universal-backstop guidance to `harness/capability-matrix.md`. Required Behaviors #8 grep formula relocates from `principles.md` body to `automation.md` Lessons-Gap Backstop. Removes the `validate.py` Verification Coverage Matrix anchor-diversity check; its enforcement contract is already covered by check 7 (evidence verifiability). SemVer MINOR — additive and refinement; no rule becomes stricter than v1.0.0 in a way that invalidates prior compliance.
- downstream_review_required:
  - README.md
  - ONBOARDING.md
  - CHANGELOG.md
  - harness/capability-matrix.md
  - harness/claude-code/README.md
  - harness/codex/README.md
  - harness/cursor/README.md
  - harness/ci/README.md
  - harness/claude-code/hooks-cookbook.md
  - harness/claude-code/skills/phase-status/SKILL.md
  - validate.py
  - tools/bootstrap.sh
-->
---
id: playbooks/02-spec
title: Phase 2: Spec
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 2-spec
severity: normative
mechanical_items: 9
judgment_items: 12
mixed_items: 1
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

The agent MUST draft canonical specifications describing the current intended system state for the active cycle. Not migration plans. Not history. Not roadmap. The contract in force.

## Spec Location and Format

Specifications MUST live in the location and format decided by D-12 (Documentation structure). If D-12 has not prescribed a specific structure, the default is a `specs/` directory in the project root with one markdown file per public contract. For machine-readable contracts (APIs, schemas, wire formats), the agent MUST use the canonical format for the technology (e.g., OpenAPI for REST APIs, protobuf for RPC, JSON Schema for data validation) alongside a markdown companion that covers the non-machine-readable sections below.

## Spec Rules

1. **Current canonical system only** — specs MUST NOT use "currently X, will become Y" language
2. **Decision-traced** — every spec section MUST trace to a decision in `decisions.md`
3. **Unambiguous** — if a behavior can be interpreted two ways, the spec is incomplete and MUST be tightened
4. **Written fresh** — the agent MUST NOT edit copies of existing documentation; the agent MUST write from the decided design
5. **Test-derivable** — conformance criteria MUST be concrete enough to produce specific test cases with expected inputs and outputs
6. **No production code** — conformance examples MUST use pseudocode, test vectors, or input/output pairs, NOT implementation-ready code

## Spec Section Structure

Ordered from context to substance to cross-cutting concerns. Labeled artifacts follow the rules in [`identifiers.md`](./identifiers.md):

- **Scope** — what this spec covers, what it excludes, and the interface's trust-boundary class. Spec-local exclusions MUST be written as plain prose or qualified references to `audit.md:NG-{n}` product non-goals where appropriate. Specs MUST NOT mint new canonical `NG-{n}` labels; product non-goals live in the Product surface of `audit.md`. The Scope section MUST declare the interface's trust-boundary class: cross-trust-boundary (public API, third-party webhook, user input) OR internal-only (private function, internal queue). Internal-only interfaces MAY record `schema: N/A — internal only` and skip the Machine-readable Contract subsection below.
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

**Tally:** 5 `[M]` · 1 `[M+J]` · 10 `[J]`.

**`[J]` evidence-location discipline.** Judgment checks here use the canonical verification/evidence contract from `principles-gates.md` (Verification Coverage Matrix → Evidence verifiability). Record verifiable references in the session log or `.agent-state/reviews/`; bare checkmarks and prose-only citations are not sufficient. For `micro` or `small` scope projects, author self-review still requires those evidence references.

- [ ] **[J]** Specs MUST NOT contradict other specifications
- [ ] **[J]** Error semantics MUST cover all failure modes, not just the happy path
- [ ] **[J]** Conformance criteria MUST be concrete enough to write tests from, not vague aspirations
- [ ] **[M]** Each critical behavior MUST have a declared proof class. Mechanical: `grep -cE '^\*\*Proof class:\*\*' specs/<spec>.md` MUST be non-zero.
- [ ] **[M]** No `[NEEDS CLARIFICATION: ...]` markers MAY remain in the spec. Mechanical: `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits. This is the canonical scope defined in [`identifiers.md`](./identifiers.md) — playbook files are intentionally excluded because they document the marker convention itself.
- [ ] **[M]** Every significant behavior in the Contract section MUST carry an `FR-{n}` or `NFR-{n}` label per [`identifiers.md`](./identifiers.md); trivial inline prose MAY remain unlabeled. Mechanical: `grep -cE '\b(FR|NFR)-\d+\b' specs/<spec>.md` MUST be non-zero (or the spec MUST declare `FR-none` with justification).
- [ ] **[M+J]** Every conformance criterion MUST carry an `SC-{n}` label and MUST reference the `FR-` or `NFR-` it validates. Mechanical: every `SC-\d+:` line MUST contain an `FR-` or `NFR-` reference on the same line. Judgment: the cross-reference MUST be correct (the cited FR/NFR is actually what the SC validates).
- [ ] **[M]** Specs MUST NOT define spec-local `NG-{n}` / `NG-none` labels. Mechanical: `grep -nE '^\s*([-*+]\s*)?NG-(\d+|none):' specs/<spec>.md` MUST return zero; qualified references such as `audit.md:NG-1` are permitted.
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

## Phase Gate

Apply the shared gate procedure from `AGENTS.md` Phase Gates and `principles-gates.md` (Gate Outcome Vocabulary, Three-Tier Gate Criteria, Multi-Perspective Verification, Verification Coverage Matrix). Run the Adversarial Review Protocol per its Per-phase timing hooks table in `principles-gates.md` before scoring this checklist. This checklist records the Phase 2-specific criteria only.

**Tally:** 3 `[M]` · 0 `[M+J]` · 3 `[J]`. **Tiers:** 6 `[must-meet]` · 0 `[should-meet]` · 0 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** All public contracts MUST have specifications. Mechanical: every public contract identified during Phase 0 audit MUST have a corresponding file under `specs/`.
- [ ] **[J]** **[must-meet]** All specifications MUST pass the quality checks above (delegates to the Quality Checks section above)
- [ ] **[M]** **[must-meet]** Specification review MUST be completed (separate-agent review for standard/large scope; self-review for micro/small). Mechanical: a review outcome is recorded in the session log in `phase.md`.
- [ ] **[J]** **[must-meet]** Specifications MUST be cross-referenced and mutually consistent
- [ ] **[J]** **[must-meet]** Conformance criteria MUST cover all critical behaviors with declared proof classes
- [ ] **[M]** **[must-meet]** No stale placeholders in authored artifacts. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b|\((forthcoming|pending)\)' .agent-state/decisions.md specs/` MUST return zero hits.

## Terminal Phase (Spec-Only Projects)

For projects where Phase 2 is the terminal phase (specification-only repositories, governance documents, as declared in `phase.md`), the Phase Gate above doubles as the terminal completion gate for the lifecycle mode recorded in `phase.md`. When all gate criteria pass, the agent MUST:

1. Mark Phase 2 status as `completed` in `phase.md`
2. Mark Phase 3 as `not-applicable` in `phase.md`
3. Run Multi-Perspective Verification from `principles-gates.md` as the final quality check
4. If `Lifecycle mode` is `finite-delivery`, record project completion in the session log
5. If `Lifecycle mode` is `steady-state`, record cycle completion in the session log and note that the next material work item MUST restart at Phase 0 rather than reopening Phase 2 directly
