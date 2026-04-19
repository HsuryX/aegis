# Changelog

All notable changes to aegis are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versioning follows the policy below.

## Update Guide for Downstream Projects

This guide assumes the project imported aegis from its canonical repository and keeps `AGENTS.md`, `playbooks/`, `harness/`, and `validate.py` as framework files updated from upstream. Projects that forked aegis to maintain their own customized framework treat the forked repository as canonical and apply the same guide with the fork as the upstream (substitute `/path/to/aegis/` in the commands below with the fork's repository root). Either way, `.agent-state/` remains project-owned and is NEVER overwritten by an upgrade.

When upgrading a downstream project from aegis `vX.Y.Z` to a newer version:

1. Read the CHANGELOG entry for every intermediate version between yours and the target. Each entry classifies the bump as MAJOR / MINOR / PATCH and lists Added / Changed / Deprecated / Removed / Fixed / Security / Versioning subsections.
2. For each `Changed` or `Removed` item, check whether your local playbook amendments (if any, tracked as `framework` gaps in your `.agent-state/gaps.md` with Status: resolved-with-local-change) are affected. Typical conflict points: changes to `D-1..D-12` semantics, new gate items, new frontmatter fields, renamed or removed sections.
3. Copy the updated files from aegis into your project. For most MINOR/PATCH upgrades:
   ```bash
   cp -a /path/to/aegis/playbooks/ ./playbooks/
   cp -a /path/to/aegis/AGENTS.md /path/to/aegis/CHANGELOG.md ./
   cp -a /path/to/aegis/harness/ ./harness/
   cp /path/to/aegis/validate.py ./
   # Preserve your .agent-state/ and any local overrides.
   ```
4. Run `python3 validate.py` in the target project. Expect exit 0. If a version-consistency check fails, bump the remaining playbook frontmatter to match.
5. If you had local amendments (step 2), re-evaluate each against the new aegis rules. An amendment that conflicts with an upstream rule is either (a) now subsumed by the upstream rule (delete the local amendment), (b) still needed but must be re-expressed on top of the new rule (update the gap and the local change), or (c) a signal that aegis's upstream rule should change (file a `framework` gap upstream).
6. Record the upgrade in your `.agent-state/phase.md` Session Log with the old → new version pair so future agents can trace which SYNC-IMPACT comments they've already honored.

**MAJOR upgrades** (v1 → v2, v2 → v3, etc.) are rare and carry explicit migration instructions in their CHANGELOG entry — a Migration Notes subsection at the top of the version's section. Do not attempt a MAJOR upgrade without reading the Migration Notes.

**Pinning a version.** If you want a downstream project to stay on a specific aegis version, record the pinned version in your project's `AGENTS.md` Version banner and frontmatter. Any upgrade is then explicit and consented.

## Versioning Policy

aegis uses [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) interpreted for a meta-governance framework. Each amendment MUST be classified as MAJOR, MINOR, or PATCH before shipping. The Amendment Protocol in `AGENTS.md` REQUIRES a version bump per amendment; bumps are mechanical per the rules below. The policy is binding from v1.0.0 forward.

### MAJOR (X.0.0) — breaking changes

A change is MAJOR when it invalidates prior compliance — that is, when a project that satisfied aegis v{X-1}.Y.Z would no longer satisfy v{X}.0.0 without structural updates. MAJOR changes include:

- Rule priority reordering (the Rule Priority Reference Card is changed in a way that flips conflict outcomes)
- Phase structure change (adding, removing, reordering, or merging phases; changing phase-terminal rules)
- Verdict semantic change (changing what `keep`, `redesign`, or `delete` mean; replacing a verdict with a new one that has different semantics)
- Required decision added (adding to the `D-1..D-12` reserved range)
- State file renamed, moved, or restructured such that reader compatibility breaks
- Workflow gate semantics change (what a `Go` or `Hold` outcome means; how tier classification interacts with outcome)
- Removal of any rule that was load-bearing in prior gates

Compat symlinks or transitional layers MAY be provided for one major version but DO NOT make a MAJOR change MINOR — the semver contract is about the canonical form, not the transitional convenience.

### MINOR (X.Y.0) — additive, backward-compatible

A change is MINOR when it adds capability without invalidating prior compliance. MINOR changes include:

- Additive rules, fields, sections, or playbooks
- New gap type, new failure pattern, new verdict value
- New lifecycle state that does not replace an existing one
- New gate outcome in the vocabulary
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

### Amendment workflow

Per `AGENTS.md` Amendment Protocol:
1. The agent records a `framework` gap entry.
2. The user approves, modifies, or rejects the amendment.
3. **Precedent check:** the agent MUST cite a concrete observed failure (gap entry, failure-pattern, lesson, or dated session-log incident) that the amendment prevents. Amendments without precedent MUST be narrativized or rejected.
4. On approval, the amended file is prepended with a SYNC-IMPACT HTML comment per `playbooks/principles-gates.md` Sync Impact Reports.
5. The version bump MUST be classified per this policy and recorded in the SYNC-IMPACT `version:` field and in this CHANGELOG as an entry under `[Unreleased]` (during development) or a versioned section (on ship).
6. The agent updates `AGENTS.md` Version banner and every playbook's frontmatter `version:` field to the new version before the amendment is considered shipped.

---

## [Unreleased]

(No amendments yet. See `AGENTS.md` Amendment Protocol for the process.)

## [v1.0.0] — 2026-04-19

Initial release of aegis — a governance framework for AI coding agents. This release establishes the v1.0.0 baseline: four-phase lifecycle (Audit / Design / Spec / Implement), verdict discipline, nine-type gap taxonomy, scope-proportional ceremony, Amendment Protocol with precedent requirement and SYNC-IMPACT chain-of-custody, Multi-Perspective Verification, Multi-Agent Handoff Protocol, and a mechanical validator (`validate.py`). See `AGENTS.md` for the canonical framework entry, `README.md` for onboarding, `ONBOARDING.md` for the 5-minute primer, and `playbooks/` for phase-specific rules. Subsequent releases will list specific additions, changes, and deprecations per Keep-a-Changelog convention.
