#!/usr/bin/env python3
"""Mechanical validator for aegis.

Automates the [M] items that the adversarial review protocol checks by hand.
Judgment [J] items remain the reviewer's responsibility — this script only
verifies what can be deterministically grepped or parsed.

Checks:
  1. Frontmatter parses on AGENTS.md and every playbooks/*.md and carries
     all 11 required fields (id, title, version, last_reviewed, applies_to,
     severity, mechanical_items, judgment_items, mixed_items, references,
     supersedes)
  2. references: paths in frontmatter resolve to existing files
  3. mechanical_items / judgment_items / mixed_items counts each match the
     body's pure **[M]** / pure **[J]** / **[M+J]** tag counts respectively
  4. State files in .agent-state/ begin with a <!-- SCHEMA: ... --> block
  5. CLAUDE.md is a symlink to AGENTS.md
  6. Version agrees across: AGENTS.md frontmatter, AGENTS.md body banner,
     every playbook frontmatter, and the top versioned CHANGELOG section.
  7. Every Evidence cell in every Verification Coverage Matrix block in
     .agent-state/phase.md (+ phase-archive.md if present) carries a
     verifiable reference per principles.md D5: file:line, sha256:hex,
     session-log anchor, subagent ref, or literal "(pending)" when the
     row's Result cell is also pending. Prose-only cells fail.
  8. Derived-enumeration parity: cross-file lists that must agree — gap
     types (playbooks/gaps.md vs .agent-state/gaps.md vs skills/gap/SKILL.md),
     decision states (playbooks/01-design.md vs .agent-state/decisions.md
     vs skills/decision/SKILL.md). Each concept has ONE canonical owner;
     every other location MUST carry the same set.
  9. Every Accepted or Final decision in .agent-state/decisions.md carries
     a non-empty "Alternatives considered:" field (placeholder text,
     empty, or literal "TBD" fails). Non-significant decisions MAY record
     "Alternatives considered: N/A — not significant" per the glossary.
     Vacuous when no decisions exist yet.
 10. CHANGELOG.md Pre-Ship Self-Compliance Evidence discipline: for the
     most-recent non-[Unreleased] MINOR or MAJOR section, a Pre-Ship
     Self-Compliance Evidence subsection MUST exist and every artifact
     row MUST be verifiable (not prose like "verified"/"checked"). PATCH
     sections are exempt per AGENTS.md Amendment Protocol.
 11. Gap entry completeness: no `Status: captured` entries MAY survive
     into a gate run (Quick Capture MUST be triaged to full `open`
     entries), and every `Status: open` entry MUST carry 6 baseline
     SCHEMA fields (Status, Severity, Type, Description, Resolution
     path, Date opened). Vacuous on empty gap trackers.
 12. Silent-deferral banned-phrase scan: src/, tests/, specs/ (when
     present) MUST NOT contain marker phrases indicating silent scope
     reduction ("v1", "placeholder", "for now", "initial version", etc.)
     UNLESS at least one matching open scope-reduction gap exists.
 13. SC-{n} set coverage: every declared SC-{n} identifier in specs/
     MUST have at least one `Covers: SC-{n}` or `covers_SC-{n}` string
     in tests/ or src/. Set-based (not count-based) — prevents fake
     references from inflating counts.
 14. Verification Coverage Matrix anchor diversity: within each matrix
     block in .agent-state/phase.md, the distinct-set size of Evidence
     anchors MUST be at least 3 — a 5-row matrix pointing at the same
     artifact in every row is not honest witness coverage.
 15. Multi-agent lock-file validity: when .agent-state/.lock-decisions
     exists, it MUST contain 4 required fields (agent_id, acquired_at,
     expected_duration_minutes, purpose) and `acquired_at` MUST be within
     the last 24 hours. Vacuous for single-agent sessions (no lock).
 16. Subsystem Ownership entry: for scope classification standard or
     large, either a D-13+ Subsystem Ownership decision or a "Subsystem
     Ownership: N/A" gap entry MUST exist. Vacuous for micro/small
     scope or when scope classification is not yet set.
 17. SYNC-IMPACT format compliance: every framework file carrying a
     `<!-- SYNC-IMPACT ... -->` HTML comment MUST have version (X.Y.Z →
     A.B.C), bump (MAJOR|MINOR|PATCH), date (YYYY-MM-DD), and non-empty
     rationale fields. Catches format drift in future amendments.

check_7 (evidence verifiability) enforces full reference resolution:
file:line must be within file length; file#anchor must resolve to an
existing file; <subagent:NAME> must have an archived review at
.agent-state/reviews/*-NAME.md. See check_evidence_verifiability for
details.

Usage: python3 validate.py
Exit 0 on clean, non-zero with a bulleted failure list otherwise.
Uses Python stdlib only — no external dependencies.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent
FAILURES: list[str] = []

REQUIRED_FRONTMATTER_FIELDS = {
    "id",
    "title",
    "version",
    "last_reviewed",
    "applies_to",
    "severity",
    "mechanical_items",
    "judgment_items",
    "mixed_items",
    "references",
    "supersedes",
}


def fail(msg: str) -> None:
    FAILURES.append(msg)


def strip_leading_html_comments(text: str) -> str:
    """Remove any leading <!-- ... --> blocks (e.g., SYNC-IMPACT comments)."""
    pattern = re.compile(r"\A\s*<!--.*?-->\s*", re.DOTALL)
    while True:
        m = pattern.match(text)
        if not m:
            return text
        text = text[m.end() :]


def parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str]:
    """Parse simple flat YAML frontmatter.

    Returns (frontmatter_dict, body_string). If the file has no frontmatter,
    returns (None, full_text).
    """
    raw = path.read_text(encoding="utf-8")
    text = strip_leading_html_comments(raw)
    if not text.startswith("---"):
        return None, raw
    close_idx = text.find("\n---", 3)
    if close_idx == -1:
        fail(f"{path.relative_to(REPO_ROOT)}: frontmatter not closed with --- marker")
        return None, raw
    fm_text = text[3:close_idx]
    body = text[close_idx + 4 :]

    fm: dict[str, Any] = {}
    current_list: list[Any] | None = None

    for line in fm_text.split("\n"):
        if not line.strip():
            continue
        list_item = re.match(r"^\s+-\s+(.*)$", line)
        if list_item and current_list is not None:
            val = list_item.group(1).strip()
            if ":" in val:
                k, v = val.split(":", 1)
                current_list.append({k.strip(): v.strip()})
            else:
                current_list.append(val)
            continue
        kv = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if kv:
            key, value = kv.group(1), kv.group(2).strip()
            if value == "":
                current_list = []
                fm[key] = current_list
            else:
                fm[key] = value
                current_list = None

    return fm, body


def collect_frontmatter_files() -> list[Path]:
    # Frontmatter is REQUIRED on AGENTS.md and every playbooks/*.md file.
    #
    # Intentionally EXCLUDED (not a silent omission — documented decision):
    #   - README.md     — external-facing narrative; README convention is no YAML frontmatter
    #   - ONBOARDING.md — external-facing narrative; primer for first-time adopters
    #   - CHANGELOG.md  — follows Keep a Changelog format (https://keepachangelog.com/)
    #                     which does not use YAML frontmatter; version tracking is in
    #                     the per-release ## [X.Y.Z] sections themselves
    # State archive files (`*-archive.md`) are historical records — no frontmatter.
    # No `-sync-archive.md` convention — SYNC-IMPACT history lives inline only.
    files = [REPO_ROOT / "AGENTS.md"]
    files.extend(sorted(
        f for f in (REPO_ROOT / "playbooks").glob("*.md")
        if not f.name.endswith("-archive.md")
    ))
    return files


def check_frontmatter(files: list[Path]) -> None:
    for f in files:
        fm, _ = parse_frontmatter(f)
        rel = f.relative_to(REPO_ROOT)
        if fm is None:
            fail(f"[1/frontmatter] {rel}: missing or malformed frontmatter")
            continue
        missing = REQUIRED_FRONTMATTER_FIELDS - set(fm.keys())
        if missing:
            fail(f"[1/frontmatter] {rel}: missing required fields: {sorted(missing)}")


def check_references(files: list[Path]) -> None:
    for f in files:
        fm, _ = parse_frontmatter(f)
        if fm is None:
            continue
        rel = f.relative_to(REPO_ROOT)
        refs = fm.get("references")
        if refs in (None, "null", []):
            continue
        if not isinstance(refs, list):
            continue
        for ref in refs:
            if not isinstance(ref, str):
                continue
            target = REPO_ROOT / ref
            if not target.exists():
                fail(f"[2/references] {rel}: references '{ref}' but path does not exist")


def count_tags(body: str) -> tuple[int, int, int]:
    """Return (mechanical_count, judgment_count, mixed_count) of bold gate tags.

    Gate items use bold markdown:
      `**[M]**`   = pure mechanical → counted in mechanical_count
      `**[J]**`   = pure judgment   → counted in judgment_count
      `**[M+J]**` = mixed           → counted in mixed_count (NOT in pure totals)

    The three counts are independent. The frontmatter fields
    `mechanical_items`, `judgment_items`, and `mixed_items` track them
    separately. Prose mentions use backticks (`` `[M]` ``) and are not
    matched here.
    """
    plain_m = len(re.findall(r"\*\*\[M\]\*\*", body))
    plain_j = len(re.findall(r"\*\*\[J\]\*\*", body))
    mixed = len(re.findall(r"\*\*\[M\+J\]\*\*", body))
    return plain_m, plain_j, mixed


def check_tag_counts(files: list[Path]) -> None:
    for f in files:
        fm, body = parse_frontmatter(f)
        if fm is None:
            continue
        rel = f.relative_to(REPO_ROOT)
        try:
            declared_m = int(fm.get("mechanical_items", "0"))
            declared_j = int(fm.get("judgment_items", "0"))
            declared_mixed = int(fm.get("mixed_items", "0"))
        except (TypeError, ValueError):
            fail(
                f"[3/tag-counts] {rel}: mechanical_items, judgment_items, "
                f"or mixed_items is not an integer"
            )
            continue
        actual_m, actual_j, actual_mixed = count_tags(body)
        if declared_m != actual_m:
            fail(
                f"[3/tag-counts] {rel}: declares mechanical_items={declared_m} "
                f"but body has {actual_m} **[M]** tags"
            )
        if declared_j != actual_j:
            fail(
                f"[3/tag-counts] {rel}: declares judgment_items={declared_j} "
                f"but body has {actual_j} **[J]** tags"
            )
        if declared_mixed != actual_mixed:
            fail(
                f"[3/tag-counts] {rel}: declares mixed_items={declared_mixed} "
                f"but body has {actual_mixed} **[M+J]** tags"
            )


def check_state_schemas() -> None:
    state_dir = REPO_ROOT / ".agent-state"
    if not state_dir.is_dir():
        fail("[4/schema] .agent-state/ directory is missing")
        return
    for f in sorted(state_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8").lstrip()
        rel = f.relative_to(REPO_ROOT)
        if not text.startswith("<!-- SCHEMA:"):
            fail(f"[4/schema] {rel}: does not begin with <!-- SCHEMA: ... --> block")
            continue
        end = text.find("-->")
        if end == -1:
            fail(f"[4/schema] {rel}: SCHEMA block not closed with -->")


def check_claude_symlink() -> None:
    claude = REPO_ROOT / "CLAUDE.md"
    if not claude.exists():
        fail("[5/symlink] CLAUDE.md is missing")
        return
    if not claude.is_symlink():
        fail("[5/symlink] CLAUDE.md exists but is not a symlink (must point to AGENTS.md)")
        return
    target = os.readlink(claude)
    if target != "AGENTS.md":
        fail(f"[5/symlink] CLAUDE.md points to '{target}' instead of 'AGENTS.md'")


def check_version_consistency(files: list[Path]) -> None:
    agents = REPO_ROOT / "AGENTS.md"
    fm, body = parse_frontmatter(agents)
    if fm is None or "version" not in fm:
        fail("[6/version] AGENTS.md has no frontmatter version field")
        return
    canonical = str(fm["version"]).strip()

    banner = re.search(r"aegis v(\d+\.\d+\.\d+)", body)
    if not banner:
        fail("[6/version] AGENTS.md body has no 'aegis vX.Y.Z' banner line")
    elif banner.group(1) != canonical:
        fail(
            f"[6/version] AGENTS.md frontmatter version={canonical} "
            f"but body banner says v{banner.group(1)}"
        )

    for f in files:
        if f.name == "AGENTS.md":
            continue
        pm, _ = parse_frontmatter(f)
        if pm is None:
            continue
        v = str(pm.get("version", "")).strip()
        if v != canonical:
            fail(
                f"[6/version] {f.relative_to(REPO_ROOT)} frontmatter version={v} "
                f"but AGENTS.md is {canonical}"
            )

    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    versioned = re.findall(r"^##\s*\[v?(\d+\.\d+\.\d+)\]", changelog, re.MULTILINE)
    if not versioned:
        fail("[6/version] CHANGELOG.md has no versioned ## [vX.Y.Z] sections")
    elif versioned[0] != canonical:
        fail(
            f"[6/version] CHANGELOG.md top version is {versioned[0]} "
            f"but AGENTS.md is {canonical}"
        )


EVIDENCE_PATTERNS = [
    re.compile(r"^[A-Za-z0-9_./-]+\.[A-Za-z0-9]+:\d+$"),  # file:line reference
    re.compile(r"^[A-Za-z0-9_./-]+\.[A-Za-z0-9]+#[\w.-]+$"), # file#anchor reference
    re.compile(r"^sha256:[0-9a-f]{64}$"),              # command-output hash
    re.compile(r"^#session-\d{4}-\d{2}-\d{2}-[\w.-]+$"), # session-log anchor
    re.compile(r"^<subagent:[a-z][a-z0-9-]*(:[a-z0-9-]+)*>$"), # subagent ref
    re.compile(r"^\(pending\)$"),                      # pending row
]

# Extract the primary anchor from an Evidence cell: if the cell contains a
# backtick-quoted span, take that; otherwise the whole cell is the anchor.
# This lets cells carry the anchor followed by optional explanatory prose,
# e.g. `` `CHANGELOG.md#unreleased` — 16 rows matching each rule change ``.
EVIDENCE_ANCHOR_EXTRACT = re.compile(r"`([^`]+)`")


def _resolve_evidence_reference(
    ref: str, *, phase_text: str, phase_archive_text: str = ""
) -> str | None:
    """Resolve a shape-compliant evidence reference to its backing artifact.

    Returns None when the reference resolves, or a short error string when
    it does not. Shape-compliance is a precondition — callers MUST match
    EVIDENCE_PATTERNS first. Resolution is strict:
      * `file.md:N`  — file MUST exist; N MUST be within file length.
      * `file.md#anchor` — file MUST exist (anchor specificity is judgment).
      * `sha256:hex` — opaque commitment; accepted without resolution.
      * `#session-YYYY-MM-DD-slug` — grep phase.md + phase-archive.md for the
        literal slug (heading or boundary line).
      * `<subagent:NAME>` — `.agent-state/reviews/*-NAME.md` MUST exist.
      * `(pending)` — handled by caller; not passed to this resolver.
    """
    m = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)$", ref)
    if m:
        path = REPO_ROOT / m.group(1)
        if not path.exists():
            return f"file {m.group(1)} does not exist"
        line_count = len(path.read_text(encoding="utf-8", errors="replace").splitlines())
        n = int(m.group(2))
        if n < 1 or n > line_count:
            return (
                f"line {n} out of range for {m.group(1)} "
                f"(has {line_count} lines)"
            )
        return None

    m = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)#([\w.-]+)$", ref)
    if m:
        path = REPO_ROOT / m.group(1)
        if not path.exists():
            return f"file {m.group(1)} does not exist"
        return None

    if re.match(r"^sha256:[0-9a-f]{64}$", ref):
        return None

    m = re.match(r"^#session-(\d{4}-\d{2}-\d{2})-([\w.-]+)$", ref)
    if m:
        date, slug = m.group(1), m.group(2)
        haystack = phase_text + "\n" + phase_archive_text
        needle = f"session-{date}-{slug}"
        if needle in haystack:
            return None
        bdy = re.compile(rf"Session boundary {re.escape(date)}", re.IGNORECASE)
        if bdy.search(haystack) and slug.replace("-", " ").lower() in haystack.lower():
            return None
        return f"session anchor {ref} not found in phase.md/phase-archive.md"

    m = re.match(r"^<subagent:([a-z][a-z0-9-]*(?::[a-z0-9-]+)*)>$", ref)
    if m:
        name = m.group(1).replace(":", "-")
        reviews = REPO_ROOT / ".agent-state" / "reviews"
        if not reviews.is_dir():
            return (
                f"{ref}: .agent-state/reviews/ does not exist "
                f"(required for subagent refs — see reviews/README.md)"
            )
        matches = list(reviews.glob(f"*-{name}.md"))
        if not matches:
            return (
                f"{ref}: no .agent-state/reviews/*-{name}.md artifact found "
                f"(fresh-context subagent output MUST be archived)"
            )
        return None

    return f"reference form not recognized: {ref}"


def check_evidence_verifiability() -> None:
    """Enforce principles.md D5: every Evidence cell in every Verification
    Coverage Matrix block MUST carry a verifiable reference, not prose.

    Each cell's primary anchor (the first backticked span, or the full cell if
    it matches a shape pattern directly) MUST resolve to a real artifact.
    Heading detection accepts any ## or deeper — an H2-only detector would
    silently let fake evidence pass under H3 matrix formats."""
    state_dir = REPO_ROOT / ".agent-state"
    if not state_dir.is_dir():
        return  # check_state_schemas already flagged this

    phase_text = ""
    phase_archive_text = ""
    if (state_dir / "phase.md").exists():
        phase_text = (state_dir / "phase.md").read_text(encoding="utf-8")
    if (state_dir / "phase-archive.md").exists():
        phase_archive_text = (state_dir / "phase-archive.md").read_text(
            encoding="utf-8"
        )

    for phase_file in ("phase.md", "phase-archive.md"):
        f = state_dir / phase_file
        if not f.exists():
            continue

        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(REPO_ROOT)
        lines = text.splitlines()

        in_matrix = False
        header_cols: list[str] | None = None
        evidence_idx: int | None = None
        result_idx: int | None = None

        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Match any markdown heading (## or deeper). The matrix typically
            # lives under a Handoff Context ### subheading; accepting any
            # heading depth prevents fake evidence from slipping through under
            # H3 matrix formats.
            if re.match(r"^#{2,}\s", stripped):
                in_matrix = "Verification Coverage Matrix" in stripped
                header_cols = None
                evidence_idx = None
                result_idx = None
                continue

            if not in_matrix or not stripped.startswith("|"):
                continue

            cells = [c.strip() for c in stripped.strip("|").split("|")]

            if header_cols is None:
                header_cols = [c.lower() for c in cells]
                if "evidence" in header_cols:
                    evidence_idx = header_cols.index("evidence")
                if "result" in header_cols:
                    result_idx = header_cols.index("result")
                if evidence_idx is None:
                    in_matrix = False
                continue

            if all(set(c) <= set("-:") or c == "" for c in cells):
                continue

            if evidence_idx is None or evidence_idx >= len(cells):
                continue

            evidence = cells[evidence_idx]
            if not evidence:
                fail(
                    f"[7/evidence] {rel}:{lineno} empty Evidence cell — "
                    f"principles.md D5 requires a verifiable reference"
                )
                continue

            if evidence == "(pending)":
                if result_idx is not None and result_idx < len(cells):
                    result = cells[result_idx].lower()
                    if result and result != "pending":
                        fail(
                            f"[7/evidence] {rel}:{lineno} Evidence is (pending) "
                            f"but Result is {result!r} — pending evidence is only "
                            f"valid for a pending row"
                        )
                continue

            # Extract the primary anchor — first backticked span if present,
            # else the cell itself (for bare-anchor cells).
            anchor = evidence
            backticked = EVIDENCE_ANCHOR_EXTRACT.search(evidence)
            if backticked:
                anchor = backticked.group(1).strip()

            if not any(p.match(anchor) for p in EVIDENCE_PATTERNS):
                fail(
                    f"[7/evidence] {rel}:{lineno} Evidence cell's primary "
                    f"anchor {anchor!r} is not shape-compliant — expected "
                    f"file.md:line | file.md#anchor | sha256:hex | "
                    f"#session-YYYY-MM-DD-slug | <subagent:name> | (pending)"
                )
                continue

            err = _resolve_evidence_reference(
                anchor,
                phase_text=phase_text,
                phase_archive_text=phase_archive_text,
            )
            if err is not None:
                fail(
                    f"[7/evidence] {rel}:{lineno} Evidence anchor "
                    f"{anchor!r} cannot be resolved: {err}"
                )


# --- check_8: derived-enumeration parity -----------------------------------

def _extract_gap_types_canonical() -> set[str]:
    """Extract gap types from playbooks/gaps.md Gap Type Taxonomy table (rows
    of the form ``| **{type}** | meaning | when | resolution |``)."""
    text = (REPO_ROOT / "playbooks" / "gaps.md").read_text(encoding="utf-8")
    types: set[str] = set()
    # The Gap Type Taxonomy table starts after the "## Gap Type Taxonomy" heading;
    # rows are `| **name** | ...`. Only capture within that table region.
    in_taxonomy = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_taxonomy = line.strip() == "## Gap Type Taxonomy"
            continue
        if not in_taxonomy:
            continue
        m = re.match(r"^\|\s*\*\*([a-z-]+)\*\*\s*\|", line)
        if m:
            types.add(m.group(1))
    return types


def _extract_gap_types_schema_enum() -> set[str]:
    """Extract gap types from the SCHEMA block ``**Type:** a | b | ...`` in
    .agent-state/gaps.md."""
    text = (REPO_ROOT / ".agent-state" / "gaps.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Type:\*\*\s*([a-z \|-]+)", text)
    if not m:
        return set()
    return {t.strip() for t in m.group(1).split("|") if t.strip()}


def _extract_gap_types_skill() -> set[str]:
    """Extract gap types from harness/claude-code/skills/gap/SKILL.md bullets
    of the form ``- **name** —``."""
    path = REPO_ROOT / "harness" / "claude-code" / "skills" / "gap" / "SKILL.md"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    types: set[str] = set()
    in_types_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_types_section = line.strip() == "## Gap types"
            continue
        if not in_types_section:
            continue
        m = re.match(r"^- \*\*([a-z-]+)\*\*\s*—", line)
        if m:
            types.add(m.group(1))
    return types


def _extract_decision_states_canonical() -> set[str]:
    """Extract decision-state values from playbooks/01-design.md Decision
    Entry Format ``**Status:** Draft | Proposed | ...`` line."""
    text = (REPO_ROOT / "playbooks" / "01-design.md").read_text(encoding="utf-8")
    m = re.search(
        r"\*\*Status:\*\*\s*(Draft\s*\|[^\n]+?)\n",
        text,
    )
    if not m:
        return set()
    states: set[str] = set()
    for piece in m.group(1).split("|"):
        name = piece.strip()
        # "Superseded (by D-{new})" collapses to "Superseded" for the enum.
        name = re.sub(r"\s*\(.*?\)", "", name).strip()
        if name:
            states.add(name)
    return states


def _extract_decision_states_schema() -> set[str]:
    """Extract decision-state values from .agent-state/decisions.md SCHEMA
    ``**Status:** ...`` line."""
    text = (REPO_ROOT / ".agent-state" / "decisions.md").read_text(encoding="utf-8")
    m = re.search(r"\*\*Status:\*\*\s*([A-Za-z \|\-\(\){}]+)", text)
    if not m:
        return set()
    states: set[str] = set()
    for piece in m.group(1).split("|"):
        name = piece.strip()
        name = re.sub(r"\s*\(.*?\)", "", name).strip()
        if name:
            states.add(name)
    return states


def _extract_decision_states_skill() -> set[str]:
    """Extract decision-state values from skills/decision/SKILL.md ``Status
    (Draft | ...)`` line."""
    path = REPO_ROOT / "harness" / "claude-code" / "skills" / "decision" / "SKILL.md"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    m = re.search(r"`?Status`?\s*\(([^)]+)\)", text)
    if not m:
        return set()
    return {s.strip() for s in m.group(1).split("|") if s.strip()}


def check_derived_enumeration_parity() -> None:
    """Every derived list of a canonical enumeration MUST equal the canonical
    set. Catches the class of defect where a derived list silently drifts from
    its canonical source."""

    groups: list[tuple[str, str, set[str], list[tuple[str, set[str]]]]] = [
        (
            "gap types",
            "playbooks/gaps.md (Gap Type Taxonomy)",
            _extract_gap_types_canonical(),
            [
                (".agent-state/gaps.md (SCHEMA)", _extract_gap_types_schema_enum()),
                (
                    "harness/claude-code/skills/gap/SKILL.md",
                    _extract_gap_types_skill(),
                ),
            ],
        ),
        (
            "decision states",
            "playbooks/01-design.md (Decision Entry Format)",
            _extract_decision_states_canonical(),
            [
                (".agent-state/decisions.md (SCHEMA)", _extract_decision_states_schema()),
                (
                    "harness/claude-code/skills/decision/SKILL.md",
                    _extract_decision_states_skill(),
                ),
            ],
        ),
    ]

    for name, canonical_src, canonical_set, derived in groups:
        if not canonical_set:
            fail(
                f"[8/parity] {name}: canonical set at {canonical_src} "
                f"could not be extracted"
            )
            continue
        for derived_src, derived_set in derived:
            if not derived_set:
                # An empty derived set is suspicious — flag it.
                fail(
                    f"[8/parity] {name}: derived set at {derived_src} "
                    f"is empty (expected parity with {canonical_src})"
                )
                continue
            missing = canonical_set - derived_set
            extra = derived_set - canonical_set
            if missing or extra:
                parts = []
                if missing:
                    parts.append(f"missing={sorted(missing)}")
                if extra:
                    parts.append(f"extra={sorted(extra)}")
                fail(
                    f"[8/parity] {name}: {derived_src} disagrees with "
                    f"{canonical_src} — {'; '.join(parts)}"
                )


# --- check_9: decision alternatives present -------------------------------

def check_decision_alternatives_present() -> None:
    """Every `Accepted` or `Final` D-{n} entry in .agent-state/decisions.md
    MUST have a non-empty `Alternatives considered:` field. Vacuous when no
    entries exist (template state)."""
    path = REPO_ROOT / ".agent-state" / "decisions.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    # Split on decision headings; skip any that occur inside SCHEMA comments.
    # Everything from `### D-{n}:` until the next `###` or end-of-file is one
    # entry.
    entries = re.split(r"(?m)^### (D-\d+):", text)
    # re.split returns [prelude, id1, body1, id2, body2, ...]
    for i in range(1, len(entries), 2):
        did = entries[i].strip()
        body = entries[i + 1] if i + 1 < len(entries) else ""
        status_match = re.search(r"\*\*Status:\*\*\s*([A-Za-z]+)", body)
        if not status_match:
            continue
        status = status_match.group(1).strip()
        if status not in ("Accepted", "Final"):
            continue
        alt_match = re.search(
            r"\*\*Alternatives considered:\*\*\s*(.+?)(?=\n\*\*|\n###|\Z)",
            body,
            re.DOTALL,
        )
        if not alt_match:
            fail(
                f"[9/alternatives] {did}: Status={status} but no "
                f"'Alternatives considered:' field found"
            )
            continue
        value = alt_match.group(1).strip()
        placeholders = {
            "",
            "TBD",
            "_(to be filled)_",
            "(to be filled)",
            "{to be filled}",
        }
        if value in placeholders or value.startswith("{"):
            fail(
                f"[9/alternatives] {did}: Status={status} but "
                f"'Alternatives considered:' is placeholder/empty"
            )


# --- check_10: CHANGELOG Pre-Ship Self-Compliance Evidence ----------------

_PROSE_ONLY_ARTIFACTS = {"verified", "checked", "clean", "done", "ok"}


def check_changelog_evidence_completeness() -> None:
    """The most-recent non-[Unreleased] MINOR or MAJOR CHANGELOG section MUST
    include a Pre-Ship Self-Compliance Evidence subsection with verifiable
    artifacts (not prose). PATCH sections are exempt."""
    path = REPO_ROOT / "CHANGELOG.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    # Find versioned sections: "## [X.Y.Z] - YYYY-MM-DD (MAJOR|MINOR|PATCH)"
    # Capture the first non-[Unreleased] section only (top of the file).
    pattern = re.compile(
        r"^##\s*\[v?(\d+\.\d+\.\d+)\][^\n]*?\(\s*(MAJOR|MINOR|PATCH)\s*\)",
        re.MULTILINE | re.IGNORECASE,
    )
    m = pattern.search(text)
    if not m:
        return  # No versioned sections yet; nothing to check.
    bump = m.group(2).upper()
    if bump == "PATCH":
        return  # Exempt per AGENTS.md Amendment Protocol.

    version = m.group(1)
    # Extract the section body (from this ## heading to the next ## or EOF).
    start = m.start()
    next_section = re.search(r"^##\s", text[m.end() :], re.MULTILINE)
    end = m.end() + next_section.start() if next_section else len(text)
    body = text[start:end]

    if "Pre-Ship Self-Compliance Evidence" not in body:
        fail(
            f"[10/changelog-evidence] CHANGELOG.md [{version}] ({bump}): "
            f"missing 'Pre-Ship Self-Compliance Evidence' subsection "
            f"(required for MINOR/MAJOR per AGENTS.md Amendment Protocol)"
        )
        return

    # Inside the subsection, every row under a markdown table or every bullet
    # in a list MUST contain a verifiable artifact. Reject rows whose artifact
    # is one of the prose-only tokens.
    subsection_match = re.search(
        r"### Pre-Ship Self-Compliance Evidence(.*?)(?=\n###|\n##|\Z)",
        body,
        re.DOTALL,
    )
    if not subsection_match:
        fail(
            f"[10/changelog-evidence] CHANGELOG.md [{version}]: "
            f"'Pre-Ship Self-Compliance Evidence' section is malformed"
        )
        return
    subsection_text = subsection_match.group(1)

    for lineno, raw_line in enumerate(subsection_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 2:
            continue
        # Skip header + separator rows.
        if all(set(c) <= set("-:") or c == "" for c in cells):
            continue
        if any(c.lower() in ("rule", "fix", "finding", "change", "artifact") for c in cells):
            continue
        artifact = cells[-1].strip().lower()
        # Allow `-n` (en-dash) or any cell containing a verifiable token.
        if not artifact or artifact in _PROSE_ONLY_ARTIFACTS:
            fail(
                f"[10/changelog-evidence] CHANGELOG.md [{version}] "
                f"Pre-Ship Self-Compliance Evidence row {lineno}: "
                f"artifact {artifact!r} is prose-only (expected grep "
                f"output, file:line, SHA, subagent ref, or similar)"
            )


# --- check_11: gap entry completeness (red-team #6) ----------------------

_GAP_OPEN_REQUIRED_FIELDS = (
    "Status",
    "Severity",
    "Type",
    "Description",
    "Resolution path",
    "Date opened",
)


def check_gap_entry_completeness() -> None:
    """Reject `Status: captured` at gate-run time — captured entries MUST be
    triaged to full `open` entries before the next phase gate (gaps.md Quick
    Capture rule). Every `Status: open` entry MUST carry the 6 baseline
    SCHEMA fields.

    Vacuous when gaps.md has no `### G-{n}` entries (template state).
    """
    path = REPO_ROOT / ".agent-state" / "gaps.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    # Split on ### G-{n} entries; [pre, id1, body1, id2, body2, ...]
    parts = re.split(r"(?m)^### (G-\d+):", text)
    for i in range(1, len(parts), 2):
        gid = parts[i].strip()
        body = parts[i + 1] if i + 1 < len(parts) else ""
        status_match = re.search(r"\*\*Status:\*\*\s*([A-Za-z-]+)", body)
        if not status_match:
            continue
        status = status_match.group(1).strip().lower()
        if status == "captured":
            fail(
                f"[11/gap-triage] gaps.md {gid}: Status is 'captured' — "
                f"Quick Capture entries MUST be triaged to 'open' with full "
                f"SCHEMA fields before the next phase gate "
                f"(see playbooks/gaps.md Quick Capture)"
            )
            continue
        if status != "open":
            continue
        for field in _GAP_OPEN_REQUIRED_FIELDS:
            if not re.search(rf"\*\*{re.escape(field)}:\*\*", body):
                fail(
                    f"[11/gap-completeness] gaps.md {gid}: Status=open but "
                    f"required field '{field}' is missing"
                )


# --- check_12: silent-deferral banned-phrase scan (red-team #12) ---------

_DEFERRAL_PHRASES = (
    "v1",
    "v2",
    "simplified version",
    "static for now",
    "placeholder",
    "defer to follow-up",
    "good enough for now",
    "initial version",
    "first pass",
    "stub for the moment",
    "minimal implementation",
    "coming in v2",
    "for now",
    "later",
)

_DEFERRAL_SCAN_DIRS = (
    "src",
    "tests",
    "specs",
)


def check_silent_deferral_phrases() -> None:
    """Grep src/, tests/, specs/ (when present) for banned marker phrases
    indicating silent scope reduction. Any hit MUST have a matching
    `scope-reduction` gap open in .agent-state/gaps.md, otherwise fail.

    Vacuous when none of the scanned dirs exist (spec-only projects like
    aegis itself).
    """
    # Collect open scope-reduction gap IDs — matches act as exemptions.
    gaps_path = REPO_ROOT / ".agent-state" / "gaps.md"
    has_scope_reduction_gaps = False
    if gaps_path.exists():
        gtext = gaps_path.read_text(encoding="utf-8")
        for part in re.split(r"(?m)^### (G-\d+):", gtext)[1:]:
            if re.search(r"\*\*Type:\*\*\s*scope-reduction", part):
                if re.search(r"\*\*Status:\*\*\s*open", part):
                    has_scope_reduction_gaps = True
                    break

    for scan_dir in _DEFERRAL_SCAN_DIRS:
        d = REPO_ROOT / scan_dir
        if not d.is_dir():
            continue
        for path in d.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in (".py", ".md", ".ts", ".js", ".go", ".rs",
                                   ".java", ".kt", ".swift", ".cpp", ".c",
                                   ".h", ".rb", ".php", ".cs"):
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = path.relative_to(REPO_ROOT)
            lines = text.splitlines()
            for lineno, raw in enumerate(lines, start=1):
                line = raw.lower()
                # Skip the validate.py banned-phrase list itself (meta).
                if "_deferral_phrases" in line or "banned marker" in line:
                    continue
                for phrase in _DEFERRAL_PHRASES:
                    if phrase in line:
                        if has_scope_reduction_gaps:
                            # Exempt: an open scope-reduction gap acknowledges
                            # the deferral. Note: this does not verify the gap
                            # references THIS specific file — a future amendment
                            # could tighten by matching gap Description to file
                            # path.
                            break
                        fail(
                            f"[12/deferral] {rel}:{lineno} contains banned "
                            f"deferral phrase {phrase!r} — add a "
                            f"scope-reduction gap to gaps.md OR remove the "
                            f"phrase (see playbooks/03-implement.md Hard "
                            f"Rule 3)"
                        )
                        break


# --- check_13: SC-{n} set coverage (red-team #7) -------------------------

def check_sc_coverage_set() -> None:
    """Every declared SC-{n} identifier in specs/ MUST be referenced by at
    least one `Covers: SC-{n}` or `covers_SC-{n}` string in tests/ or src/.
    Set-based — count-based satisfaction (N fake references to SC-7) passes
    the count check but fails the set check.

    Vacuous when specs/ does not exist.
    """
    specs_dir = REPO_ROOT / "specs"
    if not specs_dir.is_dir():
        return

    declared: set[str] = set()
    for md in specs_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Declared SCs use the heading or bullet form `### SC-N` or `- SC-N:`.
        for m in re.finditer(r"(?m)^(?:###\s+|[-*]\s+)(SC-\d+)\b", text):
            declared.add(m.group(1))

    if not declared:
        return

    covered: set[str] = set()
    for scan_dir in ("tests", "src"):
        d = REPO_ROOT / scan_dir
        if not d.is_dir():
            continue
        for path in d.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for m in re.finditer(r"\b(?:Covers:|covers_)\s*(SC-\d+)\b", text):
                covered.add(m.group(1))

    missing = declared - covered
    if missing:
        fail(
            f"[13/sc-coverage] {len(missing)} declared SC-{{n}} identifier(s) "
            f"have zero `Covers:`/`covers_` references in tests/ or src/: "
            f"{', '.join(sorted(missing))}"
        )


# --- check_14: Verification Coverage Matrix anchor diversity (#4) --------

def check_matrix_anchor_diversity() -> None:
    """Within each Verification Coverage Matrix block in .agent-state/phase.md,
    the distinct-set size of Evidence anchors MUST be at least 3 out of 5
    perspective rows. A matrix where all rows cite the same subagent or the
    same session anchor is a red flag: one artifact cannot honestly witness
    all five perspectives.

    Vacuous when phase.md has no matrix or < 5 rows (template state).
    """
    path = REPO_ROOT / ".agent-state" / "phase.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    in_matrix = False
    header_cols: list[str] | None = None
    evidence_idx: int | None = None
    current_block_anchors: list[str] = []
    block_start_line = 0

    def _flush(block_anchors: list[str], start_line: int) -> None:
        if len(block_anchors) < 5:
            return
        # Extract the first backticked anchor from each row for uniqueness.
        uniq: set[str] = set()
        for cell in block_anchors:
            m = EVIDENCE_ANCHOR_EXTRACT.search(cell)
            anchor = (m.group(1).strip() if m else cell).lower()
            uniq.add(anchor)
        if len(uniq) < 3:
            fail(
                f"[14/matrix-diversity] phase.md:{start_line} Verification "
                f"Coverage Matrix has {len(block_anchors)} rows but only "
                f"{len(uniq)} distinct Evidence anchor(s) — a single "
                f"artifact cannot witness all 5 perspectives honestly"
            )

    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if re.match(r"^#{2,}\s", stripped):
            _flush(current_block_anchors, block_start_line)
            current_block_anchors = []
            block_start_line = lineno
            in_matrix = "Verification Coverage Matrix" in stripped
            header_cols = None
            evidence_idx = None
            continue
        if not in_matrix or not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header_cols is None:
            header_cols = [c.lower() for c in cells]
            if "evidence" in header_cols:
                evidence_idx = header_cols.index("evidence")
            if evidence_idx is None:
                in_matrix = False
            continue
        if all(set(c) <= set("-:") or c == "" for c in cells):
            continue
        if evidence_idx is None or evidence_idx >= len(cells):
            continue
        cell = cells[evidence_idx]
        if cell and cell != "(pending)":
            current_block_anchors.append(cell)

    _flush(current_block_anchors, block_start_line)


# --- check_15: multi-agent lock-file validity (red-team #5) --------------

_LOCK_REQUIRED_FIELDS = ("agent_id", "acquired_at", "expected_duration_minutes", "purpose")


def check_multi_agent_lock_validity() -> None:
    """When `.agent-state/.lock-decisions` exists, it MUST parse as a YAML-like
    key-value file containing 4 required fields (agent_id, acquired_at,
    expected_duration_minutes, purpose) per `principles-conditional.md` Multi-
    Agent Coordination. `acquired_at` MUST be a valid ISO-8601 or
    YYYY-MM-DD HH:MM UTC timestamp within the last 24 hours — stale locks
    indicate an orphaned session that should have been released.

    Vacuous when the lock file does not exist (single-agent sessions).
    """
    lock_path = REPO_ROOT / ".agent-state" / ".lock-decisions"
    if not lock_path.exists():
        return
    try:
        text = lock_path.read_text(encoding="utf-8")
    except OSError as e:
        fail(f"[15/multi-agent-lock] .agent-state/.lock-decisions: read error {e}")
        return

    found: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^([a-z_]+)\s*:\s*(.+?)\s*$", line)
        if m:
            found[m.group(1)] = m.group(2).strip()

    missing = [f for f in _LOCK_REQUIRED_FIELDS if f not in found]
    if missing:
        fail(
            f"[15/multi-agent-lock] .agent-state/.lock-decisions missing "
            f"required fields: {missing}"
        )
        return

    # Age check — lock older than 24h is stale per Multi-Agent Coordination.
    from datetime import datetime, timezone
    acquired_raw = found["acquired_at"]
    acquired = None
    for fmt in (
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M UTC",
        "%Y-%m-%d %H:%M:%S UTC",
        "%Y-%m-%d",
    ):
        try:
            parsed = datetime.strptime(acquired_raw, fmt)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            acquired = parsed
            break
        except ValueError:
            continue
    if acquired is None:
        fail(
            f"[15/multi-agent-lock] .lock-decisions acquired_at "
            f"{acquired_raw!r} does not match any accepted timestamp format"
        )
        return
    age_hours = (datetime.now(timezone.utc) - acquired).total_seconds() / 3600
    if age_hours > 24:
        fail(
            f"[15/multi-agent-lock] .lock-decisions is {age_hours:.1f} hours "
            f"old — locks older than 24h are stale; release or refresh per "
            f"Multi-Agent Coordination"
        )


# --- check_16: Subsystem Ownership N/A entry (red-team #13) --------------

def check_subsystem_ownership_present() -> None:
    """For standard/large scope projects, either a `D-13+` Subsystem Ownership
    decision MUST exist in .agent-state/decisions.md OR a `Subsystem Ownership`
    N/A narrative entry MUST exist in .agent-state/gaps.md (per AGENTS.md
    Multi-Agent Handoff Protocol). Vacuous when phase.md scope is micro/small
    or when phase.md cannot be parsed.
    """
    phase_path = REPO_ROOT / ".agent-state" / "phase.md"
    if not phase_path.exists():
        return
    phase_text = phase_path.read_text(encoding="utf-8")
    scope_match = re.search(
        r"\*\*Scope classification:\*\*\s*([a-z-]+)", phase_text, re.IGNORECASE
    )
    if not scope_match:
        return
    scope = scope_match.group(1).strip().lower()
    if scope not in ("standard", "large"):
        return

    decisions_text = ""
    decisions_path = REPO_ROOT / ".agent-state" / "decisions.md"
    if decisions_path.exists():
        decisions_text = decisions_path.read_text(encoding="utf-8")

    gaps_text = ""
    gaps_path = REPO_ROOT / ".agent-state" / "gaps.md"
    if gaps_path.exists():
        gaps_text = gaps_path.read_text(encoding="utf-8")

    has_ownership_decision = bool(
        re.search(
            r"(?m)^###\s+D-\d+:\s*.*Subsystem\s*Ownership", decisions_text, re.IGNORECASE
        )
    )
    has_ownership_gap_entry = bool(
        re.search(r"Subsystem Ownership:\s*N/A", gaps_text, re.IGNORECASE)
    )

    if not (has_ownership_decision or has_ownership_gap_entry):
        fail(
            f"[16/subsystem-ownership] scope={scope!r} but neither a "
            f"D-13+ Subsystem Ownership decision nor a 'Subsystem Ownership: "
            f"N/A' informational gap entry exists — required per AGENTS.md "
            f"Multi-Agent Handoff Protocol"
        )


# --- check_17: SYNC-IMPACT format compliance (Phase E whole-project) ----

_SYNC_IMPACT_REQUIRED_FIELDS = ("version", "bump", "date", "rationale")
_SYNC_IMPACT_BUMP_VALUES = {"MAJOR", "MINOR", "PATCH"}


def check_sync_impact_format() -> None:
    """Every framework file with a `<!-- SYNC-IMPACT ...` HTML comment MUST
    carry the canonical fields per `principles-gates.md` Sync Impact Reports:
    version (from X.Y.Z → A.B.C), bump (MAJOR/MINOR/PATCH), date (YYYY-MM-DD),
    rationale (non-empty), and downstream_review_required (list or 'none').

    Vacuous for files without a SYNC-IMPACT block (pre-amendment state).
    """
    import datetime as _dt

    for path in (REPO_ROOT / "AGENTS.md", *sorted((REPO_ROOT / "playbooks").glob("*.md"))):
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if "SYNC-IMPACT" not in text[:2000]:
            continue  # no SYNC-IMPACT block in the file's top region

        rel = path.relative_to(REPO_ROOT)
        block = re.search(r"<!--\s*\n?\s*SYNC-IMPACT\n(.*?)-->", text, re.DOTALL)
        if not block:
            fail(f"[17/sync-impact] {rel}: SYNC-IMPACT marker present but "
                 f"no matching `<!--\\nSYNC-IMPACT ... -->` block found")
            continue
        body = block.group(1)

        fields: dict[str, str] = {}
        for line in body.splitlines():
            m = re.match(r"^-\s*([a-z_]+):\s*(.*)$", line)
            if m:
                fields[m.group(1)] = m.group(2).strip()

        for req in _SYNC_IMPACT_REQUIRED_FIELDS:
            if req not in fields:
                fail(f"[17/sync-impact] {rel}: SYNC-IMPACT missing required "
                     f"field '{req}'")

        ver = fields.get("version", "")
        if ver and not re.match(r"^\d+\.\d+\.\d+\s*(→|->)\s*\d+\.\d+\.\d+$", ver):
            fail(f"[17/sync-impact] {rel}: version {ver!r} is not in "
                 f"`X.Y.Z → A.B.C` form")

        bump = fields.get("bump", "")
        if bump and bump not in _SYNC_IMPACT_BUMP_VALUES:
            fail(f"[17/sync-impact] {rel}: bump {bump!r} must be one of "
                 f"{sorted(_SYNC_IMPACT_BUMP_VALUES)}")

        date = fields.get("date", "")
        if date:
            try:
                _dt.date.fromisoformat(date)
            except ValueError:
                fail(f"[17/sync-impact] {rel}: date {date!r} is not a valid "
                     f"YYYY-MM-DD")

        rationale = fields.get("rationale", "")
        if rationale and len(rationale) < 30:
            fail(f"[17/sync-impact] {rel}: rationale is too short "
                 f"({len(rationale)} chars) — cite specific rules affected")


def main() -> int:
    files = collect_frontmatter_files()
    check_frontmatter(files)
    check_references(files)
    check_tag_counts(files)
    check_state_schemas()
    check_claude_symlink()
    check_version_consistency(files)
    check_evidence_verifiability()
    check_derived_enumeration_parity()
    check_decision_alternatives_present()
    check_changelog_evidence_completeness()
    check_gap_entry_completeness()
    check_silent_deferral_phrases()
    check_sc_coverage_set()
    check_matrix_anchor_diversity()
    check_multi_agent_lock_validity()
    check_subsystem_ownership_present()
    check_sync_impact_format()

    if FAILURES:
        print(f"validate.py: {len(FAILURES)} failure(s)", file=sys.stderr)
        for msg in FAILURES:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    agents_fm, _ = parse_frontmatter(REPO_ROOT / "AGENTS.md")
    version = agents_fm["version"] if agents_fm else "?"
    playbook_count = sum(1 for f in files if f.name != "AGENTS.md")
    print(
        f"validate.py: all checks passed "
        f"(AGENTS.md + {playbook_count} playbooks, version {version})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
