<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/identifiers
title: Labeled Artifact Identifiers
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
  - playbooks/glossary.md
  - playbooks/principles.md
supersedes: null
---

# Labeled Artifact Identifiers

This file defines every labeled artifact family the framework uses. Every significant artifact MUST carry a stable, greppable, never-reused identifier from one of the families below. Labels enable mechanical traceability — a reviewer can grep "what decision does FR-7 trace to?" or "what code implements SC-3?" without reading prose.

This file is referenced from every playbook that produces labeled artifacts. The rules defined here are normative; the playbooks MUST conform to them.

> **Terminology.** See [`glossary.md`](./glossary.md) for **artifact**, **contract**, **spec**, **gap**, **significant decision**.

## Playbook Naming Convention

Files under `playbooks/` follow one of two naming patterns. The pattern is normative — adding a new playbook MUST use the form that matches its role.

- **Numbered phase playbooks** — `NN-name.md` where `NN ∈ {00, 01, 02, 03}`. These are the four sequential phase playbooks loaded by `AGENTS.md` Session Start Protocol step 5 based on the current phase recorded in `phase.md`. The numeric prefix preserves ordering in directory listings and signals "load me when in phase NN". The current set is fixed: `00-audit.md`, `01-design.md`, `02-spec.md`, `03-implement.md`. Adding a new phase to the framework would add a new numbered playbook and is a MAJOR amendment per `CHANGELOG.md` Versioning Policy.
- **Unnumbered cross-phase playbooks** — `name.md` with no prefix. These are reference and rule playbooks that apply across phases or in well-defined sub-contexts: `principles.md` (Tier 0, always loaded) + its two tier splits `principles-gates.md` (Tier 1, loaded before each phase gate, at amendments, or on scope-classification change) and `principles-conditional.md` (Tier 2, loaded when a triggering condition fires per `AGENTS.md` Session Start Protocol step 4b); `standards.md` (loaded when evaluating, specifying, or producing code); `glossary.md` / `identifiers.md` / `gaps.md` / `failure-patterns.md` (consulted by reference); `automation.md` / `zen.md` (always available; loaded as needed); `security-threat-model.md` (loaded when D-5 applicability fires — project handles credentials, PII, or LLM inference); and `release-readiness.md` (loaded as a sub-flow of `03-implement.md` Pre-Release Gate). Adding a new cross-phase playbook is typically a MINOR amendment.

When adding a new playbook, the author MUST decide: does this rule set govern one specific phase end-to-end (numbered) or does it apply across phases or as a sub-flow (unnumbered)? The first new playbook in either category MUST update this section to enumerate it.

## Label Families

Seven families plus one transient marker:

| Family | Name | Lives in | Scope | Format |
|---|---|---|---|---|
| **D-{n}** | Decisions | `decisions.md`, commit trailers | Global per project | Monotonic integer; `D-1`..`D-12` reserved for Required Decisions, `D-13`+ for project-specific |
| **G-{n}** | Gaps | `gaps.md`, `gaps-archive.md`, commit trailers | Global per project | Monotonic integer |
| **FR-{n}** | Functional requirements | spec `Contract` sections | Per spec file | Monotonic integer within spec |
| **NFR-{n}** | Non-functional requirements | spec `Contract` sections | Per spec file | Monotonic integer within spec, independent of FR |
| **SC-{n}** | Success criteria (testable, binary) | `audit.md` Product surface + spec `Conformance criteria` | Per spec file (mirrored in audit for product-level) | Monotonic integer within spec |
| **NG-{n}** | Non-Goals (explicitly out of scope) | `audit.md` Product surface + spec `Scope` section | Per spec file (mirrored in audit for product-level) | Monotonic integer within spec |
| **L-{n}** | Lessons | `.agent-state/lessons.md`, session log Lessons Learned column | Global per project | Monotonic integer |
| `[NEEDS CLARIFICATION: ...]` | Transient marker | any in-progress document | (transient) | Prose, no integer |

## Per-Family Rules

### D-{n} — Decisions

- **Reserved range:** `D-1` through `D-12` are reserved for the Required Decisions enumerated in `01-design.md`. These slots MUST be filled (with either a decision in `Accepted` or `Final` state, or an explicit `not-applicable` justification) before the Design Closure Gate passes.
- **Project range:** `D-13` and above are project-specific decisions added as the project demands.
- **Monotonic:** IDs MUST be assigned in order of creation and MUST NOT be reused. When an `Accepted` or `Final` decision is revised, the original ID remains with `Status: Superseded (by D-{new})`; the replacement receives a new ID, goes through the normal `Draft` → `Proposed` → `Accepted` → `Final` lifecycle, and populates its `Supersedes:` field with the old ID. See `01-design.md` Decision Entry Format and Decision Lifecycle.
- **Supersession is two-way:** every supersede creates a **backward mark** on the old entry (`Status: Superseded (by D-{new})`) AND a **forward reference** on the new entry (`Supersedes: D-{old}`). Both fields MUST be populated in the same change set — a one-sided supersede is incomplete and MUST fail the Phase 1 gate's mechanical check. The old entry retains its ID in place; the new entry gets a fresh monotonic ID and enters the lifecycle at `Draft`. Future readers use the forward reference to trace "what replaced this" and the backward mark to trace "what this replaced"; neither direction is optional.
- **Stability:** once a decision ID has been referenced anywhere (another decision, a spec, a commit trailer, a code comment), it MUST NOT be renumbered.
- **Grep pattern:** `\bD-\d+\b`.
- **Lookup:** `grep -n '^### D-{n}:' .agent-state/decisions.md .agent-state/decisions-archive.md`.

### G-{n} — Gaps

- **Monotonic:** IDs MUST be assigned in order across the entire project lifetime and MUST NOT be reused after resolution. A resolved gap retains its ID for historical traceability even after archival.
- **Archival:** per `principles.md` Required Behaviors #6 (state-file hygiene), resolved gaps are archived to `gaps-archive.md` when the active file exceeds 300 lines. Archive entries retain their original ID.
- **Grep pattern:** `\bG-\d+\b`.
- **Lookup:** `grep -n '^### G-{n}:' .agent-state/gaps.md .agent-state/gaps-archive.md`.

### FR-{n} — Functional requirements

- **Per-spec scope:** FR IDs are scoped to each spec file. `FR-1` in `specs/user-auth.md` is a different requirement from `FR-1` in `specs/billing.md`.
- **Monotonic within a spec:** MUST be assigned in order within the spec's `Contract` section. MUST NOT be reused within the same spec.
- **One behavior per label:** each FR describes exactly one behavior. Complex behaviors MUST be decomposed into several FR labels rather than bundling into one label.
- **Significance threshold:** FR labels are REQUIRED for significant requirements only (same threshold as `principles.md` Quality Seeking — a requirement is significant if it would affect more than one file OR if a reasonable implementer could disagree on its meaning). Trivial inline prose MAY remain unlabeled.
- **Cross-file reference form:** when referencing an FR from outside its owning spec, the reference MUST qualify with the file path: `specs/user-auth.md:FR-7`, not bare `FR-7`.
- **Grep pattern (unqualified):** `\bFR-\d+\b`.

### NFR-{n} — Non-functional requirements

- Same rules as FR, applied to non-functional concerns: performance targets, availability, latency budgets, security posture, resource limits, observability, and accessibility targets.
- NFR IDs are **independent of FR IDs** within the same spec — a spec may have `FR-1`..`FR-7` and `NFR-1`..`NFR-3` simultaneously, and the numbers do not interleave.
- **Grep pattern:** `\bNFR-\d+\b`.

### SC-{n} — Success criteria

- **Testable and binary:** every SC MUST resolve to a pass/fail answer by a specific test, fixture, or auditable check. Vague aspirations such as "the system SHOULD feel responsive" are NOT valid SCs. "99% of user-facing operations complete within 200ms at steady-state load" IS a valid SC.
- **Two homes:** SCs are captured in `audit.md` Product surface (stakeholder-facing success conditions, product-level) and mirrored in each spec's `Conformance criteria` section (tied to specific fixtures, test vectors, or auditable checks).
- **Cross-reference to FR/NFR:** every SC entry in a spec's Conformance section MUST reference the `FR-{n}` or `NFR-{n}` it validates. Format: `SC-3: validates FR-7, FR-9 — {concrete criterion}`.
- **Grep pattern:** `\bSC-\d+\b`.

### NG-{n} — Non-Goals

- **Explicitly out of scope:** NG labels enumerate what the system deliberately does NOT do. They exist to prevent silent scope creep during implementation by making the negative space of the product explicit.
- **Two homes:** NGs are captured in `audit.md` Product surface (product-level exclusions) and mirrored in each spec's `Scope` section (spec-level exclusions).
- **Empty section forbidden:** every spec MUST have a non-empty `Non-Goals` section. If the spec has no exclusions, the author MUST write `NG-none: no explicit exclusions for this spec — {one-sentence justification why exclusions do not apply}`. The agent MUST NOT leave the section empty or omit it.
- **Grep pattern:** `\bNG-\d+\b` (or `NG-none`).

### L-{n} — Lessons

- **Monotonic:** IDs MUST be assigned in order of consolidation across the entire project lifetime and MUST NOT be reused. Lessons are aggregated from the session log Lessons Learned column into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8 and `03-implement.md` Post-Completion Housekeeping.
- **Lifecycle:** session log entries (informal prose) → consolidation (assigned an `L-{n}` ID, categorized per the schema in `.agent-state/lessons.md`) → cross-project promotion (when the same lesson appears in this project AND ≥ 1 prior project's `lessons.md`, the lesson is moved to the Candidate Patterns section and a `framework` gap entry is drafted per the Amendment Protocol in `AGENTS.md`).
- **Cross-project:** lessons are the framework's longitudinal memory — recurring `L-{n}` patterns across projects are the primary input to framework amendment proposals.
- **No commit trailer:** unlike `D-`, `FR-`, `SC-`, and `G-`, lessons are aggregated post-hoc from session logs and do NOT have a commit trailer form. A commit MUST NOT cite an `L-{n}` ID; the lesson is the *outcome* of work, not the work itself.
- **Grep pattern:** `\bL-\d+\b`.
- **Lookup:** `grep -n '^### L-{n}:' .agent-state/lessons.md`.

### `[NEEDS CLARIFICATION: ...]` — Transient marker

- **Purpose:** a greppable in-document marker for an unresolved question that does NOT yet warrant a `gaps.md` entry — typically a clarification the author wants to raise during review of the same document.
- **Form:** real markers use `[NEEDS CLARIFICATION: {specific question}]` with a concrete question after the colon. Meta-references in governance documentation (this file, playbooks, and schemas) describing the marker MUST be wrapped in markdown backticks — `` `[NEEDS CLARIFICATION: ...]` `` — so they are excluded from the mechanical check.
- **Transient by design:** real markers MUST NOT persist past the phase gate of the document they appear in. Phase gates fail mechanically if any real markers remain in authored artifacts.
- **Conversion to gaps:** if a marker cannot be resolved within the current document before its phase gate, the author MUST convert it to a gap entry in `gaps.md` and remove the marker from the document.
- **Mechanical check:** every phase gate MUST include a grep verification scoped to authored project documents only (specs, audit entries, decisions, in-progress gap entries). The playbook directory is excluded — meta-references in governance text are allowed and expected. Canonical check:
  ```
  grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md
  ```
  This check is a `[M]` (mechanical) item and MUST return zero hits before the gate passes. A hook or CI script SHOULD run it automatically.
- **Grep pattern (canonical for the check):** `\[NEEDS CLARIFICATION:` (colon required — matches real markers, not bare-word documentation mentions).

## Commit Trailer Forms

Per `03-implement.md` Traceability, commit trailers MAY combine label families. All of the following are valid:

```
Implements: D-3
Implements: D-3, D-7
Implements: D-3, FR-7
Implements: D-3
Implements: D-7
Covers: SC-3
Closes: G-12
```

Rules:

- `Implements:` trailers cite the **decision(s) and/or functional requirement(s)** the commit realizes. MUST reference at least one `D-{n}` when the project has formal decisions (all scopes except micro).
- `Covers:` trailers cite the **success criterion or functional requirement** the commit adds test coverage for. OPTIONAL at the commit level — the `Covers:` relationship MAY also be expressed at the test level (test-name suffix `test_foo_covers_SC_3` or in-file comment `// Covers: SC-3` as the first line of the test body). The Phase 3 gate's test-traceability check accepts all three forms; see `03-implement.md` Traceability → Test traceability for the complete rule and the `grep` check.
- `Closes:` trailers cite the **gap** the commit resolves. OPTIONAL; use when the commit is specifically the resolution of a tracked gap.
- Multiple trailer types MAY coexist in one commit message. Multiple IDs within the same trailer MAY be comma-separated on one line OR split across repeated trailer lines (both forms are valid).

A complete commit message combining all four trailer types looks like:

```
feat(auth): add OAuth2 authorization code flow with PKCE

Implements the authorization code grant per RFC 6749 §4.1 with PKCE
(RFC 7636) for public clients. Adds the token endpoint, authorization
endpoint, and the PKCE verifier/challenge derivation.

Implements: D-5, FR-7
Implements: NFR-3
Covers: SC-2
Closes: G-18
```

In this example, `D-5` is the authentication architecture decision, `FR-7` is the functional requirement for the authorization flow in `specs/auth.md`, `NFR-3` is the non-functional requirement for PKCE support, `SC-2` is the success criterion for OAuth2 conformance, and `G-18` is a previously-tracked gap about the missing authorization endpoint. The commit cites all four in one message because the change realizes the decision, implements specific requirements, adds test coverage for a success criterion, and closes a tracked gap simultaneously.

Exceptions for commits that do not cite decisions are limited to maintenance changes (`chore(...)` per `standards.md` Git Conventions) and micro-scope projects (see `00-audit.md` Project Scope Classification).

## ID Collision Rules

- **Global families (D-, G-):** one counter per family, per project. No collisions possible within a family.
- **Per-spec families (FR-, NFR-, SC-, NG-):** scoped per spec file. Two different spec files MAY both contain `FR-1`, but each `FR-1` refers to the requirement in its own file. When cross-referencing these labels from outside their owning spec, the reference MUST qualify with the file path (e.g., `specs/user-auth.md:FR-7`).
- **Cross-family uniqueness:** D-, G-, FR-, NFR-, SC-, NG-, L- are distinct families. `D-1` and `FR-1` are always different artifacts.

## Per-Gate Mechanical Checks

Every phase gate MUST include the following mechanical `[M]` checks related to labels:

- `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits (markers allowed in governance docs; forbidden in authored artifacts once a gate is approached)
- For Phase 1 (Design): `grep -c '^### D-' .agent-state/decisions.md` MUST be at least the number of Required Decisions applicable to the scope
- For Phase 2 (Spec): for each spec file, `grep -cE '\bFR-\d+\b' specs/<spec>.md` MUST be non-zero (or the spec MUST declare `FR-none` in its Contract section with justification)
- For Phase 2 (Spec): for each spec file, `grep -cE '\bNG-\d+\b|NG-none' specs/<spec>.md` MUST be non-zero
- For Phase 3 (Implement): `grep -nE '^(Implements|Covers|Closes): (D|FR|SC|G)-' <commit-message>` MUST match every non-maintenance commit

These checks are automatable via hooks, CI scripts, or the `/verify` skill defined in `harness/claude-code/skills/verify/SKILL.md`.
