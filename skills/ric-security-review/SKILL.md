---
name: ric-security-review
description: Use when a non-trivial change touches code, data, authentication, authorization, tenants, secrets, dependencies, infrastructure, integrations, deployment, or any user-controlled input.
---
# RIC Security Review

Every non-trivial delivery requires an independent security review.

## Procedure

1. Pin the artifact version or source revision.
2. The dispatched security reviewer loads `ric-independent-review`, `ric-security-review`, the primary domain skill, and relevant infrastructure or data-safety skills.
3. Review trust boundaries, authentication, authorization, tenant/data scope, input handling, output exposure, secrets, logging, dependencies, supply chain, abuse cases, availability, and destructive-operation risk.
4. Verify server-side enforcement; hidden UI controls are not authorization.
5. Verify sensitive claims with tests, configuration, or code evidence when possible.
6. Remain read-only and return a structured gate decision only to `ric-delivery-loop`.

Read [references/security-rubric.md](references/security-rubric.md) for the minimum review surface.

## Stop Conditions

Return `FAIL_REWORK` for actionable `S0` or `S1` findings. Return `BLOCKED` when required secrets, access, or evidence are unavailable. Never waive a safety policy or fabricate evidence.
