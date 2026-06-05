# Framework Adapters

Use this reference after inspecting the project stack.

## Inspection Checklist

Before coding, inspect:

- `package.json`.
- Router setup.
- Layout shell.
- UI library.
- Table/form abstractions.
- Request client.
- Auth/session store.
- Permission model.
- State management.
- Styling solution.
- Existing test/build commands.

## Framework Skill Retrieval Protocol

After inspection and before writing framework-specific UI code, actively retrieve the relevant framework skill.

Detection signals:

- `antd`, `@ant-design/pro-components`, `@ant-design/icons`, `ant-design-pro`, `@umijs/*`: retrieve `ant-design` and/or `antd`.
- `element-plus`, `@element-plus/icons-vue`: retrieve `element-plus` or `element`.
- `naive-ui`: retrieve `naive-ui` or `naive`.
- `@arco-design/web-react`, `@arco-design/web-vue`: retrieve `arco` or `arco-design`.
- Existing imports from a framework count even if the dependency is indirect.

Rules:

- If the matching skill exists, read it before selecting components, props, tokens, or table/form patterns.
- If no matching skill exists, use this file plus the project's installed package version and official API documentation. Do not invent props, events, tokens, or component names.
- Do not add a second UI library for a missing convenience component.
- Do not override framework internals or broad generated class names when token/theme APIs exist.
- Include framework-specific checks in final validation when available.

## React + Ant Design / ProComponents

Use when the project already has Ant Design or for new React admin systems.

Preferred tools:

- `antd` for base components.
- `@ant-design/pro-components` for ProTable, ProForm, ProLayout when already used or appropriate.
- React Router, Umi, Next, or local router based on existing project.

Rules:

- Retrieve and apply `ant-design` and/or `antd` skill before writing Ant Design component code.
- If `@ant-design/cli` is available, query APIs with `antd info <Component> --format json` before using component props for Table, Button, Form, Select, Modal, Drawer, Dropdown, Menu, Pagination, ConfigProvider, ProTable, and other changed components.
- Query tokens/semantic hooks before custom styling; prefer ConfigProvider/theme tokens, component tokens, `classNames`, and `styles` over global `.ant-*` overrides.
- After changing antd code, run `antd lint <changed-path> --format json` when the CLI is available.
- Use ProTable for standard CRUD tables when available.
- Use Ant Design Form validation and layout conventions.
- Use Modal for short forms and Drawer for long forms/detail.
- Use ConfigProvider/theme tokens instead of scattered CSS overrides.
- Keep menu and route definitions typed/structured.

## Vue 3 + Element Plus

Use when the project already has Vue/Element Plus or for Vue admin systems.

Preferred tools:

- `el-container`, `el-menu`, `el-header`, `el-aside`, `el-main`.
- `el-table`, `el-form`, `el-dialog`, `el-drawer`, `el-pagination`.
- Vue Router route meta for title/permission/menu.
- Pinia for auth/menu/user state when used.

Rules:

- Retrieve an Element Plus-related skill first when available.
- Use route meta for breadcrumb/menu permission when possible.
- Keep table columns in structured definitions.
- Use scoped slots for row actions and status tags.
- Use dialog for short forms and drawer for complex forms/detail.
- If no skill is available, check the installed Element Plus version and official API before using props/events.

## Naive UI

Use when the project already uses Naive UI.

Preferred tools:

- `n-layout`, `n-menu`, `n-data-table`, `n-form`, `n-modal`, `n-drawer`, `n-pagination`.

Rules:

- Retrieve a Naive UI-related skill first when available.
- Follow Naive UI theme tokens.
- Use DataTable remote pagination/sorting/filtering when data is server-side.
- Keep action render functions accessible and permission-aware.
- If no skill is available, check the installed Naive UI version and official API before using props/events.

## Arco Design

Use when the project uses Arco React or Arco Vue.

Rules:

- Retrieve an Arco-related skill first when available.
- Follow Arco layout/menu/table/form/modal/drawer patterns.
- Use design tokens instead of ad hoc colors.
- Keep density consistent with the project's existing Arco config.
- If no skill is available, check the installed Arco version and official API before using props/events.

## TanStack Table

Use when custom table behavior is needed or the project already uses it.

Rules:

- Pair with the existing UI primitives.
- Model sorting, pagination, column visibility, row selection, and loading explicitly.
- Do not hand-roll table state in many unrelated components.

## Avoid Stack Drift

Do not:

- Add a second UI library for one component.
- Replace the router.
- Introduce a new state library for a single page.
- Add chart/table/form libraries without checking existing capabilities.
- Mix Tailwind admin primitives into a fully tokenized component-library app unless local conventions already support it.
