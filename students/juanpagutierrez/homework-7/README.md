# Homework 7: Data-Driven Test Suite

**Student:** Juan Pablo Gutierrez (`juanpagutierrez`)
**Module:** 7 - Data-Driven Testing
**Language:** Python 3.11+ with pytest

An e-commerce order processing system (order pricing, customer validation and
an end-to-end checkout) tested mostly from external CSV and JSON data.

## Results

| | |
| --- | --- |
| Tests | **457 passed**, 0 failed (`test_results.txt`) |
| Coverage of `src/` | **100%** statements and **100%** branches (`coverage_report.html`) |
| Pylint (course configuration) | **10.00/10** |
| Test data | 42 order cases (CSV), 45 customer cases (JSON), 6 workflows with 37 steps (JSON), 100 generated orders (CSV) |
| Bonus | **A** Faker data generation and **C** test data validation |

## Setup

```bash
cd students/juanpagutierrez/homework-7
python -m venv venv
venv\Scripts\activate            # Windows  (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
```

## Running

```bash
# All tests
pytest

# With coverage, as the automated grading runs it
pytest --cov=src --cov-branch --cov-report=term-missing

# One part at a time
pytest tests/test_order_calculator.py       # Part 1
pytest tests/test_customer_validator.py     # Part 2
pytest tests/test_order_traditional.py tests/test_order_data_driven.py   # Part 3
pytest tests/test_integration.py            # Part 4

# One case by its test_name from the data files
pytest -k discount_save10_at_threshold

# Check the data files without running any test (Bonus C)
python -m src.data_validation

# Regenerate the 100 Faker orders (Bonus A); review the diff before committing
python -m src.data_generator
```

## Structure

```
homework-7/
├── src/
│   ├── order_calculator.py      # Part 1: Order (subtotal, discounts, tax, shipping, total)
│   ├── customer_validator.py    # Part 2: email, phone, address, Luhn, expiration, CVV
│   ├── order_processor.py       # Part 4: validate -> create -> calculate -> pay -> confirm
│   ├── data_loader.py           # Reads the CSV/JSON files into typed test cases
│   ├── data_validation.py       # Bonus C: checks the data files, reports line numbers
│   └── data_generator.py        # Bonus A: Faker orders and customers
├── tests/
│   ├── test_order_calculator.py     # Part 1, from order_calculations.csv
│   ├── test_customer_validator.py   # Part 2, from customer_validation.json
│   ├── test_order_traditional.py    # Part 3, 10 hardcoded tests
│   ├── test_order_data_driven.py    # Part 3, the same 10 tests from order_comparison.csv
│   ├── test_integration.py          # Part 4, from order_workflows.json
│   ├── test_data_validation.py      # Bonus C
│   └── test_data_generator.py       # Bonus A, 100-order regression
├── test_data/
│   ├── order_calculations.csv
│   ├── customer_validation.json
│   ├── order_workflows.json
│   ├── order_comparison.csv
│   └── generated_orders.csv
├── README.md
├── COMPARISON_REPORT.md         # Part 3 analysis
├── TEST_DATA_SPEC.md            # Format of every data file and the business rules
├── coverage_report.html
├── test_results.txt
└── requirements.txt
```

## How the data-driven tests work

1. `src/data_loader.py` reads a data file and **validates it first**
   (`src/data_validation.py`). A broken file stops the run with messages like
   `order_calculations.csv:14: [is_express] must be 'true' or 'false', got 'ture'`.
2. Each row or object becomes a small dataclass (`OrderCase`, `CustomerCase`,
   `Workflow`).
3. A test is parameterized with the list of cases and uses
   `ids=lambda case: case.test_name`, so each case appears in the report under
   its own name, for example
   `test_order_calculation[shipping_express_rounds_half_up]`.

The test files contain no expected values for the main scenarios. Adding a case
means adding a row to a CSV or an object to a JSON file; see `TEST_DATA_SPEC.md`.

## Design decisions

- **Money uses `Decimal`** and each amount is rounded to cents with half-up
  rounding. With floats, express shipping for 0.1 kg and 20 km is
  `3.0749999999999997` and `round()` gives 3.07 instead of 3.08. The
  `shipping_express_float_rounding_trap` case covers this.
- **Thresholds are inclusive.** The starter code rejects only
  `subtotal < min_order`, so SAVE10 accepts exactly $50.00.
- **NEWUSER requires `customer_type == "new"`.** The rule says "first order";
  the starter code did not check it.
- **Invalid input raises `ValueError`.** This covers negative price, quantity,
  weight and distance, a non-integer quantity, and an unknown customer type. A
  zero quantity is allowed and adds nothing.
- **The validator collects all errors** in a fixed order and with fixed
  messages instead of stopping at the first one, so the JSON can compare exact
  lists.
- **Dates are injectable** (`today=` / `on_date=`), so expiration tests give the
  same result on any day.
- **The assignment's sample CSV row has shipping 5.50**, but its own rules give
  1.50 for 1 kg and 10 km. The data follows the rules; details are in
  `TEST_DATA_SPEC.md`.

## How the tests were checked

- The expected values in `order_calculations.csv` were calculated by hand and
  then checked with a separate script that uses `fractions` and does not use
  the project code. The script found 0 differences.
- Eight deliberate bugs were introduced into the code one at a time: an 8% → 9%
  tax rate, an express multiplier of 1.4, exclusive discount thresholds,
  banker's rounding, FREESHIP ignored, Luhn doubling the wrong digits, the
  expiration month off by one, and totals not being reset after a code changes.
  Each bug made at least one test fail.
- 2,000 Faker customers (20 seeds) were checked against the validator. This
  found that Faker's `state_abbr()` can return `PW` and `FM`, which are not US
  states; the generator now draws states from the validator's own list.
