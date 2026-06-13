# ImageGen Runtime Fallbacks

## Capability Selection

1. Prefer the environment's agent-native image generation capability.
2. Otherwise use an approved MCP or IDE image capability.
3. Otherwise use the configured provider CLI or API only when its active policy permits fallback and required credentials exist.
4. If none is available, return `BLOCKED`.

Codex, Claude Code, Cursor, Windsurf, Cline, Aider, and other agents may map these capabilities differently. Describe capabilities, not product-specific promises.

## Fallback Rules

- Load the selected image provider's current skill or official documentation before execution.
- Respect provider-specific confirmation and model-downgrade requirements.
- Never expose, hardcode, or fabricate credentials.
- For CLI or API work, use existing configured scripts rather than one-off credential-handling code.
- Network failures may use the environment's approved proxy or retry policy.
- Keep intermediate files separate from final project assets and remove unnecessary intermediates.

## Evidence

Record capability used, provider/model when known, prompt, inputs, dimensions, final path, inspection result, and unresolved limitations. Visual deliverables still require independent visual review when they affect product quality.
