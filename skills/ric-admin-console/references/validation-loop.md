# Independent UI Verification Loop

Use this loop after implementing or substantially changing a runnable admin UI. It separates visual evidence from behavioral evidence and requires fresh-context reviewers. Do not replace it with terminal-only validation, implementation-agent self-review, or screenshots that claim to prove interactions.

## Independent Roles

- **Visual reviewer**: reads `ric-visual-design-review`, the approved visual direction, and the relevant domain/framework skills. Reviews screenshots and rendered states without modifying production code.
- **Design QA reviewer**: reads `ric-design-qa` when a design source, source screenshot, ImageGen direction, or approved reference exists. Compares source and implementation at matched dimensions.
- **Interaction validator**: reads `ric-acceptance-validation`, `acceptance.json`, and this domain skill. Operates the real UI and records actions, assertions, and outcomes without modifying production code.
- **Fixer**: receives scoped findings, modifies the implementation, and cannot approve the resulting revision.

Every result must identify the source revision or artifact version it reviewed. A new revision invalidates affected prior evidence.

## Required Loop

1. **Skill point inventory**: list the task-relevant requirements from `ric-admin-console` and any triggered UI/design/image/framework skills: layout, menu, auth, permissions, breadcrumbs, page header, loading, table, modal/drawer, scrollbar, generated assets, and framework component rules.
2. **Static checks**: run available lint, test, build, typecheck, and framework-specific checks.
3. **Browser run**: start or reuse the dev/preview server. If the preferred port is busy, use another port. In Codex, prefer the Browser plugin. In other agent environments, use Playwright, Cypress, Puppeteer, IDE browser preview, or another available browser automation surface.
4. **Visual evidence matrix**: the visual reviewer captures screenshots for relevant pages, states, and viewports. Minimum desktop viewports are `1366x768`, `1440x900`, and `1920x1080`; add mobile/narrow viewports when responsive behavior is in scope.
5. **Behavioral evidence matrix**: the interaction validator executes browser actions and assertions for routes, permissions, state restoration, forms, loading, responsive behavior, and accessibility. Screenshots may accompany evidence but cannot replace assertions.
6. **Independent comparison**: reviewers compare evidence against the skill point inventory, approved design artifacts, acceptance criteria, and `acceptance-checklist.md`.
7. **Fix loop**: if any mismatch appears, assign a fixer, rerun affected tests and required full suites, reload the browser, and repeat affected visual/design/interaction gates. Default to three rounds. If the same finding makes no progress twice, reviewers conflict, or scope changes materially, escalate to an adjudicator or the user.
8. **Final evidence**: report reviewer roles, bound source revision/artifact version, checked pages/states, viewport sizes, interaction assertions, issues found, fixes made, loop count, evidence paths, and residual risk.

## Minimum Screenshot Coverage

Capture every relevant item below:

- Login page, unauthenticated state, or session-expired state when auth is in scope.
- Workbench/default page when the system has a default entry.
- Main list page with initial loading, empty, data, multi-select, batch delete, column settings, refresh, and pagination/infinite-scroll state as applicable.
- Detail page or detail modal/drawer when detail behavior exists.
- Create/edit modal or drawer, including long-content overflow.
- Long sidebar menu, wide/long table, long dropdown, modal body, and drawer body for scrollbar and double-scrollbar checks.
- Permission-denied, hidden action, disabled action, or 403 state when RBAC/menu permissions are in scope.
- Generated asset placements: logo, app icon, avatar, background, empty-state image, announcement/banner, login visual panel, workbench/module texture.
- Locale/theme states when implemented: language switch, translated menu/breadcrumb/table/form strings, light theme, dark theme, and system/default theme behavior.
- Public portal or user-facing surfaces when the admin system includes them.
- Public portal, login, invite, registration, tenant welcome, and immersive workbench surfaces must include at least one mobile viewport.
- Advanced motion or WebGL/canvas surfaces require video or motion trace, performance profile, reduced-motion evidence, and a nonblank canvas/WebGL assertion.

## Visual Review Scope

Check screenshots for:

- Layout mode, fixed header/sidebar behavior, menu grouping, active state, collapse state, and profile dropdown.
- Breadcrumb and title/header spacing is clear; page title appears once; create action appears once; selection clear action appears once.
- Skeleton-first loading appears before data; visible data refresh uses spinner plus concise Chinese loading text.
- Tables show sorting state, pagination/infinite-scroll state, column settings, row actions, selection, and permission-aware batch delete.
- Modal/drawer/form states include title, body, action area, validation, submit loading, success/failure, and internal scrolling when needed.
- Scrollbars are hidden when unnecessary and polished when visible: transparent track, semi-transparent rounded thumb, thin width, no arrows, no double scrollbar.
- Generated assets render from project paths, do not cover text/actions, do not contain fake UI copy, and match the Brand Asset Pack.
- Multilingual UI has no untranslated visible strings in the checked scope, no desktop button wrapping caused by longer translations, and locale-aware date/number/currency formatting.
- Theme switching preserves contrast and hierarchy for LOGO, avatar, generated assets, charts, table selected/hover rows, modal masks, dropdowns, skeletons, and scrollbars.
- Portal or user-facing surfaces show stronger brand expression when required, while CRUD/permission/audit/settings/detail pages remain utility-first.
- Framework-specific component composition follows the triggered skill: shadcn/AntD/Element/Naive/Arco components, tokens, spacing, accessibility, and validation patterns.

## Interaction Validation Scope

Use real browser actions and assertions to prove:

- Parent breadcrumb clicks navigate upward; fallback parent-route navigation works when history is unavailable.
- Detail -> list return preserves filters, sorting, pagination, selected tab, and scroll state as required.
- Menus, profile dropdown, modal, drawer, search, reset, refresh, column settings, pagination, selection, clear-selection, batch actions, and confirmation flows work.
- Hidden, disabled, and allowed actions match route, menu, button, tenant, and server-side permissions.
- Keyboard navigation, focus order, focus return, form validation, loading locks, submit success/failure, and destructive confirmation work.
- Session expiration, authentication redirect, 403/no-permission, and unauthenticated states behave as specified.
- Responsive navigation and content interactions work at required narrow/mobile viewports.
- No interaction depends only on screenshots, visual inference, or front-end hiding of sensitive operations.

## Blocking And Fallback

If independent browser verification cannot be completed:

- State the exact blocker: project cannot start, dependency install failed, missing env secret, missing backend/mock, unavailable browser automation, auth cannot be completed, or no independent reviewer capability exists.
- Use the strongest available substitute: static render tests, storybook screenshots, Playwright/E2E screenshots, component snapshots, DOM inspection, or build artifacts.
- Mark the affected gate `BLOCKED` or request explicit acceptance of degraded mode.
- Do not claim visual, behavioral, or independent verification passed unless the corresponding evidence was actually collected by an eligible reviewer.
