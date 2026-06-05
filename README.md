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

- Use `ric-admin-console` for admin panels, CRUD consoles, permissions, tables, back offices, operations consoles, workflow systems, Chinese enterprise management UI, branded admin login pages, visual workbenches, SaaS console homepages, dashboard first screens, actionable breadcrumbs with return-state preservation, skeleton-first loading states, RBAC/menu/SSO planning questions, active ImageGen brand asset packs, shadcn-first React admin implementation, optional Ant Design fallback by user choice or existing project convention, framework-specific UI skill routing, deduplicated list pages, polished scrollbars, browser screenshot validation loops, and admin-specific generated assets.
- Use `ric-design-taste-frontend` for public landing pages, portfolios, marketing pages, and visual redesigns. It routes admin-console work to `ric-admin-console`, including admin pages that need strong brand expression.
- Use `ric-image-to-code` when a screenshot or generated design reference must be analyzed and implemented.
- Use `ric-infra-safety` for Elasticsearch, Kafka, TimescaleDB/PostgreSQL, Redis, NATS, MinIO, migrations, schemas, topics, indices, keys, and storage.
- Use `ric-node-pnpm` for Node/FNM/pnpm work.
- Use `ric-full-output-enforcement` when an agent must produce complete unabridged artifacts.

## Image Generation Fallback

RIC image-generation skills prefer the agent's built-in image generation capability when it exists. If the built-in image tool, MCP image tool, IDE image tool, or agent-native image capability is missing or unavailable, they should use the bundled CLI fallback documented in [references/ric-imagegen-fallback.md](references/ric-imagegen-fallback.md).

The CLI fallback requires `OPENAI_API_KEY` in the environment. Do not hardcode keys.

## Skills

### Upstream-Derived Design Skills

| Folder | Install name | Use for |
| --- | --- | --- |
| `ric-design-taste-frontend` | `ric-design-taste-frontend` | Anti-slop landing pages, portfolios, marketing pages, visual redesigns. Hands admin-console work, including branded admin login/workbench screens, to `ric-admin-console`. |
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
| `ric-admin-console` | `ric-admin-console` | Chinese enterprise admin systems, CRUD, permissions, tables, branded login pages, visual workbenches, SaaS console homepages, actionable breadcrumbs, skeleton-first loading, RBAC/menu/SSO planning, shadcn-first React stack, optional Ant Design fallback, framework-specific UI skill routing, active ImageGen brand assets, browser screenshot validation loops, list-page quality, detail pages, profile center, workflow, logs, settings. |
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
- Breadcrumbs with upward navigation, fallback parent routes, and preserved list filters/sorting/pagination/tab/scroll state when returning from detail pages.
- Profile dropdown with personal information, system settings, logout, and optional security/message/theme entries.
- Authenticated, unauthenticated, permission-denied, session-expired, and partial-permission states.
- Grouped collapsible menus with route-active state.
- Branded login pages with clear authentication path, trust cues, visual assets, and complete auth states.
- Workbench default page with dashboard hero, command header, or branded overview when it is the primary entry surface.
- List pages with query cards, table cards, create/edit/delete, sorting, pagination, cross-page selection, column settings, refresh, import/export.
- Main content page quality rules: one page title, one create action, one selection-clear action, permission-aware batch delete, no duplicated refresh/settings controls.
- Framework routing with shadcn-first React defaults; React implementations should retrieve and use the `shadcn` skill, while Ant Design/antd is a secondary path for explicit user choice or existing AntD projects; Element Plus, Naive UI, and Arco keep their matching retrieval rules.
- Detail pages, profile center, permissions, approval workflows, dashboards, settings, audit logs, messages, import/export, async task center, and error pages.
- Planning-stage confirmation of RBAC, menu management, organization/tenant/data permissions, third-party login/SSO, audit, messaging, import/export, and async task needs when scope is unclear.
- Skeleton-first loading: shell renders first, then card/table/detail/chart/avatar/media placeholders, with data loading spinners plus clear Chinese text for visible waits.
- Active ImageGen asset planning and generated or existing bitmap assets for a coherent Brand Asset Pack: logo/mark, app icon, module icon style, login/workbench/module backgrounds, empty states, announcements, onboarding, report covers, default avatars, profile placeholders, and subtle dashboard textures when brand/design-system assets are insufficient.
- Polished scrollbar and overflow behavior: no double scrollbars, hidden when unnecessary, transparent track, semi-transparent rounded thumb, thin width, and no arrows.
- Browser screenshot validation loop for runnable UI work: start or reuse the app, capture key pages/states at `1366x768`, `1440x900`, and `1920x1080`, compare screenshots against skill requirements, fix mismatches, and repeat until complete or an external blocker is reported.

The default visual direction is refined Chinese enterprise admin UI: clear, compact, trustworthy, information-dense, production-oriented, and capable of productized brand expression on login pages, workbench first screens, module homepages, onboarding, dashboard first screens, and command-center surfaces. Ordinary CRUD, permissions, audit logs, settings, and detail pages remain utility-first.

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
