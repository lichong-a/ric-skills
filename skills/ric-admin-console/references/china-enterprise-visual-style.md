# China Enterprise Visual Style

Use this reference for the default visual taste of Chinese enterprise admin systems.

## Core Taste

The default style is enterprise-refined:

- Clean but not empty.
- Dense but not cramped.
- Stable but not old-fashioned.
- Polished but not decorative.
- Business-first and action-oriented.

Users should feel they can operate the system for hours without visual fatigue.

## Common References

Use these as directional references, not as assets to copy:

- Ant Design Pro and Ant Group internal-console patterns.
- DingTalk enterprise management surfaces.
- Feishu/Lark admin and workspace surfaces.
- WeCom enterprise management surfaces.
- Alibaba Cloud and Tencent Cloud consoles.
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
- Avoid uncontrolled gradients.
- Avoid large saturated backgrounds.
- Avoid "template blue" by improving hierarchy, spacing, typography, and state details.

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

## Density

Default density is medium-high.

Rules:

- Query cards should not consume half the viewport.
- Table row height should be readable, commonly 40-56px depending on system.
- Cards should group related work, not wrap every tiny element in a card.
- Use compact spacing for operations pages and more generous spacing for workbench/dashboard pages.

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

## Icons

Rules:

- Use one icon family.
- Use icons for actions such as refresh, settings, export, import, delete, edit, view, more.
- Icon-only buttons need tooltip/accessible labels.
- Destructive icons use error color only when the action is immediate or dangerous.

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

## Anti-Template Rules

Do not ship:

- Default empty blue-white-gray Ant Design pages without hierarchy.
- Giant dashboard cards with fake metrics.
- Copy like "欢迎回来，管理员" everywhere without role context.
- `John Doe`, `Acme`, `测试数据1`, or meaningless placeholders.
- Every page with the same card/table/action layout when the business does not require it.
- Overuse of tags and colors until nothing has priority.
- Unclear icon-only operations with no tooltip.
- Missing empty/error/loading states.
