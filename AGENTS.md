<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: AGENTS
title: aegis
version: 1.0.0
last_reviewed: 2026-04-19
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

**Version:** aegis v1.0.0 · canonical entry file per the AGENTS.md convention · RFC 2119 normative keywords in ALL CAPS · `CLAUDE.md` at the repo root is a symlink to this file for Claude Code compatibility.

aegis uses RFC 2119 normative language (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) written in ALL CAPS. See `playbooks/principles.md` Normative Language section for the full semantics.

> **Terminology.** aegis uses terms defined in [`playbooks/glossary.md`](./playbooks/glossary.md): **artifact**, **canonical**, **gap**, **spec**, **surface**, **verify**. Individual playbooks referenced from AGENTS.md declare additional glossary terms in their own Terminology blocks — consult the glossary when any rule reads ambiguously.

## Session Start Protocol

Every session MUST begin with these steps, in order:
1. Read `.agent-state/phase.md` — determine current phase, gate status, and check the Handoff Context for in-progress work from the previous session
2. Read `.agent-state/audit.md`, `decisions.md`, and `gaps.md` — know what has been audited, what has been decided (in `Accepted` or `Final` state), and what is still active (`Draft`, `Proposed`, or `Deferred`). **Archive-read scaling** (per `playbooks/00-audit.md` [Scope-Proportional Ceremony Matrix](./playbooks/00-audit.md#scope-proportional-ceremony-matrix)): for `standard` and `large` scope projects the agent MUST read archive files (`decisions-archive.md`, `gaps-archive.md`, `phase-archive.md`) at session start when they exist; for `micro` and `small` scope projects the agent MUST read the archives only when creating or revising entries that may conflict with archived truth. In all cases, the runtime rule in `playbooks/principles.md` Archive Consultation applies — agents creating or revising entries at any point in the session MUST check the archive for conflicts before writing. The agent MUST surface any contradiction between an archive entry and a proposed new entry before proceeding.
3. **Verify state integrity** — check that state files are mutually consistent, AND record the check outcome as a **concrete integrity block** in `phase.md` Handoff Context so the check is auditable (not a self-attested "verified"):
   - If `phase.md` reports Phase N as completed, the agent MUST verify that state files contain evidence supporting Phase N's gate (e.g., Phase 1 completed requires all Required Decisions to be in `Accepted` or `Final` state in `decisions.md`, with the count matching the scope classification)
   - If a state file contains only its template with no entries, the agent MUST treat the project as if that phase's work has not begun, regardless of what `phase.md` claims
   - If contradictions exist between state files, the agent MUST NOT silently proceed — the agent MUST report the inconsistency to the user with status NEEDS_CONTEXT, describe what is inconsistent, and wait for instructions on which source to trust
   - If `phase.md` is missing or unparseable, the agent MUST treat the project as Phase 0 (Audit) with no prior progress
   - The agent MUST check `gaps.md` for entries with type `deviation` — if any have outlived their expiry condition, the agent MUST flag them to the user for re-evaluation before proceeding
   - The agent MUST read the SYNC-IMPACT HTML comment at the top of `AGENTS.md` and each file under `playbooks/` (when present). If a SYNC-IMPACT comment records an amendment since the agent's last-read date of that file, AND the comment's `downstream_review_required` list includes a file the agent has not yet re-read, the agent MUST re-read that file before proceeding. See `playbooks/principles-gates.md` Sync Impact Reports for the full format and reader responsibilities
   - **Required integrity block format** — the agent MUST append a one-line block to the current session's Handoff Context of the form: `Integrity check {YYYY-MM-DD HH:MM UTC}: Phase {N} claimed {status}; decisions Accepted/Final = {count} (expected ≥ {floor}); gaps critical/open = {count}; deviations expired = {count or 0}; SYNC-IMPACT re-reads triggered = {list or "none"}.` When any claimed-vs-actual divergence is present, the block MUST additionally enumerate the divergence with file paths. Self-attested prose like "state integrity verified" is NOT an acceptable substitute — the concrete block is the only valid form.
4. Read `playbooks/principles.md` — load Tier 0 cross-phase rules (always-load core). The file itself documents the Tier 1 / Tier 2 splits below.

   **4a.** Load [`playbooks/principles-gates.md`](./playbooks/principles-gates.md) (Tier 1) BEFORE any phase gate evaluation, when preparing or reviewing a framework amendment, or when scope classification changes mid-project. Contents: Multi-Perspective Verification (+ Adversarial Review Protocol + Verification Coverage Matrix), Sync Impact Reports, Gate Outcome Vocabulary (+ Three-Tier Gate Criteria), Scope-Proportional Ceremony pointer.

   **4b.** Load [`playbooks/principles-conditional.md`](./playbooks/principles-conditional.md) (Tier 2) when a triggering condition fires: (a) the agent is measuring session-start Context Budget for a release; (b) ≥ 2 agents are active on the project (Multi-Agent Coordination); (c) the agent encounters an edge-case rule misfit requiring the Spirit = Letter discipline. Loading the whole file is cheap; loading only the relevant section is also acceptable.

5. Read the playbook for the current phase from `playbooks/`: `00-audit.md`, `01-design.md`, `02-spec.md`, or `03-implement.md`
6. Read `playbooks/standards.md` when the current phase involves evaluating, specifying, or producing code
7. Work within the current phase; if the gate is not met, work toward meeting it
8. Before ending the session, the agent MUST update all changed state files and MUST record a session log entry in `phase.md`
9. **Session scope guard** — if the user's opening prompt specifies work that includes **more than two** of: (i) a phase transition, (ii) a new subsystem, (iii) a new integration, (iv) a new gate-blocking item, (v) an architectural change, the agent MUST propose session sequencing to the user BEFORE beginning work. The proposal MUST list: (a) session 1 scope — one phase transition or one major concern, (b) session 2 scope — the next slice, (c) the interim state-file checkpoint each session produces, and (d) the rationale for the decomposition. The agent MAY proceed on the combined scope only after explicit user confirmation; in the absence of confirmation, the agent MUST work only the first session's scope. This guard is the defense against the `kitchen-sink-session` failure pattern in `failure-patterns.md` — concrete cost: a session that tries to close Phase 0 + open Phase 1 + refactor two subsystems produces shallow artifacts on all four. Single-phase, single-concern sessions pass the guard trivially and proceed without user confirmation.

## Zen Priming

Twenty aphorisms prime every session — rigor, tension pairs, and the philosophy behind the rules. The canonical list with commentary lives in [`playbooks/zen.md` § The Twenty](./playbooks/zen.md#the-twenty). They are priming, not rules; rules live in the playbooks. True tension pairs to watch: 8/9 (preserve vs. rewrite) and 16/17 (scope reduction vs. explicit deferral). Naming the tension is how drift is avoided.

## Foundational Principle

Current codebase, documentation, specifications, tests, naming, and repository structure are **diagnostic evidence, not design authority**. The agent MUST understand them thoroughly. The agent MUST NOT treat them as authoritative by default. What exists is input for analysis. What SHOULD exist is determined by design.

## Quality Primacy

Quality takes precedence over speed — Rule Priority #4. Full protocol: `playbooks/principles.md` Quality Seeking + `playbooks/principles-gates.md` Multi-Perspective Verification + Rationalization Prevention.

## Technology Currency

Projects SHOULD use the latest stable release (LTS where applicable). Projects SHOULD leverage new features that improve clarity, safety, or performance. Deprecated APIs or patterns MUST NOT be used when modern replacements exist.

## Verdict Discipline

Every existing element starts as **not accepted**. It enters the canonical system only after explicit review with exactly one verdict:

- **keep** — correct in both substance AND form; adopted as-is with zero structural changes
- **keep-with-conditions** — correct in substance, but requires specific follow-up work to be adopted as-is. Every condition MUST be recorded as a gap entry of type `conditional` in `gaps.md` with an explicit trigger for when the condition MUST be met. The next phase gate MUST fail if any `conditional` gap linked to a `keep-with-conditions` verdict is unresolved when its trigger fires. This verdict MUST NOT be used as a softer `keep` — conditions are mandatory, tracked, and auditable, and an unmet condition reverts the verdict to `redesign`
- **redesign** — addresses a valid need but in the wrong form; MUST be redesigned from first principles
- **delete** — does not belong in the final system; MUST be removed

There MUST NOT be an implicit fifth state. Existence, age, test coverage, and downstream dependents MUST NOT be used as justification for a verdict.

## Phase Gates

| Phase | Gate to Advance |
|-------|----------------|
| 0. Audit | All surfaces catalogued with verdicts in `audit.md`; strategy decided; top risks in `gaps.md` |
| 1. Design | Design closure checklist and Pre-Closure Certainty Check in `01-design.md` both pass; all critical gaps resolved |
| 2. Spec | All public contracts have reviewed specs; spec quality checks pass; all critical gaps resolved |
| 3. Implement | All code traces to decisions; project completion criteria in `03-implement.md` met |

Gate outcomes (`Go`, `Conditional Go`, `Hold`, `Recycle`, `Kill`) and the three-tier criteria classification (`[must-meet]`, `[should-meet]`, `[nice-to-have]`) are defined in `principles-gates.md` Gate Outcome Vocabulary (Tier 1 — load before each gate). Each phase playbook's gate section classifies every item by tier; the outcome determines whether the agent advances, holds, or escalates.

The agent MUST NOT write implementation code before phase 3. If uncertain, the agent MUST check `phase.md`. The scope classification in `00-audit.md` determines which phases are required: micro-scope projects advance directly from Phase 0 to Phase 3 (the agent MUST mark Phases 1–2 as `not-applicable` in `phase.md`); small-scope projects use abbreviated Phases 1–2; standard and large projects use the full framework. For projects that do not produce implementation code (specification-only repositories, governance documents), Phase 2 is the terminal phase — the agent MUST record this in `phase.md` and follow `02-spec.md` Terminal Phase completion procedure. Exploratory code (spikes, benchmarks, prototypes) MAY be produced in earlier phases only when a design decision cannot be made without empirical evidence — the agent MUST record it as a gap with `type: evidence`, MUST bound the scope to the specific question, and MUST delete the code after the evaluation. Exploratory code MUST NEVER be promoted to production; Phase 3 implementation MUST be written fresh.

### Phase Regression Procedure

Phase regression is permitted when new evidence invalidates conclusions from a prior phase. This is the **standard phase regression procedure** referenced from other playbooks (e.g., the Cascade Rule in `01-design.md`, which requires re-evaluating every downstream decision when a settled decision is revised and re-running the Whole-System Composition Check). To regress, the agent MUST:

1. Update `phase.md` to the earlier phase
2. Re-read the corresponding playbook in `playbooks/`
3. Record the regression in the session log with what changed and why
4. Re-run the earlier phase's gate criteria before re-advancing to the original phase

If regression from the same phase occurs more than twice, or if total regressions exceed three in a session, the agent **MUST escalate**: stop work, report status BLOCKED, and wait for user direction — repeated regression may indicate a scope or requirements problem.

### Phase Advancement

When a phase gate passes, the agent MUST update `phase.md`: set the new current phase, mark the previous gate as met with the date, and record the advancement in the session log.

## Emergency Protocol

Emergency hotfix workflow for production-critical issues (production down, active security breach, data loss, user-declared emergency) is in [`playbooks/03-implement.md` Hotfix Workflow](./playbooks/03-implement.md#hotfix-workflow) — the agent MUST propose the emergency to the user and obtain approval before bypassing the normal phase sequence.

## Workspace Discipline

If a `_legacy/` directory exists, it is **read-only reference**: the agent MUST NOT edit it, and MUST NOT copy code from it without explicit redesign through the verdict process. The agent MAY refer to it for behavioral clues and edge cases, but MUST NOT treat it as a template.

Framework files (`AGENTS.md`, `playbooks/`) are **read-only** for the agent. `.agent-state/` files are the working documents — the agent MUST read and update them normally. The Claude Code harness lives at `harness/claude-code/` — `harness/claude-code/settings.json` and `harness/claude-code/skills/` are the canonical locations and MAY be configured by the human maintainer during project setup. The Claude Code harness denies the agent's own writes to `harness/claude-code/settings.json` so the agent cannot grant itself new permissions — configuration changes MUST be made by the human maintainer; the agent MUST request changes through the Amendment Protocol below. `CLAUDE.md` at repo root is a symlink to `AGENTS.md` retained for Claude Code compatibility — editing either path edits the same canonical file, and the Claude Code harness settings MUST deny writes to both patterns because symlink resolution is not guaranteed. If a collaborator needs personal overrides (e.g., experiments or local preferences), they MUST use `AGENTS.local.md` (not checked in) rather than editing `AGENTS.md` — shared framework rules stay consistent for all collaborators.

By default, only one Claude Code session SHOULD operate on the project's state files at a time — concurrent sessions can produce conflicting decisions and corrupt state. When multiple agents must work simultaneously, the agents MUST strictly follow the Multi-Agent Coordination protocol in `principles-conditional.md` (Tier 2 — load when ≥ 2 agents active) — it defines partitioning, state file discipline, and conflict resolution rules that make concurrent work safe.

When applying aegis to a new project, the agent MUST verify that `.agent-state/` files are in their initial template state — if they contain data from a previous project, the agent MUST reset them before beginning Phase 0. See `00-audit.md` Strategy Decision and README Adoption for clean-room, in-place, and hybrid setup procedures.

The naming convention for files under `playbooks/` (numbered phase playbooks vs. unnumbered cross-phase playbooks) is normative. See `playbooks/identifiers.md` Playbook Naming Convention before adding a new playbook.

## Amendment Protocol

Framework files are read-only for the agent. Only the user MAY amend them. When a framework rule needs to change:

1. **Agent identifies the issue** — the agent MUST record the specific rule, why it is inadequate, and a proposed change in `gaps.md` with type `framework` and severity `critical`
2. **Agent proposes to user** — the agent MUST present the gap entry and proposed amendment; the agent MUST NOT proceed as if the amendment is already in effect
3. **Precedent requirement (no speculative rules)** — the proposed amendment MUST cite concrete precedent from one of: (a) `G-{n}` gap with observed incident; (b) `failure-patterns.md` entry observed at least once; (c) `L-{n}` lesson; (d) dated session-log incident; (e) cross-framework convergence — the proposed pattern is documented in ≥ 3 distinct mature external frameworks (one pattern occurrence per framework suffices) with the framework names and URLs cited in the CHANGELOG rationale. Without precedent: downgrade to narrative (CHANGELOG only) or reject.
4. **User decides** — the user MAY approve, modify, or reject the amendment
5. **If approved** — the user modifies the framework file; the agent MUST record the amendment in the session log with the date and rationale. The user or the agent MUST prepend the changed file with a SYNC-IMPACT HTML comment recording the version bump, summary, downstream files flagged for re-review, rationale, and date. See `playbooks/principles-gates.md` Sync Impact Reports for the format and bump-level semantics. The version bump MUST be classified per the Versioning Policy in `CHANGELOG.md` as MAJOR, MINOR, or PATCH; the agent MUST update `AGENTS.md` Version banner, every affected playbook's frontmatter `version:` field, and the `CHANGELOG.md` `[Unreleased]` section (or a new versioned section if shipping immediately) before the amendment is considered shipped. The CHANGELOG entry MUST follow Keep a Changelog format with `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security` subsections as applicable. After updating the framework file and SYNC-IMPACT comment, the author MUST run a **derived-document sweep**: grep for every file that paraphrases, abbreviates, or enumerates content from the changed playbook (skills `SKILL.md`, harness READMEs, `.mdc` files, `README.md`) and verify alignment. Every derived file with stale content MUST be updated in the same change set and listed in the SYNC-IMPACT `downstream_review_required` field.

   **Pre-ship self-compliance check.** Before the amendment is considered shipped, the author MUST apply every new or changed normative rule in the release to the release itself and MUST paste the concrete verification artifact for each into `.agent-state/phase.md` Handoff Context Verification Evidence block — if the rule requires a gap entry, file the gap; if it requires a measurement, paste the measurement; if it requires a grep artifact, paste the grep output; if it requires a specific document format, verify with grep. A **concrete verification artifact** means one of the five verifiable-reference forms defined in [`playbooks/principles-gates.md` Verification Coverage Matrix → Evidence verifiability](./playbooks/principles-gates.md#verification-coverage-matrix) (file line, file anchor, sha256 commitment, session-log anchor, or subagent-output reference); prose assertions like "verified" or "checked" are explicitly NOT acceptable artifacts. The CHANGELOG entry MUST include a **Pre-Ship Self-Compliance Evidence** subsection listing each new rule and its verification artifact (copy from or pointer to `phase.md` Evidence block). An amendment MUST NOT be marked shipped while any of its own new rules are unsatisfied without an explicit `deviation` gap recording the deferral with a user-approved expiry condition. This step is the recursive guard: the rule that fixes a self-compliance failure is itself subject to the same rule. **Termination:** the recursion is bounded because the rule set is finite — recursion terminates when every new or changed rule in the release has a concrete verification artifact (or an explicit `deviation` gap); each rule's artifact is independently checkable, so the fixed-point is reached in at most one pass per new rule.

   **Fresh-context review of the evidence block.** For MINOR and MAJOR releases, the Pre-Ship Self-Compliance Evidence block in `.agent-state/phase.md` and the CHANGELOG Pre-Ship Self-Compliance Evidence subsection MUST be reviewed by a fresh-context subagent per `playbooks/principles-gates.md` Adversarial Review Protocol before the amendment is marked shipped. The reviewer's task is specific: (a) confirm every new or changed normative rule in the release has a row in the evidence block; (b) confirm each row's artifact is concrete (a verifiable reference, not prose assertion like "verified" or "checked"); (c) enumerate any missing rows or non-verifiable artifacts. A missing row or non-verifiable artifact is a blocker — the release MUST NOT ship until the row is added or the rule is explicitly `deviation`-gapped. PATCH releases are exempt from this recursive review (author-only review suffices for single-rule clerical corrections).

6. **Temporary deviations** — if the user approves a deviation without amending the framework, the agent MUST record it in `gaps.md` with type `deviation` and an explicit expiry condition (e.g., "until Phase 2 completes" or "until D-{n} is revised")

Temporary deviations that outlive their expiry condition MUST be re-evaluated. The agent MUST flag expired deviations at session start. If more than 3 active deviations exist simultaneously, the agent MUST report degraded governance status to the user — accumulated deviations may indicate the framework needs amendment rather than continued deviation.

## Multi-Agent Handoff Protocol

When a phase is passed from one agent or team to another — including cross-session handoffs within the same project when the session is ending and another agent will resume — the originating agent MUST produce an **Exit Audit** and the receiving agent MUST produce an **Entry Acknowledgment**. Both MUST be recorded in `.agent-state/phase.md` Handoff Context section using the triplet structure (`Exit audit` / `In progress` / `Entry acknowledgment`).

**Exit Audit fields** (populated by the exiting agent before the session ends):

1. **Phase state summary** — current phase, gate status, scope classification
2. **Open items** — decisions in `Draft` / `Proposed` / `Deferred` state with IDs; open gaps with severity; pending reviews or verification passes
3. **Known risks carried forward** — blockers, incomplete threat-model cells, `scope-reduction` gaps with unexpired triggers, `[NEEDS CLARIFICATION]` markers
4. **Verification evidence pointer** — session log anchor for the most recent Verification Coverage Matrix; files modified in this session; validate.py last-run result

**Entry Acknowledgment fields** (populated by the receiving agent when the next session starts, immediately after Session Start Protocol step 2):

1. **Re-read confirmation** — list of files re-read per SYNC-IMPACT comments since last known session date; archive files consulted
2. **Discrepancies found** — any inconsistency between the exit audit and actual state-file contents, reported as session-log notes with status NEEDS_CONTEXT when material
3. **Accepted scope** — what the receiving agent commits to progressing this session; if this differs from the exit audit's Open items, the agent MUST explain why

**Subsystem Ownership requirement.** For projects meeting ALL of (a) scope ∈ {standard, large}, (b) ≥ 2 subsystems, and (c) ≥ 3 distinct agents or team members participating across the project's lifetime, the project MUST record a D-13+ Subsystem Ownership decision (per `01-design.md` Required Decisions → D-13+ candidates) mapping each subsystem to a named owner. All three conditions are required — a 2-subsystem solo project and a 10-subsystem 2-person project both fail condition (c) and are exempt. Handoffs that cross subsystem boundaries MUST notify the receiving subsystem owner via the session log and MUST coordinate per `principles-conditional.md` Multi-Agent Coordination (lock file protocol on `decisions.md`).

Projects exempt under this rule — including every single-agent project regardless of subsystem count — SHOULD record `Subsystem Ownership: N/A — {one-sentence reason naming which of (a)/(b)/(c) is absent; for single-agent projects: "single-agent project; all subsystems owned by {agent identifier}"}` as a one-line informational gap entry (severity: `info`, no typed classification — the canonical gap-type taxonomy in `playbooks/gaps.md` does not reserve a type for this purely informational N/A record) in `.agent-state/gaps.md` when the scope is `standard` or `large`. For `micro` and `small` scope projects, the exemption is implicit from the scope classification and the N/A entry is OPTIONAL — recording it adds no signal because the reason is self-evident. This downgrade (MUST → SHOULD with tier-bounded exemption) aligns with the [Scope-Proportional Ceremony Matrix](./playbooks/00-audit.md#scope-proportional-ceremony-matrix) in `playbooks/00-audit.md`: ceremony scales with scope.

Single-agent projects (per the [Scope-Proportional Ceremony Matrix](./playbooks/00-audit.md#scope-proportional-ceremony-matrix) in `playbooks/00-audit.md`) satisfy this protocol with a single-line session boundary in `phase.md` Handoff Context. A solo agent SHOULD write one line of the form `Session boundary {YYYY-MM-DD HH:MM UTC}: {one-sentence exit state}` at session end rather than the full Exit Audit + Entry Acknowledgment triplet. The full triplet is REQUIRED only when (a) the project uses more than one agent identity, (b) the outgoing session is ending in BLOCKED or NEEDS_CONTEXT state and the incoming session needs explicit carry-forward, or (c) the scope classification is `standard` or `large` with cross-subsystem work in flight. For other single-agent sessions the full triplet is NOT RECOMMENDED — the protocol cost exceeds the coordination benefit. This relaxation preserves unambiguous session boundaries where they matter (multi-agent coordination, blocked handoffs) without imposing them where they do not (solo continuation of clean work).

## Authority Discipline

One fact, one canonical owner (zen #5) — there MUST NOT be duplicate truth. Specifications own product truth; code implements specifications; tests verify specification compliance. No derived artifact (cache, index, summary, convenience layer) MAY silently become authoritative.

## Tooling Integration

When available, the project SHOULD use automation to enforce framework rules rather than relying on manual discipline alone. See `playbooks/automation.md` for the agent-neutral automation principles and `harness/claude-code/hooks-cookbook.md` for the Claude Code hook, LSP, MCP, skill, and task system implementation.
