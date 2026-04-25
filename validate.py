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
  4. State files in .agent-state/ begin with a <!-- SCHEMA: ... --> block,
     and `.agent-state/{phase,audit}.md` both carry valid matching
     `Lifecycle mode` values (`finite-delivery` or `steady-state`)
  5. CLAUDE.md is a symlink to AGENTS.md
  6. Version agrees across: AGENTS.md frontmatter, AGENTS.md body banner,
     every playbook frontmatter, and the top versioned CHANGELOG section.
  7. Every Evidence cell in every Verification Coverage Matrix block in
     .agent-state/phase.md (+ phase-archive.md if present) carries a
     verifiable reference per playbooks/principles-gates.md Verification Coverage Matrix: file.md:N,
     file.md#anchor, sha256:hex, #session-YYYY-MM-DD-slug, <subagent:NAME>,
     or literal "(pending)" when the row's Result cell is also pending.
     Prose-only cells fail.
  8. Derived-enumeration parity: cross-file lists that must agree — gap
     types (playbooks/gaps.md vs .agent-state/gaps.md vs skills/gap/SKILL.md),
     decision states (playbooks/01-design.md vs .agent-state/decisions.md
     vs skills/decision/SKILL.md), gate outcomes (playbooks/principles-gates.md
     vs ONBOARDING.md), and completion statuses (playbooks/principles.md vs
     ONBOARDING.md). Each concept has ONE canonical owner; every other location
     MUST carry the same set.
  9. Every Accepted or Final decision in .agent-state/decisions.md carries
     a non-empty "Alternatives considered:" field (placeholder text,
     empty, or literal "TBD" fails). Non-significant decisions MAY record
     "Alternatives considered: N/A — not significant" per the glossary.
     Vacuous when no decisions exist yet.
  10. CHANGELOG boundary discipline: CHANGELOG.md MUST stay semver
      taxonomy + release narrative. It MUST NOT restate amendment workflow via
      a `### Amendment workflow` section or `### Pre-Ship Self-Compliance
      Evidence` subsection; that workflow is canonical in
      playbooks/principles-gates.md.
 11. Gap entry completeness: no `Status: captured` entries MAY survive
     into a gate run (Quick Capture MUST be triaged to full `open` entries),
     every full (`open` or `resolved`) entry MUST carry the canonical baseline
     fields (Status, Severity, Type, Blocks, Description, Resolution path,
     Resolution, Date opened, Date resolved), resolved entries MUST populate
     Resolution + Date resolved, type-specific fields MUST exist for
     `deviation`, `conditional`, `scope-reduction`, and `grandfathered`
     entries, and silent severity changes relative to `gaps-archive.md`
     MUST be recorded in `Severity history` when the same `G-{n}` appears in
     both files. Vacuous on empty gap trackers.
 12. Silent-deferral banned-phrase scan: src/, tests/, specs/ (when
     present) MUST NOT contain marker phrases indicating silent scope
     reduction ("simplified version", "good enough for now", "coming in v2",
     etc.) UNLESS each hit has a corresponding open scope-reduction gap
     whose body cites the affected repo-relative file path.
  13. Phase-aware path-qualified SC set coverage: before Phase 3, declared
      `specs/<spec>.md:SC-{n}` identifiers may exist before tests/src coverage;
      in Phase 3, every declared SC identifier in specs/ MUST have at least one
      approved in-file comment form (`// Covers:` or `# Covers:` with the
      qualified SC) or equivalent `covers_<spec_path_slug>_SC_<n>` suffix in
      tests/ or src/. Set-based (not count-based) — prevents fake references
      from inflating counts.

 14. Multi-agent lock-file validity: when .agent-state/.lock-decisions
     exists, it MUST contain 4 required fields (agent_id, acquired_at,
     expected_duration_minutes, purpose) and `acquired_at` MUST be within
     the last 24 hours. Vacuous for single-agent sessions (no lock).
 15. Subsystem Ownership artifact placement: the validator MUST NOT
     broaden AGENTS.md applicability beyond its full AND-rule (scope
     standard/large AND >=2 subsystems AND >=3 distinct agents/team members).
     Because current state files do not encode those latter two counts
     canonically, this check rejects the stale pseudo-gap form
     (`Subsystem Ownership: N/A` in .agent-state/gaps.md) and, when a local
     .agent-state/phase.md note is present, requires the canonical N/A note
     shape (single-agent form or predicate-labeled exemption reason).
 16. SYNC-IMPACT format compliance: every framework file carrying a
     `<!-- SYNC-IMPACT ... -->` HTML comment MUST have version (X.Y.Z →
     A.B.C), bump (MAJOR|MINOR|PATCH), date (YYYY-MM-DD), rationale, and
     downstream_review_required fields per principles-gates.md. Non-empty
     downstream_review_required entries MUST resolve to existing repo-
     relative file paths. Catches format drift in future amendments.
 17. Framework amendment evidence bundle: every session anchor in
     `.agent-state/phase.md` that records a finite `#### Amendment evidence
     bundle` (or its canonical bundle-item markers) MUST satisfy the
     canonical pattern: authorization, semver + changed-file-set,
     per-file SYNC-IMPACT refs for changed canonical framework files,
     derived-doc sweep, validator pass, and a fresh-context review artifact
     for semantic (MINOR/MAJOR) amendments. When such a review artifact is
     cited, its archive file MUST satisfy the key schema checks from
     `.agent-state/reviews/README.md`.

check_7 (evidence verifiability) enforces full reference resolution:
file.md:N must be within file length; file.md#anchor must resolve to an
existing file; #session-YYYY-MM-DD-slug must exist in phase.md or
phase-archive.md; <subagent:NAME> must have an archived review at
.agent-state/reviews/*-NAME.md. See check_evidence_verifiability for
details.

Usage: python3 validate.py [--product-ship]
Exit 0 on clean, non-zero with a bulleted failure list otherwise.
Uses Python stdlib only — no external dependencies.

`--product-ship` preserves the product-ship mechanical checks while skipping
the amendment-lane-only checks 16-17 (SYNC-IMPACT format compliance and the
framework amendment evidence bundle).
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent
FAILURES: list[str] = []

_LIFECYCLE_MODE_VALUES = {"finite-delivery", "steady-state"}


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

    lifecycle_values: dict[str, str] = {}
    for state_file in ("phase.md", "audit.md"):
        state_path = state_dir / state_file
        rel = state_path.relative_to(REPO_ROOT)
        if not state_path.exists():
            fail(f"[4/lifecycle-mode] {rel}: required state file is missing")
            continue
        text = state_path.read_text(encoding="utf-8")
        match = re.search(r"(?m)^\*\*Lifecycle mode:\*\*\s*(.+?)\s*$", text)
        if not match:
            fail(f"[4/lifecycle-mode] {rel}: missing '**Lifecycle mode:**' field")
            continue
        value = match.group(1).strip()
        if value not in _LIFECYCLE_MODE_VALUES:
            fail(
                f"[4/lifecycle-mode] {rel}: Lifecycle mode {value!r} must be one of "
                f"{sorted(_LIFECYCLE_MODE_VALUES)}"
            )
            continue
        lifecycle_values[state_file] = value

    phase_mode = lifecycle_values.get("phase.md")
    audit_mode = lifecycle_values.get("audit.md")
    if phase_mode and audit_mode and phase_mode != audit_mode:
        fail(
            "[4/lifecycle-mode] .agent-state/phase.md and .agent-state/audit.md "
            f"must match, got {phase_mode!r} vs {audit_mode!r}"
        )


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
SESSION_BLOCK_RE = re.compile(
    r"(?ms)^### (session-\d{4}-\d{2}-\d{2}-[\w.-]+)\n(.*?)(?=^### |\Z)"
)
SEMVER_CLASS_RE = re.compile(r"\b(MAJOR|MINOR|PATCH)\b")
CANONICAL_FRAMEWORK_FILE_RE = re.compile(r"\b(?:AGENTS\.md|playbooks/[A-Za-z0-9_.-]+\.md)\b")


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
    """Enforce principles-gates.md Verification Coverage Matrix rules: every
    Evidence cell in every Verification Coverage Matrix block MUST carry a
    verifiable reference, not prose.

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
                    f"principles-gates.md requires a verifiable reference"
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
                    f"file.md:N | file.md#anchor | sha256:hex | "
                    f"#session-YYYY-MM-DD-slug | <subagent:NAME> | (pending)"
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
    m = re.search(r"`?Status`?\s*\((.+?)\)\s*[—-]", text)
    if not m:
        return set()
    states: set[str] = set()
    for piece in m.group(1).split("|"):
        name = piece.strip()
        if name:
            states.add(name)
    return states


def _extract_gate_outcomes_canonical() -> set[str]:
    """Extract gate outcomes from the Gate Outcome Vocabulary table in
    playbooks/principles-gates.md."""
    text = (REPO_ROOT / "playbooks" / "principles-gates.md").read_text(encoding="utf-8")
    outcomes: set[str] = set()
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.strip() == "## Gate Outcome Vocabulary"
            continue
        if not in_section:
            continue
        m = re.match(r"^\|\s*\*\*([^*]+)\*\*\s*\|", line)
        if m:
            outcomes.add(m.group(1).strip())
    return outcomes


def _extract_completion_statuses_canonical() -> set[str]:
    """Extract reporting statuses from playbooks/principles.md Completion
    Status Protocol."""
    text = (REPO_ROOT / "playbooks" / "principles.md").read_text(encoding="utf-8")
    statuses: set[str] = set()
    in_section = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.strip() == "## Completion Status Protocol"
            continue
        if not in_section:
            continue
        m = re.match(r"^- \*\*([A-Z_]+)\*\*\s*—", line)
        if m:
            statuses.add(m.group(1).strip())
    return statuses


def _extract_onboarding_backticked_set(label: str) -> set[str]:
    """Extract a backtick-enumerated set from a labeled ONBOARDING.md line."""
    path = REPO_ROOT / "ONBOARDING.md"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"(?m)^\*\*{re.escape(label)}\*\*.*?:\s*(.+)$", text)
    if not m:
        return set()
    listed = m.group(1).split(". See", 1)[0]
    return {token.strip() for token in re.findall(r"`([^`]+)`", listed) if token.strip()}


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
        (
            "gate outcomes",
            "playbooks/principles-gates.md (Gate Outcome Vocabulary)",
            _extract_gate_outcomes_canonical(),
            [
                ("ONBOARDING.md", _extract_onboarding_backticked_set("Gate outcomes")),
            ],
        ),
        (
            "completion statuses",
            "playbooks/principles.md (Completion Status Protocol)",
            _extract_completion_statuses_canonical(),
            [
                ("ONBOARDING.md", _extract_onboarding_backticked_set("Completion statuses")),
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


# --- check_10: CHANGELOG workflow de-duplication ------------------------


def check_changelog_workflow_boundary() -> None:
    """CHANGELOG.md owns semver taxonomy + release narrative only.

    Amendment workflow text lives in playbooks/principles-gates.md, so the
    changelog MUST NOT duplicate it via dedicated workflow headings or the
    retired recursive evidence subsection.
    """
    path = REPO_ROOT / "CHANGELOG.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")

    banned_headings = []
    if re.search(r"(?m)^###\s+Amendment workflow\s*$", text):
        banned_headings.append("### Amendment workflow")
    if re.search(r"(?m)^###\s+Pre-Ship Self-Compliance Evidence\s*$", text):
        banned_headings.append("### Pre-Ship Self-Compliance Evidence")

    if banned_headings:
        fail(
            "[10/changelog-boundary] CHANGELOG.md duplicates amendment workflow via "
            f"{', '.join(banned_headings)} — workflow belongs in "
            "playbooks/principles-gates.md; CHANGELOG.md should stay semver taxonomy + release narrative"
        )


# --- check_11: gap entry completeness (red-team #6) ----------------------

_GAP_FULL_REQUIRED_FIELDS = (
    "Status",
    "Severity",
    "Type",
    "Blocks",
    "Description",
    "Resolution path",
    "Resolution",
    "Date opened",
    "Date resolved",
)

_GAP_REQUIRED_VALUE_PLACEHOLDERS = {
    "",
    "TBD",
    "_(to be filled)_",
    "(to be filled)",
    "{to be filled}",
}

_GAP_LIFECYCLE_VALUES = {"captured", "open", "resolved"}
_GAP_SEVERITY_VALUES = {"critical", "non-critical"}


def _extract_gap_field(body: str, field: str) -> str | None:
    m = re.search(
        rf"\*\*{re.escape(field)}:\*\*\s*(.*?)(?=\n\*\*|\n###|\Z)",
        body,
        re.DOTALL,
    )
    if not m:
        return None
    return m.group(1).strip()


def _gap_field_has_required_value(body: str, field: str) -> bool:
    value = _extract_gap_field(body, field)
    if value is None:
        return False
    return value not in _GAP_REQUIRED_VALUE_PLACEHOLDERS and not value.startswith("{")


def _extract_audit_surface_names() -> set[str]:
    path = REPO_ROOT / ".agent-state" / "audit.md"
    if not path.exists():
        return set()
    text = path.read_text(encoding="utf-8")
    return {m.group(1).strip() for m in re.finditer(r"(?m)^###\s+([^\n]+)$", text)}


def _iter_gap_entries(text: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    pattern = re.compile(
        r"(?ms)^### (G-\d+):[^\n]*\n(.*?)(?=^### G-\d+:|^## |^---\s*$|\Z)"
    )
    for m in pattern.finditer(text):
        entries.append((m.group(1).strip(), m.group(2)))
    return entries


def _collect_gap_severities(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    severities: dict[str, str] = {}
    for gid, body in _iter_gap_entries(text):
        severity = _extract_gap_field(body, "Severity")
        if severity is None:
            continue
        severities[gid] = severity.splitlines()[0].strip().lower()
    return severities


def check_gap_entry_completeness() -> None:
    """Reject `Status: captured` at gate-run time and enforce the documented
    type-specific required fields for full gap entries.

    Vacuous when gaps.md has no `### G-{n}` entries (template state).
    """
    path = REPO_ROOT / ".agent-state" / "gaps.md"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    audit_surfaces = _extract_audit_surface_names()
    archive_severities = _collect_gap_severities(REPO_ROOT / ".agent-state" / "gaps-archive.md")
    canonical_gap_types = _extract_gap_types_canonical()
    severity_history_line_re = re.compile(
        r"^\d{4}-\d{2}-\d{2}:\s*(critical|non-critical)\s*→\s*"
        r"(critical|non-critical)\s*—\s*.+$"
    )

    for gid, body in _iter_gap_entries(text):
        status_value = _extract_gap_field(body, "Status")
        if status_value is None:
            continue
        status = status_value.splitlines()[0].strip()
        if status not in _GAP_LIFECYCLE_VALUES:
            fail(
                f"[11/gap-enum] gaps.md {gid}: Status value {status!r} must be one of "
                f"{sorted(_GAP_LIFECYCLE_VALUES)}"
            )
            continue
        if status == "captured":
            fail(
                f"[11/gap-triage] gaps.md {gid}: Status is 'captured' — "
                f"Quick Capture entries MUST be triaged to 'open' with full "
                f"SCHEMA fields before the next phase gate "
                f"(see playbooks/gaps.md Quick Capture)"
            )
            continue

        severity_value = _extract_gap_field(body, "Severity")
        severity = severity_value.splitlines()[0].strip() if severity_value else None
        if severity is not None and severity not in _GAP_SEVERITY_VALUES:
            fail(
                f"[11/gap-enum] gaps.md {gid}: Severity value {severity!r} must be one of "
                f"{sorted(_GAP_SEVERITY_VALUES)}"
            )

        if status in {"open", "resolved"}:
            for field in _GAP_FULL_REQUIRED_FIELDS:
                if not re.search(rf"\*\*{re.escape(field)}:\*\*", body):
                    fail(
                        f"[11/gap-completeness] gaps.md {gid}: Status={status} but "
                        f"required field '{field}' is missing"
                    )
            for field in ("Status", "Severity", "Type", "Blocks", "Description", "Resolution path", "Date opened"):
                if not _gap_field_has_required_value(body, field):
                    fail(
                        f"[11/gap-completeness] gaps.md {gid}: Status={status} requires "
                        f"a non-empty '{field}' field"
                    )
            blocks = _extract_gap_field(body, "Blocks")
            if blocks is not None:
                blocks_value = blocks.splitlines()[0].strip()
                if not re.fullmatch(r"phase advancement|nothing|D-\d+", blocks_value):
                    fail(
                        f"[11/gap-completeness] gaps.md {gid}: Blocks value "
                        f"{blocks_value!r} must be 'phase advancement', 'nothing', or 'D-{{n}}'"
                    )
            if status == "resolved":
                for field in ("Resolution", "Date resolved"):
                    if not _gap_field_has_required_value(body, field):
                        fail(
                            f"[11/gap-completeness] gaps.md {gid}: Status=resolved requires "
                            f"a non-empty '{field}' field"
                        )

        severity_history = _extract_gap_field(body, "Severity history")
        if severity_history is not None:
            history_lines = [line.strip() for line in severity_history.splitlines() if line.strip()]
            if not history_lines:
                fail(f"[11/gap-severity-history] gaps.md {gid}: 'Severity history' is blank")
            last_new_severity = None
            for line in history_lines:
                m = severity_history_line_re.fullmatch(line)
                if not m:
                    fail(
                        f"[11/gap-severity-history] gaps.md {gid}: history line {line!r} "
                        f"must match 'YYYY-MM-DD: old → new — justification'"
                    )
                    continue
                last_new_severity = m.group(2)
            if severity is not None and last_new_severity is not None and last_new_severity != severity:
                fail(
                    f"[11/gap-severity-history] gaps.md {gid}: current Severity={severity!r} "
                    f"does not match last Severity history target {last_new_severity!r}"
                )
        archived_severity = archive_severities.get(gid)
        if archived_severity and severity is not None and archived_severity != severity:
            if severity_history is None:
                fail(
                    f"[11/gap-severity-history] gaps.md {gid}: Severity changed from archive "
                    f"{archived_severity!r} to current {severity!r} without a 'Severity history' field"
                )

        gap_type = _extract_gap_field(body, "Type")
        if gap_type is None or status not in {"open", "resolved"}:
            continue
        gap_type_normalized = gap_type.splitlines()[0].strip()
        if gap_type_normalized not in canonical_gap_types:
            fail(
                f"[11/gap-enum] gaps.md {gid}: Type value {gap_type_normalized!r} must be one of "
                f"{sorted(canonical_gap_types)}"
            )
            continue

        def require_type_field(field: str) -> None:
            if _gap_field_has_required_value(body, field):
                return
            fail(
                f"[11/gap-type] gaps.md {gid}: Type={gap_type_normalized} requires "
                f"a non-empty '{field}' field"
            )

        if gap_type_normalized == "deviation":
            require_type_field("Expiry condition")
        elif gap_type_normalized == "conditional":
            require_type_field("Trigger condition")
            linked_verdict = _extract_gap_field(body, "Linked verdict")
            if linked_verdict is not None:
                if not _gap_field_has_required_value(body, "Linked verdict"):
                    fail(
                        f"[11/gap-type] gaps.md {gid}: Type=conditional has a blank "
                        f"'Linked verdict' field"
                    )
                elif audit_surfaces and linked_verdict not in audit_surfaces:
                    fail(
                        f"[11/gap-type] gaps.md {gid}: Linked verdict {linked_verdict!r} "
                        f"does not match any audit surface {sorted(audit_surfaces)}"
                    )
        elif gap_type_normalized == "scope-reduction":
            require_type_field("Trigger condition")
        elif gap_type_normalized == "grandfathered":
            require_type_field("Expiry condition")
            require_type_field("Initial artifact set")


# --- check_12: silent-deferral banned-phrase scan (red-team #12) ---------

_DEFERRAL_PHRASES = (
    "simplified version",
    "static for now",
    "defer to follow-up",
    "good enough for now",
    "stub for the moment",
    "coming in v2",
)

_DEFERRAL_SCAN_DIRS = (
    "src",
    "tests",
    "specs",
)


def check_silent_deferral_phrases() -> None:
    """Grep src/, tests/, specs/ (when present) for banned marker phrases
    indicating silent scope reduction. Any hit MUST have a matching
    `scope-reduction` gap open in .agent-state/gaps.md whose body cites the
    affected repo-relative file path, otherwise fail.

    Vacuous when none of the scanned dirs exist (spec-only projects like
    aegis itself).
    """
    # Collect open scope-reduction gap bodies keyed by G-id. A hit is exempt
    # only when a gap body cites the affected repo-relative file path.
    gaps_path = REPO_ROOT / ".agent-state" / "gaps.md"
    scope_reduction_gaps: dict[str, str] = {}
    if gaps_path.exists():
        gtext = gaps_path.read_text(encoding="utf-8")
        for gid, body in _iter_gap_entries(gtext):
            if re.search(r"\*\*Type:\*\*\s*scope-reduction\b", body):
                if re.search(r"\*\*Status:\*\*\s*open\b", body):
                    scope_reduction_gaps[gid] = body.lower()

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
                        rel_path = rel.as_posix().lower()
                        matching_gaps = [
                            gid for gid, gap_body in scope_reduction_gaps.items()
                            if rel_path in gap_body
                        ]
                        if matching_gaps:
                            break
                        fail(
                            f"[12/deferral] {rel}:{lineno} contains banned "
                            f"deferral phrase {phrase!r} — add an open "
                            f"scope-reduction gap that cites {rel} OR remove the "
                            f"phrase (see playbooks/03-implement.md Hard "
                            f"Rule 3)"
                        )
                        break


# --- check_13: path-qualified SC set coverage (red-team #7) --------------

def _spec_path_slug(rel_path: str) -> str:
    """Lowercase rel_path, replace every non-alphanumeric char with `_`, and strip leading/trailing `_`."""
    return re.sub(r"[^A-Za-z0-9]+", "_", rel_path).strip("_").lower()


def _current_phase_slug() -> str:
    """Return the current phase slug from `.agent-state/phase.md`, or empty when unavailable."""
    phase_path = REPO_ROOT / ".agent-state" / "phase.md"
    try:
        text = phase_path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    m = re.search(r"(?m)^\*\*Current phase:\*\*\s*([^\n]+?)\s*$", text)
    return m.group(1).strip() if m else ""


def check_sc_coverage_set() -> None:
    """Every declared `specs/<spec>.md:SC-{n}` identifier in specs/ MUST be
    referenced by at least one approved in-file comment form (`// Covers:` or
    `# Covers:` with the qualified SC) or equivalent
    `covers_<spec_path_slug>_SC_<n>` suffix in tests/ or src/, where
    `<spec_path_slug>` lowercases the spec path, replaces every non-alphanumeric
    character with `_`, and strips leading/trailing `_`.

    Set-based — count-based satisfaction (N fake references to one SC) passes
    the count check but fails the set check.

    Vacuous when specs/ does not exist, and intentionally skipped before Phase 3
    because spec-quality phases may declare `SC-{n}` before implementation/test
    artifacts exist.
    """
    specs_dir = REPO_ROOT / "specs"
    if not specs_dir.is_dir():
        return

    if _current_phase_slug() in {"0-audit", "1-design", "2-spec"}:
        return

    declared_suffixes: dict[str, str] = {}
    for md in specs_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = md.relative_to(REPO_ROOT).as_posix()
        slug = _spec_path_slug(rel)
        # Declared SCs may appear as plain `SC-N:` conformance lines or the
        # equivalent heading / bullet forms.
        for m in re.finditer(r"(?m)^(?:###\s+|[-*]\s+)?(SC-\d+)(?::|\b)", text):
            sc_id = m.group(1)
            declared_suffixes[f"{rel}:{sc_id}"] = (
                f"covers_{slug}_{sc_id.replace('-', '_').lower()}"
            )

    if not declared_suffixes:
        return

    covered: set[str] = set()
    comment_ref_re = re.compile(
        r"(?m)^\s*(?://|#)\s*Covers:\s*(specs/[A-Za-z0-9_./-]+\.md:SC-\d+)\b"
    )
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
            lower_text = text.lower()
            for m in comment_ref_re.finditer(text):
                covered.add(m.group(1))
            for qualified_ref, suffix_token in declared_suffixes.items():
                if re.search(rf"\b{re.escape(suffix_token)}\b", lower_text):
                    covered.add(qualified_ref)

    missing = set(declared_suffixes) - covered
    if missing:
        fail(
            f"[13/sc-coverage] {len(missing)} declared path-qualified "
            f"SC identifier(s) have zero approved comment/suffix traceability references in "
            f"tests/ or src/: {', '.join(sorted(missing))}"
        )

# --- check_19: traceability metric (file-level rollup) -------------------

_TRACEABILITY_SCAN_DIRS = (
    "src",
    "tests",
)

_TRACEABILITY_FILE_SUFFIXES = (
    ".py", ".md", ".ts", ".js", ".go", ".rs",
    ".java", ".kt", ".swift", ".cpp", ".c",
    ".h", ".rb", ".php", ".cs",
)

_TRACEABILITY_PATTERNS = (
    re.compile(r"(?m)^\s*(?://|#)\s*Implements:\s*(?:D-\d+|specs/[^\s,:]+\.md:(?:FR|NFR)-\d+)"),
    re.compile(r"(?m)^\s*(?://|#)\s*Covers:\s*specs/[^\s,:]+\.md:(?:SC|FR)-\d+"),
    re.compile(r"\bcovers_[A-Za-z0-9_]+_(?:SC|FR)_\d+\b"),
)

_TRACEABILITY_THRESHOLD_PCT = 80.0


def check_traceability() -> None:
    """File-level rollup of traceability coverage. Counts files in src/ and
    tests/ that carry at least one Implements:/Covers: trailer comment or
    `covers_*` test-name suffix, and reports the ratio. Emits a stderr
    warning (NOT a failure) when the ratio is below 80%.

    Vacuous when neither src/ nor tests/ exist (true of the framework repo
    itself before downstream adoption, and true of spec-only projects).

    The traceability *requirement* lives in `playbooks/03-implement.md`
    Traceability and `playbooks/identifiers.md` Commit Trailer Forms; this
    check makes the requirement audit-able. Per-SC strict coverage
    enforcement is owned by `check_sc_coverage_set` (check 13), which
    DOES fail; this check is a complementary file-level rollup that
    surfaces neglect, not duplicate enforcement.
    """
    total_files = 0
    traced_files = 0
    for scan_dir in _TRACEABILITY_SCAN_DIRS:
        d = REPO_ROOT / scan_dir
        if not d.is_dir():
            continue
        for path in d.rglob("*"):
            if not path.is_file():
                continue
            if path.suffix not in _TRACEABILITY_FILE_SUFFIXES:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            total_files += 1
            for pattern in _TRACEABILITY_PATTERNS:
                if pattern.search(text):
                    traced_files += 1
                    break

    if total_files == 0:
        return  # vacuous: no implementation/test code to scan

    pct = 100.0 * traced_files / total_files
    if pct < _TRACEABILITY_THRESHOLD_PCT:
        print(
            f"[19/traceability] WARNING: {traced_files} of {total_files} scanned "
            f"files in src/, tests/ carry Implements:/Covers: references "
            f"({pct:.1f}%); below the {_TRACEABILITY_THRESHOLD_PCT:.0f}% threshold. "
            f"Review trailer/comment coverage per playbooks/03-implement.md "
            f"Traceability.",
            file=sys.stderr,
        )
    else:
        print(
            f"validate.py: traceability — {traced_files} of {total_files} "
            f"scanned files carry Implements:/Covers: references ({pct:.1f}%)"
        )


# --- check_14: multi-agent lock-file validity (red-team #5) --------------

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


def _is_single_sentence_reason(reason: str) -> bool:
    trimmed = reason.strip()
    if not trimmed:
        return False
    core = trimmed[:-1].rstrip() if trimmed[-1] in '.!?' else trimmed
    return bool(core) and not any(ch in core for ch in '.!?')



def _is_canonical_subsystem_ownership_note(line: str) -> bool:
    match = re.fullmatch(r'Subsystem Ownership:\s*N/A\s+—\s+(.+)', line)
    if not match:
        return False

    reason = match.group(1).strip()
    if not _is_single_sentence_reason(reason):
        return False

    core = reason[:-1].rstrip() if reason.endswith(('.', '!', '?')) else reason
    if 'single-agent project;' in core:
        owner_parts = core.split('all subsystems owned by', 1)
        return len(owner_parts) == 2 and bool(owner_parts[1].strip())

    return bool(re.search(r'\([abc]\)', core))


# --- check_15: Subsystem Ownership artifact placement (red-team #13) ------

def check_subsystem_ownership_present() -> None:
    """Validate Subsystem Ownership artifact placement without broadening
    AGENTS.md applicability. The canonical rule depends on three predicates:
    scope in {standard, large}, >=2 subsystems, and >=3 distinct agents or
    team members. Because the current state files do not encode the latter two
    counts canonically, this check MUST NOT fail solely from scope. It rejects
    the stale pseudo-gap form in .agent-state/gaps.md and validates any local
    phase.md N/A note against the canonical shape requirements: one sentence
    naming the absent predicate(s), or the explicit single-agent form.
    """
    gaps_path = REPO_ROOT / '.agent-state' / 'gaps.md'
    gaps_text = gaps_path.read_text(encoding='utf-8') if gaps_path.exists() else ''
    phase_path = REPO_ROOT / '.agent-state' / 'phase.md'
    phase_text = phase_path.read_text(encoding='utf-8') if phase_path.exists() else ''

    if re.search(r'Subsystem Ownership:\s*N/A', gaps_text, re.IGNORECASE):
        fail(
            '[16/subsystem-ownership] stale pseudo-gap found in .agent-state/gaps.md — '
            'Subsystem Ownership exemptions belong in .agent-state/phase.md Handoff Context per AGENTS.md'
        )

    for match in re.finditer(r'^Subsystem Ownership:.*$', phase_text, re.MULTILINE):
        line = match.group(0).strip()
        if _is_canonical_subsystem_ownership_note(line):
            continue
        fail(
            '[16/subsystem-ownership] non-canonical note in .agent-state/phase.md — '
            'use a one-sentence `Subsystem Ownership: N/A — ...` note that either '
            'names the absent applicability predicate(s) as `(a)`/`(b)`/`(c)` or uses '
            'the explicit single-agent form `single-agent project; all subsystems owned by {agent}`'
        )


# --- check_16: SYNC-IMPACT format compliance (Phase E whole-project) ----

_SYNC_IMPACT_REQUIRED_FIELDS = ("version", "bump", "date", "rationale", "downstream_review_required")
_SYNC_IMPACT_BUMP_VALUES = {"MAJOR", "MINOR", "PATCH"}


def _is_valid_repo_relative_file_path(path_text: str) -> bool:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return False
    resolved = (REPO_ROOT / candidate).resolve()
    try:
        resolved.relative_to(REPO_ROOT.resolve())
    except ValueError:
        return False
    return resolved.exists() and resolved.is_file()


def _parse_sync_impact_fields(body: str) -> dict[str, str | list[str]]:
    fields: dict[str, str | list[str]] = {}
    current_list_field: str | None = None

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        field_match = re.match(r"^-\s*([a-z_]+):\s*(.*)$", line)
        if field_match:
            key, value = field_match.group(1), field_match.group(2).strip()
            current_list_field = None
            if key == "downstream_review_required":
                if value in {"", "[]"}:
                    fields[key] = []
                    if value == "":
                        current_list_field = key
                else:
                    fields[key] = [value]
            else:
                fields[key] = value
            continue

        if current_list_field == "downstream_review_required":
            item_match = re.match(r"^\s*-\s*(.+?)\s*$", line)
            if item_match:
                current_value = fields.setdefault(current_list_field, [])
                if isinstance(current_value, list):
                    current_value.append(item_match.group(1).strip())
                continue
            if line.strip():
                current_list_field = None

    return fields


def check_sync_impact_format() -> None:
    """Every framework file with a `<!-- SYNC-IMPACT ...` HTML comment MUST
    carry the canonical fields per `principles-gates.md` Sync Impact Reports:
    version (from X.Y.Z → A.B.C), bump (MAJOR/MINOR/PATCH), date (YYYY-MM-DD),
    rationale, and downstream_review_required (list field; empty list allowed).
    Non-empty downstream_review_required entries MUST be valid repo-relative
    file paths.

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
                 f"no matching `<!--\nSYNC-IMPACT ... -->` block found")
            continue
        body = block.group(1)

        fields = _parse_sync_impact_fields(body)

        for req in _SYNC_IMPACT_REQUIRED_FIELDS:
            if req not in fields:
                fail(f"[17/sync-impact] {rel}: SYNC-IMPACT missing required "
                     f"field '{req}'")

        ver = fields.get("version", "")
        if isinstance(ver, str) and ver and not re.match(r"^\d+\.\d+\.\d+\s*(→|->)\s*\d+\.\d+\.\d+$", ver):
            fail(f"[17/sync-impact] {rel}: version {ver!r} is not in "
                 f"`X.Y.Z → A.B.C` form")

        bump = fields.get("bump", "")
        if isinstance(bump, str) and bump and bump not in _SYNC_IMPACT_BUMP_VALUES:
            fail(f"[17/sync-impact] {rel}: bump {bump!r} must be one of "
                 f"{sorted(_SYNC_IMPACT_BUMP_VALUES)}")

        date = fields.get("date", "")
        if isinstance(date, str) and date:
            try:
                _dt.date.fromisoformat(date)
            except ValueError:
                fail(f"[17/sync-impact] {rel}: date {date!r} is not a valid "
                     f"YYYY-MM-DD")

        rationale = fields.get("rationale", "")
        if isinstance(rationale, str) and rationale and len(rationale) < 30:
            fail(f"[17/sync-impact] {rel}: rationale is too short "
                 f"({len(rationale)} chars) — cite specific rules affected")

        downstream_paths = fields.get("downstream_review_required")
        if isinstance(downstream_paths, list):
            for entry in downstream_paths:
                if entry and not _is_valid_repo_relative_file_path(entry):
                    fail(
                        f"[17/sync-impact] {rel}: downstream_review_required entry "
                        f"{entry!r} must be an existing repo-relative file path"
                    )


def _first_resolvable_evidence_ref(
    value: str, *, phase_text: str, phase_archive_text: str = ""
) -> str | None:
    refs = [ref.strip() for ref in EVIDENCE_ANCHOR_EXTRACT.findall(value) if ref.strip()]
    if not refs:
        candidate = value.strip()
        if any(p.match(candidate) for p in EVIDENCE_PATTERNS):
            refs = [candidate]
    for ref in refs:
        if ref == "(pending)":
            continue
        if not any(p.match(ref) for p in EVIDENCE_PATTERNS):
            continue
        if _resolve_evidence_reference(
            ref, phase_text=phase_text, phase_archive_text=phase_archive_text
        ) is None:
            return ref
    return None



# --- check_17: framework amendment evidence bundle ------------------------

def _extract_evidence_refs(value: str) -> list[str]:
    refs = [ref.strip() for ref in EVIDENCE_ANCHOR_EXTRACT.findall(value) if ref.strip()]
    if refs:
        return [ref for ref in refs if any(p.match(ref) for p in EVIDENCE_PATTERNS)]
    candidate = value.strip()
    if any(p.match(candidate) for p in EVIDENCE_PATTERNS):
        return [candidate]
    return []


def _parse_file_line_ref(ref: str) -> tuple[str, int] | None:
    m = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)$", ref)
    if not m:
        return None
    return m.group(1), int(m.group(2))


def _parse_file_anchor_ref(ref: str) -> tuple[str, str] | None:
    m = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)#([\w.-]+)$", ref)
    if not m:
        return None
    return m.group(1), m.group(2)


def _sync_impact_top_comment_line_range(rel_path: str) -> tuple[int, int] | None:
    path = REPO_ROOT / rel_path
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    block = re.match(r"\A<!--\s*\n?\s*SYNC-IMPACT\n.*?-->", text, re.DOTALL)
    if not block:
        return None
    return 1, len(block.group(0).splitlines())


def _review_artifact_ref_path(ref: str) -> str | None:
    file_line = _parse_file_line_ref(ref)
    if file_line:
        rel_path, _ = file_line
        path = REPO_ROOT / rel_path
        if (
            rel_path.startswith(".agent-state/reviews/")
            and rel_path != ".agent-state/reviews/README.md"
            and path.exists()
        ):
            return rel_path
        return None

    file_anchor = _parse_file_anchor_ref(ref)
    if file_anchor:
        rel_path, anchor = file_anchor
        path = REPO_ROOT / rel_path
        if (
            rel_path.startswith(".agent-state/reviews/")
            and rel_path != ".agent-state/reviews/README.md"
            and path.exists()
        ):
            text = path.read_text(encoding="utf-8", errors="replace")
            if _extract_markdown_section(text, anchor):
                return rel_path
        return None

    return None


def _markdown_slug(heading: str) -> str:
    slug = heading.strip().lower()
    slug = re.sub(r"\s+#+$", "", slug)
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug.strip("-")


def _extract_markdown_section(text: str, anchor: str) -> str:
    lines = text.splitlines()
    collected: list[str] = []
    active_level: int | None = None
    for line in lines:
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            level = len(m.group(1))
            heading = m.group(2).strip()
            if active_level is not None and level <= active_level:
                break
            if _markdown_slug(heading) == anchor:
                collected = [line]
                active_level = level
                continue
        if active_level is not None:
            collected.append(line)
    return "\n".join(collected)


CANONICAL_REVIEW_SEVERITIES = {"CRITICAL", "HIGH", "MEDIUM", "LOW"}
REVIEW_JUSTIFICATION_CLASSES = {
    "ALREADY_SPECIFIED",
    "OUT_OF_SCOPE_NG-n",
    "RISK_ACCEPTED_BY_USER",
}


def _validate_review_archive_artifact(rel_path: str, *, session_anchor: str) -> None:
    """Validate the key review-archive schema expectations used by the
    amendment-lane fresh-context review contract.

    This is intentionally bounded to the auditable requirements in
    `.agent-state/reviews/README.md`, not a free-form content review.
    """
    path = REPO_ROOT / rel_path
    if not path.exists():
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} does not exist"
        )
        return

    text = path.read_text(encoding="utf-8", errors="replace")
    ordered_headings = (
        "### Metadata",
        "### Reviewer prompt",
        "### Subagent response",
        "### Disposition",
    )
    previous = -1
    for heading in ordered_headings:
        idx = text.find(heading)
        if idx == -1:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} is missing required section {heading!r}"
            )
            return
        if idx < previous:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} has out-of-order section {heading!r}"
            )
            return
        previous = idx

    metadata = _extract_markdown_section(text, "metadata")
    prompt = _extract_markdown_section(text, "reviewer-prompt")
    response = _extract_markdown_section(text, "subagent-response")
    disposition = _extract_markdown_section(text, "disposition")
    for name, section in (
        ("metadata", metadata),
        ("reviewer prompt", prompt),
        ("subagent response", response),
        ("disposition", disposition),
    ):
        if not section.strip():
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} has an empty {name} section"
            )
            return

    for label in (
        "- Date (UTC):",
        "- Phase:",
        "- Scope classification:",
        "- Model identifier:",
        "- Cited from:",
    ):
        if label not in metadata:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} metadata is missing {label!r}"
            )

    if session_anchor not in metadata or (
        f".agent-state/phase.md#{session_anchor}" not in metadata
        and f".agent-state/phase-archive.md#{session_anchor}" not in metadata
    ):
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} must cite `.agent-state/phase.md#{session_anchor}` (or phase-archive) in metadata"
        )

    if prompt.count("```") < 2:
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} reviewer prompt must preserve a verbatim fenced prompt block"
        )
    prompt_lower = prompt.lower()
    if "directly affected derived guidance" not in prompt_lower:
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} reviewer prompt must explicitly include directly affected derived guidance in scope"
        )
    if "if needed" in prompt_lower:
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} reviewer prompt uses non-canonical conditional scope wording ('if needed')"
        )

    if "| INFO |" in text or "(INFO" in text:
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} uses non-canonical severity `INFO`; use only CRITICAL/HIGH/MEDIUM/LOW"
        )

    if (
        "| Finding | Severity | Disposition | Citation | Severity-matched escalation check |"
        not in disposition
    ):
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} disposition section must include the canonical audit table header"
        )
        return

    row_count = 0
    for line in disposition.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if len(cells) < 5:
            continue
        if all(set(c) <= set("-:") or c == "" for c in cells):
            continue
        if cells[0] == "Finding":
            continue
        if not cells[0].startswith("F-"):
            continue
        row_count += 1
        severity = cells[1]
        disposition_value = cells[2]
        citation = cells[3]
        if severity not in CANONICAL_REVIEW_SEVERITIES:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} row {cells[0]!r} uses non-canonical severity {severity!r}"
            )
        if not citation:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} row {cells[0]!r} has an empty citation cell"
            )
        if (
            disposition_value not in REVIEW_JUSTIFICATION_CLASSES
            and _parse_file_line_ref(disposition_value) is None
            and _parse_file_anchor_ref(disposition_value) is None
        ):
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} row {cells[0]!r} has non-canonical disposition {disposition_value!r}"
            )
        if severity in {"CRITICAL", "HIGH"} and disposition_value in {
            "ALREADY_SPECIFIED",
            "OUT_OF_SCOPE_NG-n",
        }:
            fail(
                f"[18/amendment-bundle] review artifact {rel_path!r} row {cells[0]!r} violates severity-matched escalation; {severity} findings resolved by [J] must use RISK_ACCEPTED_BY_USER"
            )

    if row_count == 0:
        fail(
            f"[18/amendment-bundle] review artifact {rel_path!r} disposition section has no finding rows"
        )


def _evidence_ref_text(ref: str, *, phase_text: str, phase_archive_text: str = "") -> str:
    file_line = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)$", ref)
    if file_line:
        path = REPO_ROOT / file_line.group(1)
        if not path.exists():
            return ""
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        line_no = int(file_line.group(2))
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return ""

    file_anchor = re.match(r"^([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)#([\w.-]+)$", ref)
    if file_anchor:
        path = REPO_ROOT / file_anchor.group(1)
        if not path.exists():
            return ""
        text = path.read_text(encoding="utf-8", errors="replace")
        return _extract_markdown_section(text, file_anchor.group(2)) or text

    session_anchor = re.match(r"^#(session-\d{4}-\d{2}-\d{2}-[\w.-]+)$", ref)
    if session_anchor:
        anchor = session_anchor.group(1)
        for haystack in (phase_text, phase_archive_text):
            for match in SESSION_BLOCK_RE.finditer(haystack):
                if match.group(1) == anchor:
                    return match.group(0)
        return ""

    return ""


def _bundle_context_text(value: str, *, phase_text: str, phase_archive_text: str = "") -> str:
    parts = [value]
    for ref in _extract_evidence_refs(value):
        detail = _evidence_ref_text(ref, phase_text=phase_text, phase_archive_text=phase_archive_text)
        if detail:
            parts.append(detail)
    return "\n".join(parts)


def check_framework_amendment_evidence_bundles() -> None:
    """Validate canonical finite amendment evidence bundles in phase.md.

    The bundle shape is owned by playbooks/principles-gates.md Amendment
    Protocol. This check enforces the bounded bundle once per amendment and
    does not reintroduce the retired recursive ritual.
    """
    phase_path = REPO_ROOT / ".agent-state" / "phase.md"
    if not phase_path.exists():
        return
    phase_text = phase_path.read_text(encoding="utf-8")
    phase_archive_text = ""
    phase_archive_path = REPO_ROOT / ".agent-state" / "phase-archive.md"
    if phase_archive_path.exists():
        phase_archive_text = phase_archive_path.read_text(encoding="utf-8")

    bundle_markers = (
        "#### Amendment evidence bundle",
        "- Authorization / user directive:",
        "- Semver classification + changed file set:",
        "- Canonical framework SYNC-IMPACT refs:",
        "- Diff-scoped derived-doc sweep:",
        "- Validator pass:",
        "- Fresh-context review artifact:",
    )
    required_labels = (
        "Authorization / user directive",
        "Semver classification + changed file set",
        "Canonical framework SYNC-IMPACT refs",
        "Diff-scoped derived-doc sweep",
        "Validator pass",
    )

    for session_anchor, block in SESSION_BLOCK_RE.findall(phase_text):
        if not any(marker in block for marker in bundle_markers):
            continue

        if "#### Amendment evidence bundle" not in block:
            fail(
                f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                "missing `#### Amendment evidence bundle`"
            )
            continue

        bundle_items: dict[str, str | None] = {label: None for label in required_labels}
        for label in required_labels:
            item_match = re.search(rf"(?m)^- {re.escape(label)}:\s*(.+)$", block)
            if not item_match:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    f"missing bundle item {label!r}"
                )
                continue
            bundle_items[label] = item_match.group(1).strip()

        review_match = re.search(r"(?m)^- Fresh-context review artifact:\s*(.+)$", block)
        review_value = review_match.group(1).strip() if review_match else None

        for label in required_labels:
            value = bundle_items.get(label)
            if not value:
                continue
            ref = _first_resolvable_evidence_ref(
                value,
                phase_text=phase_text,
                phase_archive_text=phase_archive_text,
            )
            if ref is None:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    f"bundle item {label!r} needs a resolvable evidence reference"
                )

        semver_value = bundle_items.get("Semver classification + changed file set")
        semver_class: str | None = None
        changed_canonical_files: set[str] = set()
        if semver_value:
            semver_context = _bundle_context_text(
                semver_value,
                phase_text=phase_text,
                phase_archive_text=phase_archive_text,
            )
            semver_match = SEMVER_CLASS_RE.search(semver_context)
            if not semver_match:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "semver bundle item must classify the amendment as MAJOR, MINOR, or PATCH"
                )
            else:
                semver_class = semver_match.group(1)

            changed_canonical_files = set(CANONICAL_FRAMEWORK_FILE_RE.findall(semver_context))
            if not changed_canonical_files:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "semver bundle item must name at least one changed canonical framework file"
                )

        sync_value = bundle_items.get("Canonical framework SYNC-IMPACT refs")
        referenced_sync_files: set[str] = set()
        if sync_value:
            sync_refs = _extract_evidence_refs(sync_value)
            if not sync_refs:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "SYNC-IMPACT bundle item needs at least one resolvable evidence reference"
                )
            for ref in sync_refs:
                err = _resolve_evidence_reference(
                    ref,
                    phase_text=phase_text,
                    phase_archive_text=phase_archive_text,
                )
                if err is not None:
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"SYNC-IMPACT ref {ref!r} is not resolvable: {err}"
                    )
                    continue

                file_line = _parse_file_line_ref(ref)
                if not file_line:
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"SYNC-IMPACT ref {ref!r} must be a file:line reference into the changed file's leading SYNC-IMPACT comment"
                    )
                    continue

                rel_path, line_no = file_line
                if rel_path not in changed_canonical_files:
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"SYNC-IMPACT ref {ref!r} points to {rel_path!r}, which is not a changed canonical framework file"
                    )
                    continue

                sync_range = _sync_impact_top_comment_line_range(rel_path)
                if sync_range is None:
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"changed canonical file {rel_path!r} does not start with a SYNC-IMPACT comment"
                    )
                    continue

                start_line, end_line = sync_range
                if not (start_line <= line_no <= end_line):
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"SYNC-IMPACT ref {ref!r} must point into {rel_path!r}'s leading SYNC-IMPACT comment (lines {start_line}-{end_line})"
                    )
                    continue

                referenced_sync_files.add(rel_path)

            for changed_file in sorted(changed_canonical_files):
                if changed_file not in referenced_sync_files:
                    fail(
                        f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                        f"SYNC-IMPACT bundle item missing ref for changed canonical file {changed_file!r}"
                    )

        review_refs = _extract_evidence_refs(review_value) if review_value else []
        review_artifact_paths = {
            path for ref in review_refs if (path := _review_artifact_ref_path(ref))
        }

        if semver_class in {"MAJOR", "MINOR"}:
            if not review_value:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "semantic framework amendment requires a fresh-context review artifact"
                )
            elif "N/A" in review_value:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "semantic framework amendment requires a fresh-context review artifact reference"
                )
            elif not review_artifact_paths:
                fail(
                    f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                    "fresh-context review item must cite an archived review artifact under .agent-state/reviews/"
                )
        elif review_value and "N/A" not in review_value and not review_artifact_paths:
            fail(
                f"[18/amendment-bundle] .agent-state/phase.md {session_anchor}: "
                "fresh-context review item must cite an archived review artifact under .agent-state/reviews/"
            )

        for rel_path in sorted(review_artifact_paths):
            _validate_review_archive_artifact(
                rel_path,
                session_anchor=session_anchor,
            )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Mechanical validator for aegis.")
    parser.add_argument(
        "--product-ship",
        action="store_true",
        help="run product-ship checks only (skips amendment-lane-only checks 17-18)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    FAILURES.clear()
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
    check_changelog_workflow_boundary()
    check_gap_entry_completeness()
    check_silent_deferral_phrases()
    check_sc_coverage_set()
    check_traceability()
    check_multi_agent_lock_validity()
    check_subsystem_ownership_present()
    if not args.product_ship:
        check_sync_impact_format()
        check_framework_amendment_evidence_bundles()

    if FAILURES:
        prefix = "validate.py (--product-ship)" if args.product_ship else "validate.py"
        print(f"{prefix}: {len(FAILURES)} failure(s)", file=sys.stderr)
        for msg in FAILURES:
            print(f"  - {msg}", file=sys.stderr)
        return 1

    agents_fm, _ = parse_frontmatter(REPO_ROOT / "AGENTS.md")
    version = agents_fm["version"] if agents_fm else "?"
    playbook_count = sum(1 for f in files if f.name != "AGENTS.md")
    if args.product_ship:
        print(
            f"validate.py: all applicable checks passed "
            f"(product-ship mode; skipped checks 17-18, AGENTS.md + {playbook_count} playbooks, version {version})"
        )
    else:
        print(
            f"validate.py: all checks passed "
            f"(AGENTS.md + {playbook_count} playbooks, version {version})"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
