# Cross-harness capability matrix

This is the shared control ledger for aegis harness claims. Use it with the per-harness READMEs when deciding what is actually enforced, what is shipped but inactive, and what is still manual.

## Legend

- **Native support** — the harness or platform can do this.
- **Active now** — active in this repo today with no extra setup beyond using the harness against this checkout: no copying templates, moving files, editing config, or running setup commands.
- **Shipped here but inactive** — templates, examples, or optional integrations present in the repo but not active until the adopter wires them.
- **Bypass / fail-open** — the main way a control can be skipped or weakened.
- **Adopter action** — what a maintainer must do before relying on the control.

`Active now` is strict. A file under `harness/` is **not** active if the real harness only loads it from somewhere else (for example Cursor rules at repo-root `.cursor/rules/`).

## Security-claim model

For security and enforcement claims, aegis uses two explicit axes:

- **Control class**
  - **Executable** — blocks or rejects the unsafe action at the point of execution
  - **Backstop** — detects or fails the problem later (validator, CI, audit hook, review checkpoint)
  - **Advisory** — guidance, prompt shaping, or documentation only
- **Activation state**
  - **Active now** — operating in this repo today with no extra setup
  - **Shipped but inactive** — present in the repo, but not operating until installed or wired
  - **Not available here** — not provided by this harness/repo combination

Rules for reading the matrix:

1. **Advisory** text does **not** count as a mitigation by itself.
2. **Shipped but inactive** and similar labels describe capability, not current protection.
3. CI / validator checks are usually **backstops**, not equivalent to local inline protection.
4. When a harness README or playbook makes a security claim, this file is the canonical owner of the claim's control class and activation state.

## Minimum safety contract

Every harness README should answer these five questions without implying parity that does not exist:

1. What protects `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/`?
2. Is the Session Start Protocol automatic, hinted, or fully manual?
3. How does the operator run `python3 validate.py`, and is that automatic or manual?
4. Is Build/Type/Lint/Test/Security verification wired locally, CI-backed, shipped but inactive, or absent?
5. Which control class and activation state apply to each meaningful protection claim?

## Current repo facts

- **Active controls today:** none.
- **Shipped here but inactive today:** Claude Code `harness/claude-code/settings.json` canonical settings source/template, Claude hook recipes, and repo skills that still depend on local Claude setup; Codex `config.toml.example`; Cursor `.mdc` templates under `harness/cursor/.cursor/rules/`; GitHub Actions workflow example under `harness/ci/`.
- **Not applied today:** repo-root `.claude/settings.json`, repo-root `.cursor/rules/`, repo-root `.github/workflows/*`, OS `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/`, installed git hooks.
- **Shared manual backstop available today:** `python3 validate.py`.

## Harness summary

| Harness | Native support | Active now (no extra setup) | Shipped here but inactive | Control class | Activation state | Biggest bypass / fail-open | Adopter action before relying on it | Status evidence | Status owners | Bypass owner/evidence | Adopter action owner/evidence |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **Claude Code** | `permissions.deny`, hooks, SessionStart/Stop, skills | none | canonical `harness/claude-code/settings.json` source/template; hook recipes in the cookbook; repo skills still depend on local Claude setup | executable + backstop available | shipped but inactive | the settings template is inert until installed into Claude Code's loaded settings path; Bash subprocess writes can still modify files after install | install or sync the template into Claude Code's real loaded settings path, then optionally add OS `chmod`, wire hooks from the cookbook, and install CI | active_now=`harness/capability-matrix.md:47`; shipped=`harness/claude-code/settings.json` | active_now: framework maintainer; shipped: framework maintainer | owner: framework maintainer; evidence: `AGENTS.md` Bash-bypass discipline | owner: adopter/runtime owner; evidence: `harness/claude-code/README.md` setup guidance |
| **Codex** | `AGENTS.md` loading; optional approval policy; optional sandbox | none | `config.toml.example` | advisory by default; executable/backstop only after adopter adds OS/git/CI controls | shipped but inactive for optional hardening; otherwise advisory-only | no per-file deny rules; no hook layer; example config is inactive until copied | choose approval/sandbox settings, apply OS `chmod`, and add git hooks + CI | active_now=`harness/capability-matrix.md:47`; shipped=`harness/codex/config.toml.example` | active_now: framework maintainer; shipped: framework maintainer | owner: framework maintainer; evidence: no shipped hook/deny mechanism | owner: adopter/runtime owner; evidence: `harness/codex/README.md` hardening guidance |
| **Cursor** | advisory repo-root `.cursor/rules/*.mdc` loading | none | `.mdc` rule templates under `harness/cursor/.cursor/rules/` | advisory by default; backstop only after adopter adds CI/git/OS controls | shipped but inactive for templates/backstops; advisory-only after rule copy | rules are inactive until moved to repo-root `.cursor/rules/`; active rules still do not hard-block writes | copy the rules to repo-root `.cursor/rules/`, then add OS `chmod`, git hooks, and CI | active_now=`harness/capability-matrix.md:47`; shipped=`harness/cursor/.cursor/rules/` | active_now: framework maintainer; shipped: framework maintainer | owner: framework maintainer; evidence: Cursor rules are advisory/non-blocking | owner: adopter/runtime owner; evidence: `harness/cursor/README.md` setup guidance |
| **CI** | provider workflow engine (GitHub Actions, GitLab CI, etc.) | none | `github-actions-aegis-verify.yml.example` | backstop | shipped but inactive | no enforcement until a workflow is installed and required by branch policy | copy the template to `.github/workflows/` or equivalent, replace placeholders, and enable required checks | active_now=`harness/capability-matrix.md:47`; shipped=`harness/ci/github-actions-aegis-verify.yml.example` | active_now: framework maintainer; shipped: framework maintainer | owner: framework maintainer; evidence: workflow is example-only until installed | owner: adopter/runtime owner; evidence: `harness/ci/README.md` setup guidance |

AGENTS.md loading or README prose does **not** count as an active enforcement control in this table. `Active now` means an active control, not merely shipped documentation. Likewise, `harness/claude-code/settings.json` is shipped canonical source material, not an active control, until it is installed into Claude Code's real loaded settings path.

## Control-by-control matrix

| Control | Claude Code | Codex | Cursor | CI |
|---|---|---|---|---|
| **Framework-file write protection** | **Shipped but inactive in this checkout** — `harness/claude-code/settings.json` contains `permissions.deny` entries for Edit/Write/NotebookEdit on `AGENTS.md`, `CLAUDE.md`, `playbooks/**`, and `_legacy/**`, but they are inactive until installed into Claude Code's loaded settings path | **Not available here as a native control**; rely on optional OS `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/` and operator discipline | **Not available here as a native control**; rely on optional OS `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/` and operator discipline | N/A |
| **Session-start cue** | Native SessionStart support exists, but is **shipped but inactive here**; session discipline is still manual | **Not available here** | **Not available here**; rules may remind, but they do not enforce | N/A |
| **Rule / guidance loading** | `AGENTS.md` + repo docs; skills ship in-repo, but activation depends on local Claude setup | `AGENTS.md` support only; no skills or hook system | `.mdc` rule system exists, but this repo ships rules under `harness/cursor/.cursor/rules/`; they are **shipped but inactive** until copied to repo-root `.cursor/rules/` | N/A |
| **`python3 validate.py`** | Available and manual now; can be hooked later | Available and manual now | Available and manual now | Template can run it once CI is installed |
| **Build / Type / Lint / Test / Security verification** | Hook support exists, but is **shipped but inactive here**; manual today | Manual today; git hooks / CI optional | Manual today; advisory rules only; git hooks / CI optional | Shipped but inactive; no live workflow in this repo |
| **OS read-only backstop** | Documented for `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/`, but is **not available here as an active control** until the adopter applies it | Documented for `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/`, but is **not available here as an active control** until the adopter applies it | Documented for `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/`, but is **not available here as an active control** until the adopter applies it | N/A |

## Biggest differences at a glance

- **Claude Code** ships the strongest native mechanism plus the canonical settings template, but this checkout does not install it into a live Claude Code settings path.
- **Codex** currently depends on manual discipline plus optional sandbox/approval settings and adopter-installed backstops.
- **Cursor** currently ships advisory rule templates only; they are not active until copied from `harness/cursor/.cursor/rules/` to repo-root `.cursor/rules/`.
- **CI** is shipped but inactive, not a live guarantee, until an adopter installs a workflow under `.github/workflows/` or the equivalent CI location.
