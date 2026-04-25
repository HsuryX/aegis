<!-- SCHEMA:
# NOTE: curly-brace tokens below — `{n}`, `{title}`, `{to be filled}`, `{audit surface name}`, etc. — are SCHEMA placeholders
# describing the entry format, NOT unfilled state that needs populating. Unfilled state appears as actual decision entries below this
# comment block. Do not confuse SCHEMA placeholder syntax with the check_9 "Alternatives considered MUST be non-empty" rule — that
# rule applies only to real decision entries outside this comment.
file_type: state
sections:
  - "Naming Table"
  - "Active Decisions"
  - "Accepted and Final Decisions"
  - "Terminal Decisions"
entry_format: |
  ### D-{n}: {title}
  **Status:** Draft | Proposed | Accepted | Final | Superseded (by D-{new}) | Rejected | Deferred | not-applicable | emergency
  # Mirrors 01-design.md Decision Lifecycle — that section is canonical. Update this enum when the canonical list changes.
  **Supersedes:** D-{old} | null
  **Date opened:** YYYY-MM-DD
  **Date accepted:** YYYY-MM-DD | {to be filled}
  **Date final:** YYYY-MM-DD | {to be filled}
  **Surface:** {audit surface name}
  **Context:** {problem statement}
  **Prior art:** {1-3 sentences on how similar problems solved elsewhere — REQUIRED for significant decisions}
  **Decision:** {chosen approach}
  **Alternatives considered:** {enumerated options with strengths and weaknesses}
  **Why this option wins:** {rationale}
  **Unresolved concerns:** {risks or objections acknowledged but accepted — record why they are acceptable; leave blank if none. MUST NOT be omitted.}
  **Downstream impact:** {decision IDs that depend on this one}
  **Confirmation:** {how compliance is validated — REQUIRED at Accepted and Final}
reference: playbooks/01-design.md Decision Entry Format + Decision Lifecycle
-->

# Decision Ledger

Identifiers follow the rules in [`../playbooks/identifiers.md`](../playbooks/identifiers.md): `D-1` through `D-12` are reserved for the Required Decisions in `01-design.md`; `D-13` and above are project-specific. IDs are monotonic and MUST NOT be reused. A superseded decision keeps its original ID with `Status: Superseded (by D-{new})`; the replacement receives a new ID, goes through the normal `Draft` → `Proposed` → `Accepted` → `Final` lifecycle (see `01-design.md` Decision Entry Format + Decision Lifecycle), and MUST populate its `Supersedes:` field with the old ID.

## Naming Table

Entries ordered alphabetically by Canonical Term. See `01-design.md` for population rules.

| Concept | Canonical Term | Owner | Forbidden Aliases |
|---------|---------------|-------|-------------------|

Owner column rule: `Owner` names the current canonical owner of the concept, not merely a file that mentions the term.

## Active Decisions

(none)

## Accepted and Final Decisions

(none)

## Terminal Decisions

(none)
