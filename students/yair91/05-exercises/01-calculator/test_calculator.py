"""Unit tests for the Calculator class.

Each test follows Arrange-Act-Assert and verifies one behaviour. A fresh
Calculator is created before every test so the suite can run in any order.
"""

import pytest

from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # ----- add -----------------------------------------------------------

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(-5, 3) == -2

    def test_add_with_zero_returns_other_operand(self):
        """Test that zero is the identity for addition."""
        assert self.calc.add(7, 0) == 7

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    # ----- subtract ------------------------------------------------------

    def test_subtract_positive_result(self):
        """Test a subtraction whose result is positive."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Test a subtraction whose result is negative."""
        assert self.calc.subtract(4, 10) == -6

    def test_subtract_equal_numbers_returns_zero(self):
        """Test that subtracting a number from itself returns zero."""
        assert self.calc.subtract(7, 7) == 0

    # ----- multiply ------------------------------------------------------

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert self.calc.multiply(6, 7) == 42

    def test_multiply_by_zero(self):
        """Test that multiplying by zero returns zero."""
        assert self.calc.multiply(99, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test that two negatives multiply to a positive."""
        assert self.calc.multiply(-6, -7) == 42

    def test_multiply_mixed_signs(self):
        """Test that one negative operand makes the result negative."""
        assert self.calc.multiply(-6, 7) == -42

    # ----- divide --------------------------------------------------------

    def test_divide_normal_case(self):
        """Test a division with an exact result."""
        assert self.calc.divide(10, 2) == 5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test dividing a negative by a positive."""
        assert self.calc.divide(-10, 2) == -5

    def test_divide_with_decimal_result(self):
        """Test a division that does not come out exact."""
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    # ----- power ---------------------------------------------------------

    def test_power_positive_exponent(self):
        """Test raising a number to a positive power."""
        assert self.calc.power(2, 10) == 1024

    def test_power_zero_exponent(self):
        """Test that any base to the power of zero is one."""
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test that a negative exponent produces the reciprocal."""
        assert self.calc.power(2, -2) == pytest.approx(0.25)

    def test_power_fractional_exponent(self):
        """Test that an exponent of 0.5 behaves like a square root."""
        assert self.calc.power(9, 0.5) == pytest.approx(3.0)

    # ----- sqrt ----------------------------------------------------------

    def test_sqrt_positive_number(self):
        """Test the square root of a perfect square."""
        assert self.calc.sqrt(16) == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test that the square root of zero is zero, the boundary value."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_non_perfect_square(self):
        """Test the square root of a number that is not a perfect square."""
        assert self.calc.sqrt(2) == pytest.approx(1.414213, rel=1e-5)

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.sqrt(-1)

    # ----- modulo --------------------------------------------------------

    def test_modulo_normal_case(self):
        """Test a remainder that is not zero."""
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_exact_division_returns_zero(self):
        """Test that an exact division leaves no remainder."""
        assert self.calc.modulo(10, 5) == 0

    def test_modulo_by_zero_raises_error(self):
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    def test_modulo_negative_dividend(self):
        """Test Python's sign convention: the result takes the divisor's sign."""
        assert self.calc.modulo(-10, 3) == 2

    # ----- absolute ------------------------------------------------------

    def test_absolute_positive_number(self):
        """Test that a positive number is returned unchanged."""
        assert self.calc.absolute(5) == 5

    def test_absolute_negative_number(self):
        """Test that a negative number loses its sign."""
        assert self.calc.absolute(-5) == 5

    def test_absolute_zero(self):
        """Test the boundary between positive and negative."""
        assert self.calc.absolute(0) == 0

    # ----- factorial -----------------------------------------------------

    def test_factorial_of_zero(self):
        """Test that 0! is 1 by definition."""
        assert self.calc.factorial(0) == 1

    def test_factorial_of_one(self):
        """Test that 1! is 1, the second early-return case."""
        assert self.calc.factorial(1) == 1

    def test_factorial_of_positive_number(self):
        """Test a factorial that goes through the loop."""
        assert self.calc.factorial(5) == 120

    def test_factorial_negative_raises_error(self):
        """Test that a negative input raises ValueError."""
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_non_integer_raises_error(self):
        """Test that a float raises ValueError before the sign is checked."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(3.5)

    def test_factorial_string_raises_error(self):
        """Test that a value of the wrong type raises ValueError, not TypeError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial("5")
