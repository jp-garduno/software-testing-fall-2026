# White-box testing: exercises 1 and 2

**Student:** David Valdez (`davidvaldezm`)  
**Language:** Python 3.11+ with pytest

This submission implements the first two Python exercises in the White Box
Testing module:

1. `Calculator`: unit tests for arithmetic operations and error paths.
2. `ShoppingCart`: stateful class tests for item management, discounts, and
   collection edge cases.

## Setup and execution

From this directory, create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run the suite and generate statement and branch coverage:

```powershell
python -m pytest -v --cov=src --cov-branch --cov-report=term-missing --cov-report=html
```

The HTML report is generated at `htmlcov/index.html`. Both exercises are
expected to reach 100% statement and branch coverage.

## Project layout

```text
src/
  calculator.py       # Exercise 1 implementation
  shopping_cart.py    # Exercise 2 implementation
tests/
  test_calculator.py
  test_shopping_cart.py
```

The tests use fresh objects per case, assert error messages where meaningful,
and cover normal, boundary, and invalid-input paths.

