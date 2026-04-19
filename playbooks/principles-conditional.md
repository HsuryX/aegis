<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/principles-conditional
title: Cross-Phase Principles — Triggered (Tier 2)
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: all
  - trigger: context-overflow, multi-agent-active, rule-misfit
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

*Load when: measuring the session-start Context Budget; operating with ≥ 2 agents on the same project; resolving an edge case where a rule's letter and intent seem to diverge.*

This file contains the portions of aegis's cross-phase principles that apply only when a specific condition fires. The always-load Tier 0 core lives in [`principles.md`](./principles.md); Tier 1 gate-scoped content lives in [`principles-gates.md`](./principles-gates.md).

## Context Budget

**Session-start budget** (SHOULD): `AGENTS.md` + `playbooks/principles.md` + the current-phase playbook + `playbooks/standards.md` (when code is involved) SHOULD total **≤ 12,000 tokens** combined. Measure with `cat {those files} | wc -w`, then divide by 1.3. Optional playbooks (`security-threat-model.md`, `release-readiness.md`, `failure-patterns.md`, `principles-gates.md`, `principles-conditional.md`) and state files do not count.

**Overflow handling.** When exceeded, the amendment that caused overflow MUST be re-evaluated at the next Amendment Protocol pass. The author MUST propose one of: (a) split to a load-on-demand playbook, (b) prose compression without losing rule semantics, or (c) narrativization — move explanation to CHANGELOG rationale and drop the playbook prose. **Persistent overflow** — two consecutive release measurements over cap — promotes this SHOULD to `MUST-address-in-next-release`, either via further reduction or via load-on-demand restructure; the next release MUST NOT ship while still over cap without an explicit user-approved deferral recorded in `gaps.md` as a `deviation` gap with expiry condition.

The 12,000 token target comes from cross-framework convergence (Cursor `.mdc` always-apply under ~2,000 tokens; Copilot `copilot-instructions.md` measurable degradation past ~1,000 lines; Aider `CONVENTIONS.md` community ≤ 150 lines; spec-kit token-tax warning; Anthropic Claude Code context-degradation guidance).

## Multi-Agent Coordination

When multiple agents work on the same project simultaneously:

- **Work partitioning** — agents MUST be assigned to non-overlapping subsystem boundaries as defined in the architecture decision; agents MUST NOT cross subsystem boundaries without explicit coordination
- **State file discipline** — agents MUST append to state files and MUST NOT overwrite other agents' entries; each entry MUST include the date and agent identifier to distinguish authors
- **Decision authority** — only one agent MAY propose changes to `decisions.md` at a time. Multi-agent sessions enforce this via a lock file at `.agent-state/.lock-decisions` containing four fields: `agent_id`, `acquired_at` (ISO-8601), `expected_duration_minutes`, `purpose` (one-line). Acquire (create file) before editing; release (delete) after the edit commits. Stale locks (`acquired_at + 2 × expected_duration_minutes` in the past) MAY be broken, with the break recorded in `phase.md` session log naming the prior holder + prior purpose + break reason. Single-agent sessions skip the lock; all agents MUST read state files at session start to pick up others' changes
- **File conflict resolution** — when two agents produce conflicting changes to the same file, the implementation that more closely matches the specification wins; ties MUST escalate to the user
- **Session handoff** — when one agent's work depends on another's output, the dependent agent MUST wait for the upstream agent to complete and update state files before proceeding

For single-agent sessions, this section does not apply.

## Spirit = Letter

The letter of a rule is what is written; the spirit is the intent behind it. In aegis, **the letter IS the spirit** — a rule's literal wording is the only agreed-upon truth. This is a deliberate choice because AI agents reading rules have no reliable access to unwritten intent.

**Consequence 1: no "spirit of the rule" exceptions.** The agent MUST NOT claim "this violates the letter but honors the spirit" to bypass a rule. If a rule's letter is wrong in a specific case, the case MUST be recorded in `gaps.md` with type `framework` and the Amendment Protocol invoked — the letter is amended, not bypassed.

**Consequence 2: no implicit intent.** The agent MUST NOT infer unstated intent from a rule. If a rule says "all APIs MUST use JSON", the agent MUST NOT apply it to internal function calls by inferring "the spirit is to use structured data everywhere" — that is rule expansion, not rule application. If the broader rule is desired, the broader rule MUST be written explicitly.

**Consequence 3: bad-faith reads catch ambiguity, not intent.** The Adversarial Review Protocol's bad-faith-read test asks "can a motivated adversary comply with the letter while violating the intent?" — but when a bad-faith read succeeds, the fix is to **rewrite the rule so the letter is precise**, NOT to rely on unwritten intent. Ambiguous letters are the defect; precise letters are the fix.

**Consequence 4: user instructions trump written rules.** When the user issues an explicit instruction that conflicts with a written rule, the user's instruction wins (Rule Priority #3). This is NOT "spirit overrides letter" — it is "user authority overrides framework authority". The deviation MUST be recorded per the Amendment Protocol.

**When in doubt:** read the rule literally. If the literal reading is absurd or produces harm, STOP and ask the user — do not paper over the defect with an interpretive leap.
