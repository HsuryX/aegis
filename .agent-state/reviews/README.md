# Subagent Review Archive

This directory stores **fresh-context review outputs** that back two auditable
citation forms in `.agent-state/phase.md` / `.agent-state/phase-archive.md`:
(1) `<subagent:NAME>` references in a Verification Coverage Matrix and
(2) file-or-anchor references cited as a `Fresh-context review artifact` in a
framework-amendment evidence bundle. Each archived file is the chain-of-custody
artifact for one fresh-context dispatch under the Adversarial Review Protocol or
its semantic-amendment counterpart in `playbooks/principles-gates.md`.

## Naming convention

```
{YYYY-MM-DD}-{NAME}.md
```

- `{YYYY-MM-DD}` — UTC date the subagent was dispatched.
- `{NAME}` — stable review-topic slug. When the artifact is cited via
  `<subagent:NAME>`, it MUST match the regex `^[a-z][a-z0-9-]*(:[a-z0-9-]+)*$`
  (the same regex `validate.py` enforces on the reference itself).
- The filename MUST satisfy the glob `*-{NAME}.md` so the artifact remains
  mechanically discoverable for either citation mode.

## Required content

Each archived file MUST contain, in order:

1. **Metadata header** — `Date (UTC)`, `Phase`, `Scope classification`,
   `Model identifier` (use `unknown` if unavailable), and an exact `Cited from:` pointer naming the
   `.agent-state/phase.md` / `.agent-state/phase-archive.md` anchor that cites
   this artifact (either a Verification Coverage Matrix row or an amendment
   evidence-bundle item).
2. **Reviewer prompt** — verbatim prompt used to dispatch the subagent.
   Paraphrased or summarized prompts are not acceptable; the exact text MUST
   be recoverable for re-run or re-audit. When the artifact backs an amendment
   evidence bundle, the prompt scope MUST explicitly include the changed
   normative files **and any directly affected derived guidance** — wording such
   as "if needed" is not sufficient.
3. **Subagent response** — full, unedited response from the subagent.
4. **Disposition section** — one row per finding reported by the subagent.
   Each row MUST carry:
   - Finding identifier (`F-{n}`)
   - Severity (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`)
   - Disposition — either a committed edit reference (`file:line` or
     `file.md#anchor`) or one of the three `[J]` justification classes:
     `ALREADY_SPECIFIED`, `OUT_OF_SCOPE_NG-n`, `RISK_ACCEPTED_BY_USER`
   - Citation — the `file:line` or anchor that supports the disposition
   - Severity-matched escalation check — `CRITICAL` and `HIGH` findings
     resolved by `[J]` MUST use `RISK_ACCEPTED_BY_USER` per
     `principles-gates.md` § Adversarial Review Protocol.

Severity tokens anywhere in the archive artifact MUST use only the canonical
set `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`. `INFO` is not a valid archive
severity; informational notes MUST be plain prose or recorded at `LOW`.

## Retention

Indefinite. This archive is the chain-of-custody for every `<subagent:NAME>`
reference and every amendment-bundle `Fresh-context review artifact` reference
ever cited in `.agent-state/phase.md` or `.agent-state/phase-archive.md`. Do
NOT delete on session close. When the archive grows large, move older files to
`reviews-archive/` (follow the same naming convention); do not discard.

## Cross-references

- Dispatch protocol: [`playbooks/principles-gates.md` § Adversarial Review Protocol](../../playbooks/principles-gates.md#adversarial-review-protocol)
- Evidence format: [`playbooks/principles-gates.md` § Verification Coverage Matrix](../../playbooks/principles-gates.md#verification-coverage-matrix)
- Amendment evidence format: [`playbooks/principles-gates.md` § Amendment Protocol](../../playbooks/principles-gates.md#amendment-protocol)
- Validator contract: `validate.py` check_evidence_verifiability + amendment-bundle review-artifact validation
- Session log linkage: the session that dispatched the subagent MUST cite this
  artifact via its relative path or a matching `<subagent:NAME>` reference in
  the relevant Verification Coverage Matrix row or amendment evidence bundle.
