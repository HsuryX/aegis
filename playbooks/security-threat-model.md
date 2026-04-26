<!--
SYNC-IMPACT
- version: 1.1.0 → 1.2.0
- bump: MINOR
- date: 2026-04-25
- rationale: Framework support-scope release; see CHANGELOG.md#v120 for the evidence and migration summary.
- downstream_review_required:
  - CHANGELOG.md
-->
---
id: playbooks/security-threat-model
title: Security Threat Model
version: 1.2.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 0-audit
  - phase: 1-design
severity: normative
mechanical_items: 2
judgment_items: 8
mixed_items: 1
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/standards.md
  - playbooks/01-design.md
supersedes: null
---

# Security Threat Model

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **structural problem**, **surface**, **trust boundary**.

This playbook defines the STRIDE-based threat modeling procedure for aegis projects. It is a **cross-phase** playbook: Phase 0 produces a preliminary threat model as part of the Security surface audit; Phase 1 produces the full STRIDE matrix as a companion artifact to D-5 (Security model); Phase 3 consumes the matrix for Post-Completion Control signal design.

## Applicability

The threat model MUST be completed when ANY of the following is true:

- The system handles **secrets** (API keys, passwords, tokens, signing keys, session tokens, OAuth credentials)
- The system stores or processes **user data** (PII, PHI, payment, authentication, authorization state, personal configuration)
- The system exposes an interface that crosses a **trust boundary** (user→system, system→third-party, unauthenticated→authenticated, internal→external, less-privileged→more-privileged)
- The system accepts **input from an external source that could be adversarial** (network requests, file uploads, inter-process messages, environment variables from untrusted sources)

Projects meeting NONE of the above MAY record the decision as `threat model: N/A — {one-sentence justification, e.g., "internal build tool with no secrets, no user data, no external input"}` in the D-5 (Security model) decision entry and skip the remainder of this playbook. The agent MUST NOT invoke the N/A escape without verifying against the four conditions; the justification MUST state which of the four applicability conditions are absent and why.

## STRIDE Overview

STRIDE is a threat classification framework developed by Microsoft. Each letter names a class of attacker goal:

| Letter | Threat | Attacker goal |
|--------|--------|---------------|
| **S** | Spoofing | Pretending to be another user, system, or component |
| **T** | Tampering | Modifying data or code without authorization |
| **R** | Repudiation | Denying an action was performed when it was |
| **I** | Information disclosure | Reading data without authorization |
| **D** | Denial of service | Preventing legitimate access |
| **E** | Elevation of privilege | Gaining capabilities beyond those granted |

For each trust boundary, the agent MUST enumerate at least one mitigation, a cited residual-risk note (`residual risk tracked in G-{n}`), or explicit structural `N/A — {one-sentence structural justification}` per STRIDE letter. An unaddressed cell is an unknown risk — the STRIDE matrix is exhaustive by design; completeness is the entire point. Structural N/A is valid ONLY when the boundary's architecture makes the threat class inapplicable (e.g., a read-only service has no Repudiation vector because there are no actions to deny; a boundary with no privilege model has no Elevation of privilege vector). Vague N/A ("not relevant", "doesn't apply") is a gaming attempt and fails the judgment check below.

## Phase 0: Preliminary Threat Model

During the Security surface audit (`00-audit.md` Per-Surface Entry Format → Security), the agent MUST record a preliminary threat model in the surface entry. Minimum content:

- **Trust boundaries identified** — named interfaces where trust changes (e.g., "public REST API ingress", "database read/write boundary", "third-party webhook receiver")
- **Top-3 threat vectors** — the three most likely attacker paths given the system's role and interface class, stated as STRIDE letter + one-line description (e.g., "I: unauthenticated GET /users/{id} could enumerate user IDs")
- **Existing mitigations present in current code** — audit-level observation only; no redesign here

The preliminary model is NOT the full STRIDE matrix. It is the Phase 0 input that informs D-5's scope and complexity estimate. A preliminary model with zero trust boundaries MUST trigger the applicability re-check in the N/A escape — if there are truly no trust boundaries, the system qualifies for N/A; if the agent missed one, the preliminary model is incomplete.

## Phase 1: Full STRIDE Matrix

Before the Design Closure Gate, the full STRIDE matrix MUST be populated and attached to D-5 (Security model) as a linked artifact at `specs/threat-model.md`. Required structure:

```
## Threat Model

### Boundary: {name — e.g., "public REST API ingress"}

**Description:** {who crosses this boundary, in which direction, carrying what data}
**Assets at risk:** {what an attacker would gain by compromising this boundary}

**STRIDE matrix:**

- **Spoofing:** {scenario} → mitigation: {D-{n}, specs/<spec>.md:FR-{n}, specs/<spec>.md:NFR-{n}, specs/<spec>.md:SC-{n}, standard rule, "residual risk tracked in G-{n}", or "N/A — {structural justification}"}
- **Tampering:** {scenario} → mitigation: {...}
- **Repudiation:** {scenario} → mitigation: {...}
- **Information disclosure:** {scenario} → mitigation: {...}
- **Denial of service:** {scenario} → mitigation: {...}
- **Elevation of privilege:** {scenario} → mitigation: {...}

**Residual risk:** {residual risks linked to real `G-{n}` entries; "none" is acceptable only when every STRIDE letter is mitigated or structurally `N/A`} 
**Detection signal:** {how this boundary's failure would be noticed in the current system}
**Response procedure:** {what the responder does when the detection signal fires}
```

Every mitigation reference MUST resolve to an artifact that exists by the Phase 1 gate — a decision, a path-qualified spec reference such as `specs/<spec>.md:FR-{n}` / `specs/<spec>.md:NFR-{n}` / `specs/<spec>.md:SC-{n}`, a standards.md rule, or a cited `G-{n}` gap referenced as `residual risk tracked in G-{n}`. A mitigation reading "TBD" or "add later" is not a mitigation and MUST be recorded as a real `G-{n}` entry using the canonical gap type that matches why the risk remains open.

## Mitigation Categories

Each STRIDE cell's mitigation SHOULD fall into one of these categories:

- **Control** — a mechanism that prevents the threat (authentication, authorization, input validation, encryption, rate limiting)
- **Detection** — a mechanism that reveals the threat when it occurs (logging, audit trails, anomaly alerting)
- **Response** — a procedure that handles the threat after detection (revocation, rollback, incident response)
- **Residual risk tracked in `G-{n}`** — an explicit statement that the residual risk is tolerable for now, with the cited `G-{n}` carrying the real canonical gap type, justification, and re-evaluation rule

A mitigation is complete when at least one of control/detection/response is present; residual-risk tracking is a valid but weaker option that MUST cite why the risk is tolerated plus how the cited gap will be re-evaluated (trigger or expiry, as applicable).

When a mitigation depends on harness or workflow controls, the agent MUST classify it using the canonical control-class model plus the relevant activation context. Harness-side controls use `harness/capability-matrix.md` (or the project's equivalent local control ledger) for **Executable** / **Backstop** / **Advisory** plus activation state. Framework workflow backstops (for example validator runs, gate review, rollback procedure) MAY count as active mitigations only when the mitigation text names them explicitly as workflow-executed in the current governance flow. `workflow-executed now` is explanatory prose, not a fourth activation-state enum — it means the backstop is required by the current phase/gate/release workflow and has fresh evidence in the current session or cited artifact trail. Only **Active now** harness controls or explicitly named workflow-executed backstops count as active mitigations. **Shipped but inactive** or **Not available here** controls describe capability, not present protection. Advisory/manual discipline alone MUST NOT be the only claimed mitigation for a STRIDE cell; if no active executable or backstop control exists, the cell remains a residual risk and MUST cite the appropriate `G-{n}` entry.

## LLM-Aware Threat Classes

When the project performs LLM inference in any code path — the system calls a language model API, embeds a local model, or routes prompts/responses between components — the STRIDE matrix MUST be populated with LLM-specific attack classes per the current OWASP Top 10 for LLM Applications. Each class maps to one or more STRIDE letters; list them in the relevant boundary's STRIDE matrix alongside the general-purpose threats:

- **Prompt injection** (direct and indirect) — maps primarily to **Tampering** (attacker-supplied content modifies instructions) and **Spoofing** (attacker impersonates a trusted system role). Indirect injection via retrieved/scraped content is especially subtle.
- **Insecure output handling** — maps to **Tampering** and **Information disclosure** when unvalidated LLM output is passed to downstream systems (SQL, shell, HTML, tool-calling dispatch).
- **Sensitive information disclosure** — maps to **Information disclosure** (training data leakage, prompt/context leakage across tenants, embedded secrets in prompts).
- **Data and model poisoning** — maps to **Tampering** (training/fine-tuning inputs, retrieval corpora, embedding caches).
- **Excessive agency** (over-permissive tool access) — maps to **Elevation of privilege** when the LLM agent can invoke destructive or privileged tools without commensurate authorization checks.
- **Overreliance** — maps to **Repudiation** (users accept LLM output uncritically with no audit trail of what was reviewed vs. auto-accepted) and is ALSO a latent-incident vector when the system lacks a human-in-the-loop checkpoint.
- **Unbounded consumption** — maps to **Denial of service** (token-flooding, recursive prompts, infinite tool loops) and costs control (economic DoS).

Projects performing LLM inference MUST record in D-5 which of the above classes are applicable to their system. Non-applicable classes MAY use the same `N/A — {structural justification}` escape as general STRIDE letters (e.g., "N/A — local-only inference, no external prompt ingress"). The OWASP LLM Top 10 version cited in D-5 MUST be the version current as of the last threat-model review.

## Review and Update Cadence

The threat model MUST be reviewed when:

- Trust boundaries change (new interface added; existing interface's trust level changes)
- New user data classes are introduced (e.g., adding payment processing to a system that previously handled only profile data)
- A CVE affects the system's stack (libraries, runtime, platform) in a way that invalidates a prior mitigation
- A security incident reveals a previously-unenumerated threat
- At release-readiness review (per `release-readiness.md` Security section)

Each review MUST produce either a "no change required" session log entry or an amendment to D-5 with an updated matrix.

## Mechanical Checks

Tags use the canonical bold-gate-marker form per `playbooks/automation.md` validate.py check #3: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

- [ ] **[M]** Boundary count consistency — the agent MUST verify that `grep -c '^### Boundary:' specs/threat-model.md` equals the count of distinct trust boundaries declared in D-5. Mismatch is a structural problem and MUST halt the Phase 1 gate.
- [ ] **[M]** STRIDE completeness — every boundary section MUST contain exactly one bullet for each of the six canonical STRIDE letters. `grep -cE '^- \*\*(Spoofing|Tampering|Repudiation|Information disclosure|Denial of service|Elevation of privilege):' specs/threat-model.md` MUST equal 6 × (boundary count), and a per-boundary inspection MUST confirm no letter is duplicated or missing. Each bullet MUST carry either a mitigation reference (`D-{n}` or path-qualified spec IDs such as `specs/<spec>.md:FR-{n}` / `specs/<spec>.md:NFR-{n}` / `specs/<spec>.md:SC-{n}`), a standards.md rule, a `residual risk tracked in G-{n}` reference, or an explicit structural `N/A — {one-sentence structural justification}` value. Empty-after-colon bullets fail.
- [ ] **[J]** Mitigation specificity — every STRIDE cell's mitigation MUST name a specific `D-{n}` identifier, a path-qualified spec reference such as `specs/<spec>.md:FR-{n}` / `specs/<spec>.md:NFR-{n}` / `specs/<spec>.md:SC-{n}`, a standards.md rule by section name, or an explicit `residual risk tracked in G-{n}` reference. Cells reading only "encrypted" or "validated" without a reference are judgment failures.
- [ ] **[J]** N/A justification honesty — every STRIDE letter marked `N/A` MUST cite a structural reason grounded in the boundary's architecture (e.g., "N/A — read-only service, no state to repudiate"; "N/A — single-tenant CLI, no privilege model"). Vague justifications ("N/A — not relevant", "N/A — doesn't apply", "N/A — out of scope") fail. The reviewer MUST ask: does the cited reason follow from a concrete architectural property of the boundary? If the answer is no, the N/A is gaming and the cell MUST be populated with a real mitigation or a cited `G-{n}` residual-risk entry.
- [ ] **[J]** Residual-risk justification — every cited `residual risk tracked in G-{n}` reference MUST point to a real gap entry whose reason and re-evaluation rule are explicit. "We'll fix it later" is not a justification.
- [ ] **[M+J]** Review-cadence trigger check — the agent MUST audit whether any of the review triggers (trust boundary change, new user data class, stack CVE, security incident) has fired since last review. Mechanical: compare the last-review date in D-5 against current state; Judgment: materiality of any flagged triggers.
- [ ] **[J]** Detection/response completeness for Post-Completion Control — every residual risk (including detection-only and response-only mitigations) MUST have a detection signal AND a response procedure documented. Missing either is a latent incident.
- [ ] **[J]** Compliance cross-walk accuracy — when D-5 records mappings to OWASP ASVS, NIST CSF, or ISO 27035, the mappings MUST cite specific sections (not just framework names). Vague cross-walks provide no audit value.
- [ ] **[J]** Applicability re-check honesty — when the project claims the N/A escape, the justification MUST cite which of the four applicability conditions is absent AND MUST be revisited whenever D-5 changes. A stale "N/A — internal only" claim on a system that added external input crossing a trust boundary is silent deferral.
- [ ] **[J]** STRIDE letter scope interpretation — "Spoofing" covers identity impersonation (users, services, certificates); "Tampering" covers data-at-rest, data-in-transit, and code; "Repudiation" covers deniability scenarios relevant to the project (audit trails, payment dispute); "Information disclosure" covers side channels and enumeration, not just direct reads; "Denial of service" covers resource exhaustion and algorithmic complexity, not just network flooding; "Elevation of privilege" covers both horizontal (cross-tenant) and vertical (role escalation) cases. The agent MUST interpret letters at project-specific depth, not abstractly.
- [ ] **[J]** Trust-boundary completeness — D-5 MUST enumerate every interface where trust changes; new interfaces added during spec or implementation require returning to Phase 1 and updating the threat model before the next release.

## Integration with Post-Completion Control

Threat model residual risks become inputs to the Reaction Plans output of Post-Completion Control in `03-implement.md`. Each unmitigated residual risk (including detection-only and response-only mitigations) MUST have:

- A **detection signal** — the metric, log pattern, or alert that indicates the threat is materializing in production
- A **response procedure** — the runbook or decision flow operators follow when the signal fires

A residual risk without a detection signal is an invisible risk; a risk with a detection signal but no response procedure is a latent incident. The Release Readiness Review MUST verify both exist before release.

## Relationship to Other Frameworks

aegis's STRIDE approach is compatible with:

- **OWASP Application Security Verification Standard (ASVS)** — the STRIDE matrix satisfies ASVS Level 1 threat modeling requirements
- **NIST Cybersecurity Framework** — STRIDE mitigations map to Identify (boundary enumeration), Protect (controls), Detect (detection signals), Respond (response procedures)
- **ISO 27035** — STRIDE matrix + Post-Completion Control signals/procedures align with ISO 27035 Phases 1–2 (Plan and prepare; Detection and reporting)

Projects with compliance requirements for a specific framework MAY record the mapping in D-5 but MUST NOT substitute the other framework's vocabulary for STRIDE's — STRIDE is the canonical form within aegis, cross-walks are documentation-only.
