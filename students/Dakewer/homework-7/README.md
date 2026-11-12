# Homework 7: Data-Driven Test Suite

Order-processing system (order calculator + customer validator + a small
workflow engine) tested with **external CSV/JSON data** and `pytest`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
./run_tests.sh                   # everything + coverage + result files
# or just the tests:
python -m pytest -v
python -m pytest tests/test_order_calculator.py -v     # one module
python -m pytest --cov=src --cov-report=term-missing   # coverage in terminal
```

`run_tests.sh` validates the data files, regenerates the seeded bonus data,
runs all tests, and writes `test_results.txt` and `coverage_report.html`.

## Project layout

```
src/
  order_calculator.py      Order: subtotal, discounts, tax, shipping, total
  customer_validator.py    email, phone, address, Luhn card, expiration
  order_processor.py       OrderWorkflow engine used by integration tests
tests/
  data_loader.py                 CSV loader + shared assertions
  test_order_calculator.py       data-driven, order_calculations.csv
  test_customer_validator.py     data-driven, customer_validation.json
  test_order_traditional.py      10 hardcoded tests (Part 3)
  test_order_data_driven.py      same 10 scenarios from CSV (Part 3)
  test_integration.py            workflows from order_workflows.json
  test_generated_orders.py       100 generated orders (bonus A)
  test_data_validation.py        tests for the validator tool (bonus C)
test_data/                       all test data (see TEST_DATA_SPEC.md)
tools/
  generate_orders.py             bonus A: Faker-based data generator
  validate_test_data.py          bonus C: data validation with line numbers
  inline_coverage.py             builds the single-file coverage_report.html
```

## Results

| Item | Count |
|---|---|
| Order calculation cases (CSV) | 34 (min. 25) |
| Customer validation cases (JSON) | 37 (min. 30) |
| Workflows (JSON) | 6 (min. 3) |
| Generated regression orders | 100 |
| Total tests | 241, all passing |
| Statement coverage of `src/` | 100% |

## Business-rule decisions

The assignment leaves a few points open; these are the choices made (also
documented in the module docstrings):

- Money uses `Decimal`, rounded half-up to cents per component.
- Discount minimums are **inclusive** ($50.00 qualifies for `SAVE10`),
  matching the starter code's `subtotal < min_order` check.
- `NEWUSER` only applies when `customer_type == "new"`.
- Weight cost uses `weight x quantity` for each item.
- Invalid (negative / non-numeric) prices, quantities, weights or distances
  raise `ValueError`.
- The sample row in the assignment text lists `expected_shipping = 5.50`
  for 1 kg and 10 km, but the stated rules give `0.50 + 1.00 = 1.50`.
  The rules were followed (see `shipping_weight_and_distance`).
- Test tolerance is half a cent (`abs=0.005`). The sample test's
  `rel=1e-2` would accept a 1% error, which is too loose for money.

## Bonus implemented

- **Option A** - `tools/generate_orders.py` (Faker, seeded, 100 orders).
- **Option C** - `tools/validate_test_data.py` (required fields, types,
  duplicate names, line numbers in error messages).

## Conventional commits

Commit history follows `type(scope): message` (`feat`, `test`, `docs`, `chore`).
