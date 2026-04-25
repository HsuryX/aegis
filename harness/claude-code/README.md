# Claude Code harness

This directory contains Claude-Code-specific configuration for aegis. Read this file together with the shared [`../capability-matrix.md`](../capability-matrix.md), which is the authoritative summary of what is active now vs merely supported by the harness.

## What this repo ships

This repo ships the canonical Claude Code settings source at `harness/claude-code/settings.json`.

- **`permissions.deny` in the shipped `settings.json`** — source/template for blocking Edit, Write, and NotebookEdit against protected patterns before the tool runs once the file is installed into Claude Code's real loaded settings path. The current deny list covers `AGENTS.md`, `CLAUDE.md` (symlink), `playbooks/**`, `_legacy/**`, `CHANGELOG.md`, `harness/claude-code/settings.json`, and common linter / formatter config files.

Until that install/sync step happens, the file under `harness/claude-code/` is shipped canonical source material, not an active repo-wired control. The rest of the Claude features below are native capabilities or shipped content, but they are not all wired as active guarantees here.

## What Claude Code can support natively

Claude Code is the most capable aegis harness from an enforcement perspective. It supports:

- **Deny rules** (`permissions.deny` in `settings.json`) — supported natively; this repo ships the canonical template/source, but it is not active here until installed into Claude Code's loaded settings path.
- **PreToolUse hooks** — can block on violations before Write/Edit/Bash.
- **PostToolUse hooks** — can auto-format, lint, type-check, or verify after a tool runs.
- **PreCompact hook** — can remind the agent to flush state before context compression.
- **Stop hook** — can run end-of-session verification.
- **SessionStart hook** — can initialize context at session start.
- **Skills** (`skills/`) — project-scoped commands such as `/verify`, `/decision`, `/gap`, `/audit-surface`, and `/phase-status`, subject to Claude Code's local skill-path configuration.

## What is not wired here yet

- **Hooks are not currently configured in the shipped `harness/claude-code/settings.json` template/source.** The cookbook documents them, but this repo does not presently claim them as active protection.
- **OS-level read-only is documented but not applied by the repo.** If a maintainer wants Bash-resistant protection, they must run `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/` themselves.
- **CI parity is not active in this repo.** aegis ships CI templates under `harness/ci/`, but there is no live workflow under repo-root `.github/workflows/`.

## What Claude Code cannot enforce

- **Symlink transparency is version-dependent.** Some Claude Code versions resolve symlinks before applying deny rules, others do not. The framework's mitigation is to deny BOTH the symlink name (`CLAUDE.md`) AND the target name (`AGENTS.md`) explicitly in the installed settings file and the PreToolUse hook script.
- **Bash hook timeouts fail open.** If a PreToolUse hook exceeds its timeout (default 60 seconds), Claude Code kills the process and treats the call as non-blocking. The framework MUST set realistic timeouts (under 5 seconds for cheap checks) and MUST avoid long-running hook scripts.
- **Cross-session state integrity is not tool-enforced.** No hook runs between sessions. The Session Start Protocol in `AGENTS.md` is the framework's own convention for verifying state consistency — Claude Code does not block a session with inconsistent state.
- **Transitive Bash circumvention.** `permissions.deny` protects tool writes, not arbitrary shell writes. A `sed -i` or shell redirect can still modify files unless the maintainer adds OS-level read-only protection and/or a Bash-review hook.

## How to compensate

- **Manual `python3 validate.py` at phase boundaries.** This repo ships the validator now; use it even if no hooks are wired.
- **Optional `/verify` skill.** If Claude is configured to load the repo's skills, `/verify` is a convenient wrapper. If not, run the Verification Sequence manually.
- **OS-level read-only protection.** `chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/` adds a filesystem backstop against Bash circumvention. When the framework author needs to edit, they temporarily restore write permission.
- **CI gates.** Install a workflow from `harness/ci/README.md` if you want a repo-level backstop for formatter/linter/type-check/test/validator runs.
- **Fresh-context adversarial review at phase boundaries.** The hooks cannot verify design correctness — a separate-agent review from `playbooks/01-design.md`, `02-spec.md`, and `03-implement.md` is the framework's own compensation for this limitation.

## Files in this harness

- `settings.json` — canonical shipped source/template for permissions (deny rules) and any future hook wiring; install or sync it into Claude Code's loaded settings path to make it active.
- `skills/` — five Claude Code skills (`/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status`). Each has its own `SKILL.md`.
- `hooks-cookbook.md` — Claude-Code-specific hook examples, permission syntax, LSP configuration, MCP examples, skill authoring constraints, and task system guidance.

## Minimum Claude Code version

aegis requires Claude Code 2.x or later. Earlier versions lack the full hook surface described above.

## Setup checklist

New project adoption — run these steps after copying aegis into the target repo. Claude Code has the strongest native support, but this repo only ships the canonical `permissions.deny` template by default.

### 1. File permissions

```bash
chmod +x tools/bootstrap.sh validate.py
chmod -R a-w AGENTS.md playbooks/ CLAUDE.md _legacy/
```

OS-level read-only is optional belt-and-suspenders on top of an installed `permissions.deny` configuration. Both layers are recommended because `permissions.deny` does not block Bash subprocess writes.

### 2. Install and verify the deny list

After `tools/bootstrap.sh`, install or sync `harness/claude-code/settings.json` into the real Claude Code loaded settings path you use (for example repo-root `.claude/settings.json`, if that is your chosen location), then confirm the active file includes deny rules for at least: `AGENTS.md`, `CLAUDE.md`, `playbooks/**`, `_legacy/**`, and `harness/claude-code/settings.json` itself. See `hooks-cookbook.md` § Settings template for the canonical contents.

### 3. Optionally wire hooks

If you want more than the default deny-list protection, wire the recommended hook set from `hooks-cookbook.md` into the active Claude Code settings file, using `harness/claude-code/settings.json` as the canonical source:

- SessionStart — context initialization + scope-guard warning
- PreCompact — state flush reminder
- PostToolUse (Write|Edit) — formatter + linter + type check
- PreToolUse (Write|Edit) — file-size + naming-alias + framework-file deny
- PostToolUse (Bash) — protected-file circumvention detector
- Stop — build + Evidence-cell verifiability + state-update reminder
- commit-msg — conventional-commits + `Implements:` trailer enforcement

If you skip this step, the matrix stays truthful: Claude still has native hook support, but your repo is using only the deny rules you installed, not hooks.

### 4. Skill installation

Confirm skills are loadable via `/{name}` if you want the convenience layer:

```bash
ls harness/claude-code/skills/
# Expected: audit-surface, decision, gap, phase-status, verify
```

Each skill has a `SKILL.md` defining when Claude invokes it. Availability depends on Claude Code's configured skill path.

### 5. CI gates

Even with native Claude Code protection, CI is still the best repo-level backstop for PRs from other agents or manual edits. Use `harness/ci/README.md` and the template under `harness/ci/` as the starting point.

### 6. Session-start discipline

SessionStart hooks can remind, but the agent still MUST execute the Session Start Protocol manually — hooks cannot replace the read-and-verify discipline. The hook reminds; the agent does.
