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
id: AGENTS
title: aegis
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
severity: normative
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - playbooks/principles.md
  - playbooks/principles-gates.md
  - playbooks/principles-conditional.md
  - playbooks/glossary.md
  - playbooks/standards.md
  - playbooks/automation.md
  - playbooks/identifiers.md
  - playbooks/zen.md
  - playbooks/gaps.md
  - playbooks/security-threat-model.md
  - playbooks/00-audit.md
  - playbooks/01-design.md
  - playbooks/02-spec.md
  - playbooks/03-implement.md
supersedes: null
---

# aegis

*A governance framework for AI coding agents.*

**Version:** aegis v1.1.0 · operational entrypoint per the AGENTS.md convention · `CLAUDE.md` at the repo root is a symlink to this file for Claude Code compatibility.

Normative language semantics, classification rubric, and the bad-faith-read test are defined in `playbooks/principles.md` Normative Language. RFC 2119 keywords appear in ALL CAPS throughout aegis.

> **Terminology.** aegis uses terms defined in [`playbooks/glossary.md`](./playbooks/glossary.md): **artifact**, **canonical**, **gap**, **spec**, **surface**, **verify**. Individual playbooks referenced from AGENTS.md declare additional glossary terms in their own Terminology blocks — consult the glossary when any rule reads ambiguously.

## Session Start Protocol

Every session MUST begin with these steps, in order:
1. Read `.agent-state/phase.md` — determine current phase, lifecycle mode, gate status, and check the Handoff Context for in-progress work from the previous session
2. Read `.agent-state/audit.md`, `decisions.md`, and `gaps.md` — know what has been audited, what has been decided (in `Accepted` or `Final` state), and what is still active (`Draft`, `Proposed`, or `Deferred`). **Archive-read scaling** (per `playbooks/00-audit.md` [Scope-Proportional Ceremony Matrix](./playbooks/00-audit.md#scope-proportional-ceremony-matrix)): for `standard` and `large` scope projects the agent MUST read archive files (`decisions-archive.md`, `gaps-archive.md`, `phase-archive.md`) at session start when they exist; for `micro` and `small` scope projects the agent MUST read the archives only when creating or revising entries that may conflict with archived truth. In all cases, the runtime rule in `playbooks/principles.md` Archive Consultation applies — agents creating or revising entries at any point in the session MUST check the archive for conflicts before writing. The agent MUST surface any contradiction between an archive entry and a proposed new entry before proceeding.
3. **Verify state integrity** — check that project-state ledgers are mutually consistent, AND record the check outcome as a **concrete integrity block** in `phase.md` Handoff Context so the check is auditable (not a self-attested "verified"):
   - If `phase.md` reports Phase N as completed, the agent MUST verify that project-state ledgers contain evidence supporting Phase N's gate (e.g., Phase 1 completed requires all Required Decisions to be in `Accepted` or `Final` state in `decisions.md`, with the count matching the scope classification)
   - If a state ledger contains only its template with no entries, the agent MUST treat the project as if that phase's work has not begun, regardless of what `phase.md` claims
   - If contradictions exist between project-state ledgers, the agent MUST NOT silently proceed — the agent MUST report the inconsistency to the user with status NEEDS_CONTEXT, describe what is inconsistent, and wait for instructions on which source to trust
   - If `phase.md` is missing or unparseable, the agent MUST treat the project as Phase 0 (Audit) with no prior progress
   - The agent MUST check `gaps.md` for entries with type `deviation` — if any have outlived their expiry condition, the agent MUST flag them to the user for re-evaluation before proceeding
   - The agent MUST read the SYNC-IMPACT HTML comment at the top of `AGENTS.md` and each file under `playbooks/` (when present). If a SYNC-IMPACT comment records an amendment since the agent's last-read date of that file, the agent MUST re-read that amended framework file itself before using its rules; if the comment's `downstream_review_required` list includes a file the agent has not yet re-read, the agent MUST also re-read that downstream file before proceeding. See `playbooks/principles-gates.md` Sync Impact Reports for the full format and reader responsibilities
   - **Required integrity block** — the agent MUST append a one-line block to the current session's Handoff Context recording (a) timestamp, (b) claimed phase + status, (c) at least one verifiable count or evidence reference (e.g., decisions Accepted/Final, critical-open gaps, expired deviations, SYNC-IMPACT re-reads triggered, or `python3 validate.py` exit code). When any claimed-vs-actual divergence is present, the block MUST enumerate the divergence with file paths. Self-attested prose like "state integrity verified" is NOT acceptable — the block MUST cite countable or tool-checkable evidence. Reference template: `Integrity check {YYYY-MM-DD HH:MM UTC}: Phase {N} {status}; D-Accepted/Final={count} (≥{floor}); G-critical/open={count}; deviations-expired={count}; SYNC-IMPACT re-reads={list or "none"}; validate.py={pass|fail}.`
4. Read `playbooks/principles.md` — load the always-on cross-phase doctrine
5. Load supplements only when their trigger fires:
   - `playbooks/principles-gates.md` BEFORE any phase gate evaluation, when preparing or reviewing a framework amendment, or when scope classification changes mid-project
   - `playbooks/principles-conditional.md` when measuring session-start Context Budget for a release, coordinating ≥ 2 agents, preparing or receiving a formal handoff, or resolving a Spirit = Letter edge case
6. Read the playbook for the current phase from `playbooks/`: `00-audit.md`, `01-design.md`, `02-spec.md`, or `03-implement.md`
7. Read `playbooks/standards.md` when the current phase involves evaluating, specifying, or producing code
8. **Session scope guard** — if the user's opening prompt specifies work that includes **more than two** of: (i) a phase transition, (ii) a new subsystem, (iii) a new integration, (iv) a new gate-blocking item, (v) an architectural change, the agent MUST propose session sequencing to the user BEFORE beginning work. The proposal MUST list: (a) session 1 scope — one phase transition or one major concern, (b) session 2 scope — the next slice, (c) the interim state-file checkpoint each session produces, and (d) the rationale for the decomposition. The agent MAY proceed on the combined scope only after explicit user confirmation; in the absence of confirmation, the agent MUST work only the first session's scope. This guard is the defense against the `kitchen-sink-session` failure pattern in `failure-patterns.md` — concrete cost: a session that tries to close Phase 0 + open Phase 1 + refactor two subsystems produces shallow artifacts on all four. Single-phase, single-concern sessions pass the guard trivially and proceed without user confirmation.
9. Work within the current phase; if the gate is not met, work toward meeting it
10. Before ending the session, the agent MUST update all changed project-state ledgers and MUST record a session log entry in `phase.md`

## Load Map

- **Always on** — `AGENTS.md` and `playbooks/principles.md`
- **Gate / amendment / scope-change rigor** — `playbooks/principles-gates.md`
- **Triggered coordination and edge-case rules** — `playbooks/principles-conditional.md`
- **Current phase** — exactly one of `playbooks/00-audit.md`, `01-design.md`, `02-spec.md`, `03-implement.md`, chosen from `phase.md`
- **Code/spec quality bar** — `playbooks/standards.md` when code, tests, or technical specs are in scope
- **Everything else** — consulted by reference from the active playbooks, not loaded by default

## Foundational Principle

Current codebase, documentation, specifications, tests, naming, and repository structure are **diagnostic evidence, not design authority**. The agent MUST understand them thoroughly. The agent MUST NOT treat them as authoritative by default. What exists is input for analysis. What SHOULD exist is determined by design.

## Verdict Discipline

Every existing element starts as **not accepted**. It enters the canonical system only after explicit review with exactly one verdict:

- **keep** — correct in both substance AND form; adopted as-is with zero structural changes
- **keep-with-conditions** — correct in substance, but requires specific follow-up work to be adopted as-is. Every condition MUST be recorded as a gap entry of type `conditional` in `gaps.md` with an explicit trigger for when the condition MUST be met. The next phase gate MUST fail if any `conditional` gap linked to a `keep-with-conditions` verdict is unresolved when its trigger fires. This verdict MUST NOT be used as a softer `keep` — conditions are mandatory, tracked, and auditable, and an unmet condition reverts the verdict to `redesign`
- **redesign** — addresses a valid need but in the wrong form; MUST be redesigned from first principles
- **delete** — does not belong in the canonical system; MUST be removed

There MUST NOT be an implicit fifth state. Existence, age, test coverage, and downstream dependents MUST NOT be used as justification for a verdict.

## Authority Discipline

One fact, one canonical owner (zen #5) — there MUST NOT be duplicate truth. The Product surface in `audit.md` owns product boundary, product goals, global non-goals, and product success criteria; specifications own contract truth and conformance truth; code implements specifications; tests verify specification conformance; project validation checks delivered behavior against the Product surface. No derived artifact (cache, index, summary, convenience layer) MAY silently become authoritative.

## Phase Gates

| Phase | Gate to Advance |
|-------|----------------|
| 0. Audit | All surfaces catalogued with verdicts in `audit.md`; strategy + lifecycle mode decided; top risks in `gaps.md` |
| 1. Design | Design closure checklist + Pre-Closure Certainty Check in `01-design.md` both pass; Authority model has no duplicate or missing owners; whole-system composition check passes; threat model complete or N/A recorded; all critical gaps resolved |
| 2. Spec | All public contracts have reviewed specs; every spec declares a Proof class; spec quality checks pass; all critical gaps resolved |
| 3. Implement | All code traces to decisions and specs (`Implements:` / `Covers:`); Phase 3 completion criteria in `03-implement.md` met; Product surface goals validated |

Detailed gate outcomes, multi-perspective verification, amendment mechanics, SYNC-IMPACT handling, and release-facing gate procedure live in `playbooks/principles-gates.md`.

## Lifecycle Mode

Lifecycle mode is an axis orthogonal to the 0 → 1 → 2 → 3 phase system. Phase 0 strategy MUST choose exactly one lifecycle mode and record it in both `.agent-state/audit.md` and `.agent-state/phase.md`:

- **finite-delivery** — work targets a bounded delivery endpoint. Terminal-phase completion means the project or slice is complete until new scope is explicitly opened.
- **steady-state** — the repo is expected to continue through recurring change/governance cycles. Terminal-phase completion means the current cycle is complete, not that the product is forever final. After terminal-phase housekeeping, the next material work item MUST restart at Phase 0; that next Phase 0 MAY classify the work as a bounded-change cycle per the rule below. This mode MUST NOT bypass decisions, specifications, reviews, rollback/hotfix discipline, amendment rules, or release discipline; it changes terminal semantics only. Release Readiness runs only for cycles that actually ship.

## Implementation Boundary

The agent MUST NOT write implementation code before Phase 3. If uncertain, the agent MUST check `phase.md`. Scope classification in `00-audit.md` determines which phases are required: **micro** advances directly from Phase 0 to Phase 3 (the agent MUST mark Phases 1–2 as `not-applicable` in `phase.md`); **small** uses abbreviated Phases 1–2; **standard** and **large** use the full framework. Spec-only repositories (no implementation code) treat Phase 2 as terminal — see `02-spec.md` Terminal Phase. In `finite-delivery` mode, terminal completion means the project or slice is complete; in `steady-state` mode, the current cycle is complete and the next material work item returns to Phase 0 for reclassification.

**Bounded-change cycle.** Existing non-micro projects MAY skip Phases 1–2 for a cycle when existing Accepted/Final decisions and reviewed specs already fully cover the requested work and no new design concept is introduced. The full eligibility criteria and the required `phase.md` record format are defined in `playbooks/00-audit.md` Bounded-Change Rule. The agent MUST record the cycle there before proceeding; otherwise the normal full cycle applies.

**Exploratory code.** Spikes, benchmarks, and prototypes MAY be produced in earlier phases only when a design decision cannot be made without empirical evidence. The agent MUST record an `evidence`-type gap, bound the scope to the specific question, and delete the code after evaluation. Exploratory code MUST NEVER be promoted to production; Phase 3 implementation MUST be written fresh.

## Phase Regression

When new evidence invalidates prior phase work, the agent MUST: (1) update `phase.md` to the earlier phase, (2) re-read the corresponding playbook, (3) record the regression in the session log with what changed and why, and (4) re-run the earlier phase's gate before re-advancing. If regression from the same phase occurs more than twice, or if total regressions exceed three in a session, the agent MUST stop, report status BLOCKED, and wait for user direction. See `playbooks/glossary.md` *phase regression* for the term definition.

## Workspace Discipline

If a `_legacy/` directory exists, it is **read-only reference**: the agent MUST NOT edit it, and MUST NOT copy code from it without explicit redesign through the verdict process. The agent MAY refer to it for behavioral clues and edge cases, but MUST NOT treat it as a template.

Framework files (`AGENTS.md`, `playbooks/`) are **read-only** for the agent. `.agent-state/` files are the project-state ledgers — the agent MUST read and update them normally. The Claude Code harness lives at `harness/claude-code/`. The discipline:

- **Canonical sources.** `harness/claude-code/settings.json` and `harness/claude-code/skills/` are the canonical shipped source locations. They MAY be configured by the human maintainer during project setup. Configuration changes themselves MUST be made by the human maintainer, not the agent.
- **Activation.** `harness/claude-code/settings.json` is not active from file presence alone — it becomes active only when the maintainer installs or syncs it into Claude Code's real loaded settings path.
- **Write denial.** When that loaded settings file is in use, it MUST deny the agent's direct Edit/Write/NotebookEdit writes to the canonical settings source.
- **Bash subprocess gap.** Settings-level write denial does not block Bash subprocess writes; shell-resistant protection still requires OS-level or hook backstops.
- **Symlink coverage.** `CLAUDE.md` at the repo root is a symlink to `AGENTS.md` retained for Claude Code compatibility. Editing either path edits the same canonical file. The loaded Claude Code settings MUST deny writes to both patterns because symlink resolution is not guaranteed.
- **Local overrides.** If a collaborator needs personal overrides (experiments or local preferences), they MUST use `AGENTS.local.md` (not checked in) rather than editing `AGENTS.md` — shared framework rules stay consistent for all collaborators.

By default, only one active agent session SHOULD write project state at a time — concurrent sessions can produce conflicting decisions and corrupt state. When multiple agents are active, or when a formal handoff is needed, the agent MUST load `playbooks/principles-conditional.md` and follow its coordination and handoff rules.

When applying aegis to a new project, the agent MUST verify that `.agent-state/` ledgers are in their initial template state — if they contain data from a previous project, the agent MUST reset them before beginning Phase 0. See `00-audit.md` Strategy Decision and README Adoption for clean-room, in-place, and hybrid setup procedures.

The naming convention for files under `playbooks/` (numbered phase playbooks vs. unnumbered cross-phase playbooks) is normative. See `playbooks/identifiers.md` Playbook Naming Convention before adding a new playbook.
