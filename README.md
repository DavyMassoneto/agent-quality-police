# agent-quality-police

Strict governance framework for Claude Code, Codex, and OpenCode with rules, skills, and audit agents that block testing and typing bypasses.

## Purpose

This repository is a reusable governance pack for coding agents. It is designed to be copied into a project or used as the source for a stricter house style. The framework assumes:

- TDD is mandatory when tests are viable.
- Tests must prove observable behavior, not internal implementation.
- TypeScript must stay strongly typed without `any`, assertions, non-null assertions, comment-based bypasses, or inline structural types.
- Review must be hostile to fake greens, config weakening, and abstraction noise.

## Canonical Structure

- `framework/entrypoints/`: canonical source for generated prompts and package entrypoints.
- `docs/policy/`: canonical quality definition and workflow.
- `framework/rules/`: canonical always-on rules.
- `framework/skills/`: canonical skill source.
- `framework/agents/specs/`: canonical agent specs.
- `framework/agents/prompts/`: canonical agent prompts.
- `framework/distribution/plugin.json`: canonical package/plugin metadata.
- `framework/package/`: canonical package installer source.
- `AGENTS.md`: generated repository routing contract.
- `plugins/agent-quality-police/`: package-ready generated distribution.
- `.github/workflows/publish-package.yml`: generated npm publish workflow for the package distribution.
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
- `framework/rules/`
- `framework/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `scripts/`
- `tests/`

Generated outputs in this repository:

- `AGENTS.md`
- `plugins/agent-quality-police/`
- `.github/workflows/publish-package.yml`

Never hand-edit generated outputs.

### Generated-only reuse

Copy these files if you want to consume the framework in another repository without rebuilding it:

- `AGENTS.md`
- `docs/policy/`
- `plugins/agent-quality-police/`

Do not run `python3 scripts/build_framework.py` in this mode. The build step is for framework development and requires canonical sources such as `framework/agents/specs/` and `framework/agents/prompts/`. Running build without those sources would be incorrect, and the builder now fails explicitly instead of silently deleting agent projections.

### Framework development

Copy or clone the full framework development set before running build:

- `framework/entrypoints/`
- `docs/policy/`
- `framework/rules/`
- `framework/skills/`
- `framework/agents/specs/`
- `framework/agents/prompts/`
- `framework/distribution/plugin.json`
- `framework/package/`
- `plugins/agent-quality-police/`
- `scripts/`
- `tests/`

After the canonical sources are present, run:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

The build step refreshes the repository contract plus the package-ready distribution generated from the canonical framework sources.

### Package-style installation

The generated package lives at `plugins/agent-quality-police/` and includes a Node entrypoint:

```bash
node plugins/agent-quality-police/bin/aqp.mjs install
```

This is the intended local installation path for user-level Claude Code, Codex, and OpenCode setup. The installer runs interactively, asks which tools to install for, and asks per tool whether it may manage the global root entrypoint file.

For npm distribution, the generated package also includes:

- `plugins/agent-quality-police/README.md`
- `plugins/agent-quality-police/LICENSE`
- `.github/workflows/publish-package.yml`

The workflow publishes from `plugins/agent-quality-police/`, which is the directory intended to back `npx agent-quality-police install` after npm publication.

If the user allows root management, the installer writes:

- Claude Code: `~/.claude/CLAUDE.md`
- Codex: `~/.codex/AGENTS.md`
- OpenCode: `~/.config/opencode/AGENTS.md`

If the user denies root management, the installer still installs skills, agents, docs, and optional commands, then prints the exact fallback content to paste into the global root file so the LLM can still load the policy autonomously:

- Claude Code: append the generated `CLAUDE.md` prompt body manually
- Codex: append the generated `AGENTS.md` prompt body manually
- OpenCode: append the generated `AGENTS.md` prompt body manually

### Release Flow

Before publishing a new version, update the canonical package metadata in `framework/distribution/plugin.json`, then run:

```bash
python3 scripts/build_framework.py
python3 scripts/validate_framework.py
python3 -m unittest tests/test_framework_tools.py
node --test tests/node/install.test.mjs
```

Publishing is performed by GitHub Actions through `.github/workflows/publish-package.yml` and publishes the generated package from `plugins/agent-quality-police/`.

To release a new version:

```bash
git tag plugin-vX.Y.Z
git push origin plugin-vX.Y.Z
```

After the workflow completes, the package is available through:

```bash
npx agent-quality-police install
```

### Codex `skills.config`

This repository does not emit `skills.config` in `plugins/agent-quality-police/.codex/agents/*.toml`.

Reason:

- Codex already discovers packaged skills from `.agents/skills`.
- The current official `skills.config` examples for custom agents use an absolute path.
- This repository does not bake absolute path values into versioned files.

If OpenAI documents a safe relative-path form for versioned repositories, the projection can be revisited.

## Evolution Rules

- Update `docs/policy/quality-definition.md` first when changing the meaning of quality.
- Add new reusable workflows as skills under `framework/skills/`.
- Add new agents by creating a spec under `framework/agents/specs/` and rebuilding.
- Do not hand-edit generated files under `AGENTS.md`, `plugins/agent-quality-police/`, or `.github/workflows/publish-package.yml`.
