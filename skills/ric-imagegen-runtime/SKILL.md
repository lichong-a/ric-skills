---
name: ric-imagegen-runtime
description: Use when generated or edited raster assets are required in an environment where ImageGen capabilities, providers, credentials, or output paths may vary.
---
# RIC ImageGen Runtime

Provide a capability-based ImageGen execution contract without tying the workflow to one agent product.

## Required Procedure

1. Load the active environment's ImageGen skill or official provider guidance before generation.
2. Record the asset purpose, dimensions, prompt, exact text, constraints, output path, and consuming location.
3. Detect available capabilities in this order: agent-native image generation, approved MCP/IDE image tool, canonical trusted provider CLI/API fallback.
4. Follow the selected provider's authorization, model, transparency, and downgrade rules. Never fabricate a tool result or silently change provider/model policy.
5. Save project-bound final assets inside the project. Do not leave referenced assets only in a temporary or agent-private location.
6. Inspect each output for dimensions, text accuracy, watermark, artifacts, brand fit, and constraints. Iterate with targeted changes.
7. Record selected output, rejected variants, prompt, execution path, and validation evidence.

Read [references/runtime-fallbacks.md](references/runtime-fallbacks.md) when selecting or degrading the execution path. Resolve CLI paths to their canonical location and require explicit confirmation for environment overrides or paths outside the trusted system-skill directory.

## Stop Conditions

Return `BLOCKED` when no approved image capability is available, required credentials are missing, generation would violate policy, or the output cannot be validated. Never substitute a fake screenshot, placeholder, or unrelated stock image while claiming ImageGen completion.
