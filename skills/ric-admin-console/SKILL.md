---
name: ric-admin-console
description: "Chinese enterprise admin-console design and implementation skill for polished, information-dense, production-ready management systems. Use for admin panels, CRUD consoles, permission systems, data tables, workbench pages, workflow approval systems, operations consoles, SaaS back offices, and internal tools. Supports sidebar, top navigation, sidebar-plus-topbar layouts, authenticated and unauthenticated states, grouped collapsible menus, breadcrumbs, profile dropdowns, list/detail/workbench/profile/settings/audit/approval pages, modals, drawers, forms, tables, and China-market enterprise visual taste across React, Vue, and existing project stacks."
---
# RIC Admin Console Skill

Use this skill for Chinese enterprise management systems: admin panels, back offices, operations consoles, CRUD systems, permission systems, workflow approval systems, internal tools, data-heavy dashboards, and SaaS control panels.

Do not apply marketing-page taste rules here. Admin consoles are product surfaces for repeated work. Optimize for clarity, scan speed, predictable navigation, permission-aware actions, state coverage, and dense but orderly information.

## 1. Operating Protocol

1. Perform skill retrieval before work.
2. Inspect the existing project before choosing libraries: `package.json`, router, UI library, layout components, table/form stack, state management, auth/permission model, request client, mock/data layer, and styling system.
3. Prefer the existing stack. Do not replace Ant Design, Element Plus, Naive UI, Arco, or another established UI system unless the user asks.
4. Prefer PowerShell commands on Windows. Use pnpm over npm for Node projects.
5. Do not change global Node/FNM configuration. Use temporary `fnm use` or `fnm exec` only when needed.
6. Treat permissions as a first-class design input. Buttons, menus, routes, API calls, and bulk actions must have a shared permission source.
7. Provide loading, empty, error, disabled, success, and unauthenticated states for every interactive area.
8. Never create destructive database/cache/message/object-storage operations. Follow `ric-infra-safety` for infrastructure and namespace rules.
9. Finish with repository validation: lint/test/build when available, and browser or screenshot checks for layout work.

Read these references when the task needs detail:

- `references/layout-patterns.md` for shell layouts, menus, top bars, breadcrumbs, auth states.
- `references/page-patterns.md` for workbench, list, detail, profile, settings, permissions, approval, logs, messages, import/export, tasks.
- `references/component-contracts.md` for query cards, tables, pagination, modals, drawers, forms, actions, status UI.
- `references/china-enterprise-visual-style.md` for Chinese enterprise visual taste, density, Chinese typography, color, spacing, and anti-template rules.
- `references/framework-adapters.md` for React/Vue/UI-library decision rules.
- `references/acceptance-checklist.md` before declaring work complete.

## 2. Design Read

Before implementation, state one concise design read:

`Reading this as: <system type> for <user role>, with <layout mode>, <data density>, <permission complexity>, and <framework/UI library>.`

Examples:

- `Reading this as: user/role management for operations staff, with sidebar-plus-topbar layout, high table density, RBAC permissions, and React + Ant Design Pro.`
- `Reading this as: approval workflow console for department managers, with topnav-only layout, medium density, route-level permissions, and Vue 3 + Element Plus.`

Ask only one clarification if the layout mode, auth model, or framework choice cannot be inferred from the repo and materially changes implementation.

## 3. Stack Selection

Use multi-stack decision-making:

1. Existing React + Ant Design: use Ant Design, ProComponents, ProLayout, ProTable, Modal/Drawer/Form patterns already present.
2. Existing Vue + Element Plus: use Element Plus layout, menu, table, form, dialog/drawer, pagination, popconfirm patterns.
3. Existing Naive UI or Arco: stay within that library and mirror its density/token system.
4. Existing custom design system: use the local primitives and only add external packages when missing capabilities are real.
5. New React project without user preference: recommend React + Vite or Next + Ant Design + ProComponents.
6. New Vue project without user preference: recommend Vue 3 + Vite + Element Plus.

One UI system per app. Do not mix Ant Design and Element Plus, Ant Design and Material, or shadcn and ProComponents unless the repo already does so and migration is out of scope.

## 4. Visual Direction

Default to enterprise-refined Chinese admin taste:

- Clear, trustworthy, compact, and stable.
- Medium-high information density.
- Blue/neutral base with controlled semantic colors, or the product's existing brand color.
- Strong table readability, predictable action placement, consistent icons, polished empty states, and clear status tags.
- Chinese text rhythm: short labels, direct button copy, no oversized English marketing slogans.

Avoid:

- Marketing hero sections, giant slogans, decorative landing-page illustrations, large editorial typography.
- Excessive gradients, glassmorphism, huge round cards, animated backgrounds, and overbuilt motion.
- Default-looking blue-white-gray templates with no hierarchy, poor spacing, generic fake metrics, or meaningless charts.

## 5. Required Shell Layouts

Support these layout modes. Pick one based on the brief or existing project:

1. `sidebar-only`
   - Left sidebar menu.
   - Logo at the top of the sidebar.
   - User avatar, nickname, settings, and secondary icons at the bottom.
   - Main content area on the right.

2. `topnav-only`
   - Top menu.
   - Logo on the left.
   - Avatar, nickname, settings, and secondary icons on the right.
   - Header stays fixed while scrolling.

3. `sidebar-with-topbar`
   - Left sidebar menu plus top bar.
   - Top bar has logo on the left and avatar/nickname/settings/secondary icons on the right.
   - Top bar stays fixed while scrolling.
   - Top bar center can be empty, announcement, unread messages, global search, shortcuts, environment tag, tenant switcher, or a custom business module.

All modes require:

- Breadcrumbs at the top of the content page.
- Current route highlighted in the menu.
- Grouped menus that can expand and collapse.
- Permission-aware menu visibility and disabled states.
- Responsive collapse behavior for narrow screens.
- Main content scrolling without breaking fixed top/header regions.

## 6. Authentication And Permissions

Model these states explicitly:

- Anonymous / unauthenticated.
- Logged in but missing permission.
- Logged in with partial permissions.
- Logged in as administrator or privileged role.
- Token expired / session timeout.

Rules:

- Hide protected menus and actions when unauthenticated.
- Do not show create/edit/delete/export/import/bulk actions without permission.
- Route guards must align with menu filtering and button visibility.
- Sensitive back-end operations must still enforce permissions server-side.
- When a user lacks permission, prefer a clean disabled state or 403 page over broken invisible failures.

## 7. Navigation And Breadcrumbs

Menus:

- Provide navigation for pages and functional areas.
- Support grouped menu sections.
- Support expand/collapse per group.
- Support nested items when the system hierarchy requires it.
- Show route-active state, disabled state, external-link state, and unread/count badges when applicable.

Breadcrumbs:

- Show the current page location in the system hierarchy.
- Let users navigate upward.
- Preserve list state when returning from detail pages.
- Keep breadcrumb labels consistent with route titles and menu labels.

Avatar dropdown:

- Clicking avatar or nickname opens a dropdown.
- Required items: personal information, system settings, logout.
- Optional items: account security, notification preferences, theme, tenant switch, message center.
- Logout must be explicit and safe; clear tokens/session and redirect to login.

## 8. Default Workbench

Most admin systems should open to a workbench page.

Include relevant cards:

- User summary: name, role, department, current tenant, quick status.
- Calendar: in-progress projects, tasks, deadlines, meetings, approvals.
- Todo list: pending tasks, approvals, incidents, messages.
- Activity feed: operations, workflow updates, team dynamics.
- Quick start / shortcuts: frequently used modules and create actions.
- Personalized metrics: role-relevant counts, trend deltas, SLA reminders, health indicators.
- System notices: announcements, maintenance, unread messages.

Do not use meaningless fake data. If mock data is necessary, make it domain-specific and replaceable.

## 9. List Page Protocol

A standard list page contains a query card and a table card.

Query card:

- Place it at the top.
- Fields reflect real table query dimensions.
- Include search and reset actions on the right.
- Pressing Enter in inputs triggers search.
- Searching updates table data and resets pagination to page 1 unless using infinite scroll.
- Keep advanced filters collapsible when more than one row is needed.

Table card top-left:

- Primary create action.
- Bulk delete only when row selection exists.
- Other batch actions only when permission and selection semantics are clear.

Table card top-right:

- Refresh icon.
- Column settings icon.
- Density icon when the UI library supports it.
- Export/import icons only when authorized.

Table body:

- First column is selection only when multi-select is supported.
- Selection can support cross-page selection; if so, show selected count, clear selection, and cross-page semantics.
- Second column is usually the name/title column.
- Clicking name opens a detail page or detail modal/drawer depending on complexity.
- Sortable headers show visible sort state.
- Status fields use consistent semantic tags.
- The last column is actions: edit, delete, and more actions in an overflow menu.

Table footer:

- Use pagination by default.
- Infinite scroll mode removes pagination but must show loading, reached-end, and retry states.

## 10. Modal, Drawer, And Form Protocol

Modal:

- Contains title, content area, and action area.
- Content scrolls internally after reaching 90% viewport height or 70% viewport width.
- Do not show scrollbars when content does not overflow.
- Use for short create/edit/detail flows.

Drawer:

- Prefer for long forms, complex detail, side-by-side inspection, or preserving list context.
- Use clear sectioning and sticky footer actions for long content.

Forms:

- Labels use concise Chinese business language.
- Required fields, validation messages, help text, disabled fields, loading, submit failure, submit success, and dirty state must be handled.
- Long forms should be grouped by business meaning.
- Dangerous operations require confirmation and clear effect wording.

## 11. Detail And Profile Pages

Detail pages:

- Use a page for complex detail and a modal/drawer for simple detail.
- Include basic information, status, associated data, operation history/activity, attachments when applicable, and permission-aware actions.
- Preserve list filters, pagination, and sorting on return.
- Choose tabs, descriptions, timeline, child tables, and audit logs based on business complexity.

Personal center:

- Enter from avatar dropdown.
- Include profile, password change, account security, login records, notification preferences.
- Password change includes old password, new password, confirmation, strength hint, and submit feedback.
- Separate editable profile fields from read-only organization/role fields.

## 12. Additional Page Patterns

Implement the right pattern for the business domain:

- Permission management: users, roles, departments, permission points, menu permissions, data permissions.
- Approval/workflow: pending, processed, initiated, detail, timeline, current node, operation buttons.
- Dashboard: metrics, trend charts, distributions, ranking, alerts, and explicit metric definitions.
- Settings: system, notification, integration, parameter config, save/reset, dangerous zone.
- Audit logs: operation logs, login logs, API logs, filters for time, actor, module, result.
- Message center: unread messages, announcements, task reminders, batch read, filters, detail.
- Error pages: 403, 404, 500, network error, login expired, no permission, empty state.
- Import/export: template download, upload, parse preview, error-row download, import progress.
- Task center: async task list, progress, success/failure, retry, result download.

## 13. Implementation Discipline

- Use structured data for routes, menus, permissions, table columns, form schemas, and status dictionaries.
- Keep layout shell separate from page content.
- Keep list state in URL query, router state, or a predictable store so back navigation works.
- Centralize request/loading/error handling.
- Do not duplicate column definitions across table, detail, export, and column settings when a shared model can be used.
- Use stable keys for menu items, table rows, form fields, and permissions.
- Keep Chinese copy concise and business-specific.

## 14. Final Check

Before finishing, read `references/acceptance-checklist.md` and verify:

- Layout mode matches the brief.
- Auth and permission states are handled.
- Menus, breadcrumbs, active route, and profile dropdown work.
- Workbench/list/detail/profile patterns match the request.
- Tables handle loading, empty, error, sorting, pagination/infinite scroll, column settings, selection, and actions.
- Modals/drawers/forms handle overflow, validation, submission, and dangerous confirmations.
- Visual style is enterprise-refined Chinese admin UI, not marketing-page design.
- Repository lint/test/build or available validation commands pass.

