# aegis — Onboarding

A 5-minute introduction for new projects adopting aegis. The canonical rules live in `AGENTS.md` and `playbooks/`; this file is a reader's guide, not a source of truth. When any statement here disagrees with a playbook, the playbook wins.

## Vocabulary at a glance

One-page cheat sheet — everything a cold reader needs so `AGENTS.md` reads without forward references. Defer to the cross-referenced files for full definitions.

**Phase classification (see `playbooks/00-audit.md` Project Scope Classification):**
- `micro` — single-file utility or one-off script; Phases 1 & 2 skipped, goes 0 → 3
- `small` — single-purpose library or CLI; Phases 1 & 2 abbreviated
- `standard` — typical application, 2–10 subsystems; full four-phase workflow
- `large` — multi-subsystem system with ≥3 contributors; full workflow + multi-agent coordination

**Verdict vocabulary** (Phase 0 audit outputs): `keep` · `keep-with-conditions` · `redesign` · `delete`. No implicit fifth state.

**Gate outcomes** (Phase 0–3 exit): `Go` · `Conditional Go` · `Hold` · `Recycle` · `Kill`. See `playbooks/principles-gates.md` Gate Outcome Vocabulary.

**Gap type taxonomy** (9 types — `playbooks/gaps.md` canonical): `evidence` (spike needed) · `analysis` (deeper thinking) · `decision` (new decision required) · `framework` (framework rule is wrong) · `deviation` (agreed departure with expiry) · `conditional` (condition on keep-with-conditions) · `scope-reduction` (tracked deferral) · `failure-pattern` (anti-pattern detected) · `grandfathered` (pre-adoption artifact with expiry).

**Label families** (7 prefixes — `playbooks/identifiers.md`): `D-{n}` design decisions · `G-{n}` gaps · `FR-{n}` functional requirements · `NFR-{n}` non-functional · `SC-{n}` success criteria · `NG-{n}` non-goals · `L-{n}` lessons.

**D-1 … D-12 Required Decisions** (Phase 1 standard/large — `playbooks/01-design.md` is canonical): D-1 Architecture (subsystems, boundaries, dependency direction) · D-2 Authority model (who owns truth for each concept) · D-3 Public contracts (interfaces + machine-readable schema for cross-trust-boundary) · D-4 Data model (object shapes, persistence, wire format) · D-5 Security model (trust boundaries, secrets, auth, STRIDE when applicable) · D-6 Error and recovery model · D-7 Naming model (canonical terms + Naming Table) · D-8 Configuration model · D-9 Observability model (logging, metrics, tracing — OpenTelemetry (OTel) cited when applicable) · D-10 Test strategy (pyramid, per-layer floors, trust-boundary coverage) · D-11 Repository structure (scope-conditional — standard/large REQUIRED; small MAY be N/A) · D-12 Documentation structure (scope-conditional) · D-13+ project-specific (common candidates: Contract Format, Subsystem Ownership, Accessibility Model).

**Surfaces** (Phase 0 audit categories — `playbooks/00-audit.md`): Product · Architecture · Runtime · Operations · Security · Quality · Organization. Scope determines which are required (micro: Product+Security; small: Product+Architecture+Security+Quality; standard/large: all 7).

**Failure patterns** (12 named — `playbooks/failure-patterns.md`): each has a Counter Rule cross-referenced from normative playbooks. Consulted by reference when diagnosing a rationalization.

## Five key terms

- **Phase** — one of four stages: `0-audit` → `1-design` → `2-spec` → `3-implement`. Each phase has a gate with mandatory criteria; the project MUST NOT advance to the next phase until the gate passes. See `AGENTS.md` Phase Gates.
- **Surface** — one of the audit categories examined in Phase 0 (Product, Architecture, Runtime, Operations, Security, Quality, Organization, plus any project-specific additions). Earlier surfaces constrain later ones. See `playbooks/00-audit.md`.
- **Verdict** — the disposition assigned to every existing element during Phase 0 audit: `keep` / `keep-with-conditions` / `redesign` / `delete`. Every element MUST receive exactly one verdict; there is no implicit fifth state. See `playbooks/glossary.md` verdict.
- **Gap** — unresolved information or missing work tracked in `.agent-state/gaps.md`. Nine gap types are defined in `playbooks/gaps.md`; every gap has a severity, type, trigger, and resolution path.
- **Decision** — resolved architectural choice recorded in `.agent-state/decisions.md` with a `D-{n}` identifier. D-1..D-12 are reserved for the Required Decisions in `playbooks/01-design.md`; D-13+ are project-specific.

## Reading order for your first session

On the first session, read these files in this order:

1. This file (`ONBOARDING.md`) — vocabulary at a glance + primer
2. `playbooks/glossary.md` — canonical definitions (artifact, canonical, gap, spec, surface, verify, verdict, etc.); read this BEFORE AGENTS.md so forward references resolve as you encounter them
3. `AGENTS.md` — canonical entry; Session Start Protocol + Foundational Principle + Quality Primacy + Verdict Discipline + Phase Gates + Amendment Protocol
4. `playbooks/principles.md` — Tier 0 cross-phase rules (always-load core): Normative Language, Rule Priority, Quality Seeking, Autonomy Protocol, Prohibited Shortcuts, Rationalization Prevention, Required Behaviors
5. `playbooks/00-audit.md` — you always start in Phase 0. Read Quantitative anchors + Decision tree + Worked Example to calibrate.

Load on demand (when their trigger condition fires):

- `playbooks/principles-gates.md` (Tier 1) — before each phase gate, when preparing an amendment, or when scope classification changes
- `playbooks/principles-conditional.md` (Tier 2) — when measuring session-start Context Budget, working multi-agent, or resolving a rule edge case
- `playbooks/standards.md` — when evaluating, specifying, or producing code
- `playbooks/01-design.md`, `02-spec.md`, `03-implement.md` — when the phase advances
- `playbooks/identifiers.md`, `gaps.md`, `failure-patterns.md`, `zen.md`, `security-threat-model.md`, `release-readiness.md`, `automation.md` — consulted by reference

## Dependency graph

```
AGENTS.md
  │  (Session Start Protocol step 4)
  ▼
playbooks/principles.md   (Tier 0 — always-load)
  │
  ├── principles-gates.md         (Tier 1 — load at gate / amendment)
  ├── principles-conditional.md   (Tier 2 — load when triggered)
  ├── glossary.md, identifiers.md, standards.md
  ├── failure-patterns.md, gaps.md, zen.md
  │
  ▼
playbooks/00-audit.md ─► 01-design.md ─► 02-spec.md ─► 03-implement.md
                                                       │
                                                       ▼
                                                 release-readiness.md
                                                       ▲
                                                       │
                              security-threat-model.md ─┘  (consulted in Phase 0/1 when applicable)
```

## First day checklist

- [ ] Run `./tools/bootstrap.sh <target>` if not already done (see `README.md` for manual install alternative)
- [ ] Read `AGENTS.md` in full (once — re-reads happen via SYNC-IMPACT triggers)
- [ ] Read `playbooks/principles.md` in full
- [ ] Read `playbooks/00-audit.md` in full (focus on Project Scope Classification → Quantitative anchors)
- [ ] Classify project scope in `.agent-state/phase.md` (micro / small / standard / large)
- [ ] Begin the Product surface audit per `playbooks/00-audit.md` Per-Surface Entry Format

## When stuck

- Terminology ambiguous → `playbooks/glossary.md`
- A framework rule feels wrong → use the Amendment Protocol (`AGENTS.md` → Amendment Protocol). Do NOT self-authorize a deviation; propose the amendment to the user.
- Gate failing on a judgment call → `playbooks/principles-gates.md` Gate Outcome Vocabulary; report the outcome as `Hold` or `Conditional Go` with specific evidence
- Scope feels too large for one session → `AGENTS.md` Session Start Protocol step 9; propose session sequencing to the user
- Multiple concerns collide in one session → same as above; the defense against the `kitchen-sink-session` failure pattern

## What this framework is NOT

- NOT a linter or a static analyzer. The framework governs *how the project is built*, not the syntax of individual files.
- NOT a replacement for language-specific standards. See `playbooks/standards.md` for aegis's minimum bar; layer language-specific guidelines on top.
- NOT prescriptive about tooling beyond hooks and CI. You choose the build system, test runner, CI provider, and deployment model — the framework provides the governance, you provide the tools.
- NOT a one-shot setup. aegis is an ongoing discipline: every session runs Session Start Protocol, every gate verifies, every amendment goes through Amendment Protocol.

## Framework rules vs. project state

This section is canonical for the read/write split between framework and project. `README.md § Structure` is canonical for the file inventory; `README.md § Relationship to AGENTS.md and CLAUDE.md` is canonical for the symlink mechanics. Do not duplicate those — cross-reference them when needed.

aegis ships as two kinds of files:

- **Framework rules** — `AGENTS.md`, `CLAUDE.md` symlink, everything under `playbooks/`, and `harness/` adapters. Read-only from the agent's perspective. Changes flow through the Amendment Protocol.
- **Project state** — everything under `.agent-state/`. The agent reads and writes these every session. They record your project's audit findings, decisions, gaps, lessons, and session log.

When you copy aegis into your project, `.agent-state/` becomes YOUR project's working memory; `playbooks/` and `harness/` remain aegis's rules. Project-local amendments are recorded in your `.agent-state/gaps.md` with type `deviation` (temporary) or `framework` (proposed upstream) — they do NOT propagate back to aegis unless you file them upstream.
