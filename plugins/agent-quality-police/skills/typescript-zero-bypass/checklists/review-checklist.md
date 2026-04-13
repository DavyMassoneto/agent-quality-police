# Review Checklist

- Are all types named and meaningful?
- Did the diff avoid assertions and non-null assertions?
- Did the code avoid fake fallback branches that only satisfy the compiler?
- Is external input validated at the edge instead of coerced in the middle?
