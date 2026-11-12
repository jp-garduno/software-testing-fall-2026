# Homework 7: Data-Driven Test Suite — E-Commerce Order Processing

**Student**: Pablo Portillo
**Module**: 7 — Data-Driven Testing

## Description

An e-commerce order processing system in Python, tested with data-driven tests that read their cases from CSV and
JSON files, following [homework-7.md](../../../07-data-driven-testing/homework/homework-7.md). The test logic lives
in a few parametrized test functions, and the cases live in `test_data/`.

| | |
| --- | --- |
| Tests | 289 passed ([test_results.txt](test_results.txt)) |
| Statement coverage of `src/` | 100% |
| Branch coverage of `src/` | 100% ([coverage_report.html](coverage_report.html)) |
| Static analysis | pylint 10.00/10 with the course configuration |
| Bonus | A (data generation with Faker) and C (test data validation) |

| Test data | Required | Delivered |
| --- | --- | --- |
| `order_calculations.csv` | 25+ cases | 43 (33 calculations, 10 error cases) |
| `customer_validation.json` | 30+ cases | 42 |
| `order_workflows.json` | 3+ workflows | 7 (34 steps) |
| `generated_orders.csv` (bonus A) | 100 orders | 100 |

## Prerequisites

- Python 3.11+
- pytest, pytest-cov and Faker (`requirements.txt`). Faker is only needed to regenerate
  `generated_orders.csv`, and it is pinned so the file comes out identical.

## Installation

```bash
# From this directory
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the Tests

```bash
python -m pytest -v
```

The test data is checked while pytest collects the tests, so a broken file stops the run with its file and line
number. To check the data files on their own:

```bash
python -m tools.data_files
```

## Coverage Report

```bash
python -m pytest --cov=src --cov-branch --cov-report=term-missing
python -m tools.coverage_report
```

The second command writes `coverage_report.html`, a single page built from the coverage data. coverage.py's own
HTML report (`--cov-report=html`, written to `htmlcov/`, ignored by git) is a folder of pages with generated
JavaScript, and the grading workflow lints every `.js` file in the submission, so it is not committed.

`test_results.txt` is the output of `python -m pytest -v --cov=src --cov-branch --cov-report=term-missing`.

## Regenerating the Generated Orders (bonus A)

```bash
python -m tools.generate_orders
```

This rewrites `test_data/generated_orders.csv` with the same 100 orders, because the seed is fixed. Its expected
amounts come from the current implementation, so it is a regression snapshot: rerun it only after an intended
rule change, and review the diff.

## Project Structure

```
homework-7/
├── src/
│   ├── order_calculator.py       # Part 1: Order — subtotal, discount codes, tax, shipping, total
│   ├── customer_validator.py     # Part 2: email, phone, billing address, credit card (Luhn, expiry, CVV)
│   └── checkout.py               # Part 4: Checkout — validate, create order, pay, confirm
├── tests/
│   ├── test_order_calculator.py  # Part 1: order_calculations.csv
│   ├── test_customer_validator.py# Part 2: customer_validation.json
│   ├── test_order_traditional.py # Part 3: 10 hard-coded tests
│   ├── test_order_data_driven.py # Part 3: the same 10 tests from order_comparison.csv
│   ├── test_integration.py       # Part 4: order_workflows.json with a fake payment gateway
│   ├── test_generated_orders.py  # Bonus A: 100 generated orders, and the generator itself
│   ├── test_data_files.py        # Bonus C: the data validator reports bad data with line numbers
│   ├── test_coverage_report.py   # The coverage page renderer
│   └── order_cases.py            # Builds an Order from a CSV row (shared by three test files)
├── test_data/
│   ├── order_calculations.csv
│   ├── order_comparison.csv
│   ├── generated_orders.csv
│   ├── customer_validation.json
│   └── order_workflows.json
├── tools/
│   ├── data_files.py             # Bonus C: loads and validates every data file
│   ├── generate_orders.py        # Bonus A: seeded Faker generator
│   └── coverage_report.py        # Writes coverage_report.html
├── COMPARISON_REPORT.md          # Part 3: traditional vs data-driven analysis
├── TEST_DATA_SPEC.md             # Format of every data file and the rules the expected values follow
├── coverage_report.html
├── test_results.txt
├── pytest.ini
└── requirements.txt
```

## Implementation

### Order calculator (Part 1)

`Order(items, customer_type="regular", order_date=None)` follows the skeleton in the statement:
`apply_discount(code)`, `set_shipping(distance_km, is_express)`, `calculate_subtotal()`, `calculate_discount()`,
`calculate_tax()`, `calculate_shipping()` and `calculate_total()`.

- Money is computed with `Decimal` and every amount is rounded half up to the cent. Plain floats would make
  sums like `0.1 + 0.2` come out as `0.30000000000000004`; with `Decimal` the totals are exact, so the tests can
  compare them with `==` instead of a tolerance.
- SAVE10 and SAVE20 accept an order at exactly their minimum, NEWUSER only applies to `new` customers, and
  SUMMER25 represents an expired code (last valid day 2026-08-31). Codes are case-insensitive; a code that does not
  qualify returns `False` and leaves the order unchanged.
- Shipping is $0.50 per kg of weight x quantity plus $0.10 per km, x 1.5 for express, and $0 with FREESHIP.
- Negative or non-numeric prices, quantities, weights or distances, fractional quantities, unknown customer types,
  missing item fields and empty orders raise `ValueError` with a message naming the item.

[TEST_DATA_SPEC.md](TEST_DATA_SPEC.md#rules-the-expected-values-follow) lists every rule, and the two places
where the statement is ambiguous and which reading this implementation follows.

### Customer validator (Part 2)

`validate_customer(customer, today=None)` returns a `ValidationResult` with `is_valid` and every error found, in
a fixed order: email, phone, address, credit card. `today` can be fixed so expiry results do not depend on when
the tests run.

### Checkout (Part 4)

`Checkout(gateway, today=None)` runs one order end to end: `validate_customer`, `create_order`,
`calculate_total`, `process_payment` and `generate_confirmation`. Business outcomes are returned as results (a
rejected order, a declined payment), while steps called out of order raise `CheckoutError` (no order yet, paying
twice, confirming an unpaid order). The payment gateway is passed in, so the integration tests use a fake one
whose available credit each workflow sets.

## Bonus Features

- **A. Data generation**: `tools/generate_orders.py` produces 100 valid orders with Faker and a fixed seed, saved to
  `generated_orders.csv` and replayed by `test_generated_orders.py`. A test also checks that rerunning the
  generator gives back exactly the committed file.
- **C. Data validation**: `tools/data_files.py` validates required fields, data types, allowed values and
  internal consistency (totals that add up, `is_valid` matching `errors`) for every file, and reports each problem
  with its file and line number. `test_data_files.py` feeds it 38 broken files to prove it catches them.

## Author

Pablo Portillo — Software Testing, Fall 2026
