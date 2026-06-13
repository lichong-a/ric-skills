---
name: ric-backend-service
description: Use when creating or changing API servers, backend services, workers, scheduled jobs, integrations, persistence logic, service lifecycle, or runtime observability.
---
# RIC Backend Service

For non-trivial delivery, operate as the single primary executor under `ric-delivery-loop`; do not approve requirements, design, code review, security review, tests, or acceptance.

## Role

Own backend implementation within the approved requirements and contracts. Do not waive contract, security, review, test, or deployment gates.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Use `ric-api-design` for public or cross-component contract changes.
- Use `ric-infra-safety` before persistent-data or shared-service operations.
- Hand implementation to independent `ric-code-review` and `ric-testing-quality`.

## Inputs And First Pass

Inspect the framework, entry points, service boundaries, configuration, API contracts, auth model, persistence, transactions, messaging, observability, tests, deployment files, and shutdown behavior. Record approved acceptance criteria and affected failure modes.

## Implementation Contract

- Keep transport handlers thin and business logic explicit.
- Validate inputs and authorization at trust boundaries.
- Enforce tenant and data scope per operation.
- Define transaction boundaries and consistency expectations.
- Make retryable operations idempotent.
- Protect shared state with explicit concurrency controls.
- Propagate cancellation and deadlines.
- Set bounded outbound-call timeouts and retries with jitter/backoff.
- Preserve compatibility unless an approved contract change exists.

## Service Lifecycle

- Validate configuration at startup and fail clearly on invalid required values.
- Separate liveness from readiness.
- Do not report ready before required dependencies are usable.
- Implement graceful shutdown, stop accepting new work, drain bounded in-flight work, and release resources.
- Define startup, shutdown, retry exhaustion, and dependency-degradation behavior.
- Respect resource limits and avoid unbounded queues, payloads, or concurrency.

## Configuration And Observability

- Use typed or validated configuration and environment-based secrets.
- Emit structured logs with correlation identifiers and no secrets.
- Add metrics for request/job rate, failures, latency, retries, saturation, and dependency health when supported.
- Add traces across meaningful boundaries when the project supports tracing.
- Document operator-visible health and failure signals.

## Required Evidence

Provide:

- implementation mapped to approved acceptance criteria and contracts;
- configuration and lifecycle changes;
- unit and integration evidence for success, validation, authorization, not-found, dependency failure, timeout, cancellation, idempotency, transaction rollback, and concurrency when relevant;
- health/readiness and graceful-shutdown verification;
- residual operational and compatibility risks.

## Gate And Handoff

Independent code review must inspect the pinned diff and evidence. `ric-testing-quality` runs the formal test gate. Any implementation discovery that changes requirements or contract semantics returns to the appropriate design gate. Only evidence-backed work proceeds to documentation or deployment readiness.
