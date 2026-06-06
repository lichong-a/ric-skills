# China Enterprise Visual Style

Use this reference for the default visual taste of Chinese enterprise admin systems: enterprise-refined, efficient, and capable of productized brand expression on selected first-screen surfaces.

## Core Taste

The default style is enterprise-refined:

- Clean but not empty.
- Dense but not cramped.
- Stable but not old-fashioned.
- Polished but not decorative.
- Business-first and action-oriented.
- Branded on entry surfaces without becoming a marketing page.

Users should feel they can operate the system for hours without visual fatigue.

Login pages, workbench first screens, module homepages, onboarding, announcements, and command centers may feel more visually memorable. CRUD, permission, audit, settings, and dense detail pages should stay utility-first.

## Common References

Use these as directional references, not as assets to copy:

- Ant Design Pro and Ant Group internal-console patterns.
- DingTalk enterprise management surfaces.
- Feishu/Lark admin and workspace surfaces.
- WeCom enterprise management surfaces.
- Alibaba Cloud and Tencent Cloud consoles.
- Productized SaaS console homepages with branded workbench/overview screens.
- Data command centers and operation cockpit surfaces when the business calls for monitoring.
- SaaS back offices for CRM, SCRM, e-commerce, finance, HR, operations, and workflow.

## Color

Default:

- Neutral background: cool gray or warm gray, very light.
- Content cards: white or near-white.
- Primary color: brand blue or existing brand color.
- Semantic colors: success green, warning orange, error red, info blue.

Rules:

- Use one primary brand color.
- Semantic colors keep their meaning everywhere.
- Use gradients, textures, and saturated surfaces only on selected `product` or `immersive` regions such as login, workbench hero, announcement, onboarding, or big-screen dashboards.
- Avoid uncontrolled gradients and generic AI-purple backgrounds.
- Avoid "template blue" by improving hierarchy, spacing, typography, and state details.

## Theme Switching

When theme switching is requested or a new product should be theme-ready, prefer `light/dark/system` with token-driven implementation.

Rules:

- Define semantic tokens for surface, elevated surface, border, text, muted text, primary action, focus, hover, selected row, danger, warning, success, info, chart colors, and scrollbar.
- Persist user choice through the existing user settings store, cookie, or local storage. Do not ignore server-side user preference if one exists.
- LOGO, app icon, default avatar, generated backgrounds, empty-state art, and report covers must work on both light and dark shells. Generate variants when one asset cannot pass contrast.
- Table hover/selected states, modal masks, dropdowns, popovers, skeletons, loading overlays, chart colors, and scrollbars must be checked in both themes.
- Avoid page-by-page manual inversion. Theme should come from provider, CSS variables, or design-system tokens.

## Language And Locale

China-market defaults are usually Simplified Chinese first, but admin systems often need English, Traditional Chinese, or tenant-specific languages.

Rules:

- Keep Chinese labels concise and business-specific.
- When i18n is in scope, menus, breadcrumbs, route titles, page headers, table columns, button labels, status tags, validation errors, loading text, empty states, toasts, and permission messages must use translation keys.
- English labels are often longer; validate sidebar width, toolbar buttons, breadcrumbs, dropdowns, table headers, and modal titles in every implemented language.
- Date, number, percentage, and currency formatting should use locale-aware APIs or the chosen i18n library.
- Do not put critical text inside generated images because it cannot be localized reliably.

## Typography

Chinese admin UI needs readable system fonts:

- Prefer system font stacks unless the project has a design token.
- Keep Chinese labels concise.
- Use numeric tabular alignment for metrics and tables when available.
- Avoid oversized display typography.
- Avoid English-only decorative headings.

Recommended scale:

- Page title: 18-24px.
- Card title: 15-18px.
- Body/table: 13-14px.
- Secondary text: 12-13px.
- Metrics: 24-36px depending on card size.

First-screen surfaces may use larger, more expressive Chinese headings, but keep them concise and tied to the product or task. Operational pages should not inherit hero-scale typography.

## Density

Default density is medium-high.

Rules:

- Query cards should not consume half the viewport.
- Table row height should be readable, commonly 40-56px depending on system.
- Cards should group related work, not wrap every tiny element in a card.
- Use compact spacing for operations pages and more generous spacing for workbench/dashboard pages.
- Use richer composition for login/workbench/module homepages, but keep primary actions and key data above the fold.

## Spacing

Common shell spacing:

- Page padding: 16-24px desktop.
- Card padding: 16-24px.
- Card gap: 12-20px.
- Form field vertical gap: 16-24px.
- Toolbar gap: 8-12px.

Rules:

- Keep spacing consistent across pages.
- Avoid giant page gutters from marketing designs.
- Avoid cards inside cards unless there is real containment hierarchy.

## Brand Expression

Use brand expression on:

- Login page.
- Workbench first screen.
- Module homepage.
- Onboarding or announcement surface.
- Dashboard overview or command center.
- Report cover or export preview.

Good brand expression:

- Product-specific headline and subcopy.
- Controlled brand color and one accent system.
- Existing or generated visual asset.
- Distinct first-screen composition.
- Clear primary CTA and secondary utility links.
- Business-specific empty/loading/error states.

Avoid:

- Generic slogans.
- Trust-logo walls and testimonials inside admin tools.
- Random decorative graphics unrelated to the product.
- Hero treatment on CRUD/query/table pages.
- Fake company names, fake metrics, or fake product claims.

## Icons

Rules:

- Use one icon family.
- Use icons for actions such as refresh, settings, export, import, delete, edit, view, more.
- Icon-only buttons need tooltip/accessible labels.
- Destructive icons use error color only when the action is immediate or dangerous.
- Logo, app icon, module icons, default avatar, and generated small-icon packs should share one visual language when they are project-specific assets.
- If the user explicitly asks for all small icons to be generated, generate a coherent small-icon pack and consume it through shared icon components; do not mix random bitmap icons across pages.

## Generated Assets

Use generated bitmap assets only when they improve the product experience and existing brand/design-system assets are insufficient.

Good generated admin assets:

- Brand Asset Pack: logo/mark, app icon, sidebar/topbar mark, module icon style, default avatar, empty-state art, and background textures.
- Login illustration or subtle background.
- Empty-state illustrations for no data, no messages, no tasks, no permissions, import success/failure, and disconnected integrations.
- Low-contrast dashboard texture backgrounds.
- Onboarding or announcement banner visuals.
- Neutral profile/avatar placeholder sets.
- Report cover or export preview visuals.

Rules:

- Use the agent-native, built-in, MCP, or IDE image generation capability when available.
- If image generation tooling is missing or unavailable, use the RIC CLI fallback in `references/ric-imagegen-fallback.md`.
- Keep generated assets quiet and secondary to data and actions on utility pages; allow stronger brand presence on login, onboarding, workbench hero, and command-center first screens.
- Avoid critical text in images.
- Avoid fake brands, fake logos, watermarks, QR codes, decorative mascots, and high-saturation marketing art.
- Store project-bound assets in the workspace and reference them from code.

## Loading And Skeletons

Rules:

- Render the shell first; never leave the main area blank while waiting for data.
- Prefer skeletons for initial content loading: cards, table rows, detail label/value pairs, charts, avatar blocks, media, and form sections.
- Use spinner plus concise Chinese text for visible data refreshes, such as table reload or remote search.
- Skeleton shape should match the final content footprint closely enough to prevent layout jump.
- Loading visuals should use the same radius, density, and tone as the final UI.

## Cards

Cards are for grouping work areas:

- Query card.
- Table card.
- Workbench module.
- Metric group.
- Detail section.

Rules:

- Keep radii modest, usually 4-8px unless the design system specifies otherwise.
- Use light borders or subtle shadows.
- Avoid deeply nested cards.
- Avoid landing-page style floating cards.

## Tables

Tables carry most admin value.

Rules:

- Align numeric columns consistently.
- Keep status readable.
- Use fixed action column for wide tables.
- Use column visibility instead of squeezing too many columns.
- Use horizontal scroll intentionally for dense enterprise data.
- Avoid fake precision and meaningless columns.

## Motion

Motion is functional:

- Hover feedback.
- Expand/collapse.
- Drawer/modal transitions.
- Loading skeletons.
- Dropdown opening.

Avoid:

- Scroll storytelling.
- Parallax.
- Animated backgrounds.
- Decorative looping motion.
- Excessive page transitions.

On login, onboarding, workbench hero, and command-center screens, motion can be more expressive if it communicates reveal, status, data update, or guided focus. It must remain optional and respect reduced-motion preferences when the stack supports it.

Public portals, tenant welcome pages, help/marketing-adjacent pages, and user-facing console entry pages may use stronger motion and 3D treatment. GSAP, Three.js/WebGL, 3D tilt cards, and canvas scenes are acceptable only on these low-frequency high-expression surfaces, with cleanup, reduced-motion fallback, and screenshot verification. Ordinary CRUD, permissions, audit logs, settings, and dense detail pages stay motion-light.

## Anti-Template Rules

Do not ship:

- Default empty blue-white-gray Ant Design pages without hierarchy.
- Login pages that are just a centered default form with no brand signal.
- Workbenches that are only equal metric cards and "welcome admin" copy.
- Empty states that only say "暂无数据" with no business explanation or next action.
- Giant dashboard cards with fake metrics.
- Copy like "欢迎回来，管理员" everywhere without role context.
- `John Doe`, `Acme`, `测试数据1`, or meaningless placeholders.
- Every page with the same card/table/action layout when the business does not require it.
- Overuse of tags and colors until nothing has priority.
- Unclear icon-only operations with no tooltip.
- Missing empty/error/loading states.
