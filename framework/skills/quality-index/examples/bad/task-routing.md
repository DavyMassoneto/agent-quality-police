# Bad Routing

Task: rename a private helper and add a feature.

Routing mistake:

1. load every skill in the repository
2. skip tests because the rename is “minor”
3. ship without `bypass-auditor`

Why this is bad:

- It hides the real feature risk under irrelevant context.
- It assumes rename and behavior change can share a shortcut.
- It skips the mandatory audit flow.
