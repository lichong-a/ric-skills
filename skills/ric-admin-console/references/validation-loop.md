# Browser Screenshot Verification Loop

Use this loop after implementing or substantially changing a runnable admin UI. Do not replace it with terminal-only validation.

## Required Loop

1. **Skill point inventory**: list the task-relevant requirements from `ric-admin-console` and any triggered UI/design/image/framework skills: layout, menu, auth, permissions, breadcrumbs, page header, loading, table, modal/drawer, scrollbar, generated assets, and framework component rules.
2. **Static checks**: run available lint, test, build, typecheck, and framework-specific checks.
3. **Browser run**: start or reuse the dev/preview server. If the preferred port is busy, use another port. Open the real page in Browser or another available browser automation surface.
4. **Screenshot matrix**: capture screenshots for relevant pages, states, and viewports. Minimum desktop viewports are `1366x768`, `1440x900`, and `1920x1080`; add mobile/narrow viewports when responsive behavior is in scope.
5. **Visual comparison**: compare screenshots against the skill point inventory and `acceptance-checklist.md`.
6. **Fix loop**: if any mismatch appears, modify the implementation, rerun relevant static checks, reload the browser, recapture screenshots, and compare again. Repeat until all required checks pass or an external blocker is explicit.
7. **Final evidence**: report checked pages/states, viewport sizes, issues found, fixes made, loop count, and residual risk.

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

## What To Compare

Check screenshots for:

- Layout mode, fixed header/sidebar behavior, menu grouping, active state, collapse state, and profile dropdown.
- Breadcrumb parent clicks navigate upward and detail -> list preserves filters, sorting, pagination, tab, and scroll state.
- Breadcrumb and title/header spacing is clear; page title appears once; create action appears once; selection clear action appears once.
- Skeleton-first loading appears before data; visible data refresh uses spinner plus concise Chinese loading text.
- Tables show sorting state, pagination/infinite-scroll state, column settings, row actions, selection, and permission-aware batch delete.
- Modal/drawer/form states include title, body, action area, validation, submit loading, success/failure, and internal scrolling when needed.
- Scrollbars are hidden when unnecessary and polished when visible: transparent track, semi-transparent rounded thumb, thin width, no arrows, no double scrollbar.
- Generated assets render from project paths, do not cover text/actions, do not contain fake UI copy, and match the Brand Asset Pack.
- Framework-specific component composition follows the triggered skill: shadcn/AntD/Element/Naive/Arco components, tokens, spacing, accessibility, and validation patterns.

## Blocking And Fallback

If browser screenshots cannot be completed:

- State the exact blocker: project cannot start, dependency install failed, missing env secret, missing backend/mock, unavailable Browser tool, or auth cannot be completed.
- Use the strongest available substitute: static render tests, storybook screenshots, Playwright/E2E screenshots, component snapshots, DOM inspection, or build artifacts.
- Do not claim browser screenshot verification passed unless real screenshots of the runnable UI were captured and compared.
