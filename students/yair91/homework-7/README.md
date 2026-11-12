# Homework 7: Data-Driven Test Suite

A data-driven suite for an e-commerce order processing system. The test data
lives in CSV and JSON files, outside the test code.

**Author**: Emmanuel Arias (`yair91`) · Module 7 · Fall 2026

## Results

```
257 passed
Coverage of src/   100 % (306/306 statements)
Pylint             10.00/10
```

| Part | Deliverable | Cases |
| --- | --- | --- |
| 1 · Order Calculator | `src/order_calculator.py` + `test_data/order_calculations.csv` | 35 rows (minimum 25) |
| 2 · Customer Validation | `src/customer_validator.py` + `test_data/customer_validation.json` | 39 cases (minimum 30) |
| 3 · Comparison Analysis | `tests/test_order_traditional.py` and `tests/test_order_data_driven.py` | 10 scenarios in both forms |
| 4 · Integration | `test_data/order_workflows.json` | 5 workflows (minimum 3) |
| Bonus A | `src/data_generator.py` | 100 regression orders |
| Bonus C | `src/data_validator.py` | Validation of the data files |

## Prerequisites

- Python 3.9 or newer. The code avoids syntax newer than 3.9, so it also runs
  on the 3.11 the course targets.
- The packages in `requirements.txt`.

## Installation

```bash
cd students/yair91/homework-7
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest -v
```

With coverage:

```bash
pytest --cov=src --cov-report=term-missing
```

A browsable HTML report, file by file:

```bash
pytest --cov=src --cov-report=html
open htmlcov/index.html          # Linux: xdg-open
```

The coverage summary submitted with the homework is in
[`coverage_report.html`](coverage_report.html), and the full output of the run
is in [`test_results.txt`](test_results.txt).

One suite at a time:

```bash
pytest tests/test_order_calculator.py -v      # Part 1
pytest tests/test_customer_validator.py -v    # Part 2
pytest tests/test_order_traditional.py -v     # Part 3, traditional version
pytest tests/test_order_data_driven.py -v     # Part 3, data-driven version
pytest tests/test_integration.py -v           # Part 4
pytest tests/test_data_validator.py -v        # Bonus C
pytest tests/test_data_generator.py -v        # Bonus A
```

Linting with the same configuration the grading workflow uses:

```bash
pylint --rcfile=../../../.github/grading/pylintrc src tests
```

## Structure

```
homework-7/
├── src/
│   ├── order_calculator.py      Part 1: subtotal, discount, tax, shipping
│   ├── customer_validator.py    Part 2: email, phone, address, Luhn, expiry
│   ├── data_generator.py        Bonus A: 100 reproducible regression orders
│   └── data_validator.py        Bonus C: checks the data files
├── tests/
│   ├── conftest.py              paths and loading of the data files
│   ├── test_order_calculator.py
│   ├── test_customer_validator.py
│   ├── test_order_traditional.py
│   ├── test_order_data_driven.py
│   ├── test_integration.py
│   ├── test_data_generator.py
│   └── test_data_validator.py
├── test_data/
│   ├── order_calculations.csv   35 rows
│   ├── customer_validation.json 39 cases
│   ├── order_workflows.json     5 workflows
│   └── generated_orders.csv     100 generated orders
├── README.md
├── COMPARISON_REPORT.md         Part 3: traditional versus data-driven
├── TEST_DATA_SPEC.md            format of each data file
├── coverage_report.html
├── test_results.txt
├── pytest.ini
└── requirements.txt
```

The format of every data file is documented in
[`TEST_DATA_SPEC.md`](TEST_DATA_SPEC.md), and the Part 3 comparison with its
measured numbers is in [`COMPARISON_REPORT.md`](COMPARISON_REPORT.md).

## Decisions the brief leaves open

**`NEWUSER` only applies to new customers.** The rule says "15% off first
order", but the starter code in the brief does not check the customer type, so
it would accept the code for anyone. Here a `regular` customer attempting
`NEWUSER` gets `False` and no discount.

**Shipping adds weight and distance.** `weight × 0.50 + distance × 0.10`, and
express multiplies that total by 1.5. The brief lists both rules without
saying whether they add up or one replaces the other.

**Tax does not apply to shipping.** It is 8 % of (subtotal − discount), exactly
as written, so shipping is added after the tax is computed.

**Zero quantity is valid; negatives are not.** The brief asks for edge cases
with "zero quantity, negative values" without saying what should happen. Here
an article with quantity zero is legitimate and contributes 0 to the subtotal,
while a negative price, weight, quantity or distance raises `ValueError` with a
specific message. The rows with `expected_error` in the CSV cover those cases.

**Expiry is compared against a fixed date.** `customer_validator.py` uses
November 2026 as its reference instead of `datetime.now()`. With a real clock a
`12/26` card would be valid today and stop being valid next year, and the suite
would start failing on its own without anyone touching it.

## About the data and why its origin matters

The amounts in `order_calculations.csv` were **not** generated by calling the
calculator. They were computed with a formula written separately, from the text
of the brief, and then cross-checked against the implementation: 0 deviations
across the 35 rows. The same goes for the expected errors in
`customer_validation.json`, written by hand and cross-checked afterwards.

If the expected values came from the code under test, the tests would prove
nothing: they would only confirm the code agrees with itself.

The one exception is `generated_orders.csv`, which does come from the
calculator and is labelled as a regression set. It detects that something
changed; it does not prove that something is right.

## About bonus A and Faker

The brief suggests Faker for generating data. It is not used here: the grading
workflow installs only the `requirements.txt` at the root of the repository,
where Faker does not appear, so a test that imported it would fail during
grading.

The generator uses `random` with a fixed seed, from the standard library. That
gives something Faker does not give out of the box: the same seed always
produces the same file, and a regression set that changes on every run is no
use for catching regressions.

```bash
PYTHONPATH=src python src/data_generator.py
md5 test_data/generated_orders.csv     # the same hash on every run
```
