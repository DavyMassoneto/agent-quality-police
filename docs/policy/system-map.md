# System Map

## Canonical Sources

- `AGENTS.md`: cross-tool routing contract
- `docs/policy/quality-definition.md`: canonical meaning of quality
- `docs/policy/workflow.md`: canonical execution sequence
- `.claude/skills/`: canonical skill source
- `framework/agents/specs/`: canonical agent source

## Generated Projections

- `.agents/skills/`: Codex-compatible skill mirror generated from `.claude/skills/`
- `.claude/agents/`: Claude subagents generated from canonical specs
- `.opencode/agents/`: OpenCode agents generated from canonical specs
- `.codex/agents/`: Codex agents generated from canonical specs

## Operational Scripts

- `scripts/build_framework.py`: rebuild skill and agent projections
- `scripts/validate_framework.py`: structural and content validation
- `tests/test_framework_tools.py`: regression tests for the script layer
