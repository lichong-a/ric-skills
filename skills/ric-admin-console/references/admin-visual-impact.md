# Admin Visual Impact

Use this reference when an admin-console task needs brand expression, a strong first screen, generated assets, CTA quality, layout rhythm, or anti-template visual judgment.

The goal is not to make admin pages look like marketing pages. The goal is to make product entry surfaces feel branded, confident, memorable, and still efficient for repeated work.

## Visual Impact Modes

Choose one mode per page or region:

- `utility`: CRUD lists, query/table pages, forms, permissions, audit logs, settings, detail subviews. Optimize for scan speed, density, state clarity, and permission-aware actions.
- `product`: workbench, module homepage, SaaS console homepage, dashboard summary, announcement center. Use stronger brand hierarchy, richer layout rhythm, and clear CTA hierarchy while keeping data scannable.
- `immersive`: login, welcome/onboarding, big-screen command center, report cover, launch/guide page. Use high-impact composition, generated or brand assets, and stronger motion/visual treatment.

Do not apply `immersive` to normal CRUD pages.

## Inherited Taste Rules For Admin

Borrow these from high-end frontend design:

- Start with a brand read: product category, user role, trust level, visual mood, and business density.
- Avoid default AI-purple gradients, centered generic hero, three equal feature cards, fake screenshot divs, and template-blue dashboards.
- Use real or generated visual assets when a surface depends on first impression or orientation.
- Keep one primary brand color, with semantic colors reserved for status.
- Use one icon family and consistent stroke/weight.
- Give CTAs one intent per surface. Do not duplicate equivalent actions.
- Audit CTA contrast and desktop wrapping.
- Use layout variety across first-screen modules; do not repeat identical card grids everywhere.
- Run a copy self-audit and remove vague, poetic, or AI-sounding copy.

Do not inherit these blindly:

- Giant marketing H1s across operational pages.
- Trust-logo walls, social proof strips, testimonial blocks, scroll storytelling, parallax, and decorative page-length narratives.
- Oversized editorial typography inside dense work surfaces.
- Decorative hero art for query/table pages.
- Fake product screenshots made from rectangles when a real component preview or generated asset is needed.

## Login Page

A login page is a brand surface and should not feel like a default form template.

Required:

- Brand mark/name visible in the first viewport.
- Authentication form with one primary login CTA.
- Clear secondary actions: forgot password, SSO, register/join tenant, help, or security notice when relevant.
- Trust cues appropriate to enterprise use: data security, tenant isolation, auditability, service status, or support link.
- Visual asset or brand background when the project has assets or image generation is available.

Rules:

- Keep form fields readable and high contrast over any background.
- Do not put critical login text inside generated images.
- Avoid generic slogans like "Empower your business" unless the product brief actually uses them.
- Avoid random blue-purple mesh backgrounds without brand rationale.
- Provide loading, validation, disabled, error, expired-session, and unauthenticated states.

## Workbench First Screen

The workbench top region can be a dashboard hero, command header, or branded overview.

It should answer:

- Who am I operating as?
- What needs attention today?
- What changed since last login?
- What primary action should I take next?
- Which business indicators are abnormal?

Good modules:

- Identity and role context.
- Today focus: approvals, incidents, tasks, deadlines, unread messages.
- Priority metrics with clear units and trend meaning.
- Quick starts for frequent actions.
- Notices or maintenance windows.
- Calendar or timeline when dates matter.

Rules:

- Use visual hierarchy, not giant whitespace, to create impact.
- Use brand texture or generated visuals only as background support.
- Keep primary actions above the fold and permission-aware.
- Metrics must be domain-specific or clearly mock/sample data.
- Avoid the same white card repeated eight times with only fake numbers changed.

## Module Homepage

Use for major modules such as user center, risk control, orders, finance, data assets, workflow, or integration management.

Required:

- Module purpose in one concise Chinese headline.
- Primary CTA for the next common action.
- Current status summary.
- Shortcuts to major subpages.
- Recent activity, risk, or alerts when useful.

Rules:

- Layout can be more expressive than a table page, but must still route users quickly.
- Avoid marketing-style feature storytelling unless the page is onboarding a new module.
- Do not hide operational actions behind visual decoration.

## Empty States And Onboarding

Empty states should be useful, branded, and actionable.

Required:

- State-specific title, not only "暂无数据".
- Business explanation: why it is empty and what the user can do.
- Permission-aware CTA when an action is possible.
- Secondary action such as import, template download, invite teammate, configure integration, or view docs when relevant.
- Existing or generated asset when it improves comprehension.

Rules:

- If the user lacks permission, do not show a create CTA.
- Keep illustration secondary to the action.
- Use different empty-state copy for different modules.

## Dashboards And Command Centers

Dashboards may use stronger visual impact than CRUD pages.

Allowed:

- Dark or brand-forward theme when monitoring context benefits.
- Animated counters or chart transitions when data changes.
- Dense visual rhythm for operations rooms and big screens.
- Background texture, map, topology, or generated scene when tied to the domain.

Required:

- Metric definitions, units, time range, refresh state, abnormal thresholds, and no-data/error states.
- Semantic colors with consistent meaning.
- Drill-down or next action for important anomalies.

Avoid:

- Decorative charts with no decision value.
- Fake precision.
- Saturated color everywhere.
- Motion that hides whether data is current.

## Active ImageGen Protocol

Use existing brand/design-system assets first. If insufficient, actively invoke the available agent image-generation capability. If it is missing or unavailable, use the RIC CLI fallback documented in `../../references/ric-imagegen-fallback.md`.

Do not treat ImageGen as optional when a high-impact admin surface needs a bitmap asset. Once the requirement is clear, generate the asset or explicitly state why a generated bitmap is not needed.

For a new admin system or a visual refresh, plan a coherent Brand Asset Pack before page implementation. The pack should cover the shell brand mark, generated backgrounds, default avatar, empty-state art, and any project-specific bitmap icon family that is not covered by the chosen UI icon library.

Generate assets for:

- Logo/brand mark exploration when the user has no existing brand asset.
- Sidebar/topbar brand mark or app icon variants.
- Project-specific module icon set when generic UI icons are insufficient.
- Full small-icon pack when the user explicitly asks for all small icons to be generated; wire it through a shared icon component instead of scattering raw image tags.
- Login visual panel or background.
- Workbench/module background texture.
- Empty-state illustrations.
- Onboarding or announcement banner.
- Report cover or export preview.
- Neutral profile/avatar placeholder set.
- Page-title or command-header background texture when the page needs a branded header surface.

Triggers:

- New admin system with no usable logo, default avatar, or visual identity assets.
- User asks for unified LOGO, icons, background, or avatar assets.
- `immersive` login page with no existing visual panel/background.
- `product` workbench or module homepage that would otherwise become only cards and text.
- Empty/error/import/export states that would otherwise be generic or visually blank.
- Announcement/onboarding banner that introduces a feature, migration, or maintenance event.
- Dashboard/command-center surface that needs a low-noise map, topology, texture, or monitoring backdrop.
- Report/export preview when the user sees a document-like result.

Do not generate for:

- Ordinary CRUD table backgrounds.
- Functional operation icons already covered by the chosen UI/icon library, unless the user explicitly wants a custom generated icon set.
- Logos, trademarks, QR codes, fake company marks, or fake trust badges.
- Critical UI text that should be real HTML text.

Prompt direction:

- Chinese enterprise SaaS admin product.
- Refined, low-noise, modern, trustworthy.
- Brand color compatible.
- No readable fake UI text inside image.
- No fake logo, trademark, QR code, watermark, or fake company data.

Workflow:

1. Write an Asset Plan before code: asset name, use, intended aspect ratio, generation path, save path, and consuming component.
2. For a Brand Asset Pack, define the shared style first: shape language, color family, light/dark compatibility, icon weight, avatar tone, and background noise level.
3. If built-in ImageGen exists, use it and move/copy the selected project-bound result into the workspace.
4. If built-in/MCP/IDE/agent-native ImageGen is missing or unavailable, use the RIC CLI fallback directly.
5. If `OPENAI_API_KEY` is missing for CLI fallback, stop and ask for it.
6. Wire saved assets into the app. Do not leave referenced assets only in a tool temp folder.
7. At handoff, report the final asset paths and whether built-in ImageGen or CLI fallback was used.

## Final Visual Self-Check

Before finishing a high-impact admin surface, verify:

- The page still works as an admin product surface.
- Brand expression is visible without blocking operations.
- The first viewport has a clear primary action and clear state.
- Visual assets are real, generated, or existing project assets.
- CTA labels are concise, non-duplicated, high contrast, and unwrapped.
- Copy is direct Chinese business language.
- Utility pages remain utility-first.
