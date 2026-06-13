# Acceptance Validation Contract

For each acceptance criterion, record:

- Criterion ID and linked requirement IDs.
- Tested source revision and artifact versions.
- Environment and prerequisites.
- Actions performed.
- Expected and actual result.
- Evidence path, screenshot, trace, log, or assertion.
- Decision and residual risk.

## Evidence Rules

- Evidence must demonstrate the claim; screenshots do not prove interactions.
- Browser behavior requires clicks, assertions, traces, or equivalent reproducible actions.
- Visual quality requires visual-review evidence.
- Missing environment, secret, data, or capability produces `BLOCKED`, not a synthetic pass.
- Stale evidence from an earlier revision is invalid.
