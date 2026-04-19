<!-- SCHEMA:
file_type: state
sections:
  - "Strategy"
  - "Surface Audits"
entry_format: |
  ### {SurfaceName}
  **Exists:** {description of current state}
  **Strong:** {what is correct about it}
  **Wrong:** {what is wrong with it}
  **Reference:** {file paths or section pointers as evidence}
  **Verdict:** keep | keep-with-conditions | redesign | delete
  **Conditions:** {required only when Verdict is keep-with-conditions; list linked G-{n} conditional gap IDs}
  **Design notes:** {implications for Phase 1}
reference: playbooks/00-audit.md Per-Surface Entry Format
-->

# Audit Register

Phase 0 output. Every surface listed in `playbooks/00-audit.md` MUST have an entry (or an explicit "not applicable" with reason) before the Phase 0 gate can pass. For green-field projects, start with the **Product** surface by eliciting goals, users, constraints, and success criteria.

## Strategy

(Populated after all surface audits complete. Record the chosen strategy — **in-place evolution**, **clean-room rewrite**, **hybrid evolution**, or **new-build** (green-field) — and the rationale per `playbooks/00-audit.md` Strategy Decision.)

**Approach:**

**Rationale:**

**Top risks:**

## Surface Audits

(One `### {SurfaceName}` entry per surface. Use the entry format in the SCHEMA above. See `playbooks/00-audit.md` Surfaces for the full list and `playbooks/00-audit.md` Per-Surface Entry Format for field semantics.)
