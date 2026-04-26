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
id: playbooks/principles-gates
title: Cross-Phase Principles — Gate/Amendment-Scoped (Tier 1)
version: 1.2.0
last_reviewed: 2026-04-25
applies_to:
  - phase: all
  - trigger: phase-gate, amendment, scope-classification
severity: normative
mechanical_items: 0
judgment_items: 0
mixed_items: 0
references:
  - CHANGELOG.md
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/00-audit.md
  - playbooks/01-design.md
  - playbooks/02-spec.md
  - playbooks/03-implement.md
supersedes: null
---

# Cross-Phase Principles — Gate/Amendment-Scoped (Tier 1)

*Load when: evaluating a phase gate, preparing an amendment, or applying scope-proportional ceremony.*

This file contains the parts of aegis's cross-phase doctrine that apply at gates, amendments, and other bounded control points rather than every moment. The thin operator kernel lives in `AGENTS.md`; the always-load doctrine lives in [`principles.md`](./principles.md); Tier 2 triggered content lives in [`principles-conditional.md`](./principles-conditional.md).

This file is the canonical owner of aegis's verification, evidence, review-core, and gate-outcome model. Phase playbooks MAY define phase-local sequencing or deliverable-specific checks, but they SHOULD point back here rather than restate the evidence contract or gate semantics.

> **Terminology.** This file inherits the glossary from `principles.md` (terms: **artifact**, **canonical**, **gap**, **review**, **significant decision**, **verify**). Consult the glossary first when a rule reads ambiguously.

## Multi-Perspective Verification

At every phase gate, the agent MUST perform five-perspective verification before advancing. Each perspective MUST produce a clean result (zero findings), and the evidence MUST be recorded in the session log.

**The five perspectives:**

1. **Structural consistency** — cross-references, templates, formatting
2. **Semantic precision** — every rule unambiguous and non-contradictory
3. **Adversarial compliance** — can the rules be gamed while technically followed? For standard and large scope projects, this perspective MUST be executed via the Adversarial Review Protocol below — a fresh-context subagent delegated specifically to find `[NEEDS CLARIFICATION]` markers, vague prose, and completeness gaps. Self-checking this perspective in the main session is prone to blind spots; the fresh-context execution is the defense
4. **End-to-end simulation** — walk through a realistic scenario step by step
5. **Cold read** — read each artifact under review without consulting prior session memory or the author's framing notes; flag every undefined term used as if it were defined, every rule that names a judge identical to its subject, and every threshold expressed as adjective rather than measurable value. Distinct from Adversarial compliance (perspective 3): cold read finds gaps a first-time reader would hit; adversarial compliance finds gaps a hostile reader would exploit. For standard and large scope, cold read SHOULD be performed by a reviewer who did not author the artifact (a fresh-context subagent qualifies); for micro and small scope, the author MAY self-perform it after a deliberate context break

A gate passes only when all perspectives produce clean results. If a fix could affect a previously clean perspective, the agent MUST re-verify it before claiming closure. If a perspective finds zero issues, the agent SHOULD treat that as a signal to look harder. When multiple perspectives flag the same issue, the agent MUST escalate its severity.

**Phase emphasis** — all five perspectives apply at every gate, but invest depth where it matters most: Phase 0 (Audit) and Phase 3 (Implement) emphasize structural consistency + cold read; Phase 1 (Design) emphasizes adversarial compliance + end-to-end simulation; Phase 2 (Spec) emphasizes semantic precision + end-to-end simulation.

### Adversarial Review Protocol

At every phase gate, the agent MUST run an adversarial review subagent in a fresh context before evaluating the gate's checklist. This review is distinct from the phase-specific reviews (audit review, design review, specification review, code review) defined in each phase playbook — those reviews validate **content fidelity** and correctness; adversarial review catches **completeness gaps** in prose that reads as complete but conceals unresolved questions.

**When it runs:** before the agent checks off any gate item, at the end of every Phase N → N+1 transition, and pre-completion for spec-only projects (Phase 2 terminal).

**Scope required by project scope classification** (see `00-audit.md` Project Scope Classification):
- **micro / small**: adversarial review is RECOMMENDED (may skip for trivial internal tools; apply for anything customer-facing).
- **standard**: adversarial review is REQUIRED for Phase 1 Design gate and Phase 2 Spec gate.
- **large**: adversarial review is REQUIRED at every phase gate (Phase 0 Audit, Phase 1 Design, Phase 2 Spec, Phase 3 Implement).

**Reviewer prompt (canonical):**

> Read [files under review]. You are reviewing for completeness, not correctness — assume all claims are defensible in context. Your job: surface incomplete specifications, self-evaluated gates, vague scope, ambiguous thresholds, missing exception conditions, undefined terms, and prose that appears complete but hides unresolved questions. Apply both checks in sequence:
>
> **(1) Incompleteness** — for each reviewed section, mark every (a) `[NEEDS CLARIFICATION]` or equivalent placeholder, (b) rule with a subject or threshold that a new reader could interpret two ways, (c) rule that requires judgment calls without naming the judge.
>
> **(2) Exploitability (bad-faith read)** — for each normative rule, ask: can a motivated adversary comply with the letter while violating the spirit? Flag:
>   (a) vague subject (who does this apply to?),
>   (b) unstated scope (when does this apply? which artifacts?),
>   (c) ambiguous threshold ("significant", "substantial", "appropriate" — unquantified),
>   (d) missing exception condition (what releases the rule?),
>   (e) self-evaluated gate (is the enforcer the same entity bound by the rule?).
>
> Report: a numbered list of findings with file:line, category ((1) incompleteness or (2) exploitability sub-letter), severity, and a one-sentence clarification request. Do NOT propose fixes — only surface the gaps. Under 500 words.

**After the reviewer returns**, the agent MUST address every flagged finding before evaluating the gate. A finding addressed is a finding with a committed edit or a recorded `[J]` judgment-based decision to keep the text as-is with documented reasoning. Ignoring a finding or "deferring it to next phase" is NOT an acceptable resolution — the finding either becomes a committed change or an explicit, recorded decision.

**`[J]` disposition justification classes.** A `[J]` judgment-based decision to keep the text as-is MUST cite exactly one of these three justification classes (without a justification class, the `[J]` is not a valid disposition and the finding remains unaddressed):

1. **ALREADY_SPECIFIED** — the flagged gap is resolved elsewhere in the same release (cite `file.md:N` or `file.md#anchor` of the resolving text). Use when the reviewer surfaced an apparent hole that in fact has coverage the reviewer missed.
2. **OUT_OF_SCOPE_NG-n** — the flagged gap is a real issue but outside the current release's scope; a `G-{n}` gap MUST be filed in `.agent-state/gaps.md` using the canonical gap type that matches why the issue remains open, and its deferral MUST be tracked explicitly (for requirement deferral, that means `Type: scope-reduction` with an explicit Trigger condition naming the release that will resolve it). Use when deferral is legitimate and tracked.
3. **RISK_ACCEPTED_BY_USER** — the user has explicitly accepted the risk; the session log MUST contain a dated user confirmation line (e.g., `{YYYY-MM-DD} {HH:MM} UTC: User accepted risk on finding F-{n} per conversation at {timestamp}`). Use only when the risk has been surfaced to and acknowledged by the user.

**Severity-matched escalation.** Any CRITICAL or HIGH adversarial finding resolved by `[J]` (not a committed edit) MUST use `RISK_ACCEPTED_BY_USER` — `ALREADY_SPECIFIED` and `OUT_OF_SCOPE_NG-n` are permitted only for MEDIUM or LOW findings. This prevents blanket-dismissal of severe findings via `[J]`.

**Audit trail.** Every subagent dispatch producing findings MUST leave an archive artifact at `.agent-state/reviews/{date}-{topic}.md` per `.agent-state/reviews/README.md`. The dispositions (one row per finding, with the justification class and citation) SHOULD be recorded in that artifact's Disposition section, not only in the session log.

For standard/large scope gate reviews, a `[J]` disposition is considered independently checked only when it is both (a) recorded in the archived review artifact with citation and (b) not contradicted by the current fresh-context gate review or the current Verification Coverage Matrix. An author cannot silently self-approve a `[J]` disposition without that second check.

**Per-phase timing hooks.** Each phase playbook's Phase Gate runs this protocol before scoring its checklist; the only per-phase difference is when in the phase flow the review fires. The agent MUST honor the timing hook for the current phase:

| Phase | Timing hook |
|---|---|
| 0 (Audit) | After audit entries and Strategy section are current; resolve findings before scoring the gate. |
| 1 (Design) | After the decision set is current and before the Whole-System Composition Check closes the gate. |
| 2 (Spec) | After Specification Review is complete and before the gate is scored — spec fidelity is checked first, completeness second. |
| 3 (Implement) | After code review and re-verification are current; resolve findings before scoring Phase 3 Completion Criteria. |

Phase playbooks MUST cite this protocol from their Phase Gate intro rather than re-stating it. This is the canonical owner of the per-phase timing rule.

**Re-run order when fixes change earlier outputs.** When the agent's response to adversarial findings touches an earlier-in-phase artifact (Phase 1 example: a fix updates a decision entry the Whole-System Composition Check already scored), the agent MUST re-run the affected upstream check before re-scoring this protocol's findings. Concretely: at Phase 1, if any fix touches a decision entry, the Whole-System Composition Check MUST be re-run scoped to the changed decisions before the Adversarial Review findings are marked addressed; at Phase 2, if any fix touches a spec, Specification Review MUST be re-run scoped to the changed spec; at Phase 3, if any fix touches code, the Verification Sequence MUST be re-run scoped to the changed files. The order is: address adversarial findings → re-run the upstream check that the fix invalidated → re-score the gate. Skipping the upstream re-run is the same fix-induced-regression class that the Verification Coverage Matrix counts toward the regression-loop limit (3 per gate).

### Verification Coverage Matrix

At every phase gate, the agent MUST maintain a Verification Coverage Matrix in the session log recording which perspectives have been exercised and their results. The gate MUST NOT pass until all rows show `Exercised = yes` and `Result = clean`.

| # | Perspective | Exercised | Result | Evidence | Re-verified after fixes |
|---|------------|-----------|--------|----------|------------------------|
| 1 | Structural consistency | yes / no | clean / N findings / pending | session log ref | yes / no / N/A |
| 2 | Semantic precision | yes / no | clean / N findings / pending | session log ref | yes / no / N/A |
| 3 | Adversarial compliance | yes / no | clean / N findings / pending | subagent output ref | yes / no / N/A |
| 4 | End-to-end simulation | yes / no | clean / N findings / pending | session log ref | yes / no / N/A |
| 5 | Cold read | yes / no | clean / N findings / pending | session log ref | yes / no / N/A |

The matrix SHOULD be completed in **one well-structured verification pass** when a single agent owns all five perspectives. When perspectives are owned by different experts or agents (e.g., the Adversarial perspective is delegated to a security subagent; the End-to-end simulation is exercised by a separate integration agent), the matrix MAY be filled across multiple sessions PROVIDED: (a) each row's `Exercised`, `Result`, and `Evidence` cells MUST be populated by the owning agent, (b) the session log MUST track which agent exercised which perspective with session dates, (c) the gate outcome MUST be `Hold` (not `advance`, not `regress`) until all five rows show `Result = clean`. The expert-staged path MUST NOT be used to paper over a single agent's incomplete work — if one agent attempts to own all five perspectives but fills them across multiple sessions, the gate MUST treat this as incomplete verification (Hold) regardless of session count. Multiple rounds are the exception (regression handling below), not the norm. If a project routinely requires 3+ rounds to achieve all-clean, the audit or design quality is insufficient — the agent SHOULD investigate root cause rather than continuing to iterate.

**Evidence verifiability.** Every `Evidence` cell MUST contain a verifiable reference that RESOLVES to a real artifact. Permitted forms — each one backtick-quoted within the cell, followed optionally by prose context:

1. **File line** — `file.md:N` where the file exists AND line N is within file length.
2. **File anchor** — `file.md#anchor` where the file exists (anchor specificity is judgment).
3. **SHA-256 commitment** — `sha256:hex` (64 hex chars); opaque content commitment for captured command output.
4. **Session-log anchor** — `#session-YYYY-MM-DD-slug` where the slug appears as a Session-boundary line, heading, or literal anchor in `.agent-state/phase.md` or `.agent-state/phase-archive.md`.
5. **Subagent-output reference** — `<subagent:NAME>` where a file `.agent-state/reviews/*-NAME.md` exists, containing the reviewer prompt, full output, and metadata per `.agent-state/reviews/README.md`.
6. **Pending placeholder** — `(pending)` ONLY when the row's `Result` cell is also `pending`.

A cell containing only prose (`verified`, `checked`, `clean`, etc.) or a shape-compliant-but-unresolvable reference (e.g., `<subagent:never-dispatched>` with no archive file, or `file.md:9999` beyond file length) is NOT verifiable and the gate MUST fail with `Hold`. `validate.py` check_7 enforces both shape AND resolution — a shape-only check is gameable by fabricated anchors, so the filesystem is the arbiter, not the cell's formatting. Each claim MUST be re-checkable by a cold reader, and each subagent review MUST leave an archive trail under `.agent-state/reviews/`.

**Regression verification:** when any perspective produces findings and the agent applies fixes, the agent MUST re-exercise all 5 perspectives **scoped to the changed files** before re-evaluating the gate. If regression verification itself produces new findings (fix-induced regressions), the cycle repeats: fix → re-verify (scoped to new diff). The agent MUST count regression loops. At regression loop count 3 for the same gate, the agent MUST STOP and escalate per the Phase Regression Procedure in `AGENTS.md` — repeated fix-induced regressions indicate the fix strategy itself is flawed, not that the verification needs more passes.

**Scope limit:** each perspective SHOULD be scoped to a manageable unit — the agent SHOULD NOT attempt to verify the entire project in one perspective pass if the project exceeds 2000 lines of authored text. For large projects, decompose verification by subsystem or surface and record per-subsystem results in the matrix. Empirical evidence from code review research (Cisco Systems, Cohen et al. 2006) shows defect detection quality degrades sharply beyond 200 units of change per review session and 90 minutes of continuous review.

## Amendment Protocol

This file is the canonical owner of framework-amendment mechanics. `AGENTS.md` tells the agent **when** to load this protocol; this section defines **how** amendments, deviations, SYNC-IMPACT updates, and amendment evidence work.

When a framework rule needs to change:

1. **Agent identifies the issue** — the agent MUST record the specific rule, why it is inadequate, and a proposed change in `gaps.md` with type `framework` and severity `critical`
2. **Agent proposes to user** — the agent MUST present the gap entry and proposed amendment; the agent MUST NOT proceed as if the amendment is already in effect
3. **Precedent requirement (no speculative rules)** — the proposed amendment MUST cite concrete precedent from one of: (a) `G-{n}` gap with observed incident; (b) `failure-patterns.md` entry observed at least once; (c) `L-{n}` lesson; (d) dated session-log incident; (e) cross-framework convergence — the proposed pattern is documented in ≥ 3 distinct mature external frameworks (one pattern occurrence per framework suffices) with the framework names and URLs cited in the CHANGELOG rationale. Without precedent: downgrade to narrative (CHANGELOG only) or reject.
4. **User decides** — the user MAY approve, modify, or reject the amendment
5. **If approved** — the user or agent authoring the change MUST record the amendment evidence with the date and rationale. The version bump MUST be classified per the Versioning Policy in `CHANGELOG.md` as MAJOR, MINOR, or PATCH; the author MUST update `AGENTS.md` Version banner, every affected playbook's frontmatter `version:` field, and the `CHANGELOG.md` `[Unreleased]` section (or a new versioned section if shipping immediately) before the amendment is considered shipped. The CHANGELOG entry MUST follow Keep a Changelog format with `Added` / `Changed` / `Deprecated` / `Removed` / `Fixed` / `Security` subsections as applicable. Every changed canonical framework file (`AGENTS.md`, `playbooks/*.md`) MUST be prepended with a compact SYNC-IMPACT HTML comment per [Sync Impact Reports](#sync-impact-reports) below. After updating the framework files, the author MUST run a **diff-scoped derived-document sweep** for files that paraphrase, abbreviate, or enumerate the changed rule (skills `SKILL.md`, harness READMEs, `README.md`, similar projections) and MUST update every stale derived file in the same change set. The author MUST run `python3 validate.py` clean before the amendment is considered shipped.

   **Finite amendment evidence bundle.** Before the amendment is marked shipped, the author MUST record one bounded evidence bundle under a session anchor in `.agent-state/phase.md`. The bundle MUST cite verifiable references for: (a) the user approval or user directive that authorized the amendment, (b) the semver classification plus changed file set, (c) each changed canonical framework file's SYNC-IMPACT update, (d) the diff-scoped derived-document sweep result, and (e) the clean `python3 validate.py` run. The bundle verifies the amendment control loop once per amendment; it MUST NOT expand into per-rule recursive self-compliance accounting.

   **Clean-template framework release exception.** In the aegis framework repository itself, when a release is designated as a clean-template framework release, the finite amendment evidence bundle MAY live in `CHANGELOG.md` instead of active `.agent-state/phase.md`. The CHANGELOG entry MUST name the release authority, semver class, changed-file categories, derived-document sweep, review method and disposition, verification commands, and clean-template confirmation. The active `.agent-state/` ledgers MUST then end with no tracked diff. Teams that require durable review chain-of-custody MUST either retain a non-template review artifact outside `.agent-state/` or decline this clean-template exception for that release.

   **Fresh-context adversarial review for semantic amendments.** For amendments classified MINOR or MAJOR, the author MUST run a fresh-context adversarial review per the Adversarial Review Protocol above against the changed normative text and any directly affected derived guidance before the amendment is marked shipped. Except under the clean-template framework release exception above, the amendment evidence bundle MUST cite the resulting review artifact. Under the clean-template exception, the CHANGELOG evidence entry MUST summarize the review method, findings, and dispositions and MUST state whether a durable transcript artifact was retained. PATCH amendments MAY use author review only.
6. **Temporary deviations** — if the user approves a deviation without amending the framework, the agent MUST record it in `gaps.md` with type `deviation` and an explicit expiry condition (e.g., `until Phase 2 completes` or `until D-{n} is revised`)

Temporary deviations that outlive their expiry condition MUST be re-evaluated. The agent MUST flag expired deviations at session start. If more than 3 active deviations exist simultaneously, the agent MUST report degraded governance status to the user — accumulated deviations may indicate the framework needs amendment rather than continued deviation.

## Sync Impact Reports

When an approved framework amendment ships under the Amendment Protocol above, the amended file MUST be prepended with a compact SYNC-IMPACT HTML comment. This comment is a routing pointer, not the release narrative; detailed change explanations live in `CHANGELOG.md`.

**Format** (canonical — the comment MUST be an HTML comment and MUST include all five fields below):

```html
<!--
SYNC-IMPACT
- version: {prior}.{prior}.{prior} → {new}.{new}.{new}
- bump: MAJOR | MINOR | PATCH
- date: {YYYY-MM-DD}
- rationale: {short explanation or `CHANGELOG.md#anchor` pointer citing the release rationale}
- downstream_review_required:
  - {path/to/derived/file.md — what paraphrase or enumeration needs re-review}
  - (repeat one line per file, or leave the list empty if no derived files reference the changed content)
-->
```

SYNC-IMPACT comments MUST stay short enough to scan during session start. The whole comment SHOULD stay under 12 lines; the validator enforces this compact shape for new amendments.

**Required fields** (a SYNC-IMPACT comment is malformed if any of these is missing):

| Field | Format | Purpose |
|---|---|---|
| `version` | `X.Y.Z → A.B.C` | Prior and new canonical versions |
| `bump` | `MAJOR` \| `MINOR` \| `PATCH` | Classification per `CHANGELOG.md` Versioning Policy |
| `date` | `YYYY-MM-DD` | Amendment ship date |
| `rationale` | ≥ 30 characters, or points to a `CHANGELOG.md#anchor` release rationale | Why this change is necessary |
| `downstream_review_required` | List of relative paths; empty list allowed | Files that paraphrase or enumerate the changed content |

**Version bump classification** (one of MAJOR / MINOR / PATCH; see `CHANGELOG.md` Versioning Policy for full semantics):
- **MAJOR** — a rule becomes stricter than any prior version, OR an existing rule is broken for downstream compliance
- **MINOR** — a new rule is added, or an existing rule is relaxed, or the release touches ≥ 3 playbooks with coordinated integrity fixes / consolidations / enforcement-clarifying tightenings
- **PATCH** — clarifications, typos, cross-reference corrections, no rule semantics change

**Writer responsibilities** when creating or updating a SYNC-IMPACT comment:

1. The writer MUST populate all REQUIRED fields before marking the amendment as complete.
2. The `downstream_review_required` list MUST be generated by a diff-scoped search for forward references to the changed content. For repository-wide releases, the list MAY point only to `CHANGELOG.md` when that CHANGELOG entry names the derived files or file categories re-reviewed.
3. The `rationale` field MUST either cite the concrete precedent directly or point to a CHANGELOG release anchor that records the precedent and migration summary.

**Reader responsibilities** at session start (per `AGENTS.md` Session Start Protocol step 3):

1. The agent MUST read the top of each framework file (`AGENTS.md`, `playbooks/*.md`) for SYNC-IMPACT comments.
2. For each SYNC-IMPACT comment whose `date` is after the agent's last-read date of that file: the agent MUST treat the file as "changed since last session" and re-read it before proceeding. `Last-read date` means the most recent UTC date this project recorded that the file was re-read in `phase.md` (or `phase-archive.md`) session state, entry acknowledgment, or SYNC-IMPACT propagation note. If no such record exists for a file, the agent MUST treat the file as unread since last session and re-read it.
3. For each entry in `downstream_review_required` of such a comment: the agent MUST re-read the cited file before using its rules, even if the downstream file itself has no recent SYNC-IMPACT comment.
4. The agent MUST record in the session log which files it re-read due to SYNC-IMPACT triggers so future sessions can trace the propagation.

## Gate Outcome Vocabulary

Every phase gate produces exactly one of five outcomes (named in this vocabulary for audit consistency). The agent MUST use these exact terms in the session log.

These gate outcomes are DISTINCT from the Completion Status Protocol's reporting statuses (`DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`). A phase/release report MAY include both layers, but the gate outcome names the phase or release disposition and the completion status names the task/session report.

| Outcome | Meaning | What happens next |
|---------|---------|---|
| **Go** | All `[must-meet]` items pass; all `[should-meet]` items pass or have documented justification; `[nice-to-have]` items logged. | Advance to next phase. Update `phase.md`: set new current phase, mark the previous gate as met with the date. |
| **Conditional Go** | All `[must-meet]` items pass; one or more `[should-meet]` items fail but the failures are bounded and can be addressed during the next phase without degrading that phase's work. | Advance to next phase. Each unmet `[should-meet]` item MUST be recorded as a `conditional`-type gap entry in `gaps.md` with `Trigger condition: "before Phase {N+1} gate"`. The next phase gate MUST fail if any `conditional` gap from this advancement is unresolved. |
| **Hold** | One or more `[must-meet]` items fail; the failures are specific and bounded. | Remain in current phase. The agent MUST list exactly which `[must-meet]` items fail and what is needed to resolve each. Resume gate evaluation when the items close. |
| **Recycle** | `[must-meet]` items fail AND the failures indicate significant rework of the current phase's output — the output is structurally inadequate, not just incomplete. More severe than Hold. | Remain in current phase. The agent MUST record the recycle in the session log with what MUST be reworked and why the output is structurally inadequate. If the same gate recycles more than twice, the agent MUST escalate per the Phase Regression Procedure in `AGENTS.md`. |
| **Kill** | The project is canceled. Terminal state. | Update `phase.md` with `Status: killed` and the reason. No further phase work. The user MUST authorize a Kill — the agent MUST NOT self-authorize project termination. |

**Selecting the outcome:** the agent MUST NOT upgrade a `Hold` to a `Conditional Go` to advance faster. The distinction is load-bearing: `Conditional Go` means the unmet items are `[should-meet]` and can genuinely be addressed in the next phase; `Hold` means the unmet items are `[must-meet]` and MUST be resolved before advancement. When uncertain, `Hold` is the correct default — the Rationalization Prevention table's "The design is probably good enough to start coding" counter applies here.

### Three-Tier Gate Criteria

Every phase gate's criteria are classified into three tiers to make outcome selection deterministic:

- **`[must-meet]`** — the item MUST pass for the gate to produce `Go` or `Conditional Go`. Failure produces `Hold` or `Recycle`. Items that protect safety, correctness, verdict discipline, authority discipline, or explicit user instructions belong here.
- **`[should-meet]`** — the item SHOULD pass but the gate MAY produce `Conditional Go` when the failure is bounded and addressable in the next phase. Items that represent quality default behaviors with legitimate exceptions belong here.
- **`[nice-to-have]`** — the item SHOULD be considered and its outcome logged, but it does NOT gate advancement. Items that represent elective enhancements, polish, or style alignment belong here.

The tier classification is set when the gate is defined and MUST NOT be renegotiated at the gate — reclassifying a `[must-meet]` item to `[should-meet]` at gate time is the "goalpost move" anti-pattern (see Rationalization Prevention). If a tier is genuinely wrong, the agent MUST record a `framework` gap entry and propose the change via the Amendment Protocol above.

## Scope-Proportional Ceremony

The per-tier protocol applicability matrix lives in [`00-audit.md` Scope-Proportional Ceremony Matrix](./00-audit.md#scope-proportional-ceremony-matrix) (canonical authority alongside the Project Scope Classification). It is consulted at Phase 0 Strategy Decision and applied to every subsequent session. Tiers below `standard` are EXPLICITLY PERMITTED to skip or simplify the marked protocols.

**Gate-protocol mini-matrix** (rapid lookup — full matrix at the canonical link above):

| Scope tier | Adversarial Review at gate | Multi-Perspective Verification | Verification Coverage Matrix |
|---|---|---|---|
| `micro` | optional | self-check OK | optional |
| `small` | recommended | self-check OK | required |
| `standard` | required at Phases 1, 2 | five perspectives required | required |
| `large` | required at every phase | five perspectives required, fresh-context for cold read | required |
