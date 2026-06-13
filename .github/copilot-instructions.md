# RIC Skills Repository Instructions

Use `ric-delivery-loop` as the default entry for every non-trivial product or engineering delivery. Select exactly one active primary executor from `skills/catalog.json`.

Maintaining this skill repository, editing skill text, updating schemas, or making
a mechanical repository fix does not automatically require the complete delivery
loop. Use repository checks directly, then invoke `ric-skill-quality` explicitly
when final independent skill behavior evaluation is needed.

Mandatory rules:

1. Retrieve relevant skills before work.
2. Keep authors/fixers separate from fresh-context, read-only reviewers, test executors, and validators.
3. Every non-trivial delivery requires independent security review.
4. A changed source revision invalidates old code, security, test, visual, design-QA, and acceptance results.
5. During a complete delivery loop, missing independent reviewer capability means `BLOCKED`; degraded handoff never becomes PASS.
6. Use `.ric-work/<run-id>/` JSON artifacts and validate them with `scripts/validate-delivery-run.py`.
7. Preserve user changes, prefer PowerShell and pnpm/FNM rules, set `PYTHONUTF8=1`, and follow `ric-infra-safety`.
8. Never fabricate execution, screenshots, plugin calls, ImageGen output, tests, review, or evidence.

For narrow single-stage requests, use the relevant domain or quality-gate skill directly without claiming the complete delivery loop ran.
