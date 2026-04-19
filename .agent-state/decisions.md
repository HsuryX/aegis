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
| | | | |

## Active Decisions

(Decisions in `Draft`, `Proposed`, or `Deferred` state — still being decided. Actionable items first.)

## Accepted and Final Decisions

(Decisions that have passed review. `Accepted` = reviewed and approved, implementation not yet complete. `Final` = implemented, verified by the Confirmation mechanism, and in production use.)

## Terminal Decisions

(`Superseded`, `Rejected`, and `not-applicable` entries retained for traceability. Superseded entries cite their replacement via `Status: Superseded (by D-{new})`; replacement entries live in Accepted/Final above and cite the superseded ID via `Supersedes:`. Rejected entries retain their Alternatives considered analysis to prevent re-deliberation. `not-applicable` entries document why a Required slot was skipped under the scope classification.)

---

Entry format: see `01-design.md` Decision Entry Format and Decision Lifecycle. Fields: Status, Date opened, Date accepted, Date final, Surface, Supersedes (if applicable), Context, Prior art, Decision, Alternatives considered, Why this option wins, Confirmation, Unresolved concerns, Downstream impact.
