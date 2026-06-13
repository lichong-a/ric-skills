---
name: ric-deployment-ops
description: Use when a verified change must be packaged, released, rolled out, monitored, rolled back, or assessed for production readiness through CI/CD or runtime operations.
---
# RIC Deployment And Operations

## Role

Own release readiness and deployment execution when explicitly requested. Consume approved evidence; do not waive failed review, test, safety, or documentation gates.

## Required Companions

- Apply `ric-agent-operating-rules` and `ric-infra-safety`.
- Require current `ric-code-review`, `ric-security-review`, `ric-testing-quality`, `ric-acceptance-validation`, and `ric-docs` evidence.
- Use the primary domain skill for service-specific operational behavior.

## Release Inputs

Require:

- immutable artifact identifier and source revision;
- approved requirements and release scope;
- test, review, security, and acceptance decisions;
- environment/configuration diff and secret sources;
- migration sequence and safety classification;
- rollout strategy, rollback plan, health thresholds, and ownership.

## Go/No-Go Gate

Do not release unless:

- mandatory gates pass on the release revision;
- artifacts are reproducible and integrity-identifiable;
- required configuration and secrets exist without being exposed;
- migrations are additive, ordered, verified, and recoverable;
- health/readiness, monitoring, alerting, and operator ownership are defined;
- rollback triggers and stop conditions are measurable.

## Rollout Contract

- Use the repository's established strategy: feature flag, canary, blue-green, rolling, or equivalent.
- Deploy the smallest safe scope first.
- Check health, errors, latency, saturation, and domain success metrics after each step.
- Stop automatically or manually when declared thresholds fail.
- Preserve data and audit evidence during rollback.

## Rollback Contract

- Define what rolls back, what remains forward-only, and how compatibility is preserved.
- Test rollback or a realistic recovery procedure before production when feasible.
- Never rely on destructive schema or data removal.
- Record rollback decision authority and verification steps.

## Required Evidence

Produce:

- go/no-go decision and approver;
- artifact, revision, environment, and deployment timestamps;
- executed steps and observed health metrics;
- migration and rollback verification;
- incidents, deviations, residual risks, and follow-up owners;
- final decision: `PASS`, `PASS_WITH_ADVISORIES`, `FAIL_REWORK`, `BLOCKED`, or `ESCALATE`.

## Exit Criteria

Pass only when rollout health meets declared thresholds and rollback/recovery remains viable. A missing gate, secret, owner, observable threshold, or safe migration blocks release.
