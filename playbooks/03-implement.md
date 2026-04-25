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
id: playbooks/03-implement
title: Phase 3: Implementation
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 3-implement
severity: normative
mechanical_items: 7
judgment_items: 10
mixed_items: 2
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/identifiers.md
  - playbooks/standards.md
  - playbooks/gaps.md
  - playbooks/02-spec.md
supersedes: null
---

# Phase 3: Implementation

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **gap**, **review**, **spec**, **trust boundary**, **unit**, **validate**, **verify**. "Unit" in the Per-Task Attempt Limit means the smallest increment producing one verifiable outcome — not a commit, not a file. See the glossary for the full distinction between verify, validate, and review.

## Objective

The agent MUST write code that faithfully implements canonical specifications. Every change MUST trace to a design decision. Code quality MUST meet the standards in `playbooks/standards.md`.

**Workflow per change:** Pre-Implementation Check → TDD (test → implement → refactor) → Post-Change Verification → Verification Sequence (run tools, record evidence) → Post-Implementation Cleanup → Re-verify → Code Review.

## Lifecycle Mode

The agent MUST read `Lifecycle mode` from `phase.md` before evaluating completion or release:

- **finite-delivery** — passing the Phase 3 completion criteria means the project or slice has reached its planned endpoint.
- **steady-state** — passing the Phase 3 completion criteria means the current change/governance cycle is complete. The next material work item MUST restart at Phase 0 after housekeeping. This mode MUST NOT be used to bypass decisions, specifications, reviews, hotfix/rollback discipline, amendment rules, or release checks.

Both lifecycle modes use the same default 0 → 1 → 2 → 3 phase sequence. Existing projects MAY use the bounded-change rule from `00-audit.md` to classify a cycle as 0 → 3 when existing decisions and reviewed specs already fully cover the requested work. Lifecycle mode changes terminal meaning, not required rigor.

## Pre-Implementation Check

Before writing any code, the agent MUST:
1. Confirm via `phase.md` that the project is in phase 3
2. Read `playbooks/standards.md`
3. Check the project's scope classification in `audit.md` — **micro-scope** projects do not have formal decisions or specifications; the agent MUST proceed directly to the TDD workflow using `standards.md` as the quality bar. Existing non-micro projects MAY also arrive here from a bounded-change 0 → 3 cycle, but only when `phase.md` already records Phases 1–2 as `not-applicable` for the cycle under the `00-audit.md` bounded-change rule and cites the reused decisions/spec anchors plus the delta-audited surfaces. Steps 4–7 below apply to every non-micro implementation cycle, including bounded-change cycles.
4. Read `decisions.md` — know what is decided, including the test strategy
5. Identify which decision(s) the intended change implements
6. Identify which specification(s) the change implements — tests MUST be derived from these specifications, not from the decisions alone
7. If no decision or specification covers the change, the agent MUST STOP — return to Design phase (if a decision is missing) or Spec phase (if the decision exists but no spec does)

Implementation is not the place to discover missing design. If the agent finds itself making architectural judgment calls while coding, that is evidence of a design gap — the agent MUST treat it as a gap, not as an opportunity to decide on the fly.

If a bounded-change cycle reaches this phase and any of steps 4–7 fail in practice, the bounded-change assumption is false. The agent MUST stop, return to Phase 1 or Phase 2 as appropriate, and clear the `not-applicable` shortcut for that cycle.

**WIP limit:** The agent MUST implement one specification at a time through the full cycle (test → implement → verify → review) before starting the next. Parallel implementation of independent specifications MAY be permitted only when the agent can hold full context of all parallel units without degrading quality.

## Traceability

Every code change MUST reference the decision it implements using labels from [`identifiers.md`](./identifiers.md):

```
type(scope): description

Implements: D-{n}
```

Trailer forms:

- `Implements: D-{n}` — single decision
- `Implements: D-3, D-7` — multiple decisions (comma-separated) OR as repeated `Implements:` lines
- `Implements: D-3, specs/auth.md:FR-7` — decision plus functional requirement from a spec
- `Implements: specs/auth.md:NFR-3` — non-functional requirement from a spec
- `Covers: specs/<spec>.md:SC-{n}` or `Covers: specs/<spec>.md:FR-{n}` — optional commit metadata summarizing that the commit adds test coverage for a spec conformance criterion or functional requirement
- `Closes: G-{n}` — commit resolves a tracked gap

Multiple trailer types MAY coexist in one commit message. A change that traces to no decision MUST NOT be made — except for: (1) maintenance changes (typo fixes, formatting, dependency updates, documentation corrections) which MAY use `chore(scope): description` without a decision trace, and (2) micro-scope projects where formal decisions do not exist — the agent MAY use `type(scope): description` per `standards.md` Git Conventions. If a "maintenance" change starts requiring judgment calls, it has crossed into design territory and the agent MUST open a decision. If a micro-scope project starts requiring architectural judgment calls, it has outgrown its scope classification and the agent MUST reclassify per `00-audit.md`.

### Test traceability

Every test MUST cite the path-qualified `specs/<spec>.md:SC-{n}` (conformance criterion) or `specs/<spec>.md:FR-{n}` (functional requirement) it validates. Per-test traceability accepts only two mechanically verifiable forms; optional commit-level `Covers:` trailers do NOT satisfy this requirement:

- **Test-name suffix** — `test_auth_denies_expired_token_covers_specs_auth_md_SC_3` (preferred for table-driven tests where the suffix survives refactor). In suffix form, the spec path slug lowercases the spec path, replaces every non-alphanumeric character with `_`, and strips leading/trailing `_` (for example `specs/auth.md` → `specs_auth_md`).
- **In-file comment** — `// Covers: specs/auth.md:SC-3` or `# Covers: specs/auth.md:SC-3` in the test file (preferred when tests are committed separately from the feature)

Commit-level `Covers:` trailers such as `Covers: specs/auth.md:SC-3, specs/auth.md:FR-7` MAY still be used as optional change-summary metadata, but they do NOT count as per-test traceability.

At the Phase 3 gate, mechanical check: `grep -rnE '^\s*(//|#)\s*Covers:\s*specs/[^ ,:]+\.md:(SC|FR)-[0-9]+|covers_[A-Za-z0-9_]+_(SC|FR)_[0-9]+' tests/ src/ --include='*.py' --include='*.ts' --include='*.go' --include='*.rs'` MUST return a count at least equal to the count of declared `SC-{n}` entries across all specs, and `python3 validate.py` check 13 MUST confirm set coverage on the fully qualified `specs/<spec>.md:SC-{n}` identifiers. Untraced tests indicate spec coverage gaps — every test exercises some behavior, and every spec'd behavior MUST have at least one test.

**Legacy-test grandfathering at adoption time.** When aegis is adopted on a project with pre-existing tests, the traceability requirement applies ONLY to tests added or edited after adoption. Pre-adoption tests MAY be grandfathered under a single project-level gap entry (type: `grandfathered`, Expiry condition: "until 100% of originally-grandfathered tests have been edited, superseded, or deleted", Initial artifact set: {file list or `git log` anchor identifying the pre-adoption tests}). The gap MUST list the initial test-file set (or a `git log` anchor) so the expiry is verifiable. Grandfathering MUST NOT be invoked retroactively on tests modified after adoption — any touched test MUST carry the required suffix or in-file `Covers:` comment per the two accepted per-test forms above.

### Commit message format enforcement

Commit messages MUST match the conventional-commits regex and MUST include the `Implements:` trailer for non-maintenance commits:

- Header regex: `^(feat|fix|refactor|docs|test|chore|perf|ci)(\([a-z0-9-]+\))?: .+$`
- Trailer requirement: `grep -E '^Implements: (D-[0-9]+|specs/[^ :]+\.(md|ya?ml|json):(FR|NFR|SC)-[0-9]+)' <commit-msg-file>` MUST return a match UNLESS the commit type is `chore` OR scope classification is micro
- Exceptions logged: maintenance commits (`chore:`) skip the trailer; micro-scope projects follow `standards.md` Git Conventions exception path

Enforcement MAY be automated via a `commit-msg` git hook (see `harness/claude-code/hooks-cookbook.md` → Commit validation hook). At the Phase 3 gate, mechanical check on the last commit: header matches the regex AND trailer is present (or exception applies).

## Hard Rules

1. **No architectural discovery** — if the architecture needs to change, the agent MUST stop coding, update `decisions.md`, and re-enter Design phase
2. **No copy-paste from reference material** — the agent MUST use `_legacy/` or external sources for behavioral clues and MUST write new code fresh
3. **No silent scope change** — the agent MUST implement exactly what is decided. The agent MUST NOT add capability beyond specifications and MUST NOT silently drop requirements. After implementation, the agent MUST verify every specification requirement is present — silent scope reduction is as harmful as scope creep. Silent deferral is forbidden; explicit deferral is permitted only when tracked. The distinction is load-bearing:
   - **Silent deferral (forbidden)**: dropping, weakening, or postponing a specified requirement without a corresponding entry in `gaps.md`. The following scope-reduction phrases are markers for silent deferral and MUST NOT appear in code, comments, or commit messages: "simplified version", "static for now", "defer to follow-up", "good enough for now", "stub for the moment", "coming in v2". Canonical list mirrors `validate.py` `_DEFERRAL_PHRASES`; see `standards.md` Self-Review Checklist for the mechanical scan.
   - **Explicit deferral (permitted)**: postponing a specified requirement via a `gaps.md` entry of type `scope-reduction` with severity assessed, an explicit trigger condition for when the requirement MUST be restored, and user confirmation when the requirement is `critical`. The agent MUST record the deferral before making the code change that relies on it, not after.
   If any scope-reduction marker phrase is detected during Post-Change Verification, the agent MUST either restore the requirement, convert it to an explicit deferral via a tracked `gaps.md` entry, or renegotiate with the user.
4. **No compatibility shims** — shims MUST NOT be introduced unless explicitly recorded as a design decision with justification
5. **Exact naming** — the agent MUST use canonical terms from the naming table and MUST NOT introduce synonyms
6. **Correct placement** — files MUST be placed where the decided repository structure specifies
7. **Standards compliance** — all code MUST pass the self-review checklist in `standards.md`
8. **Root cause before fix** — when a test fails or a build breaks, the agent MUST investigate the root cause before attempting a fix. The agent MUST NOT apply band-aid patches that mask the underlying problem

## Test-Driven Implementation

The agent MUST follow the TDD workflow defined in `standards.md`:
1. Write a failing test derived from the specification
2. Write minimal implementation to make it pass
3. Refactor to meet code quality standards
4. Verify coverage meets the target defined in the test strategy decision

## Database Migration Protocol

Applies when the project has a persistent data store. Every schema change MUST follow this protocol:

1. Every schema change MUST be implemented as a versioned, reversible migration file — not ad-hoc DDL
2. Migrations MUST trace to a decision ID just like code changes (`Implements: D-{n}`)
3. Migration ordering: additive changes MUST come first (new tables, new nullable columns), then data transformations, then destructive changes (column removal, type changes) in a separate migration
4. Every migration MUST have a corresponding rollback migration that restores the prior schema without data loss — or MUST document why rollback is destructive and REQUIRES explicit approval
5. Data migrations (transforming existing data to fit a new schema) MUST be separate from schema migrations and MUST be idempotent
6. The agent MUST run the migration forward and backward in a test environment before applying to any shared environment; migration execution MUST be included in the Verification Sequence
7. For existing projects using in-place evolution or hybrid strategy, the agent MUST audit the current migration state as part of the Data Model surface in Phase 0

## Post-Change Verification

Ordered by severity: correctness → authority → consistency → completeness. Every item MUST be verified. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**Tally:** 4 `[M]` · 1 `[M+J]` · 6 `[J]`.

- [ ] **[M+J]** Code MUST match the specification it implements — verified at all four levels: (1) artifact exists, (2) substantive (not a stub or placeholder), (3) wired (imported and actually called/used), (4) data flows through it end-to-end. Mechanical: existence (1) and wiring (3) are greppable. Judgment: substantive (2) and end-to-end (4) require interpretation.
- [ ] **[J]** Error handling MUST cover all failure paths identified in the spec's error semantics
- [ ] **[J]** No new authority path MAY have been introduced (no artifact MAY have silently become a truth source)
- [ ] **[J]** No existing behavior MAY have been preserved by accident (only by explicit decision)
- [ ] **[M]** Naming MUST match the canonical naming table exactly. Mechanical: grep changed files against the Forbidden Aliases column of the Naming Table — any hit is a violation. Enforcement MAY be automated via a PreToolUse (Write|Edit) hook that re-reads `decisions.md` on each invocation and rejects writes whose content matches any alias (see `harness/claude-code/hooks-cookbook.md` → Naming-table alias hook).
- [ ] **[M]** File location MUST match the decided repository structure. Mechanical: new files MUST appear under the path assigned to their subsystem in D-11.
- [ ] **[M]** Every new test MUST cite a path-qualified `specs/<spec>.md:SC-{n}` or `specs/<spec>.md:FR-{n}` in one of the two accepted per-test forms (test-name suffix or in-file comment; see Traceability → Test traceability). Mechanical: diff-scoped grep for `^\s*(//|#)\s*Covers:\s*specs/[^ ,:]+\.md:(SC|FR)-[0-9]+|covers_[A-Za-z0-9_]+_(SC|FR)_[0-9]+` in the added test files MUST return ≥ 1 reference per new test case.
- [ ] **[M]** Commit message MUST match conventional-commits format AND carry the `Implements: D-{n}` trailer (exceptions: `chore(...)` and micro-scope). Mechanical: the most recent commit message MUST satisfy the Traceability → Commit message format enforcement regex.
- [ ] **[J]** If this change affects a specification, the spec MUST be updated or deferral MUST be recorded in `gaps.md`
- [ ] **[J]** Observability requirements from the observability model decision MUST be implemented. For governance/tooling repos, this means the D-9 signal contract (governance-state, machine signals, chain-of-custody) rather than generic service-style logging/trace/metrics; for application/service repos, follow the service observability model actually chosen in D-9.
- [ ] **[J]** Self-review checklist from `standards.md` MUST pass (delegates to the Self-Review Checklist in `standards.md`)

## Verification Sequence

Ordered by dependency — each step MUST pass before the next is meaningful. After each meaningful implementation change, the agent MUST run the sequence in this order. The agent MUST record actual command output as evidence and MUST NOT check boxes from memory or confidence.

**Evidence loop (applies to every step below):** use the canonical evidence-before-assertion rule from `principles.md` and the evidence contract from `principles-gates.md`. For each verification step, run the proving command fresh in the current session, inspect the full output including exit code, record a verifiable evidence reference in `phase.md`, and only then mark the step as passed.

1. **Build** — the agent MUST verify the project compiles/builds without errors
2. **Type check** — the agent MUST run the type checker (if applicable)
3. **Lint** — the agent MUST run the project linter (if configured)
4. **Test** — the agent MUST run the full test suite and MUST record pass count and coverage percentage
5. **Security scan** — the agent MUST check for hardcoded secrets and known vulnerabilities (if tooling exists)
6. **Self-diff review** — the implementing agent MUST review its own diff to confirm it matches the design intent and nothing unintended was introduced. This is **self-review** by the implementing agent and is **distinct** from the subsequent Code Review section below, which REQUIRES a separate agent in a fresh context for standard and large scope projects. Both are required; neither substitutes for the other — the self-diff review catches "did I write what I intended?", while Code Review catches "does what was written match the spec and standards when read without the implementer's mental model?"

The agent MUST NOT claim a change is complete until all applicable steps produce clean output with recorded evidence. Minimum proof expectations remain specific even though the canonical evidence contract lives in `principles-gates.md`: test-pass claims need fresh test output with zero failures; build-success claims need the build command with exit 0; bug-fix claims need the reproducer now passing; requirements-met claims need a traced spec checklist; no-regressions claims need the relevant full-suite output rather than spot checks. Previous runs, partial suites, and confidence statements are not sufficient.

## Post-Implementation Cleanup

After verification passes, the agent MUST perform a dedicated cleanup review before marking complete:

- The agent MUST remove defensive code that guards against states the specification declares impossible
- The agent MUST remove over-engineering or premature abstractions not required by the specification
- The agent MUST remove dead code, unused imports, unused dependencies, and leftover debug artifacts
- The agent MUST simplify any code that is more complex than the specification requires
- The agent MUST verify the change is the minimal correct implementation — no more, no less

This is a separate pass from implementation, not an afterthought within it. After cleanup, the agent MUST re-run the Verification Sequence to confirm cleanup did not introduce regressions.

## Code Review

For standard and large scope projects, the agent MUST request a code review from a separate agent in a fresh context (no shared session state with the implementing agent) after Post-Implementation Cleanup and re-verification. For micro and small scope projects, self-review against the criteria below is sufficient — the author MUST record the scope classification as justification.

1. **Reviewer receives:** (a) the diff under review, (b) the relevant specification in full (not just the file path), (c) the decision ID(s) the change implements with the full text of each decision's Context, Decision, and Alternatives considered sections (not just the IDs), (d) the audit surface entries from `audit.md` that the change's subsystem derives from (the Product surface for scope/goal validation, plus the surface(s) corresponding to the subsystem under change), and (e) the self-review checklist from `standards.md`. The reviewer MAY request additional context for specific ambiguities encountered during review — the agent MUST provide the requested context as a targeted excerpt, not the whole project. The reviewer MUST NOT receive: the implementing agent's planning notes, unrelated specifications, other diffs, or the main session's context. The reviewer MUST operate in a fresh context with only the items listed above
2. **Review criteria:** specification fidelity, security checklist compliance, naming table compliance, error path coverage, and whether the code would be understandable to a cold reader
3. **Review outcomes:**
   - `approve` — the agent MAY proceed to commit
   - `request-changes` — the agent MUST implement the reviewer's feedback, re-run the Verification Sequence, and re-request review
   - `escalate` — a design concern was identified; the agent MUST return to Design phase
4. **Trivial changes exception:** for formatting, comment fixes, or single-line fixes with no behavioral change, self-review is sufficient — the author MUST record the triviality judgment in the commit message

## Per-Task Attempt Limit

A **unit** (see [`glossary.md`](./glossary.md): unit) is the smallest test/fix/implementation increment that produces one verifiable outcome — not a commit, not a file, not a pull request. If a unit fails after 3 attempts, the agent MUST:
1. Stop attempting
2. Record what was tried, what failed, and where the mental model was wrong
3. Report status as BLOCKED with specific details (see Completion Status Protocol in `principles.md`)
4. Escalate to the user or return to Design phase if the failure indicates a design gap

The agent MUST NOT spiral — repeated attempts without new information waste context and degrade session quality.

## Escalation Triggers

Ordered by severity of impact if not escalated. The agent MUST stop implementation and return to Design phase if:
- A security concern is discovered that is not addressed in the security model decision
- A subsystem boundary needs to change
- Two decisions in `Accepted` or `Final` state contradict each other in practice
- A specification gap makes correct implementation ambiguous
- A concept arises that has no canonical name
- The agent is tempted to add an adapter to avoid redesigning something

## Rollback Protocol

When a deployed change causes production issues despite passing all verification, the agent MUST:

1. **Revert first, debug second** — roll back to the last known good state before investigating root cause
2. **Revert commit format:** use `revert(scope): revert "original message"` with body explaining the production symptoms observed
3. **Open a gap entry** with severity `critical` and type `evidence`, documenting: what failed, what verification missed, and the symptoms
4. **Root cause analysis** MUST determine whether the gap is in the verification process, the specification, or the design
5. **Fix goes through normal workflow** — starting from whichever phase the root cause lives in
6. **Update verification** — if the failure reveals a class of issues that current verification does not catch, the agent MUST update the Verification Sequence or the test strategy decision
7. For changes involving database migrations, the rollback MUST include the reverse migration; if the reverse migration would cause data loss, this constraint MUST be documented in the deployment plan and MUST require explicit approval before forward deployment

## Hotfix Workflow

**Emergency authorization.** When a production-critical issue requires immediate action (production down, active security breach, data loss, or user-declared emergency), the normal phase sequence MAY be bypassed via this workflow. This section is aegis's canonical emergency hotfix workflow. The agent MUST NOT self-authorize an emergency — the agent MUST propose the emergency to the user first; the user MUST approve before the workflow proceeds. The emergency protocol is not a shortcut for impatience — if the issue can wait for the normal workflow, the agent MUST use the normal workflow. The scope of an approved emergency is limited to the specific triggering issue; adjacent cleanup MUST go through the normal phase workflow.

This workflow MUST be used only for production-critical issues:

1. The agent MUST propose the emergency to the user and obtain approval — the agent MUST NOT self-authorize a phase bypass. The agent MUST record an emergency decision entry `D-{n}: [HOTFIX] {title}` with `Status: emergency` and justification
2. The agent MUST write the minimal scoped fix with full test coverage for the specific issue
3. The agent MUST run the Verification Sequence — no exceptions, even under time pressure
4. The agent MUST deploy following the project's deployment process
5. The agent MUST open a reconciliation gap entry `G-{n}` with severity `critical` and type `decision`, referencing the emergency decision
6. Within 48 hours, the agent MUST either ratify the emergency decision into the design (add full alternatives analysis to the decision entry, update specs) or revert the hotfix and implement a proper fix through the normal phase workflow

## Phase 3 Completion Criteria

Apply the shared gate procedure from `AGENTS.md` Phase Gates and `principles-gates.md` (Gate Outcome Vocabulary, Three-Tier Gate Criteria, Multi-Perspective Verification, Verification Coverage Matrix). Run the Adversarial Review Protocol per its Per-phase timing hooks table in `principles-gates.md` before scoring this checklist. This checklist records the Phase 3-specific completion criteria only.

**Tally:** 3 `[M]` · 1 `[M+J]` · 4 `[J]`. **Tiers:** 5 `[must-meet]` · 2 `[should-meet]` · 1 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** Every specification MUST have a corresponding implementation. Mechanical: for each spec, `grep -rn '{spec_path}' <implementation-roots-declared-in-D-11>` returns non-zero OR the session log cites the implementing path explicitly for repos whose implementation is not concentrated under a single code root. `Implementation roots declared in D-11` means the canonical code/tool/spec roots that D-11 says this repo uses for implementation work.
- [ ] **[M+J]** **[must-meet]** Every implementation MUST pass its verification sequence with recorded evidence. Mechanical: the session log in `phase.md` contains recorded command output for Build/Type/Lint/Test/Security per the Verification Sequence. Judgment: the evidence actually corresponds to the change (and wasn't pasted from a prior run).
- [ ] **[J]** **[should-meet]** Post-implementation cleanup MUST have been performed on all code
- [ ] **[M]** **[must-meet]** All tests MUST pass with coverage meeting the test strategy targets. Mechanical: test runner exit code 0 + coverage tool output meets or exceeds D-10 target.
- [ ] **[M]** **[must-meet]** No decisions in `Draft` or `Proposed` state MAY remain in `decisions.md` at Phase 3 completion — every decision referenced by implementation MUST be in `Final` state for the current canonical system; decisions not cited by implementation MUST be in `Superseded`, `Rejected`, `not-applicable`, or `Deferred` (with a live trigger condition documented in `Unresolved concerns`). Mechanical: `grep -A2 '^### D-' .agent-state/decisions.md | grep -E '^\*\*Status:\*\* (Draft|Proposed)$'` MUST return zero hits. Judgment: every `Deferred` decision's trigger condition MUST still be live; expired triggers MUST force transition to `Final` or `Rejected` before Phase 3 completion.
- [ ] **[J]** **[should-meet]** The self-review checklist MUST pass for every source file (delegates to `standards.md` Self-Review Checklist)
- [ ] **[J]** **[nice-to-have]** A cold reader MUST be able to navigate from specification to implementation and verify compliance
- [ ] **[J]** **[must-meet]** Product validation: the implemented system MUST address the goals, non-goals, and product success criteria from the Product surface in `audit.md` — the agent MUST walk through each original product requirement (`PSC-{n}` and `NG-{n}` labels, recorded in the Product surface entry/design notes per Phase 0 audit conventions) and confirm each is met, explicitly deferred, or renegotiated with the user

## Post-Completion Control

After all Phase 3 Completion Criteria pass and before Post-Completion Housekeeping, the agent MUST produce the four DMAIC Control outputs. Their purpose is to ensure that the completed implementation **stays correct** after the agent ends the session — drift caught at the gate is cheap; drift caught months later is expensive.

1. **Mistake-proofing hooks** — for every rule the agent discovered during implementation that is mechanically checkable (greppable, exit-code-verifiable, pattern-matchable) and was being enforced only by discipline, the agent MUST propose a hook in the relevant harness (`harness/claude-code/hooks-cookbook.md` for the Claude Code harness; equivalent in other harnesses) or a CI gate. Proposals are recorded in the session log; adoption is subject to the Amendment Protocol in `principles-gates.md` if the rule lives in a playbook.
2. **Standard Operating Procedures (SOPs)** — for every recurring operational task surfaced during implementation (database migration rollout, secret rotation, deployment promotion, incident triage), the agent MUST either cite the existing procedure in the repository or draft a new procedure. Procedures live under `docs/` or `playbooks/` per D-12 (Documentation structure). An operation performed once without a procedure is acceptable; twice without a procedure is a `failure-pattern` gap.
3. **Reaction plans** — for each known failure mode of the implemented system (per the spec's error semantics and any open `gaps.md` entries with live trigger or expiry conditions), the agent MUST record the detection signal, the responder (human or automated), the first mitigation step, and the escalation path. Reaction plans live alongside the SOPs. A failure mode without a reaction plan is a gap of type `analysis` — the implementation is not yet production-complete.
4. **Guardrails** — for every runtime invariant that MUST hold but is not verified by tests (rate limits, quotas, circuit breakers, resource caps, concurrency limits), the agent MUST record the invariant, where it is enforced, and how to verify it is still enforced after future changes. Guardrails that depend on external configuration (cloud IAM, feature flags, environment variables) MUST cite the canonical source of truth.

Control outputs are recorded in the session log and cross-referenced from the Post-Completion Housekeeping archive step. The agent MUST NOT advance to housekeeping with any of the four outputs missing; missing outputs become `conditional` gap entries tied to the next completion-gate pass.

## Pre-Release Gate

After Post-Completion Control produces its four outputs and before Post-Completion Housekeeping runs, the agent MUST route the release through the applicable pre-release lane(s): **product ship safety** and, when needed, **framework amendment safety**. The routing rules are load-bearing:

1. **Product ship lane** — when the current cycle actually ships implementation behavior, the agent MUST complete the Release Readiness Review defined in [`release-readiness.md`](./release-readiness.md). That checklist owns tests, coverage, rollback readiness, operational readiness, security/privacy review, lessons consolidation, and the other ship-facing checks. A non-shipping steady-state cycle MAY skip this lane, but only when no ship or deploy is occurring.
2. **Framework amendment lane** — when the release diff changes framework rules or rule-enforcement artifacts (at minimum `AGENTS.md`, files under `playbooks/`, and validator / harness changes made to implement the same amendment), the agent MUST complete the Amendment Protocol in `playbooks/principles-gates.md` separately. SYNC-IMPACT applies only to changed canonical framework files (`AGENTS.md`, `playbooks/*.md`); the amendment lane owns semver classification, SYNC-IMPACT, the diff-scoped derived-doc sweep, validator pass, and the finite amendment evidence bundle.

If both lanes apply, both MUST pass before ship. Neither lane substitutes for the other. An implementation MAY satisfy Phase 3 completion while one or both lanes remain on hold; the ship decision is `Go` or `Conditional Go` only when every applicable lane reaches that outcome per `principles-gates.md` Gate Outcome Vocabulary.

## Post-Completion Housekeeping

After all Phase 3 completion criteria pass, the agent MUST:
1. Archive resolved gaps and superseded decisions to their respective `-archive.md` files
2. Consolidate session log Lessons Learned into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8 — each lesson receives a monotonic `L-{n}` identifier, is categorized per the schema (process | rigor | tooling | scope | rationalization | coordination | other), and cites evidence from the session log. If the same lesson appears across ≥ 2 sessions in this project, the agent MUST evaluate it for a framework amendment; if it appears in this project AND at least one prior project's `lessons.md`, the agent MUST draft a `framework` gap entry per the Amendment Protocol in `principles-gates.md`
3. Reset `phase.md` Handoff Context for the next development cycle
4. Run a final gap scan — any non-critical gaps that accumulated during implementation SHOULD be evaluated for the next cycle

In `steady-state` mode, completing housekeeping closes the current cycle only; the next material work item MUST begin again at Phase 0. In `finite-delivery` mode, the project MAY remain at terminal completion until new scope is explicitly opened.
