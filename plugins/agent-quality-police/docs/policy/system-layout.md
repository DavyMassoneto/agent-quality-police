# System Layout

## Canonical Sources

- `framework/entrypoints/`: canonical source for generated root entrypoints and OpenCode config
- `docs/policy/quality-definition.md`: canonical meaning of quality
- `docs/policy/workflow.md`: canonical execution sequence
- `.claude/skills/`: canonical skill source
- `framework/agents/specs/`: canonical agent source
- `framework/distribution/plugin.json`: canonical package and plugin metadata
- `framework/package/`: canonical package installer source

## Generated Projections

- `AGENTS.md`: generated cross-tool routing contract for repository scope
- `CLAUDE.md`: generated Claude router for repository scope
- `opencode.json`: generated OpenCode config for repository scope
- `.agents/skills/`: Codex-compatible skill mirror generated from `.claude/skills/`
- `.opencode/skills/`: OpenCode-compatible skill mirror generated from `.claude/skills/`
- `.claude/agents/`: Claude subagents generated from canonical specs
- `.opencode/agents/`: OpenCode agents generated from canonical specs
- `.codex/agents/`: Codex agents generated from canonical specs
- `plugins/agent-quality-police/`: package-ready distribution generated from canonical sources
- `.claude-plugin/marketplace.json`: Claude marketplace catalog for the generated package
- `.agents/plugins/marketplace.json`: Codex marketplace catalog for the generated package

## Operational Scripts

- `scripts/build_framework.py`: rebuild skill projections, agent projections, and package distributions
- `scripts/validate_framework.py`: structural and content validation
- `tests/test_framework_tools.py`: regression tests for the script layer
- `tests/node/install.test.mjs`: regression tests for the package installer
