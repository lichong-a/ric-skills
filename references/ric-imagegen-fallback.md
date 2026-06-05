# RIC Image Generation Fallback

Use this reference from any RIC skill that needs generated bitmap assets.

## Rule

Prefer the environment's built-in image generation capability when it exists. If the built-in image generation tool, MCP image tool, IDE image tool, or agent-native image capability is missing or unavailable, use the bundled CLI fallback directly instead of stopping.

This RIC repository intentionally changes the upstream default: missing built-in image tooling is not a blocker when the CLI path is available.

## CLI Requirements

The fallback CLI is:

```powershell
$env:IMAGE_GEN = "$env:USERPROFILE\.codex\skills\.system\imagegen\scripts\image_gen.py"
python $env:IMAGE_GEN --help
```

Equivalent path when `CODEX_HOME` is set:

```powershell
$env:IMAGE_GEN = "$env:CODEX_HOME\skills\.system\imagegen\scripts\image_gen.py"
python $env:IMAGE_GEN --help
```

Requirements:

- Network access.
- `OPENAI_API_KEY` in the environment.
- Do not hardcode the key.
- Do not modify `scripts/image_gen.py`.
- Save final project-bound assets under the workspace, usually `output/imagegen/` or the app's asset directory.
- Use `tmp/imagegen/` only for temporary JSONL prompts or scratch files.

If `OPENAI_API_KEY` is missing, stop and tell the user the exact missing variable. Do not fabricate credentials.

## One-Off Generation

```powershell
python $env:IMAGE_GEN generate `
  --prompt "A refined enterprise admin login illustration, abstract operations dashboard forms, clean blue-gray palette, no text, no logo, no watermark" `
  --use-case "ui-mockup" `
  --size 1536x1024 `
  --quality high `
  --out output/imagegen/admin-login-illustration.png
```

## Batch Generation

Use `generate-batch` when multiple distinct assets are needed and CLI fallback is being used.

```powershell
New-Item -ItemType Directory -Force tmp/imagegen, output/imagegen/admin-assets | Out-Null
@'
{"prompt":"Refined empty-state illustration for a Chinese enterprise admin system, no text, no logo, light blue-gray palette","use_case":"ui-mockup","size":"1024x1024","quality":"medium","out":"empty-state.png"}
{"prompt":"Subtle enterprise dashboard texture background, clean grid, low contrast, no text, no logo","use_case":"productivity-visual","size":"1536x1024","quality":"medium","out":"dashboard-texture.png"}
'@ | Set-Content -LiteralPath tmp/imagegen/admin-assets.jsonl -Encoding UTF8

python $env:IMAGE_GEN generate-batch `
  --input tmp/imagegen/admin-assets.jsonl `
  --out-dir output/imagegen/admin-assets `
  --concurrency 5
```

## Transparent Assets

For simple opaque cutouts, built-in image generation plus chroma-key removal is preferred when available. If the built-in tool is unavailable and the user needs true transparent output, CLI fallback can use:

```powershell
python $env:IMAGE_GEN generate `
  --model gpt-image-1.5 `
  --prompt "Clean enterprise app icon on transparent background, no text, no watermark" `
  --background transparent `
  --output-format png `
  --out output/imagegen/app-icon.png
```

Use `gpt-image-1.5` only when true transparency is required. Keep `gpt-image-2` as the normal CLI default.

## Prompt Rules

- State where the asset will be used: login page, workbench empty state, onboarding card, report cover, module icon, background texture, profile placeholder, or announcement banner.
- For admin-console assets, keep them quiet, enterprise-refined, and non-decorative.
- Avoid readable text in generated images unless the exact text is required.
- Avoid logos, trademarks, watermarks, QR codes, fake company names, and fake data.
- Generate distinct assets with distinct prompts instead of using `--n` for unrelated deliverables.
