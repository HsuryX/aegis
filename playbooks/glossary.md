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
id: playbooks/glossary
title: Glossary
version: 1.2.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
severity: reference
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - AGENTS.md
supersedes: null
---

# Glossary

This file is the single canonical source for every framework term with multiple common meanings, subtle distinctions, or measurable criteria. When a playbook rule uses one of these terms, the playbook links here via its Terminology block. When a new term enters any playbook and has more than one meaning in common usage, the author MUST add it to this file before shipping the playbook change.

Entries are ordered alphabetically. Each entry defines the term precisely, distinguishes it from near-neighbors, and points to the playbook where the term is most heavily exercised.

This file is non-normative — it defines meaning, not rules. Rules live in the playbooks and use the terms defined here.

---

## artifact

Any file produced or managed by the framework: audit entries in `audit.md`, decisions in `decisions.md`, gaps in `gaps.md`, specifications (typically under `specs/` when present), session log entries in `phase.md`, code, commits, and the playbooks themselves. When a rule says "every artifact MUST trace to a decision", it applies to every item except the framework files (which trace to amendments per the Amendment Protocol instead of to project decisions).

See also: **contract**, **spec**.

## authority model

The architectural answer to "who owns truth for each domain concept" — the required Design phase decision D-2 in `01-design.md`. For every durable concept in the system, the authority model identifies exactly one subsystem, audit surface, or spec as the canonical owner. Other components MUST consult that owner rather than maintaining their own copy of the truth.

A missing or ambiguous authority model is a **structural problem**: it leads to duplicate truth, silent divergence between copies, and the "ghost authority" failure pattern where a derived artifact (cache, index, summary, convenience layer) drifts into being treated as canonical. The authority model is the precondition for the `AGENTS.md` Authority Discipline rule ("one fact, one canonical owner"). The Whole-System Composition Check in `01-design.md` mechanically verifies that no two subsystems claim authority over the same concept.

See `01-design.md` Required Decisions (D-2) and `AGENTS.md` Authority Discipline.

## canonical

The single authoritative form. When a concept has several plausible names or representations, the canonical one is the source of truth. The framework enforces canonical form via the **Naming Table** in `decisions.md` — every durable concept has exactly one entry with one canonical term and any number of forbidden aliases.

"Canonical", "source of truth", and "primary" all mean the same thing here. The framework prefers "canonical" throughout to reduce vocabulary.

See `01-design.md` Naming Table for the enforcement mechanism and `AGENTS.md` Authority Discipline for the underlying principle ("one fact, one canonical owner").

## contract

A single **section** of a **specification** — the invariants, formats, and behaviors for one interface. **Not a synonym for "spec".** One spec may contain several contracts (for example, a REST API spec may contain one contract per endpoint; a library spec may contain one contract per public function). The `Contract` section is defined in `02-spec.md` Spec Section Structure.

Common mistake: calling an entire spec document "the contract". Use "spec" or "specification" for the whole document; use "contract" only for the section that describes one interface's invariants.

**Prose contract vs. machine-readable contract.** A contract has two complementary forms:

- **Prose contract** — the `Contract` section in the spec written in markdown. Describes invariants in English with MUST/SHOULD/MAY force. Primary audience: human reviewers and the agent during implementation.
- **Machine-readable contract** — a structured artifact in one of the canonical forms enumerated in `standards.md` Contract Formats (the sole canonical list — this entry does not re-enumerate to avoid duplicate truth). Machines validate requests and responses against it. Primary audience: tooling, test generators, and consumers. Required for any cross-trust-boundary interface per `02-spec.md` Spec Section Structure → Machine-readable Contract. Internal-only interfaces MAY record `schema: N/A — internal only` with a one-line justification.

Both forms MUST agree. The prose contract is authoritative for intent; the machine-readable contract is authoritative for format. A conflict between them is a defect that MUST halt the spec gate until resolved and be tracked as a gap entry; if the conflict reflects a framework rule problem rather than a local spec error, that gap's type is `framework`.

See **spec** for the enclosing document.

## cycle completion

Terminal completion in `steady-state` lifecycle mode. It means the current change/governance cycle has satisfied its terminal-phase gate and housekeeping; it does **not** mean the product is forever done. After cycle completion, the next material work item restarts at Phase 0.

See **lifecycle mode**, **steady-state**, `02-spec.md` Terminal Phase, and `03-implement.md` Post-Completion Housekeeping.

## decision

A resolved architectural or design choice recorded in `.agent-state/decisions.md` with a `D-{n}` identifier. A decision represents **resolved information** — distinct from a **gap**, which represents unresolved information. The `D-1..D-12` range is reserved for the Required Decisions enumerated in `01-design.md`; `D-13+` are project-specific additions. Decisions move through the lifecycle states `Draft` → `Proposed` → `Accepted` → `Final` (or to `Rejected`, or to `Deferred` pending a later return to `Draft` or `Rejected`); only `Accepted` or `Final` decisions constrain subsequent phases.

See `01-design.md` Required Decisions for the canonical enumeration and Decision Lifecycle for state transitions, and `identifiers.md` for the `D-{n}` identifier rules. Distinct from **significant decision** below, which defines when Quality Seeking's full alternatives analysis is required.

## feature slice

A logically coherent subset of the total product scope that can traverse the design-spec-implement phase sequence **independently** while respecting shared cross-cutting decisions. Slices MUST be large enough to produce a verifiable outcome on their own and small enough to design without global context. The Decomposition Rule in `01-design.md` governs when feature-sliced delivery applies; each slice carries its own per-phase status in `.agent-state/phase.md` Feature Slices section, and each slice MUST read and respect decisions in `Accepted` or `Final` state from other slices before proceeding.

Feature slices are distinct from:
- **Subsystems** (`01-design.md` Whole-System Composition Check) — subsystems are structural partitions of the current canonical system; slices are temporal partitions of the delivery sequence.
- **Phases** (`AGENTS.md` Phase Gates) — phases are framework-wide stages; slices are scope-bounded instances that each traverse the phases.
- **Spikes** (`01-design.md` Prototyping Protocol) — spikes are time-bounded evidence-gathering exercises; slices are permanent scope partitions.

## gate

A **phase gate** — the threshold that MUST be met before the agent advances from one phase to the next. Defined for each phase in `AGENTS.md` Phase Gates and operationalized in each phase playbook's Phase Gate section. A gate's items are tagged `[M]` (mechanical), `[J]` (judgment), or `[M+J]` (mixed) and classified into three tiers: `[must-meet]`, `[should-meet]`, `[nice-to-have]`.

Evaluating a gate produces exactly one of five outcomes defined in `principles-gates.md` Gate Outcome Vocabulary:

- **Go** — all `[must-meet]` items met; advance
- **Conditional Go** — all `[must-meet]` items pass; one or more `[should-meet]` items fail but the failures are bounded and can be addressed during the next phase without degrading that phase's work. Each unmet `[should-meet]` item is recorded as a `conditional` gap with `Trigger condition: "before Phase {N+1} gate"` per `principles-gates.md` Gate Outcome Vocabulary
- **Hold** — at least one `[must-meet]` item unmet; remain in the phase and work toward meeting it
- **Recycle** — `[must-meet]` items fail AND the failures indicate significant rework of the current phase's output; the output is structurally inadequate, not just incomplete. The project remains in the current phase, the recycle is recorded in the session log, and repeated recycles escalate per `AGENTS.md` Phase Regression Procedure. Distinguish from `Hold` (specific bounded failures, still same phase) per `principles-gates.md` Gate Outcome Vocabulary
- **Kill** — terminal cancellation of the project or slice; no further phase work, and the user MUST authorize the termination

Gates are thresholds, not targets (see `zen.md` aphorism #20). `Conditional Go` is available only when all `[must-meet]` items already pass; using it to bypass, relabel, or paper over a failing `[must-meet]` item is a gamed gate, not a met one (see `zen.md` aphorism #12).

Distinct from **verdict**: gate outcomes apply to a phase as a whole; verdicts apply to individual audit items.

### Adversarial Gate Check

A fresh-context review subagent run before each phase gate per `principles-gates.md` Adversarial Review Protocol (canonical owner of the protocol AND the per-phase timing hooks table); REQUIRED for `standard` and `large` scope, OPTIONAL for `micro` and `small`. Distinct from the phase gate itself — the Adversarial Gate Check produces the completeness and bad-faith-reader evidence that the phase gate then evaluates against `[must-meet]` / `[should-meet]` / `[nice-to-have]` criteria.

## gap

Missing, unclear, or blocking information tracked in `gaps.md`. A gap represents **unresolved information** — distinct from a **decision** (see above), which represents resolved information.

Each gap has:
- **Severity**: `critical` (blocks phase advancement) or `non-critical` (tracked but permits advancement)
- **Type**: `evidence` (spike needed), `analysis` (deeper thinking needed), `decision` (new decision required), `framework` (framework rule is wrong), `deviation` (framework-rule exception with explicit expiry), `conditional` (verdict/gate carry-forward obligation), `scope-reduction` (explicit tracked deferral of a requirement), `failure-pattern` (named anti-pattern detected), or `grandfathered` (pre-adoption artifact preserved under explicit expiry). There is no separate `accepted-risk` type; residual-risk prose MUST point to a real `G-{n}` entry of one of these types. Canonical taxonomy of 9 types is defined in `playbooks/gaps.md` — see it for the full table with resolution rules.

When in doubt about whether information is a gap, the framework treats it as one — false positives cost less than false negatives.

See [`gaps.md`](./gaps.md) for the full gap playbook (type taxonomy, lifecycle, resolution rules, phase-gate interaction), `.agent-state/gaps.md` for the working entry template, and `playbooks/principles-gates.md` Amendment Protocol for the amendment and deviation flows.

## harness

The agent-specific adapter layer — hooks, permissions, skills, settings, and any other agent-idiosyncratic configuration. Distinct from the **agent-neutral playbooks**, which describe what the framework requires without assuming a specific coding agent.

aegis ships prioritized harness adapters for Claude Code and Codex plus a CI backstop template, all under `harness/`. The shipped vs. active state of each supported surface, the canonical control table, and adoption pointers live in [`harness/capability-matrix.md`](../harness/capability-matrix.md). Per-harness setup details live in each prioritized harness's README.

See also `automation.md` for agent-neutral automation principles.

## lifecycle mode

A Phase 0 strategy choice recorded in `.agent-state/audit.md` and `.agent-state/phase.md` that defines what terminal completion means. The two canonical values are:

- **finite-delivery** — terminal completion means a bounded project or slice is complete until new scope is explicitly opened.
- **steady-state** — terminal completion means only the current cycle is complete; future work re-enters at Phase 0.

Lifecycle mode does not add a fifth phase and does not relax audit/design/spec/implementation rigor. It changes terminal semantics only.

## phase regression

A backwards transition from a later phase to an earlier one when new evidence invalidates the prior phase's work — for example, Phase 3 implementation reveals a missing decision and the project regresses to Phase 1. Canonical owner: `AGENTS.md` Phase Regression. Repeated regressions (more than twice from the same phase, or more than three total in one session) escalate to status BLOCKED awaiting user direction.

Distinct from a **phase gate Hold** (the project remains in the current phase pending bounded fixes) and from a **Recycle** (current-phase output is structurally inadequate but does not reset to an earlier phase).

## review

**Human-checked** or **separate-agent-checked in a fresh context.** Produces a rendered judgment with rationale. Distinct from **verify** (tool-checked) and **validate** (requirements-checked).

A review MUST be performed by someone other than the artifact's author. For standard/large scope, review uses a separate agent invoked in a fresh context; for micro/small scope, self-review against the current phase playbook's Quality Checks is sufficient with the scope classification recorded as justification.

The framework defines four reviews: **Code review** (`03-implement.md`), **Specification review** (`02-spec.md`), **Design review** (`01-design.md` Whole-System Composition Check), and **Audit review** (`00-audit.md` Quality Checks).

## significant concern

A problem or task item that meets ANY of the following: (a) would require its own decision entry under the `significant decision` criteria if solved in isolation, (b) would open a gap entry of `critical` severity if left unresolved (per `gaps.md` Severity Criteria — the framework uses a two-level scale, `critical` or `non-critical`), (c) crosses more than one subsystem boundary or more than one surface in the Phase 0 taxonomy, (d) introduces a new external integration, or (e) changes a published contract (FR/NFR/SC label, machine-readable schema, or public API).

Trivial task items — formatting a single file, renaming a local variable, responding to a single lint warning, updating one date stamp — are NOT significant concerns. Architectural choices, security reviews, cross-file refactors, new framework amendments, new subsystems, new integrations, and migrations ARE significant concerns.

Used in `AGENTS.md` Session Start Protocol step 8 to trigger the kitchen-sink-session scope guard: a session whose opening prompt spans more than one phase transition OR combines a phase transition with more than one significant concern MUST propose session sequencing before beginning work. Without this definition, step 8 could be gamed by downscoping the concern label.

See `gaps.md` Severity Criteria for criterion (b); `00-audit.md` Per-Surface Entry Format for criterion (c); `significant decision` below for criterion (a).

## significant decision

A decision where (a) changing it later would require modifying more than one file, OR (b) two reasonable engineers could disagree on the answer.

For decisions that clearly fail this test (e.g., local variable naming, single-line formatting), a brief inline justification is sufficient — no formal alternatives analysis is REQUIRED. When uncertain whether a decision is significant, the agent MUST treat it as significant. The Quality Seeking protocol applies in full to significant decisions.

See `principles.md` Quality Seeking for the full rule.

## spec / specification

A canonical, test-derivable description of what the current canonical system does for one public interface or one subsystem surface. Specs own contract truth and conformance truth per Authority Discipline (see `AGENTS.md`); product boundary, product goals, product non-goals, and product success criteria live in the Product surface of `audit.md`.

A spec contains one or more **contract** sections (interfaces and their invariants), plus Scope, Definitions, Error semantics, Security considerations, and Conformance criteria sections. Specs describe what the system does, not how it does it — implementation-level detail belongs in code, not in specs.

See `02-spec.md` for the full spec format, rules, and quality checks.

## steady-state

A lifecycle mode for long-lived repositories that expect recurring change/governance cycles rather than one forever-final endpoint. The same four phases and the same gates still apply; only terminal semantics differ. Release Readiness runs only for cycles that actually ship.

See **lifecycle mode** and **cycle completion**.

## STRIDE

The threat classification taxonomy (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) used by the security threat model. Canonical owner: `security-threat-model.md` § STRIDE Overview, including applicability rules and examples. Referenced from `01-design.md` Required Decisions D-5 when any `security-threat-model.md` applicability condition is true.

## structural problem

A defect in **form** — wrong boundary, wrong authority, wrong dependency direction, wrong placement, wrong naming, or wrong layering. Distinct from:
- **Behavioral defects** — wrong output for a given input, usually fixed by correcting logic
- **Quality defects** — untested, poorly named, duplicated, or over-complicated code within an otherwise correct structure, usually fixed by cleanup

Structural problems require **redesign**, not patching. The verdict for a structural problem is typically `redesign` or `delete`, never `keep` — see `AGENTS.md` Verdict Discipline. Adding an adapter or wrapper to hide a structural problem is a prohibited shortcut (see `principles.md` Prohibited Shortcuts).

In Phase 0 audit, the "top 3 highest-risk structural problems" recorded in `gaps.md` are specifically these form-level defects, not quality or behavioral issues.

## surface

A Phase 0 audit category. There are seven surfaces, ordered by the constraint chain — earlier surfaces constrain later ones:

1. **Product** — boundary, scope, goals, product success criteria, non-goals
2. **Architecture** — subsystems, dependency direction, public contracts, data model, versioning
3. **Runtime** — behavior, state, errors, recovery, configuration
4. **Operations** — build, CI/CD, deployment, observability
5. **Security** — trust boundaries, secrets, authentication, authorization
6. **Quality** — tests, dependency health, code quality, accessibility
7. **Organization** — naming consistency, documentation accuracy, repository structure

Each surface is recorded in `audit.md` with the Per-Surface Entry Format. Micro projects audit Product + Security; small projects audit Product + Architecture + Security + Quality; standard and large projects audit all seven.

See `00-audit.md` Surfaces for the full list and audit order.

## trust boundary

The interface where data or control crosses from one trust domain into another. Common trust boundaries include:

- User → system (any user-facing interface)
- System → third-party (external API calls, webhooks, data imports)
- Low-privilege component → high-privilege component (privilege escalation points)
- Untrusted network → trusted network
- Unauthenticated → authenticated context
- Anonymous data → identified data

Three rules apply at every trust boundary:
- **Input validation** is REQUIRED (see `standards.md` Input validation)
- **Authentication and authorization** MUST be verified when the crossing involves privileged operations (see `standards.md` Security)
- **Test coverage** target is 95% minimum for code paths crossing trust boundaries, vs. the 80% default (see `standards.md` Testing)

The per-project enumeration of trust boundaries is the output of the security model decision (D-5) in `01-design.md` Required Decisions.

## unit

In the Per-Task Attempt Limit, a unit is the smallest test/fix/implementation increment that produces one verifiable outcome. Examples:
- One failing test now passes
- One implementation function is correct end-to-end
- One data transformation matches its expected output on fixture data
- One bug is reproduced and then fixed

A unit is **not** the same as:
- One commit (a commit may contain multiple units, or a partial unit bundled with maintenance)
- One file (a file may implement multiple units)
- One pull request (a PR usually contains multiple units)

The Per-Task Attempt Limit (`03-implement.md`) applies **per unit**: if a single unit fails after 3 attempts, the agent MUST stop, record what failed and where the mental model was wrong, report status BLOCKED, and escalate to the user or return to an earlier phase.

## validate

**Requirements-checked.** Asks: "does this satisfy the requirement?" May involve judgment (e.g., "does this UI match the product's definition of good?") or product validation at completion ("does the implemented system address the Product surface goals, `PSC-{n}` product success criteria, and `NG-{n}` product non-goals from the audit?").

Distinct from:
- **verify** — tool-checked, produces mechanical evidence
- **review** — human or separate-agent judgment on the artifact's construction

Validation is the terminal check: tools verify the code, reviewers review the artifact, and validation confirms the requirement is met. In `03-implement.md` Phase 3 Completion Criteria, item 9 is a validation check: the agent walks through each Product surface goal and confirms it is met, explicitly deferred, or renegotiated with the user.

## verdict

The disposition assigned to every existing element during `00-audit.md` Phase 0. Canonical owner: `AGENTS.md` Verdict Discipline (defines the four verdicts `keep` / `keep-with-conditions` / `redesign` / `delete` and the prohibition on a fifth state). Verdicts are recorded in `.agent-state/audit.md` per the Per-Surface Entry Format defined in `00-audit.md`. Green-field projects with no existing element to audit MAY omit the Verdict field and record scope classification as the justification in the session log.

Distinct from **review** (a separate check on the author's work product) and from **gate** (a phase-level disposition, not an element-level one).

## verify

**Tool-checked.** Produces machine-readable evidence — command output, test results, lint output, type-check output, security scan output, file existence, checksums, etc. Automatic or automatable.

Distinct from:
- **validate** — requirements-checked (the requirement, not the tool, is the arbiter)
- **review** — human or separate-agent judgment with rationale

When the framework says "the agent MUST verify X", the expected evidence is a tool invocation with its output recorded in the session log or in the relevant spec's Conformance section. Phrases like "I checked", "it looks fine", "should work", "probably correct" are explicitly forbidden as verification evidence — see `principles.md` Completion Status Protocol for the full list.

See `03-implement.md` Verification Sequence for the canonical tool order (Build → Type check → Lint → Test → Security scan → Diff review) that every meaningful implementation change MUST run through.

## well-maintained (dependency)

Concrete, measurable criteria for "well-maintained" when evaluating an external dependency under `standards.md` Dependency Discipline. A dependency qualifies as well-maintained when ALL of the following are true:

- Last release within 12 months, OR documented maintainer response to critical issues within 30 days (whichever is applicable for the domain — long-stable libraries with infrequent releases may qualify on responsiveness alone)
- A security advisory process exists (CVE tracking, a security contact, or an equivalent public disclosure channel)
- A test suite is present and runs on each release
- Release notes are documented for recent versions
- No known unpatched critical CVEs

The test strategy decision (D-10) MAY override these criteria for project-specific cases — for example, a project may choose to accept a dependency on a stable-but-inactive library whose scope is narrow enough that inactivity is not a risk. When overriding, the decision entry MUST document the override and its justification.
