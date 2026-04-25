# Codex CLI harness

This directory contains Codex-CLI-specific guidance for aegis. Read it together with the shared [`../capability-matrix.md`](../capability-matrix.md), which is the authoritative summary of what is active now vs optional or manual.

## What this repo wires now

This repo does **not** currently wire a Codex-side blocking control. What ships today is:

- `AGENTS.md` / playbook guidance that Codex can read
- `config.toml.example` as an optional starter
- documentation for manual, OS-level, git-hook, and CI backstops

Treat Codex in this repo as **manual discipline first**, with optional sandbox / approval / OS / CI hardening added by the adopter.

## What Codex enforces natively

- **AGENTS.md reading.** Codex CLI follows the AGENTS.md convention and loads `AGENTS.md` at session start. The agent sees the thin operator kernel (Session Start Protocol, load map, phase boundaries, workspace discipline) and uses it to pull in the current playbooks.
- **Project-scoped configuration** via `config.toml` (optional — see `config.toml.example`). Codex supports per-project profile selection, model choice, approval policies, and sandbox modes.
- **Approval policies.** Codex can require user approval before running commands or writing files, depending on the configured policy.
- **Workspace sandboxing.** Codex can restrict file writes to the project directory via sandbox modes.

## What Codex cannot enforce

- **No hook equivalent.** Codex has no PreToolUse/PostToolUse mechanism comparable to Claude Code. The agent is responsible for self-regulating against the rules in `AGENTS.md` and the playbooks.
- **No deny rules for individual files.** Codex does not block file writes based on pattern deny lists. Write protection for `AGENTS.md`, `CLAUDE.md`, `playbooks/`, and `_legacy/` is agent-self-discipline plus OS-level `chmod`.
- **No skill commands.** Codex does not have the Claude Code `/{name}` skill mechanism. The framework skills (`/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status`) are documented as behaviors the agent SHOULD invoke manually, not as tool commands.
- **No SessionStart hook.** The agent MUST self-execute the Session Start Protocol from `AGENTS.md` at the beginning of every session. This is a rule of discipline, not a tool-enforced constraint.
- **No PreCompact hook.** When context compression runs, the agent MUST flush unsaved state to files manually — there is no automatic reminder.

## How to compensate

Universal backstops (OS `chmod`, git pre-commit hooks, CI workflow, manual Session Start Protocol, manual `python3 validate.py`) are documented once in [`../capability-matrix.md`](../capability-matrix.md) — see the Controls table and Notes. Apply them to compensate for Codex's missing native enforcement.

## Files in this harness

- `config.toml.example` — example Codex CLI project configuration with commented-out fields. Copy to your Codex config location and uncomment/adjust.
- `README.md` — this file.

## Minimum Codex CLI version

aegis requires a Codex CLI build with AGENTS.md support. Earlier versions without AGENTS.md reading need a different harness.

## Setup checklist

After copying aegis into the target repo:

1. **Universal backstops** — apply OS `chmod`, install git pre-commit hooks (commit-msg conventional-commits regex + `Implements:` trailer; pre-commit `python3 validate.py`), and install the CI workflow template from [`harness/ci/`](../ci/README.md). Same as every harness — see [`../capability-matrix.md`](../capability-matrix.md) for the canonical control table.
2. **Codex-specific: session-start discipline.** Codex has no SessionStart hook. Pin a "read `.agent-state/phase.md` first" reminder in the project's Codex prompt library or README so the agent self-executes the Session Start Protocol from `AGENTS.md`.
3. **Codex-specific: `config.toml`.** Copy `config.toml.example` to the appropriate Codex config location if stricter defaults are wanted. Verify `AGENTS.md` reading is enabled; configure approval policy and sandboxing to match the repo's risk level. These are optional hardening controls, not repo-wired guarantees.
