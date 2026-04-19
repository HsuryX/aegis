# CI harness

Agent-neutral CI templates. Every adopter — Claude Code, Codex, Cursor, or anything that reads `AGENTS.md` — can use these as a baseline. Claude Code's `PostToolUse` hooks run locally; Codex and Cursor have no hook equivalent; CI is the only mechanical gate common to all three.

## What's here

| File | Purpose |
|---|---|
| `github-actions-aegis-verify.yml.example` | GitHub Actions workflow mirroring the Verification Sequence from `playbooks/03-implement.md` — Build → Type check → Lint → Test → Secret scan → `validate.py` → Placeholder scan. |

## How to adopt

1. Copy the `.example` file to the adopting project's `.github/workflows/` directory and drop the `.example` suffix.
2. Replace every `<project ...>` placeholder with the adopter's real build/test commands. Delete any step that does not apply (e.g. projects without a type checker SHOULD remove the Type check step rather than leaving a no-op).
3. Confirm `python3 validate.py` returns 0 locally before pushing the workflow. The workflow runs `validate.py`; if it fails locally, it will fail in CI.
4. On GitLab, Bitbucket Pipelines, CircleCI, or other CI platforms, translate the step sequence directly — the logical steps are the same; only the YAML syntax changes.

## Why this ships in the framework

`playbooks/automation.md` Principle 3 ("CI mirrors local verification") requires adopters to wire a CI job equivalent to the local hooks. Without a shipped template, every adopter re-derives the same workflow from the skeleton quoted in `harness/codex/README.md`. This CI harness ships a ready-to-fork GitHub Actions template so adopters can wire verification in one step.

## Scope proportionality

`micro` and `small` scope projects (per `00-audit.md` Strategy Decision) MAY skip the Secret scan and Placeholder scan steps if the project's surface is narrow enough that the grep cost exceeds the signal. `standard` and `large` scope projects SHOULD run the full sequence.
