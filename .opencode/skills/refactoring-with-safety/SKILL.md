---
name: refactoring-with-safety
description: Refactor without masking risk. Use when changing structure, names, extraction boundaries, or flow while claiming to preserve behavior.
---

# Objective

Make refactors prove preservation instead of assuming it.

## When To Use

- Structural cleanup without intended behavior change
- Extracting modules or moving responsibilities
- Legacy code improvements where current behavior is unclear

## When Not To Use

- Straightforward feature work with a clear new behavior target
- Changes that are purely formatting

## Workflow

1. Characterize the current behavior first.
2. Freeze the public contract with tests.
3. Change structure in small slices.
4. Re-run the characterization after each slice.
5. Stop calling it a refactor if behavior changes.

## Quality Criteria

- Existing behavior is documented by tests or explicit evidence.
- Structural change and behavior change are not smuggled together.
- New abstractions clarify responsibility instead of centralizing uncertainty.

## Anti-Patterns

- “Refactor” commits that also alter business rules
- mass renames plus logic change plus config edits in one step
- extracting helpers before the current behavior is pinned down

## Examples

- Good sequence: `examples/good/characterization-sequence.md`
- Bad sequence: `examples/bad/behavior-change-masquerading.md`

## Checklist

- See `checklists/refactor-checklist.md`

## References

- `references/refactor-sequence.md`
