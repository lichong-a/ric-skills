---
name: ric-node-pnpm
description: "RIC Node.js, FNM, and pnpm workflow skill. Use for Node, JavaScript, TypeScript, React, Vue, Next.js, Vite, package management, dependency installation, scripts, monorepos, and workspace tasks. Enforces Node 24.x default through FNM, no global default changes, pnpm 11.x preference, PowerShell examples, and lockfile hygiene."
---
# RIC Node And pnpm Workflow

Use this skill for Node.js projects.

## Defaults

- OS: Windows 11 x64.
- Shell: PowerShell.
- Node.js: managed by FNM.
- Default Node: 24.x.
- Package manager: pnpm 11.x.

## Hard Rules

- Never run `fnm default *`.
- Never modify user-wide FNM configuration.
- Do not introduce `package-lock.json` unless the project already uses npm.
- Prefer pnpm over npm.
- Prefer workspace-aware commands in monorepos.

## Inspection

Before changing dependencies or scripts, inspect:

- `package.json`
- `pnpm-lock.yaml`
- `pnpm-workspace.yaml`
- `.npmrc`
- `.node-version`
- `.nvmrc`
- `engines`
- existing scripts
- existing lockfiles

## Commands

Check current runtime:

```powershell
fnm current
fnm default
node --version
pnpm --version
```

Temporarily use another Node version:

```powershell
fnm use <version>
```

Run a command under a specific version:

```powershell
fnm exec --using <version> -- pnpm install
```

Install dependencies:

```powershell
pnpm install
pnpm add <package>
pnpm add -D <package>
pnpm --filter <workspace-name> add <package>
```

Run scripts:

```powershell
pnpm test
pnpm lint
pnpm build
pnpm --filter <workspace-name> test
```

## Dependency Discipline

- Check existing packages before adding new ones.
- Prefer established repo conventions.
- Avoid adding a new UI, state, test, or build library for one small need.
- For frontend icons, use the existing icon family.
- Keep dependency changes minimal and justified.

## Verification

After dependency or Node-related changes:

- Run `pnpm install` if lockfile needs update.
- Run relevant scripts from `package.json`.
- Report if scripts are missing or fail.

