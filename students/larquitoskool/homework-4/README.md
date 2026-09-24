# Homework 4: Black Box Testing - SecureBank System

## Description
Comprehensive black box test suite for an online banking system using EP, BVA, decision tables, and state transition testing.

## Prerequisites
- Python 3.11+
- pytest and pytest-cov

## Installation
```bash
pip install -r requirements.txt
```

## Running Tests
To run all tests:
```bash
python3 -m pytest tests/ -v
```

To run tests with coverage report:
```bash
python3 -m pytest tests/ -v --cov=src --cov-report=html --cov-report=term
```
*Note: The HTML coverage report can be viewed by opening `htmlcov/index.html` in your browser.*

## Project Structure
- `design/` - Test design documentation
- `src/` - Banking system implementation
- `tests/` - Automated test suite
- `reports/` - Test execution and analysis reports
- `reports/screenshots/` - Execution and coverage screenshots

## Test Coverage
- Equivalence Partitioning: 5 tests
- Boundary Value Analysis: 6 tests
- Decision Tables: 5 tests
- State Transitions: 4 tests
- **Total**: 20 tests

## Author
Carlos Rubio