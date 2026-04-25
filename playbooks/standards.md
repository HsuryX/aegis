<!--
SYNC-IMPACT
- version: 1.0.0 → 1.1.0
- bump: MINOR
- date: 2026-04-25
- rationale: Framework refinement release. Adds the bounded-change 0 -> 3 path for already-governed work (`00-audit.md`); the harness security-claim model with explicit control-class (`Executable` / `Backstop` / `Advisory`) and activation-state (`Active now` / `Shipped but inactive` / `Not available here`) classification (`harness/capability-matrix.md`); the Canonical Dependency Edges DAG seeding the Whole-System Composition Check (`01-design.md`); the Adversarial Review Protocol Per-phase timing-hooks table (`principles-gates.md`); the Scope-Proportional gate-protocol mini-matrix (`principles-gates.md` Scope-Proportional Ceremony); the `phase regression` glossary entry; and `validate.py check_traceability` — a file-level `Implements:`/`Covers:` rollup (warning-only, vacuous on the framework repo itself). Extends Required Behaviors #7 with an archive-decay re-evaluation rule for consulted archive entries >= 12 months old (`principles.md`). Expands the existing Cold Read perspective with a concrete protocol (`principles-gates.md`). Adds a date-only UTC variant to the scope-reduction sign-off format for `micro`/`small` projects (`00-audit.md` ceremony matrix + `release-readiness.md` checklist); the full git-email anchored form remains for `standard`/`large`. Relaxes Session Start Protocol Step 3 — the integrity block now accepts any form that cites countable or tool-checkable evidence; the prior templated form is preserved as a reference example. Promotes the implementation-boundary rule to a dedicated `## Implementation Boundary` section in `AGENTS.md` (v1.0.0 carried the rule as a paragraph below the Phase Gates table); the new section's bounded-change summary paragraph points at `00-audit.md` for the full Bounded-Change Rule; surfaces additional Phase 1 gate items (Authority model, Whole-System Composition Check, threat-model applicability) and Phase 2 Proof-class declaration in the `AGENTS.md` Phase Gates table; decouples the Phase 1 threat-model gate from `specs/threat-model.md` artifact-existence (binds to whichever path D-5 declares); reformats the `AGENTS.md` Workspace Discipline second paragraph from a single run-on into a 6-bullet list (preserving v1.0.0 content and adding a Bash-subprocess-gap caveat); trims the scope-reduction marker phrase list (`validate.py` `_DEFERRAL_PHRASES`, mirrored in `standards.md` / `03-implement.md` / `harness/cursor/.cursor/rules/phase-3.mdc`) to unambiguous multi-word forms only, dropping false-positive-prone tokens. De-duplicates the Verdict Discipline definition (`AGENTS.md` is sole canonical owner; glossary holds a one-paragraph redirect); removes the four per-phase `## Adversarial Gate Check` stanzas (replaced by the new Per-phase timing-hooks table); removes the redundant placeholder grep at `02-spec.md` Quality Checks (the Phase Gate scan is a strict superset). Compresses Codex and Cursor harness READMEs by deferring universal-backstop guidance to `harness/capability-matrix.md`. Required Behaviors #8 grep formula relocates from `principles.md` body to `automation.md` Lessons-Gap Backstop. Removes the `validate.py` Verification Coverage Matrix anchor-diversity check; its enforcement contract is already covered by check 7 (evidence verifiability). SemVer MINOR — additive and refinement; no rule becomes stricter than v1.0.0 in a way that invalidates prior compliance.
- downstream_review_required:
  - README.md
  - ONBOARDING.md
  - CHANGELOG.md
  - harness/capability-matrix.md
  - harness/claude-code/README.md
  - harness/codex/README.md
  - harness/cursor/README.md
  - harness/ci/README.md
  - harness/claude-code/hooks-cookbook.md
  - harness/claude-code/skills/phase-status/SKILL.md
  - validate.py
  - tools/bootstrap.sh
-->
---
id: playbooks/standards
title: Quality Standards
version: 1.1.0
last_reviewed: 2026-04-25
applies_to:
  - phase: 2-spec
  - phase: 3-implement
severity: normative
mechanical_items: 11
judgment_items: 16
mixed_items: 3
references:
  - AGENTS.md
  - playbooks/principles.md
  - playbooks/glossary.md
  - playbooks/03-implement.md
supersedes: null
---

# Quality Standards

Read this file when evaluating, specifying, or producing code. These standards apply in all phases where code, tests, or technical documentation are involved. For spec-only projects (Phase 2 terminal), apply only the sections relevant to specification and documentation quality — code-specific sections (TDD workflow, coverage targets, security checklist, performance awareness) are not applicable when no production code exists.

> **Terminology.** This playbook uses terms defined in [`glossary.md`](./glossary.md): **gap**, **review**, **trust boundary**, **validate**, **verify**, **well-maintained**. "Verify" (tool-checked), "validate" (requirements-checked), and "review" (human or separate-agent judgment) are three distinct activities — the glossary explains the distinction and when each applies.

These standards define the minimum acceptable quality bar, not the target. Thoroughness in every step prevents costly rework. When a standard says "<50 lines" or "80% coverage", treat those as floors — pursue higher quality when the situation warrants it.

## Code Quality

Ordered by concern: correctness → readability → robustness. When a language has an established idiom that achieves the same goal differently (e.g., Go's pointer receivers for mutation, Rust's ownership for immutability), code MUST follow the language's idiom.

- **Immutability**: code SHOULD create new objects and SHOULD NOT mutate existing ones; mutation is permitted only when performance-critical and explicitly justified in a decision entry or comment
- **Error handling**: errors MUST be handled explicitly at every level, MUST use user-friendly messages at UI boundaries, and MUST carry structured detail at service boundaries. Errors MUST NOT be silently swallowed. When propagating errors, the code MUST add context at each level so the error chain shows origin and path
- **Input validation**: all data crossing a trust boundary (user input, API responses, database results, file content, environment variables, message queue payloads, and any other cross-boundary data) MUST be validated before processing
- **Type safety**: code SHOULD prefer strong types over string-typed or loosely-typed data and SHOULD encode invariants in the type system where the language supports it
- **Naming**: identifiers MUST be descriptive, consistent, and unambiguous. Code MUST NOT use abbreviations unless universally understood in the domain. Identifiers MUST match the canonical naming table
- **Comments**: comments SHOULD explain WHY only when not obvious from code and MUST NOT restate WHAT. Stale comments MUST be removed — they are worse than none
- **Small functions**: functions SHOULD be under 50 lines with a single clear responsibility
- **Small files**: files SHOULD be under 800 lines with high cohesion within a single concern
- **No deep nesting**: nesting SHOULD NOT exceed 4 levels; code SHOULD use early returns, guard clauses, or extraction to reduce depth
- **Organization**: code SHOULD be grouped by feature or domain (not by file type) and SHOULD co-locate related code
- **No hardcoded values**: constants, configuration, or environment variables MUST be used for anything that could change or that carries semantic meaning
- **Resource cleanup**: connections, locks, and temporary state MUST be closed or released in all exit paths including error paths
- **Edge case awareness**: code MUST consider empty inputs, boundary values, unicode, concurrent access, extremely large inputs, and zero/null/missing cases
- **Generated code**: code from generators, scaffolding tools, or build pipelines is excluded from manual quality review, but generated files MUST be regenerated from canonical sources rather than manually patched. Generated files MUST be clearly marked (e.g., header comment) and SHOULD be excluded from linting where appropriate

## Ordering Conventions

Every ordered list in code MUST follow a stated, consistent principle — MUST NOT be arbitrary or historical order. Default conventions (which a project design decision MAY override when justified):

- **Imports**: standard library → external packages → internal modules → relative imports; alphabetical within each group; separated by blank lines between groups
- **File-level declarations**: exported types/interfaces → exported constants → exported functions/classes → internal helpers
- **Function parameters**: required before optional; context or configuration objects last
- **Object/struct fields**: identifier → required data → optional data → computed/derived → metadata/timestamps
- **Enum/constant groups**: by logical grouping (lifecycle order, severity order, or alphabetical); one principle per group, applied consistently
- **API response fields**: id → type → core attributes → relationships → metadata → timestamps
- **Database columns**: primary key → foreign keys → required columns → optional columns → audit timestamps (created, updated)
- **Test cases**: happy path → boundary/edge cases → error/failure cases
- **Configuration entries**: group by concern; alphabetical within groups

When the language or framework has an established idiomatic ordering convention, code MUST follow it over these defaults.

## Testing

- **Coverage target**: the default metric is **line coverage**, and projects MUST meet a minimum of 80% line coverage. Paths crossing trust boundaries (authentication, authorization, payment, data mutation, secret handling) MUST meet 95% line coverage minimum. In addition, **security-critical paths** (authentication, authorization, payment, secret handling) SHOULD target **≥70% branch coverage** on top of the line-coverage requirement — branch coverage catches untested conditional paths that line coverage misses (e.g., the `else` branch of an `if` that rarely fires, or the exception path of a `try` that is exercised only under adversarial input). **Enforcement:** an unmet line-coverage target (80% default or 95% trust-boundary) blocks Phase 3 gate advancement via the Phase 3 Completion Criteria `[M]` coverage item in `03-implement.md`. An unmet branch-coverage SHOULD target fails the Self-Review checklist and MUST be either fixed or called out explicitly in the gate/release-readiness judgment; it MUST NOT be recast as `scope-reduction` unless an actual specified requirement is being deferred. The test strategy decision (D-10) MAY override either target with a project-specific bar when justified — for example, a project with formally-verified authentication code MAY set a lower empirical coverage target, and a project with no security-critical paths MAY omit the branch-coverage requirement entirely. Coverage-target overrides are user-facing quality commitments: the agent MUST propose any override to the user before adopting it, MUST NOT self-authorize, and MUST record the approved override in the D-10 decision entry with explicit justification and the user approval date
- **TDD workflow** (default; the test strategy decision D-10 MAY adopt a different workflow with justification): the agent SHOULD write a failing test → write minimal implementation to pass → refactor. If a test is difficult to write, that signals a design problem — the agent MUST refactor for testability rather than skipping the test
- **Test types** (all REQUIRED for non-trivial projects): unit (functions, components), integration (APIs, data access, service boundaries), E2E (critical user flows)
- **Test quality**: tests MUST verify behavior described in specifications, not implementation details. Tests MUST be isolated (no shared mutable state, no execution-order dependency). Each test MUST have a clear assertion about one behavior
- **Deterministic test data**: tests MUST use factories, fixtures, or seeded generators. Tests MUST NOT depend on production data or unseeded randomness
- **Regression discipline**: every bug fix MUST include a test that reproduces the bug before the fix

### Test pyramid

Default test distribution (D-10 MAY override with justification): **70% unit, 20% integration, 10% e2e**. The ratio reflects the inverted cost/speed/confidence triangle — unit tests are cheap and fast but narrow; e2e tests are expensive and slow but broad. Non-default shapes MAY be justified for specific system classes: data-pipeline systems often invert to 20:60:20 (fewer unit tests, more integration because transformations are the contract); UI-heavy systems MAY push e2e higher via component-level visual tests. D-10 MUST record the target ratio; the Post-Change Verification item in `03-implement.md` MUST report actual distribution against D-10's target.

### Per-layer coverage

Coverage targets are **per-layer, not blended**. Each test runner (unit, integration, e2e) MUST report its own coverage, and each MUST meet its own floor:

- Unit: ≥ 80% line coverage (default; raise to 95% for trust-boundary code)
- Integration: ≥ 70% line coverage for API surfaces and data-access layers
- E2E: each critical user flow from the Product surface MUST have at least one passing e2e test; there is no percentage floor because e2e counts flows, not lines

A blended 80% that comes from 100% unit / 0% integration MUST NOT pass the gate. The test strategy decision D-10 MUST name three independent commands — one per layer — and the release-readiness check MUST validate all three. Mechanical: e.g., `pytest tests/unit --cov-fail-under=80`, `pytest tests/integration --cov-fail-under=70`, `pytest tests/e2e` (with critical-flow assertions).

### Contract Formats

*(Canonical location for the Contract Format decision — `01-design.md` D-13+ Contract Format, `02-spec.md` Machine-readable Contract, and `glossary.md` Machine-readable contract all point here. Do not re-enumerate the format list elsewhere; amendments happen in this subsection.)*

When a project exposes any cross-trust-boundary interface, the machine-readable contract MUST use one of the canonical forms declared in D-13+ (Contract Format decision):

- **REST APIs** → OpenAPI 3.1 (`openapi.yaml` or `openapi.json`)
- **RPC / gRPC** → protobuf (`.proto` files)
- **Event / streaming** → AsyncAPI 2.6 (`asyncapi.yaml`)
- **Data validation** → JSON Schema Draft 2020-12 (`*.schema.json`)
- **CLI** → machine-readable help parseable to a `--json` flag output or a dedicated schema file

Internal-only interfaces MAY record `schema: N/A — internal only` in the spec Scope section with a one-line justification. Mixed forms are permitted when the system exposes multiple interface classes (e.g., a system with a REST API + an event bus SHOULD have both OpenAPI and AsyncAPI artifacts). Machine-readable contracts MUST be checked into the repo at `specs/schemas/` unless D-13+ specifies otherwise, and MUST be the source of truth that code and tests derive from (not the other way around).

## Security

Ordered by severity of impact if missed. Items that do not apply to the current system MAY be skipped (e.g., CSRF for non-web systems, SQL injection for projects without databases) — the security model decision defines which items are relevant. Before any commit, the agent MUST verify every applicable item. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**Tally:** 5 `[M]` · 2 `[M+J]` · 11 `[J]`.

- [ ] **[M]** No hardcoded secrets (API keys, passwords, tokens, certificates, private keys) — this rule applies to state files and decision entries as well. Secrets MUST be referenced by name (e.g., "`API_KEY` environment variable") and MUST NOT appear by value. Mechanical: secret scanners (`gitleaks`, `trufflehog`, regex-based detectors) catch the common cases.
- [ ] **[J]** Authentication and authorization verified for every protected resource
- [ ] **[M]** No weak or deprecated cryptographic algorithms (MD5, SHA1 for security purposes, ECB mode, static IVs); current standards MUST be used for hashing, encryption, and key derivation. Mechanical: grep for the deprecated algorithm names in code.
- [ ] **[J]** All user input validated and sanitized before processing
- [ ] **[M+J]** Parameterized queries only (no string concatenation in SQL or query builders). Mechanical: grep for string concatenation adjacent to SQL keywords. Judgment: the match is a false positive check.
- [ ] **[J]** Output encoding applied where content is rendered (XSS prevention)
- [ ] **[J]** CSRF protection on all state-changing operations
- [ ] **[J]** No PII or secrets in logs, error messages, or debug output
- [ ] **[J]** Error responses do not expose internal details, stack traces, or infrastructure information
- [ ] **[J]** Rate limiting on all public-facing endpoints
- [ ] **[M+J]** No unsafe deserialization of untrusted data without schema validation and type checking. Mechanical: grep for dangerous deserializers (`pickle.loads`, `yaml.load` without `SafeLoader`, `eval`, `Function` constructor). Judgment: context determines whether the input is trusted.
- [ ] **[J]** Outbound request URLs validated and restricted (SSRF prevention); allowlists MUST be used for external service calls
- [ ] **[M]** Dependencies checked for known vulnerabilities. Mechanical: `npm audit`, `pip-audit`, `cargo audit`, or equivalent exits clean.
- [ ] **[J]** Package names verified against official registry to prevent typosquatting (exact spelling, publisher/organization, download counts)
- [ ] **[J]** No private package names that could be confused with public packages (dependency confusion prevention)
- [ ] **[J]** Prototype-polluting patterns avoided in object merging, deep cloning, and query parameter parsing — code MUST use `Object.create(null)` or `Map` for dictionaries from untrusted input
- [ ] **[M]** Lockfile integrity verified (`npm audit signatures`, `pip hash checking`, or equivalent) to detect tampered packages
- [ ] **[J]** For critical dependencies (auth, crypto, serialization), transitive dependency tree reviewed — transitive dependencies carry the same supply chain risk

## Performance Awareness

- Code MUST NOT introduce O(n²) or worse complexity in any path that processes user-controlled input sizes
- Collections and queries MUST NOT be unbounded — limits and pagination MUST be applied
- N+1 query patterns MUST NOT be used — code MUST use joins, batching, or eager loading instead
- Expensive resources (DB connections, file handles, HTTP clients) MUST be closed or pooled
- State-changing operations SHOULD be idempotent where feasible — safe to retry without unintended side effects
- Code MUST be profiled before optimizing — the agent MUST NOT optimize without evidence of a bottleneck

## Accessibility

Applies when the system has user-facing interfaces (web, mobile, desktop, or CLI). Items that do not apply to the current system MAY be skipped — the accessibility model decision defines scope.

- User-facing systems MUST target interface-specific accessibility standards as the minimum bar. The applicable standard depends on the interface class, and the accessibility model decision MUST declare which apply:
  - **Web** (browser-rendered HTML/CSS/JS): MUST target WCAG 2.2 Level AA compliance
  - **iOS** (native Apple platforms — iOS, iPadOS, macOS native apps): MUST follow Apple's Accessibility Programming Guide + WCAG 2.2 AA where the underlying content is web-like (WKWebView, embedded HTML)
  - **Android** (native Google platforms): MUST follow the Android Accessibility Guidelines + WCAG 2.2 AA where the underlying content is web-like (WebView, embedded HTML)
  - **Desktop** (native Windows/Linux/macOS applications): MUST follow the platform's native accessibility guidelines (Windows UI Automation, GNOME Accessibility Toolkit, macOS Accessibility API) — or WCAG 2.2 AA when the UI is rendered via a web engine
  - **CLI** (terminal applications): MUST be keyboard-navigable end-to-end, MUST NOT convey information through color alone, MUST respect the `NO_COLOR` environment variable (disable ANSI color output when set), MUST respect `TERM=dumb` (disable cursor-based rendering and fall back to plain output when set), and MUST degrade to plain text when stdout is not a TTY (piped output, redirected output). Usage help and error messages MUST remain readable by a screen reader operating against a terminal emulator
  - **Other interface classes** (voice, game controller, kiosk, embedded): the accessibility model decision MUST name the applicable standard or SHOULD default to the closest of the above with project-specific adjustments recorded in D-10 or the accessibility model decision
- Markup MUST use semantic HTML elements (`button`, `nav`, `main`, heading levels) instead of generic `div`/`span` with ARIA roles that duplicate native semantics
- All interactive elements MUST be reachable and operable via keyboard alone; focus order MUST follow logical reading order; focus indicators MUST be visible
- Color contrast MUST meet 4.5:1 for normal text and 3:1 for large text and UI components
- All non-decorative images MUST have meaningful `alt` text; decorative images MUST have empty `alt=""`
- Dynamic content changes MUST be announced via ARIA live regions; form inputs MUST have associated labels
- Implementations MUST respect `prefers-reduced-motion` — non-essential animations MUST be disabled or reduced accordingly
- Projects SHOULD include automated accessibility testing (e.g., axe-core) in the Verification Sequence when applicable

### Testing approach

The Accessibility Model decision (D-13+ candidate in `01-design.md`) MUST declare the project's accessibility testing strategy. At minimum, the decision MUST specify:

- **Automated scans** — which tool runs at which gate. Web projects SHOULD run axe-core or pa11y on every PR that touches UI code; native mobile projects SHOULD run platform-native accessibility linters (Xcode Accessibility Audit for iOS; accessibility-test-framework for Android) as part of the integration test suite. Automated tooling catches an estimated 30–40% of WCAG violations — necessary but not sufficient.
- **Manual audit cadence** — how often a human (or screen-reader-equipped agent) walks through the product. Recommended cadences: per release for standard-scope projects, per milestone for large-scope projects. Audits MUST exercise keyboard-only navigation, screen reader (VoiceOver / NVDA / TalkBack) narration, 200% zoom, and reduced-motion mode.
- **Assistive-technology target** — which AT versions and combinations the project commits to supporting (e.g., "VoiceOver on iOS 17+; NVDA 2023+ with Firefox; macOS VoiceOver with Safari"). The list MUST be narrow enough to be testable and broad enough to cover the Product surface's declared user population.
- **CI integration** — the accessibility scan command MUST appear in the Verification Sequence. If the project runs on CI, the scan MUST be a blocking check for PRs that modify UI code.

Projects with no user-facing interface MAY record the Accessibility Model as `accessibility: N/A — no user interface` in the session log and skip all of the above; the absence of UI MUST be verified against the Product surface before invoking this escape.

## Deployment Safety

- Changes with user-visible behavioral impact SHOULD be deployable behind a feature flag or toggle mechanism when the project's deployment model supports it
- Feature flags MUST have: a clear owner, an expiration date or removal criterion, and a documented off-state that matches pre-change behavior
- Feature flags MUST NOT be treated as a substitute for testing — flagged code paths MUST meet the same coverage and quality standards as unflagged paths
- Stale feature flags (past expiration or fully rolled out) are technical debt — the agent MUST track removal as a gap entry
- Rollback capability: every deployment MUST be reversible; if a change includes irreversible steps (destructive database migrations, external API changes), the rollback constraints MUST be documented in the deployment plan

## Dependency Discipline

- Projects SHOULD use the latest stable release (LTS where applicable) and SHOULD leverage newer platform features when they improve clarity, safety, or performance. Deprecated APIs or patterns MUST NOT be used when supported replacements exist
- Each external dependency MUST be justified: what it provides that would be costly to build and maintain
- Projects SHOULD prefer well-maintained libraries with active communities over abandoned or niche packages
- Production dependency versions MUST be pinned explicitly; floating ranges MUST NOT be used in production dependencies; lock files MUST be committed for reproducible builds
- Projects MUST periodically audit for known vulnerabilities and license compatibility

## Self-Review Checklist

Ordered by severity: security → correctness → quality → completeness. The agent MUST run this checklist before marking any code change complete. For items that can be machine-verified, the agent MUST record actual command output as evidence and MUST NOT check items from memory or confidence. Tags: `[M]` mechanical, `[J]` judgment, `[M+J]` both.

**Tally:** 7 `[M]` · 1 `[M+J]` · 4 `[J]`.

- [ ] **[M]** No secrets, debug statements, or unresolved TODOs in committed code. Mechanical: secret scanner + `grep -rnE '\b(console\.log|print|debugger|TODO|FIXME|XXX)\b' src/` returns zero.
- [ ] **[J]** Security checklist passes for relevant code (delegates to the Security section above)
- [ ] **[J]** Errors handled explicitly in all paths
- [ ] **[M]** Tests exist, pass, and cover the new behavior. Mechanical: test runner exit 0 + new test files or test cases are present in the diff.
- [ ] **[M]** Coverage meets target. Mechanical: coverage tool output meets or exceeds D-10 target.
- [ ] **[M]** Naming matches canonical naming table. Mechanical: grep changed files against Forbidden Aliases in the Naming Table — any hit is a violation.
- [ ] **[J]** Readable to someone with no prior context
- [ ] **[M]** Functions focused, under 50 lines. Mechanical: line-count scan of changed functions.
- [ ] **[M]** Files cohesive, under 800 lines. Mechanical: `wc -l` on changed files.
- [ ] **[M]** Automated formatters, linters, and type checkers pass when configured in the project. Mechanical: formatter/linter/type-checker exit 0.
- [ ] **[M+J]** No silent scope reduction — every requirement from the traced specification MUST be present in the code OR explicitly deferred via a `gaps.md` entry of type `scope-reduction` per `03-implement.md` Hard Rule 3. Prohibited scope-reduction marker phrases ("simplified version", "static for now", "defer to follow-up", "good enough for now", "stub for the moment", "coming in v2") MUST NOT appear unless each occurrence is tracked in a gap entry. The phrase set is deliberately narrow — only multi-word forms that have negligible legitimate use as substantive technical content. Mechanical: `grep -rnEi 'simplified version|static for now|defer to follow-up|good enough for now|stub for the moment|coming in v2' src/ tests/ specs/` returns zero, or every hit has a corresponding open `scope-reduction` gap whose body cites the affected repo-relative file path. The canonical list and scan implementation live in `validate.py` `_DEFERRAL_PHRASES` and `check_silent_deferral_phrases` — the prose here mirrors that list. Judgment: the requirement-coverage comparison against the spec's FR labels, and whether each deferral's trigger condition is honest and specific.
- [ ] **[J]** Documentation updated if externally visible behavior changed

## Git Conventions

- Commit messages MUST use the format `type(scope): description` (conventional commits)
- `type` MUST be one of: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`
- Each commit SHOULD contain one logical change
- The message body MUST explain WHY, not WHAT — the diff shows what
- Commits that implement a decision MUST include `Implements: D-{n}` referencing the design decision
