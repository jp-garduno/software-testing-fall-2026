# Homework 7: Data-Driven Test Suite - E-Commerce Order Processing

## Description

An order processing system and a data-driven test suite for it. The system prices orders (discount codes, 8% tax,
weight- and distance-based shipping, express), validates customers (email, phone, address, credit card with the Luhn
check and expiry), and runs end-to-end order workflows. Every scenario is stored in external CSV, JSON or Excel files
in `test_data/`; the test code only loads them.

## Prerequisites

- Python 3.11+ (also verified on Python 3.9)
- `pytest`, `pytest-cov`, `openpyxl` (all in `requirements.txt`)

## Installation

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running Tests

```bash
pytest -v
pytest --cov=src --cov-branch --cov-report=term-missing
```

`pytest.ini` sets `pythonpath = . src`, so plain `pytest` works from this directory. Test data paths are resolved
relative to the test files, so the working directory does not matter.

To regenerate the single-file coverage report:

```bash
pytest --cov=src --cov-branch --cov-report=json
python tools/make_coverage_report.py   # writes coverage_report.html
```

## Results

- **Tests**: 305 passing, about 0.3 s, none skipped (`test_results.txt`)
- **Coverage**: 100% statements (384/384), 100% branches (132/132) (`coverage_report.html`)
- **pylint**: 10/10 with the course configuration

## Project Structure

| Path | Contents |
| ---- | -------- |
| `src/order_calculator.py` | `Order`: subtotal, discount codes, tax, shipping, total |
| `src/customer_validator.py` | Email, phone, address, credit card (Luhn, expiry, CVV) |
| `src/order_workflow.py` | `OrderWorkflow`: validate, create, price, pay, confirm |
| `src/data_validator.py` | Checks the data files and reports problems with line numbers |
| `tests/test_order_calculator.py` | 78 tests: the 38 CSV cases (values and a sum invariant for the 31 valid rows, a rejection check for the 7 error rows) + 9 behaviour tests |
| `tests/test_customer_validator.py` | 114 tests: the 48 JSON cases checked twice + Luhn/CVV/expiry unit tests |
| `tests/test_order_traditional.py` | 10 hard-coded order tests (Part 3) |
| `tests/test_order_data_driven.py` | The same 10 tests, data-driven (Part 3) |
| `tests/test_integration.py` | 14 tests: the 5 workflows from JSON + workflow rule tests |
| `tests/test_order_excel.py` | 42 tests: the order cases read from an Excel workbook + consistency checks (bonus D) |
| `tests/test_data_validation.py` | 37 tests: the data validator, on shipped and deliberately broken files (bonus C) |
| `tests/data_loader.py` | Loads CSV / JSON / XLSX into pytest parameters |
| `test_data/` | `order_calculations.csv` (38), `order_calculations.xlsx`, `customer_validation.json` (48), `order_workflows.json` (5), `comparison_orders.csv` (10) |
| `tools/` | `count_loc.py`, `csv_to_xlsx.py`, `make_coverage_report.py` |
| `TEST_DATA_SPEC.md` | Format of every data file, the business-rule decisions and where the assignment text is inconsistent |
| `COMPARISON_REPORT.md` | Traditional vs data-driven analysis with measured numbers |

## Bonus Features

- **Option C, data validation**: `src/data_validator.py` checks required fields, types, consistency, duplicate names,
  unknown workflow actions and the minimum case counts, and reports line numbers. It is tested on the real files (no
  problems) and on broken ones (every problem found, with the right line).
- **Option D, Excel**: `test_data/order_calculations.xlsx` has one sheet per test category and is loaded with
  `openpyxl`; a test checks it stays identical to the CSV. Regenerate it with `python tools/csv_to_xlsx.py`.

## Notes

- Expected values were calculated by hand, not generated from the code under test.
- Where the assignment text contradicts itself (the sample shipping value, the `>` vs inclusive minimum order, a sample
  card that is already expired) the decision is documented in `TEST_DATA_SPEC.md`.
- Python only; no JavaScript version.
