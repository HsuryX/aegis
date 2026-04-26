---
name: verify
description: Run aegis verification before claiming completion or phase advancement
---

# verify

Use after meaningful implementation or framework changes and before claiming
completion.

Minimum framework verification:

1. Run `python3 validate.py`.
2. For release/product-ship checks, run `python3 validate.py --product-ship`.
3. For Python validator edits, run `python3 -m py_compile validate.py`.
4. For shell script edits, run `bash -n <script>`.
5. Read outputs and fix failures before reporting completion.

For governed downstream projects, also run the project-specific build, type
check, lint, tests, and security scan named by the project's decisions/specs.

Record command evidence in the session log or release evidence bundle. Do not
claim "tests pass" or "verified" without the actual commands and exit status.
