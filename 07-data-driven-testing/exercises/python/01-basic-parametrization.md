# Exercise 1: Basic Parametrization (Python)

## Objective

Learn to write parameterized tests using `pytest.mark.parametrize`.

## Part 1: Simple Parameterization

### Task

Create a calculator module and test it with multiple inputs using parametrization.

### Implementation

**calculator.py**:

```python
def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract b from a"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide a by b"""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**test_calculator.py**:

```python
import pytest
from calculator import add, subtract, multiply, divide

# TODO: Implement parameterized tests

@pytest.mark.parametrize("a,b,expected", [
    # Add your test cases here
])
def test_add(a, b, expected):
    pass  # Implement

@pytest.mark.parametrize("a,b,expected", [
    # Add your test cases here
])
def test_subtract(a, b, expected):
    pass  # Implement

@pytest.mark.parametrize("a,b,expected", [
    # Add your test cases here
])
def test_multiply(a, b, expected):
    pass  # Implement

@pytest.mark.parametrize("a,b,expected", [
    # Add your test cases here
])
def test_divide(a, b, expected):
    pass  # Implement

@pytest.mark.parametrize("a,b", [
    # Add test cases that should raise ValueError
])
def test_divide_by_zero(a, b):
    pass  # Implement with pytest.raises
```

### Requirements

1. Test `add()` with at least 5 different inputs:

   - Positive numbers
   - Negative numbers
   - Zero
   - Decimal numbers

2. Test `subtract()` with at least 5 different inputs

3. Test `multiply()` with at least 5 different inputs including edge cases

4. Test `divide()` with at least 5 different inputs

5. Test `divide()` raises `ValueError` for division by zero (at least 3 cases)

6. Use descriptive test IDs for better readability

### Example

```python
@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (1.5, 2.5, 4.0),
    (-5, -3, -8),
], ids=["positive", "negative_positive", "zeros", "decimals", "both_negative"])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

## Part 2: String Operations

### Task

Create parameterized tests for string operations.

**string_ops.py**:

```python
def reverse_string(s):
    """Reverse a string"""
    return s[::-1]

def is_palindrome(s):
    """Check if string is palindrome (case-insensitive)"""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def count_vowels(s):
    """Count vowels in a string"""
    vowels = "aeiouAEIOU"
    return sum(1 for char in s if char in vowels)

def capitalize_words(s):
    """Capitalize first letter of each word"""
    return ' '.join(word.capitalize() for word in s.split())
```

**test_string_ops.py**:

```python
import pytest
from string_ops import reverse_string, is_palindrome, count_vowels, capitalize_words

# TODO: Implement parameterized tests for all functions
```

### Requirements

1. Test `reverse_string()` with at least 5 cases:

   - Regular string
   - Empty string
   - Single character
   - String with spaces
   - String with special characters

2. Test `is_palindrome()` with at least 7 cases:

   - True palindromes
   - False cases
   - Case-insensitive palindromes
   - Palindromes with spaces

3. Test `count_vowels()` with at least 6 cases

4. Test `capitalize_words()` with at least 5 cases

## Part 3: Multiple Parameters

### Task

Test a function that calculates shipping cost based on multiple factors.

**shipping.py**:

```python
def calculate_shipping(weight, distance, is_express):
    """
    Calculate shipping cost

    Args:
        weight: Package weight in kg
        distance: Distance in km
        is_express: Boolean for express shipping

    Returns:
        Shipping cost in dollars
    """
    if weight <= 0 or distance <= 0:
        raise ValueError("Weight and distance must be positive")

    base_cost = weight * 0.5 + distance * 0.1

    if is_express:
        base_cost *= 1.5

    return round(base_cost, 2)
```

**test_shipping.py**:

```python
import pytest
from shipping import calculate_shipping

# TODO: Create comprehensive parameterized tests
```

### Requirements

1. Test valid inputs with at least 8 combinations of:

   - Different weights (light, medium, heavy)
   - Different distances (short, medium, long)
   - Express and standard shipping

2. Test invalid inputs (negative weight/distance)

3. Use meaningful test IDs

## Expected Output

```bash
$ pytest test_calculator.py -v

test_calculator.py::test_add[positive] PASSED
test_calculator.py::test_add[negative_positive] PASSED
test_calculator.py::test_add[zeros] PASSED
test_calculator.py::test_add[decimals] PASSED
test_calculator.py::test_add[both_negative] PASSED
test_calculator.py::test_subtract[...] PASSED
...
test_calculator.py::test_divide_by_zero[...] PASSED

==================== 30+ passed in 0.05s ====================
```

## Hints

1. Use `pytest.raises()` for exception testing:

   ```python
   with pytest.raises(ValueError):
       divide(10, 0)
   ```

2. Use `ids` parameter for readable test names:

   ```python
   @pytest.mark.parametrize("input,expected", [...], ids=["case1", "case2"])
   ```

3. You can use `pytest.approx()` for floating-point comparisons:
   ```python
   assert result == pytest.approx(expected, rel=1e-9)
   ```

## Submission

Submit the following files:

- `calculator.py` and `test_calculator.py`
- `string_ops.py` and `test_string_ops.py`
- `shipping.py` and `test_shipping.py`
- Screenshot of test results showing all tests passing

## Grading Criteria

- Correct implementation: 40%
- Comprehensive test coverage: 30%
- Use of parameterization: 20%
- Code quality and naming: 10%
