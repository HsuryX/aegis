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
id: playbooks/failure-patterns
title: Failure Patterns
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
severity: reference
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/gaps.md
  - playbooks/03-implement.md
supersedes: null
---

# Failure Patterns

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **canonical**, **gap**, **review**, **verify**.

## Purpose

Named failure modes the agent can reference in gap entries, session logs, and reviews. Having a name for a failure makes it detectable; detection makes it preventable. This registry is a companion to the Rationalization Prevention table in `principles.md` — that table catches rationalizations as they form; this registry catches failures after they have already taken shape.

When the agent observes one of these patterns, the agent MUST:
1. Record a gap entry with `type: failure-pattern` citing the pattern name (see `playbooks/gaps.md`)
2. Apply the counter rule immediately
3. Note in the session log's Lessons Learned whether the pattern was caught during work or only during review — the latter indicates a gap in the detection layer

## Registry

Patterns are alphabetized. Each entry: **Symptom** · **Counter** · **Cross-reference**. For framework-amendment anti-patterns (e.g., hypothetical-rule inflation — adding rules without observed precedent), see [`principles-gates.md` Amendment Protocol](./principles-gates.md#amendment-protocol) (Precedent requirement). This registry covers project-work failures; amendment-process discipline lives with the protocol that enforces it.

### composition-drift
- **Symptom:** Each local decision is individually correct; the whole-system composition is wrong. Decision A works; decision B works; A+B produce contradictory behavior or leaky abstractions.
- **Counter:** Whole-System Composition Check. The Phase 1 gate requires the composition to hold, not just individual decisions.
- **Cross-reference:** `01-design.md` Whole-System Composition Check; `principles.md` Rationalization Prevention ("I already checked each decision individually").

### cosmetic-rename
- **Symptom:** Code is renamed, reformatted, or shuffled between files without fixing the underlying structural problem. The symptom disappears from sight; the cause remains.
- **Counter:** Verdict Discipline. Renaming is not a verdict. If the verdict is `redesign`, cosmetic renames MUST NOT substitute for structural redesign.
- **Cross-reference:** `AGENTS.md` Verdict Discipline; `glossary.md` `structural problem`.

### defensive-legacy
- **Symptom:** Code is kept "just in case" without an explicit verdict. Often paired with "we might need this" or "someone else depends on this."
- **Counter:** Verdict Discipline. Every element requires one of four verdicts (keep / keep-with-conditions / redesign / delete). "Just in case" is not a verdict; existence is not justification.
- **Cross-reference:** `AGENTS.md` Verdict Discipline.

### ghost-authority
- **Symptom:** A derived artifact (cache, index, summary, convenience layer, documentation excerpt) silently becomes authoritative. Downstream code reads from it as if it were the source of truth.
- **Counter:** Authority Discipline. One fact, one canonical owner. Derived artifacts MUST NOT become authoritative — either they regenerate from the canonical source, or the canonical source moves.
- **Cross-reference:** `AGENTS.md` Authority Discipline.

### goalpost-move
- **Symptom:** Gate criteria are redefined at the gate to match what was delivered, rather than delivery being validated against pre-defined criteria.
- **Counter:** The Three-Tier Gate Criteria classification is set when the gate is defined and MUST NOT be renegotiated at gate time. If a tier is genuinely wrong, the agent MUST record a `framework` gap and propose the change via the Amendment Protocol — the new tier then applies to future gates, not the current one.
- **Cross-reference:** `principles.md` Three-Tier Gate Criteria; `principles-gates.md` Amendment Protocol.

### infinite-exploration
- **Symptom:** Spikes or prototypes proliferate without termination. Each spike produces a partial answer; the next spike begins before the prior answer is integrated.
- **Counter:** Max-Two-Spikes protocol. The third spike requires user approval with explicit evidence from the first two and decomposition analysis. Recurrent third-spike requests signal that scope itself needs decomposition.
- **Cross-reference:** `01-design.md` Prototyping Protocol.

### kitchen-sink-session
- **Symptom:** A single session attempts too many concurrent concerns. Each individual concern gets degraded attention; quality drops uniformly.
- **Counter:** One concern per session. Wave sequencing and session-level scoping exist to constrain per-session blast radius. If mid-session the agent discovers more work than one session can hold with quality, the agent MUST stop and record the remainder as the next session's entry in the Handoff Context.
- **Cross-reference:** `AGENTS.md` Session Start Protocol; `.agent-state/phase.md` Handoff Context.

### premature-abstraction
- **Symptom:** A generalization, framework, or abstraction is introduced before a second genuine use case exists. The abstraction must later be reshaped when the second use case arrives, paying the cost twice.
- **Counter:** YAGNI. Introduce abstractions when repetition is real, not speculative. Three similar lines are better than a premature abstraction.
- **Cross-reference:** `AGENTS.md` Foundational Principle (what SHOULD exist is determined by design; speculative abstraction does not belong).

### rationalization-cascade
- **Symptom:** One rationalization (individually plausible) enables the next (individually plausible), which enables the next. The chain's endpoint is a decision that would have been obviously wrong in isolation.
- **Counter:** Rationalization Prevention table. Each rationalization in the table is paired with a concrete counter; recognizing any one in the chain breaks the cascade.
- **Cross-reference:** `principles.md` Rationalization Prevention.

### silent-deferral
- **Symptom:** Work is pushed to a later session without a tracked gap entry, trigger condition, or expiry. The agent claims something is done or out of scope when it has merely been deferred.
- **Counter:** Hard Rule 3 (No silent scope change). Requirement deferral is permitted only as an explicit `scope-reduction` gap entry with a trigger condition and, for critical scope, user confirmation. `deviation` is reserved for framework-rule exceptions, not product-requirement deferral.
- **Cross-reference:** `03-implement.md` Hard Rule 3; `playbooks/gaps.md` type taxonomy.

### trust-then-verify-gap
- **Symptom:** The agent claims verification without recording command output. Status reports say "verified" but the evidence is missing or inferred.
- **Counter:** Self-Review evidence rule. Every verification claim MUST include actual command output. Confidence is not evidence.
- **Cross-reference:** `standards.md` Self-Review Checklist; `principles.md` Rationalization Prevention ("Should work" / "Looks correct" / "I'm confident").

### wrapper-preservation
- **Symptom:** When a boundary is wrong, an adapter or wrapper is introduced to avoid redesigning the boundary. The wrong boundary persists; the adapter adds complexity without resolving the underlying misfit.
- **Counter:** Hard Rule 4 (No compatibility shims) and Verdict Discipline. If the boundary is wrong, the verdict is `redesign` — not `keep` with an adapter.
- **Cross-reference:** `03-implement.md` Hard Rule 4; `principles.md` Rationalization Prevention ("An adapter here is simpler than redesigning the boundary").

## Adding Patterns

New patterns SHOULD be added when the same unnamed failure mode appears across two or more sessions' Lessons Learned. The agent MUST draft the addition as a framework amendment per `principles-gates.md` Amendment Protocol. Pattern entries MUST follow the format above: alphabetical insertion, Symptom / Counter / Cross-reference bullets, concrete counter rule pointing to an existing playbook section rather than prose advice.

## Relationship to Rationalization Prevention

`principles.md` Rationalization Prevention catches **the thought** ("I already verified this in a previous session", "This edge case is unlikely"). This registry catches **the resulting shape** (the wrapper is committed; the spike never terminates; the deferral is undocumented). Both layers are required — the thought layer prevents cheap failures; the pattern layer prevents the expensive failures that slipped through.
