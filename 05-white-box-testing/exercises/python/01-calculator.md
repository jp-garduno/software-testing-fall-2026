# Exercise 1: Calculator Unit Tests

**Duration**: 45-60 minutes  
**Difficulty**: Beginner  
**Topics**: Unit testing, pytest, edge cases, statement coverage

## Objectives

By completing this exercise, you will:

- Write unit tests for individual methods using pytest
- Test edge cases and error conditions
- Measure statement coverage with pytest-cov
- Understand the basics of test-driven development

## Background

Unit testing is the foundation of white box testing. In this exercise, you'll implement a `Calculator` class and write comprehensive unit tests that verify each method works correctly, including edge cases that might cause errors.

## Part 1: Implementation (15 minutes)

Create a file named `calculator.py` with the following starter code:

```python
import math

class Calculator:
    """A simple calculator with basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide a by b. Raises ValueError if b is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        return base ** exponent

    def sqrt(self, x):
        """Calculate square root. Raises ValueError if x is negative."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)
```

## Part 2: Write Unit Tests (25 minutes)

Create a file named `test_calculator.py` and write comprehensive tests:

```python
import pytest
from calculator import Calculator

class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # TODO: Write tests for add method
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        pass  # Replace with your implementation

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        pass

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        pass

    # TODO: Write tests for subtract method
    def test_subtract_positive_result(self):
        pass

    def test_subtract_negative_result(self):
        pass

    # TODO: Write tests for multiply method
    def test_multiply_positive_numbers(self):
        pass

    def test_multiply_by_zero(self):
        pass

    def test_multiply_negative_numbers(self):
        pass

    # TODO: Write tests for divide method
    def test_divide_normal_case(self):
        pass

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        pass  # Hint: Use pytest.raises(ValueError)

    def test_divide_negative_numbers(self):
        pass

    # TODO: Write tests for power method
    def test_power_positive_exponent(self):
        pass

    def test_power_zero_exponent(self):
        pass

    def test_power_negative_exponent(self):
        pass

    # TODO: Write tests for sqrt method
    def test_sqrt_positive_number(self):
        pass

    def test_sqrt_zero(self):
        pass

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        pass  # Hint: Use pytest.raises(ValueError)
```

### Your Tasks

1. **Implement all test methods** - Replace `pass` with actual test code
2. **Test normal cases** - Verify methods work with typical inputs
3. **Test edge cases** - Zero, negative numbers, large numbers
4. **Test error conditions** - Use `pytest.raises()` for expected exceptions

### Example Test Implementation

```python
def test_add_positive_numbers(self):
    """Test adding two positive numbers."""
    result = self.calc.add(5, 3)
    assert result == 8

def test_divide_by_zero_raises_error(self):
    """Test that dividing by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        self.calc.divide(10, 0)
```

## Part 3: Run Tests and Measure Coverage (10 minutes)

### Run Your Tests

```bash
# Run all tests
pytest test_calculator.py -v

# Run a specific test
pytest test_calculator.py::TestCalculator::test_add_positive_numbers -v
```

### Measure Statement Coverage

```bash
# Run tests with coverage
pytest --cov=calculator --cov-report=term-missing test_calculator.py

# Generate HTML coverage report
pytest --cov=calculator --cov-report=html test_calculator.py
# Open htmlcov/index.html in your browser
```

### Understanding Coverage Output

```
---------- coverage: platform win32, python 3.x -----------
Name            Stmts   Miss  Cover   Missing
---------------------------------------------
calculator.py      15      0   100%
---------------------------------------------
TOTAL              15      0   100%
```

- **Stmts**: Total number of statements
- **Miss**: Number of statements not executed
- **Cover**: Percentage of statements covered
- **Missing**: Line numbers not covered

## Part 4: Additional Challenges (10 minutes)

Add these methods to your `Calculator` class and write tests for them:

```python
def modulo(self, a, b):
    """Return remainder of a divided by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a % b

def absolute(self, x):
    """Return absolute value of x."""
    return abs(x)

def factorial(self, n):
    """Calculate factorial of n. Raises ValueError if n is negative or not an integer."""
    if not isinstance(n, int):
        raise ValueError("Factorial requires an integer")
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```

## Evaluation Criteria

Your solution will be evaluated on:

- **Test Coverage**: 100% statement coverage achieved
- **Edge Cases**: All edge cases tested (zero, negative, large numbers)
- **Error Handling**: Exceptions properly tested with pytest.raises()
- **Test Quality**: Tests are clear, well-named, and independent
- **Code Organization**: Tests are properly grouped and documented

## Common Mistakes to Avoid

1. **Not testing edge cases** - Always test zero, negative numbers, and boundaries
2. **Testing multiple things in one test** - Each test should verify one specific behavior
3. **Not using pytest.raises() correctly** - Must use context manager for exception testing
4. **Forgetting to assert** - Every test needs an assertion
5. **Not using setup_method** - Create fresh instances for test isolation
6. **Magic numbers** - Use meaningful test values that make the test clear

## Tips for Success

- Write test method names that describe what they test
- Use the Arrange-Act-Assert pattern in each test
- Run tests frequently as you write them
- Check coverage after each new test to see what's still missing
- Use parametrize for testing multiple similar cases (advanced)

## Example: Using pytest.approx for Floating Point

When testing floating point results, use `pytest.approx()`:

```python
def test_sqrt_positive_number(self):
    """Test square root of a positive number."""
    result = self.calc.sqrt(16)
    assert result == pytest.approx(4.0)

def test_divide_with_decimal_result(self):
    """Test division resulting in decimal."""
    result = self.calc.divide(10, 3)
    assert result == pytest.approx(3.333333, rel=1e-5)
```

## Submission

Submit the following files:

- `calculator.py` - Your Calculator implementation (with additional methods)
- `test_calculator.py` - Your complete test suite
- Screenshot of coverage report showing 100% coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 2: Shopping Cart](./02-shopping-cart.md) for class testing
- Review [Module Theory: Statement Coverage](../theory/02-statement-coverage.md)
- Learn about branch coverage and why statement coverage alone isn't enough
