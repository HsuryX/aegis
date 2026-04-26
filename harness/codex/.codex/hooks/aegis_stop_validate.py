#!/usr/bin/env python3
"""Codex hook template: run aegis validation before stop/completion.

Wire to Codex Stop or equivalent completion events after copying this template
into the active `.codex/` configuration area. The hook is intentionally bounded
to `python3 validate.py`; project build/test commands remain project-specific.

Stop hooks must not emit plain text on stdout. This script writes validation
details to stderr on failure, leaves stdout empty on success, and exits with a
Codex blocking status on validation failure.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def _block_exit_code() -> int:
    try:
        return int(os.environ.get("AEGIS_CODEX_HOOK_BLOCK_EXIT", "2"))
    except ValueError:
        return 2


def main() -> int:
    validator = Path("validate.py")
    if not validator.exists():
        return 0

    result = subprocess.run(
        [sys.executable, "validate.py"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        print(
            "aegis stop validation failed; fix validate.py failures before completion.",
            file=sys.stderr,
        )
        if result.stdout:
            print(result.stdout, end="", file=sys.stderr)
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        return _block_exit_code()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
