# Install Steps

Copy these paths into the target repository:

- `docs/policy/`
- `.claude/`
- `.agents/`
- `.claude-plugin/marketplace.json`
- `.opencode/agents/`
- `.codex/agents/`
- `plugins/agent-quality-police/`
- `opencode.json`
- `scripts/`
- `tests/`

Canonical source paths that must be present before build:

- `framework/entrypoints/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/`
- `framework/package/`

Then run the build and validation commands from the repository root.

For package-style global installation after build, use the generated package entrypoint:

- `node plugins/agent-quality-police/bin/aqp.mjs install all`
