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
id: playbooks/identifiers
title: Labeled Artifact Identifiers
version: 1.1.0
last_reviewed: 2026-04-25
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

This file defines every labeled artifact family the framework uses. Every significant artifact MUST carry a stable, greppable, never-reused identifier from one of the families below. Labels enable mechanical traceability — a reviewer can grep "what decision does specs/auth.md:FR-7 trace to?" or "what code implements specs/auth.md:SC-3?" without reading prose.

This file is referenced from every playbook that produces labeled artifacts. The rules defined here are normative; the playbooks MUST conform to them.

> **Terminology.** See [`glossary.md`](./glossary.md) for **artifact**, **contract**, **spec**, **gap**, **significant decision**.

## Playbook Naming Convention

AGENTS.md is the thin operator kernel; files under `playbooks/` carry the doctrine it loads. They follow one of two naming patterns. The pattern is normative — adding a new playbook MUST use the form that matches its role.

- **Numbered phase playbooks** — `NN-name.md` where `NN ∈ {00, 01, 02, 03}`. These are the four sequential phase playbooks loaded by `AGENTS.md` Session Start Protocol step 6 based on the current phase recorded in `phase.md`. The numeric prefix preserves ordering in directory listings and signals "load me when in phase NN". The current set is fixed: `00-audit.md`, `01-design.md`, `02-spec.md`, `03-implement.md`. Adding a new phase to the framework would add a new numbered playbook and is a MAJOR amendment per `CHANGELOG.md` Versioning Policy.
- **Unnumbered cross-phase playbooks** — `name.md` with no prefix. These are doctrine and reference playbooks that apply across phases or in well-defined sub-contexts: `principles.md` (always-load doctrine), `principles-gates.md` (gate/amendment-scoped rigor loaded before each phase gate, at amendments, or on scope-classification change), and `principles-conditional.md` (triggered coordination/handoff/context-budget/spirit=letter rules loaded when a triggering condition fires per `AGENTS.md` Session Start Protocol); `standards.md` (loaded when evaluating, specifying, or producing code); `glossary.md` / `identifiers.md` / `gaps.md` / `failure-patterns.md` (consulted by reference); `automation.md` / `zen.md` (always available; loaded as needed); `security-threat-model.md` (loaded when D-5 applicability fires; see its Applicability section for the canonical four-condition trigger list); and `release-readiness.md` (loaded as a sub-flow of `03-implement.md` Pre-Release Gate). Adding a new cross-phase playbook is typically a MINOR amendment.

When adding a new playbook, the author MUST decide: does this rule set govern one specific phase end-to-end (numbered) or does it apply across phases or as a sub-flow (unnumbered)? The first new playbook in either category MUST update this section to enumerate it.

## Label Families

Eight families plus one transient marker:

| Family | Name | Lives in | Scope | Format |
|---|---|---|---|---|
| **D-{n}** | Decisions | `decisions.md`, commit trailers | Global per project | Monotonic integer; `D-1`..`D-12` reserved for Required Decisions, `D-13`+ for project-specific |
| **G-{n}** | Gaps | `gaps.md`, `gaps-archive.md`, commit trailers | Global per project | Monotonic integer |
| **FR-{n}** | Functional requirements | spec `Contract` sections | Per spec file | Monotonic integer within spec |
| **NFR-{n}** | Non-functional requirements | spec `Contract` sections | Per spec file | Monotonic integer within spec, independent of FR |
| **PSC-{n}** | Product success criteria (auditable, binary) | `audit.md` Product surface | Global per project | Monotonic integer |
| **SC-{n}** | Spec conformance criteria (testable, binary) | spec `Conformance criteria` | Per spec file | Monotonic integer within spec |
| **NG-{n}** | Product non-goals (explicitly out of scope) | `audit.md` Product surface | Global per project | Monotonic integer |
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

### PSC-{n} — Product success criteria

- **Product-surface only:** PSC labels live only in the Product surface of `audit.md`. They capture product-level success outcomes, not spec-local conformance checks.
- **Auditable and binary:** every PSC MUST resolve to a pass/fail answer by a specific test, audit, or release check. Vague aspirations such as "the system SHOULD feel responsive" are NOT valid PSCs. "99% of user-facing operations complete within 200ms at steady-state load" IS a valid PSC.
- **Global per project:** PSC IDs are monotonic across the project and MUST NOT be reused.
- **Distinct from SC:** a PSC MAY be realized by one or more spec `SC-{n}` entries, but the labels are not mirrored and do not share numbering semantics.
- **Grep pattern:** `\bPSC-\d+\b`.

### SC-{n} — Spec conformance criteria

- **Spec-only:** every SC lives in a spec's `Conformance criteria` section. SC labels are spec conformance criteria, not product-level success outcomes.
- **Testable and binary:** every SC MUST resolve to a pass/fail answer by a specific test, fixture, or auditable check.
- **Cross-reference to FR/NFR:** every SC entry in a spec's Conformance section MUST reference the `FR-{n}` or `NFR-{n}` it validates. Format: `SC-3: validates FR-7, FR-9 — {concrete criterion}`.
- **Per-spec scope:** SC IDs are scoped to each spec file. When referencing an SC from outside its owning spec, the reference MUST qualify with the file path: `specs/auth.md:SC-3`, not bare `SC-3`.
- **Grep pattern:** `\bSC-\d+\b`.

### NG-{n} — Non-Goals

- **Explicitly out of scope:** NG labels enumerate what the product deliberately does NOT do. They exist to prevent silent scope creep during implementation by making the negative space of the Product surface explicit.
- **Product-surface only:** NG labels live only in the Product surface of `audit.md` and are global across the project.
- **Specs may reference, not redefine:** a spec Scope section MAY cite applicable product non-goals via qualified references such as `audit.md:NG-2`, but specs MUST NOT mint bare `NG-{n}` labels or `NG-none`.
- **Global per project:** NG IDs are monotonic across the project and MUST NOT be reused.
- **Grep pattern:** `\bNG-\d+\b`.

### L-{n} — Lessons

- **Monotonic:** IDs MUST be assigned in order of consolidation across the entire project lifetime and MUST NOT be reused. Lessons are aggregated from the session log Lessons Learned column into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8 and `03-implement.md` Post-Completion Housekeeping.
- **Lifecycle:** session log entries (informal prose) → consolidation (assigned an `L-{n}` ID, categorized per the schema in `.agent-state/lessons.md`) → cross-project promotion (when the same lesson appears in this project AND ≥ 1 prior project's `lessons.md`, the lesson is moved to the Candidate Patterns section and a `framework` gap entry is drafted per the Amendment Protocol in `principles-gates.md`).
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
Implements: D-3, specs/auth.md:FR-7
Implements: specs/auth.md:NFR-3
Covers: specs/auth.md:SC-3
Closes: G-12
```

Rules:

- `Implements:` trailers cite the **decision(s) and/or requirement(s)** the commit realizes. MUST reference at least one `D-{n}` when the project has formal decisions (all scopes except micro). When citing `FR-{n}` or `NFR-{n}` from outside the owning spec, the reference MUST use the qualified form `specs/<spec>.md:FR-{n}` or `specs/<spec>.md:NFR-{n}`.
- `Covers:` trailers cite the **spec conformance criterion or functional requirement** the commit adds test coverage for. OPTIONAL at the commit level — this is change-summary metadata, not per-test traceability. Per-test traceability lives only in the test artifact itself via the test-name suffix form (`test_foo_covers_specs_auth_md_SC_3`) or an in-file comment (`// Covers: specs/auth.md:SC-3`) in the test file. In suffix form, the spec path slug lowercases the spec path, replaces every non-alphanumeric character with `_`, and strips leading/trailing `_` (for example `specs/auth.md` → `specs_auth_md`). See `03-implement.md` Traceability → Test traceability for the canonical rule.
- `Closes:` trailers cite the **gap** the commit resolves. OPTIONAL; use when the commit is specifically the resolution of a tracked gap.
- Multiple trailer types MAY coexist in one commit message. Multiple IDs within the same trailer MAY be comma-separated on one line OR split across repeated trailer lines (both forms are valid).

A complete commit message combining all four trailer types looks like:

```
feat(auth): add OAuth2 authorization code flow with PKCE

Implements the authorization code grant per RFC 6749 §4.1 with PKCE
(RFC 7636) for public clients. Adds the token endpoint, authorization
endpoint, and the PKCE verifier/challenge derivation.

Implements: D-5, specs/auth.md:FR-7
Implements: specs/auth.md:NFR-3
Covers: specs/auth.md:SC-2
Closes: G-18
```

In this example, `D-5` is the authentication architecture decision, `specs/auth.md:FR-7` is the functional requirement for the authorization flow, `specs/auth.md:NFR-3` is the non-functional requirement for PKCE support, `specs/auth.md:SC-2` is the spec conformance criterion for OAuth2 conformance, and `G-18` is a previously-tracked gap about the missing authorization endpoint. The commit cites all four in one message because the change realizes the decision, implements specific requirements, adds test coverage for a conformance criterion, and closes a tracked gap simultaneously.

Exceptions for commits that do not cite decisions are limited to maintenance changes (`chore(...)` per `standards.md` Git Conventions) and micro-scope projects (see `00-audit.md` Project Scope Classification).

## ID Collision Rules

- **Global families (D-, G-, PSC-, NG-, L-):** one counter per family, per project. No collisions possible within a family.
- **Per-spec families (FR-, NFR-, SC-):** scoped per spec file. Two different spec files MAY both contain `FR-1`, but each `FR-1` refers to the requirement in its own file. When cross-referencing these labels from outside their owning spec, the reference MUST qualify with the file path (e.g., `specs/user-auth.md:FR-7`).
- **Cross-family uniqueness:** D-, G-, FR-, NFR-, PSC-, SC-, NG-, L- are distinct families. `D-1` and `FR-1` are always different artifacts.

## Per-Gate Mechanical Checks

Every phase gate MUST include the following mechanical `[M]` checks related to labels:

- `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits (markers allowed in governance docs; forbidden in authored artifacts once a gate is approached)
- For Phase 1 (Design): `grep -c '^### D-' .agent-state/decisions.md` MUST be at least the number of Required Decisions applicable to the scope
- For Phase 2 (Spec): for each spec file, `grep -cE '\bFR-\d+\b' specs/<spec>.md` MUST be non-zero (or the spec MUST declare `FR-none` in its Contract section with justification)
- For Phase 2 (Spec): for each spec file, `grep -nE '^\s*([-*+]\s*)?NG-(\d+|none):' specs/<spec>.md` MUST return zero — spec-local NG labels are forbidden; exclusions belong in prose or qualified `audit.md:NG-{n}` references
- For Phase 3 (Implement): `grep -nE '^Implements: ((D-[0-9]+|specs/[^ ,:]+\.md:(FR|NFR)-[0-9]+)(, (D-[0-9]+|specs/[^ ,:]+\.md:(FR|NFR)-[0-9]+))*)$' <commit-message>` MUST match every `Implements:` trailer
- For Phase 3 (Implement): `grep -nE '^Covers: (specs/[^ ,:]+\.md:(SC|FR)-[0-9]+)(, specs/[^ ,:]+\.md:(SC|FR)-[0-9]+)*$' <commit-message>` MUST match every `Covers:` trailer when present
- For Phase 3 (Implement): `grep -nE '^Closes: G-[0-9]+(, G-[0-9]+)*$' <commit-message>` MUST match every `Closes:` trailer

These checks are automatable via hooks, CI scripts, or the `/verify` skill defined in `harness/claude-code/skills/verify/SKILL.md`.
