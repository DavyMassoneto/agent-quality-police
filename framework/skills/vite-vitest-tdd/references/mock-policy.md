# Mock Policy

## Acceptable Mock

Use a mock when the collaborator is outside the unit under test and the behavior claim still depends on the unit’s public result.

## Fraudulent Mock

Reject a mock when it returns the exact answer that the unit under test was supposed to compute, or when the test only asserts call counts without user-visible consequence.
