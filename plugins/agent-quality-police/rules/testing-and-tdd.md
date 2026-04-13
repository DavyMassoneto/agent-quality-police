---
paths:
  - "**/*.{test,spec}.{ts,tsx,js,jsx}"
  - "**/*.{ts,tsx,js,jsx}"
---

# Testing And TDD

- Write the failing test first when tests are viable.
- Assert behavior through the public contract.
- Keep tests short enough that the claim is obvious without helper archaeology.
- Use mocks only when the real collaborator would make the test less probative, slower beyond reason, or impossible to control.
- Reject tests that only assert calls, implementation details, or internals when a public behavior assertion exists.
