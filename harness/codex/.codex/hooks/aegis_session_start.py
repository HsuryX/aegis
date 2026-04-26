#!/usr/bin/env python3
"""Codex hook template: remind the agent to run aegis session start.

Install by copying `harness/codex/.codex/` to the repo's active `.codex/`
configuration area and wiring this script to the Codex SessionStart event.
The script is intentionally non-mutating: it returns additional developer
context for the current session and exits 0.
"""

from __future__ import annotations

import json
import sys


def main() -> int:
    try:
        _ = json.load(sys.stdin)
    except json.JSONDecodeError:
        # Codex hook payload shape can evolve; the reminder does not depend on it.
        pass

    additional_context = "\n".join(
        [
            "aegis Session Start Protocol:",
            "1. Read .agent-state/phase.md.",
            "2. Read .agent-state/audit.md, decisions.md, and gaps.md.",
            "3. Verify ledger integrity with countable/tool-checkable evidence.",
            "4. Read AGENTS.md plus the current phase playbook.",
            "5. Run python3 validate.py before claiming a gate or release.",
        ]
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": additional_context,
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
