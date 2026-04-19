# Codex CLI harness

This directory contains Codex-CLI-specific configuration for aegis. Codex reads `AGENTS.md` natively per the AGENTS.md convention, so most of the framework works out of the box. This harness covers the Codex-specific gaps.

## What Codex enforces natively

- **AGENTS.md reading.** Codex CLI follows the AGENTS.md convention and loads `AGENTS.md` at session start. The agent sees the full framework (Session Start Protocol, Phase Gates, Workspace Discipline, etc.) as part of its initial instructions.
- **Project-scoped configuration** via `config.toml` (optional — see `config.toml.example`). Codex supports per-project profile selection, model choice, and approval policies.
- **Approval policies.** Codex can require user approval before running commands or writing files, depending on the configured policy. The framework recommends `on-request` for trusted development and stricter modes for sensitive repositories.
- **Workspace sandboxing.** Codex can restrict file writes to the project directory via sandbox modes.

## What Codex cannot enforce

- **No hook equivalent.** Codex has no PreToolUse/PostToolUse mechanism comparable to Claude Code. The agent is responsible for self-regulating against the rules in `AGENTS.md` and the playbooks.
- **No deny rules for individual files.** Codex does not block file writes based on pattern deny lists. Write protection for `AGENTS.md` and `playbooks/` is agent-self-discipline plus OS-level `chmod`.
- **No skill commands.** Codex does not have the Claude Code `/{name}` skill mechanism. The framework skills (`/verify`, `/decision`, `/gap`, `/audit-surface`, `/phase-status`) are documented as behaviors the agent SHOULD invoke manually, not as tool commands.
- **No SessionStart hook.** The agent MUST self-execute the Session Start Protocol from `AGENTS.md` at the beginning of every session. This is a rule of discipline, not a tool-enforced constraint.
- **No PreCompact hook.** When context compression runs, the agent MUST flush unsaved state to files manually — there is no automatic reminder.

## How to compensate

- **OS-level protection.** `chmod -R a-w AGENTS.md playbooks/` makes framework files read-only at the filesystem level. The agent cannot modify them even via Bash redirects or `sed -i`. When the framework author needs to edit, they temporarily restore write permission.
- **CI gates.** A CI job MUST run the formatter, linter, type checker, test suite, and verification greps (including the canonical `[NEEDS CLARIFICATION:` check from `playbooks/identifiers.md`). Without local hooks, CI is the only mechanical check.
- **Pre-commit hooks via Git.** A Git pre-commit hook (via husky, lefthook, or similar) SHOULD run the same verification that Claude Code's PostToolUse hook runs locally. This is independent of Codex and works regardless of which agent produced the change.
- **Manual Session Start Protocol.** At session start, the agent MUST read `.agent-state/phase.md`, `audit.md`, `decisions.md`, `gaps.md` in order, per the Session Start Protocol in `AGENTS.md`. Codex does not block a session that skips this step — the agent is trusted to follow the protocol.
- **Manual Verification Sequence.** At phase transitions, the agent MUST run Build → Type check → Lint → Test → Security scan → Diff review manually and record output in `phase.md`. The `/verify` skill is not available in Codex; the agent replicates its steps by hand.

## Files in this harness

- `config.toml.example` — example Codex CLI project configuration with commented-out fields. Copy to your Codex config location and uncomment/adjust.
- `README.md` — this file.

## Minimum Codex CLI version

aegis requires a Codex CLI build with AGENTS.md support. Earlier versions without AGENTS.md reading MUST use Claude Code or Cursor instead.

## Setup checklist

New project adoption — run these steps after copying aegis into the target repo. Because Codex has no native hook mechanism, all enforcement is delegated to OS filesystem, git hooks, and CI.

### 1. File permissions

```bash
chmod +x tools/bootstrap.sh validate.py
chmod -R a-w AGENTS.md playbooks/ CLAUDE.md
```

This makes framework files read-only at the OS level — any write attempt fails regardless of which agent tries it. When the framework author needs to edit, temporarily restore write permission (`chmod -R u+w`) and re-lock after the edit ships.

### 2. Git hooks

Use husky, lefthook, or a plain `.git/hooks/` script. Install commit-msg and pre-commit hooks that replicate what Claude Code does natively:

```bash
# .git/hooks/commit-msg (conventional-commits + Implements: trailer)
#!/bin/bash
header=$(head -1 "$1")
if ! [[ "$header" =~ ^(feat|fix|refactor|docs|test|chore|perf|ci)(\([a-z0-9-]+\))?:\ .+$ ]]; then
  echo "commit-msg: header must match conventional-commits regex" >&2
  exit 1
fi
type="${BASH_REMATCH[1]}"
if [ "$type" != "chore" ] && ! grep -qE '^Implements: D-[0-9]+' "$1"; then
  echo "commit-msg: non-chore commit requires 'Implements: D-N' trailer" >&2
  exit 1
fi
```

lefthook example (`lefthook.yml`):

```yaml
commit-msg:
  commands:
    conventional-commits:
      run: .git/hooks/commit-msg {1}
pre-commit:
  commands:
    validator:
      run: python3 validate.py
    formatter:
      run: <project formatter command>
    linter:
      run: <project linter command>
```

### 3. CI gates

Configure a CI job that mirrors the Verification Sequence. A ready-to-use GitHub Actions template ships with aegis at `harness/ci/github-actions-aegis-verify.yml.example` — copy it to `.github/workflows/aegis-verify.yml`, replace the `<project ...>` placeholders with your real commands, and commit. The template includes Build → Type check → Lint → Test → Secret scan → `validate.py` → Placeholder scan with `if: always()` gating so a single PR surfaces all failures at once. See `harness/ci/README.md` for adoption notes per CI platform.

GitLab CI equivalent uses the same step sequence under a `script:` block per job — the logical steps are identical; only the YAML syntax differs.

### 4. Session-start discipline (agent self-check)

At the top of every session the agent MUST manually execute the Session Start Protocol in `AGENTS.md`. Codex cannot enforce this — pin a "read .agent-state/phase.md first" reminder in the project's Codex prompt library or README.

### 5. Codex `config.toml`

Copy `config.toml.example` to the appropriate Codex config location. Verify `AGENTS.md` reading is enabled. Configure approval policy to `on-request` for write operations if using a repo with strict framework-read-only discipline.
