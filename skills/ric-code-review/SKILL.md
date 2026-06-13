---
name: ric-code-review
description: Use when an implementation, diff, pull request, migration, configuration change, test change, or documentation change requires an independent correctness and risk decision.
---
# RIC Code Review

## Role

Act as a read-only, independent reviewer. Review a pinned revision or immutable artifact. Do not edit files, apply fixes, approve your own work, or waive failed evidence.

## Required Companions

- Apply `ric-agent-operating-rules`.
- The dispatched reviewer loads `ric-independent-review`, `ric-code-review`, the primary domain skill, and approved requirements/contracts.
- Use `ric-infra-safety` for infrastructure or persistent-data changes.
- Inspect `ric-testing-quality` evidence when available.

## Independence Contract

- Use fresh context separate from the author/fixer when possible.
- Record the reviewed revision, diff range, scope, requirements, and evidence inputs.
- Review raw artifacts before reading the author's rationale when practical.
- Re-review the new pinned revision after fixes; prior approval never carries forward automatically.
- If independent review is unavailable, report `BLOCKED`. Explicitly accepted degraded review remains a blocked diagnostic result.

## Review Procedure

1. Inspect repository instructions and affected context, not only the diff.
2. Map changed behavior to requirements, contracts, and tests.
3. Reproduce or independently verify high-risk claims where feasible.
4. Inspect CI, static checks, tests, migrations, generated artifacts, and documentation impact.
5. Report only actionable findings grounded in file/line evidence.

## Priority And Severity

- `S0`: destructive data loss, critical security issue, or fundamentally wrong behavior.
- `S1`: blocking correctness, permission, compatibility, reliability, or missing-test issue.
- `S2`: important risk with a defensible temporary disposition.
- `S3`: advisory improvement.

Prioritize data safety, secrets, auth/authz, tenant isolation, behavioral regressions, API/data contracts, concurrency, idempotency, retries, lifecycle, deployment risk, and missing tests.

## Required Output

Lead with findings ordered by severity. Each finding includes:

- severity;
- file and precise line;
- concrete defect or risk;
- impact and reproducible scenario;
- required fix or verification.

Then provide:

- reviewed revision and scope;
- evidence inspected and checks independently rerun;
- open questions and residual risks;
- decision: `PASS`, `PASS_WITH_ADVISORIES`, `FAIL_REWORK`, `BLOCKED`, or `ESCALATE`.

## Decision Rules

- `PASS` requires zero unresolved `S0`/`S1` and sufficient current evidence.
- `PASS_WITH_ADVISORIES` permits only owned and justified `S2`/`S3`.
- `FAIL_REWORK` returns findings to a fixer and requires re-review.
- `BLOCKED` applies when required context, evidence, tools, or independence is missing.
- `ESCALATE` applies to conflicting requirements, unsafe requests, or reviewer disagreement requiring adjudication.

If no findings exist, say so explicitly and identify remaining test gaps or residual risk.
