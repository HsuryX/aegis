---
name: verify
description: Use when implementation changes are complete and ready for quality verification before phase advancement
---

# /verify

Runs the full Verification Sequence defined in `playbooks/03-implement.md`. Use after every meaningful implementation change and before advancing any phase gate.

## Steps (ordered — each MUST pass before the next is meaningful)

1. **Build** — verify the project compiles/builds without errors
2. **Type check** — run the type checker if applicable
3. **Lint** — run the project linter if configured
4. **Test** — run the full test suite; record pass count and coverage percentage
5. **Security scan** — check for hardcoded secrets and known vulnerabilities
6. **Self-diff review** — the implementing agent reviews its own diff to confirm it matches design intent (distinct from the subsequent Code Review by a separate agent — see `playbooks/03-implement.md` Code Review section)

The agent MUST record actual command output as evidence in the session log in `.agent-state/phase.md` and MUST NOT check items from memory or confidence.

## When to invoke

- After every meaningful implementation change (the Post-Change Verification gate in `playbooks/03-implement.md`)
- Before advancing a phase gate (Phase 1 → 2, Phase 2 → 3, Phase 3 → project completion)
- After post-implementation cleanup (to confirm cleanup did not introduce regressions)
- Before marking any session as complete

## Evidence format

Record in `phase.md` session log:

```
Verification run — 2026-04-15 14:30 UTC
- Build: PASS (exit 0)
- Type: PASS (mypy: 0 errors)
- Lint: PASS (ruff: 0 errors)
- Test: PASS (pytest: 142 tests, 0 failures, 87% coverage)
- Security: PASS (pip-audit: 0 vulnerabilities)
- Diff review: PASS (3 files changed, matches D-11 intent)
```

Free-form claims like "tests pass" without the command output that proves it are explicitly forbidden — see `playbooks/principles.md` Completion Status Protocol.

**Verification Coverage Matrix (at phase gates)**. When closing a phase gate, the session log MUST contain the 5-perspective matrix (Structural / Semantic / Adversarial / End-to-end / Cold read) per `playbooks/principles.md` Verification Coverage Matrix. Every `Evidence` cell MUST carry a verifiable reference — a file path + line number (e.g., `specs/auth.md:42`), a SHA-256 hash of captured command output, a session-log anchor, or a subagent-output reference (`<subagent:security-reviewer>`). Prose-only cells fail the gate. Empty cells also fail — incomplete matrices hold the gate, they do not advance it.

**Test-to-spec traceability.** Every test MUST cite the `SC-{n}` or `FR-{n}` it validates, in one of three forms: commit trailer `Covers: SC-3, FR-7`, test-name suffix `covers_SC_3`, or in-file comment `// Covers: SC-3` as the first line of the test body. At Phase 3 gate, `grep -rnE '(Covers:|covers_)(SC|FR)-\d+' tests/ src/` MUST return ≥ the count of `SC-{n}` entries across specs.

**Legacy-test grandfathering at adoption time**. For projects adopting aegis on pre-existing codebases, legacy tests MAY be grandfathered under a single `gaps.md` entry (type: `grandfathered`, severity: `info`). The grandfathered gap MUST list the initial test-file set (or a `git log` anchor) so the expiry is verifiable. Tests edited or added after adoption MUST carry the `Covers: SC-{n}` / `Covers: FR-{n}` traceability per the three accepted forms above — grandfathering is NOT retroactive. See `playbooks/gaps.md` Gap Type Taxonomy (grandfathered row) and `playbooks/03-implement.md` Test Traceability for the canonical rule.

## Required evidence per claim

| Claim | Required Evidence | NOT Sufficient |
|-------|------------------|----------------|
| "Tests pass" | Test command output showing 0 failures | Previous run, "should pass", partial suite |
| "Build succeeds" | Build command with exit 0 | Linter passing, "looks correct" |
| "Bug fixed" | Test reproducing original symptom now passes | Code changed and assumed fixed |
| "Requirements met" | Line-by-line spec checklist verified | Tests passing (tests may not cover all reqs) |
| "No regressions" | Full test suite output, not just changed tests | Spot-checking a few tests |
