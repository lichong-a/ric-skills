# Security Review Rubric

Check applicable areas:

- Authentication, session lifecycle, account recovery, and third-party identity.
- Authorization, RBAC/ABAC, tenant boundaries, object-level access, and privilege escalation.
- Validation, injection, request forgery, upload handling, unsafe parsing, and output encoding.
- Secrets, tokens, credentials, logs, traces, analytics, and error exposure.
- Data classification, encryption, retention, export, deletion, and audit trails.
- Concurrency, replay, idempotency, rate limits, abuse, denial of service, and resource exhaustion.
- Dependencies, lockfiles, build inputs, generated artifacts, and supply-chain risk.
- Infrastructure namespace rules, non-destructive operations, migrations, backups, and rollback.

Findings must name the threat, affected asset, exploit path, impact, evidence, and required remediation. Lack of evidence is not evidence of safety.
