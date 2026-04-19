<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/release-readiness
title: Release Readiness Review
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: 3-implement
severity: normative
mechanical_items: 21
judgment_items: 8
mixed_items: 1
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/standards.md
  - playbooks/03-implement.md
  - playbooks/gaps.md
  - CHANGELOG.md
supersedes: null
---

# Release Readiness Review

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **artifact**, **canonical**, **gap**, **review**, **spec**, **verify**.

## Purpose

A mechanical pre-release checklist the agent MUST complete before any release (versioned ship, production deploy, or terminal-phase completion). Adapted from the Kubernetes Enhancement Proposal (KEP) Production Readiness Review. Every item MUST return a concrete evidence string, `N/A` with justification, or `FAIL` — the agent MUST NOT advance to release without a clean pass or explicit deviation per the Amendment Protocol.

Items tagged `[M]` are mechanical (greppable, exit-code-verifiable); `[J]` are judgment (require rendered human-readable assessment).

**Tally:** 19 `[M]` · 8 `[J]`.

## Checklist

### Rules compliance

- [ ] **[M]** Every MUST in `AGENTS.md` and every playbook is satisfied. Mechanical: `grep -rnE '\bMUST\b' AGENTS.md playbooks/` enumerates the list; each hit MUST be traceable to evidence. If any MUST is not satisfied, record it as a `deviation` gap entry per the Amendment Protocol — an open MUST blocks release.
- [ ] **[M]** Every MUST NOT is not violated. Same enumeration process against `MUST NOT`.
- [ ] **[J]** Every SHOULD is either followed or an explicit deviation is recorded. Judgment: for each `SHOULD`, the agent MUST state "followed" or "deviation recorded as G-{n}".
- [ ] **[M]** All `[M]` gate items across all phases produce clean evidence (grep output, exit code 0, file existence confirmation). Mechanical: per-phase aggregation from `phase.md` session log.
- [ ] **[J]** All `[J]` gate items across all phases have rendered judgment recorded. Judgment: per-phase aggregation; bare `pass` without rationale is insufficient.

### Artifacts and markers

- [ ] **[M]** No `[NEEDS CLARIFICATION:` markers remain. Mechanical: `grep -rnE '\[NEEDS CLARIFICATION:' specs/ .agent-state/audit.md .agent-state/decisions.md .agent-state/gaps.md` MUST return zero hits (playbook files are intentionally excluded per `identifiers.md`).
- [ ] **[M]** No stale placeholders (`TBD`, `TODO`, `FIXME`, `XXX`, `(forthcoming)`, `(pending)`) remain in shipped files. Mechanical: `grep -rnE '\b(TBD|TODO|FIXME|XXX)\b|\((forthcoming|pending)\)' <release-scope>` MUST return zero hits; exceptions MUST be recorded as `deviation` gaps.
- [ ] **[M]** Every spec has a non-empty Non-Goals section or declares `NG-none` with justification. Mechanical: `grep -cE '\bNG-(\d+|none)\b' specs/<spec>.md` MUST be non-zero for every file in `specs/`.
- [ ] **[M]** Every significant behavior in every spec carries an `FR-{n}` or `NFR-{n}` label. Mechanical: per-spec grep count MUST be non-zero.
- [ ] **[M]** Every conformance criterion carries an `SC-{n}` label that cross-references `FR-` or `NFR-` on the same line. Mechanical: every `SC-\d+:` line MUST contain an `FR-` or `NFR-` reference.
- [ ] **[M]** Every spec declaring a cross-trust-boundary interface has a non-empty Machine-readable Contract subsection. Mechanical: for every spec with `cross-trust-boundary` in its Scope section, `grep -cE '^\*\*schema:\*\*' specs/<spec>.md` MUST return ≥ 1 (or the spec MUST explicitly record `schema: N/A — internal only` with justification).
- [ ] **[M]** Every test cites an `SC-{n}` or `FR-{n}` in at least one of the three accepted forms (commit trailer, test-name suffix, in-file comment). Mechanical: `grep -rnE '(Covers:|covers_)(SC|FR)-\d+' tests/ src/` returns ≥ the count of `SC-{n}` entries across all specs; untraced tests MUST be recorded as `scope-reduction` gaps or fixed.
- [ ] **[M]** Every frontmatter block parses as valid YAML and carries all required fields (`id`, `title`, `version`, `last_reviewed`, `applies_to`, `severity`, `mechanical_items`, `judgment_items`, `mixed_items`, `references`, `supersedes`). Mechanical: `python3 validate.py` exit 0 (the validator's check #1 enumerates the same 11 fields).

### Version and changelog

- [ ] **[M]** `AGENTS.md` Version banner matches every playbook's frontmatter `version:` field. Mechanical: all version fields agree.
- [ ] **[M]** `CHANGELOG.md` has an entry for the current version with `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security` subsections as applicable, and classifies the bump as MAJOR / MINOR / PATCH per the Versioning Policy. Mechanical: `grep -E '^## \[v?{VERSION}\]' CHANGELOG.md` returns exactly one line.
- [ ] **[M]** Every file amended since the last release has either a SYNC-IMPACT HTML comment dated after the last release OR is exempt under the non-amendment edits clause in `playbooks/principles.md` Sync Impact Reports. Mechanical: diff-guided inspection of top-of-file region for every changed file.
- [ ] **[J]** The CHANGELOG entry's `Added` / `Changed` / `Fixed` subsections accurately describe the shipped changes. Judgment: a skeptical reader who has not seen the code MUST be able to infer the scope of the release from the CHANGELOG alone.

### Gaps and deviations

- [ ] **[M]** Zero open `critical` gaps in `.agent-state/gaps.md`. Mechanical: `grep -A1 '^### G-' .agent-state/gaps.md | grep -B1 'Severity:\*\* critical' | grep 'Status:\*\* open'` MUST return zero hits.
- [ ] **[M]** Zero open `conditional` gaps whose trigger has fired. Mechanical: per-entry check — for every `conditional` gap, the agent MUST evaluate whether the trigger condition has been met; if yes and status is open, gate fails.
- [ ] **[M]** Zero expired `deviation` gaps. Mechanical: per-entry check — for every `deviation` gap, `Expiry condition:` MUST be either "not yet met" (still valid) or "met + resolved".
- [ ] **[J]** Top 3 audit risks are addressed or explicitly accepted. Judgment: the agent MUST restate each top-3 risk from `.agent-state/audit.md` and cite the decision, spec, or accepted-risk gap entry that addresses it.
- [ ] **[J]** Every `scope-reduction` gap with severity `critical` OR linked to a decision in `D-1..D-12` MUST carry explicit user sign-off in the gap's Resolution field, formatted as `user-signed-off by {git-email} on {ISO-8601-UTC-timestamp}` where `{git-email}` matches `git config user.email` on the signing agent's machine (or a `.mailmap` entry) AND is re-verifiable via `git log --format='%ae' | grep -F '{git-email}'` returning ≥ 1 commit on the signing branch. Example: `user-signed-off by alice@example.com on 2026-04-17T14:30:00Z`. Judgment: sign-offs that recycle the same boilerplate phrase across multiple gaps are not substantive — the reviewer MUST confirm each is a distinct, informed decision that the user saw the scope reduction and accepted the consequences. Mechanical adjunct: `grep -cE '^- \*\*Resolution:\*\*.*user-signed-off by [^ ]+@[^ ]+ on 20[0-9]{2}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z' .agent-state/gaps.md` MUST equal the count of open critical scope-reduction gaps (or critical-linked-to-D-1..D-12 gaps, whichever is higher). The git-email anchor prevents attribution laundering ("signed off by user" or human-readable names without email addresses no longer pass). This check prevents the "silent deferral despite tracking" risk — a gap entry alone is insufficient when the deferral materially reduces the shipped product vs. decided scope.

### Testing and verification

- [ ] **[M]** All test suites pass. Mechanical: test-runner exit code 0 on the canonical test command for the project.
- [ ] **[M]** Coverage targets met per the test strategy decision (D-10). Mechanical: coverage report value ≥ target; branch coverage ≥ 70% for security-critical paths per `standards.md` D14.
- [ ] **[M+J]** Verification Coverage Matrix from the final phase gate MUST be complete and all-clean. Mechanical: the session log contains a filled matrix per `principles.md` Verification Coverage Matrix with every Exercised cell = yes, every Result cell = clean, every Re-verified cell = yes or N/A. Judgment: evidence cited for each perspective is genuine and covers the release scope.

### Operational readiness

- [ ] **[J]** Post-Completion Control outputs (mistake-proofing hooks, SOPs, reaction plans, guardrails) per `03-implement.md` are present. Judgment: each of the four is present OR a `conditional` gap entry tracks its production.
- [ ] **[M]** Rollback protocol is documented and tested. Mechanical: `03-implement.md` Rollback Protocol section exists; for this release, either the protocol was exercised (dry run or real) or an accepted-risk `deviation` gap records the exemption.
- [ ] **[J]** Lessons from this project have been consolidated into `.agent-state/lessons.md` per `principles.md` Required Behaviors #8. Judgment: the file has entries with `L-{n}` identifiers matching the session log's Lessons Learned columns, and recurring patterns are flagged as candidates.

### Security and privacy

- [ ] **[M]** No secrets in the repository. Mechanical: secret-scanning tool (trufflehog, gitleaks, or equivalent) exit code 0; exception list exists for any false positives.
- [ ] **[J]** Security considerations section exists and is substantive for every spec. Judgment: "substantive" means it names trust boundaries and enumerates applicable threats, not "applicable security practices apply" boilerplate.

## Outcome

The agent MUST report the release-readiness outcome using the Completion Status Protocol in `principles.md` and the Gate Outcome Vocabulary:

- **Go** — every `[M]` item produced clean evidence and every `[J]` item has a rendered judgment that is acceptable. Release proceeds.
- **Conditional Go** — every `[M]` item produced clean evidence, but one or more `[J]` items have acceptable-but-deferrable concerns recorded as `conditional` gap entries with explicit triggers. Release proceeds; conditions MUST be tracked to resolution.
- **Hold** — any `[M]` item failed or any `[J]` item's concern is load-bearing. Release does NOT proceed. Specific failing items are addressed and the questionnaire is re-run.
- **Recycle** — multiple `[M]` failures or broad `[J]` concerns indicate the release scope itself is premature. The agent MUST return to an earlier phase per the Phase Regression Procedure in `AGENTS.md`.
- **Kill** — per `AGENTS.md` Phase Gates, reserved for user-authorized project cancellation.

## Relationship to Phase 3 Project Completion Criteria

This questionnaire is stricter than the Phase 3 Project Completion Criteria. Completion Criteria determine whether an implementation is "done"; Release Readiness determines whether a "done" implementation is ready to *ship*. An implementation MAY satisfy Project Completion while failing Release Readiness — typically when operational readiness, versioning/changelog discipline, or security/privacy review items are open. In that case, the implementation is "complete" but the release is "on hold" until the release-readiness gaps close.
