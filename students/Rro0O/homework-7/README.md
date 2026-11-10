# Homework 7: Data-Driven Test Suite — E-Commerce Order Processing

Student: Rogelio Sosa (Rro0O) · Module 7: Data-Driven Testing · Language: Python

A small order-processing system (order calculator, customer validator, workflow
engine) tested mostly from **external data files** (CSV and JSON). Test logic is
written once; scenarios live in `test_data/`.

## Layout

```
homework-7/
├── src/
│   ├── order_calculator.py    # Order: subtotal, discounts, tax, shipping, total
│   ├── customer_validator.py  # email, phone, address, Luhn card, expiration
│   ├── order_workflow.py      # step engine for end-to-end workflows
│   ├── data_generator.py      # Bonus A: Faker-based generator (100 orders)
│   └── data_validator.py      # Bonus C: validates data files, reports line numbers
├── tests/
│   ├── data_loader.py                 # CSV/JSON loading helpers
│   ├── test_order_calculator.py       # CSV-driven (32 cases) + edge-case unit tests
│   ├── test_customer_validator.py     # JSON-driven (32 cases) + helper tests
│   ├── test_order_traditional.py      # 10 tests, hard-coded data
│   ├── test_order_data_driven.py      # same 10 scenarios, data from CSV
│   ├── test_integration.py            # JSON workflows (7)
│   ├── test_data_generator.py         # Bonus A
│   └── test_data_validator.py         # Bonus C
├── test_data/
│   ├── order_calculations.csv         # 32 cases
│   ├── customer_validation.json       # 32 cases
│   ├── order_workflows.json           # 7 workflows
│   └── generated_orders.csv           # 100 generated regression orders (Bonus A)
├── README.md · COMPARISON_REPORT.md · TEST_DATA_SPEC.md
├── coverage_report.html · test_results.txt
└── requirements.txt · pytest.ini
```

## Setup and run

```bash
cd students/Rro0O/homework-7
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

pytest                                  # all tests
pytest --cov=src --cov-report=term-missing
pytest tests/test_order_data_driven.py -v

python src/data_validator.py            # validate test_data/ (prints file:line problems)
python src/data_generator.py            # regenerate test_data/generated_orders.csv
python scripts/make_reports.py          # rebuild test_results.txt + coverage_report.html
```

Python 3.9+ (CI uses 3.11). Test data paths are resolved relative to the test
files, so tests can be run from any directory.

## Business rules implemented

| Area     | Rule                                                                                      |
| -------- | ----------------------------------------------------------------------------------------- |
| Subtotal | Σ price × quantity                                                                        |
| Discount | `SAVE10` 10% if subtotal ≥ 50 · `SAVE20` 20% if ≥ 100 · `FREESHIP` free shipping · `NEWUSER` 15%, new customers only · anything else: no discount |
| Tax      | 8% of (subtotal − discount)                                                               |
| Shipping | Σ(weight × qty) × $0.50 + km × $0.10; express × 1.5; `FREESHIP` → 0                       |
| Total    | subtotal − discount + tax + shipping                                                      |

Design decisions (documented because the assignment text leaves them open):

- Minimum order thresholds are **inclusive** (a $50.00 order qualifies for `SAVE10`), matching the starter code (`subtotal < min_order` rejects).
- Money uses `Decimal`, rounded half-up to cents, so `19.99 × 3 × 8%` is `4.80`, never `4.79`.
- Negative price/quantity/weight/distance raise `ValueError`; zero quantity and empty orders are valid and cost nothing.
- The sample row in the assignment (`weight 1, 10 km → shipping 5.50`) contradicts the written rule ($0.10/km → $1.50). The **written rules** are implemented.
- Card expiration is valid through the last day of the expiration month. Tests inject a fixed reference date so they never expire.

## Results

See `test_results.txt` and `coverage_report.html` (281 tests, 99% coverage of `src/`).
Analysis: `COMPARISON_REPORT.md`. Data format: `TEST_DATA_SPEC.md`.

## Bonus features (A and C)

- **A – Data generation:** `src/data_generator.py` produces 100 reproducible orders with Faker (`seed=2026`) in `test_data/generated_orders.csv`; they run as a regression baseline.
- **C – Data validation:** `src/data_validator.py` checks headers, required fields, data types, item structure and internal consistency, reporting `file:line` for every problem; it also runs as part of the test suite.
