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

- React/Vite/Next/React Router project with no established mature UI library: retrieve `shadcn` and treat it as the recommended default.
- `components.json`, `@/components/ui`, `~/components/ui`, `shadcn`, `@radix-ui/*`, `class-variance-authority`, `tailwindcss`, `tailwind.config.*`, `app/globals.css` with shadcn tokens, or existing shadcn imports: retrieve `shadcn`.
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
- After runnable UI changes, include browser screenshots in final validation. Static API/CLI/lint checks do not replace screenshot verification for component composition, spacing, state, and overflow behavior.

## React + shadcn/ui

Use as the default for new React admin systems and for React projects that do not already have a mature UI library or design system.

Preferred tools:

- shadcn/ui source components for layout, navigation, data display, forms, overlays, feedback, and empty states.
- Tailwind semantic tokens and CSS variables from the project shadcn config.
- Radix/base primitives through shadcn components, not direct ad hoc primitive wiring unless local components already do that.
- TanStack Table with shadcn `Table` when sorting, pagination, column visibility, row selection, remote loading, or cross-page selection needs explicit state.
- The project's existing router, request client, auth store, and icon library from shadcn project context.

Rules:

- Retrieve and apply the `shadcn` skill before writing shadcn code, even if you have used shadcn before.
- Run shadcn commands with the project's package runner. Prefer `pnpm dlx shadcn@latest` when pnpm is the project manager; otherwise follow the package manager detected by `components.json`, lockfile, or `package.json`.
- Before selecting components, run or refresh `shadcn info --json` and use its aliases, `isRSC`, Tailwind version, CSS file, base primitive, icon library, resolved paths, framework, package manager, and preset.
- Before implementing or fixing shadcn components, run `shadcn docs <component...>` and fetch/read the returned docs or examples for the exact components being used.
- Check installed components first; do not import a shadcn component that has not been added, and do not re-add one that already exists.
- Use `shadcn search`, `view`, and `add --dry-run`/`--diff` when selecting or updating registry components. Do not fetch raw registry or GitHub component files manually.
- Use shadcn components before custom markup: `Sidebar`, `Breadcrumb`, `Card`, `Table`, `Button`, `DropdownMenu`, `Dialog`, `Sheet`, `Drawer`, `AlertDialog`, `Form`/`Field`, `Input`, `Select`, `Checkbox`, `Badge`, `Avatar`, `Tabs`, `Pagination`, `Empty`, `Skeleton`, `Alert`, `Separator`, `Tooltip`, `ScrollArea`, `sonner`, and `Chart` when available.
- Follow shadcn composition rules: complete `Card` structure, grouped menu/select items, required dialog/sheet/drawer titles, `AvatarFallback`, `asChild`/`render` according to the detected base, `data-invalid`/`aria-invalid` validation, and `data-icon` icons in buttons.
- Follow shadcn styling rules: semantic tokens, `cn()`, `gap-*` instead of `space-*`, `size-*` for square dimensions, no raw color utilities for semantic state, no manual overlay z-index, and no broad overrides of generated UI components.
- For admin list pages, pair TanStack state with shadcn `Table`, `Checkbox`, `DropdownMenu`, `Button`, `Badge`, `Pagination`, `Skeleton`, `Empty`, and `AlertDialog` so selection, sorting, column visibility, batch delete, loading, empty, and confirmation behavior stay explicit.
- For forms and query cards, use shadcn form/field primitives and the project validation approach; avoid raw div-only form layouts.
- For modals and long forms, use `Dialog` for short flows and `Sheet`/`Drawer` for long flows, with required titles and accessible triggers.
- Do not introduce Ant Design, ProComponents, Material UI, or another component library into a shadcn admin system unless the user explicitly asks and migration/mixing is in scope.
- In screenshot verification, confirm shadcn composition is visible: `Breadcrumb`, `Card`, `Table`, `Dialog`/`Sheet`/`Drawer`, `AlertDialog`, `Skeleton`, `Empty`, `ScrollArea`, semantic tokens, consistent gaps, and no raw div-only replacement for installed primitives.

## React + Ant Design / ProComponents

Use when the project already has Ant Design, when the user explicitly chooses Ant Design, or when the team/business requirement explicitly needs Ant Design Pro patterns. Ant Design is the secondary React option for new admin systems; do not choose it by default when shadcn is viable.

Preferred tools:

- `antd` for base components.
- `@ant-design/pro-components` for ProTable, ProForm, ProLayout when already used or appropriate.
- React Router, Umi, Next, or local router based on existing project.

Rules:

- Retrieve and apply `ant-design` and/or `antd` skill before writing Ant Design component code.
- If the project is not already AntD-based and the user did not choose AntD, present shadcn as the recommended React option and ask before adding AntD.
- Do not mix AntD/ProComponents with shadcn source components unless the repo already does so or the user explicitly approves a migration strategy.
- If `@ant-design/cli` is available, query APIs with `antd info <Component> --format json` before using component props for Table, Button, Form, Select, Modal, Drawer, Dropdown, Menu, Pagination, ConfigProvider, ProTable, and other changed components.
- Query tokens/semantic hooks before custom styling; prefer ConfigProvider/theme tokens, component tokens, `classNames`, and `styles` over global `.ant-*` overrides.
- After changing antd code, run `antd lint <changed-path> --format json` when the CLI is available.
- Use ProTable for standard CRUD tables when available.
- Use Ant Design Form validation and layout conventions.
- Use Modal for short forms and Drawer for long forms/detail.
- Use ConfigProvider/theme tokens instead of scattered CSS overrides.
- Keep menu and route definitions typed/structured.
- In screenshot verification, confirm Ant Design/ProComponents layouts use the expected token density, table/form/modal conventions, loading states, and no accidental shadcn/AntD visual mixing.

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
