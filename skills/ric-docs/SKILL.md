---
name: ric-docs
description: "RIC documentation skill. Use for README files, setup guides, runbooks, API docs, architecture notes, change logs, deployment docs, admin-console usage docs, environment variable documentation, and handoff notes for ric projects."
---
# RIC Documentation

Use this skill for project and operational documentation.

## Principles

- Write for the next engineer or operator.
- Keep docs accurate to the repo.
- Prefer commands that work in PowerShell on Windows.
- Include pnpm commands for Node projects.
- Never include real secrets.
- Document environment variables by name.

## README Structure

Recommended:

1. Project purpose.
2. Tech stack.
3. Prerequisites.
4. Environment variables.
5. Install.
6. Run locally.
7. Test/build.
8. Deployment notes.
9. Important conventions.

## Runbooks

Include:

- Symptoms.
- Checks.
- Commands.
- Expected output.
- Safe remediation.
- Escalation.

Do not include destructive database/cache/message/storage commands.

## API Docs

Include:

- Endpoint/operation.
- Auth/permission.
- Request.
- Response.
- Errors.
- Pagination/filter/sort.
- Examples.

## Admin Docs

For admin systems, document:

- Roles and permissions.
- Menu structure.
- Main workflows.
- Import/export behavior.
- Audit/log behavior.
- Common failure states.

## Changelog

Keep entries concise:

- Added.
- Changed.
- Fixed.
- Security.
- Migration notes when needed.

