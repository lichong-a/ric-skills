---
name: ric-full-output-enforcement
description: "RIC derivative of full-output-enforcement for complete, unabridged implementation output. Use when exhaustive code, file edits, migration steps, or long artifacts are required; forbids placeholders, omitted files, TODO stubs, and asking the user to assemble missing pieces."
---
---

## RIC Strengthening Layer

Apply these rules before the upstream-derived instructions below:

1. Perform skill retrieval before work so the most relevant installed skill guidance is available.
2. Prefer Windows PowerShell syntax for commands and examples unless the user explicitly asks for another shell.
3. For Node.js work, respect FNM-managed Node 24.x as the default. Never run `fnm default *` or change user-wide FNM configuration. Use `fnm use <version>` or `fnm exec --using <version> -- <command>` only for temporary project needs, and prefer pnpm 11.x over npm.
4. Before importing third-party packages, inspect the project manifest and use the existing framework, UI library, router, state, styling, and test conventions.
5. Reuse shared ric infrastructure before creating new services. Never perform destructive operations against databases, caches, message systems, or object storage.
6. All writable Elasticsearch indices, PostgreSQL/TimescaleDB resources, Redis keys, Kafka/NATS subjects when applicable, and storage assets must respect the ric namespace rules from `ric-infra-safety`.
7. Secrets must come from environment variables. Do not hardcode credentials or fabricate missing secrets.
8. When the request is an admin panel, management console, CRUD system, permission system, dense dashboard, Chinese enterprise back office, operations console, or table-heavy product UI, stop applying marketing-page rules and use `ric-admin-console` instead.
9. Complete the implementation or artifact fully. Do not leave TODO placeholders, omitted files, fake data without labeling, or instructions for the user to assemble missing parts.
10. Verify the result with the repository's available lint, test, build, static validation, or visual checks before declaring completion.

---
# Full-Output Enforcement

## Baseline

Treat every task as production-critical. A partial output is a broken output. Do not optimize for brevity — optimize for completeness. If the user asks for a full file, deliver the full file. If the user asks for 5 components, deliver 5 components. No exceptions.

## Banned Output Patterns

The following patterns are hard failures. Never produce them:

**In code blocks:** `// ...`, `// rest of code`, `// implement here`, `// TODO`, `/* ... */`, `// similar to above`, `// continue pattern`, `// add more as needed`, bare `...` standing in for omitted code

**In prose:** "Let me know if you want me to continue", "I can provide more details if needed", "for brevity", "the rest follows the same pattern", "similarly for the remaining", "and so on" (when replacing actual content), "I'll leave that as an exercise"

**Structural shortcuts:** Outputting a skeleton when the request was for a full implementation. Showing the first and last section while skipping the middle. Replacing repeated logic with one example and a description. Describing what code should do instead of writing it.

## Execution Process

1. **Scope** — Read the full request. Count how many distinct deliverables are expected (files, functions, sections, answers). Lock that number.
2. **Build** — Generate every deliverable completely. No partial drafts, no "you can extend this later."
3. **Cross-check** — Before output, re-read the original request. Compare your deliverable count against the scope count. If anything is missing, add it before responding.

## Handling Long Outputs

When a response approaches the token limit:

- Do not compress remaining sections to squeeze them in.
- Do not skip ahead to a conclusion.
- Write at full quality up to a clean breakpoint (end of a function, end of a file, end of a section).
- End with:

```
[PAUSED — X of Y complete. Send "continue" to resume from: next section name]
```

On "continue", pick up exactly where you stopped. No recap, no repetition.

## Quick Check

Before finalizing any response, verify:
- No banned patterns from the list above appear anywhere in the output
- Every item the user requested is present and finished
- Code blocks contain actual runnable code, not descriptions of what code would do
- Nothing was shortened to save space


