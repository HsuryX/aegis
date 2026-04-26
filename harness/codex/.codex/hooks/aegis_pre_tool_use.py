#!/usr/bin/env python3
"""Codex hook template: block direct edits to protected aegis framework files.

This is a best-effort Codex-side backstop when installed in a real Codex hook
configuration. It does not replace OS permissions, CI, or git hooks, and it
does not cover every possible shell subprocess write path.

Framework maintainers can bypass this template by setting
`AEGIS_FRAMEWORK_MAINTENANCE=1` in the Codex process environment before the
session starts. The hook intentionally does not trust words inside the pending
tool payload as authorization.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import Any


PROTECTED_PATTERNS = (
    re.compile(r"(^|/)AGENTS\.md$"),
    re.compile(r"(^|/)CLAUDE\.md$"),
    re.compile(r"(^|/)playbooks/"),
    re.compile(r"(^|/)_legacy/"),
)

EDIT_TOOLS = {"apply_patch", "edit", "write", "notebookedit"}
PATH_KEYS = {"path", "file_path", "filename", "notebook_path", "target_file"}

def _walk_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        strings: list[str] = []
        for item in value.values():
            strings.extend(_walk_strings(item))
        return strings
    if isinstance(value, list):
        strings = []
        for item in value:
            strings.extend(_walk_strings(item))
        return strings
    return []


def _walk_path_values(value: Any) -> list[str]:
    if isinstance(value, dict):
        paths: list[str] = []
        for key, item in value.items():
            if key in PATH_KEYS and isinstance(item, str):
                paths.append(item)
            paths.extend(_walk_path_values(item))
        return paths
    if isinstance(value, list):
        paths = []
        for item in value:
            paths.extend(_walk_path_values(item))
        return paths
    return []


def _patch_target_paths(text: str) -> list[str]:
    if "*** Begin Patch" not in text:
        return []
    targets: list[str] = []
    for match in re.finditer(
        r"(?m)^\*\*\* (?:Add|Update|Delete) File:\s+(.+?)\s*$|^\*\*\* Move to:\s+(.+?)\s*$",
        text,
    ):
        targets.append((match.group(1) or match.group(2)).strip())
    return targets


def _repo_relative(path_text: str) -> str:
    path = Path(path_text)
    if not path.is_absolute():
        return path.as_posix()
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def _tool_name(payload: dict[str, Any]) -> str:
    for key in ("tool_name", "tool", "name"):
        value = payload.get(key)
        if isinstance(value, str):
            return value.lower()
    return ""


def _is_framework_maintenance(payload: dict[str, Any]) -> bool:
    return os.environ.get("AEGIS_FRAMEWORK_MAINTENANCE") == "1"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    tool = _tool_name(payload)
    if tool and tool not in EDIT_TOOLS:
        return 0

    if _is_framework_maintenance(payload):
        return 0

    candidate_paths = _walk_path_values(payload)
    for raw in _walk_strings(payload):
        candidate_paths.extend(_patch_target_paths(raw))

    for raw in candidate_paths:
        rel = _repo_relative(raw)
        if any(pattern.search(rel) for pattern in PROTECTED_PATTERNS):
            print(
                "aegis protected-file backstop: direct edits to AGENTS.md, "
                "CLAUDE.md, playbooks/, or _legacy/ require a maintainer-set "
                "AEGIS_FRAMEWORK_MAINTENANCE=1 environment override or redesign "
                "through the verdict process.",
                file=sys.stderr,
            )
            return int(os.environ.get("AEGIS_CODEX_HOOK_BLOCK_EXIT", "2"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
