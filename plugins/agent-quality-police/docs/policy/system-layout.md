# System Layout

## Canonical Sources

- `framework/entrypoints/`: canonical source for generated prompts and package entrypoints
- `docs/policy/quality-definition.md`: canonical meaning of quality
- `docs/policy/workflow.md`: canonical execution sequence
- `framework/rules/`: canonical always-on rules
- `framework/skills/`: canonical skill source
- `framework/agents/specs/`: canonical agent source
- `framework/agents/prompts/`: canonical agent prompt source
- `framework/distribution/plugin.json`: canonical package and plugin metadata
- `framework/package/`: canonical package installer source

## Generated Projections

- `AGENTS.md`: generated repository contract from canonical sources
- `plugins/agent-quality-police/`: package-ready distribution generated from canonical sources
- `.github/workflows/publish-package.yml`: generated npm publish workflow for the package distribution

## Operational Scripts

- `scripts/build_framework.py`: rebuild repository and package outputs from canonical sources
- `scripts/validate_framework.py`: structural and content validation
- `tests/test_framework_tools.py`: regression tests for the script layer
- `tests/node/install.test.mjs`: regression tests for the package installer
