---
name: governance-installation
description: Install or update this governance framework in another repository. Use when copying the pack, regenerating projections, or validating that a target repository is aligned with the canonical policy.
---

# Objective

Install or refresh the framework without letting generated projections drift away from the canonical policy.

## When To Use

- Copying the framework into another repository
- Updating skills, rules, or agent specs and rebuilding projections
- Verifying that generated files were refreshed after a policy change

## When Not To Use

- Day-to-day feature work inside a repository that already has the framework installed

## Workflow

1. Copy the canonical files first.
2. Run `python3 scripts/build_framework.py`.
3. Run `python3 scripts/validate_framework.py`.
4. If scripts changed, run `python3 -m unittest tests/test_framework_tools.py`.
5. Commit only after projections and validation are green.

## Quality Criteria

- Canonical and generated layers are both present.
- `.agents/skills/` matches `.claude/skills/`.
- Agent projections exist for Claude, OpenCode, and Codex.
- No placeholders, missing links, or stale projections remain.

## Anti-Patterns

- Editing generated files by hand
- Copying only the generated layers and skipping the canonical source
- Publishing without running build and validation

## Examples

- Good install flow: `examples/good/install-sequence.md`
- Bad install flow: `examples/bad/stale-projection.md`

## Checklist

- See `checklists/install-checklist.md`

## References

- `references/install-steps.md`
