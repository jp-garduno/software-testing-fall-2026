"""Unit tests for the Calculator exercise."""

import pytest

from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Add two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Add two negative numbers."""
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        """Add a positive number and a negative number."""
        assert self.calc.add(5, -8) == -3

    def test_subtract_positive_result(self):
        """Subtract to get a positive result."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Subtract to get a negative result."""
        assert self.calc.subtract(4, 10) == -6

    def test_multiply_positive_numbers(self):
        """Multiply two positive numbers."""
        assert self.calc.multiply(6, 7) == 42

    def test_multiply_by_zero(self):
        """Multiplying by zero returns zero."""
        assert self.calc.multiply(99, 0) == 0

    def test_multiply_negative_numbers(self):
        """Multiply two negative numbers."""
        assert self.calc.multiply(-4, -3) == 12

    def test_divide_normal_case(self):
        """Divide two non-zero values."""
        assert self.calc.divide(15, 4) == pytest.approx(3.75)

    def test_divide_by_zero_raises_error(self):
        """Dividing by zero raises the documented error."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Division preserves the expected sign."""
        assert self.calc.divide(-12, 3) == -4

    def test_power_positive_exponent(self):
        """Calculate a positive exponent."""
        assert self.calc.power(2, 5) == 32

    def test_power_zero_exponent(self):
        """Every non-zero base to exponent zero is one."""
        assert self.calc.power(7, 0) == 1

    def test_power_negative_exponent(self):
        """Calculate a negative exponent."""
        assert self.calc.power(2, -3) == pytest.approx(0.125)

    def test_sqrt_positive_number(self):
        """Calculate the square root of a positive number."""
        assert self.calc.sqrt(81) == 9

    def test_sqrt_zero(self):
        """The square root of zero is zero."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        """Negative square roots raise the documented error."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.sqrt(-1)
