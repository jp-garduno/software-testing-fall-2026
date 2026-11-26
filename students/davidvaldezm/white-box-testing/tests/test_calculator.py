"""Unit tests for the Calculator exercise."""

import pytest

from calculator import Calculator


class TestCalculator:
    """Test each Calculator operation independently."""

    def setup_method(self):
        """Create a new calculator for every test."""
        self.calculator = Calculator()

    def test_add_positive_numbers(self):
        assert self.calculator.add(5, 3) == 8

    def test_add_negative_numbers(self):
        assert self.calculator.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        assert self.calculator.add(5, -8) == -3

    def test_subtract_positive_result(self):
        assert self.calculator.subtract(8, 3) == 5

    def test_subtract_negative_result(self):
        assert self.calculator.subtract(3, 8) == -5

    def test_multiply_positive_numbers(self):
        assert self.calculator.multiply(4, 6) == 24

    def test_multiply_by_zero(self):
        assert self.calculator.multiply(12, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calculator.multiply(-4, 6) == -24

    def test_divide_normal_case(self):
        assert self.calculator.divide(10, 4) == pytest.approx(2.5)

    def test_divide_negative_numbers(self):
        assert self.calculator.divide(-12, 3) == pytest.approx(-4)

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calculator.divide(10, 0)

    def test_power_positive_exponent(self):
        assert self.calculator.power(2, 3) == 8

    def test_power_zero_exponent(self):
        assert self.calculator.power(7, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calculator.power(2, -2) == pytest.approx(0.25)

    def test_sqrt_positive_number(self):
        assert self.calculator.sqrt(16) == pytest.approx(4)

    def test_sqrt_zero(self):
        assert self.calculator.sqrt(0) == pytest.approx(0)

    def test_sqrt_negative_raises_error(self):
        with pytest.raises(ValueError, match="Cannot calculate square root"):
            self.calculator.sqrt(-1)

