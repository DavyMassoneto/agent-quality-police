# agent-quality-police

Strict governance framework for Claude Code, Codex, and OpenCode with rules, skills, and audit agents that block testing and typing bypasses.

## Purpose

This repository is a reusable governance pack for coding agents. It is designed to be copied into a project or used as the source for a stricter house style. The framework assumes:

- TDD is mandatory when tests are viable.
- Tests must prove observable behavior, not internal implementation.
- TypeScript must stay strongly typed without `any`, assertions, non-null assertions, comment-based bypasses, or inline structural types.
- Review must be hostile to fake greens, config weakening, and abstraction noise.

## Canonical Structure

- `framework/entrypoints/`: canonical source for generated root entrypoints and OpenCode config.
- `docs/policy/`: canonical quality definition and workflow.
- `.claude/rules/`: always-on Claude rules.
- `.claude/skills/`: canonical skill source.
- `.agents/skills/`: generated Codex skill projection.
- `.opencode/skills/`: generated OpenCode skill projection.
- `framework/agents/specs/`: canonical agent specs.
- `framework/distribution/plugin.json`: canonical package/plugin metadata.
- `framework/package/`: canonical package installer source.
- `AGENTS.md`: generated repository routing contract.
- `CLAUDE.md`: generated repository Claude router.
- `opencode.json`: generated repository OpenCode config.
- `.claude/agents/`, `.opencode/agents/`, `.codex/agents/`: generated agent projections.
- `plugins/agent-quality-police/`: package-ready generated distribution.
- `.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`: generated local marketplaces.
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
node --test tests/node/install.test.mjs
```

## Installation and Reuse

Canonical sources in this repository:

- `framework/entrypoints/`
- `docs/policy/`
- `.claude/rules/`
- `.claude/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `scripts/`
- `tests/`

Generated outputs in this repository:

- `AGENTS.md`
- `CLAUDE.md`
- `opencode.json`
- `.agents/skills/`
- `.opencode/skills/`
- `.claude/agents/`
- `.opencode/agents/`
- `.codex/agents/`
- `plugins/agent-quality-police/`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`

Never hand-edit generated outputs.

### Generated-only reuse

Copy these files if you want to consume the framework in another repository without rebuilding it:

- `AGENTS.md`
- `CLAUDE.md`
- `opencode.json`
- `docs/policy/`
- `.claude/rules/`
- `.claude/skills/`
- `.agents/skills/`
- `.opencode/skills/`
- `.claude/agents/`
- `.opencode/agents/`
- `.codex/agents/`
- `plugins/agent-quality-police/`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `opencode.json`

Do not run `python3 scripts/build_framework.py` in this mode. The build step is for framework development and requires canonical sources such as `framework/agents/specs/` and `framework/agents/prompts/`. Running build without those sources would be incorrect, and the builder now fails explicitly instead of silently deleting agent projections.

### Framework development

Copy or clone the full framework development set before running build:

- `framework/entrypoints/`
- `docs/policy/`
- `.claude/rules/`
- `.claude/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `.agents/skills/`
- `.claude/agents/`
- `.opencode/agents/`
- `.codex/agents/`
- `plugins/agent-quality-police/`
- `.claude-plugin/marketplace.json`
- `.agents/plugins/marketplace.json`
- `opencode.json`
- `scripts/`
- `tests/`

After the canonical sources are present, run:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

The build step refreshes generated projections so Codex and OpenCode stay aligned with the canonical Claude skill set and the canonical agent specs, and also emits a package-ready distribution plus local marketplace catalogs for Claude and Codex.

### Package-style installation

The generated package lives at `plugins/agent-quality-police/` and includes a Node entrypoint:

```bash
node plugins/agent-quality-police/bin/aqp.mjs install
```

This is the intended local installation path for user-level Claude Code, Codex, and OpenCode setup. The installer runs interactively, asks which tools to install for, and asks per tool whether it may manage the global root entrypoint file.

If the user allows root management, the installer writes:

- Claude Code: `~/.claude/CLAUDE.md`
- Codex: `~/.codex/AGENTS.md`
- OpenCode: `~/.config/opencode/AGENTS.md`

If the user denies root management, the installer still installs skills, agents, docs, and optional commands, then prints the exact fallback content to paste into the global root file so the LLM can still load the policy autonomously:

- Claude Code: append the generated `CLAUDE.md` prompt body manually
- Codex: append the generated `AGENTS.md` prompt body manually
- OpenCode: append the generated `AGENTS.md` prompt body manually

For Claude Code distribution, the repository now also emits `.claude-plugin/marketplace.json`, which follows the official marketplace/plugin model and can later be switched to an npm source when publishing the generated package.

### Codex `skills.config`

This repository does not emit `skills.config` in `.codex/agents/*.toml`.

Reason:

- Codex already discovers repository skills from `.agents/skills`.
- The current official `skills.config` examples for custom agents use an absolute path.
- This repository does not bake absolute path values into versioned files.

If OpenAI documents a safe relative-path form for versioned repositories, the projection can be revisited.

## Evolution Rules

- Update `docs/policy/quality-definition.md` first when changing the meaning of quality.
- Add new reusable workflows as skills under `.claude/skills/`.
- Add new agents by creating a spec under `framework/agents/specs/` and rebuilding.
- Do not hand-edit generated files under `.agents/skills/`, `.claude/agents/`, `.opencode/agents/`, `.codex/agents/`, `plugins/agent-quality-police/`, `.claude-plugin/marketplace.json`, or `.agents/plugins/marketplace.json`.
