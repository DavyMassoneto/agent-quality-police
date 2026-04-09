# Modeling Patterns

## Preferred Shapes

- Use `interface` for object contracts.
- Use named union types for state transitions.
- Keep parsing at the external boundary.
- Turn uncertain input into explicit success or failure results.

## Forbidden Shortcuts

- `any`
- assertions
- non-null assertions
- ts-comment bypasses
- generic records standing in for domain design
