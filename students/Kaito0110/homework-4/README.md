# Homework 4 - Black Box Testing Suite: SecureBank Online Banking

**Student**: Kaito0110
**Module**: 4 - Black Box Testing
**Language**: Python (pytest)

---

## Description

This project implements a comprehensive black-box test suite for **SecureBank**, a simulated online banking system. All four black-box testing techniques are applied systematically:

1. **Equivalence Partitioning (EP)** — 16 test cases
2. **Boundary Value Analysis (BVA)** — 19 test cases
3. **Decision Tables (DT)** — 13 test cases
4. **State Transition Testing (ST)** — 12+ test cases

**Total: 30+ automated test cases (exceeds the required 20)**

---

## Project Structure

```text
homework-4/
├── src/
│   └── banking.py          # System Under Test (SecureBank implementation)
├── tests/
│   └── test_banking.py     # Complete black-box test suite
├── docs/
│   ├── test-design.md      # Test design documentation
│   ├── execution-report.md # Test execution report
│   └── analysis-report.md  # Comparative analysis of techniques
├── .pylintrc               # Pylint configuration
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Tests

From the repository root:

```bash
# Run all tests
pytest students/Kaito0110/homework-4/tests/test_banking.py -v

# Run with coverage report
pytest students/Kaito0110/homework-4/tests/test_banking.py -v --cov=students/Kaito0110/homework-4/src --cov-report=term-missing
```

---

## System Under Test: SecureBank

### Account Types

| Type     | Min Balance | Monthly Fee | Fee Waiver Threshold | Daily Transfer Limit |
| -------- | ----------- | ----------- | -------------------- | -------------------- |
| Savings  | \$100       | \$5         | \$1,000              | \$2,000              |
| Checking | \$0         | \$10        | \$5,000              | \$5,000              |
| Premium  | \$10,000    | \$0         | N/A                  | \$50,000             |

### Account States

- **Active**: Full access to all operations
- **Frozen**: Read-only; no transactions allowed
- **Suspended**: Below minimum balance; restricted
- **Closed**: Permanently terminated; no operations

---

## Test Techniques Summary

### Equivalence Partitioning

Groups inputs into classes where all members are expected to behave identically. Covers transfer amount, account type, balance, payee, and date range.

### Boundary Value Analysis

Tests values at and around boundaries: minimum transfer ($0.00, $0.01), daily limits ($4,999.99, $5,000.00, $5,000.01), minimum balance thresholds, and fee waiver thresholds.

### Decision Tables

Covers combinations of conditions for transfer validation (8 rules), monthly fee processing (5 rules), and bill payment validation (4 rules).

### State Transition Testing

Validates all valid state transitions: Active↔Frozen, Active→Suspended, Suspended→Active, and all states→Closed. Verifies invalid transitions are rejected.
