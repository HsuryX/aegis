# aegis — Onboarding

A 5-minute introduction for new projects adopting aegis. `AGENTS.md` is the canonical operational entrypoint, and `playbooks/` own the detailed rules; this file is a reader's guide, not a source of truth. When any statement here disagrees with `AGENTS.md` or a playbook, the canonical file wins.

## Vocabulary at a glance

One-page cheat sheet — everything a cold reader needs so `AGENTS.md` reads without forward references. Defer to the cross-referenced files for full definitions.

**Phase classification (see `playbooks/00-audit.md` Project Scope Classification):**
- `micro` — single-file utility or one-off script; Phases 1 & 2 skipped, goes 0 → 3
- `small` — single-purpose library or CLI; Phases 1 & 2 abbreviated
- `standard` — typical application, 2–10 subsystems; full four-phase workflow by default
- `large` — multiple teams or subsystems with independent release cycles; full workflow + Decomposition Rule. Multi-agent coordination loads only when ≥ 2 agents are active

**Lifecycle mode** (Phase 0 strategy axis): `finite-delivery` — bounded endpoint; `steady-state` — recurring cycles, returning to Phase 0 after terminal housekeeping. Same default four-phase path either way.

**Bounded-change cycle** (`playbooks/00-audit.md`): for an existing project whose accepted decisions and reviewed specs already fully cover the requested work, Phase 0 may mark Phases 1–2 `not-applicable` for that cycle and let the work go 0 → 3. This is re-use of existing design/spec truth, not a shortcut around it.

**Operating roles** (`README.md`): daily operator first, framework maintainer second, adopter third.

**Verdict vocabulary** (Phase 0 audit outputs): `keep` · `keep-with-conditions` · `redesign` · `delete`. No implicit fifth state.

**Gate outcomes** (Phase 0–3 exit): `Go` · `Conditional Go` · `Hold` · `Recycle` · `Kill`. See `playbooks/principles-gates.md` Gate Outcome Vocabulary.

**Completion statuses** (task/session reports, not gate outcomes): `DONE` · `DONE_WITH_CONCERNS` · `BLOCKED` · `NEEDS_CONTEXT`. See `playbooks/principles.md` Completion Status Protocol.

**Gap type taxonomy** (9 types — `playbooks/gaps.md` canonical): `evidence` (spike needed) · `analysis` (deeper thinking) · `decision` (new decision required) · `framework` (framework rule is wrong) · `deviation` (framework-rule exception with expiry) · `conditional` (verdict/gate carry-forward obligation) · `scope-reduction` (explicit specified-requirement deferral) · `failure-pattern` (anti-pattern detected) · `grandfathered` (pre-adoption artifact with expiry).

**Label families** (8 prefixes — `playbooks/identifiers.md`): `D-{n}` design decisions · `G-{n}` gaps · `FR-{n}` functional requirements · `NFR-{n}` non-functional · `PSC-{n}` product success criteria · `SC-{n}` spec conformance criteria · `NG-{n}` product non-goals · `L-{n}` lessons.

**Surfaces** (Phase 0 audit categories — `playbooks/00-audit.md`): Product · Architecture · Runtime · Operations · Security · Quality · Organization. Scope determines which are required (micro: Product+Security; small: Product+Architecture+Security+Quality; standard/large: all 7).

**Required Decisions / failure patterns**: keep these by reference, not from memory. Use `playbooks/01-design.md` for D-1 … D-12 and `playbooks/failure-patterns.md` for the named anti-pattern catalog.

## Five key terms

- **Phase** — one of four stages: `0-audit` → `1-design` → `2-spec` → `3-implement`. Each phase has a gate with mandatory criteria; the project MUST NOT advance to the next phase until the gate passes. Existing projects may use the bounded-change 0 → 3 rule only when `00-audit.md` says the current work is already fully covered by existing design/spec truth. Lifecycle mode is a separate axis: in `steady-state`, terminal completion closes the current cycle rather than the product forever. See `AGENTS.md` Phase Gates.
- **Surface** — one of the audit categories examined in Phase 0 (Product, Architecture, Runtime, Operations, Security, Quality, Organization, plus any project-specific additions). Earlier surfaces constrain later ones. See `playbooks/00-audit.md`.
- **Verdict** — the disposition assigned to every existing element during Phase 0 audit: `keep` / `keep-with-conditions` / `redesign` / `delete`. Every element MUST receive exactly one verdict; there is no implicit fifth state. See `playbooks/glossary.md` verdict.
- **Gap** — unresolved information or missing work tracked in `.agent-state/gaps.md`. Nine gap types are defined in `playbooks/gaps.md`; every gap has a severity, type, lifecycle status, and resolution path, and some types also carry trigger or expiry fields.
- **Decision** — resolved architectural choice recorded in `.agent-state/decisions.md` with a `D-{n}` identifier. D-1..D-12 are reserved for the Required Decisions in `playbooks/01-design.md`; D-13+ are project-specific.

## Reading order for your first session

For the first operational session, start with `AGENTS.md` and follow its Session Start Protocol. Use this file as a companion explainer, not as an alternate startup path.

1. `AGENTS.md` — canonical operational entrypoint: Session Start Protocol, load map, phase boundaries, workspace discipline
2. `playbooks/principles.md` — always-load cross-phase doctrine: Normative Language, Rule Priority, Quality Seeking, Autonomy Protocol, Prohibited Shortcuts, Rationalization Prevention, Required Behaviors
3. `playbooks/00-audit.md` — you always start in Phase 0. Read Quantitative anchors + Decision tree + Worked Example to calibrate.
4. `playbooks/glossary.md` — canonical definitions (artifact, canonical, gap, spec, surface, verify, verdict, etc.) for any term you need while reading the files above

Load on demand (when their trigger condition fires):

- `playbooks/principles-gates.md` — before each phase gate, when preparing an amendment, or when scope classification changes
- `playbooks/principles-conditional.md` — when measuring session-start Context Budget, working multi-agent, preparing a formal handoff, or resolving a rule edge case
- `playbooks/standards.md` — when evaluating, specifying, or producing code
- `playbooks/01-design.md`, `02-spec.md`, `03-implement.md` — when the phase advances
- `playbooks/identifiers.md`, `gaps.md`, `failure-patterns.md`, `zen.md`, `security-threat-model.md`, `release-readiness.md`, `automation.md` — consulted by reference

## Dependency graph

```
AGENTS.md
  │  (Session Start Protocol step 4)
  ▼
playbooks/principles.md   (always-load doctrine)
  │
  ├── principles-gates.md         (gate / amendment rigor)
  ├── principles-conditional.md   (triggered coordination / handoff / edge cases)
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
- [ ] Choose lifecycle mode in `.agent-state/phase.md` and `.agent-state/audit.md` Strategy (`finite-delivery` / `steady-state`)
- [ ] For existing projects, decide whether the current work item is full-cycle or a bounded-change 0 → 3 case under `playbooks/00-audit.md`
- [ ] Begin the Product surface audit per `playbooks/00-audit.md` Per-Surface Entry Format

## When stuck

- Terminology ambiguous → `playbooks/glossary.md`
- A framework rule feels wrong → use the Amendment Protocol in `playbooks/principles-gates.md`. In the aegis framework repo itself, explicit maintainer work uses `AGENTS.md` Framework Maintenance Mode; in governed downstream projects, do NOT self-authorize a rule change as a local shortcut.
- Gate evaluation or failure handling → `playbooks/principles-gates.md` Gate Outcome Vocabulary; report the actual gate outcome as `Go`, `Conditional Go`, `Hold`, `Recycle`, or `Kill` with specific evidence, and report task/session status separately as `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, or `NEEDS_CONTEXT` per `playbooks/principles.md`
- Scope feels too large for one session → `AGENTS.md` Session Start Protocol step 8; propose session sequencing to the user
- Multiple concerns collide in one session → same as above; the defense against the `kitchen-sink-session` failure pattern

## What this framework is NOT

- NOT a linter or a static analyzer. The framework governs *how the project is built*, not the syntax of individual files.
- NOT a replacement for language-specific standards. See `playbooks/standards.md` for aegis's minimum bar; layer language-specific guidelines on top.
- NOT prescriptive about tooling beyond hooks and CI. You choose the build system, test runner, CI provider, and deployment model — the framework provides the governance, you provide the tools.
- NOT a one-shot setup. aegis is an ongoing discipline: every session runs Session Start Protocol, every gate verifies, every amendment goes through the Amendment Protocol in `playbooks/principles-gates.md`.

## Framework rules vs. project state

This section summarizes the read/write split; `AGENTS.md`, D-2, D-11, and D-12 remain canonical for the rules themselves. `README.md` is a projection and should be cross-referenced as a guide, not treated as a canonical owner.

aegis ships as two kinds of files:

- **Framework rules** — `AGENTS.md`, `CLAUDE.md` symlink, and everything under `playbooks/`. Read-only from governed-project agents by default. Framework maintainers change them only through Framework Maintenance Mode and the Amendment Protocol in `playbooks/principles-gates.md`.
- **Maintainer-controlled harness surfaces** — `harness/claude-code/settings.json`, `harness/claude-code/skills/`, `harness/codex/.codex/`, and `harness/codex/.agents/skills/` are shipped source/template locations and MAY be configured by the human maintainer during setup. They are not active from file presence alone; they become active only when synced into each tool's real loaded configuration.
- **Project state** — everything under `.agent-state/`. The agent reads and writes these every session. They record your project's audit findings, decisions, gaps, lessons, and session log.

When you copy aegis into your project, `.agent-state/` becomes YOUR project's working memory; `AGENTS.md` and `playbooks/` remain aegis's rules, while shipped harness templates stay maintainer-controlled setup artifacts. Temporary framework-rule exceptions are recorded in your `.agent-state/gaps.md` with type `deviation`; proposed framework-rule changes use type `framework` — neither propagates back to aegis unless you file it upstream.
