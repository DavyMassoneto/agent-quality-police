# Good Sequence

1. Add a characterization test that captures current invoice rounding behavior.
2. Keep the old implementation untouched until that test is green.
3. Extract the calculator into a named module.
4. Re-run the characterization test.
5. Remove duplication only after the behavior remains proven.

Why this is good:

- The behavior was frozen before structure changed.
- Each step had a clear proof boundary.
