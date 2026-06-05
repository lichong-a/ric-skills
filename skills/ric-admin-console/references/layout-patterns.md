# Layout Patterns

Use this reference when building or reviewing the admin shell.

## Layout Selection

Choose one shell mode:

- `sidebar-only`: best for function-rich systems with many modules and stable left navigation.
- `topnav-only`: best for shallow systems, portal-like products, or systems with a few top-level areas.
- `sidebar-with-topbar`: best default for medium/large enterprise systems because it supports module navigation plus global actions.

Do not mix shell modes randomly across pages. If a special full-screen page is needed, document it as an exception, such as login, report preview, print view, or big-screen monitoring.

## Sidebar-Only

Structure:

- Sidebar width: usually 208-240px expanded; 56-72px collapsed.
- Top: logo and product name.
- Middle: grouped navigation.
- Bottom: avatar, nickname, settings icon, optional message/help icons.
- Main content: page header/breadcrumb area plus content.

Rules:

- Keep menu item height consistent, usually 40-48px.
- Use icons only when they improve scanning; keep one icon style.
- Collapse behavior must keep active state visible.
- Long menu groups scroll inside the sidebar, not the whole page.
- The bottom user area stays reachable even with long menus.

## Topnav-Only

Structure:

- Header height: usually 56-64px.
- Left: logo and product name.
- Center/left: top-level navigation.
- Right: search/message/help/settings/avatar.
- Header is fixed on scroll.
- Content starts below the fixed header.

Rules:

- Keep desktop nav on one row.
- Use overflow/more menu when top-level items exceed available width.
- Avoid multi-row top navigation.
- Use tabs or secondary nav inside modules when deeper hierarchy is needed.

## Sidebar-With-Topbar

Structure:

- Sidebar: module navigation.
- Topbar: global context and account actions.
- Topbar left: logo or current product/tenant context.
- Topbar center: optional announcement, unread messages, global search, shortcuts, environment tag, tenant switcher, or empty.
- Topbar right: message/help/settings/avatar/nickname.
- Topbar stays fixed while content scrolls.

Rules:

- Decide whether logo belongs in sidebar or topbar. Do not duplicate it visually unless one is collapsed.
- Keep topbar center content low-noise. Do not turn it into a second dense menu.
- The topbar must not cover breadcrumbs or page content.
- Use sticky positioning carefully; avoid double scrollbars.

## Breadcrumbs

Every content page needs breadcrumbs unless it is a full-screen exception.

Breadcrumb rules:

- Start from the nearest system root, not necessarily "Home" if the app uses workbench as root.
- Labels match menu and route names.
- Last item is the current page and is not clickable.
- Parent items must navigate upward through real links or click handlers; a breadcrumb that only displays text is incomplete.
- Detail pages should preserve list filters, sorting, pagination, selected tab, and scroll position when going back.
- If browser history is not reliable, empty, or points outside the admin app, navigate to the parent route with saved query state instead of calling `back()` blindly.
- If a route has no explicit parent, derive it from route metadata, menu tree, or the nearest navigable ancestor.
- Breadcrumb labels, menu labels, route titles, document titles, and page headers should come from shared route/menu metadata when practical.
- Leave visible spacing between breadcrumbs and the page title/header; the breadcrumb line must not visually stick to the H1.
- Verify parent breadcrumb clicks in the browser or router test, including detail -> list return-state behavior.

Browser screenshot verification:

- Capture the selected shell layout at `1366x768`, `1440x900`, and `1920x1080`.
- Confirm fixed sidebar/topbar regions do not cover breadcrumbs or page content.
- Click parent breadcrumb items in Browser and verify upward navigation, then return to the detail flow and confirm list filters, sorting, pagination, selected tab, and scroll state are preserved.
- Capture long-menu and collapsed-menu states when the sidebar can overflow or collapse.

## Menus

Menu model fields should include:

- `key`
- `title`
- `path`
- `icon`
- `children`
- `group`
- `permission`
- `disabled`
- `external`
- `badge`
- `hidden`

Rules:

- Generate menus from route and permission metadata when possible.
- Keep menu keys stable.
- Do not duplicate menu labels across the same level.
- Keep grouping meaningful: "系统管理", "业务管理", "数据中心", "运营管理", "审计监控".
- Support group collapse/expand.
- Current route highlight must work for detail pages under a list menu item.

## Auth Shell States

Provide shell behavior for:

- Loading current user.
- Anonymous user.
- Logged in user.
- Missing permission.
- Session expired.

Rules:

- Anonymous state should not render protected menu/actions.
- Session expiration should redirect to login or show a clear re-login prompt.
- Permission failures should use 403 page or disabled actions with explanation.

## Responsive Behavior

Admin systems are desktop-first, but must not break on tablets and narrow windows.

Rules:

- Collapse sidebar below a project-defined breakpoint.
- For mobile-sized widths, use drawer navigation.
- Keep topbar actions accessible through overflow menu.
- Table-heavy pages may use horizontal scroll, fixed columns, or responsive column hiding.
- Never allow fixed headers to cover content.
