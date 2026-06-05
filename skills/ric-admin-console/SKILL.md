---
name: ric-admin-console
description: "Chinese enterprise admin-console skill for polished production management systems. Use for admin panels, CRUD consoles, RBAC, data tables, branded login pages, workbench first screens, approvals, operations consoles, SaaS back offices, dashboards, and internal tools. Supports sidebar/topnav/sidebar-plus-topbar layouts, auth states, grouped menus, breadcrumbs, profile dropdowns, list/detail/workbench/profile/settings/audit/approval pages, modals, drawers, forms, tables, active ImageGen asset planning, shadcn-first React stack with shadcn skill retrieval, optional Ant Design/antd fallback by user choice or existing project convention, Element Plus/Naive UI/Arco routing, deduplicated headers/toolbars, polished scrollbars, generated visual assets, and China-market enterprise taste."
---
# RIC Admin Console Skill

Use this skill for Chinese enterprise management systems: admin panels, back offices, operations consoles, CRUD systems, permission systems, workflow approval systems, internal tools, data-heavy dashboards, branded login pages, visual workbenches, and SaaS control panels.

Do not blindly apply marketing-page taste rules to every admin page. Admin consoles are product surfaces for repeated work, but selected first-screen surfaces still need strong brand expression, visual assets, layout rhythm, CTA quality, and anti-template design judgment. Use high visual impact on login pages, workbench first screens, welcome/onboarding pages, empty states, announcement banners, dashboard first screens, big-screen command centers, module homepages, and productized SaaS console homepages. Keep ordinary CRUD, permission config, audit logs, settings, and detail pages optimized for clarity, scan speed, predictable navigation, permission-aware actions, state coverage, and dense but orderly information.

## 1. Operating Protocol

1. Perform skill retrieval before work.
2. Inspect the existing project before choosing libraries: `package.json`, router, UI library, layout components, table/form stack, state management, auth/permission model, request client, mock/data layer, and styling system.
3. After detecting the UI framework, perform framework skill retrieval and read the relevant installed skill when available. For React admin systems without an established UI system, retrieve and use `shadcn` before component selection or code. For React + Ant Design/ProComponents/antd imports, retrieve and use `ant-design` and/or `antd`; follow their CLI/API lookup rules when writing antd component code.
4. Prefer the existing stack. Do not replace shadcn/ui, Ant Design, Element Plus, Naive UI, Arco, or another established UI system unless the user asks.
5. Prefer PowerShell commands on Windows. Use pnpm over npm for Node projects.
6. Do not change global Node/FNM configuration. Use temporary `fnm use` or `fnm exec` only when needed.
7. Treat permissions as a first-class design input. Buttons, menus, routes, API calls, and bulk actions must have a shared permission source.
8. Provide loading, empty, error, disabled, success, and unauthenticated states for every interactive area.
9. Never create destructive database/cache/message/object-storage operations. Follow `ric-infra-safety` for infrastructure and namespace rules.
10. Finish with repository validation: lint/test/build when available, framework-specific checks when available, and browser or screenshot checks for layout work.

Read these references when the task needs detail:

- `references/layout-patterns.md` for shell layouts, menus, top bars, breadcrumbs, auth states.
- `references/page-patterns.md` for workbench, list, detail, profile, settings, permissions, approval, logs, messages, import/export, tasks.
- `references/component-contracts.md` for query cards, tables, pagination, modals, drawers, forms, actions, status UI.
- `references/china-enterprise-visual-style.md` for Chinese enterprise visual taste, density, Chinese typography, color, spacing, and anti-template rules.
- `references/admin-visual-impact.md` for admin-adapted brand expression, hero/first-screen composition, CTA quality, visual assets, layout rhythm, motion restraint, and anti-template rules.
- `references/framework-adapters.md` for shadcn-first React defaults, framework skill retrieval, and React/Vue/UI-library decision rules.
- `references/acceptance-checklist.md` before declaring work complete.
- `../../references/ric-imagegen-fallback.md` when admin-specific bitmap assets are needed and built-in image generation is unavailable.

## 2. Design Read

Before implementation, state one concise design read:

`Reading this as: <system type> for <user role>, with <layout mode>, <visual impact mode>, <data density>, <permission complexity>, and <framework/UI library>.`

Examples:

- `Reading this as: user/role management for operations staff, with sidebar-plus-topbar layout, utility visual mode, high table density, RBAC permissions, and React + shadcn/ui + TanStack Table.`
- `Reading this as: SaaS console login plus workbench for tenant admins, with sidebar-plus-topbar layout, product/immersive visual modes, medium-high density, tenant permissions, and React + shadcn/ui.`
- `Reading this as: approval workflow console for department managers, with topnav-only layout, product visual mode, medium density, route-level permissions, and Vue 3 + Element Plus.`

Ask only one clarification if the layout mode, auth model, or framework choice cannot be inferred from the repo and materially changes implementation.

## 3. Asset Plan

After the design read and before implementation, create a concise Asset Plan:

`Asset Plan: <needed assets or none>, <source: existing brand asset | ImageGen | RIC CLI fallback | not needed>, <save path>, <where used>.`

Active ImageGen is required when a `product` or `immersive` surface needs visual differentiation and no suitable existing brand/design-system asset exists. This includes login visual panels, workbench/module backgrounds, onboarding/announcement banners, empty-state illustrations, report/export covers, and dashboard/command-center backgrounds.

Rules:

- Do not skip needed visual assets after the requirement is clear.
- Do not substitute pure CSS gradients, blank placeholders, hand-rolled decorative SVG, or fake screenshot divs when a bitmap asset is needed.
- If built-in image generation, MCP image tooling, IDE image tooling, or agent-native image capability is available, use it first for project-bound bitmap assets.
- If image generation is needed but no built-in/agent-native tool is available, read `../../references/ric-imagegen-fallback.md` and use the bundled CLI fallback directly.
- The CLI fallback requires `OPENAI_API_KEY`; if it is missing, stop and ask for that environment variable.
- `utility` pages do not need decorative generation unless they contain important empty, error, import/export, report, or onboarding states.
- At final handoff, report generated asset paths or state that no image asset was needed for this page type.

## 4. Stack Selection

Use multi-stack decision-making:

1. Existing React + shadcn/ui: use shadcn source components, Tailwind semantic tokens, Radix/base primitives, local aliases, and TanStack Table when table state needs explicit control.
2. Existing Vue + Element Plus: use Element Plus layout, menu, table, form, dialog/drawer, pagination, popconfirm patterns.
3. Existing Naive UI or Arco: stay within that library and mirror its density/token system.
4. Existing custom design system: use the local primitives and only add external packages when missing capabilities are real.
5. Existing React + Ant Design: keep Ant Design, ProComponents, ProLayout, ProTable, Modal/Drawer/Form patterns already present unless the user explicitly chooses a migration.
6. New React project or React project without an established UI system: recommend React + Vite or Next + shadcn/ui + Tailwind + Radix primitives + TanStack Table.
7. New Vue project without user preference: recommend Vue 3 + Vite + Element Plus.

React default: shadcn-first. Ant Design/ProComponents is the secondary React option and should be used only when the user chooses it, the project is already deeply AntD-based, or the team/business requirement explicitly needs Ant Design Pro patterns. If a React project already uses AntD and the task suggests shadcn, ask the user to choose between the recommended shadcn direction and preserving AntD before mixing or migrating.

One UI system per app. Do not mix Ant Design and Element Plus, Ant Design and Material, or shadcn and ProComponents unless the repo already does so and migration is explicitly in scope.

Before writing framework-specific component code, read `references/framework-adapters.md` and apply its skill retrieval protocol. If a matching skill is unavailable, use the existing project version and official API documentation rather than inventing props, events, tokens, or component names.

## 5. Visual Direction

Default to enterprise-refined Chinese admin taste:

- Clear, trustworthy, compact, and stable.
- Medium-high information density.
- Productized brand expression on selected first-screen surfaces.
- Blue/neutral base with controlled semantic colors, or the product's existing brand color.
- Strong table readability, predictable action placement, consistent icons, polished empty states, and clear status tags.
- Chinese text rhythm: short labels, direct button copy, no oversized English marketing slogans.

Apply visual impact by surface:

- `utility`: tables, forms, permissions, logs, settings, and dense detail pages. Low visual drama, high efficiency.
- `product`: workbench, module homepages, SaaS console homepages, dashboard summaries, announcement centers. Stronger brand tone, richer layout rhythm, clear CTA hierarchy.
- `immersive`: login pages, welcome/onboarding pages, big-screen command centers, report covers, and hero-like console entry pages. Visual assets and first impression matter, but actions and state clarity still win.

Inherit the useful parts of `ric-design-taste-frontend`: brand read, visual asset priority, anti-default discipline, CTA contrast/wrap checks, copy self-audit, layout diversity, and restrained motion. Adapt them for admin workflows instead of copying landing-page structure.

Avoid globally:

- Marketing hero sections on ordinary CRUD pages, giant slogans in operational screens, decorative illustrations that compete with data, and large editorial typography inside dense tools.
- Excessive gradients, glassmorphism, huge round cards, animated backgrounds, and overbuilt motion.
- Default-looking blue-white-gray templates with no hierarchy, poor spacing, generic fake metrics, or meaningless charts.

## 6. Admin Visual Impact

Use high visual design only where it improves brand recognition, orientation, business understanding, or action conversion.

Required high-impact surfaces:

- Login page: branded first screen, clear authentication path, trustworthy copy, primary login CTA, secondary help/security links, and a visual asset or brand background when assets are available.
- Workbench first screen: dashboard hero, command header, or branded overview that summarizes identity, today's priorities, urgent tasks, key metrics, notices, and quick starts.
- Module homepage: visual overview that explains the module's purpose, primary actions, status, and next best actions.
- Empty states: business-specific explanation, permission-aware CTA, and generated or existing visual asset when useful.
- Announcement/onboarding: focused message, one primary CTA per intent, supporting visual, and dismiss/read state.
- Dashboard/big screen: stronger theme, chart rhythm, motion when useful, clear metric definitions, refresh/state indicators, and visible abnormal states.

Rules:

- Do not turn every content page into a hero page.
- Do not use marketing copy where operational copy is needed.
- Do not invent fake business numbers, fake brands, fake logos, QR codes, or decorative trust claims.
- Keep CTA labels direct and action-specific. Avoid duplicate CTA intent on the same surface.
- Button text must not wrap on desktop and must pass contrast checks.
- Hero/command-header copy must be short enough to scan while working.
- Use real UI components for product previews. Avoid fake screenshot divs.
- Motion must communicate navigation, loading, reveal, expansion, or data change; avoid scroll storytelling and decorative loops in normal admin work.
- Before finishing, reread visible copy and replace vague, poetic, or AI-sounding text with concise business language.

Read `references/admin-visual-impact.md` before implementing login, workbench first screen, module homepage, onboarding, empty state, dashboard hero, command-center visuals, or any generated admin bitmap asset.

## 7. Admin Asset Generation

Admin systems usually need fewer generated visuals than marketing pages, but they still benefit from deliberate project-specific assets. When the system needs visual assets and no suitable existing brand/design-system asset exists, invoke the relevant agent image generation ability instead of shipping generic placeholders.

Generate assets for:

- Login page illustration, visual panel, or brand background.
- Empty states for workbench, list pages, import/export, messages, tasks, and permissions.
- Low-contrast dashboard texture or module background.
- Announcement or onboarding banner.
- Product/module icon concepts when no icon system exists.
- Profile/avatar placeholder sets when the system needs neutral defaults.
- Report cover or export preview artwork when the product has document/report flows.

Rules:

- Prefer existing brand assets and UI-library icon systems first for functional icons.
- Generated admin assets must be quiet, enterprise-refined, low-noise, and secondary to the data.
- Do not generate decorative hero art for normal CRUD pages.
- Do not put critical UI text inside generated images.
- Do not use fake logos, trademarks, QR codes, watermarks, fake company names, or fake business data inside generated images.
- Save project-bound generated assets into the workspace and wire them into the app; never leave referenced assets only in a tool temp folder.
- If the built-in image generation tool, MCP image tool, IDE image tool, or agent-native image capability is missing or unavailable, read `../../references/ric-imagegen-fallback.md` and use the bundled CLI fallback directly. The CLI path requires `OPENAI_API_KEY`; if it is missing, stop and ask for that environment variable.

## 8. Required Shell Layouts

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

## 9. Authentication And Permissions

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

## 10. Navigation And Breadcrumbs

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

## 11. Default Workbench

Most admin systems should open to a workbench page. Treat the top of the workbench as a product surface, not a generic card dump.

Include relevant cards:

- User summary: name, role, department, current tenant, quick status.
- Calendar: in-progress projects, tasks, deadlines, meetings, approvals.
- Todo list: pending tasks, approvals, incidents, messages.
- Activity feed: operations, workflow updates, team dynamics.
- Quick start / shortcuts: frequently used modules and create actions.
- Personalized metrics: role-relevant counts, trend deltas, SLA reminders, health indicators.
- System notices: announcements, maintenance, unread messages.

Workbench visual rules:

- Use a dashboard hero, command header, or branded overview when the workbench is a primary entry page.
- Show identity and priorities: role, department/tenant, today's focus, urgent work, key metrics, notices, and quick starts.
- Give CTAs clear operational intent, such as create order, handle approval, invite user, view risk, or configure integration.
- Use brand visuals, textures, or generated assets only when they support orientation and hierarchy.
- Keep core numbers, tasks, and actions immediately scannable.

Do not use meaningless fake data. If mock data is necessary, make it domain-specific and replaceable.

## 12. List Page Protocol

A standard list page contains a query card and a table card.

Page header:

- Render the current page title once.
- Breadcrumb labels, page header title, module hero title, and table card title must not repeat the same title as separate large headings.
- If a module hero or command header already owns the page title, the table card title should be a compact dataset label or omitted.

Query card:

- Place it at the top.
- Fields reflect real table query dimensions.
- Include search and reset actions on the right.
- Pressing Enter in inputs triggers search.
- Searching updates table data and resets pagination to page 1 unless using infinite scroll.
- Keep advanced filters collapsible when more than one row is needed.

Table card top-left:

- Primary create action only when it is not already present in a page hero or command header.
- Bulk delete appears when row selection exists and the user has delete permission.
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

Selection toolbar:

- Show one selected-count message.
- Show one clear action, default label `清空选择`.
- Do not render both `取消选择` and `清空选择`.
- When deletion is allowed, show `批量删除` after selection; use danger styling and require confirmation with selected count and cross-page semantics.
- Disable batch actions when the selection is empty or permission is missing.

Table footer:

- Use pagination by default.
- Infinite scroll mode removes pagination but must show loading, reached-end, and retry states.

## 13. Modal, Drawer, And Form Protocol

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

## 14. Detail And Profile Pages

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

## 15. Additional Page Patterns

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

## 16. Scrollbar And Overflow Discipline

- Avoid double scrollbars between `body`, shell, main content, cards, tables, modals, and drawers.
- Long sidebar menus, table regions, modal bodies, and drawer bodies may scroll; normal cards should not create unnecessary internal scroll areas.
- Do not show scrollbars when content does not overflow.
- Use a shared scrollbar style such as `ric-scroll-region`: transparent track, semi-transparent rounded thumb on hover/scroll/focus, thin width, and no arrow buttons.
- For WebKit, hide scrollbar buttons with `::-webkit-scrollbar-button { display: none; }`.
- For Firefox, use `scrollbar-width: thin` and `scrollbar-color: rgba(...) transparent`.

Read `references/component-contracts.md` for the full scrollbar and overflow contract before implementing complex list/table/modal pages.

## 17. Implementation Discipline

- Use structured data for routes, menus, permissions, table columns, form schemas, and status dictionaries.
- Keep layout shell separate from page content.
- Keep list state in URL query, router state, or a predictable store so back navigation works.
- Centralize request/loading/error handling.
- Do not duplicate column definitions across table, detail, export, and column settings when a shared model can be used.
- Use stable keys for menu items, table rows, form fields, and permissions.
- Keep Chinese copy concise and business-specific.

## 18. Final Check

Before finishing, read `references/acceptance-checklist.md` and verify:

- Layout mode matches the brief.
- Auth and permission states are handled.
- Menus, breadcrumbs, active route, and profile dropdown work.
- Workbench/list/detail/profile patterns match the request.
- Tables handle loading, empty, error, sorting, pagination/infinite scroll, column settings, selection, and actions.
- Main content pages avoid duplicated titles, duplicated create buttons, duplicated selection-clear actions, and missing batch delete when deletion is allowed.
- Modals/drawers/forms handle overflow, validation, submission, and dangerous confirmations.
- Scrollbars are hidden when unnecessary and polished when visible; no double-scrollbar layout.
- Visual style is enterprise-refined Chinese admin UI with admin-adapted brand impact where the page type needs it.
- Login, workbench, module homepage, onboarding, announcement, dashboard hero, and empty states use visual assets, CTA hierarchy, copy self-audit, and anti-template judgment when relevant.
- Asset Plan was followed; generated asset paths are reported, or no generated asset was needed for the page type.
- Framework-specific skills and checks were used when a matching UI framework skill exists.
- Ordinary CRUD, permission, audit, settings, and detail pages remain efficient and are not polluted by marketing-page hero patterns.
- Repository lint/test/build or available validation commands pass.
