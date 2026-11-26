# Homework 7: Data-Driven Test Suite — E-Commerce Order Processing

Comprehensive data-driven testing suite in Python (`pytest`) for an e-commerce order processing system covering order calculation, customer & payment validation (including Luhn credit card verification), traditional vs. data-driven comparison analysis, end-to-end workflow integration testing, and bonus features (synthetic test data generation + pre-test schema validation).

## Project Structure

```text
homework-7/
├── src/
│   ├── __init__.py
│   ├── order_calculator.py       # Part 1: Order totals, discounts, tax (8%), and shipping
│   ├── customer_validator.py     # Part 2 & 4: Customer/card validation + E2E workflow engine
│   └── data_validator.py         # Bonus (Options A & C): CSV/JSON validator + 100-order generator
├── tests/
│   ├── __init__.py
│   ├── test_order_calculator.py  # Parameterized CSV tests for Order (30 CSV cases + edge cases)
│   ├── test_customer_validator.py# Parameterized JSON tests for customer validation (34 JSON cases + unit tests)
│   ├── test_order_traditional.py # Part 3: 10 hardcoded non-parameterized tests
│   ├── test_order_data_driven.py # Part 3: Same 10 tests parameterized from CSV
│   ├── test_integration.py       # Part 4: Parameterized end-to-end order workflows
│   └── test_bonus_features.py    # Bonus tests for 100 generated orders & schema validator
├── test_data/
│   ├── order_calculations.csv    # 30 order test cases across 5 categories
│   ├── customer_validation.json  # 34 customer validation test cases across 6 categories
│   ├── order_workflows.json      # 4 complete multi-step order workflows
│   └── generated_orders.csv      # 100 programmatically generated regression test cases
├── README.md                     # Setup and execution instructions
├── COMPARISON_REPORT.md          # Traditional vs. Data-Driven quantitative and qualitative analysis
├── TEST_DATA_SPEC.md             # External test data format and schema specification
├── coverage_report.html          # HTML coverage report (100% coverage)
├── test_results.txt              # Test execution log showing all tests passing
└── requirements.txt              # Python dependencies
```

## Setup Instructions

1. **Create and activate a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Test Suite

Run all tests from the `homework-7` directory:

```bash
PYTHONPATH=src pytest -v
```

Run with coverage report generation:

```bash
PYTHONPATH=src pytest -v --cov=src --cov-report=term-missing --cov-report=html
```

## Summary of Test Suites & Coverage

| Test Suite | Data Source | Test Cases | Purpose |
| :--- | :--- | :---: | :--- |
| `test_order_calculator.py` | `test_data/order_calculations.csv` | 31 | Validates subtotal, discount rules (`SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER`), 8% tax, and standard/express shipping |
| `test_customer_validator.py` | `test_data/customer_validation.json` | 40 | Validates email, US phone `(XXX) XXX-XXXX`, billing address, Luhn credit card checksum, expiration, and CVV |
| `test_order_traditional.py` | Hardcoded in Python | 10 | Baseline traditional test suite with 10 individual test functions |
| `test_order_data_driven.py` | `test_data/order_calculations.csv` | 10 | Data-driven equivalent of the 10 baseline scenarios |
| `test_integration.py` | `test_data/order_workflows.json` | 5 | End-to-end workflows (`validate_customer` -> `create_order` -> `calculate_total` -> `process_payment`) |
| `test_bonus_features.py` | `test_data/generated_orders.csv` | 6 | Regression over 100 generated orders (Option A) and CSV/JSON schema validation with line-number error reporting (Option C) |
| **Total** | | **102** | **100% Statement Coverage across `src/`** |
