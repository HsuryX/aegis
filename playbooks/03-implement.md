<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/03-implement
title: Phase 3: Implementation
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: 3-implement
severity: normative
mechanical_items: 8
judgment_items: 10
mixed_items: 3
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

## Pre-Implementation Check

Before writing any code, the agent MUST:
1. Confirm via `phase.md` that the project is in phase 3
2. Read `playbooks/standards.md`
3. Check the project's scope classification in `audit.md` — **micro-scope** projects do not have formal decisions or specifications; the agent MUST proceed directly to the TDD workflow using `standards.md` as the quality bar. Steps 4–7 below apply to small, standard, and large scope only.
4. Read `decisions.md` — know what is decided, including the test strategy
5. Identify which decision(s) the intended change implements
6. Identify which specification(s) the change implements — tests MUST be derived from these specifications, not from the decisions alone
7. If no decision or specification covers the change, the agent MUST STOP — return to Design phase (if a decision is missing) or Spec phase (if the decision exists but no spec does)

Implementation is not the place to discover missing design. If the agent finds itself making architectural judgment calls while coding, that is evidence of a design gap — the agent MUST treat it as a gap, not as an opportunity to decide on the fly.

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
- `Implements: D-3, FR-7` — decision plus functional requirement from a spec
- `Covers: SC-{n}` — commit adds test coverage for a success criterion
- `Closes: G-{n}` — commit resolves a tracked gap

Multiple trailer types MAY coexist in one commit message. A change that traces to no decision MUST NOT be made — except for: (1) maintenance changes (typo fixes, formatting, dependency updates, documentation corrections) which MAY use `chore(scope): description` without a decision trace, and (2) micro-scope projects where formal decisions do not exist — the agent MAY use `type(scope): description` per `standards.md` Git Conventions. If a "maintenance" change starts requiring judgment calls, it has crossed into design territory and the agent MUST open a decision. If a micro-scope project starts requiring architectural judgment calls, it has outgrown its scope classification and the agent MUST reclassify per `00-audit.md`.

### Test traceability

Every test MUST cite the `SC-{n}` (conformance criterion) or `FR-{n}` (functional requirement) it validates. The reference MAY appear in any of three forms — all three are accepted by the Phase 3 gate check:

- **Commit trailer** — `Covers: SC-3, FR-7` in the commit message that adds the test (preferred when multiple tests are added in one commit)
- **Test-name suffix** — `test_auth_denies_expired_token_covers_SC_3` (preferred for table-driven tests where the suffix survives refactor)
- **In-file comment** — `// Covers: SC-3` or `# Covers: SC-3` as the first line of the test body (preferred when tests are committed separately from the feature)

At the Phase 3 gate, mechanical check: `grep -rnE '(Covers:|covers_)(SC|FR)-\d+' tests/ src/ --include='*.py' --include='*.ts' --include='*.go' --include='*.rs'` MUST return a count at least equal to the count of `SC-{n}` entries across all specs. Untraced tests indicate spec coverage gaps — every test exercises some behavior, and every spec'd behavior MUST have at least one test.

**Legacy-test grandfathering at adoption time.** When aegis is adopted on a project with pre-existing tests, the traceability requirement applies ONLY to tests added or edited after adoption. Pre-adoption tests MAY be grandfathered under a single project-level gap entry (type: `grandfathered`, severity: `info`, Trigger: adoption date, Expiry condition: "until 100% of originally-grandfathered tests have been edited, superseded, or deleted"). The gap MUST list the initial test-file set (or a `git log` anchor) so the expiry is verifiable. Grandfathering MUST NOT be invoked retroactively on tests modified after adoption — any touched test MUST carry the `Covers:` trailer, suffix, or comment per the three accepted forms above.

### Commit message format enforcement

Commit messages MUST match the conventional-commits regex and MUST include the `Implements:` trailer for non-maintenance commits:

- Header regex: `^(feat|fix|refactor|docs|test|chore|perf|ci)(\([a-z0-9-]+\))?: .+$`
- Trailer requirement: `grep -E '^Implements: D-[0-9]+' <commit-msg-file>` MUST return a match UNLESS the commit type is `chore` OR scope classification is micro
- Exceptions logged: maintenance commits (`chore:`) skip the trailer; micro-scope projects follow `standards.md` Git Conventions exception path

Enforcement MAY be automated via a `commit-msg` git hook (see `harness/claude-code/hooks-cookbook.md` → Commit validation hook). At the Phase 3 gate, mechanical check on the last commit: header matches the regex AND trailer is present (or exception applies).

## Hard Rules

1. **No architectural discovery** — if the architecture needs to change, the agent MUST stop coding, update `decisions.md`, and re-enter Design phase
2. **No copy-paste from reference material** — the agent MUST use `_legacy/` or external sources for behavioral clues and MUST write new code fresh
3. **No silent scope change** — the agent MUST implement exactly what is decided. The agent MUST NOT add capability beyond specifications and MUST NOT silently drop requirements. After implementation, the agent MUST verify every specification requirement is present — silent scope reduction is as harmful as scope creep. Silent deferral is forbidden; explicit deferral is permitted only when tracked. The distinction is load-bearing:
   - **Silent deferral (forbidden)**: dropping, weakening, or postponing a specified requirement without a corresponding entry in `gaps.md`. The following scope-reduction phrases are markers for silent deferral and MUST NOT appear in code, comments, or commit messages: "v1", "simplified version", "static for now", "placeholder", "defer to follow-up", "good enough for now".
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
- [ ] **[M]** Every new test MUST cite an `SC-{n}` or `FR-{n}` in one of the three accepted forms (commit trailer, test-name suffix, or in-file comment; see Traceability → Test traceability). Mechanical: diff-scoped grep for `(Covers:|covers_)(SC|FR)-\d+` in the added test files MUST return ≥ 1 reference per new test case.
- [ ] **[M]** Commit message MUST match conventional-commits format AND carry the `Implements: D-{n}` trailer (exceptions: `chore(...)` and micro-scope). Mechanical: the most recent commit message MUST satisfy the Traceability → Commit message format enforcement regex.
- [ ] **[J]** If this change affects a specification, the spec MUST be updated or deferral MUST be recorded in `gaps.md`
- [ ] **[J]** Observability requirements from the observability model decision MUST be implemented (structured logging at service boundaries, trace context propagation, metrics for identified operations)
- [ ] **[J]** Self-review checklist from `standards.md` MUST pass (delegates to the Self-Review Checklist in `standards.md`)

## Verification Sequence

Ordered by dependency — each step MUST pass before the next is meaningful. After each meaningful implementation change, the agent MUST run the sequence in this order. The agent MUST record actual command output as evidence and MUST NOT check boxes from memory or confidence.

**Evidence loop (applies to every step below):** for each verification step: (1) identify the exact command that proves the claim, (2) run it fresh in the current session (not from memory or a prior run), (3) read the complete output including exit code, (4) evaluate whether the output confirms the claim — if no, state the actual status; if yes, state the claim with the output as evidence, (5) only then mark the step as passed. This 5-step loop is the mechanical definition of "verified" throughout the framework.

1. **Build** — the agent MUST verify the project compiles/builds without errors
2. **Type check** — the agent MUST run the type checker (if applicable)
3. **Lint** — the agent MUST run the project linter (if configured)
4. **Test** — the agent MUST run the full test suite and MUST record pass count and coverage percentage
5. **Security scan** — the agent MUST check for hardcoded secrets and known vulnerabilities (if tooling exists)
6. **Self-diff review** — the implementing agent MUST review its own diff to confirm it matches the design intent and nothing unintended was introduced. This is **self-review** by the implementing agent and is **distinct** from the subsequent Code Review section below, which REQUIRES a separate agent in a fresh context for standard and large scope projects. Both are required; neither substitutes for the other — the self-diff review catches "did I write what I intended?", while Code Review catches "does what was written match the spec and standards when read without the implementer's mental model?"

The agent MUST NOT claim a change is complete until all applicable steps produce clean output with recorded evidence. Each claim REQUIRES specific proof:

| Claim | Required Evidence | NOT Sufficient |
|-------|------------------|----------------|
| "Tests pass" | Test command output showing 0 failures | Previous run, "should pass", partial suite |
| "Build succeeds" | Build command with exit 0 | Linter passing, "looks correct" |
| "Bug fixed" | Test reproducing original symptom now passes | Code changed and assumed fixed |
| "Requirements met" | Line-by-line spec checklist verified | Tests passing (tests may not cover all reqs) |
| "No regressions" | Full test suite output, not just changed tests | Spot-checking a few tests |

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

**Emergency authorization.** When a production-critical issue requires immediate action (production down, active security breach, data loss, or user-declared emergency), the normal phase sequence MAY be bypassed via this workflow. This is the **emergency protocol** referenced from `AGENTS.md`. The agent MUST NOT self-authorize an emergency — the agent MUST propose the emergency to the user first; the user MUST approve before the workflow proceeds. The emergency protocol is not a shortcut for impatience — if the issue can wait for the normal workflow, the agent MUST use the normal workflow. The scope of an approved emergency is limited to the specific triggering issue; adjacent cleanup MUST go through the normal phase workflow.

This workflow MUST be used only for production-critical issues:

1. The agent MUST propose the emergency to the user and obtain approval — the agent MUST NOT self-authorize a phase bypass. The agent MUST record an emergency decision entry `D-{n}: [HOTFIX] {title}` with `Status: emergency` and justification
2. The agent MUST write the minimal scoped fix with full test coverage for the specific issue
3. The agent MUST run the Verification Sequence — no exceptions, even under time pressure
4. The agent MUST deploy following the project's deployment process
5. The agent MUST open a reconciliation gap entry `G-{n}` with severity `critical` and type `decision`, referencing the emergency decision
6. Within 48 hours, the agent MUST either ratify the emergency decision into the design (add full alternatives analysis to the decision entry, update specs) or revert the hotfix and implement a proper fix through the normal phase workflow

## Adversarial Gate Check

Before evaluating the Project Completion Criteria below, the agent MUST run an adversarial review subagent per `principles-gates.md` Adversarial Review Protocol. This review is distinct from the Code Review section above: Code Review validates the diff's specification fidelity; adversarial review catches completeness gaps across the whole implementation — specs with no matching code, decisions with `Confirmation` fields that describe a mechanism but the mechanism is absent, prose in session logs that says "verified" without recorded command output, `Deferred` decisions with expired trigger conditions that were never resolved, or `[NEEDS CLARIFICATION]` markers still present in any authored artifact.

**Scope:** required for standard and large scope projects; optional for micro and small. **Input:** the full `specs/` directory, `decisions.md`, the session log in `phase.md`, the Verification Sequence evidence blocks, and `gaps.md` (for deferred triggers). **Output:** a list of `file:line` findings. The agent MUST address every finding before the Project Completion Criteria evaluate.

## Project Completion Criteria

Ordered by verification progression: implementation existence → automated verification → quality assurance → state closure → cold-reader navigability. The project is complete when ALL of the following are true. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**HALT AND REPORT.** Evaluate each item below against the Gate Outcome Vocabulary and Three-Tier Gate Criteria in `principles-gates.md`. Report the gate outcome (`Go`, `Conditional Go`, `Hold`, `Recycle`, or `Kill`) using the Completion Status Protocol — include evidence for each `[M]` item and a rendered judgment for each `[J]` item. For `Conditional Go`, record each unmet `[should-meet]` item as a `conditional` gap entry. For `Hold` or `Recycle`, list the specific `[must-meet]` items that fail.

**Tally:** 4 `[M]` · 2 `[M+J]` · 4 `[J]`. **Tiers:** 7 `[must-meet]` · 2 `[should-meet]` · 1 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** Every specification MUST have a corresponding implementation. Mechanical: for each spec, `grep -rn '{spec_path}' src/` returns non-zero OR an implementation map entry references the spec.
- [ ] **[M+J]** **[must-meet]** Every implementation MUST pass its verification sequence with recorded evidence. Mechanical: the session log in `phase.md` contains recorded command output for Build/Type/Lint/Test/Security per the Verification Sequence. Judgment: the evidence actually corresponds to the change (and wasn't pasted from a prior run).
- [ ] **[J]** **[should-meet]** Post-implementation cleanup MUST have been performed on all code
- [ ] **[M]** **[must-meet]** All tests MUST pass with coverage meeting the test strategy targets. Mechanical: test runner exit code 0 + coverage tool output meets or exceeds D-10 target.
- [ ] **[M]** **[must-meet]** No open gaps MAY remain in `gaps.md` (all MUST be resolved or explicitly accepted with justification). Mechanical: `grep -A1 '^### G-' .agent-state/gaps.md | grep 'Status:\*\* open'` MUST return zero hits (or each remaining open gap MUST be explicitly marked as accepted).
- [ ] **[M]** **[must-meet]** No decisions in `Draft` or `Proposed` state MAY remain in `decisions.md` at project completion — every decision referenced by implementation MUST be in `Final` state; decisions not cited by implementation MUST be in `Superseded`, `Rejected`, `not-applicable`, or `Deferred` (with a live trigger condition documented in `Unresolved concerns`). Mechanical: `grep -A1 '^### D-' .agent-state/decisions.md | grep -E 'Status:\*\* (Draft|Proposed)'` MUST return zero hits. Judgment: every `Deferred` decision's trigger condition MUST still be live; expired triggers MUST force transition to `Final` or `Rejected` before project completion.
- [ ] **[J]** **[should-meet]** The self-review checklist MUST pass for every source file (delegates to `standards.md` Self-Review Checklist)
- [ ] **[J]** **[nice-to-have]** A cold reader MUST be able to navigate from specification to implementation and verify compliance
- [ ] **[J]** **[must-meet]** Product validation: the implemented system MUST address the goals, non-goals, and success criteria from the Product surface in `audit.md` — the agent MUST walk through each original product requirement (SC-n, NG-n labels from [`identifiers.md`](./identifiers.md)) and confirm each is met, explicitly deferred, or renegotiated with the user
- [ ] **[M+J]** **[must-meet]** Verification Coverage Matrix complete: all 5 perspectives exercised with clean results. Mechanical: the session log contains a filled matrix with no `no` or `findings` entries. Judgment: the evidence cited for each perspective is genuine. See `principles-gates.md` Verification Coverage Matrix — the matrix is the canonical structured record of multi-perspective verification.

## Post-Completion Control

After all Project Completion Criteria pass and before Post-Completion Housekeeping, the agent MUST produce the four DMAIC Control outputs. Their purpose is to ensure that the completed implementation **stays correct** after the agent ends the session — drift caught at the gate is cheap; drift caught months later is expensive.

1. **Mistake-proofing hooks** — for every rule the agent discovered during implementation that is mechanically checkable (greppable, exit-code-verifiable, pattern-matchable) and was being enforced only by discipline, the agent MUST propose a hook in the relevant harness (`harness/claude-code/hooks-cookbook.md` for the Claude Code harness; equivalent in other harnesses) or a CI gate. Proposals are recorded in the session log; adoption is subject to the Amendment Protocol if the rule lives in a playbook.
2. **Standard Operating Procedures (SOPs)** — for every recurring operational task surfaced during implementation (database migration rollout, secret rotation, deployment promotion, incident triage), the agent MUST either cite the existing procedure in the repository or draft a new procedure. Procedures live under `docs/` or `playbooks/` per D-12 (Documentation structure). An operation performed once without a procedure is acceptable; twice without a procedure is a `failure-pattern` gap.
3. **Reaction plans** — for each known failure mode of the implemented system (per the spec's error semantics and the `gaps.md` entries marked `deferred`), the agent MUST record the detection signal, the responder (human or automated), the first mitigation step, and the escalation path. Reaction plans live alongside the SOPs. A failure mode without a reaction plan is a gap of type `analysis` — the implementation is not yet production-complete.
4. **Guardrails** — for every runtime invariant that MUST hold but is not verified by tests (rate limits, quotas, circuit breakers, resource caps, concurrency limits), the agent MUST record the invariant, where it is enforced, and how to verify it is still enforced after future changes. Guardrails that depend on external configuration (cloud IAM, feature flags, environment variables) MUST cite the canonical source of truth.

Control outputs are recorded in the session log and cross-referenced from the Post-Completion Housekeeping archive step. The agent MUST NOT advance to housekeeping with any of the four outputs missing; missing outputs become `conditional` gap entries linked to the project's terminal completion verdict.

## Pre-Release Gate

After Post-Completion Control produces its four outputs and before Post-Completion Housekeeping runs, the agent MUST complete the Release Readiness Review defined in [`release-readiness.md`](./release-readiness.md). Release Readiness is stricter than the Project Completion Criteria above — Project Completion determines whether the implementation is "done"; Release Readiness determines whether a "done" implementation is ready to *ship*. The checklist enforces MUST satisfaction, `[M]` evidence, `[J]` rendered judgment, stale-marker sweep, Non-Goals coverage, SYNC-IMPACT currency, version + CHANGELOG alignment, security review, rollback readiness, and lessons consolidation via `.agent-state/lessons.md` (per `principles.md` Required Behaviors #8). An implementation MAY satisfy Project Completion while failing Release Readiness — typically when versioning / changelog discipline, operational readiness, or security review items are open. In that case, the implementation is "complete" but the release is "on hold" until the release-readiness gaps close. The Gate Outcome of the Release Readiness Review (Go / Conditional Go / Hold / Recycle / Kill per `principles-gates.md` Gate Outcome Vocabulary) is the ship decision.

## Post-Completion Housekeeping

After all completion criteria pass, the agent MUST:
1. Archive resolved gaps and superseded decisions to their respective `-archive.md` files
2. Consolidate session log Lessons Learned into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8 — each lesson receives a monotonic `L-{n}` identifier, is categorized per the schema (process | rigor | tooling | scope | rationalization | coordination | other), and cites evidence from the session log. If the same lesson appears across ≥ 2 sessions in this project, the agent MUST evaluate it for a framework amendment; if it appears in this project AND at least one prior project's `lessons.md`, the agent MUST draft a `framework` gap entry per the Amendment Protocol in `AGENTS.md`
3. Reset `phase.md` Handoff Context for the next development cycle
4. Run a final gap scan — any non-critical gaps that accumulated during implementation SHOULD be evaluated for the next cycle
