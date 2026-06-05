# Copilot Instructions: RIC Taste Standard

> **Note:** GitHub Copilot automatically reads this file to set its global behavior. This repository is a RIC derivative of `Leonxlnx/taste-skill`, so Copilot should follow the RIC skill set rather than upstream install names.

## The RIC Anti-Slop Manifesto

1. **Use the right RIC skill:** Landing pages use `ric-design-taste-frontend`; admin panels, CRUD, permissions, tables, and back offices use `ric-admin-console`.
2. **No generic UI:** Do not generate default SaaS templates or default blue-white admin shells without hierarchy, state coverage, and business-specific structure.
3. **Complete implementation:** No placeholders, no `// TODO: add actual code here`, no omitted files.
4. **PowerShell and pnpm by default:** Prefer Windows PowerShell examples and pnpm commands. Do not change global FNM defaults.
5. **Infrastructure safety:** Reuse shared RIC infrastructure, use environment variables for secrets, and never generate destructive data operations.
6. **Contextual awareness:** For deep rules, read the localized `SKILL.md` files in `skills/`.
