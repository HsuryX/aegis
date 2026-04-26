# Codex CLI harness

This directory contains Codex-specific templates for aegis. Read it together
with [`../capability-matrix.md`](../capability-matrix.md), which is the
authoritative active-vs-shipped capability table.

## What this repo wires now

Nothing under `harness/codex/` is active from file presence alone. The shipped
state is **shipped but inactive**:

- `config.toml.example` — optional starter configuration.
- `.codex/hooks.json` — example hook wiring.
- `.codex/rules/aegis.rules` — optional Codex command-approval starter.
- `.codex/hooks/` — hook script templates for session-start reminders,
  protected-file checks, and stop-time validation.
- `.agents/skills/` — Codex repository skill templates mirroring the baseline aegis
  workflows.
- `.codex/agents/` — a read-only adversarial-reviewer subagent template.

An adopter must copy or sync these templates into the real Codex-loaded
configuration locations and verify they fire before counting them as controls.

## What Codex can support

- **AGENTS.md reading.** Codex reads `AGENTS.md`; aegis uses it as the thin
  operator kernel and load map.
- **Rules.** Codex command-approval rules can `allow`, `prompt`, or mark
  command prefixes as `forbidden`. They are command policy, not a replacement
  for aegis prose rules.
- **Hooks.** Codex hooks can run executable checks around events such as session
  start, tool use, and stop/completion when installed in the active config.
- **Skills.** Codex skills can package repeatable workflows with `SKILL.md`
  instructions.
- **Custom subagents.** Codex agent TOML files can provide bounded read-only
  reviewers or other specialist roles.
- **Configuration, sandboxing, and approval policy.** Codex project/user config
  can set model, approval, and sandbox defaults.

## What remains outside native Codex guarantees

- **Inactive templates are not enforcement.** Files in this directory are
  evidence of shipped support, not active controls.
- **Per-file write denial is best-effort unless hooks are installed and tested.**
  The shipped pre-tool hook template blocks obvious direct edit/write paths but
  does not replace OS permissions, git hooks, or CI.
- **Shell subprocess writes remain a gap.** A hook can inspect the requested
  tool call, but shell-resistant protection still needs OS-level or CI backstops.
- **Project build/test commands are project-owned.** The stop hook runs
  `python3 validate.py`; downstream project build, lint, test, and security
  commands must come from project decisions/specs.

## Files in this harness

- `config.toml.example` — optional Codex config starting point.
- `.codex/hooks.json` — example hook wiring for the scripts below.
- `.codex/rules/aegis.rules` — optional command-approval starter.
- `.codex/hooks/aegis_session_start.py` — non-mutating Session Start Protocol
  reminder.
- `.codex/hooks/aegis_pre_tool_use.py` — best-effort protected-file edit guard.
- `.codex/hooks/aegis_stop_validate.py` — stop-time `python3 validate.py`
  runner that returns Codex's blocking status on validation failure.
- `.agents/skills/*/SKILL.md` — workflow templates: `phase-status`, `verify`,
  `decision`, `gap`, and `audit-surface`.
- `.codex/agents/aegis-adversarial-reviewer.toml` — read-only semantic reviewer
  for framework amendments and gate claims.

## Setup checklist

After copying aegis into the target repo:

1. Copy `harness/codex/.codex/` and `harness/codex/.agents/` into the active
   Codex project configuration locations for that repo; keep one canonical local
   copy of each template family to avoid drift.
2. Mark the project as trusted in Codex config before relying on project-local
   `.codex` hooks or rules.
3. Ensure hook scripts are executable (`chmod +x .codex/hooks/*.py`).
4. Enable Codex hooks in your config, adapt `.codex/hooks.json` if needed, and
   run one known-failing protected-file write to prove the pre-tool guard fires;
   if relying on Stop, also run a known-failing validation fixture to prove it
   blocks completion.
   For authorized framework maintenance, start Codex with
   `AEGIS_FRAMEWORK_MAINTENANCE=1`; the hook does not trust words inside a
   pending patch as authorization.
5. Copy or adapt `config.toml.example` if stricter approval/sandbox defaults are
   needed.
6. Install universal backstops from [`../capability-matrix.md`](../capability-matrix.md):
   OS permissions where appropriate, git hooks, CI, and manual `validate.py`
   verification.

## Minimum Codex capability

aegis requires a Codex build that supports `AGENTS.md`. The optional templates
in this harness assume Codex support for rules, hooks, skills, and custom
subagents; if a local Codex build lacks one of those surfaces, treat the
corresponding template as documentation only and rely on the universal
backstops.
