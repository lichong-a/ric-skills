---
name: ric-testing-quality
description: Use when changed behavior requires a formal unit, integration, contract, end-to-end, browser, accessibility, security, migration, data, performance, or build verification gate.
---
# RIC Testing And Quality

## Role

Own the formal test gate and evidence manifest. Test executors are independent from implementers, run assigned suites, and do not fix production code or approve untested behavior.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Read approved acceptance criteria, primary domain skill, and relevant safety policy.
- Use framework-specific testing skills when available.
- Return failures and final evidence to `ric-delivery-loop`; the orchestrator dispatches a separate triager/fixer and downstream gates.

## Test Plan Contract

Before execution, create a test plan that maps each acceptance criterion and major risk to:

- suite and test level;
- environment and prerequisites;
- executor/subagent role;
- command or browser flow;
- expected result and retained evidence;
- rerun and flake policy;
- explicit untested scope.

Dispatch independent test subagents by non-overlapping domain when the environment supports subagents. Each test executor loads `ric-testing-quality`, the primary domain skill, and applicable framework testing skills. Otherwise use isolated fresh-context executors and disclose degraded independence.

## Required Test Domains

Select based on risk:

- unit and component behavior;
- integration, API, schema, and contract compatibility;
- E2E and browser interaction;
- accessibility and responsive states;
- auth, authorization, tenant isolation, and security abuse cases;
- migrations, data semantics, reconciliation, replay, and backfills;
- build, lint, typecheck, packaging, startup, health, and shutdown;
- performance, load, or resource limits when risk warrants.

## Execution Integrity

- Test the pinned integrated revision.
- Record exact command, environment, duration, exit code, and artifact location.
- Do not delete tests, weaken assertions, ignore failures, or rerun only passing cases.
- Treat flaky tests as failures requiring triage; record reproduction attempts and ownership.
- Keep test data isolated and apply `ric-infra-safety` to persistent resources.
- Browser screenshots prove visual state; browser actions/assertions prove interaction behavior.

## Failure Loop

1. Executors report failures without changing production code.
2. A failure triager groups failures by probable root cause and assigns fix scope.
3. A fixer changes the implementation or tests only when the expected behavior was wrong.
4. Rerun affected tests, then the complete required suites, then recompute the gate.

## Evidence Manifest

Report:

- pinned revision and test-plan version;
- acceptance-criteria coverage matrix;
- commands, results, logs, screenshots, traces, and reports;
- failed, flaky, skipped, and untested cases with reasons;
- environment differences and residual risks;
- decision: `PASS`, `PASS_WITH_ADVISORIES`, `FAIL_REWORK`, `BLOCKED`, or `ESCALATE`.

## Exit Criteria

Return the decision only to `ric-delivery-loop`. Pass only when all mandatory suites pass, every acceptance criterion has sufficient evidence, no failure is untriaged, and advisories have owners. Missing required tools, unsafe infrastructure, or unverifiable behavior blocks the gate.
