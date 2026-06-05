---
name: ric-code-review
description: "RIC code review skill. Use when reviewing code, diffs, pull requests, architecture changes, frontend/admin UI changes, backend services, APIs, data pipelines, infrastructure changes, tests, and documentation. Prioritizes bugs, regressions, data safety, security, permissions, missing tests, and ric convention violations."
---
# RIC Code Review

Use this skill in review mode.

## Review Priority

Findings first, ordered by severity:

1. Data loss or destructive infrastructure risk.
2. Security, secrets, auth, or permission bypass.
3. Behavioral regressions.
4. Incorrect API/data contracts.
5. Admin UI permission or state gaps.
6. Reliability, idempotency, retry, concurrency issues.
7. Missing tests for changed behavior.
8. Maintainability issues that will cause near-term defects.

## What To Check

- Does the code follow existing repo conventions?
- Are user changes preserved?
- Are secrets hardcoded?
- Are ric namespace rules followed?
- Are destructive operations introduced?
- Are permissions enforced server-side?
- Are frontend buttons/routes aligned with permissions?
- Are loading/empty/error states complete?
- Are tests updated for the changed behavior?
- Are dependencies justified?

## Output Format

Lead with findings:

- Severity.
- File and line.
- Concrete issue.
- Why it matters.
- Suggested fix.

Then include:

- Open questions.
- Test gaps.
- Brief summary only after findings.

If no issues are found, say so and mention remaining risk/test gaps.

