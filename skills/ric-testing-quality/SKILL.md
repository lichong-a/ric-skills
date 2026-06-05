---
name: ric-testing-quality
description: "RIC testing and quality skill. Use for unit, integration, E2E, visual, accessibility, static analysis, build verification, regression coverage, test selection, and acceptance checks across frontend, backend, admin-console, API, and data-pipeline work."
---
# RIC Testing And Quality

Use this skill to decide and run verification.

## Test Selection

Match tests to risk:

- Small pure function: unit test.
- API handler/service: unit + integration.
- Data pipeline: idempotency/retry/schema tests.
- Admin UI: component/page tests plus visual/manual browser check.
- Auth/permission: explicit denied/allowed tests.
- Migration/config: dry-run or validation tests.

## Frontend Checks

Verify:

- Build passes.
- Lint/typecheck passes.
- Key user flows work.
- Loading/empty/error states render.
- Responsive layouts do not break.
- Admin tables/modals/forms match `ric-admin-console` acceptance checks.

Use browser screenshots for meaningful UI changes when app can run.

## Backend Checks

Verify:

- Unit/integration tests.
- API contract behavior.
- Validation failures.
- Permission failures.
- External dependency failures.
- Health checks.

## Data Checks

Verify:

- No destructive operations.
- Namespace compliance.
- Idempotency.
- Retry/dead-letter behavior.
- Backfill resumability when relevant.

## Commands

Use existing scripts first:

```powershell
pnpm test
pnpm lint
pnpm build
```

For other stacks, inspect project docs and manifests before choosing commands.

## Reporting

Report:

- Commands run.
- Results.
- Tests not run and why.
- Residual risks.

