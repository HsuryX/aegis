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
  **Expiry condition:** {REQUIRED for Type: deviation}
  **Trigger condition:** {REQUIRED for Type: conditional or scope-reduction}
  **Linked verdict:** {REQUIRED for Type: conditional — points to the audit surface whose keep-with-conditions verdict this gap tracks}
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

(None yet.)

## Non-Critical Gaps (tracked, not blocking)

(None yet.)

## Resolved Gaps (kept for recent history; archive to `gaps-archive.md` once stale)

(None yet.)

---

### Severity Criteria

- **Critical**: blocks phase advancement — missing information that prevents a correct result in the current phase.
- **Non-critical**: tracked but does not block advancement — the current phase can produce a correct (if incomplete) result.

When uncertain, classify as critical — false positives cost less than false negatives. For full definitions, type taxonomy, lifecycle, and resolution rules, see [`../playbooks/gaps.md`](../playbooks/gaps.md).

### Entry Template

```markdown
### G-{number}: {title}

**Status:** open | resolved
**Severity:** critical | non-critical
**Type:** evidence | analysis | decision | framework | deviation | conditional | scope-reduction | failure-pattern | grandfathered
**Blocks:** phase advancement | D-{n} | nothing

**Description:** {what is missing or unclear}
**Expiry condition:** {REQUIRED for types `deviation`, `conditional`, `scope-reduction`, `grandfathered` — when this entry expires or its trigger fires, e.g., "until Phase 2 completes", "until D-{n} is revised", "before Phase 3 implementation of spec/{name}.md", "when user count exceeds 10k", "until all originally-grandfathered artifacts have been edited/superseded/deleted"; leave blank for `evidence`, `analysis`, `decision`, `framework`, `failure-pattern` types}
**Trigger condition:** {REQUIRED for type `conditional` — specific event that MUST cause the condition to be met; REQUIRED for type `scope-reduction` — specific event that MUST cause the deferred requirement to be restored; leave blank for other types}
**Linked verdict:** {REQUIRED for type `conditional` — the `keep-with-conditions` audit surface entry this condition belongs to, as `{Surface Name}` in `audit.md`; leave blank for other types}
**Initial artifact set:** {REQUIRED for type `grandfathered` — list of file paths or `git log` anchor identifying the legacy artifacts covered, required for expiry verification}
**Severity history:** {append-only — REQUIRED if Severity has ever changed since opening. Format: `{YYYY-MM-DD}: {old} → {new} — {justification}`; downgrades MUST cite specific evidence or named user approval. See `playbooks/gaps.md` Severity history}
**Resolution path:** {specific action or information needed}
**Resolution:** {how this was actually resolved — reference D-{n} or finding; filled when resolved}

**Date opened:** YYYY-MM-DD
**Date resolved:** YYYY-MM-DD
```
