---
name: ric-agent-operating-rules
description: "RIC operating rules for coding agents. Use for any ric-skills or ric workspace task to enforce skill retrieval, Windows PowerShell preference, non-destructive execution, repository-first inspection, temporary runtime changes, user-data preservation, and verification before completion."
---
# RIC Agent Operating Rules

Use this skill as the baseline behavior for ric work.

## Required Start

1. Perform skill retrieval every time before work.
2. Inspect the repository before making decisions.
3. Prefer `rg` / `rg --files` for search.
4. Prefer PowerShell syntax for commands on Windows.
5. Avoid Bash-only commands unless the user asks or the repo requires them.

## Runtime Rules

- Node.js is managed through FNM.
- Default Node is 24.x.
- Never run `fnm default *`.
- Never modify user-wide FNM configuration.
- Use `fnm use <version>` or `fnm exec --using <version> -- <command>` for temporary version needs.
- Prefer pnpm 11.x for Node projects.
- Prefer workspace-aware pnpm commands.
- Avoid npm lockfiles unless the project already uses npm.

## Repository Rules

- Read existing patterns before editing.
- Prefer existing framework, UI library, request client, state management, logging, testing, and styling conventions.
- Keep changes scoped to the request.
- Do not revert user changes.
- Do not use destructive git operations unless explicitly requested.
- Do not leave placeholders, TODO stubs, or partial implementations.

## Data Safety

- Reuse existing shared infrastructure before creating anything new.
- Never run destructive operations against databases, caches, message systems, or storage.
- Follow ric namespace rules for writable resources.
- Use environment variables for secrets.
- Stop and ask when required secrets are missing.

## Verification

Before finishing:

- Run relevant lint/test/build/static checks when available.
- For UI work, verify key layouts visually when the app can run.
- For skill work, validate frontmatter and install names.
- Report what was changed and what was verified.

