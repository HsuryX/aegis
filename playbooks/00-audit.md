<!--
SYNC-IMPACT
- version: 0.0.0 → 1.0.0
- bump: MAJOR
- date: 2026-04-19
- rationale: Initial release — establishes the v1.0.0 baseline for the aegis governance framework. All rules in AGENTS.md and playbooks/ are introduced at this version; subsequent releases follow the Amendment Protocol in AGENTS.md and the Versioning Policy in CHANGELOG.md.
- downstream_review_required: []
-->
---
id: playbooks/00-audit
title: Phase 0: Audit
version: 1.0.0
last_reviewed: 2026-04-19
applies_to:
  - phase: 0-audit
severity: normative
mechanical_items: 2
judgment_items: 9
mixed_items: 3
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/identifiers.md
  - playbooks/standards.md
  - playbooks/01-design.md
  - playbooks/security-threat-model.md
supersedes: null
---

# Phase 0: Audit

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **review**, **structural problem**, **surface**, **trust boundary**, **verify**. "Structural problem" specifically means a defect in form (boundary, authority, placement), distinct from behavioral or quality defects — see the glossary. "Trust boundary" is used in the Security surface enumeration and is defined in the glossary as the interface where data or control crosses trust domains.

## Objective

The agent MUST catalogue every major surface. For each, the agent MUST determine what exists, what is genuinely strong, what is broken or misleading, and the preliminary verdict. The agent MUST produce a strategy decision.

## Setup

The project ships with `harness/claude-code/settings.json` pre-configured with write protection (deny rules for `AGENTS.md`, `CLAUDE.md` symlink, `playbooks/`, and `_legacy/`). The agent MUST verify this file exists before auditing — it is the minimum safety net. Full hook setup (formatter, linter, type checker, build check) waits until Phase 1 when the toolchain is decided. See `harness/claude-code/hooks-cookbook.md` for the full settings template with hook examples, and `automation.md` for the agent-neutral automation principles.

## Project Scope Classification

Before auditing surfaces, classify the project scope. This determines which governance elements are required and prevents the framework from being heavier than the project warrants.

| Scope | Criteria | Governance Level |
|-------|----------|-----------------|
| **Micro** | Single file or module, < 200 lines, no public API | Apply `standards.md` directly. Skip Phases 1-2: design decisions are inline comments, specs are the code itself. Phase 0 audit covers Product + Security surfaces. Expected: 1 session; if >2 sessions, reclassify. |
| **Small** | Single subsystem, 1-3 modules, limited public surface | Abbreviated audit (Product + Architecture + Security + Quality surfaces). Abbreviated design (D-1 through D-10 required; D-11 and D-12 only if applicable). Specs cover public contracts only. Self-review suffices for both spec and code review. Expected: 2-4 sessions; if any phase >2 sessions, re-evaluate scope. |
| **Standard** | Multiple interacting subsystems, or complex security/compliance requirements | Full framework as documented — all surfaces, all 12 decisions, full spec coverage. Expected: 5-15 sessions; if any phase >5 sessions, apply Decomposition Rule. |
| **Large** | Multiple teams or subsystems with independent release cycles | Full framework plus the Decomposition Rule. Consider feature-sliced delivery (see `01-design.md`). Each sub-project follows Standard session limits. |

The agent MUST record the classification in the Strategy section of `audit.md` alongside the approach decision. If uncertain between two tiers, the agent SHOULD choose the higher tier — under-governing costs more than over-governing.

### Quantitative anchors

The qualitative criteria above resolve ambiguity via these quantitative anchors. When scope is unclear, the agent MUST count against each axis:

| Axis | Micro | Small | Standard | Large |
|------|-------|-------|----------|-------|
| Modules | ≤ 1 | 2–3 | 4–10 | 11+ |
| Lines of code | ≤ 200 | 201–2,000 | 2,001–20,000 | 20,001+ |
| Public APIs | 0 | 1–2 | 3+ | 5+ |
| Subsystems | 0 | 1 | 2–4 | 5+ |
| Team boundaries | 1 author | 1 author | 1 team | 2+ teams |
| Release cycles | 1 | 1 | 1 shared | 2+ independent |

Scope = **highest tier that any single axis reaches**. A 3-module project with 5 public APIs classifies as Standard (public-API axis dominates), not Small. A 15-module project with 1 team classifies as Large only if release cycles or team boundaries justify; otherwise Standard with Decomposition Rule applied.

### Decision tree

When in doubt, walk this tree top-down:

1. **Multiple independent release cycles OR multiple teams owning the project?** → **Large**
2. **≥ 5 subsystems or any cross-subsystem cross-cutting concern (shared auth, shared data model, cross-service rate limiting)?** → **Standard** (Large if also matching Q1)
3. **2–4 subsystems OR any public API consumed by an external caller?** → **Standard**
4. **Exactly 1 subsystem with a limited public surface (library exports, CLI subcommands, 1–2 HTTP endpoints)?** → **Small**
5. **Single file/module, no public API, no persistence, no external callers?** → **Micro**

If none match cleanly, the agent MUST fall back to the Quantitative anchors table above. When still uncertain between two tiers, the agent MUST classify upward — under-governing costs more than over-governing (compounding cost of missing audit / design / spec artifacts when a low-classified project grows into its complexity). The `audit.md` Strategy decision MUST record the classification rationale.

### Worked examples

Two intermediate-tier examples (Micro = obvious single-file script; Large = obvious multi-team distributed system; the ambiguous cases live here):

- **Small**: a Node.js CLI tool for generating release notes from git — ~800 lines across 3 files, 2 subcommands as the public surface, no network calls. Phase 0 covers 4 surfaces; Phase 1 covers D-1..D-10; Phase 2 specs the CLI subcommand contract; Phase 3 implements with per-subcommand tests.
- **Standard**: a REST API for a bookmark manager — ~5000 lines across 4 subsystems (HTTP, business logic, storage, auth), 5 public endpoints, JWT auth, Postgres. Full framework: 7 surfaces, D-1..D-12 + project-specific D-13+, spec per endpoint, e2e tests for critical flows.

The classification MAY be revised during the audit if the project turns out to be more or less complex than initially assessed. Changing classification does not require phase regression — it is part of the audit itself. If a project outgrows its scope classification during a later phase (e.g., a micro project exceeds 200 lines or gains a public API), the agent MUST reclassify upward and apply the standard phase regression procedure from `AGENTS.md` to the earliest phase whose gate criteria have **newly become applicable** under the new scope.

"Newly applicable" means gate items that the prior scope did not require but the new scope does. For example: `small` scope requires Architecture + Quality surfaces that `micro` scope does not; reclassifying `micro` → `small` makes those surfaces newly applicable. The agent MUST walk each affected phase's gate checklist and MUST identify which items are newly applicable. Only newly-applicable items REQUIRE re-verification from scratch — items that were already met under the prior scope MAY carry forward without re-verification, but the agent MUST spot-check at least two random carry-forward items to confirm they still hold under the new scope's scrutiny.

When reclassifying, the agent MUST re-audit the surfaces required by the new scope that were not required before — prior entries MAY be used as reference but MUST be revalidated against the new scope's criteria. The agent MUST record in the session log which items were newly applicable, which were carried forward, and the outcome of the spot checks.

### Scope-Proportional Ceremony Matrix

This matrix is normative: tiers below `standard` are EXPLICITLY PERMITTED to skip or simplify the marked protocols. Tiers `standard` and `large` inherit the full discipline. The matrix is consulted at Phase 0 Strategy Decision (below) and applied to every subsequent session. `principles.md` Scope-Proportional Ceremony section points here as the canonical authority.

The Verification Coverage Matrix row below is **depth-weighted, not skip-allowed** — all five perspectives per `principles-gates.md` Multi-Perspective Verification MUST be exercised at every tier; lower tiers concentrate investigation depth on the perspectives named in the tier cell, they do not skip the others. The gate criteria in every phase playbook require all five to be exercised with clean results; this row guides where to invest depth, not what to omit.

| Protocol | micro | small | standard | large |
|---|---|---|---|---|
| Phase gates | 0 → 3 only | 0, 1 (abbreviated), 2 (abbreviated), 3 | full 0 → 1 → 2 → 3 | full 0 → 1 → 2 → 3 |
| Verdict discipline (`keep` / `keep-with-conditions` / `redesign` / `delete`) | required | required | required | required |
| Session Start Protocol | required (steps 1–8) | required (1–8); step 9 scope guard optional | full (1–9) | full (1–9) |
| Multi-Agent Handoff Protocol (Exit Audit + Entry Acknowledgment triplet) | skip (solo agent) | skip (solo agent); single-line session boundary in phase.md suffices | required when > 1 agent; single-line boundary when solo | required |
| Subsystem Ownership decision (D-13+) | N/A | N/A | required when ≥ 2 subsystems AND ≥ 3 agents (per AGENTS.md AND-trigger) | required when ≥ 2 subsystems AND ≥ 3 agents |
| Subsystem Ownership N/A gap entry (for exempt projects) | optional | optional | required | required |
| Verification Coverage Matrix (5 perspectives — depth-weighted, never skipped) | all 5; depth on structural + cold read | all 5; depth on structural, semantic, cold read | all 5; full depth on every perspective | all 5; full depth on every perspective |
| Adversarial Review subagent (fresh context) | optional (self-review MAY) | optional | REQUIRED (self-review NOT RECOMMENDED) | REQUIRED |
| Security threat model (STRIDE cells) | skip unless project handles credentials, PII, or LLM inference | minimal (one table; N/A allowed per threat class) | full STRIDE + LLM-aware classes when applicable | full STRIDE + LLM-aware classes |
| Test-to-spec traceability (`Covers: SC-{n}`) | required for new tests only | required for new tests only | required (all tests; grandfathering at adoption) | required (all tests; grandfathering at adoption) |
| Amendment Protocol (for projects that amend framework rules) | required when amending | required | required | required |
| Release-readiness.md gate | optional | SHOULD run before external release | required before external release | required before external release |
| Archive-read at session start | only when creating/revising entries that may conflict | only when creating/revising entries that may conflict | full session-start read when archives exist | full session-start read when archives exist |

**How to use.** The agent MUST record the scope classification in `phase.md` and MUST apply this matrix when deciding whether a protocol applies. Protocols marked `skip` or `optional` for the project's tier MUST NOT be invoked as ceremonial gates — doing so contradicts scope-proportionality. Scope upgrades (reclassifying upward mid-project) trigger re-audit per the preceding section; scope downgrades are RARE and require user confirmation.

## Audit Mode

- **Existing project**: the agent MUST analyze current state against each surface below and MUST evaluate code quality against `playbooks/standards.md` criteria
- **Green-field project**: there is no existing artifact to evaluate, so the **Verdict** field is not applicable. The agent MUST start with the **Product** surface by eliciting goals, users, constraints, and success criteria from the user. The agent SHOULD use these forcing questions as a starting point (skipping any already answered):

  1. Who is the primary user?
  2. What specific problem does this solve for them?
  3. Why build this now — what is the trigger?
  4. What existing solutions does this replace or compete with?
  5. What is the single metric that defines success?
  6. What is explicitly out of scope — what will this NOT do?

  For remaining surfaces, the agent MUST capture what is KNOWN (constraints, hard requirements, external dependencies) and MUST flag what is UNKNOWN as Design notes. Extensive research belongs in Phase 1, not Phase 0 — the audit's job is to MAP the decision space, not to FILL it.

## Surfaces

The agent MUST audit in this order — earlier surfaces constrain later ones:

**Product** (audit first — constrains everything)
- Boundary and scope (what this system is and is not)
- Goals, and success criteria as `SC-{n}` labels per [`identifiers.md`](./identifiers.md) — each SC MUST be testable and binary (resolvable to pass/fail by a specific test or audit)
- Non-goals and explicit exclusions as `NG-{n}` labels per [`identifiers.md`](./identifiers.md) — every exclusion MUST carry an `NG-{n}` label so implementation cannot silently broaden scope

**Architecture** (audit second — constrains all technical surfaces)
- Subsystem decomposition and dependency direction
- Public contracts — any interface consumed by code outside the subsystem's boundary: APIs, CLIs, schemas, wire formats, event interfaces, exported modules, and shared libraries
- Data model (domain objects, persistence format, wire format)
- Versioning and compatibility strategy (for APIs, libraries, data formats, and wire protocols)

**Runtime**
- Behavior, state management, and workflow model
- Error handling, failure modes, and recovery semantics
- Configuration and environment model

**Operations**
- Build, CI/CD, and release pipeline
- Deployment model and environment parity
- Observability (logging, metrics, tracing, alerting)

**Security**
- Trust boundaries and threat model — when the project handles secrets, user data, or cross-trust-boundary communication, the agent MUST produce the preliminary threat model per `playbooks/security-threat-model.md` Phase 0 section as part of this surface entry. Projects qualifying for the N/A escape record it in D-5 during Phase 1 and may leave the threat-model field as "preliminary: N/A pending D-5 justification".
- Secret and credential management and rotation
- Capability, access control, and authentication model

**Quality**
- Test coverage, test quality, and whether tests encode truth or accidents
- Dependency health (versions, maintenance status, vulnerability exposure)
- Code quality against `standards.md` criteria (if code exists)
- Accessibility compliance against `standards.md` criteria (if user-facing interfaces exist)

**Organization**
- Naming and terminology consistency across code, docs, and interfaces
- Documentation accuracy, completeness, and authority mapping
- Repository structure vs. actual architecture

## Per-Surface Entry Format

Record in `.agent-state/audit.md`:

```markdown
### {Surface Name}

**Exists:** {factual description of current state}
**Strong:** {genuinely good elements worth preserving — be specific}
**Wrong:** {stale, contradictory, misleading, accidental, or missing — be specific}
**Reference:** {file paths, URLs, or sources examined}
**Verdict:** keep | keep-with-conditions | redesign | delete
**Conditions:** {required only when Verdict is `keep-with-conditions` — list each condition as a reference to a gap entry `G-{n}` of type `conditional`, one per line; omit this field for the other three verdicts}
**Design notes:** {considerations, risks, or constraints for the design phase}
```

### Worked Example

Illustrative entries for a hypothetical standard-scope project: a TypeScript REST API for bookmark management (3 subsystems — api, db, queue; ~4000 LOC; JWT auth; PostgreSQL). Do NOT copy these entries as a template — every project's entries MUST be derived from its actual surfaces. These are shown only to calibrate prose specificity and Verdict/Conditions discipline.

```markdown
### Product

**Exists:** Bookmark REST API. Four endpoints (POST/GET/PATCH/DELETE /bookmarks). JSON body, JWT bearer auth, tag-based filtering on GET. Serves a personal-use population; ~50 MAU. ~4000 LOC in TypeScript on Node 20.
**Strong:** Clear product boundary — auth system is deliberately out of scope (delegated to external identity provider per existing README). Endpoints are documented in an OpenAPI 3.1 artifact. Happy-path tests exist for each endpoint.
**Wrong:** No pagination on GET /bookmarks — collection is unbounded; an account with 10k bookmarks causes 30s+ page loads. POST /bookmarks has no idempotency key, so retries on client-side network failure create duplicates. README claims MySQL but the schema is PostgreSQL. No rate limiting documented. Non-goals are implicit rather than labeled (`NG-{n}` entries missing).
**Reference:** README.md:12-48, openapi.yaml, src/routes/bookmarks.ts, src/auth/jwt.ts, migrations/001_initial.sql
**Verdict:** keep-with-conditions
**Conditions:** G-1 (pagination on GET /bookmarks with default limit=50, max=200), G-2 (idempotency keys on POST with 24h dedup window), G-3 (README alignment to PostgreSQL + rate limit disclosure), G-4 (explicit NG-{n} entries for multi-tenancy, sharing, and public indexing)
**Design notes:** SC-1: p95 GET /bookmarks latency < 200ms under 10k-bookmark accounts. SC-2: 100% of expired-token requests return 401 with stable error shape. NG-1: no multi-tenancy in v1; NG-2: no public sharing URLs; NG-3: no search ranking beyond tag filter. Rate-limiting approach (token-bucket vs. leaky-bucket) is a D-{n} candidate.

### Architecture

**Exists:** Three subsystems — `api/` (Express.js routes + middleware), `db/` (Prisma-generated client + migrations), `queue/` (BullMQ for async tag-extraction jobs). Dependency direction api → db and api → queue; queue does not depend on db directly (it re-calls api endpoints). One public HTTP contract, one internal queue-job contract.
**Strong:** Subsystem boundaries are explicit in folder structure; no cross-subsystem imports outside the declared direction. Prisma schema is the single source of truth for the data model.
**Wrong:** The queue subsystem re-calls api endpoints to fetch bookmark content instead of accessing the db directly — this creates a circular trust boundary (queue crosses auth on every job) and doubles latency on async jobs. No versioning strategy for the HTTP contract; a breaking change to the JSON shape would silently break SDK consumers. Internal queue-job contract is not specified anywhere.
**Reference:** src/api/*, src/db/*, src/queue/*, prisma/schema.prisma, package.json dependencies
**Verdict:** redesign
**Conditions:** (omit — redesign verdict; conditions field does not apply)
**Design notes:** The queue → api callback pattern is the structural problem to fix. Design Phase 1 MUST resolve D-1 (subsystem decomposition) with queue accessing db directly, and MUST record D-3 (public contracts) with explicit versioning (semver on the /v1/ URL prefix + deprecation policy). Internal queue-job contract MUST graduate to a spec in Phase 2.

### Security

**Exists:** JWT bearer tokens from an external identity provider (Auth0). Tokens are validated on every request via the `jsonwebtoken` library with JWKS rotation. Secrets (Auth0 client secret, DB password) live in environment variables loaded from `.env` via `dotenv`; `.env.example` is checked in without real values.
**Strong:** JWT validation is correctly implemented with JWKS key rotation (not hardcoded keys). Secret scanning runs on every PR via GitHub's native secret-scanning. No secrets in git history (verified by grep of `git log -p`).
**Wrong:** No rate limiting on any endpoint — a single IP can exhaust Auth0's rate limit with credential stuffing attempts, which would affect legitimate users. No input-size limit on POST /bookmarks body; 10MB payload DoS is trivial. No CSRF protection on PATCH/DELETE (mitigated in practice by JWT-only auth but not documented). Trust boundaries are implicit; no STRIDE matrix exists.
**Reference:** src/auth/jwt.ts, src/middleware/validate.ts, .github/workflows/scan.yml, .env.example, no threat model artifact present
**Verdict:** keep-with-conditions
**Conditions:** G-5 (rate limiting on POST/PATCH/DELETE with per-IP + per-user limits; G-1 pagination item covers GET), G-6 (input-size limit of 1MB per POST body with 413 response), G-7 (document CSRF non-applicability in D-5 rationale), G-8 (STRIDE threat model per `playbooks/security-threat-model.md` applicable; trust boundaries: public HTTP ingress, DB boundary, Auth0 JWKS fetch, BullMQ→Redis boundary)
**Design notes:** D-5 (Security model) MUST cover the four trust boundaries and MUST link to a `specs/threat-model.md` artifact. The Auth0 JWKS fetch is the most fragile trust boundary (remote dependency with fallback behavior unspecified). Rate-limiting strategy is tied to D-{n} candidate in Architecture.
```

## Quality Checks

Ordered by prerequisite chain: completeness → depth → cross-cutting analysis → meta-validation. Checks marked *(existing projects)* do not apply when there is no existing artifact to critique — for green-field projects, the agent MUST substitute the equivalent check on requirements and constraints captured in Design notes. Each check is tagged `[M]` (mechanical — automatable by grep, exit code, or pattern match), `[J]` (judgment — interpretation required), or `[M+J]` (both). The agent MUST confirm each check before advancing.

**Tally:** 1 `[M+J]` · 8 `[J]` · 0 `[M]`. This section is judgment-heavy; automation cannot substitute for auditor depth.

- [ ] **[M+J]** Every surface MUST have an entry (or explicit "not applicable" with reason). Mechanical: grep `^### {surface name}` for each required surface. Judgment: "not applicable" reason is plausible.
- [ ] **[J]** *(existing projects)* Each entry MUST state what is WRONG with specific, concrete problems — vague assessments ("could be better", "needs improvement", "not ideal") MUST NOT pass
- [ ] **[J]** *(existing projects)* Contradictions between documentation and actual behavior MUST be identified
- [ ] **[J]** *(existing projects)* Naming inconsistencies across surfaces MUST be identified
- [ ] **[J]** *(existing projects)* Artifacts that appear authoritative but are not MUST be flagged
- [ ] **[J]** *(green-field)* Each entry's Design notes MUST capture specific, concrete requirements and constraints — vague aspirations ("should be fast", "user-friendly") MUST NOT pass
- [ ] **[J]** *(green-field)* Tensions or contradictions between stakeholder requirements MUST be identified and surfaced for resolution
- [ ] **[J]** The Quality Seeking protocol MUST have been applied: the agent MUST have challenged its own assessments
- [ ] **[J]** Multi-Perspective Verification MUST produce clean results from every perspective listed in `principles-gates.md` Multi-Perspective Verification

## Strategy Decision

After audit, the agent MUST choose one strategy and MUST record it in `audit.md`'s Strategy section (Approach + Rationale + Top risks). For green-field projects with no existing codebase, the strategy MUST be new-build (no legacy to reference) — the agent MUST record this and proceed to the Phase Gate (the strategy decision is predetermined, but the gate checks still apply). The strategy MUST live in `audit.md`, not `decisions.md` — it is an audit conclusion, not a design decision.

**Scope classification and ceremony budget.** The scope classification recorded earlier in this phase determines the ceremony budget for every subsequent session. The agent MUST apply the [Scope-Proportional Ceremony Matrix](#scope-proportional-ceremony-matrix) (above, this playbook) to determine which protocols apply at the project's tier: micro, small, standard, or large. Tiers below `standard` are EXPLICITLY PERMITTED to skip or simplify the marked protocols — applying standard-tier ceremony to a micro-scope project is itself a failure mode (rules accumulating without observed-failure precedent, inflating ceremony beyond the scope's real risk). When in doubt about whether a protocol applies, the matrix is the authoritative source; this Strategy Decision section does NOT re-enumerate it to avoid duplicate truth (see `principles.md` Authority Discipline).

**In-place evolution** — when:
- Architecture is broadly sound
- Naming and boundaries are recoverable with targeted effort
- Documentation is more correct than incorrect
- The codebase can serve as base with controlled improvements

**Clean-room rewrite** — when:
- Repository structure no longer reflects intended architecture
- Naming drift is pervasive, not isolated
- Documentation is more wrong or stale than right
- Major abstractions exist primarily to preserve existing form
- You cannot describe the system's intended final form by reading the existing code

**Hybrid evolution** — when:
- Some subsystems have sound architecture (qualifying for in-place evolution) while others have pervasive structural problems (qualifying for clean-room rewrite)
- Requirements: (a) the audit MUST identify which subsystems fall into which category with explicit justification per subsystem, (b) boundaries between evolved and rewritten portions MUST be cleanly defined — if the boundary is unclear, the agent MUST default to clean-room for the ambiguous region, (c) integration contracts between evolved and rewritten subsystems MUST be treated as public contracts subject to full specification
- Record the per-subsystem strategy assignment in the Strategy section of `audit.md`

## Adversarial Gate Check

Before evaluating the Phase Gate below, the agent MUST run an adversarial review subagent per `principles-gates.md` Adversarial Review Protocol. This review catches completeness gaps in audit entries that the Quality Checks above might miss — vague `Strong` or `Wrong` fields, hand-waved verdicts, `[NEEDS CLARIFICATION]` markers in product surface goals, unspecified `SC-{n}` success criteria, or `NG-{n}` Non-Goals that are still generic.

**Scope:** required for standard and large scope projects; optional for micro and small (the author MAY self-review against the adversarial reviewer prompt). **Input:** `audit.md` entries for all in-scope surfaces, the scope classification note in `phase.md`, and the Quality Checks section above. **Output:** a list of `file:line` findings. The agent MUST address every finding — by tightening the prose, opening a `gaps.md` entry, or recording a concrete justification in the session log — before the Phase Gate below evaluates.

## Phase Gate

Ordered by prerequisite: data completeness → strategic decision → risk identification. Every item MUST be satisfied before advancing. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**HALT AND REPORT.** Evaluate each item below against the Gate Outcome Vocabulary and Three-Tier Gate Criteria in `principles-gates.md`. Report the gate outcome (`Go`, `Conditional Go`, `Hold`, `Recycle`, or `Kill`) using the Completion Status Protocol — include evidence for each `[M]` item and a rendered judgment for each `[J]` item. For `Conditional Go`, record each unmet `[should-meet]` item as a `conditional` gap entry. For `Hold` or `Recycle`, list the specific `[must-meet]` items that fail.

**Tally:** 2 `[M]` · 2 `[M+J]` · 1 `[J]`. **Tiers:** 5 `[must-meet]` · 0 `[should-meet]` · 0 `[nice-to-have]`.

- [ ] **[M]** **[must-meet]** All surfaces required by the scope classification MUST have entries in `audit.md` (for micro: Product + Security; for small: Product + Architecture + Security + Quality; for standard/large: all 7) — surfaces not required by the scope MAY be marked "not-applicable" with the scope classification as justification. Mechanical: `grep -c '^### ' .agent-state/audit.md` MUST match the required surface count for the scope.
- [ ] **[J]** **[must-meet]** All quality checks above MUST pass (delegates to the 9-item Quality Checks section above, which is judgment-heavy)
- [ ] **[M]** **[must-meet]** Strategy (in-place vs. clean-room vs. hybrid vs. new-build) MUST be decided and recorded in `audit.md`. Mechanical: `grep -n '^\*\*Approach:\*\*' .agent-state/audit.md` MUST return a match with a non-placeholder value.
- [ ] **[M+J]** **[must-meet]** Top 3 highest-risk structural problems MUST be identified and recorded in `gaps.md`. Mechanical: `grep -c '^### G-' .agent-state/gaps.md` MUST be at least 3. Judgment: "highest-risk" and "structural" require interpretation — see [`glossary.md`](./glossary.md) for the structural-problem definition.
- [ ] **[M+J]** **[must-meet]** Verification Coverage Matrix complete: all 5 perspectives exercised with clean results. Mechanical: the session log contains a filled matrix with no `no` or `findings` entries. Judgment: the evidence cited for each perspective is genuine. See `principles-gates.md` Verification Coverage Matrix.
