<!-- SCHEMA:
file_type: state
sections:
  - "Critical Gaps (block phase advancement)"
  - "Non-Critical Gaps (tracked, not blocking)"
  - "Resolved Gaps"
entry_format: |
  ### G-{n}: {title}
  **Status:** captured | open | resolved
  **Severity:** critical | non-critical
  **Type:** evidence | analysis | decision | framework | deviation | conditional | scope-reduction | failure-pattern | grandfathered
  # Mirrors playbooks/gaps.md Gap Type Taxonomy (9 types) — that section is canonical. Update this enum when the canonical list changes.
  **Blocks:** phase advancement | D-{n} | nothing
quick_capture_format: |
  ### G-{n}: {title}
  **Status:** captured
  **Quick note:** {one-line description}
  **Severity guess:** critical | non-critical
  **Date captured:** YYYY-MM-DD
quick_capture_rule: Captured entries MUST be triaged to full entries before the next phase gate. See playbooks/gaps.md Quick Capture.
  **Description:** {what is missing, unclear, or blocked}
  **Expiry condition:** {REQUIRED for Type: deviation or grandfathered}
  **Trigger condition:** {REQUIRED for Type: conditional or scope-reduction}
  **Linked verdict:** {REQUIRED only for Type: conditional entries opened from a keep-with-conditions verdict — points to the audit surface whose carry-forward this gap tracks}
  **Initial artifact set:** {REQUIRED for Type: grandfathered}
  **Resolution path:** {what unblocks this gap}
  **Resolution:** {populated when Status: resolved}
  **Date opened:** YYYY-MM-DD
  **Date resolved:** YYYY-MM-DD
reference: playbooks/gaps.md full taxonomy + lifecycle rules + phase-gate interaction table
-->

# Gap Tracker

Gaps are anything missing, unclear, or blocked. See [`../playbooks/gaps.md`](../playbooks/gaps.md) for the full taxonomy (evidence, analysis, decision, framework, deviation, conditional, scope-reduction, failure-pattern, grandfathered), lifecycle states, quick-capture rules, and phase-gate interaction table.

Identifiers follow [`../playbooks/identifiers.md`](../playbooks/identifiers.md): `G-{n}` monotonic, never reused. A resolved gap retains its ID with `Status: resolved`. Once the Resolved section grows beyond ~10 recent entries or ~200 lines, archive the oldest entries to `gaps-archive.md`.

## Critical Gaps (block phase advancement)

(none)

## Non-Critical Gaps (tracked, not blocking)

(none)

## Resolved Gaps (kept for recent history; archive to `gaps-archive.md` once stale)

(none)
