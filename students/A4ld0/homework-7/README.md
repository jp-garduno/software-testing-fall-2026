# Homework 7 · Data-driven order testing

The order calculator, customer validator, and checkout workflow are in `src/`. The automated tests are in `tests/` and their inputs are in `test_data/`.

## Run locally

Use Node.js 22 or later with npm. Open a terminal in the `homework-7` directory and install the locked Jest dependencies.

```sh
npm ci
npm test
npm run verify
npm run benchmark
```

- `npm test` validates the fixtures, runs Jest, and enforces coverage above 80% for statements, branches, and lines in `src/`.
- `npm run verify` runs the same checks and regenerates `test_results.txt` and `coverage_report.html`.
- `npm run benchmark` measures 10, 50, 100, and 500 cases and regenerates `benchmark_results.html`.

## Suite contents

| Tests | Cases |
|---|---:|
| Order calculations from CSV | 29 |
| Customer validations from JSON | 30 |
| Traditional and data-driven comparison | 10 per version |
| Checkout workflows from JSON | 4 workflows with 5 steps each |
| Additional checkout state test | 1 |

Three workflows complete payment and confirmation. The fourth verifies that an invalid customer cannot place an order. Payment is simulated in memory. Jest counts each workflow as one test that checks every step in sequence.

## Implementation decisions

- The written discount thresholds are strict. `SAVE10` requires a subtotal above $50 and `SAVE20` requires a subtotal above $100. `NEWUSER` applies to customers marked as new. An unknown or expired coupon is rejected.
- Shipping includes the quantity of each item when calculating total weight. Zero quantities are accepted. Negative prices, quantities, weights, and distances raise `RangeError`.
- Calculation results retain full precision. Tests allow a tolerance of $0.000001 for floating-point comparisons.
- The customer validator accepts expiration through the end of the stated month. Tests use a fixed date to keep expiration scenarios reproducible.
- The two bonus features are execution-time comparison and fixture validation.

See [TEST_DATA_SPEC.md](TEST_DATA_SPEC.md) for fixture formats and [COMPARISON_REPORT.md](COMPARISON_REPORT.md) for the test suite comparison.
