---
name: ric-admin-console
description: "Use when creating or changing admin panels, SaaS back offices, CRUD consoles, RBAC systems, data-heavy dashboards, branded management workbenches, or public surfaces attached to an admin product."
---
# RIC Admin Console

Build Chinese enterprise admin products that are efficient in repeated work and visually distinctive where brand expression matters. This is the single primary executor for admin products, including attached login, invite, help, portal, and user-facing console surfaces.

## Role And Companions

- For non-trivial work, run under `ric-delivery-loop` as the one active primary executor.
- Apply `ric-agent-operating-rules`, `ric-infra-safety`, and the detected framework skill.
- Use `ric-design-taste-frontend` only as an optional visual modifier for public or immersive surfaces. It never redirects or approves the task.
- Use `ric-imagegen-runtime` for required bitmap assets.
- Return code, security, test, visual, Design QA, and behavioral acceptance results to the orchestrator. Never self-approve.

## Required Procedure

1. Inspect repository instructions, routes, shell, UI system, components, request client, state, auth, permissions, tests, and existing assets.
2. Record or ask the planning decisions below before design. Ask only when they cannot be inferred and materially change implementation.
3. State one concise Design Read and select `utility`, `product`, or `immersive` visual mode per major surface.
4. Retrieve the detected framework skill and official/version-specific API guidance before framework-specific code.
5. Produce locale, theme, permission, loading/state, and Asset Plans before implementation.
6. Implement through structured route/menu/permission/component data, one UI system, complete states, and server-side authorization.
7. Run static checks, independent screenshot review, Design QA when a visual source exists, and real interaction acceptance.
8. Fix every mismatch, create a new revision, and repeat affected reviews/tests/validation. Old evidence never carries forward.

## Planning Questions

Record:

- system/product title, existing LOGO, desired brand/LOGO style, and whether ImageGen should create a brand pack;
- layout: `sidebar-only`, `topnav-only`, or `sidebar-with-topbar`;
- locale mode, default and target locales, and language persistence/routing;
- theme: light, dark, or `light/dark/system`, including persistence;
- RBAC, roles, permission points, route/button permissions, menu management, tenant/data scope, and organization structure;
- local login, third-party login, SSO, OAuth/OIDC, LDAP/AD, DingTalk, Feishu, WeCom, SMS, or other identity integration;
- audit, workflow, messages, import/export, async tasks, and public/user-facing portal scope.

Defaults when the user does not decide:

- `zh-CN`, i18n-ready structure, no invented translations;
- `light/dark/system` when the stack supports it;
- `sidebar-with-topbar`;
- project name as title; generate a RIC-style mark only when no usable brand asset exists;
- local login, basic RBAC, route-derived menus, no SSO or tenant isolation unless required.

Design Read format:

```text
Reading this as: <system/users>, <layout>, <surface modes>, <density>,
<permission model>, <locale/theme>, <brand assets>, <portal scope>, <stack>.
```

## Stack Routing

- Existing project: preserve its router, UI system, tokens, state, request, auth, permission, and test conventions.
- New React or React without a mature UI system: shadcn-first with Tailwind semantic tokens, Radix/base primitives, and TanStack Table where table state needs explicit control. Retrieve `shadcn` again during implementation.
- Existing React + Ant Design/ProComponents: preserve AntD and retrieve `ant-design`/`antd`. For a new project, AntD is a user-selected secondary option.
- Vue: preserve or select the appropriate Element Plus, Naive UI, or Arco stack and retrieve matching skills when available.
- Never silently mix UI systems or invent framework props. Use project-installed or explicitly pinned CLI versions; do not silently run `@latest`.

Read [framework-adapters.md](references/framework-adapters.md) before framework-specific implementation and [i18n-patterns.md](references/i18n-patterns.md) before multilingual work.

## Visual Modes

| Mode | Surfaces | Rule |
| --- | --- | --- |
| `utility` | CRUD, permissions, audit, settings, dense detail | scanning, density, complete states, low visual drama |
| `product` | workbench, module home, SaaS console home | stronger brand hierarchy, command header, meaningful CTA |
| `immersive` | login, invite, onboarding, portal, command center, report cover | active visual assets and controlled high-impact composition |

GSAP, Three.js/WebGL, canvas, 3D, and advanced motion are allowed only where they serve orientation, brand, data comprehension, guided focus, or state change. Keep them out of ordinary utility pages, isolate cleanup, support reduced motion, and collect video/motion/performance/nonblank-canvas evidence.

Read [china-enterprise-visual-style.md](references/china-enterprise-visual-style.md) and [admin-visual-impact.md](references/admin-visual-impact.md).

## Active Asset Plan

Before implementing `product` or `immersive` surfaces, record:

```text
Asset Plan: <assets>, <existing | agent-native/MCP/IDE ImageGen | trusted CLI>,
<workspace paths>, <consuming components>, <light/dark variants>.
```

When no suitable brand/design-system asset exists, actively generate the needed logo/mark, app icon, default avatar, background, empty-state art, announcement/onboarding art, module visual, or report cover. Do not replace required bitmap assets with blank regions, fake screenshots, generic placeholder services, or decorative hand-written SVGs.

Functional operation icons normally come from one existing icon family. Generate a custom icon pack only when the user explicitly requests it or the approved brand system requires it.

Use `ric-imagegen-runtime`. Missing agent-native tooling triggers its trusted CLI fallback; missing required credentials returns `BLOCKED`.

## Shell And Page Contracts

The selected shell must support fixed regions, grouped/collapsible permission-aware menus, current-route state, profile dropdown, auth states, and one deliberate scroll owner.

Every content page requires an actionable breadcrumb. Parent clicks must navigate upward; when history is unavailable, use the parent route. Breadcrumb, page header, and content need deliberate spacing. Page title appears once.

Initial waiting content uses shape-accurate skeletons. Visible refresh/data waits use a spinner or loading indicator plus concise text. Every async area covers loading, empty, error, disabled, success, unauthenticated, and permission states as applicable.

List pages enforce:

- one current-page title and one create action;
- one selection toolbar and one `清空选择` action;
- permission-aware `批量删除` after selection, with count, scope, and confirmation;
- explicit sorting, pagination/infinite-scroll, cross-page selection, refresh, column visibility, and failure states;
- no duplicated title, create, refresh, settings, selection, or batch controls.

Scroll regions use a unified thin scrollbar: hidden when unnecessary; transparent track, semi-transparent rounded thumb, no arrows when visible; no body/main/card double scrolling.

Read [layout-patterns.md](references/layout-patterns.md), [page-patterns.md](references/page-patterns.md), and [component-contracts.md](references/component-contracts.md).

## Permission And Security Contract

- Routes, menus, buttons, bulk actions, and API authorization derive from a shared permission model.
- Hidden UI is never server-side authorization.
- Validate tenant/data scope, dangerous actions, auditability, session expiry, unauthenticated behavior, 403 states, and negative permission cases.
- Sensitive actions require clear confirmation and current-revision security evidence.

## Independent Verification

Use [validation-loop.md](references/validation-loop.md) and [acceptance-checklist.md](references/acceptance-checklist.md).

Mandatory separation:

- screenshots and `ric-visual-design-review` prove appearance and product fit;
- `ric-design-qa` compares approved sources with implementation;
- browser actions/assertions/traces and `ric-acceptance-validation` prove behavior;
- test executors, reviewers, validators, authors, and fixers remain independent.

At minimum, verify affected login/auth states, workbench, main list loading/empty/data/multi-select/batch delete, detail, long modal/drawer/sidebar/table scrolling, permissions, generated assets, locales/themes, and required desktop/mobile viewports.

If a runnable app, browser capability, backend, secret, framework documentation, ImageGen capability, or independent reviewer is unavailable, return `BLOCKED` for the affected gate. Never claim evidence that did not run.
