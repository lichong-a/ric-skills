---
name: ric-node-pnpm
description: Use when a task changes Node.js versions, JavaScript or TypeScript dependencies, package-manager state, workspace scripts, lockfiles, or pnpm monorepo configuration.
---
# RIC Node And pnpm

## Role

Own Node.js runtime and package-management decisions. Do not choose application architecture or approve the final delivery gate.

## Required Companions

- Apply `ric-agent-operating-rules`.
- Use the detected framework or domain skill for application changes.
- Hand verification to `ric-testing-quality` when dependency or script changes affect delivery.

## Inputs

Inspect before changing anything:

- `package.json`, workspace manifests, and existing scripts;
- `pnpm-lock.yaml`, other lockfiles, `.npmrc`, and package-manager fields;
- `.node-version`, `.nvmrc`, `.tool-versions`, and `engines`;
- current `fnm`, Node, pnpm, and Corepack state.

## Runtime Contract

- Node is managed by FNM; default Node is 24.x.
- Never run `fnm default *` or modify user-wide FNM configuration.
- Use `fnm use <version>` or `fnm exec --using <version> -- <command>` temporarily.
- Prefer pnpm 11.x and workspace-aware commands.
- Do not introduce `package-lock.json` or another package manager unless the repository already uses it or the user explicitly requests migration.

## Dependency Contract

- Reuse existing packages before adding dependencies.
- Add the smallest justified dependency surface.
- Do not introduce a second UI, state, testing, logging, or build system for a narrow need.
- Preserve peer-dependency and workspace-version conventions.
- Explain security-sensitive, native, postinstall, or supply-chain-sensitive additions.
- Do not silence install warnings without understanding them.

## Procedure

1. Record current runtime and package-manager state.
2. Determine the repository's authoritative package manager and Node range.
3. Make the minimal dependency or script change.
4. Update only the authoritative lockfile.
5. Run affected scripts and inspect lockfile diff for unexpected churn.

## Evidence

Report:

- Node and pnpm versions used;
- manifests and lockfiles changed;
- dependencies added, removed, or upgraded with rationale;
- install, lint, typecheck, test, and build results;
- warnings, compatibility risks, and unverified platforms.

## Exit Criteria

Pass only when runtime changes are temporary, lockfile state is coherent, relevant scripts pass, and no unintended package-manager artifacts exist.
