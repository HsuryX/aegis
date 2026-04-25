# Claude Code hooks cookbook

Claude-Code-specific implementation of aegis's automation rules. For the agent-neutral principles — "automate what rules describe", "hook vs. instruction decision tree", "CI mirrors local verification", "deterministic commands → hooks", "fail-open is a failure mode" — see [`../../playbooks/automation.md`](../../playbooks/automation.md). This cookbook is the concrete realization of those principles in Claude Code's hook, permission, LSP, skill, and task-system mechanisms.

> **Terminology.** This file uses terms defined in [`../../playbooks/glossary.md`](../../playbooks/glossary.md): **gap**, **harness**, **verify**.

## Hook basics

Hooks MUST be configured in the real loaded Claude settings path, using `harness/claude-code/settings.json` as the shipped source. Hooks automate what rules describe — they are the Claude Code realization of the principles in `playbooks/automation.md`.

Claude Code hook commands receive the tool invocation as JSON on stdin. Hook scripts MUST extract fields by parsing stdin — there is no `$FILE_PATH` shell variable. The only Claude-provided environment variable useful here is `$CLAUDE_PROJECT_DIR` (the project root). A hook that fails to parse stdin correctly will silently no-op, so the author MUST verify each hook by echoing a sample payload through it before committing.

**Stdin payload — JSON Schema** (normative; hook authors MUST treat the `required` fields below as always present and guard optional fields with existence checks):

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ClaudeCodeHookStdin",
  "type": "object",
  "required": ["session_id", "cwd", "hook_event_name"],
  "properties": {
    "session_id": {"type": "string", "description": "Stable per-session identifier"},
    "transcript_path": {"type": "string", "description": "Absolute path to the session transcript; may be absent on SessionStart"},
    "cwd": {"type": "string", "description": "Absolute working directory when the hook fires"},
    "permission_mode": {"type": "string", "enum": ["default", "acceptEdits", "plan", "bypassPermissions"]},
    "hook_event_name": {"type": "string", "enum": ["PreToolUse", "PostToolUse", "Stop", "SessionStart", "PreCompact", "UserPromptSubmit", "TaskCreated", "TaskCompleted", "CwdChanged", "WorktreeCreate"]},
    "tool_name": {"type": "string", "description": "Present only on PreToolUse and PostToolUse"},
    "tool_input": {"type": "object", "description": "Tool-specific input — shape varies by tool; see Tool-input shapes below"},
    "tool_response": {"type": "object", "description": "Present only on PostToolUse; the tool's output"},
    "source": {"type": "string", "enum": ["startup", "resume", "clear", "compact"], "description": "Present only on SessionStart"}
  },
  "additionalProperties": true
}
```

**Tool-input shapes** (non-exhaustive; authors MUST validate shape before reading):
- `Write`: `{"file_path": string, "content": string}`
- `Edit`: `{"file_path": string, "old_string": string, "new_string": string, "replace_all": boolean}`
- `Read`: `{"file_path": string, "offset": integer, "limit": integer}`
- `Bash`: `{"command": string, "description": string, "timeout": number, "run_in_background": boolean}`
- `Grep` / `Glob`: file-search parameters (see the Claude Code tool reference)

Hook authors MUST parse stdin defensively: missing keys, unexpected types, and schema evolution across Claude Code versions are all possible. A hook that dereferences `tool_input.file_path` without existence-checking MUST throw on `Bash` invocations where `file_path` does not exist — mask with `tool_input?.file_path` or equivalent before use.

**Exit code semantics — commonly misunderstood:**

- `0` = allow/success (action proceeds)
- `2` = **block** (action is prevented, stderr is surfaced to the user and Claude). This is the ONLY blocking code.
- `1` or any other non-zero = logged error, **non-blocking** (action still proceeds). Buggy hooks that crash with exit 1 silently allow — fail-open behavior.

Matchers in `PreToolUse`/`PostToolUse` are regex strings on the tool name (e.g., `Write|Edit` matches either tool). Several hook events do **not** support matchers at all — `Stop`, `UserPromptSubmit`, `TaskCreated`, `TaskCompleted`, `CwdChanged`, `WorktreeCreate` — setting `matcher` on these events is silently ignored. `SessionStart` matches on session source (`startup`, `resume`, `clear`, `compact`), not tool names.

**Matcher anchoring — semantics and guidance.** Claude Code's matcher regex semantics have varied across versions — substring match, prefix match, and full-string match have each been observed. The SAFE pattern the author SHOULD use is **explicit anchoring with enumeration**: `^(Write|Edit)$` rather than `Write|Edit`. Anchoring prevents two classes of defect: (a) accidental match of future tools that share a prefix (e.g., `Write` unanchored would match a hypothetical `WriteJson`); (b) accidental match of tools whose name contains the matcher as a substring (e.g., `Edit` unanchored matching a hypothetical `NotebookEdit`). Before depending on a specific anchoring behavior, the author MUST empirically verify by creating a test hook whose matcher is the pattern under test and logging `hook_event_name + ":" + tool_name` to a file, then exercising every tool in the table below to confirm the expected hit set.

**Test vectors** (run these against the author's project settings to confirm matcher semantics):

| Matcher | Intended matches | Unintended risk if unanchored |
|---------|------------------|-------------------------------|
| `Write` | `Write` | `WriteJson`, any future tool whose name contains `Write` |
| `^Write$` | `Write` only | (none — anchored) |
| `Write\|Edit` | `Write`, `Edit` | `WriteJson`, `NotebookEdit`, any tool whose name contains either |
| `^(Write\|Edit)$` | `Write`, `Edit` only | (none — anchored + grouped) |
| `.*` | every tool (dangerous) | matches every tool including future ones; use only when the hook is intentionally catch-all |
| `^Bash$` | `Bash` only | (none) |
| `^Bash\|Write$` | **Accidental:** `Bash` at start OR `Write` at end — NOT the likely intent | Common anchoring bug: the author means `^(Bash\|Write)$` but writes `^Bash\|Write$` |

The last row captures a common hook bug: precedence of `|` vs. anchors. The matcher `^Bash|Write$` parses as `(^Bash) | (Write$)` in standard regex, NOT `^(Bash|Write)$`. Authors MUST group explicitly — `^(Bash|Write)$` — to get "exactly Bash or exactly Write". This also survives future tool additions safely.

**Matcher scope.** `PreToolUse` and `PostToolUse` are the only events where `matcher` is evaluated as a regex on `tool_name`. `SessionStart`'s `matcher` is a regex on `source` (one of `startup`, `resume`, `clear`, `compact`) — the same anchoring guidance applies. All other hook events silently ignore `matcher`; authors MUST verify their hook fires by logging invocations if the semantics are unclear.

**Timeouts** are in **seconds**. On timeout, Claude Code kills the hook process with SIGTERM and treats the invocation as non-blocking (**fail-open**) — the tool call proceeds even if the hook was mid-check. Three implications the author MUST account for:

- Hooks that MUST block on misuse SHOULD use a sufficiently short timeout so legitimate invocations complete well under budget.
- Hooks that MUST still block on timeout SHOULD catch SIGTERM and `exit 2` explicitly before Claude Code's kill completes.
- Any hook that relies on fail-closed behavior MUST NOT use a timeout — and MUST then be bounded so it cannot hang indefinitely.

Fail-open is a failure mode — see `playbooks/automation.md` principle 5.

## Recommended hooks

**SessionStart** — initialize session context:

- Verify state files exist (`phase.md`, `audit.md`, `decisions.md`, `gaps.md`); warn if any are missing or in template state without prior phase work
- Display current phase, gate status, open decisions count, and critical gaps count for quick orientation
- Audit that `AGENTS.md` and `playbooks/` have not been modified since the last session (checksum comparison)

**PreCompact** — flush state before context compression:

- Remind the agent to write any unsaved audit entries, decisions, gaps, and session log updates to their state files before `/compact` runs — a lossy compact can otherwise lose details that were only in conversation context
- Snapshot state file checksums for post-compact verification

**PostToolUse (Write|Edit)** — enforce code quality automatically:

- Run the project formatter on changed files (`standards.md`: Code Quality)
- Run the project linter on changed files (`standards.md`: Code Quality)
- Run the type checker if applicable (`standards.md`: Type safety)

**PreToolUse (Write|Edit)** — prevent violations before they happen:

- Block modifications to `_legacy/` directory (`AGENTS.md`: Workspace Discipline)
- Block modifications to `AGENTS.md`, `CLAUDE.md` (symlink), and `playbooks/` (`AGENTS.md`: Workspace Discipline — framework files are read-only for the agent). Both `AGENTS.md` and `CLAUDE.md` MUST be matched because symlink resolution is not guaranteed across Claude Code versions.
- Block writes of 800 lines or more (`standards.md`: Small files requires <800 lines; Write only — count lines in tool input content, exit 2 to block)
- Block modifications to linter/formatter config files (e.g., `.eslintrc`, `biome.json`, `.prettierrc`) — force the agent to fix code rather than weaken quality tooling
- Block implementation source file writes when no corresponding test file exists in the project (TDD enforcement; optional — enable when TDD is the decided test strategy)

**PostToolUse (Bash)** — detect circumvention of file protections (PreToolUse Write/Edit hooks do not catch writes performed via Bash redirects, `sed -i`, or `rm`):

- After any Bash command, check that protected files (`AGENTS.md`, `CLAUDE.md`, `playbooks/`, `_legacy/`) were not modified. For git-tracked projects: `git diff --quiet HEAD -- AGENTS.md CLAUDE.md playbooks/ _legacy/ 2>/dev/null || echo "WARN: protected files modified" >&2`. For non-git projects: store baseline checksums at session start and compare after each Bash call.
- Additional defense: set framework files read-only at the filesystem level (`chmod -R a-w AGENTS.md playbooks/`) — this prevents Bash-based circumvention at the OS layer, and any write attempt (including `sed -i`) fails immediately. When the framework author needs to edit, they temporarily restore write permission.

**Stop** — final verification before session ends:

- Run the project build to catch regressions (`03-implement.md`: Verification Sequence)
- Remind to update state files if phase is active
- Optional: if formatter and linter are not already configured as PostToolUse hooks, the agent MAY batch them at Stop on files edited during the session (the author MUST choose one location — MUST NOT run both per-edit and at session end)
- For spec-only projects (Phase 2 terminal), omit the Stop build hook or set `<build-command>` to `/bin/true`
- **Evidence-cell verifiability check**: if the session is closing a phase gate and the session log contains a Verification Coverage Matrix, verify every `Evidence` cell uses one of the canonical forms: `file.md:N`, `file.md#anchor`, `sha256:{64 hex}`, `#session-YYYY-MM-DD-slug`, `<subagent:NAME>`, or `(pending)` only when the row's `Result` is `pending`. Empty or prose-only Evidence cells MUST produce exit 2 and block session end — see `principles-gates.md` Verification Coverage Matrix → Evidence verifiability.

**Commit-msg (git hook)** — commit message format enforcement (`03-implement.md` Traceability → Commit message format enforcement):

- Validate header regex: `^(feat|fix|refactor|docs|test|chore|perf|ci)(\([a-z0-9-]+\))?: .+$`
- Require `Implements: D-\d+` trailer unless commit type is `chore` OR project scope is `micro` (scope readable from `.agent-state/phase.md`)
- Optionally lint a path-qualified `Covers: specs/<spec>.md:SC-\d+` or `Covers: specs/<spec>.md:FR-\d+` trailer when present as change-summary metadata, but MUST NOT treat commit-msg validation as sufficient per-test traceability; per-test enforcement still belongs in the test files via slugged suffixes or in-file `Covers:` comments
- Installation: under `.git/hooks/commit-msg` or managed by husky/lefthook; for Claude Code users, a Stop hook MAY replicate this on the most recent commit when git hooks are not installed

**SessionStart (kitchen-sink-session detector)** — advisory warning (`AGENTS.md` Session Start Protocol step 8):

- Parse the user's opening prompt via the prompt hook JSON stdin
- Regex for distinct-concern markers: `/\b(and then|also|plus|additionally|furthermore)\b/gi` and count
- If ≥ 3 distinct concerns OR the prompt references ≥ 2 phase transitions, emit stderr advisory: "Scope guard: prompt contains multiple concerns. Consider session sequencing per AGENTS.md step 8." This is non-blocking (exit 0) — the agent then decides whether to propose sequencing to the user

**PreToolUse (Write|Edit) — Naming-table alias enforcement** (`03-implement.md` Post-Change Verification naming check + `standards.md` Naming):

- At hook startup, parse `.agent-state/decisions.md` and extract the Forbidden Aliases column from the Naming Table
- On each Write/Edit call, grep the tool input content against the extracted alias list
- On any match: emit the specific alias + canonical replacement to stderr and exit 2 (block the write)
- The hook MUST re-read `decisions.md` on each invocation — the Naming Table is mutable during Phase 1; caching would produce false negatives
- No-op when `decisions.md` has no Naming Table (Phase 0 projects, or spec-only projects where naming is decided elsewhere)

## Permissions (native write protection)

Claude Code's `permissions.deny` field in `harness/claude-code/settings.json` provides native write blocking for Edit/Write/NotebookEdit tools — more reliable than PreToolUse hooks because it is enforced by Claude Code itself, not by user code. Projects MUST use this as the **primary** defense for framework files; PreToolUse hooks serve as belt-and-suspenders. Note: `permissions.deny` does NOT block Bash subprocess writes, so the PostToolUse Bash circumvention check and filesystem `chmod` defense remain necessary for complete coverage.

Path syntax for Read/Edit permission rules: `./path` or `/path` = project-relative; `//path` = filesystem absolute; `~/path` = home directory. Glob patterns (`**` for recursive, `*` for single segment) are supported. This differs from sandbox filesystem paths where `/` is filesystem-absolute — permission rules use `/` as a project-relative shortcut. The canonical form in Anthropic's docs uses `./` for clarity; both work but `./` is preferred.

**Important:** Projects MUST set `permissions.disableBypassPermissionsMode` to `"disable"` to prevent users from bypassing the deny rules via `--dangerously-skip-permissions` or `--permission-mode bypassPermissions`. Without this, the entire native protection can be trivially disabled. Note: this field lives **inside** the `permissions` object, not at the top level.

## Settings template

The project ships with `harness/claude-code/settings.json` pre-configured with the `permissions` block below. During Phase 1 (when the toolchain is decided), expand it with the `hooks` section — replace `<formatter>`, `<linter>`, and `<build-command>` with project-specific commands.

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "includeGitInstructions": false,
  "permissions": {
    "deny": [
      "Edit(./AGENTS.md)",
      "Edit(./CLAUDE.md)",
      "Write(./AGENTS.md)",
      "Write(./CLAUDE.md)",
      "NotebookEdit(./AGENTS.md)",
      "NotebookEdit(./CLAUDE.md)",
      "Edit(./playbooks/**)",
      "Write(./playbooks/**)",
      "NotebookEdit(./playbooks/**)",
      "Edit(./CHANGELOG.md)",
      "Write(./CHANGELOG.md)",
      "Edit(./harness/claude-code/settings.json)",
      "Write(./harness/claude-code/settings.json)",
      "Edit(./_legacy/**)",
      "Write(./_legacy/**)",
      "NotebookEdit(./_legacy/**)",
      "Edit(./.eslintrc*)",
      "Edit(./biome.json)",
      "Edit(./.prettierrc*)",
      "Write(./.eslintrc*)",
      "Write(./biome.json)",
      "Write(./.prettierrc*)"
    ],
    "disableBypassPermissionsMode": "disable"
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const p=JSON.parse(d||'{}').tool_input?.file_path;if(typeof p==='string'&&p)require('child_process').spawnSync('<formatter>',[p],{stdio:'inherit'})}catch{}})\"",
            "timeout": 10
          },
          {
            "type": "command",
            "command": "node -e \"let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{try{const p=JSON.parse(d||'{}').tool_input?.file_path;if(typeof p==='string'&&p)require('child_process').spawnSync('<linter>',['--fix',p],{stdio:'inherit'})}catch{}})\"",
            "timeout": 10
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{let i;try{i=JSON.parse(d||'{}')}catch{return};const p=require('path').normalize(String(i.tool_input?.file_path??'').split(String.fromCharCode(92)).join('/'));if(p.includes('/_legacy/')||p.startsWith('_legacy/')){console.error('BLOCKED: writes to _legacy/ are forbidden');process.exit(2)}if(p==='AGENTS.md'||p==='CLAUDE.md'||p.includes('/playbooks/')||p.startsWith('playbooks/')){console.error('BLOCKED: framework files are read-only');process.exit(2)}})\"",
            "timeout": 5
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "node -e \"let d='';process.stdin.on('data',c=>d+=c);process.stdin.on('end',()=>{let i;try{i=JSON.parse(d||'{}')}catch{return};const c=typeof i.tool_input?.content==='string'?i.tool_input.content:'';const l=c===''?0:c.split('\\n').length-(c.endsWith('\\n')?1:0);if(l>=800){console.error('BLOCKED: '+l+' lines meets or exceeds 800-line limit');process.exit(2)}})\"",
            "timeout": 5
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "<build-command>",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

Replace `<formatter>`, `<linter>`, and `<build-command>` with project-specific commands during setup. Protection scripts use Node.js for portability; rewrite in the project's runtime if Node.js is not available. For complex hook logic (like the path protection above), consider extracting to a standalone script file (e.g., `harness/claude-code/hooks/protect-files.js`) for readability and testability.

**Line count correctness (800-line guard):** the line-count expression `c===''?0:c.split('\n').length-(c.endsWith('\n')?1:0)` handles the edge cases that a naive `c.split('\n').length` gets wrong. Reference test vectors for the formula:

| Content `c` | Expected lines | Formula result |
|---|---|---|
| `""` (empty) | 0 | 0 (via empty guard — without the guard, `"".split('\n')` returns `['']` which has length 1, producing an incorrect off-by-one) |
| `"a"` | 1 | 1 (split=`['a']`, length 1, no trailing newline, 1 − 0 = 1) |
| `"a\n"` | 1 | 1 (split=`['a','']`, length 2, trailing newline, 2 − 1 = 1) |
| `"a\nb"` | 2 | 2 (split=`['a','b']`, length 2, no trailing newline, 2 − 0 = 2) |
| `"a\nb\n"` | 2 | 2 (split=`['a','b','']`, length 3, trailing newline, 3 − 1 = 2) |

Projects rewriting this in another runtime MUST port the test vectors and MUST verify empty-string handling matches the table before shipping the hook.

## Hook troubleshooting

If a hook malfunctions (blocks legitimate work, crashes repeatedly, or produces false positives):

1. The agent MUST report the specific hook, its error output, and the blocked action to the user
2. The user MAY temporarily disable the hook in `harness/claude-code/settings.json` — the agent MUST record the override in `gaps.md` with severity and reason
3. The agent MUST fix the hook logic, re-test with the failing case, and restore it
4. The agent MUST NOT work around a broken hook by restructuring code to avoid triggering it — the agent MUST fix the hook

**CI/CD pipeline** SHOULD mirror the Verification Sequence from `03-implement.md` (Build → Type check → Lint → Test → Security scan; excluding Diff review, which requires manual judgment). The same checks that run locally via hooks and the `/verify` skill SHOULD run in CI — a single source of truth for quality gates per `playbooks/automation.md` principle 3.

## LSP

Projects SHOULD enable language server plugins in `harness/claude-code/settings.json` for the project's languages:

```json
{
  "enabledPlugins": {
    "<language>-lsp@claude-plugins-official": true
  }
}
```

### When to use LSP

- **Phase 0 (Audit)**: the agent SHOULD run diagnostics on existing code to quantify technical debt and type safety issues
- **Phase 1 (Design)**: the agent SHOULD use find-references to understand existing coupling before redesigning boundaries
- **Phase 3 (Implement)**: the agent MUST use type checking as part of the Verification Sequence; SHOULD use go-to-definition to verify naming consistency; MUST use find-references before any rename

## MCP servers

Projects SHOULD configure MCP in `.mcp.json` at project root. MCP connects external knowledge and services. The agent MUST review MCP server source and permissions before enabling — MCP servers execute code and may have network access. For the agent-neutral principle and recommended integration categories, see `playbooks/automation.md` § External knowledge and services.

### Example configuration

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp@latest"]
    }
  }
}
```

## Skills

Create project-scoped skills in `harness/claude-code/skills/` to automate repetitive framework workflows. Five baseline skills ship with aegis: `verify`, `decision`, `gap`, `audit-surface`, `phase-status`. Each lives in its own subdirectory with a `SKILL.md` file.

### Recommended project skills

| Skill | Purpose | Framework rule it enforces |
|-------|---------|-------------------------------|
| `/verify` | Run the full verification sequence (build → type → lint → test → security → diff) and record output | 03-implement.md: Verification Sequence |
| `/decision` | Create a new decision entry with correct template, auto-increment ID | 01-design.md: Decision Entry Format |
| `/gap` | Create a new gap entry with correct template, auto-increment ID | gaps.md: Entry Template |
| `/audit-surface` | Create a new audit surface entry with correct template | 00-audit.md: Per-Surface Entry Format |
| `/phase-status` | Display current phase, gate status, open decisions, and critical gaps | AGENTS.md: Session Start Protocol |

### Skill authoring constraints

When creating skills, the author MUST follow the official Claude Code skill format:

- **SKILL.md body**: MUST be under 500 lines; the author MUST split into referenced files if larger
- **Name**: MUST be max 64 characters, lowercase letters, numbers, and hyphens only
- **Description**: MUST be max 1024 characters, third person. The description MUST include ONLY triggering conditions ("Use when all implementation is complete and ready for verification"); it MUST NOT include workflow summaries ("Runs build, then lint, then test..."). Claude follows description summaries instead of reading the skill body — workflow details in descriptions cause skills to execute incorrectly
- **Progressive disclosure**: file references SHOULD be kept one level deep from SKILL.md; the author SHOULD avoid deeply nested references
- **Conciseness**: the author SHOULD only add context Claude does not already have; the author SHOULD challenge each paragraph's token cost
- **Freedom levels**: the author SHOULD use high freedom (text guidance) for judgment tasks and low freedom (exact scripts) for fragile operations

## Task system

The agent SHOULD use Claude Code's built-in task system to track phase progress:

- **TaskCreate** for each major work unit within a phase (e.g., each audit surface, each design decision, each specification)
- **TaskUpdate** to mark progress as work completes
- Task status values: `todo` → `in_progress` → `completed` (or `blocked`)
- The agent SHOULD use task dependencies to enforce ordering (e.g., audit surface "Architecture" MUST complete before "Runtime")

Tasks are ephemeral session tools — they complement but MUST NOT replace the persistent state files in `.agent-state/`. See `playbooks/automation.md` § Task tracking for the agent-neutral principle.
