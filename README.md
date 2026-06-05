# RIC Skills

RIC Skills is a personal Agent Skills repository based on [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill), customized for RIC workflows, Windows/PowerShell development, pnpm/FNM Node projects, shared infrastructure safety, and Chinese enterprise admin-console design.

This repository keeps the upstream taste-skill design capabilities, renames them into `ric-*` install names, adds a shared RIC strengthening layer, and adds new engineering skills for infrastructure, backend services, data pipelines, API design, testing, code review, deployment, documentation, and admin systems.

## Attribution

This project is derived from `Leonxlnx/taste-skill`, licensed under MIT. See [NOTICE.md](NOTICE.md) and [LICENSE](LICENSE).

## Installing

Install all skills:

```powershell
npx skills add https://github.com/lichong-a/ric-skills
```

Install one skill by install name:

```powershell
npx skills add https://github.com/lichong-a/ric-skills --skill "ric-admin-console"
npx skills add https://github.com/lichong-a/ric-skills --skill "ric-design-taste-frontend"
```

The install name is the `name:` field in each `SKILL.md`, not necessarily the folder name.

## Skill Selection

Use the most specific skill for the task:

- Use `ric-admin-console` for admin panels, CRUD consoles, permissions, tables, back offices, operations consoles, workflow systems, and Chinese enterprise management UI.
- Use `ric-design-taste-frontend` for landing pages, portfolios, marketing pages, and visual redesigns.
- Use `ric-image-to-code` when a screenshot or generated design reference must be analyzed and implemented.
- Use `ric-infra-safety` for Elasticsearch, Kafka, TimescaleDB/PostgreSQL, Redis, NATS, MinIO, migrations, schemas, topics, indices, keys, and storage.
- Use `ric-node-pnpm` for Node/FNM/pnpm work.
- Use `ric-full-output-enforcement` when an agent must produce complete unabridged artifacts.

## Skills

### Upstream-Derived Design Skills

| Folder | Install name | Use for |
| --- | --- | --- |
| `ric-design-taste-frontend` | `ric-design-taste-frontend` | Anti-slop landing pages, portfolios, marketing pages, visual redesigns. Hands admin-console work to `ric-admin-console`. |
| `ric-design-taste-frontend-v1` | `ric-design-taste-frontend-v1` | Backward-compatible v1 taste-skill behavior with RIC constraints. |
| `ric-gpt-taste` | `ric-gpt-taste` | Stricter GPT/Codex premium frontend execution and motion-heavy marketing surfaces. |
| `ric-image-to-code` | `ric-image-to-code` | Image-first design analysis and implementation; admin screenshots route to `ric-admin-console`. |
| `ric-imagegen-frontend-web` | `ric-imagegen-frontend-web` | Website reference images only. |
| `ric-imagegen-frontend-mobile` | `ric-imagegen-frontend-mobile` | Mobile app screen reference images only. |
| `ric-brandkit` | `ric-brandkit` | Brand-kit boards, logo directions, identity systems, palettes, typography, mockups. |
| `ric-redesign-existing-projects` | `ric-redesign-existing-projects` | Redesign existing websites, apps, and admin systems after audit. |
| `ric-high-end-visual-design` | `ric-high-end-visual-design` | Premium visual UI direction with strong anti-generic rules. |
| `ric-full-output-enforcement` | `ric-full-output-enforcement` | Complete output enforcement, no placeholders or omitted files. |
| `ric-minimalist-ui` | `ric-minimalist-ui` | Clean editorial minimal product UI. |
| `ric-industrial-brutalist-ui` | `ric-industrial-brutalist-ui` | Industrial/brutalist/tactical telemetry UI. |
| `ric-stitch-design-taste` | `ric-stitch-design-taste` | Google Stitch-compatible semantic DESIGN.md generation. |

### RIC Native Skills

| Folder | Install name | Use for |
| --- | --- | --- |
| `ric-admin-console` | `ric-admin-console` | Chinese enterprise admin systems, CRUD, permissions, tables, workbench, detail pages, profile center, workflow, logs, settings. |
| `ric-agent-operating-rules` | `ric-agent-operating-rules` | Baseline agent behavior: skill retrieval, PowerShell, non-destructive work, verification. |
| `ric-infra-safety` | `ric-infra-safety` | Shared infrastructure reuse, ric namespace rules, secrets, non-destructive data operations. |
| `ric-node-pnpm` | `ric-node-pnpm` | Node 24/FNM/pnpm 11 workflows and lockfile hygiene. |
| `ric-backend-service` | `ric-backend-service` | Backend services, workers, health checks, config, auth, logging, shared infrastructure connections. |
| `ric-data-pipeline` | `ric-data-pipeline` | Kafka/NATS/Redis/TimescaleDB/Elasticsearch data pipelines, idempotency, retries, backfills. |
| `ric-api-design` | `ric-api-design` | API contracts, pagination, sorting, errors, permissions, compatibility. |
| `ric-testing-quality` | `ric-testing-quality` | Unit/integration/E2E/visual/static/build verification. |
| `ric-code-review` | `ric-code-review` | Review diffs for bugs, regressions, safety, permissions, missing tests. |
| `ric-deployment-ops` | `ric-deployment-ops` | Build, release, config, health checks, rollback, CI/CD, ops readiness. |
| `ric-docs` | `ric-docs` | README, runbooks, API docs, admin docs, changelogs, handoff notes. |

## Admin Console Defaults

`ric-admin-console` supports:

- Left sidebar layout with logo on top and user controls at the bottom.
- Top navigation layout with fixed header, logo left, user controls right.
- Sidebar plus fixed topbar layout with optional announcements, unread messages, global search, shortcuts, or tenant context in the topbar center.
- Breadcrumbs with upward navigation.
- Profile dropdown with personal information, system settings, logout, and optional security/message/theme entries.
- Authenticated, unauthenticated, permission-denied, session-expired, and partial-permission states.
- Grouped collapsible menus with route-active state.
- Workbench default page.
- List pages with query cards, table cards, create/edit/delete, sorting, pagination, cross-page selection, column settings, refresh, import/export.
- Detail pages, profile center, permissions, approval workflows, dashboards, settings, audit logs, messages, import/export, async task center, and error pages.

The default visual direction is refined Chinese enterprise admin UI: clear, compact, trustworthy, information-dense, and production-oriented.

## Local Registry

PowerShell:

```powershell
.\skill.ps1 ric-admin-console
.\skill.ps1 ric-design-taste-frontend
```

Bash:

```bash
./skill.sh ric-admin-console
./skill.sh ric-design-taste-frontend
```

## Development Notes

- Keep `SKILL.md` frontmatter to `name` and `description`.
- Keep install names lowercase and hyphenated.
- Preserve upstream attribution when updating derived skills.
- Validate skill frontmatter after edits.
- Prefer detailed execution protocols over vague "best practice" advice.
