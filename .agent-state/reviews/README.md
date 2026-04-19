# Subagent Review Archive

This directory stores **fresh-context subagent review outputs** that back every
`<subagent:NAME>` reference cited in a Verification Coverage Matrix
(`playbooks/principles-gates.md` §
[Verification Coverage Matrix](../../playbooks/principles-gates.md#verification-coverage-matrix)).
Each archived file is the chain-of-custody artifact for one dispatch of the
Adversarial Review Protocol
([`playbooks/principles-gates.md` § Adversarial Review Protocol](../../playbooks/principles-gates.md#adversarial-review-protocol)).

## Naming convention

```
{YYYY-MM-DD}-{NAME}.md
```

- `{YYYY-MM-DD}` — UTC date the subagent was dispatched.
- `{NAME}` — slug used in the Matrix reference `<subagent:NAME>`. Must match
  the regex `^[a-z][a-z0-9-]*(:[a-z0-9-]+)*$` (the same regex `validate.py`
  enforces on the reference itself).
- The filename MUST satisfy the glob `*-{NAME}.md` so that
  `validate.py` check_evidence_verifiability locates the artifact for a given
  `<subagent:NAME>` evidence cell.

## Required content

Each archived file MUST contain, in order:

1. **Metadata header** — date, phase, scope classification, model identifier
   (if known), and the file path of the Verification Coverage Matrix that
   cites this artifact.
2. **Reviewer prompt** — verbatim prompt used to dispatch the subagent.
   Paraphrased or summarized prompts are not acceptable; the exact text MUST
   be recoverable for re-run or re-audit.
3. **Subagent response** — full, unedited response from the subagent.
4. **Disposition section** — one row per finding reported by the subagent.
   Each row MUST carry:
   - Finding identifier (`F-{n}`)
   - Severity (`CRITICAL` / `HIGH` / `MEDIUM` / `LOW`)
   - Disposition — either a committed edit reference (file:line) or one of the
     three `[J]` justification classes: `ALREADY_SPECIFIED`,
     `OUT_OF_SCOPE_NG-n`, `RISK_ACCEPTED_BY_USER`
   - Citation — the `file:line` or anchor that supports the disposition
   - Severity-matched escalation check — `CRITICAL` and `HIGH` findings
     resolved by `[J]` MUST use `RISK_ACCEPTED_BY_USER` per
     `principles-gates.md` § Adversarial Review Protocol.

## Retention

Indefinite. This archive is the chain-of-custody for every `<subagent:NAME>`
evidence reference ever cited in `.agent-state/phase.md` or
`.agent-state/phase-archive.md`. Do NOT delete on session close. When the
archive grows large, move older files to `reviews-archive/` (follow the same
naming convention); do not discard.

## Cross-references

- Dispatch protocol: [`playbooks/principles-gates.md` § Adversarial Review Protocol](../../playbooks/principles-gates.md#adversarial-review-protocol)
- Evidence format: [`playbooks/principles-gates.md` § Verification Coverage Matrix](../../playbooks/principles-gates.md#verification-coverage-matrix)
- Validator contract: `validate.py` check_evidence_verifiability
- Session log linkage: the session that dispatched the subagent MUST cite this
  artifact via its relative path or a matching `<subagent:NAME>` reference in
  the phase gate's Verification Coverage Matrix.
