#!/usr/bin/env bash
# aegis bootstrap — initialize a new project using the aegis governance framework.
# Copies framework files into the target directory, resets .agent-state/ to
# template-only, prompts for scope classification + lifecycle mode, writes initial phase.md,
# and smoke-tests with validate.py.
#
# Usage:
#   tools/bootstrap.sh <target-dir> [--scope micro|small|standard|large]
#                                   [--lifecycle-mode finite-delivery|steady-state]
#                                   [--type application|library|cli|spec-only|other]
#                                   [--terminal-phase 0-audit|1-design|2-spec|3-implement]
#                                   [--name <project-name>]
#
# When a flag is omitted the script prompts interactively.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  sed -n '2,14p' "$0"
  exit 0
}

if [[ "${1-}" == "-h" || "${1-}" == "--help" ]]; then
  usage
fi

if [[ $# -lt 1 ]]; then
  echo "error: missing target directory" >&2
  echo "run 'tools/bootstrap.sh --help' for usage" >&2
  exit 1
fi

TARGET="$1"
shift

SCOPE=""
LIFECYCLE_MODE=""
PROJECT_TYPE=""
TERMINAL_PHASE=""
PROJECT_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scope) SCOPE="$2"; shift 2 ;;
    --lifecycle-mode) LIFECYCLE_MODE="$2"; shift 2 ;;
    --type) PROJECT_TYPE="$2"; shift 2 ;;
    --terminal-phase) TERMINAL_PHASE="$2"; shift 2 ;;
    --name) PROJECT_NAME="$2"; shift 2 ;;
    *) echo "error: unknown flag $1" >&2; exit 1 ;;
  esac
done

if [[ ! -d "$TARGET" ]]; then
  read -r -p "target directory '$TARGET' does not exist. create it? [y/N] " yn
  if [[ "$yn" =~ ^[Yy] ]]; then
    mkdir -p "$TARGET"
  else
    echo "aborted" >&2
    exit 1
  fi
fi

TARGET="$(cd "$TARGET" && pwd)"

if [[ "$TARGET" == "$SCRIPT_DIR" ]]; then
  echo "error: target directory equals aegis source directory" >&2
  exit 1
fi

echo
echo "aegis bootstrap — preparing $TARGET"
echo

# Interactive prompts when flags were not supplied.
if [[ -z "$PROJECT_NAME" ]]; then
  read -r -p "Project name (free-form, displayed in phase.md): " PROJECT_NAME
fi

if [[ -z "$SCOPE" ]]; then
  cat <<'EOF'

Scope classification (see playbooks/00-audit.md for the decision tree):
  micro    — single file/module, <200 LOC, no public API
  small    — 1 subsystem, 2-3 modules, limited public surface
  standard — multiple subsystems OR complex security/compliance
  large    — multi-team, multiple independent release cycles
EOF
  read -r -p "Scope [micro|small|standard|large]: " SCOPE
fi

case "$SCOPE" in
  micro|small|standard|large) : ;;
  *) echo "error: scope must be one of micro|small|standard|large" >&2; exit 1 ;;
esac

if [[ -z "$PROJECT_TYPE" ]]; then
  read -r -p "Project type [application|library|cli|spec-only|other]: " PROJECT_TYPE
fi

if [[ -z "$LIFECYCLE_MODE" ]]; then
  read -r -p "Lifecycle mode [finite-delivery|steady-state]: " LIFECYCLE_MODE
fi

case "$LIFECYCLE_MODE" in
  finite-delivery|steady-state) : ;;
  *) echo "error: lifecycle mode must be one of finite-delivery|steady-state" >&2; exit 1 ;;
esac

if [[ -z "$TERMINAL_PHASE" ]]; then
  if [[ "$PROJECT_TYPE" == "spec-only" ]]; then
    TERMINAL_PHASE="2-spec"
  else
    TERMINAL_PHASE="3-implement"
  fi
fi

case "$TERMINAL_PHASE" in
  0-audit|1-design|2-spec|3-implement) : ;;
  *) echo "error: terminal phase invalid" >&2; exit 1 ;;
esac

echo
echo "Configuration:"
echo "  target         = $TARGET"
echo "  project name   = $PROJECT_NAME"
echo "  scope          = $SCOPE"
echo "  lifecycle mode = $LIFECYCLE_MODE"
echo "  project type   = $PROJECT_TYPE"
echo "  terminal phase = $TERMINAL_PHASE"
echo

read -r -p "proceed? [y/N] " go
if ! [[ "$go" =~ ^[Yy] ]]; then
  echo "aborted" >&2
  exit 1
fi

# Copy framework files. Use cp -a to preserve the CLAUDE.md symlink.
echo "copying framework files..."
cp -a "$SCRIPT_DIR/AGENTS.md" "$TARGET/"
cp -a "$SCRIPT_DIR/CLAUDE.md" "$TARGET/"   # symlink → AGENTS.md
cp -a "$SCRIPT_DIR/CHANGELOG.md" "$TARGET/"
cp -a "$SCRIPT_DIR/LICENSE" "$TARGET/"
cp -a "$SCRIPT_DIR/.gitignore" "$TARGET/"
cp -a "$SCRIPT_DIR/README.md" "$TARGET/"
if [[ -f "$SCRIPT_DIR/ONBOARDING.md" ]]; then
  cp -a "$SCRIPT_DIR/ONBOARDING.md" "$TARGET/"
fi
cp -a "$SCRIPT_DIR/validate.py" "$TARGET/"
cp -a "$SCRIPT_DIR/playbooks" "$TARGET/"
cp -a "$SCRIPT_DIR/harness" "$TARGET/"
mkdir -p "$TARGET/tools"
cp -a "$SCRIPT_DIR/tools/bootstrap.sh" "$TARGET/tools/"

# Reset .agent-state/ to template-only. We read the SCHEMA blocks from the aegis
# source copies and rewrite the state files with empty entry sections.
echo "resetting .agent-state/ to template-only..."
mkdir -p "$TARGET/.agent-state"

reset_state() {
  local src="$1"
  local dst="$2"
  local stop="$3"
  # Keep everything up to (but not including) the first line matching $stop.
  awk -v stop="$stop" '
    index($0, stop) { exit }
    { print }
  ' "$src" > "$dst"
}

SRC_STATE="$SCRIPT_DIR/.agent-state"
DST_STATE="$TARGET/.agent-state"

# Defense-in-depth: before any reset logic runs, remove any pre-existing markdown
# state files in $DST_STATE. This guards against two failure modes:
#   (a) $TARGET had a stray `.agent-state/` directory from a prior partial run
#   (b) a future `cp -a` addition to this script that unintentionally copies
#       aegis's historical .agent-state/ contents into $DST_STATE
# Without this, a silent-AWK-skip would let aegis's own D-{n} / G-{n} / L-{n} /
# session-log entries masquerade as the adopter's audit history.
rm -f "$DST_STATE"/*.md

if [[ -d "$SRC_STATE" ]]; then
  # phase.md — keep SCHEMA + frontmatter prose; rewrite header values.
  cp -a "$SRC_STATE/phase.md" "$DST_STATE/phase.md"
  # audit.md — keep canonical scaffold, but drop live project-specific content.
  if [[ -f "$SRC_STATE/audit.md" ]]; then
    cp -a "$SRC_STATE/audit.md" "$DST_STATE/audit.md"
  fi
  # decisions.md, gaps.md, lessons.md — keep SCHEMA; truncate body to the SCHEMA.
  for f in decisions.md gaps.md lessons.md; do
    if [[ -f "$SRC_STATE/$f" ]]; then
      awk '
        /^-->/ && in_schema { print; in_schema=0; print_cursor=1; next }
        /^<!-- SCHEMA/ { in_schema=1 }
        in_schema { print; next }
        print_cursor { exit }
      ' "$SRC_STATE/$f" > "$DST_STATE/$f"
      echo "" >> "$DST_STATE/$f"
      echo "# ${f%.md}" >> "$DST_STATE/$f"
      echo "" >> "$DST_STATE/$f"
      echo "_(template — no entries yet. see SCHEMA above for entry format.)_" >> "$DST_STATE/$f"
      echo "" >> "$DST_STATE/$f"
    fi
  done
fi

# Rewrite phase.md header with project-specific values.
TODAY=$(date -u +%Y-%m-%d)
PHASE_MD="$DST_STATE/phase.md"
AUDIT_MD="$DST_STATE/audit.md"
python3 - "$PHASE_MD" "$AUDIT_MD" "$PROJECT_NAME" "$SCOPE" "$LIFECYCLE_MODE" "$PROJECT_TYPE" "$TERMINAL_PHASE" "$TODAY" <<'PY'
import re
import sys
from pathlib import Path

phase_path, audit_path, name, scope, lifecycle, ptype, term, today = sys.argv[1:9]

phase_text = Path(phase_path).read_text()
# Replace the values after "Current phase:", "Terminal phase:", "Lifecycle mode:", "Scope classification:", "Project type:", and "Last updated:".
phase_text = re.sub(r'(?m)^\*\*Current phase:\*\*.*$', '**Current phase:** 0-audit', phase_text)
phase_text = re.sub(r'(?m)^\*\*Terminal phase:\*\*.*$', f'**Terminal phase:** {term}', phase_text)
phase_text = re.sub(r'(?m)^\*\*Lifecycle mode:\*\*.*$', f'**Lifecycle mode:** {lifecycle}', phase_text)
phase_text = re.sub(r'(?m)^\*\*Scope classification:\*\*.*$', f'**Scope classification:** {scope}', phase_text)
phase_text = re.sub(r'(?m)^\*\*Project type:\*\*.*$', f'**Project type:** {ptype}' + (f' ({name})' if name else ''), phase_text)
phase_text = re.sub(r'(?m)^\*\*Last updated:\*\*.*$', f'**Last updated:** {today}', phase_text)
# Reset Integrity Invariants, Handoff Context, and Session Log to empty starter state.
phase_text = re.sub(
    r'## Integrity Invariants.*?(?=\n## Handoff Context)',
    '## Integrity Invariants\n\n- (none yet — first session should record the initial integrity check in Handoff Context.)\n',
    phase_text,
    count=1,
    flags=re.DOTALL,
)
phase_text = re.sub(
    r'## Handoff Context.*?(?=\n## Feature Slices \(if applicable\))',
    (
        '## Handoff Context\n\n'
        'Update before ending a session — this is the primary handoff mechanism between sessions or collaborators.\n\n'
        '**Exit audit (from prior agent):** (none — new project; no prior agent)\n\n'
        '**In progress:** fresh bootstrap. Next step: read AGENTS.md first, then ONBOARDING.md as companion context, then playbooks/00-audit.md to begin Phase 0 audit.\n\n'
        '**Entry acknowledgment (by receiving agent):** (none — new project; first session)\n\n'
        '**Next:** start Phase 0 surface audit. Record findings in .agent-state/audit.md per per-surface entry format.\n'
    ),
    phase_text,
    count=1,
    flags=re.DOTALL,
)
phase_text = re.sub(
    r'## Session Log.*\Z',
    (
        '## Session Log\n\n'
        '| Date | Phase | Duration | Work Done | Decisions Made | Gaps Found | Lessons Learned |\n'
        '|------|-------|----------|-----------|----------------|------------|-----------------|\n'
    ),
    phase_text,
    count=1,
    flags=re.DOTALL,
)
Path(phase_path).write_text(phase_text)

audit_file = Path(audit_path)
if audit_file.exists():
    audit_text = audit_file.read_text()
    schema_end = audit_text.find("-->")
    strategy_intro = re.search(r'(?s)(# Audit Register.*?)(?=\n## Strategy)', audit_text)
    surface_intro = re.search(r'(?s)(## Surface Audits.*)\Z', audit_text)
    if schema_end != -1 and strategy_intro:
        surface_section = (
            surface_intro.group(1).strip()
            if surface_intro
            else '## Surface Audits\n\n(One `### {SurfaceName}` entry per surface. Use the entry format in the SCHEMA above. See `playbooks/00-audit.md` Surfaces for the full list and `playbooks/00-audit.md` Per-Surface Entry Format for field semantics.)'
        )
        audit_text = (
            audit_text[: schema_end + 3].rstrip()
            + "\n\n"
            + strategy_intro.group(1).strip()
            + "\n\n"
            + "## Strategy\n\n"
            + "**Approach:** \n\n"
            + f"**Lifecycle mode:** {lifecycle}\n\n"
            + "**Rationale:** \n\n"
            + "**Top risks:**\n- \n\n"
            + surface_section
            + "\n"
        )
        audit_file.write_text(audit_text)
PY

# Sanity-check state reset. If any aegis-era identifier entry or session-log row
# survived the reset, abort loudly rather than let the adopter inherit false
# audit history. These checks are intentionally cheap and run before
# validate.py so their failure message is the first thing the user sees.
# Note: we concatenate with cat so grep -c returns a single total, not a
# per-file count vector.
LEAK_IDS=$(cat "$DST_STATE"/*.md 2>/dev/null | grep -cE '^(D|G|L|FR|NFR|SC)-[0-9]+' || true)
LEAK_IDS=${LEAK_IDS:-0}
if (( LEAK_IDS > 0 )); then
  echo >&2
  echo "error: state reset incomplete — $LEAK_IDS identifier entries survived in .agent-state/" >&2
  echo "        aegis's own D-{n} / G-{n} / L-{n} history must not leak into the new project" >&2
  echo "        rerun bootstrap after investigating; do NOT proceed with this target" >&2
  exit 1
fi
LEAK_ROWS=$(grep -cE '^\| 20[0-9]{2}-[0-9]{2}-[0-9]{2} \|' "$DST_STATE/phase.md" 2>/dev/null || true)
LEAK_ROWS=${LEAK_ROWS:-0}
if (( LEAK_ROWS > 0 )); then
  echo >&2
  echo "error: state reset incomplete — $LEAK_ROWS session-log rows survived in phase.md" >&2
  echo "        aegis's own session history must not leak into the new project" >&2
  exit 1
fi

# Validate.
echo "running validate.py..."
if (cd "$TARGET" && python3 validate.py); then
  echo
  echo "bootstrap complete."
  echo
  echo "Next steps:"
  echo "  1. cd $TARGET"
  echo "  2. read AGENTS.md first, then ONBOARDING.md as companion context"
  echo "  3. begin Phase 0 audit per playbooks/00-audit.md"
  echo
  if [[ -f "$SCRIPT_DIR/ONBOARDING.md" ]]; then
    echo "  (ONBOARDING.md copied to target.)"
  fi
else
  echo
  echo "validate.py reported failures — review output above." >&2
  exit 1
fi
