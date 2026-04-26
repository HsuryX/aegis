# Cross-harness capability matrix

This is the shared control ledger for aegis harness claims. Use it with the prioritized harness READMEs when deciding what is actually enforced, what is shipped but inactive, and what is still manual.

## Legend

- **Native support** — the harness or platform can do this.
- **Active now** — active in this repo today with no extra setup beyond using the harness against this checkout: no copying templates, moving files, editing config, or running setup commands.
- **Shipped here but inactive** — templates, examples, or optional integrations present in the repo but not active until the adopter wires them.
- **Bypass / fail-open** — the main way a control can be skipped or weakened.
- **Adopter action** — what a maintainer must do before relying on the control.

`Active now` is strict. A file under `harness/` is **not** active if the real harness only loads it from somewhere else.

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

Every prioritized harness README should answer these five questions without implying parity that does not exist:

1. What protects `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/`?
2. Is the Session Start Protocol automatic, hinted, or fully manual?
3. How does the operator run `python3 validate.py`, and is that automatic or manual?
4. Is Build/Type/Lint/Test/Security verification wired locally, CI-backed, shipped but inactive, or absent?
5. Which control class and activation state apply to each meaningful protection claim?

## Current repo facts

- **Active controls today:** none.
- **Shipped here but inactive today:** Claude Code `harness/claude-code/settings.json`, hook recipes, and skills; Codex `config.toml.example` plus `.codex` command-rule / hook / subagent templates and `.agents/skills` skill templates under `harness/codex/`; GitHub Actions workflow example under `harness/ci/`.
- **Not applied today:** repo-root `.claude/settings.json`, repo-root `.codex/`, repo-root `.github/workflows/*`, OS `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/`, installed git hooks.
- **Shared manual backstop available today:** `python3 validate.py`.

## Harness summary

| Harness | Native support | Active now (no extra setup) | Shipped here but inactive | Control class | Activation state | Biggest bypass / fail-open | Adopter action before relying on it |
|---|---|---|---|---|---|---|---|
| **Claude Code** | `permissions.deny`, hooks, SessionStart/Stop, skills | none | `harness/claude-code/settings.json`; hook recipes; skills | executable + backstop available | shipped but inactive | settings template is inert until installed; Bash subprocess writes can still modify files after install | install or sync settings into Claude Code's loaded path, optionally add OS `chmod`, wire hooks, and install CI |
| **Codex** | `AGENTS.md`, command rules, hooks, skills, subagents, config, sandbox/approval policies | none | `config.toml.example`; `.codex/hooks.json`; `.codex/rules`; `.codex/hooks`; `.codex/agents`; `.agents/skills` templates | advisory + executable/backstop available | shipped but inactive | templates are inert until copied into the real Codex config path and project-local `.codex` surfaces require project trust; hook coverage depends on the events Codex exposes and can fail open if misconfigured | copy selected templates into repo-root or user Codex config, mark the project trusted when using project-local `.codex`, test hooks with known-failing inputs, then add CI / OS / git backstops where needed |
| **CI** | provider workflow engine | none | `github-actions-aegis-verify.yml.example` | backstop | shipped but inactive | no enforcement until a workflow is installed and required by branch policy | copy template to `.github/workflows/` or equivalent, replace placeholders, and enable required checks |

AGENTS.md loading or README prose does **not** count as an active enforcement control in this table. `Active now` means an active control, not merely shipped documentation.

## Control-by-control matrix

| Control | Claude Code | Codex | CI |
|---|---|---|---|
| **Framework-file write protection** | **Shipped but inactive** — `settings.json` contains `permissions.deny` entries for protected patterns, inactive until installed | **Shipped but inactive** — hook template can block writes when installed; OS `chmod` remains the Bash-resistant backstop | N/A |
| **Session-start cue** | Native SessionStart support exists, shipped hook guidance inactive here | Hook/rule templates can remind the agent when installed; inactive here | N/A |
| **Rule / guidance loading** | `AGENTS.md` + `CLAUDE.md`; skills depend on local Claude setup | `AGENTS.md`; optional command rules, skills, and subagents after template install | N/A |
| **`python3 validate.py`** | Available and manual now; can be hooked later | Available and manual now; can be hooked later | Template can run it once CI is installed |
| **Build / Type / Lint / Test / Security verification** | Hook support exists, shipped but inactive here; manual today | Hook support exists, shipped but inactive here; manual today | Shipped but inactive; no live workflow in this repo |
| **OS read-only backstop** | Documented, inactive until adopter applies it | Documented, inactive until adopter applies it | N/A |

## Biggest differences at a glance

- **Claude Code** ships the strongest permission-deny template plus mature hook surfaces, but this checkout does not install them into a live Claude Code settings path.
- **Codex** now has first-class rule, hook, skill, and subagent surfaces; aegis ships templates for them, but they remain inactive until copied into the real Codex load path.
- **CI** is a shipped-but-inactive repo-level backstop until an adopter installs a workflow under `.github/workflows/` or an equivalent CI location.
- **Other agents** receive no special aegis adapter. They may still read `AGENTS.md`, but any tool-specific wiring is local adopter work and is not counted as shipped framework support.
