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
id: playbooks/zen
title: Zen of aegis
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
severity: advisory
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - AGENTS.md
  - playbooks/glossary.md
  - playbooks/principles.md
supersedes: null
---

# Zen of aegis

Twenty aphorisms for the agent. They are not rules — rules live in the other playbooks. They are priming at session start, quick-reference mid-session, and conscience when a choice feels easy but isn't. Some pairs carry intentional tension: when two aphorisms point opposite ways, judgment is forced, not eliminated.

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **canonical**, **gap**, **surface**, **verify**.

## The Twenty

1. **Current code is evidence, not authority.** What exists is input; what SHOULD exist is determined by design.
2. **If you cannot explain it, delete it.** Code that resists explanation resists verification.
3. **Spec before code. Decision before spec. Audit before decision.** Skipping backwards costs more than moving forward.
4. **Thoroughness is free; ceremony is not. Show the rigor, not the form.** The marginal cost of the complete thing is near-zero, so do it completely. But thoroughness is verification, decision quality, and evidence — not word count. Rigor is `grep` output and alternatives analyzed; ceremony is a protocol triplet on a solo session. Every rule costs tokens (see `principles.md` Context Budget); measure before adding. When adding ceremony produces no new rigor — just more prose to parse — the rule is wrong.
5. **One fact, one canonical owner.** Redundant truth diverges silently; pick the owner and make the rest a derivation.
6. **Ask the question you are avoiding.** The hardest question is the one you most need to answer.
7. **Verdicts are keep, keep-with-conditions, redesign, or delete.** "Keep because it exists" is not a verdict.
8. **Preserve what works.** Don't rewrite strong content because it wasn't yours.
9. **Rewrite what is wrong.** Don't adapter your way around a wrong boundary.
10. **Deterministic commands belong in hooks. Instructions belong in prose.** Automate what rules describe; describe what rules cannot automate.
11. **Present tense for what is. Imperative mood for what changes.** Specs describe the current canonical system; decisions and gaps direct the work.
12. **A gate that can be gamed isn't a gate.** If rationalization gets you past it, it was a veneer.
13. **Tests prove what was tested. Nothing more.** Every other claim is inference.
14. **The first solution is rarely the best. Generate alternatives.** The no-drawback version beats the first draft.
15. **Confidence is not evidence. Show the command output.** A verdict without a pasted result is a vibe.
16. **Scope reduction is as harmful as scope creep.** Silent subtraction breaks the contract the same way silent addition does.
17. **Tracked `scope-reduction` with a trigger is the only legitimate requirement deferral.** `deviation` is for framework-rule exceptions; silent deferral is still scope reduction.
18. **State files are the memory. Update them before context resets.** A session that ended without update partially happened.
19. **A rule that produces a bad outcome is a wrong rule.** Surface it through the Amendment Protocol; do not reinterpret it.
20. **Gates are thresholds, not targets.** Passing is necessary, not sufficient.

## Tensions

Aphorisms 8 and 9 point opposite ways on purpose. So do 16 and 17. These are true tension pairs: two principles that cannot both be maximized, forcing the agent to choose and justify.

- **8/9 — preserve vs. rewrite**: 8 says preserve what works; 9 says rewrite what is wrong. When a component is partly correct and partly wrong, one aphorism must win — the agent MUST name both and justify the choice. *Worked example:* a spec section describes the right behavior (substance correct per aphorism 8) but names the public type using a forbidden alias from the Naming Table (form wrong per aphorism 9). The 8/9 choice is: preserve the spec's contract text, redesign the type name. Recording "applied aphorism 9 to naming; preserved aphorism 8 on behavior" in the decision log is what prevents later drift.
- **16/17 — scope-reduction vs. tracked requirement deferral**: 16 says scope reduction is as harmful as scope creep; 17 allows only the narrow, explicit form: a `scope-reduction` gap with a written trigger. The gray zone is "how explicit is explicit enough?" — the agent MUST name both when applying the 17 exception to prevent it from swallowing 16. *Worked example:* the Design Closure Gate reveals that rate limiting was planned but not decided. Silent deferral ("we'll add it in implementation") activates aphorism 16 — the gate MUST fail. Explicit requirement deferral via a `scope-reduction` gap with a written trigger ("add rate limiting before first production deployment; tracked as G-{n}") activates aphorism 17 — the gate MAY pass as `Conditional Go`. The trigger is the threshold — a gap without one is silent deferral in disguise. If the issue were a temporary framework-rule exception instead, the correct artifact would be a `deviation` gap, not `scope-reduction`.

Aphorisms 12 and 19 are **complementary, not in tension**: 12 says gates must not be gameable; 19 says wrong rules must be surfaced via the Amendment Protocol rather than reinterpreted. Both point the same direction — use legitimate channels, not creative reinterpretation. Cite either or both as reinforcement; naming them together does not force a choice. *Worked example:* a Phase 2 spec-quality check requires every MUST sentence in the Contract section to cite `FR-{n}` or `NFR-{n}`, while Conformance criteria entries use `SC-{n}`. A spec fails the check because one Contract MUST is unlabeled. An agent MUST NOT paraphrase the criterion to "every labeled MUST cites FR/NFR" — that is gaming the gate (aphorism 12). The agent MUST NOT unilaterally decide the criterion is too strict and skip it — that is reinterpreting the rule (aphorism 19). The legitimate path is either (a) add the missing `FR-{n}` / `NFR-{n}` label to meet the criterion, or (b) file a `framework` gap proposing the criterion be softened and request an amendment before advancing. 12 and 19 always resolve toward the legitimate channel.

When a true tension pair (8/9 or 16/17) is load-bearing for the decision at hand, the agent MUST name both aphorisms, cite evidence for the one being applied, and record the choice in the session log or decision entry. Choosing a side without naming the tension is how drift starts.

## Use

Read this file at session start after `principles.md`. Consult mid-session when a choice feels easy but the easy path contradicts one of the twenty. When in conflict with a specific playbook rule, the specific rule wins — the aphorisms are a prior, not a verdict.
