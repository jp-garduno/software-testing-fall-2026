# Homework 7: Data-Driven Test Suite

**Student**: Carlos Rubio  
**Project**: E-Commerce Order Processing System  
**Language**: Python  

## Overview
This repository contains a comprehensive, data-driven test suite for an e-commerce order processing system. The project strictly separates the testing logic from the test data by utilizing external CSV and JSON files, allowing for massive scalability and ease of maintenance.

The suite validates customer information, calculates order totals (including complex tax, discount, and shipping rules), and executes complete end-to-end purchasing workflows.

## Setup Instructions

1. **Install dependencies**:
   Run the following command in your terminal to install pytest and its coverage plugin:

       py -m pip install -r requirements.txt

2. **Execute all tests**:
   To run the entire test suite (including unit tests, data-driven comparisons, and integration workflows), run:

       py -m pytest -v

3. **Generate coverage report**:
   To verify that the system meets the >80% coverage requirement, execute:

       py -m pytest --cov=src --cov-report=html:coverage_report.html

   *You can view the detailed line-by-line coverage by opening the `coverage_report.html` file in your browser.*

## Project Structure
* `src/`: Core implementation modules (`order_calculator.py`, `customer_validator.py`).
* `tests/`: Automated test scripts built with `pytest.mark.parametrize`.
* `test_data/`: External test data sources containing over 65 independent test cases across CSV and JSON formats.
* `COMPARISON_REPORT.md`: An analytical comparison highlighting the benefits of Data-Driven Testing vs Traditional Testing.
* `TEST_DATA_SPEC.md`: Schema documentation for the external data files.