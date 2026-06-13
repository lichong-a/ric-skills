# Independent Review Contract

## Decision Rules

- `PASS`: complete evidence and no unresolved findings.
- `PASS_WITH_ADVISORIES`: only accepted `S2` or `S3` findings remain.
- `FAIL_REWORK`: one or more actionable findings require a new artifact version.
- `BLOCKED`: required artifact, evidence, capability, or environment is unavailable.
- `ESCALATE`: reviewers conflict, risk acceptance is required, or three loops are exhausted.

## Severity Rules

- `S0`: critical safety, security, data-loss, or fundamentally invalid outcome.
- `S1`: blocking correctness, design, permission, test, or validation defect.
- `S2`: important issue requiring owner and explicit disposition.
- `S3`: advisory improvement.

## Multi-Reviewer Rules

- Use two reviewers for requirements, design, and critical gates.
- Reviewers work independently before seeing each other's conclusions.
- An adjudicator resolves incompatible conclusions.
- The artifact owner cannot adjudicate.
- Bind re-review to the new artifact version and verify prior findings plus regression risk.
- Stop after three review/fix loops and return `ESCALATE`.
