# Gate Contract

## Decisions

- `PASS`: all mandatory evidence exists and no unresolved findings remain.
- `PASS_WITH_ADVISORIES`: only accepted `S2` or `S3` findings remain, each with owner, rationale, and disposition.
- `FAIL_REWORK`: artifact must be changed and reviewed again.
- `BLOCKED`: an external dependency, secret, capability, or safety rule prevents progress.
- `ESCALATE`: reviewer conflict, repeated failure, scope change, or risk acceptance requires adjudication.

## Severities

- `S0`: critical safety, security, data-loss, or fundamentally invalid result.
- `S1`: blocking functional, design, permission, test, or validation defect.
- `S2`: important risk that requires explicit disposition.
- `S3`: advisory improvement.

## Loop Rules

- Require zero unresolved `S0` and `S1` findings for every pass.
- Use two independent reviewers for requirements, design, and other critical review gates.
- Dispatch an adjudicator when reviewers conflict or the same finding survives two fixes.
- Allow at most three review/fix iterations per gate. Then return `ESCALATE` or `BLOCKED`.
- Bind every decision and evidence item to an immutable artifact version or source revision.
- Scope changes invalidate affected downstream gates. Design-breaking discoveries return to design review.
- Validation failures always return through fix, impacted tests, required full tests, and validation.
- A validation failure that is later passed must be bound to an older source revision; the fix and every repeated source-bound gate bind to the new final revision.
- Any source revision change invalidates code, security, test, visual, design-QA, and acceptance results bound to the old revision.
- Every `fix-applied` event names a declared fixer and the new final revision. It is a global invalidator for source-bound gates until those gates re-pass.
- Required adjudication is gate-specific, fresh-context, read-only, independent, declared in the run, and bound to the final revision. A passing run requires a passing adjudication result for every exhausted or explicitly adjudicated gate.
- A quality gate reports only to `ric-delivery-loop`; quality gates do not dispatch or approve one another.
- Degraded mode, missing independent reviewer capability, or user-accepted diagnostic handoff remains `BLOCKED`.
- Returning to requirements or design increments the run epoch. Gate iterations and run epochs are both capped at three.

## Finding IDs and Repair Cycles

Every review finding has a stable `finding_id`. `gate-failed`, `fix-applied`,
`results-invalidated`, and `gate-passed` events bind to the affected
`finding_id` set and the current `iteration`. Each iteration increment
requires a complete ordered repair cycle: a fix bound to the finding set, a new
artifact or source revision, invalidation of the stale result, and a fresh
re-review that re-resolves each finding. A finding that survives two fixes
triggers adjudication for that finding.
