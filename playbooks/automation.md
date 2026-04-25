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
id: playbooks/automation
title: Automation
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
  - playbooks/principles.md
  - playbooks/glossary.md
  - harness/claude-code/hooks-cookbook.md
  - validate.py
supersedes: null
---

# Automation

Projects SHOULD automate framework enforcement rather than rely on manual discipline alone. Automation is the difference between a rule that is "documented" and a rule that is "enforced" — documentation requires remembering and applying, while automation makes violations mechanically impossible (or visibly detected). This playbook defines the agent-neutral automation principles. For the current repo's actual harness status — especially each control's class (`Executable` / `Backstop` / `Advisory`) and activation state — see [`../harness/capability-matrix.md`](../harness/capability-matrix.md).

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **gap**, **harness**, **verify**. "Verify" always means tool-checked with recorded evidence — automation is the mechanism that makes verification cheap and repeatable.

## Core principles

### 1. Automate what rules describe

If a rule can be checked by a script, the check MUST be codified into a hook, lint rule, test assertion, or CI gate — not left to agent discipline. A rule that depends on "the agent remembering to check" is a rule one refactor or one context compression away from being forgotten.

Examples of rules that MUST be codified when the tooling is available:

- File size limits (`standards.md` Small Files — 800 lines max)
- Forbidden identifiers (Naming Table)
- Secret patterns (Security checklist)
- `[NEEDS CLARIFICATION:` markers in authored artifacts (`identifiers.md`)
- Coverage thresholds (test strategy decision D-10)

Examples of rules that CANNOT be fully codified (require judgment — keep as playbook rules):

- "Two competent engineers could disagree" → significant decision (`01-design.md` Quality Seeking)
- "Specification fidelity" → spec review (`02-spec.md` Specification Review)
- "Root cause before fix" → attempt-limit judgment (`03-implement.md` Per-Task Attempt Limit)

### 2. Hook vs. instruction decision tree

When a new rule is added, the author MUST decide: hook or instruction?

- **Deterministic check** (same pass/fail answer given the same inputs)? → hook.
- **Structural check** (grep, AST walk, regex over code or docs)? → hook.
- **Requires judgment or multi-paragraph context**? → instruction in a playbook.
- **Both**? → hook for the mechanical part, instruction for the judgment part — tag the gate item `[M+J]` per the `[M]`/`[J]` convention in `00-audit.md`, `01-design.md`, `02-spec.md`, `03-implement.md`, and `standards.md`.

### 3. CI mirrors local verification

The same checks that run locally (via hooks, `/verify`, or manual invocation) MUST also run in CI. This creates a single source of truth for quality gates: a local pass implies a CI pass, and a CI failure is a reproducible local failure. The agent MUST NOT rely on CI for checks that are not also runnable locally — debugging a CI-only failure wastes time and breaks the verification feedback loop.

### 4. Deterministic commands become hooks

If a command always produces the same answer given the same inputs (`ruff check`, `mypy`, `pytest`, `cargo check`, `eslint --fix`), it belongs in a hook. The hook fires on `PostToolUse` (or the harness equivalent) after every Write/Edit and catches the violation before it compounds.

Non-deterministic commands (those that depend on network state, time, or random data) MUST NOT be put in hooks — they cause flaky fail-open behavior that is worse than no hook.

### 5. Fail-open is a failure mode

A hook that silently no-ops on error is worse than no hook — it gives the illusion of protection. Every hook MUST be tested with a known-failing input (does it block?), a known-passing input (does it allow?), and a malformed input (does it crash or fail-open?). The third case is the one most often skipped. Hooks MUST be written defensively: parse input first, validate types, return error codes meaningfully. See per-harness cookbooks for exact defensive-hook patterns.

## Mechanical validation

`./validate.py` at the repo root automates the `[M]` portion of the adversarial review protocol. It is harness-agnostic (Python 3 stdlib only, no external dependencies) and SHOULD be run before every release and, where the harness supports it, wired as a `PostToolUse` or pre-commit hook. The exact check list lives in `validate.py` itself and may grow over time; the summary below is representative, not canonical:

1. Frontmatter on `AGENTS.md` and every `playbooks/*.md` parses and carries all required fields (`id`, `title`, `version`, `last_reviewed`, `applies_to`, `severity`, `mechanical_items`, `judgment_items`, `mixed_items`, `references`, `supersedes`). Playbooks with no gate items declare `mechanical_items: 0`, `judgment_items: 0`, `mixed_items: 0`. Playbooks with no superseded predecessor declare `supersedes: null`.
2. Every `references:` entry resolves to an existing file path.
3. Every `mechanical_items` / `judgment_items` / `mixed_items` declared count matches the body's pure `[M]` / pure `[J]` / `[M+J]` gate-tag count (tags in the bold gate-marker form: two asterisks, square brackets, asterisks). The three counts are independent: `[M+J]` items are tracked under `mixed_items` and are NOT counted toward either pure total. Prose mentions of these tags MUST use backtick-wrapped form (as in this paragraph) so they do not register as real gate items.
4. Every state file in `.agent-state/` begins with a `<!-- SCHEMA: ... -->` block.
5. `CLAUDE.md` is a symlink to `AGENTS.md` (AGENTS.md is the canonical entry file).
6. Version agrees across `AGENTS.md` frontmatter, `AGENTS.md` body banner, every playbook frontmatter, and the top versioned section of `CHANGELOG.md`.
7. Every Evidence cell in every Verification Coverage Matrix block in `.agent-state/phase.md` (and `phase-archive.md` when present) carries a verifiable reference per `principles-gates.md` Verification Coverage Matrix: `file.md:N` | `file.md#anchor` | `sha256:{64 hex}` | `#session-YYYY-MM-DD-slug` | `<subagent:NAME>` | literal `(pending)` when the row's Result cell is also `pending`. Prose-only cells fail — a filled-in cell with hand-wave ("looked fine", "tests passed") is the gameability vector this check closes.

Exit code 0 means clean; non-zero prints a bulleted failure list on stderr. The validator covers `[M]`-class checks only — `[J]` judgment items remain the reviewer's responsibility per Core Principle 1 ("rules that CANNOT be fully codified").

When the validator disagrees with a frontmatter count or references entry, the agent MUST verify which side is correct per `principles.md` Required Behaviors #5 (evidence before assertion — verify before acting on feedback). Either the declared count is stale (update the frontmatter) or the body has drifted from the documented convention (restore the convention or extend the validator intentionally via an amendment).

### Invocation cadence

The validator SHOULD run at four cadences, each serving a different quality-control layer:

1. **Pre-gate (every phase transition)** — before reporting `Go` or `Conditional Go` on any phase gate. A failing validator check at gate time MUST downgrade the outcome to `Hold`.
2. **Pre-commit (every commit)** — wired as a git `pre-commit` hook, a Claude Code `PostToolUse` hook on `Write|Edit`, or a Husky/lefthook step. Prevents broken frontmatter or version drift from being committed.
3. **CI (every pull request)** — configured as the first blocking CI job. Mirrors local pre-commit but runs in a clean environment to catch issues that pass locally but fail in CI.
4. **Pre-release** — part of the `release-readiness.md` checklist. A release-blocking check; a failing validator MUST NOT ship.

For human-facing invocation guidance (how to run, how to read output, when to invoke), see the README Validator subsection.

### Lessons-Gap Backstop

The Release Readiness gate enforces a quantitative backstop on the Lessons → Framework-gap feedback loop in `principles.md` Required Behaviors #8. Mechanical formula:

```
L = grep -c '^### L-' .agent-state/lessons.md
F = grep -cE '^\*\*Type:\*\*\s*framework\s*$' .agent-state/gaps.md
```

When `L − F > 5` (five or more lessons accumulated without any resulting framework-gap proposal), the Release Readiness gate MUST emit `Hold` until either (a) the agent drafts `framework` gaps for the recurring lesson patterns, or (b) the agent records an explicit `[J] — RISK_ACCEPTED_BY_USER` justification per `principles-gates.md` Adversarial Review Protocol citing user acceptance that the lessons do not indicate a framework defect. The bounded threshold prevents silent accumulation that an unbounded "SHOULD approximately track" rule would not catch.

## Principle → Rule → Enforcement Matrix

This matrix is the reverse index: given any aegis discipline, it names which rule citation carries the discipline and where the mechanical enforcement lives. Use it to answer "where is X enforced?" without reading every playbook.

| Discipline | Canonical rule | Enforcement mechanism | Location |
|---|---|---|---|
| Verdict Discipline | `AGENTS.md` Verdict Discipline | Audit review at phase gate; glossary canonical enum | `00-audit.md` Phase Gate; `glossary.md` verdict |
| Authority Discipline | `AGENTS.md` Authority Discipline | Whole-System Composition Check; Naming Table grep | `01-design.md` Composition Check; `03-implement.md` Post-Change Verification naming check; PreToolUse hook in `hooks-cookbook.md` |
| Traceability | `AGENTS.md` Session Start step 6; `03-implement.md` Traceability | Commit-msg hook + grep of `Implements:` / `Covers:` trailers | `hooks-cookbook.md` commit-msg hook; `03-implement.md` Post-Change Verification |
| Phase gates | `AGENTS.md` Phase Gates | Three-tier criteria + gate outcome; Verification Coverage Matrix | `principles-gates.md` Gate Outcome Vocabulary; per-phase playbook Phase Gate section |
| Verification Coverage | `principles-gates.md` Verification Coverage Matrix | 5-perspective matrix with verifiable Evidence cells; Stop hook; `validate.py` check #7 | `principles-gates.md` Verification Coverage Matrix; `hooks-cookbook.md` Stop hook; `validate.py` `check_evidence_verifiability` |
| File-size / placement | `standards.md` Code Quality; `01-design.md` D-11 | PreToolUse hook (content size); file-path grep at gate | `hooks-cookbook.md` PreToolUse Write; `03-implement.md` Post-Change Verification |
| Secret leakage | `standards.md` Security; `AGENTS.md` Workspace Discipline | PreToolUse hook (secret regex); `.gitignore`; CI secret scan | `hooks-cookbook.md` PreToolUse Write/Edit; project CI |
| Framework read-only | `AGENTS.md` Workspace Discipline | installed Claude Code `permissions.deny` derived from the canonical settings template; optional OS `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/` elsewhere | `harness/claude-code/settings.json`; `harness/capability-matrix.md` |
| Frontmatter schema | `automation.md` Mechanical validation | `validate.py` checks 1-3 | `validate.py` |
| Version consistency | `principles-gates.md` Amendment Protocol | `validate.py` check 6 | `validate.py` |
| CLAUDE.md symlink | `AGENTS.md` operational entrypoint banner | `validate.py` check 5 | `validate.py` |
| State SCHEMA presence | `automation.md` Mechanical validation | `validate.py` check 4 | `validate.py` |
| Test-spec traceability | `03-implement.md` Traceability → Test traceability | grep/validator check of slugged test-name suffixes + in-file `Covers:` comments (commit-level `Covers:` is metadata only) | `03-implement.md` Post-Change Verification; `validate.py` check 13; optional CI job |
| STRIDE threat model | `security-threat-model.md` | Mechanical boundary/STRIDE-letter grep at Phase 1 gate | `01-design.md` Design Closure Gate; `security-threat-model.md` Mechanical checks |
| Conventional commits | `standards.md` Git Conventions; `03-implement.md` Traceability → Commit message format | commit-msg git hook (regex + trailer) | `hooks-cookbook.md` commit-msg hook |
| Coverage targets | `standards.md` Testing; `01-design.md` D-10 | Per-layer test runners with `--cov-fail-under` | `03-implement.md` Post-Change Verification; D-10 decision entry |
| Accessibility | `standards.md` Accessibility; `01-design.md` D-13+ Accessibility Model | axe-core / pa11y CI scans; manual audit cadence | D-13+ decision entry; CI config |
| Placeholder scan | `01-design.md` Design Closure Gate; `02-spec.md` Quality Checks | `grep -rnE 'TBD|TODO|FIXME'` at gate | Per-phase Phase Gate / Quality Checks |
| Adversarial review | `principles-gates.md` Adversarial Review Protocol (incl. Per-phase timing hooks table) | Subagent in fresh context at gate | Phase Gate intro of each phase playbook references the protocol |

## Per-harness implementation pointers

The principles above are agent-neutral. The current repo wiring is not symmetrical across harnesses. Read [`../harness/capability-matrix.md`](../harness/capability-matrix.md) before assuming parity.

| Harness | What this repo actually ships now | Implementation reference |
|---|---|---|
| **Claude Code** | canonical `settings.json` source/template + hook recipes; nothing is active until installed into Claude Code's loaded settings path | `harness/capability-matrix.md`, `harness/claude-code/README.md`, `harness/claude-code/hooks-cookbook.md` |
| **Codex** | documentation + optional `config.toml.example`; no active blocking control | `harness/capability-matrix.md`, `harness/codex/README.md` |
| **Cursor** | advisory `.mdc` templates under `harness/cursor/.cursor/rules/`; not active at repo-root `.cursor/rules/` | `harness/capability-matrix.md`, `harness/cursor/README.md` |
| **CI** | GitHub Actions example only; no live workflow under `.github/workflows/` in this repo | `harness/capability-matrix.md`, `harness/ci/README.md` |

For Claude Code specifically, the cookbook covers hook stdin JSON shape, exit code semantics, matcher regex behavior, the recommended hook set (SessionStart, PreCompact, PostToolUse, PreToolUse Write/Edit, PostToolUse Bash, Stop), native `permissions.deny` write protection when the template is installed, the `settings.json` template, LSP plugin configuration, skill authoring constraints, and hook troubleshooting.

For Codex and Cursor, compensation strategies dominate — the agent is trusted to self-regulate unless the adopter adds OS-level `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/`, git hooks, and CI.

## External knowledge and services (MCP)

Projects SHOULD integrate external knowledge sources via MCP (Model Context Protocol) servers for Quality Seeking's pre-implementation research step. MCP is an open protocol — servers that speak it are portable across agents that support it.

Configured in `.mcp.json` at project root (Claude Code) or the equivalent per-harness location. The agent MUST review each MCP server's source and permissions before enabling — MCP servers execute code and may have network access.

Recommended integration categories (protocol-neutral; the agent uses whichever server is available in the current harness):

- **Documentation lookup** (e.g., Context7) — look up API docs, framework patterns, and version-specific behavior before implementing
- **GitHub search** — find existing implementations, templates, and battle-tested patterns before writing new code
- **Package registry** — evaluate library health, maintenance status, and alternatives for Dependency Discipline (`standards.md`)

See `harness/claude-code/hooks-cookbook.md` for the Claude Code `.mcp.json` example and activation syntax. Other harnesses follow the MCP spec's standard server invocation.

## Task tracking

When a harness provides an ephemeral task tracker (Claude Code's TaskCreate/TaskUpdate, Cursor's task panel, etc.), the agent SHOULD use it to track intra-session progress:

- One task per major work unit within a phase (each audit surface, each decision, each specification)
- Status transitions: `todo` → `in_progress` → `completed` (or `blocked`)
- Task dependencies MAY be used to enforce ordering where the harness supports them

Tasks are ephemeral session tools — they complement but MUST NOT replace the persistent state files in `.agent-state/`. When the session ends, task state is lost; `.agent-state/` remains. Any work that matters beyond the current session MUST be recorded in `phase.md`, `decisions.md`, or `gaps.md` — not just in the task tracker.
