---
name: ric-acceptance-validation
description: Use when a tested integrated revision must be independently validated against approved acceptance criteria before final delivery or release readiness.
---
# RIC Acceptance Validation

Validate observable outcomes against approved acceptance criteria. Do not modify the implementation.

## Procedure

1. Pin the tested integrated revision and acceptance artifact version.
2. The dispatched validator loads `ric-independent-review`, `ric-acceptance-validation`, the primary domain skill, and any required browser, infrastructure, accessibility, or documentation skills.
3. Execute each acceptance criterion using real behavior and collect reproducible evidence.
4. Verify permissions, negative cases, failure states, recovery, compatibility, and residual risk as applicable.
5. Keep visual critique separate from interaction assertions. Report visual/design-QA needs to `ric-delivery-loop`; do not dispatch or approve another gate.
6. Update traceability and return the gate decision only to `ric-delivery-loop`.

Read [references/validation-contract.md](references/validation-contract.md) before validating.

## Failure Loop

On failure, return `FAIL_REWORK`. After fixes, require impacted tests, required full suites, and then validation against the new revision. Never jump directly from a fix to validation.

## Exit

Pass only when every mandatory acceptance criterion has current evidence and no unresolved `S0` or `S1` remains.
