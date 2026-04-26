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
id: playbooks/release-readiness
title: Release Readiness Review
version: 1.2.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 3-implement
severity: normative
mechanical_items: 14
judgment_items: 5
mixed_items: 0
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/principles-gates.md
  - playbooks/standards.md
  - playbooks/03-implement.md
  - playbooks/gaps.md
supersedes: null
---

# Release Readiness Review

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **artifact**, **canonical**, **gap**, **review**, **spec**, **verify**.

## Purpose

A Phase 3 pre-release sub-flow checklist the agent MUST complete before shipping an implementation (versioned ship or production deploy) in either lifecycle mode. It is evaluated per release or shipping cycle, not as a once-ever product-finality ritual. Adapted from the Kubernetes Enhancement Proposal (KEP) Production Readiness Review. Shared gate duties remain canonical in `AGENTS.md`, `principles.md`, and `principles-gates.md`; this checklist covers the ship-specific delta for **product ship safety only**. Every item MUST return a concrete evidence string, `N/A` with justification, or `FAIL` — the agent MUST NOT advance to release without a clean pass or explicit deviation per the Amendment Protocol in `principles-gates.md`.

Items tagged `[M]` are mechanical (greppable, exit-code-verifiable); `[J]` are judgment (require rendered human-readable assessment).

**Tally:** 14 `[M]` · 5 `[J]` · 0 `[M+J]`.

## Boundary

This playbook owns product ship safety only. It does **not** own semver classification, SYNC-IMPACT updates, derived-document sweeps, validator passes for framework amendments, or other framework-amendment bookkeeping. If a release diff changes framework rules or their enforcement artifacts, the agent MUST run the separate amendment lane in `playbooks/principles-gates.md`; this checklist does not score that lane. Steady-state cycles that do not ship MAY skip this checklist; steady-state cycles that do ship MUST run it.

## Checklist

### Artifacts and markers


- [ ] **[M]** No `[NEEDS CLARIFICATION:` markers remain. Mechanical: `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits (playbook files are intentionally excluded per `identifiers.md`).
- [ ] **[M]** No stale placeholders (`TBD`, `TODO`, `FIXME`, `XXX`, `(forthcoming)`, `(pending)`) remain in shipped files. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b|\((forthcoming|pending)\)' <release-scope>` MUST return zero hits; exceptions MUST be recorded as `deviation` gaps.
- [ ] **[M]** No spec defines a bare `NG-{n}` / `NG-none` label; spec-scope exclusions belong in prose or qualified `audit.md:NG-{n}` references. Mechanical: `grep -nE '^\s*([-*+]\s*)?NG-(\d+|none):' specs/<spec>.md` MUST return zero for every file in `specs/`.
- [ ] **[M]** Every significant behavior in every spec carries an `FR-{n}` or `NFR-{n}` label. Mechanical: per-spec grep count MUST be non-zero.
- [ ] **[M]** Every conformance criterion carries an `SC-{n}` label that cross-references `FR-` or `NFR-` on the same line. Mechanical: every `SC-\d+:` line MUST contain an `FR-` or `NFR-` reference.
- [ ] **[M]** Every spec declaring a cross-trust-boundary interface has a non-empty Machine-readable Contract subsection. Mechanical: for every spec with `cross-trust-boundary` in its Scope section, `grep -cE '^\*\*schema:\*\*' specs/<spec>.md` MUST return ≥ 1 (or the spec MUST explicitly record `schema: N/A — internal only` with justification).
- [ ] **[M]** Release-scope tests added or edited after adoption cite a path-qualified `specs/<spec>.md:SC-{n}` or `specs/<spec>.md:FR-{n}` in at least one of the two accepted per-test forms (test-name suffix or in-file `Covers:` comment). Mechanical: diff-guided inspection of touched post-adoption tests confirms an accepted form is present; `grep -rnE '^\s*(//|#)\s*Covers:\s*specs/[^ ,:]+\.md:(SC|FR)-[0-9]+|covers_[A-Za-z0-9_]+_(SC|FR)_[0-9]+' tests/ src/` returns ≥ the count of declared `SC-{n}` entries across all specs, and `python3 validate.py --product-ship` check 13 confirms set coverage on the fully qualified `specs/<spec>.md:SC-{n}` identifiers. Untouched pre-adoption tests remain exempt only when covered by the canonical `grandfathered` exception in `03-implement.md` / `gaps.md`.
- [ ] **[M]** Every frontmatter block parses as valid YAML and carries all required fields (`id`, `title`, `version`, `last_reviewed`, `applies_to`, `severity`, `mechanical_items`, `judgment_items`, `mixed_items`, `references`, `supersedes`). Mechanical: `python3 validate.py --product-ship` exit 0 (product-ship mode preserves release-facing checks such as validator check #1 while skipping amendment-lane-only checks 16-17).

### Gaps and deviations

- [ ] **[M]** Zero open `conditional` gaps whose trigger has fired. Mechanical: per-entry check — for every `conditional` gap, the agent MUST evaluate whether the trigger condition has been met; if yes and status is open, gate fails.
- [ ] **[M]** Zero expired `deviation` gaps. Mechanical: per-entry check — for every `deviation` gap, the agent MUST evaluate whether its `Expiry condition:` has been met; if yes and status is still open, gate fails.
- [ ] **[J]** Top 3 audit risks are addressed or explicitly carried as residual risk. Judgment: the agent MUST restate each top-3 risk from `.agent-state/audit.md` and cite the decision, spec, or real `G-{n}` entry that addresses it (for example, `residual risk tracked in G-{n}`).
- [ ] **[J]** Every open `scope-reduction` gap MUST carry explicit user sign-off in the session log. The required format is scope-proportional per the `00-audit.md` Scope-Proportional Ceremony Matrix → Scope-reduction sign-off row:
  - **`micro` / `small`** (solo or low-coordination contexts): `G-{n}: user-signed-off on {YYYY-MM-DD UTC}` is sufficient. The literal `UTC` suffix is REQUIRED so the date is unambiguous when sessions cross time zones. Mechanical: for each open `scope-reduction` `G-{n}`, `grep -qE 'G-{n}: user-signed-off on 20[0-9]{2}-[0-9]{2}-[0-9]{2} UTC\b' .agent-state/phase.md` MUST succeed. Attribution-laundering risk is negligible at solo scope; the simpler line is auditable enough.
  - **`standard` / `large`**: full git-email anchored form REQUIRED — `G-{n}: user-signed-off by {git-email} on {ISO-8601-UTC-timestamp}` where `{git-email}` matches `git config user.email` on the signing agent's machine (or a `.mailmap` entry) AND is re-verifiable via `git log --format='%ae' | grep -F '{git-email}'` returning ≥ 1 commit on the signing branch. Example: `G-12: user-signed-off by alice@example.com on 2026-04-17T14:30:00Z`. Mechanical adjunct: for each open `scope-reduction` `G-{n}`, `grep -qE 'G-{n}: user-signed-off by [^ ]+@[^ ]+ on 20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z' .agent-state/phase.md` MUST succeed. The git-email anchor prevents attribution laundering ("signed off by user" or human-readable names without email addresses do not pass at this tier).

  Judgment (all scopes): sign-offs that recycle the same boilerplate phrase across multiple gaps are not substantive — the reviewer MUST confirm each is a distinct, informed decision that the user saw the scope reduction and accepted the consequences. Resolved/history entries are excluded because only matching open IDs are checked. This check prevents the "silent deferral despite tracking" risk — a gap entry alone is insufficient when the deferral materially reduces the shipped product vs. decided scope.

### Testing and verification

- [ ] **[M]** All test suites pass. Mechanical: test-runner exit code 0 on the canonical test command for the project.
- [ ] **[M]** Coverage targets met per the test strategy decision (D-10). Mechanical: coverage report value ≥ target; when D-10 adopts the default security-critical branch-coverage target, branch coverage ≥ 70% per `standards.md` Testing → Coverage target.

### Operational readiness

- [ ] **[J]** Post-Completion Control outputs (mistake-proofing hooks, SOPs, reaction plans, guardrails) per `03-implement.md` are present. Judgment: each of the four is present OR a `conditional` gap entry tracks its production.
- [ ] **[M]** Rollback protocol is documented and tested. Mechanical: `03-implement.md` Rollback Protocol section exists; for this release, either the protocol was exercised (dry run or real) or a `deviation` gap records the exemption.
- [ ] **[J]** Lessons from this project have been consolidated into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8. Judgment: the file has entries with `L-{n}` identifiers matching the session log's Lessons Learned columns, and recurring patterns are flagged as candidates.

### Security and privacy

- [ ] **[M]** No secrets in the repository. Mechanical: secret-scanning tool (trufflehog, gitleaks, or equivalent) exit code 0; exception list exists for any false positives.
- [ ] **[J]** Security considerations section exists and is substantive for every spec. Judgment: "substantive" means it names trust boundaries and enumerates applicable threats, not "applicable security practices apply" boilerplate.

## Outcome

The agent MUST report the release-readiness gate outcome using the canonical Gate Outcome Vocabulary in [`principles-gates.md`](./principles-gates.md). This playbook does not redefine those five outcomes; it applies them directly to the release decision. If the agent also summarizes session/task status to the user, that completion status (`DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`) is reported separately per `principles.md`.

Release-specific application follows the canonical gate model: shipment MAY proceed only when the gate outcome is `Go` or `Conditional Go`; it MUST NOT proceed on `Hold`, `Recycle`, or `Kill`.

## Relationship to Phase 3 Completion Criteria

This Phase 3 sub-flow is stricter than the Phase 3 Completion Criteria in `03-implement.md`. Phase 3 completion determines whether an implementation or current steady-state cycle is "done"; Release Readiness determines whether that done cycle is ready to *ship*. A combined release that also changes framework rules MUST satisfy this checklist **and** the separate amendment lane in `playbooks/principles-gates.md`. In that case, the implementation is "complete" but shipment remains "on hold" until every applicable lane is clean.
