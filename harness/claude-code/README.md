# Claude Code harness

This directory contains all Claude-Code-specific configuration for aegis: the `settings.json` permissions and hooks, plus project skills under `skills/`. The rest of the framework (`AGENTS.md`, `playbooks/`, `.agent-state/`) is agent-neutral and works with any agent that reads `AGENTS.md`.

## What Claude Code enforces natively

Claude Code is the most tightly integrated harness. It supports:

- **Deny rules** (`permissions.deny` in `settings.json`) — blocks Edit, Write, and NotebookEdit against protected patterns before the tool runs. The framework denies all three tool types for `AGENTS.md`, `CLAUDE.md` (symlink), `playbooks/**`, and `_legacy/**`; denies Edit and Write for `CHANGELOG.md`, `harness/claude-code/settings.json` (self-deny to prevent permission-grant), and linter/formatter config files. Both `AGENTS.md` and `CLAUDE.md` MUST be denied because symlink resolution is not guaranteed across versions.
- **PreToolUse hooks** — run before Write/Edit/Bash and can block (exit code 2) on violations. The framework uses PreToolUse to enforce framework-file read-only protection (`AGENTS.md`, `playbooks/`, `_legacy/` — defense-in-depth beyond deny rules), file-size limits (800-line maximum), linter/formatter config immutability, and optional TDD enforcement when the test strategy decision (D-10) selects it.
- **PostToolUse hooks** — run after Write/Edit/Bash and can auto-format, lint, type-check, or verify integrity. The framework uses PostToolUse to run the project formatter, linter, and type checker on changed files, and to detect protected-file modifications via Bash that the PreToolUse hook did not catch.
- **PreCompact hook** — runs before `/compact` and reminds the agent to flush unsaved state to files. The framework uses it to prevent lossy compaction from losing audit entries, decisions, or gap entries.
- **Stop hook** — runs at session end. The framework uses it to run the project build, remind the agent to update state files, and run batched verification.
- **SessionStart hook** — runs at session start. The framework uses it to verify state files exist and display current phase + gate status.
- **Skills** (`skills/`) — project-scoped commands invoked via `/{name}` in a Claude Code session. The framework ships five skills: `/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status`.

## What Claude Code cannot enforce

- **Symlink transparency is version-dependent.** Some Claude Code versions resolve symlinks before applying deny rules, others do not. The framework's mitigation is to deny BOTH the symlink name (`CLAUDE.md`) AND the target name (`AGENTS.md`) explicitly in `settings.json` and the PreToolUse hook script.
- **Bash hook timeouts fail open.** If a PreToolUse hook exceeds its timeout (default 60 seconds), Claude Code kills the process and treats the call as non-blocking. The framework MUST set realistic timeouts (under 5 seconds for cheap checks) and MUST avoid long-running hook scripts.
- **Cross-session state integrity is not tool-enforced.** No hook runs between sessions. The Session Start Protocol in `AGENTS.md` is the framework's own convention for verifying state consistency — Claude Code does not block a session with inconsistent state.
- **Transitive Bash circumvention.** PreToolUse hooks see the Write/Edit tool call but not the content of shell commands. A `sed -i` or shell redirect can bypass Write deny rules. The framework uses a PostToolUse Bash hook that compares file checksums to detect this after the fact, plus filesystem-level `chmod -R a-w` as defense in depth.

## How to compensate

- **Manual `/verify` at phase boundaries.** Before advancing a phase, invoke the `/verify` skill to run the full Verification Sequence and record output. This is the last line of defense if hooks fail open.
- **OS-level read-only protection.** `chmod -R a-w AGENTS.md playbooks/` makes the framework files read-only at the filesystem level, preventing even Bash circumvention. When the framework author needs to edit, they temporarily restore write permission.
- **CI gates mirror local hooks.** A CI job SHOULD run the same formatter, linter, type checker, and test suite that the PostToolUse hook runs locally, so protection is enforced even when the agent runs on an unconfigured workstation.
- **Fresh-context adversarial review at phase boundaries.** The hooks cannot verify design correctness — a separate-agent review from `playbooks/01-design.md`, `02-spec.md`, and `03-implement.md` is the framework's own compensation for this limitation.

## Files in this harness

- `settings.json` — permissions (deny rules) and hook wiring; the canonical location.
- `skills/` — five Claude Code skills (`/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status`). Each has its own `SKILL.md`.
- `hooks-cookbook.md` — Claude-Code-specific hook examples, permission syntax, LSP configuration, MCP examples, skill authoring constraints, and task system guidance.

## Minimum Claude Code version

aegis requires Claude Code 2.x or later. Earlier versions lack PreCompact and SessionStart hooks.

## Setup checklist

New project adoption — run these steps after copying aegis into the target repo. Claude Code has the fullest native enforcement of the three harnesses; most of this is verification rather than new configuration.

### 1. File permissions

```bash
chmod +x tools/bootstrap.sh validate.py
chmod -R a-w AGENTS.md playbooks/ CLAUDE.md
```

OS-level read-only is belt-and-suspenders on top of `settings.json` `permissions.deny`. Both layers are recommended because `permissions.deny` does not block Bash subprocess writes.

### 2. Verify `settings.json` deny list

After `tools/bootstrap.sh`, confirm `harness/claude-code/settings.json` includes deny rules for at least: `AGENTS.md`, `CLAUDE.md`, `playbooks/**`, `harness/claude-code/settings.json` itself. See `hooks-cookbook.md` § Settings template for the canonical contents.

### 3. Verify hooks

Confirm the recommended hook set is wired in `settings.json`:

- SessionStart — context initialization + scope-guard warning
- PreCompact — state flush reminder
- PostToolUse (Write|Edit) — formatter + linter + type check
- PreToolUse (Write|Edit) — file-size + naming-alias + framework-file deny
- PostToolUse (Bash) — protected-file circumvention detector
- Stop — build + Evidence-cell verifiability + state-update reminder
- commit-msg — conventional-commits + `Implements:` trailer enforcement

See `hooks-cookbook.md` for full recipes.

### 4. Skill installation

Confirm skills are loadable via `/{name}`:

```bash
ls harness/claude-code/skills/
# Expected: audit-surface, decision, gap, phase-status, verify
```

Each skill has a `SKILL.md` defining when Claude invokes it. Skills are auto-discovered from the configured skills directory; confirm Claude Code's skill path points to `harness/claude-code/skills/`.

### 5. CI gates

Even with native Claude Code protection, CI MUST replicate the same checks so protection holds when other agents or manual edits produce PRs. Use the GitHub Actions skeleton in `harness/codex/README.md` § CI gates as a starting point (identical step list).

### 6. Session-start discipline

SessionStart hooks automate context initialization, but the agent still MUST execute the Session Start Protocol manually — hooks cannot replace the read-and-verify discipline. The hook reminds; the agent does.
