---
name: anti-bypass-audit
description: Audit a diff for type, test, config, and review fraud. Use when a change looks suspicious, when an LLM-generated diff may have hidden bypasses, or before any final approval.
---

# Objective

Find and report bypasses with short, evidence-based language. This skill is not for rewriting code. It is for blocking unsafe diffs.

## When To Use

- Reviewing TypeScript changes
- Reviewing tests, helpers, mocks, or config
- Checking a diff before merge or publication

## When Not To Use

- Greenfield implementation before any diff exists

## Workflow

1. Scan the diff for banned tokens and suspicious structure.
2. Check whether tests prove behavior or merely confirm implementation.
3. Check whether config was weakened.
4. Produce a terse report with findings, evidence, and required correction.

## Quality Criteria

- Findings cite file evidence.
- Reports separate blockers from optional cleanup.
- The audit stays hostile to bypasses and calm in tone.

## Banned Diff Signals

- `any`
- assertions
- non-null assertions
- `Map` used as a lookup-bag in public or domain-facing contracts
- ts-comments
- `eslint-disable`
- lowered strictness in config
- fake narrowing branches
- helper or factory noise hiding test intent
- mocks that replace the behavior under test

## Report Format

- `Finding:`
- `Evidence:`
- `Required correction:`

## Examples

- Good correction: `examples/good/fixed-bypass.types.ts`, `examples/good/fixed-bypass.ts`
- Bad diff: `examples/bad/explicit-bypass.ts`

## Checklist

- See `checklists/audit-checklist.md`

## References

- `references/report-format.md`
