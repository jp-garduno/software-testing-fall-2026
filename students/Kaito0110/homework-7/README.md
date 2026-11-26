# Homework 7: Data-Driven Test Suite — E-Commerce Order Processing

## Overview

This project implements a complete **E-Commerce Order Processing System** in Python along with a comprehensive **Data-Driven Testing (DDT)** suite powered by `pytest`, external **CSV** and **JSON** datasets, a pre-test data validator, and a `Faker`-based synthetic order generator.

## System Components (`src/`)

1. **`src/order_calculator.py` (`Order`)**:
   - Calculates item subtotals (`price × quantity`).
   - Validates and applies discount codes (`SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER`).
   - Computes 8% sales tax on `(subtotal - discount)`.
   - Computes weight-based (`$0.50/kg`) and distance-based (`$0.10/km`) shipping with a `1.5×` express multiplier and `FREESHIP` override.
2. **`src/customer_validator.py`**:
   - Validates email format, US phone number format `(XXX) XXX-XXXX`, billing address (`street`, `city`, 2-letter `state`, 5/9-digit `zip`), and credit card details (Luhn checksum algorithm, `MM/YYYY` expiration date, and 3–4 digit CVV).
3. **`src/order_workflow.py` (`OrderWorkflowEngine`)**:
   - Executes end-to-end multi-step order workflows (`validate_customer` → `create_order` → `calculate_total` → `process_payment`).
4. **`src/data_tools.py` (Bonus Options A & C)**:
   - **Bonus Option A (`generate_synthetic_orders_csv`)**: Generates 100 valid, realistic e-commerce orders using `Faker` into `test_data/generated_orders.csv`.
   - **Bonus Option C (`validate_order_csv_file`)**: Validates CSV schema, required columns, JSON item payloads, and numeric/boolean data types with exact line numbers before test execution.

## Project Structure

```text
homework-7/
├── src/
│   ├── __init__.py
│   ├── order_calculator.py
│   ├── customer_validator.py
│   ├── order_workflow.py
│   └── data_tools.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_order_calculator.py
│   ├── test_customer_validator.py
│   ├── test_order_traditional.py
│   ├── test_order_data_driven.py
│   └── test_integration.py
├── test_data/
│   ├── order_calculations.csv       (28 test cases)
│   ├── customer_validation.json     (32 test cases)
│   ├── order_workflows.json         (4 end-to-end workflows)
│   └── generated_orders.csv         (100 Faker-generated orders - Bonus A)
├── README.md
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── coverage_report.html
├── test_results.txt
├── pytest.ini
└── requirements.txt
```

## Setup and Installation

```bash
pip install -r requirements.txt
```

## Running the Test Suite

Run all tests:

```bash
python -m pytest -v
```

Run tests with statement and branch coverage:

```bash
python -m pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```
