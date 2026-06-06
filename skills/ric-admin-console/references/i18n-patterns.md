# I18n Patterns

Use this reference when an admin-console task asks for multiple languages, language switching, locale-aware routing, translated menus, or when a new system should be i18n-ready.

## Planning

Before implementation, record:

- Default locale, usually `zh-CN` for China-market admin systems.
- Target locales, such as `en-US`, `zh-TW`, `ja-JP`, or tenant-specific languages.
- Mode: `zh-CN only`, `i18n-ready`, or `implemented language switch`.
- Persistence: URL segment, cookie, user profile preference, browser language, or tenant config.
- Translation ownership: local JSON/message files, CMS-managed copy, or backend-provided dictionaries.
- Formatting scope: date, time, timezone, number, percentage, currency, file size, and relative time.

Do not ask for all of this if the repo or user brief already makes it obvious. Record inferred defaults and continue.

## Mandatory Coverage

When i18n is implemented, do not leave these as hardcoded visible strings:

- Shell: app title where variable, menu labels, menu groups, topbar actions, avatar dropdown.
- Navigation: breadcrumbs, route titles, document titles, tab labels, back/return labels.
- Lists: query labels, placeholders, buttons, table column titles, status labels, sort/filter text, pagination text.
- Forms: labels, helper text, validation errors, submit/reset/cancel text, dirty-state warnings.
- Feedback: skeleton/loading text, empty states, errors, toasts, notifications, confirm dialogs.
- Auth and permissions: login errors, session expiration, 403/no-permission text, SSO labels.
- Domain dictionaries: enums, workflow states, task statuses, approval outcomes, audit result labels.

Keep translation keys stable and business-oriented. Avoid keys tied to visual position, such as `leftCardTitle`.

## Framework Defaults

Always inspect the project version and retrieve local skills or official docs before coding i18n APIs.

### Next.js App Router

Default: `next-intl`.

Use when the project uses Next.js App Router or needs server/client translations in a Next app.

Implementation expectations:

- Store messages by locale, commonly `messages/zh-CN.json` and `messages/en-US.json`, or namespaced equivalents.
- Configure request-level locale loading with next-intl request config.
- Wrap client UI with `NextIntlClientProvider` at the app boundary required by the project.
- Choose locale routing deliberately: URL segment for public/SEO surfaces; cookie or user preference for internal admin when URL locale is not desired.
- Translate metadata, page titles, breadcrumbs, menus, forms, and notifications through message keys.
- Use formatter helpers or `Intl.*` APIs for dates, numbers, percentages, and currency.
- Validate missing message keys during build/test when the project tooling supports it.

### React / Vite / SPA

Default: `react-i18next + i18next`.

Use when the project is React Router, Vite, or another client-rendered React admin.

Implementation expectations:

- Initialize `i18next` once near app startup.
- Split resources by namespace when the admin is large: `common`, `menu`, `auth`, `table`, `settings`, and domain modules.
- Use `I18nextProvider` or configured hooks according to the local app style.
- Persist language choice in user profile, cookie, or local storage; do not fight server-side tenant/user preference if one exists.
- Use suspense/loading only if the project is already configured for it; otherwise provide explicit resource loading state.
- Keep route metadata and menu labels translatable from shared dictionaries.

### Vue 3

Default: `vue-i18n` Composition API.

Implementation expectations:

- Configure `createI18n` with Composition API mode when the project uses Vue 3 composition patterns.
- Keep locale messages in structured files and use `useI18n()` in components.
- Translate Vue Router route meta titles, breadcrumbs, `el-menu` labels, table columns, form validation, empty states, and notifications.
- Pair locale switching with Pinia/user settings when the project already uses them.

### Nuxt

Default: `@nuxtjs/i18n`.

Implementation expectations:

- Use the Nuxt i18n module instead of hand-rolled locale routing.
- Configure locales, default locale, lazy message loading, and route strategy according to whether pages are public, internal, or mixed.
- For admin-only systems, prefer a strategy that does not create unnecessary public SEO routes unless required.

### Angular

Default: official Angular i18n for compile-time/localized builds.

Use Angular's official i18n when the project fits static localized builds. If the admin requires runtime language switching without reload, evaluate the existing project convention first, then consider Transloco or ngx-translate. Do not introduce a runtime i18n library without confirming the tradeoff.

### SvelteKit

Default: inspect the app routing and choose a small i18n approach that fits SvelteKit load/routing conventions.

Use URL params, cookies, or user preference consistently. Do not invent SvelteKit APIs; check official docs and the selected i18n package before implementation.

## Theme And Locale Together

Locale switching often changes density:

- Chinese labels are compact; English labels may be longer. Validate toolbar buttons, table headers, sidebars, breadcrumbs, and dropdowns in every implemented locale.
- Do not let translated button text wrap on desktop. Shorten labels or adjust layout.
- Date and number formats must not break table alignment.
- Generated images must not contain critical text, because they cannot be translated reliably.

## Verification

For runnable UI, screenshot each implemented locale for:

- Shell, menu, breadcrumb, and profile dropdown.
- Login or auth page when in scope.
- One list page with query card, table, status labels, and pagination.
- Empty/error/loading states.
- Theme switch combined with locale switch when both are implemented.

Static checks should include missing-key search, hardcoded visible string scans where practical, and type checks for message keys when the chosen library supports them.

## Official Docs To Recheck

Use the project version and current docs before implementation:

- next-intl App Router: https://next-intl.dev/docs/getting-started/app-router
- react-i18next: https://react.i18next.com/getting-started
- Vue I18n Composition API: https://vue-i18n.intlify.dev/guide/advanced/composition
- Nuxt i18n module: https://nuxt.com/modules/i18n
- Angular i18n: https://angular.dev/guide/i18n
- SvelteKit docs: https://svelte.dev/docs/kit
