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
id: playbooks/principles-conditional
title: Cross-Phase Principles — Conditional Supplements (Tier 2)
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
  - trigger: context-overflow, multi-agent-active, handoff, rule-misfit
severity: normative
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/principles-gates.md
supersedes: null
---

# Cross-Phase Principles — Triggered (Tier 2)

*Load when: measuring the session-start Context Budget; operating with ≥ 2 agents on the same project; preparing or receiving a formal handoff; resolving an edge case where a rule's letter and intent seem to diverge.*

This file contains the portions of aegis's cross-phase doctrine that apply only when a specific condition fires. The thin operator kernel lives in `AGENTS.md`; the always-load Tier 0 doctrine lives in [`principles.md`](./principles.md); Tier 1 gate/amendment-scoped content lives in [`principles-gates.md`](./principles-gates.md).

## Context Budget

**Session-start budget** (SHOULD): `AGENTS.md` + `playbooks/principles.md` + the current-phase playbook + `playbooks/standards.md` (when code is involved) SHOULD total **≤ 12,000 tokens** combined. Measure with `cat {those files} | wc -w`, then divide by 1.3. Optional playbooks (`security-threat-model.md`, `release-readiness.md`, `failure-patterns.md`, `principles-gates.md`, `principles-conditional.md`) and state files do not count.

**Overflow handling.** When exceeded, the amendment that caused overflow MUST be re-evaluated at the next Amendment Protocol pass in `principles-gates.md`. The author MUST propose one of: (a) split to a load-on-demand playbook, (b) prose compression without losing rule semantics, or (c) narrativization — move explanation to CHANGELOG rationale and drop the playbook prose. **Persistent overflow** — two consecutive release measurements over cap — promotes this SHOULD to `MUST-address-in-next-release`, either via further reduction or via load-on-demand restructure; the next release MUST NOT ship while still over cap without an explicit user-approved deferral recorded in `gaps.md` as a `deviation` gap with expiry condition.

The 12,000 token target comes from cross-framework convergence (Cursor `.mdc` always-apply under ~2,000 tokens; Copilot `copilot-instructions.md` measurable degradation past ~1,000 lines; Aider `CONVENTIONS.md` community ≤ 150 lines; spec-kit token-tax warning; Anthropic Claude Code context-degradation guidance).

## Multi-Agent Coordination

When multiple agents work on the same project simultaneously:

- **Work partitioning** — agents MUST be assigned to non-overlapping subsystem boundaries as defined in the architecture decision; agents MUST NOT cross subsystem boundaries without explicit coordination
- **State file discipline** — agents MUST append to state files and MUST NOT overwrite other agents' entries; each entry MUST include the date and agent identifier to distinguish authors
- **Decision authority** — only one agent MAY propose changes to `decisions.md` at a time. Multi-agent sessions enforce this via a lock file at `.agent-state/.lock-decisions` containing four fields: `agent_id`, `acquired_at` (ISO-8601), `expected_duration_minutes`, `purpose` (one-line). Acquire (create file) before editing; release (delete) after the edit commits. Stale locks (`acquired_at + 2 × expected_duration_minutes` in the past) MAY be broken, with the break recorded in `phase.md` session log naming the prior holder + prior purpose + break reason. Single-agent sessions skip the lock; all agents MUST read state files at session start to pick up others' changes
- **File conflict resolution** — when two agents produce conflicting changes to the same file, the implementation that more closely matches the specification wins; ties MUST escalate to the user
- **Session handoff** — when one agent's work depends on another's output, the dependent agent MUST wait for the upstream agent to complete and update state files before proceeding

For single-agent sessions, this section does not apply.

## Multi-Agent Handoff Protocol

When a phase is passed from one agent or team to another — including cross-session handoffs within the same project when the session is ending and another agent will resume — the originating agent MUST produce an **Exit Audit** and the receiving agent MUST produce an **Entry Acknowledgment**. Both MUST be recorded in `.agent-state/phase.md` Handoff Context section using the triplet structure (`Exit audit` / `In progress` / `Entry acknowledgment`).

**Exit Audit fields** (populated by the exiting agent before the session ends):

1. **Phase state summary** — current phase, gate status, scope classification
2. **Open items** — decisions in `Draft` / `Proposed` / `Deferred` state with IDs; open gaps with severity; pending reviews or verification passes
3. **Known risks carried forward** — blockers, incomplete threat-model cells, `scope-reduction` gaps with unexpired triggers, `[NEEDS CLARIFICATION]` markers
4. **Verification evidence pointer** — session log anchor for the most recent Verification Coverage Matrix; files modified in this session; `python3 validate.py` last-run result

**Entry Acknowledgment fields** (populated by the receiving agent when the next session starts, immediately after Session Start Protocol step 2):

1. **Re-read confirmation** — list of files re-read per SYNC-IMPACT comments since last known session date; archive files consulted
2. **Discrepancies found** — any inconsistency between the exit audit and actual state-file contents, reported as session-log notes with status NEEDS_CONTEXT when material
3. **Accepted scope** — what the receiving agent commits to progressing this session; if this differs from the exit audit's Open items, the agent MUST explain why

**Subsystem Ownership requirement.** For projects meeting ALL of (a) scope ∈ {`standard`, `large`}, (b) ≥ 2 subsystems, and (c) ≥ 3 distinct agents or team members participating across the project's lifetime, the project MUST record a D-13+ Subsystem Ownership decision (per `01-design.md` Required Decisions → D-13+ candidates) mapping each subsystem to a named owner. All three conditions are required — a 2-subsystem solo project and a 10-subsystem 2-person project both fail condition (c) and are exempt. Handoffs that cross subsystem boundaries MUST notify the receiving subsystem owner via the session log and MUST coordinate per Multi-Agent Coordination above (lock file protocol on `decisions.md`).

Projects exempt under this rule — including every single-agent project regardless of subsystem count — SHOULD record `Subsystem Ownership: N/A — {one-sentence reason naming which of (a)/(b)/(c) is absent; for single-agent projects: "single-agent project; all subsystems owned by {agent identifier}"}` as a one-line note in `.agent-state/phase.md` Handoff Context when the scope is `standard` or `large`. This is a local structural N/A note, not a gap entry. For `micro` and `small` scope projects, the exemption is implicit from the scope classification and the N/A note is OPTIONAL — recording it adds no signal because the reason is self-evident. This downgrade (MUST → SHOULD with tier-bounded exemption) aligns with the [Scope-Proportional Ceremony Matrix](./00-audit.md#scope-proportional-ceremony-matrix) in `00-audit.md`: ceremony scales with scope.

Single-agent projects satisfy this protocol with a single-line session boundary in `phase.md` Handoff Context. A solo agent SHOULD write one line of the form `Session boundary {YYYY-MM-DD HH:MM UTC}: {one-sentence exit state}` at session end rather than the full Exit Audit + Entry Acknowledgment triplet. The full triplet is REQUIRED only when (a) the project uses more than one agent identity, (b) the outgoing session is ending in BLOCKED or NEEDS_CONTEXT state and the incoming session needs explicit carry-forward, or (c) the scope classification is `standard` or `large` with cross-subsystem work in flight. For other single-agent sessions the full triplet is NOT RECOMMENDED — the protocol cost exceeds the coordination benefit. This relaxation preserves unambiguous session boundaries where they matter (multi-agent coordination, blocked handoffs) without imposing them where they do not (solo continuation of clean work).

## Spirit = Letter

The letter of a rule is what is written; the spirit is the intent behind it. In aegis, **the letter IS the spirit** — a rule's literal wording is the only agreed-upon truth. This is a deliberate choice because AI agents reading rules have no reliable access to unwritten intent.

**Consequence 1: no "spirit of the rule" exceptions.** The agent MUST NOT claim "this violates the letter but honors the spirit" to bypass a rule. If a rule's letter is wrong in a specific case, the case MUST be recorded in `gaps.md` with type `framework` and the Amendment Protocol in `principles-gates.md` invoked — the letter is amended, not bypassed.

**Consequence 2: no implicit intent.** The agent MUST NOT infer unstated intent from a rule. If a rule says "all APIs MUST use JSON", the agent MUST NOT apply it to internal function calls by inferring "the spirit is to use structured data everywhere" — that is rule expansion, not rule application. If the broader rule is desired, the broader rule MUST be written explicitly.

**Consequence 3: bad-faith reads catch ambiguity, not intent.** The Adversarial Review Protocol's bad-faith-read test asks "can a motivated adversary comply with the letter while violating the intent?" — but when a bad-faith read succeeds, the fix is to **rewrite the rule so the letter is precise**, NOT to rely on unwritten intent. Ambiguous letters are the defect; precise letters are the fix.

**Consequence 4: user instructions trump written rules.** When the user issues an explicit instruction that conflicts with a written rule, the user's instruction wins (Rule Priority #3). This is NOT "spirit overrides letter" — it is "user authority overrides framework authority". The deviation MUST be recorded per the Amendment Protocol in `principles-gates.md`.

**When in doubt:** read the rule literally. If the literal reading is absurd or produces harm, STOP and ask the user — do not paper over the defect with an interpretive leap.
