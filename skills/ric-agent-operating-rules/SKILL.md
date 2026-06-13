---
name: ric-agent-operating-rules
description: Use when performing any task in a RIC workspace or when repository work must preserve user changes, follow the configured Windows runtime, and apply RIC safety constraints.
---
# RIC Agent Operating Rules

## Role

Act as an always-on policy skill. Define execution constraints; do not orchestrate delivery stages, approve work, or replace a domain skill.

## Required Companion Skills

- Retrieve the primary domain skill before editing.
- Use `ric-node-pnpm` for Node.js dependency, runtime, or script work.
- Use `ric-infra-safety` before any infrastructure or persistent-data operation.
- Use `ric-testing-quality` for a formal test gate.
- Use `ric-code-review` only through an independent reviewer.

## Start Contract

Before acting:

1. Perform skill retrieval for the task.
2. Inspect repository instructions, status, manifests, conventions, and relevant files.
3. Record scope, non-goals, known user changes, required checks, and blockers.
4. Choose one primary domain skill. Treat policy and quality skills as companions, not competing executors.

## Host And Command Rules

- Prefer PowerShell for commands executed on Windows.
- Set `$env:PYTHONUTF8='1'` before every Python command.
- Prefer `rg` and `rg --files` for search.
- When network requests fail, retry with proxy `http://127.0.0.1:7897` when appropriate.
- Prefer Bash for reusable scripts committed to a repository unless project conventions require another language.
- Use temporary runtime changes. Never change user-wide defaults.

## Repository Integrity

- Read existing patterns before editing.
- Preserve user and concurrent-agent changes.
- Keep edits within assigned scope.
- Never use destructive Git commands unless explicitly requested.
- Do not leave placeholders, incomplete implementations, or fabricated verification claims.
- Bind review and verification evidence to the current revision or artifact version.

## Runtime And Secrets

- Node.js is managed through FNM; default Node is 24.x.
- Never run `fnm default *` or modify user-wide FNM configuration.
- Prefer pnpm 11.x and existing workspace-aware commands.
- Never hardcode secrets. Use environment variables or the repository's secret mechanism.
- Stop and report a blocker when a required secret is missing.

## Data And Infrastructure Safety

- Reuse existing shared infrastructure before proposing new services.
- Never perform destructive operations against persistent data, caches, queues, search indices, or storage.
- Apply RIC namespace isolation to writable resources.
- Treat nonconforming resources as read-only external assets.

## Required Output

At handoff, report:

- selected primary and companion skills;
- changed scope and preserved user changes;
- commands and tools used;
- verification evidence tied to the current revision;
- blockers, untested areas, and residual risks.

## Exit Criteria

Exit only when assigned work is complete, required checks have run, and claims are supported by evidence. A missing tool, secret, independent reviewer, or required check is `BLOCKED`, not a synthetic pass.
