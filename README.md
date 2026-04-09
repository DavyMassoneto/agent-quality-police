# agent-quality-police

Strict governance framework for Claude Code, Codex, and OpenCode with rules, skills, and audit agents that block testing and typing bypasses.

## Purpose

This repository is a reusable governance pack for coding agents. It is designed to be copied into a project or used as the source for a stricter house style. The framework assumes:

- TDD is mandatory when tests are viable.
- Tests must prove observable behavior, not internal implementation.
- TypeScript must stay strongly typed without `any`, assertions, non-null assertions, or comment-based bypasses.
- Review must be hostile to fake greens, config weakening, and abstraction noise.

## Canonical Structure

- `AGENTS.md`: canonical routing instructions for Codex and OpenCode.
- `CLAUDE.md`: Claude router that imports `AGENTS.md`.
- `docs/policy/`: canonical quality definition and workflow.
- `.claude/rules/`: always-on Claude rules.
- `.claude/skills/`: canonical skill source.
- `.agents/skills/`: generated Codex skill projection.
- `framework/agents/specs/`: canonical agent specs.
- `.claude/agents/`, `.opencode/agents/`, `.codex/agents/`: generated agent projections.
- `scripts/`: build and validation utilities.
- `tests/`: regression tests for the projection and validation utilities.

## Working Model

1. Update canonical content first.
2. Rebuild projections.
3. Validate the repository.
4. Only then commit or publish.

Commands:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
```

## Installation and Reuse

Minimal copy set:

- `AGENTS.md`
- `CLAUDE.md`
- `docs/policy/`
- `.claude/`
- `.agents/`
- `.opencode/agents/`
- `.codex/agents/`
- `opencode.json`
- `scripts/`

After copying into another repository, run:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
```

The build step refreshes generated projections so Codex and OpenCode stay aligned with the canonical Claude skill set and the canonical agent specs.

## Evolution Rules

- Update `docs/policy/quality-definition.md` first when changing the meaning of quality.
- Add new reusable workflows as skills under `.claude/skills/`.
- Add new agents by creating a spec under `framework/agents/specs/` and rebuilding.
- Do not hand-edit generated files under `.agents/skills/`, `.claude/agents/`, `.opencode/agents/`, or `.codex/agents/`.
