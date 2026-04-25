# CI harness

Agent-neutral CI templates. Read this file together with [`../capability-matrix.md`](../capability-matrix.md). This directory ships templates only — there is no active CI workflow in this repo until an adopter copies one into `.github/workflows/` or the equivalent CI location.

## What's here

| File | Purpose |
|---|---|
| `github-actions-aegis-verify.yml.example` | GitHub Actions workflow mirroring the Verification Sequence from `playbooks/03-implement.md` — Build → Type check → Lint → Test → Secret scan → `validate.py` → Placeholder scan. |

## Status in this repo

- **Active now:** none
- **Shipped here:** GitHub Actions example only
- **Becomes active when:** copied to repo-root `.github/workflows/` and enabled by the CI provider
- **Recommended pairing:** local/manual `python3 validate.py` plus harness-specific setup from the relevant README


## Minimum safety contract answers

1. **Protected surfaces (`AGENTS.md`, `CLAUDE.md`, `playbooks/`, `_legacy/`)** — **N/A in CI until installed**. This directory does not protect those paths by itself; once a workflow is installed, CI can detect violations or fail a PR, but it still does not prevent a local write the way `permissions.deny` or OS `chmod` can.
2. **Session Start Protocol** — **N/A / absent**. CI does not run session-start discipline.
3. **`python3 validate.py`** — **shipped but inactive here; automatic after installation**. In this repo today it is still a manual command; after copying the workflow to `.github/workflows/`, CI runs it automatically.
4. **Build / Type / Lint / Test / Security verification** — **shipped but inactive here**. The shipped workflow example covers them, but nothing is active until the adopter installs the workflow and replaces the placeholders.
5. **Control class + activation state** — the CI harness is a **Backstop** that is **Shipped but inactive** until a workflow is installed; this README's prose is advisory guidance only.

## How to adopt

1. Copy the `.example` file to the adopting project's `.github/workflows/` directory and drop the `.example` suffix.
2. Replace every `<project ...>` placeholder with the adopter's real build/test commands. Delete any step that does not apply (e.g. projects without a type checker SHOULD remove the Type check step rather than leaving a no-op).
3. Confirm `python3 validate.py` returns 0 locally before pushing the workflow. The workflow runs `validate.py`; if it fails locally, it will fail in CI.
4. On GitLab, Bitbucket Pipelines, CircleCI, or other CI platforms, translate the step sequence directly — the logical steps are the same; only the YAML syntax changes.

## Why this ships in the framework

`playbooks/automation.md` Principle 3 ("CI mirrors local verification") requires adopters to wire a CI job equivalent to their local verification path. Without a shipped source, every adopter re-derives the same workflow. This CI harness ships a ready-to-fork GitHub Actions template so adopters can wire verification in one step — but until they copy it into the real CI path, it remains shipped but inactive.

## Scope proportionality

`micro` and `small` scope projects (per `00-audit.md` Strategy Decision) MAY skip the Secret scan and Placeholder scan steps if the project's surface is narrow enough that the grep cost exceeds the signal. `standard` and `large` scope projects SHOULD run the full sequence.
