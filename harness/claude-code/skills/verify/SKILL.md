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
- Before advancing a phase gate (Phase 1 → 2, Phase 2 → 3, Phase 3 → terminal completion for the active lifecycle mode)
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

**Verification Coverage Matrix (at phase gates)**. When closing a phase gate, the session log MUST contain the 5-perspective matrix (Structural / Semantic / Adversarial / End-to-end / Cold read) per `playbooks/principles-gates.md` Verification Coverage Matrix. Every `Evidence` cell MUST carry one of the canonical verifiable forms from `playbooks/principles-gates.md`: `file.md:N`, `file.md#anchor`, `sha256:{64 hex}`, `#session-YYYY-MM-DD-slug`, `<subagent:NAME>`, or literal `(pending)` only when the row's `Result` is also `pending`. Prose-only or unresolvable cells fail the gate. Empty cells also fail — incomplete matrices hold the gate, they do not advance it.

**Test-to-spec traceability.** Every test MUST cite the path-qualified `specs/<spec>.md:SC-{n}` or `specs/<spec>.md:FR-{n}` it validates in one of two accepted per-test forms: test-name suffix `covers_specs_auth_md_SC_3` or in-file comment `// Covers: specs/auth.md:SC-3` in the test file. In suffix form, the spec path slug lowercases the spec path, replaces every non-alphanumeric character with `_`, and strips leading/trailing `_` (for example `specs/auth.md` → `specs_auth_md`). Optional commit-level `Covers:` trailers remain allowed as change-summary metadata, but they do NOT satisfy per-test traceability. At Phase 3 gate, `grep -rnE '^\s*(//|#)\s*Covers:\s*specs/[^ ,:]+\.md:(SC|FR)-[0-9]+|covers_[A-Za-z0-9_]+_(SC|FR)_[0-9]+' tests/ src/` MUST return ≥ the count of declared `SC-{n}` entries across specs, and `python3 validate.py` check 13 MUST confirm set coverage on the fully qualified `specs/<spec>.md:SC-{n}` identifiers.

**Legacy-test grandfathering at adoption time**. For projects adopting aegis on pre-existing codebases, legacy tests MAY be grandfathered under a single `gaps.md` entry (type: `grandfathered`). The grandfathered gap MUST list the initial test-file set (or a `git log` anchor) so the expiry is verifiable. Tests edited or added after adoption MUST carry the required path-qualified in-file `Covers:` comment or equivalent suffix form per the two accepted per-test forms above — grandfathering is NOT retroactive. See `playbooks/gaps.md` Gap Type Taxonomy (grandfathered row) and `playbooks/03-implement.md` Test Traceability for the canonical rule.

## Required evidence per claim

| Claim | Required Evidence | NOT Sufficient |
|-------|------------------|----------------|
| "Tests pass" | Test command output showing 0 failures | Previous run, "should pass", partial suite |
| "Build succeeds" | Build command with exit 0 | Linter passing, "looks correct" |
| "Bug fixed" | Test reproducing original symptom now passes | Code changed and assumed fixed |
| "Requirements met" | Line-by-line spec checklist verified | Tests passing (tests may not cover all reqs) |
| "No regressions" | Full test suite output, not just changed tests | Spot-checking a few tests |
