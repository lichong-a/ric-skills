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

## React + Ant Design / ProComponents

Use when the project already has Ant Design or for new React admin systems.

Preferred tools:

- `antd` for base components.
- `@ant-design/pro-components` for ProTable, ProForm, ProLayout when already used or appropriate.
- React Router, Umi, Next, or local router based on existing project.

Rules:

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

- Use route meta for breadcrumb/menu permission when possible.
- Keep table columns in structured definitions.
- Use scoped slots for row actions and status tags.
- Use dialog for short forms and drawer for complex forms/detail.

## Naive UI

Use when the project already uses Naive UI.

Preferred tools:

- `n-layout`, `n-menu`, `n-data-table`, `n-form`, `n-modal`, `n-drawer`, `n-pagination`.

Rules:

- Follow Naive UI theme tokens.
- Use DataTable remote pagination/sorting/filtering when data is server-side.
- Keep action render functions accessible and permission-aware.

## Arco Design

Use when the project uses Arco React or Arco Vue.

Rules:

- Follow Arco layout/menu/table/form/modal/drawer patterns.
- Use design tokens instead of ad hoc colors.
- Keep density consistent with the project's existing Arco config.

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
