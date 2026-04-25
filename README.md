# aegis

A governance framework for AI-assisted software development. Guides AI agents through a structured, quality-gated workflow from analysis to implementation — portable across Claude Code, Codex, Cursor, and any agent that reads `AGENTS.md`.

## The Problem

AI agents without governance constraints make inconsistent architectural decisions, skip quality checks, rationalize shortcuts, and produce output that is hard to maintain. This framework provides the guardrails.

## Operating roles

aegis serves three roles, in this order:

1. **Daily operator** — the agent or maintainer using aegis to govern a concrete project change safely.
2. **Framework maintainer** — the person improving aegis itself.
3. **Adopter** — the maintainer wiring aegis into a target harness and CI environment.

The framework is optimized for the daily operator first. Maintainer ceremony and adopter setup exist to support governed-project outcomes, not to become the product.

## How It Works

Four phases, each with a quality gate that must pass before advancing:

| Phase | Purpose | Key Output |
|-------|---------|------------|
| **0. Audit** | Catalogue what exists, identify what is wrong | `audit.md` with verdicts per surface |
| **1. Design** | Close all major architectural decisions | `decisions.md` with `Accepted` decisions (count varies by scope; see `playbooks/01-design.md` Required Decisions) |
| **2. Spec** | Write canonical specifications for the current canonical system | Specifications with conformance criteria |
| **3. Implement** | Write code that faithfully implements specifications | Verified code traced to decisions |

The agent reads `AGENTS.md` at session start (Claude Code reads `CLAUDE.md`, which is a symlink to `AGENTS.md`). `AGENTS.md` is the thin operator kernel and load map that bootstraps the current playbooks.

Lifecycle mode is a separate Phase 0 strategy choice recorded in `.agent-state/audit.md` and `.agent-state/phase.md`: `finite-delivery` or `steady-state`. Both modes use the same four phases by default; `steady-state` means terminal completion closes the current cycle and the next material work item restarts at Phase 0. Existing projects may also use a bounded-change 0 → 3 cycle when Phase 0 explicitly records that accepted decisions and reviewed specs already fully cover the requested work and nothing contract-, boundary-, runtime/operations-, trust-boundary-, naming-, or product-scope-shaping is changing.

## Structure

```
AGENTS.md                            # Thin operator kernel + load map (operational entrypoint)
CLAUDE.md                            # Symlink → AGENTS.md (Claude Code compatibility)
CHANGELOG.md                         # Version history + semver policy (Keep a Changelog format)
LICENSE
.gitignore
README.md                            # This file — human onboarding
ONBOARDING.md                        # Companion primer after AGENTS-first startup
validate.py                          # Mechanical validator (17 checks; see module docstring)
playbooks/                           # Canonical doctrine and phase playbooks (read-only for the agent)
  principles.md                      # Always-load cross-phase doctrine
  principles-gates.md                # Gate/amendment-scoped rigor + SYNC-IMPACT + gate outcomes
  principles-conditional.md          # Triggered context-budget / coordination / handoff / spirit=letter rules
  standards.md                       # Code quality, testing, security, accessibility standards
  glossary.md                        # Canonical definitions (verify/validate/review, spec/contract, etc.)
  identifiers.md                     # Label families (D-design decisions · G-gaps · FR-functional reqs · NFR-non-functional · PSC-product success criteria · SC-spec conformance criteria · NG-product non-goals · L-lessons) + marker rules
  automation.md                      # Agent-neutral automation principles
  zen.md                             # The Twenty aphorisms + tension protocol
  gaps.md                            # Gap playbook — 9-type taxonomy + lifecycle + phase-gate interaction
  failure-patterns.md                # Named failure modes + counter rules
  release-readiness.md               # Pre-release checklist
  security-threat-model.md           # STRIDE + LLM-aware threat classes
  00-audit.md                        # Phase 0 playbook
  01-design.md                       # Phase 1 playbook
  02-spec.md                         # Phase 2 playbook
  03-implement.md                    # Phase 3 playbook
.agent-state/                        # Agent's working documents
  phase.md                           # Current phase, terminal phase, lifecycle mode, gate status, session log
  decisions.md                       # Decision ledger + naming table
  gaps.md                            # Gap tracker (canonical gap entries with severity, lifecycle, type, and resolution fields)
  audit.md                           # Audit register with surface verdicts
  lessons.md                         # Consolidated lessons + cross-project amendment candidates
harness/                             # Agent-specific adapters (the 5% that varies per agent)
  claude-code/                       # Claude Code harness (hooks, permissions, skills)
    settings.json                    # Permissions (deny rules) and hook wiring
    hooks-cookbook.md                # Claude-Code-specific hook/permission/LSP/MCP/skill reference
    skills/                          # Project skills invoked via /{name}
      verify/SKILL.md                # /verify — full Verification Sequence
      decision/SKILL.md              # /decision — new decision entry
      gap/SKILL.md                   # /gap — new gap entry
      audit-surface/SKILL.md         # /audit-surface — new audit surface entry
      phase-status/SKILL.md          # /phase-status — current state + gate status
    README.md                        # What Claude Code enforces natively + limitations
  codex/                             # Codex CLI harness (reads AGENTS.md natively)
    config.toml.example              # Optional Codex config starting point
    README.md                        # What Codex enforces + compensation strategies
  cursor/                            # Cursor harness (.cursor/rules/*.mdc)
    .cursor/rules/                   # MDC rule files — thin pointers to playbooks/
      principles.mdc                 # Cross-phase rules (alwaysApply)
      standards.mdc                  # Quality standards (alwaysApply)
      phase-0.mdc                    # Phase 0 rules (attach/reference when in Phase 0)
      phase-1.mdc                    # Phase 1 rules (attach/reference when in Phase 1)
      phase-2.mdc                    # Phase 2 rules (attach/reference when in Phase 2)
      phase-3.mdc                    # Phase 3 rules (attach/reference when in Phase 3)
    README.md                        # What Cursor enforces + compensation strategies
  ci/                                # Agent-neutral CI templates
    github-actions-aegis-verify.yml.example  # Reusable GitHub Actions workflow (Verification Sequence)
    README.md                        # How to adopt per CI platform
tools/
  bootstrap.sh                       # One-shot installer — copies files, resets state, runs validate.py
```

> **Project artifacts.** `specs/` and `tests/` are not shipped — adopters create them per project as Phase 2 specifications and Phase 3 tests are produced. When `specs/threat-model.md` is required by D-5 applicability, it is created during Phase 1; when `specs/schemas/` is required by a machine-readable contract, it is created during Phase 2.

> **Note.** Agent-local configuration at `.claude/settings.local.json` is per-project and not shipped with the framework.

**Playbooks** are read-only for the agent. **Project-state ledgers** are the agent's working documents.

## Adoption

### New Project (quick start)

```bash
# From a fresh clone of aegis:
./tools/bootstrap.sh /path/to/your-project
```

The bootstrap script copies framework files (preserving the `CLAUDE.md → AGENTS.md` symlink via `cp -a`), resets `.agent-state/` to template-only, prompts for project name + scope + lifecycle mode + type + terminal phase, writes initial `phase.md`, and runs `validate.py` for a clean-state smoke test.

After bootstrap, follow this AGENTS-first startup order:

1. `cd /path/to/your-project`
2. Read `AGENTS.md` first; use `ONBOARDING.md` as companion setup context
3. Begin Phase 0 audit per `playbooks/00-audit.md`

During Phase 1 (when the toolchain is decided), configure hooks in the real loaded Claude settings path using `harness/claude-code/settings.json` as the shipped source — see `harness/claude-code/hooks-cookbook.md` Settings Template; replace `<formatter>`, `<linter>`, `<build-command>` with your tools. Optionally configure `.mcp.json` for documentation and search MCP servers. Codex and Cursor users follow the setup checklists in `harness/codex/README.md` and `harness/cursor/README.md`.

### New Project (manual install)

If the bootstrap script cannot be used:

```bash
# Copy the framework into your project root (use cp -a to preserve the CLAUDE.md → AGENTS.md symlink)
cp -a AGENTS.md CLAUDE.md CHANGELOG.md LICENSE validate.py .gitignore README.md ONBOARDING.md playbooks .agent-state harness tools /path/to/your-project/
```

Then manually reset `.agent-state/` to template-only and edit `phase.md` with your project's scope, lifecycle mode, and type.

### Existing Project

Copying aegis into a pre-existing codebase can conflict with files that already exist. Resolve collisions per these rules (the bootstrap script handles most automatically; manual installers follow the same logic):

- **`AGENTS.md` or `CLAUDE.md` collision** — keep the existing file as `AGENTS.local.md` and adopt aegis's as canonical. Record a `framework` gap to reconcile any project-specific rules from the local file into aegis's Amendment Protocol in `playbooks/principles-gates.md`.
- **`CHANGELOG.md` collision** — keep the target project's CHANGELOG. Prepend aegis's Versioning Policy section at the top if the target doesn't already cover semver.
- **`.agent-state/` collision (non-template contents)** — archive to `.agent-state/pre-aegis-archive/` before overwriting. Start Phase 0 with fresh templates; reference the archive for historical context only.
- **`harness/` collision** — if the target has a different `harness/` (e.g., a build harness), rename it to `harness.project/` and let aegis use `harness/claude-code/`, `harness/codex/`, `harness/cursor/`. If the target has an aegis-shaped harness already, diff `hooks-cookbook.md` and merge.
- **`playbooks/` collision** — always overwrite with aegis's canonical set. Project-specific playbooks MAY live in a separate `playbooks/local/` directory that aegis does not touch.
- **`validate.py` collision** — always overwrite with aegis's canonical version (the validator is part of the framework contract).
- **`.gitignore` collision** — merge entries; aegis's additions are non-conflicting patterns.

After resolving collisions:

1. For clean-room rewrites: move existing code to `_legacy/` (read-only reference)
2. For in-place evolution: the existing codebase is the workspace — no `_legacy/` needed
3. For hybrid evolution: some subsystems move to `_legacy/`, others stay in place (see `playbooks/00-audit.md`)
4. Configure hooks and MCP per the harness README checklist
5. Start Phase 0 (Audit) against the existing codebase

### Spec-Only Projects

For projects that produce specifications but no implementation code (governance documents, API contracts), set the terminal phase to `2-spec` in `phase.md`. Phase 3 is marked `not-applicable`. In `steady-state` mode, completing Phase 2 closes the current governance cycle rather than the product forever.

## Validator

Run `python3 validate.py` at four cadences:

- **Pre-gate** — before reporting `Go` or `Conditional Go` on any phase gate. A failing validator check MUST downgrade the outcome to `Hold`.
- **Pre-commit** — wired as a git `pre-commit` hook or a Claude Code `PostToolUse` hook. Prevents frontmatter / version drift from being committed.
- **CI** — as the first blocking CI job on every PR.
- **Pre-release** — part of the `playbooks/release-readiness.md` checklist.

Interpretation: exit code 0 = clean; non-zero prints a bulleted failure list on stderr with check number for diagnosis. See `playbooks/automation.md` § Mechanical validation for the full check list; see `harness/claude-code/hooks-cookbook.md` for harness-specific wiring.

## Customization Points

Design decisions are numbered D-1 through D-12 (defined in `playbooks/01-design.md`); project-specific decisions start at D-13. See `playbooks/identifiers.md` for the full label system (`D-`/`G-`/`FR-`/`NFR-`/`PSC-`/`SC-`/`NG-`/`L-`).

| What | Where | How |
|------|-------|-----|
| Hook commands | `harness/claude-code/hooks-cookbook.md` template | Replace `<formatter>`, `<linter>`, `<build-command>` |
| Coverage targets | `playbooks/standards.md` | Override via test strategy decision (D-10) |
| Additional design decisions | `playbooks/01-design.md` | Add as D-13+ |
| MCP servers | `.mcp.json` | Add documentation lookup, search, registry tools |
| Project skills | `harness/claude-code/skills/` | Ship `/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status` (five baseline skills) |

## Key Principles

- **Verdict Discipline** — every existing element gets an explicit `keep` / `keep-with-conditions` / `redesign` / `delete` verdict (see `AGENTS.md` Verdict Discipline for the full semantics)
- **Quality Seeking** — generate alternatives, argue against your preference, then decide
- **Authority Discipline** — one fact, one canonical owner, no duplicate truth
- **Traceability** — every code change traces to a recorded design decision
- **Verification over Confidence** — run checks, record evidence, never claim done without proof

## Relationship to AGENTS.md and CLAUDE.md

This section summarizes the symlink mechanics and reader-vs-agent split. The canonical rules still live in `AGENTS.md`, D-2, D-11, and D-12.

This README is for humans browsing the repository. `AGENTS.md` is the operational entrypoint, but it is intentionally thin: Session Start Protocol, load map, Foundational / Verdict / Authority discipline, phase gates, the implementation boundary, phase regression, and workspace discipline live there. The deeper doctrine is split into `playbooks/principles.md` (always-load), `playbooks/principles-gates.md` (gate/amendment-scoped rigor), and `playbooks/principles-conditional.md` (triggered coordination/handoff/context rules). `CLAUDE.md` is a symlink to `AGENTS.md` kept at the repo root so Claude Code continues to find the entry point via its native convention — both names resolve to the same file.

Any coding agent that reads agent instruction files can consume this framework:

- **Claude Code** reads `CLAUDE.md` (which is the symlink) and bootstraps via the Session Start Protocol
- **Codex and other AGENTS.md-aware agents** read `AGENTS.md` directly
- **Cursor** ships rule templates under `harness/cursor/.cursor/rules/`; adopters must copy them to repo-root `.cursor/rules/` to activate them, and even then the rules remain advisory rather than hard-blocking
- **Other agents** can read `AGENTS.md` manually or via a lightweight adapter

Do not duplicate framework content between this README and `AGENTS.md` — this README points to `AGENTS.md` as the source of truth.

## License

MIT — see `LICENSE`.
