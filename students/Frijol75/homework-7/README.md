# Homework 7: Data-Driven Test Suite

**Student**: Frijol75  
**Course**: Software Testing - Fall 2026  
**Assignment**: Homework 7 - Data-Driven Testing (E-Commerce Order Processing)

---

## 📋 Overview

This repository contains a comprehensive **Data-Driven Testing (DDT)** suite for an E-Commerce Order Processing System. The suite validates pricing calculations, customer profile verification, and multi-step order workflows by separating test logic from external datasets (CSV and JSON).

### Key Features
- **Order Calculation Engine** (`order_calculator.py`): Subtotals, promotional discounts (`SAVE10`, `SAVE20`, `FREESHIP`, `NEWUSER`), 8% sales tax, and multi-factor shipping (weight + distance + express multiplier).
- **Customer Verification Module** (`customer_validator.py`): Email regex, US phone format, US billing address verification, and credit card validation (Luhn algorithm, expiration dates, and CVV).
- **Extensive External Test Data**:
  - `test_data/order_calculations.csv`: 30 comprehensive test cases.
  - `test_data/customer_validation.json`: 35 customer validation scenarios.
  - `test_data/order_workflows.json`: 4 multi-step end-to-end integration workflows.
- **Traditional vs. Data-Driven Comparison**: Comparative analysis with metrics, lines of code, and performance benchmarks.
- **Bonus Features Implemented**:
  - **Option A (Data Generation)**: Programmatic generator creating 100 valid orders in CSV (`src/data_generator.py`).
  - **Option B (Performance Comparison)**: Benchmark measuring execution time between traditional and data-driven testing.
  - **Option C (Data Validation)**: Schema and integrity validator reporting line numbers and data defects (`src/data_validator.py`).

---

## 🗂️ Project Structure

```
homework-7/
├── .gitignore
├── requirements.txt
├── README.md
├── COMPARISON_REPORT.md
├── TEST_DATA_SPEC.md
├── coverage_report.html
├── test_results.txt
├── src/
│   ├── __init__.py
│   ├── order_calculator.py
│   ├── customer_validator.py
│   ├── data_generator.py        # Bonus Option A
│   └── data_validator.py        # Bonus Option C
├── tests/
│   ├── __init__.py
│   ├── test_order_calculator.py
│   ├── test_customer_validator.py
│   ├── test_order_traditional.py
│   ├── test_order_data_driven.py
│   ├── test_integration.py
│   └── test_bonus.py            # Bonus Option A, B, C tests
└── test_data/
    ├── order_calculations.csv   # 30 cases
    ├── customer_validation.json # 35 cases
    ├── order_workflows.json     # 4 workflows
    ├── comparison_10_cases.csv  # 10 comparison cases
    └── generated_orders.csv     # 100 generated orders (Bonus A)
```

---

## 🚀 Setup & Execution

### 1. Requirements & Dependencies
Install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Run All Tests
Execute all 117 tests:
```bash
pytest -v
```

### 3. Run with Test Coverage
Generate coverage summary in terminal and HTML report:
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### 4. Run Individual Test Suites
- **Order Calculator (CSV DDT)**:
  ```bash
  pytest tests/test_order_calculator.py -v
  ```
- **Customer Validator (JSON DDT)**:
  ```bash
  pytest tests/test_customer_validator.py -v
  ```
- **Traditional Tests**:
  ```bash
  pytest tests/test_order_traditional.py -v
  ```
- **Data-Driven Comparison**:
  ```bash
  pytest tests/test_order_data_driven.py -v
  ```
- **Integration Workflows**:
  ```bash
  pytest tests/test_integration.py -v
  ```
- **Bonus Features**:
  ```bash
  pytest tests/test_bonus.py -v -s
  ```

---

## 📊 Summary of Test Results & Coverage

- **Total Tests**: **118 passing tests** (100% pass rate).
- **Code Coverage**: **98% overall coverage** across `src/` modules.
- **Coverage Report**: Available in [`coverage_report.html`](./coverage_report.html) and [`test_results.txt`](./test_results.txt).
