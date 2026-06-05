---
name: ric-backend-service
description: "RIC backend service implementation skill. Use for creating or modifying server applications, APIs, jobs, workers, integrations, service configuration, health checks, logging, error handling, auth boundaries, persistence, messaging, and shared infrastructure connections while following ric safety and namespace rules."
---
# RIC Backend Service

Use this skill for backend services, API servers, workers, scheduled jobs, and integrations.

## First Pass

Inspect:

- Language and framework.
- Dependency manager.
- Configuration pattern.
- Entry points.
- Routing/API layer.
- Persistence layer.
- Logging and error handling.
- Auth and permission model.
- Test structure.
- Deployment files.

## Configuration

- Use configuration files and environment variables.
- Keep secrets out of code.
- Document required environment variables.
- Use typed/validated configuration when the stack supports it.
- Separate local/dev/test/prod settings.

## Infrastructure

Use `ric-infra-safety` whenever connecting to shared services.

Rules:

- Reuse existing shared infrastructure.
- Use ric-prefixed writable resources.
- Do not run destructive operations.
- Add connection timeouts.
- Add bounded retries.
- Log connection failures without leaking secrets.

## API And Service Design

- Keep handlers thin.
- Put business logic in services/domain modules.
- Keep repository/data-access boundaries explicit.
- Validate inputs at boundaries.
- Return consistent error shapes.
- Add request IDs/correlation IDs when local conventions support them.
- Keep backward compatibility unless the user asks for a breaking change.

## Auth And Permissions

- Authenticate before protected operations.
- Authorize per operation, not just per route.
- Treat admin-only and destructive operations carefully.
- Do not rely only on frontend permission hiding.

## Observability

- Add structured logs where supported.
- Include operation name and key identifiers.
- Do not log secrets or full credentials.
- Add health/readiness endpoints for services.
- Add metrics/tracing hooks when the project already has them.

## Testing

Add or update tests for:

- Input validation.
- Successful operation.
- Permission denied.
- Not found.
- External dependency failure.
- Idempotency/retry behavior when relevant.

Run the repo's test/build/static checks before finishing.

