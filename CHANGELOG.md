# Changelog

All notable changes to aegis are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versioning follows the policy below.

## Update Guide for Downstream Projects

This guide assumes the project imported aegis from its canonical repository and keeps `AGENTS.md`, `playbooks/`, `harness/`, and `validate.py` as framework files updated from upstream. Projects that forked aegis to maintain their own customized framework treat the forked repository as canonical and apply the same guide with the fork as the upstream (substitute `/path/to/aegis/` in the commands below with the fork's repository root). Either way, `.agent-state/` remains project-owned and is NEVER overwritten by an upgrade.

When upgrading a downstream project from aegis `vX.Y.Z` to a newer version:

1. Read the CHANGELOG entry for every intermediate version between yours and the target. Each entry classifies the bump as MAJOR / MINOR / PATCH and lists Added / Changed / Deprecated / Removed / Fixed / Security / Versioning subsections.
2. For each `Changed` or `Removed` item, check whether your local playbook amendments (if any, tracked as `framework` gaps in your `.agent-state/gaps.md` using the canonical lifecycle values — typically `Status: resolved` with the downstream-local change described in `Resolution:`) are affected. Typical conflict points: changes to `D-1..D-12` semantics, new gate items, new frontmatter fields, renamed or removed sections.
3. Copy the updated files from aegis into your project. For most MINOR/PATCH upgrades:
   ```bash
   cp -a /path/to/aegis/playbooks/ ./playbooks/
   cp -a /path/to/aegis/AGENTS.md /path/to/aegis/CHANGELOG.md /path/to/aegis/README.md ./
   cp -a /path/to/aegis/ONBOARDING.md ./  # if present in your aegis version
   cp -a /path/to/aegis/harness/ ./harness/
   cp /path/to/aegis/validate.py ./
   mkdir -p ./tools && cp /path/to/aegis/tools/bootstrap.sh ./tools/
   # Preserve your .agent-state/ and any local overrides.
   ```
4. Run `python3 validate.py` in the target project. Expect exit 0. If a version-consistency check fails, bump the remaining playbook frontmatter to match.
5. If you had local amendments (step 2), re-evaluate each against the new aegis rules. An amendment that conflicts with an upstream rule is either (a) now subsumed by the upstream rule (delete the local amendment), (b) still needed but must be re-expressed on top of the new rule (update the gap and the local change), or (c) a signal that aegis's upstream rule should change (file a `framework` gap upstream).
6. Record the upgrade in your `.agent-state/phase.md` Session Log with the old → new version pair so future agents can trace which SYNC-IMPACT comments they've already honored.

**MAJOR upgrades** (v1 → v2, v2 → v3, etc.) are rare and carry explicit migration instructions in their CHANGELOG entry — a Migration Notes subsection at the top of the version's section. Do not attempt a MAJOR upgrade without reading the Migration Notes.

**Pinning a version.** If you want a downstream project to stay on a specific aegis version, record the pinned version in your project's `AGENTS.md` Version banner and frontmatter. Any upgrade is then explicit and consented.

## Versioning Policy

aegis uses [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) interpreted for a meta-governance framework. Each amendment MUST be classified as MAJOR, MINOR, or PATCH before shipping. `playbooks/principles-gates.md` owns the amendment workflow (user approval, SYNC-IMPACT, derived-doc sweep, validator pass, amendment evidence); this file owns only the bump taxonomy and the release narrative. The policy is binding from v1.0.0 forward.

### MAJOR (X.0.0) — breaking changes

A change is MAJOR when it invalidates prior compliance — that is, when a project that satisfied aegis v{X-1}.Y.Z would no longer satisfy v{X}.0.0 without structural updates. MAJOR changes include:

- Rule priority reordering (the Rule Priority Reference Card is changed in a way that flips conflict outcomes)
- Phase structure change (adding, removing, reordering, or merging phases; changing phase-terminal rules)
- Verdict semantic change (changing what `keep`, `redesign`, or `delete` mean; adding, removing, or replacing a verdict value; or otherwise changing the canonical verdict vocabulary)
- Required decision added (adding to the `D-1..D-12` reserved range)
- State file renamed, moved, or restructured such that reader compatibility breaks
- Workflow gate semantics change (what a `Go` or `Hold` outcome means; adding, removing, or renaming a gate outcome; or changing how tier classification interacts with outcome)
- Canonical gap-model change (adding, removing, renaming, or redefining gap lifecycle statuses, severities, or types)
- Removal of any rule that was load-bearing in prior gates

Compat symlinks or transitional layers MAY be provided for one major version but DO NOT make a MAJOR change MINOR — the semver contract is about the canonical form, not the transitional convenience.

### MINOR (X.Y.0) — additive, backward-compatible

A change is MINOR when it adds capability without invalidating prior compliance. MINOR changes include:

- Additive rules, fields, sections, or playbooks
- New failure pattern
- New labeled artifact families (e.g., `SC-{n}`, `NG-{n}`)
- New required frontmatter field whose absence the existing reader tolerates

A release MAY be classified MINOR even when no new rule is introduced, provided the release touches ≥ 3 playbooks with coordinated integrity fixes, consolidations, or enforcement-clarifying tightenings. PATCH is reserved for single-file or single-rule clerical corrections.

### PATCH (X.Y.Z) — clarifications, no semantic change

A change is PATCH when the semantics of every rule before and after are identical. PATCH changes include:

- Typo fixes, grammar polish, prose tightening
- Example improvements that do not change what the rule requires
- Terminology tightening (renaming a term in the glossary where the rename is faithful and a cross-reference sweep is complete)
- Cross-reference corrections (fixing broken pointers)
- Bug fixes in mechanical check commands that restore the originally-intended behavior

### Yanked amendments

Per Keep-a-Changelog convention (v0.0.6+), an amendment that is approved and shipped but later found to be broken or harmful MAY be yanked. A yanked amendment:

- MUST retain its CHANGELOG entry with `[YANKED]` appended to the version header (e.g., `## [v1.4.7] — 2026-05-02 [YANKED]`).
- MUST append a one-paragraph yank explanation immediately under the version header, naming the defect discovered, the detection date, and the version that supersedes (if any).
- MUST trigger a `failure-patterns.md` entry documenting the pattern that led to the defective amendment passing review (answer: what verification step would have caught this? that step becomes the new precedent for the next Amendment Protocol pass).
- MUST trigger an `L-{n}` entry in `.agent-state/lessons.md` per `principles.md` Required Behaviors, with the `Amendment proposal` field naming the detection-step improvement.
- MUST NOT decrement the framework version — yanking is forward-compatible. The yanked version remains in history; a new version ships with the corrected rule (or the absence of a rule if the amendment is withdrawn entirely).
- MUST NOT be used as a routine rollback mechanism. Yanking is reserved for amendments with observed real-world harm (incorrect behavior, security regression, incompatibility). Prose polish or clarity improvements are NOT grounds for yanking — file a new PATCH instead.

Downstream projects that have adopted a yanked version SHOULD upgrade to the superseding version at the earliest session. The CHANGELOG's Update Guide for Downstream Projects applies; in addition, the yank paragraph MUST include upgrade-or-mitigation instructions specific to the defect.

---

## [Unreleased]

No unreleased changes.

<a id="v120"></a>
## [v1.2.0] — 2026-04-25

Framework self-review release. This release tightens aegis as a governance
framework and as a framework that can safely govern its own maintenance:
`AGENTS.md` now has an explicit Framework Maintenance Mode, SYNC-IMPACT comments
are compact routing metadata instead of repeated release essays, Codex is
updated from advisory-only documentation to first-class shipped-but-inactive
templates, Cursor-specific adapter support is removed from the current support
surface, and `validate.py` gains guardrails against instruction-budget bloat and
stale harness capability claims. Phase model, verdict vocabulary, lifecycle
modes, gap taxonomy, gate outcome vocabulary, and agent-neutral governance
semantics are unchanged. SemVer MINOR — this release expands shipped Codex
support and refines the prioritized harness/support-scope guidance while
removing previously shipped Cursor adapter templates from the upstream-managed
copy. Downstream projects using those templates must retain their local copy or
migrate to Claude Code, Codex, or agent-neutral manual/CI backstops.

### Added

- `AGENTS.md` Framework Maintenance Mode: framework files remain read-only for
  governed-project work, but explicitly authorized aegis maintenance may edit
  `AGENTS.md` and `playbooks/` through the Amendment Protocol. For the aegis
  repo itself, `.agent-state/` remains an adopter-facing clean template when the
  user requests a clean release state; finite amendment evidence may live in
  this CHANGELOG and final verification artifacts instead of active ledgers.
- `AGENTS.md` operator-kernel budget: `AGENTS.md` must stay under 32 KiB unless
  every shipped harness that reads it is explicitly configured and documented for
  a larger budget.
- First-class Codex shipped templates under `harness/codex/`: `.codex` command
  rules/hooks/subagents plus `.agents/skills` workflow skills.
- `validate.py` checks for `AGENTS.md` size budget, compact SYNC-IMPACT shape,
  and stale Codex harness claims such as retired "no hooks / no skills" text.

### Changed

- SYNC-IMPACT comments in `AGENTS.md` and `playbooks/*.md` now carry compact
  routing metadata that points to this CHANGELOG for release narrative and
  migration details. This removes duplicated top-of-file prose from every
  framework file while preserving downstream re-read signaling.
- `playbooks/principles-gates.md` Amendment Protocol now supports the
  clean-template framework release exception: when explicitly requested,
  framework-maintenance evidence may be recorded in the changelog instead of
  leaving active `.agent-state/` diffs in the distributed template.
- `harness/capability-matrix.md` now treats Codex as supporting `AGENTS.md`,
  rules, hooks, skills, subagents, config, sandboxing, and approval policies,
  while still classifying shipped aegis Codex templates as inactive until
  installed and tested.
- README and onboarding guidance now distinguish governed-project read-only
  rules from explicitly authorized framework maintenance, and list only Claude
  Code and Codex as prioritized agent adapters.

### Removed

- Long duplicated v1.1.0 SYNC-IMPACT release narratives from every canonical
  framework file header.
- Cursor-specific shipped adapter templates under `harness/cursor/`, including
  the former `.cursor/rules/*.mdc` playbook pointers and Cursor harness README.
- Stale Codex README assertions that Codex lacks hook, skill, or SessionStart
  surfaces.

### Fixed

- Harness documentation no longer implies active enforcement from files merely
  existing under `harness/`.
- The framework-maintenance path no longer conflicts with the default
  governed-project rule that `AGENTS.md` and `playbooks/` are read-only.

### Migration Notes

- Downstream projects should re-copy `AGENTS.md`, `playbooks/`,
  `harness/capability-matrix.md`, `harness/codex/`, `README.md`,
  `ONBOARDING.md`, `validate.py`, and `tools/bootstrap.sh`, and remove
  upstream-managed `harness/cursor/` from the official aegis copy.
- Downstream projects that rely on the former `harness/cursor/` templates should
  keep their existing local copy as project-owned adapter code or migrate to the
  prioritized Claude Code / Codex harnesses. aegis no longer ships or updates
  Cursor-specific templates.
- Projects relying on the old Codex README as proof that Codex had no hook or
  skill surfaces should replace that local guidance and reclassify any Codex
  controls using the control-class / activation-state model in
  `harness/capability-matrix.md`.
- Projects that parse SYNC-IMPACT comments should preserve the same required
  fields but expect compact comments; full release detail now lives in this
  CHANGELOG entry.

### Framework Maintenance Evidence

- Release authority: maintainer-approved v1.2.0 framework-maintenance amendment
  under the Amendment Protocol, with clean-template final state and first-class
  Codex shipped-but-inactive support as release criteria.
- SemVer classification: MINOR. Changed canonical framework files:
  `AGENTS.md` and `playbooks/*.md`; changed derived/supporting files:
  `CHANGELOG.md`, `README.md`, `ONBOARDING.md`, `harness/capability-matrix.md`,
  `harness/codex/`, removed `harness/cursor/`, `tools/bootstrap.sh`, and
  `validate.py`.
- Derived-document sweep: README, onboarding, harness capability matrix, Codex
  README/config/templates, official Codex skill-path correction, and bootstrap
  next steps updated for the new framework-maintenance, Codex capability, and
  Claude+Codex-only priority model.
- Review method and disposition: performed a diff-scoped review from
  structural, semantic, adversarial-compliance, downstream-adopter, and harness
  capability perspectives. Findings addressed before final verification:
  corrected Codex skill discovery to `.agents/skills`, command rules to
  `.rules`, SessionStart matcher coverage to `startup|resume|clear`, anchored
  the PreToolUse matcher to exact edit tools, and aligned the Stop hook failure
  path with Codex blocking semantics; tightened the Codex protected-file
  hook so framework-maintenance bypass requires a maintainer-set environment
  override instead of words inside the pending tool payload; added the Codex
  project-trust precondition for project-local `.codex` templates; removed an
  overclaim that Codex session-start templates could reject incomplete startup;
  removed Cursor-specific adapter templates and current-doc setup paths;
  corrected product-ship skip-number references after validator check
  renumbering;
  and clarified the clean-template exception so semantic-review evidence is
  summarized in this CHANGELOG rather than in active adopter-facing ledgers.
  Review evidence is summarized in this entry rather than a separate release
  artifact.
- Verification evidence:
  - `python3 validate.py` — pass; all checks passed for `AGENTS.md` + 16 playbooks, version 1.2.0.
  - `python3 validate.py --product-ship` — pass; product-ship checks passed, skipped amendment-lane-only checks 17-18.
  - `python3 -m py_compile validate.py harness/codex/.codex/hooks/*.py` — pass.
  - `python3 -m json.tool harness/codex/.codex/hooks.json` — pass.
  - `bash -n tools/bootstrap.sh` — pass.
  - Codex hook smoke tests — pass: SessionStart emits valid hook JSON;
    PreToolUse blocks protected `AGENTS.md` edits even when the pending patch
    contains framework-maintenance wording; `AEGIS_FRAMEWORK_MAINTENANCE=1`
    allows the protected edit path; ordinary `README.md` edits pass; non-edit
    tools are skipped exactly; Stop leaves stdout empty on validation success;
    and Stop returns blocking exit code 2 with stderr details on validation
    failure.
  - Codex template shape checks — pass for subagent TOML required fields,
    `.agents/skills/*/SKILL.md` shape, and `.codex/rules/*.rules` starter
    command rules.
  - Markdown relative link / anchor scan — pass; 61 local links / anchors checked.
  - `git diff --check` — pass.
  - Stale Codex claim scan over README, onboarding, Codex harness, and capability matrix — no matches.
  - `wc -c AGENTS.md` — `18734 AGENTS.md`, below the 32 KiB budget.
- Clean-template confirmation: `git diff -- .agent-state` returned no diff.

## [v1.1.0] — 2026-04-25

Framework refinement release. Adds new capabilities (bounded-change 0 → 3 path, harness security-claim model, Canonical Dependency Edges DAG, Per-phase timing-hooks table for the Adversarial Review Protocol, `phase regression` glossary entry, and the `validate.py check_traceability` rollup metric), extends existing rules (archive-decay re-evaluation under Required Behaviors #7, a concrete protocol for the Cold Read perspective, a date-only UTC variant of the scope-reduction sign-off format for `micro`/`small` projects), removes redundancies (per-phase `## Adversarial Gate Check` stanzas, duplicate Verdict Discipline definition in the glossary, redundant placeholder grep in 02-spec.md Quality Checks, no-longer-needed validator anchor-diversity check), and clarifies several `AGENTS.md` sections (Phase Gates, Implementation Boundary, Workspace Discipline, Session Start Protocol Step 3). Phase model, scope tiers, lifecycle modes, gate-outcome vocabulary, verdict discipline, and the four phases themselves are unchanged. SemVer MINOR — additive and refinement; no rule becomes stricter than v1.0.0 in a way that invalidates prior compliance.

### Added

- Bounded-change 0 → 3 path for mature, already-governed work when existing Accepted/Final decisions and reviewed specs fully cover the requested change (`playbooks/00-audit.md` Bounded-Change Rule).
- Harness security-claim model with explicit control-class (`Executable` / `Backstop` / `Advisory`) and activation-state (`Active now` / `Shipped but inactive` / `Not available here`) classification (`harness/capability-matrix.md`).
- Canonical Dependency Edges subsection seeding the Whole-System Composition Check (`playbooks/01-design.md`). Lists the canonical edges between D-1 through D-12 (e.g., `D-1 → D-2/D-3/D-4/D-5/D-6/D-10/D-11`; `D-3 → D-4/D-7/D-10`; `D-1..D-6 → D-7`). D-13+ entries extend the DAG.
- Adversarial Review Protocol Per-phase timing-hooks table (`playbooks/principles-gates.md`). Phase playbook Phase Gate intros now cite this single owner instead of carrying their own per-phase stanzas.
- Scope-Proportional gate-protocol mini-matrix in `playbooks/principles-gates.md` Scope-Proportional Ceremony so gate evaluators do not need to jump to `00-audit.md` to look up which protocols apply at their tier.
- `phase regression` glossary entry (`playbooks/glossary.md`).
- `validate.py check_traceability` — file-level `Implements:` / `Covers:` rollup over `src/` and `tests/`. Counts files with at least one trailer comment or `covers_*` test-name suffix; emits a stderr warning below 80%, NOT a failure. Vacuous on the framework repo itself. Complementary to `check_sc_coverage_set` (set coverage on declared `SC-{n}` identifiers, which DOES fail).

### Changed

- Required Behaviors #7 (Archive consultation) extended with an archive-decay re-evaluation rule. When a consulted archive entry (`decisions-archive`, `gaps-archive`, `phase-archive`) is ≥ 12 months old AND the current session creates or revises a same-domain entry, the agent SHOULD verify whether the archive's load-bearing assumptions still hold. If they have shifted, the agent MUST record a one-line margin note in the new entry plus a session-log entry; archives remain immutable. Skipping requires a `deviation` gap with justification.
- Cold Read perspective in `playbooks/principles-gates.md` Multi-Perspective Verification gains a concrete protocol: read without prior session memory, flag undefined terms, self-evaluated gates, and adjective thresholds. Distinct from Adversarial Compliance.
- Scope-reduction sign-off format gains a date-only UTC variant for `micro`/`small` projects. The full git-email anchored form remains for `standard`/`large`. New row in the `playbooks/00-audit.md` Scope-Proportional Ceremony Matrix and a corresponding split in the `playbooks/release-readiness.md` checklist. This is a relaxation for low-coordination contexts; the strict form is preserved where attribution-laundering risk is real.
- Session Start Protocol Step 3 integrity-block relaxed: the block now accepts any form citing countable or tool-checkable evidence (timestamp + claimed phase/status + at least one verifiable count or evidence reference such as `validate.py={pass|fail}`); the prior strict templated form is preserved as a reference example. Self-attested prose like "state integrity verified" is still NOT acceptable.
- `playbooks/principles-gates.md` recorded as the explicit canonical owner of verification, evidence, review-core, and gate-outcome semantics.
- `AGENTS.md` gains a dedicated `## Implementation Boundary` section. v1.0.0 carried the implementation rule as a paragraph below the Phase Gates table; v1.1.0 promotes it to a section header and adds a bounded-change summary paragraph pointing at `playbooks/00-audit.md` Bounded-Change Rule (the full eligibility criteria live there).
- `AGENTS.md` Phase Gates table now surfaces Phase 1 gate items (Authority model completeness, Whole-System Composition Check, threat-model applicability) and Phase 2 Proof-class declaration so the always-on kernel makes these visible without requiring the full `01-design.md` / `02-spec.md` load.
- Phase 1 threat-model gate decoupled from `specs/threat-model.md` artifact-existence; the gate now binds to the path D-5 declares (default `specs/threat-model.md`, but D-5 MAY name another path). Missing artifact when applicability is met fails the gate.
- `AGENTS.md` Workspace Discipline second paragraph reformatted from a single run-on paragraph into an intro sentence + 6 bullets covering canonical sources, activation, write denial, Bash subprocess gap, symlink coverage, and local overrides. The Bash-subprocess-gap caveat is new (settings-level write denial does not block Bash subprocess writes — shell-resistant protection still requires OS-level or hook backstops); the rest preserves v1.0.0 content with better scannability.
- Framework-file / workspace discipline language tightened around project-state ledgers and maintainer-controlled framework files.
- Standard / large gate review evidence and `[J]` disposition independence expectations tightened.
- Phase 3 implementation and release routing clarified for bounded-change cycles; product-ship vs framework-amendment lanes split.
- Operator-facing prose contract schema exemptions and public-contract review evidence requirements clarified.
- Scope-reduction marker phrase list (canonical: `validate.py _DEFERRAL_PHRASES`; mirrored in `playbooks/standards.md` Self-Review Checklist, `playbooks/03-implement.md` Hard Rule 3, `harness/cursor/.cursor/rules/phase-3.mdc`) trimmed to unambiguous multi-word forms only — bare tokens (`v1`, `placeholder`) dropped because they match perfectly legitimate technical content. Final list: `simplified version`, `static for now`, `defer to follow-up`, `good enough for now`, `stub for the moment`, `coming in v2`. Adopters running aegis on real code no longer drown in false positives.
- `playbooks/glossary.md` entries for `harness`, `review`, and `STRIDE` compressed to point at canonical owners rather than restate them. Adversarial Gate Check sub-entry redirects to the canonical owner in `principles-gates.md`.
- `playbooks/automation.md` Principle → Rule → Enforcement Matrix row updated to point at the canonical Adversarial Review Protocol owner.

### Removed

- Duplicated Verdict Discipline definition in `playbooks/glossary.md` (the four verdicts and the implicit-fifth-state prohibition). `AGENTS.md` Verdict Discipline is the sole canonical owner; the glossary entry is now a one-paragraph redirect.
- Multi-step universal-backstop guidance ("OS chmod / git pre-commit hooks / CI gates / manual `validate.py`") from `harness/codex/README.md` and `harness/cursor/README.md`. Universal backstops live once in `harness/capability-matrix.md`; per-harness READMEs now keep only harness-specific content.
- Four near-duplicate `## Adversarial Gate Check` stanzas across `playbooks/00-audit.md` / `01-design.md` / `02-spec.md` / `03-implement.md`. The single Per-phase timing-hooks table in `playbooks/principles-gates.md` is now the canonical owner.
- Redundant placeholder grep at `playbooks/02-spec.md` Quality Checks. The Phase Gate version is a strict superset (broader regex AND broader path scope including `.agent-state/decisions.md`); the Quality Checks bullet always passed-or-failed with the gate check, contributing no additional rigor. Tally adjusted from `6 [M]` to `5 [M]`; frontmatter `mechanical_items` from 10 to 9.
- Required Behaviors #8 grep formula in `playbooks/principles.md` body (relocated to `playbooks/automation.md` Lessons-Gap Backstop). The principle still names the threshold; the implementation lives with the rest of the mechanical validation.
- `validate.py` Verification Coverage Matrix anchor-diversity check. Its enforcement contract is already covered by check 7 (evidence verifiability), so the explicit check was redundant. Remaining checks renumber: lock-file validity → 14, Subsystem Ownership artifact → 15, SYNC-IMPACT format → 16, framework amendment evidence bundle → 17. Total now 17 baseline checks plus the new traceability rollup (warning-only).

### Fixed

- Stale references corrected around emergency/hotfix ownership, `CLAUDE.md` symlink ownership, and Phase 3 implementation-root checks.

### Migration Notes

- Downstream projects with a Phase 1 threat-model gate that referenced `specs/threat-model.md` directly are unaffected when the threat model lives at the default path. Projects storing the threat model elsewhere MUST ensure D-5 declares that path explicitly; the gate now reads the path from D-5 rather than assuming a hardcoded location.
- Downstream projects claiming harness controls as mitigations now SHOULD classify each claim by control-class (`Executable` / `Backstop` / `Advisory`) and activation-state (`Active now` / `Shipped but inactive` / `Not available here`) per the new `harness/capability-matrix.md`; shipped-but-inactive or advisory-only controls MUST NOT be counted as active mitigations.
- Downstream projects with a long-form templated integrity block in `phase.md` Handoff Context remain compliant — the relaxed rule accepts the prior template as one valid evidence form. Projects that wrote prose-only "verified" claims MUST upgrade those entries to cite at least one countable or tool-checkable evidence reference (timestamp, claimed phase/status, and at least one verifiable count or tool exit code).
- Downstream projects that copied `harness/codex/README.md` or `harness/cursor/README.md` for local guidance SHOULD re-copy after upgrade and re-confirm that their universal-backstop runbook references `harness/capability-matrix.md` rather than the deleted README sections.
- Required Behaviors #8 readers who relied on the inline `L − F > 5` grep formula now find it in `playbooks/automation.md` Lessons-Gap Backstop. The semantics are unchanged.
- Downstream projects with custom hooks or CI scripts that reference the old scope-reduction phrase list MUST update those references; the canonical list is now `validate.py _DEFERRAL_PHRASES` (`simplified version`, `static for now`, `defer to follow-up`, `good enough for now`, `stub for the moment`, `coming in v2`). The bare tokens `v1` and `placeholder` are no longer scanned (they matched too much legitimate technical content); the rule "no silent scope reduction" still applies in full — only the mechanical phrase scan is narrower.
- Downstream projects whose `playbooks/release-readiness.md` checklist verifies open `scope-reduction` sign-offs will now find scope-proportional formats. Solo `micro` / `small` projects MAY use the simpler date-only UTC form; `standard` / `large` continue to use the git-email anchored form.
- Downstream projects' phase playbooks that copied the per-phase `## Adversarial Gate Check` headers SHOULD remove them; the protocol owner is now solely `playbooks/principles-gates.md`. The Adversarial Review Protocol itself is unchanged — only the redundant per-phase stanzas were removed.
- The new `validate.py check_traceability` is a measurement, not a gate. Existing projects that pass `validate.py` today continue to pass. Adopters with `src/` or `tests/` directories will see a new metric line in stdout (and a stderr warning if traced-file ratio is below 80%) — no exit-code change.

## [v1.0.0] — 2026-04-19

Initial release of aegis — a governance framework for AI coding agents. This release establishes the v1.0.0 baseline: four-phase lifecycle (Audit / Design / Spec / Implement), verdict discipline, nine-type gap taxonomy, scope-proportional ceremony, Amendment Protocol with precedent requirement and SYNC-IMPACT chain-of-custody, Multi-Perspective Verification, Multi-Agent Handoff Protocol, and a mechanical validator (`validate.py`). See `AGENTS.md` for the canonical framework entry, `README.md` for onboarding, `ONBOARDING.md` for the 5-minute primer, and `playbooks/` for phase-specific rules. Subsequent releases will list specific additions, changes, and deprecations per Keep-a-Changelog convention.
