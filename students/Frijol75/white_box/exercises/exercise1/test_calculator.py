import math

import pytest
from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # ---------- add ----------
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(10, -4) == 6

    def test_add_zero(self):
        """Test that adding zero returns the same number."""
        assert self.calc.add(7, 0) == 7

    def test_add_large_numbers(self):
        """Test adding very large numbers."""
        assert self.calc.add(10**15, 10**15) == 2 * 10**15

    def test_add_floats(self):
        """Test adding floats using approx to avoid precision errors."""
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    # ---------- subtract ----------
    def test_subtract_positive_result(self):
        """Test subtraction that yields a positive result."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Test subtraction that yields a negative result."""
        assert self.calc.subtract(4, 10) == -6

    def test_subtract_zero_result(self):
        """Test subtracting a number from itself."""
        assert self.calc.subtract(5, 5) == 0

    def test_subtract_negative_numbers(self):
        """Test subtracting a negative number (double negative)."""
        assert self.calc.subtract(5, -3) == 8

    # ---------- multiply ----------
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert self.calc.multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        """Test that multiplying by zero returns zero."""
        assert self.calc.multiply(123, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test that two negatives give a positive."""
        assert self.calc.multiply(-4, -5) == 20

    def test_multiply_mixed_signs(self):
        """Test that a positive and a negative give a negative."""
        assert self.calc.multiply(4, -5) == -20

    def test_multiply_large_numbers(self):
        """Test multiplying very large numbers."""
        assert self.calc.multiply(10**10, 10**10) == 10**20

    # ---------- divide ----------
    def test_divide_normal_case(self):
        """Test a normal exact division."""
        assert self.calc.divide(10, 2) == 5

    def test_divide_with_decimal_result(self):
        """Test division resulting in decimal."""
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test division with negative numbers."""
        assert self.calc.divide(-10, -2) == 5
        assert self.calc.divide(-10, 2) == -5

    def test_divide_zero_by_number(self):
        """Test that zero divided by a number is zero."""
        assert self.calc.divide(0, 5) == 0

    # ---------- power ----------
    def test_power_positive_exponent(self):
        """Test raising to a positive exponent."""
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test that any number to the power of 0 is 1."""
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test a negative exponent gives the reciprocal."""
        assert self.calc.power(2, -2) == pytest.approx(0.25)

    def test_power_zero_base(self):
        """Test zero raised to a positive exponent."""
        assert self.calc.power(0, 5) == 0

    def test_power_negative_base(self):
        """Test a negative base with an odd and an even exponent."""
        assert self.calc.power(-2, 3) == -8
        assert self.calc.power(-2, 2) == 4

    # ---------- sqrt ----------
    def test_sqrt_positive_number(self):
        """Test square root of a positive number."""
        assert self.calc.sqrt(16) == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="negative number"):
            self.calc.sqrt(-4)

    def test_sqrt_non_perfect_square(self):
        """Test square root of a non-perfect square."""
        assert self.calc.sqrt(2) == pytest.approx(math.sqrt(2))

    def test_sqrt_large_number(self):
        """Test square root of a large number."""
        assert self.calc.sqrt(10**20) == pytest.approx(10**10)

    # ---------- modulo (challenge) ----------
    def test_modulo_normal_case(self):
        """Test a normal modulo operation."""
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_exact_division(self):
        """Test modulo when the division is exact."""
        assert self.calc.modulo(10, 5) == 0

    def test_modulo_by_zero_raises_error(self):
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    def test_modulo_negative_numbers(self):
        """Test modulo with negatives (Python takes the sign of the divisor)."""
        assert self.calc.modulo(-10, 3) == 2
        assert self.calc.modulo(10, -3) == -2

    # ---------- absolute (challenge) ----------
    def test_absolute_positive_number(self):
        """Test absolute value of a positive number."""
        assert self.calc.absolute(5) == 5

    def test_absolute_negative_number(self):
        """Test absolute value of a negative number."""
        assert self.calc.absolute(-5) == 5

    def test_absolute_zero(self):
        """Test absolute value of zero."""
        assert self.calc.absolute(0) == 0

    def test_absolute_float(self):
        """Test absolute value of a negative float."""
        assert self.calc.absolute(-2.5) == pytest.approx(2.5)

    # ---------- factorial (challenge) ----------
    def test_factorial_zero(self):
        """Test that 0! is 1."""
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        """Test that 1! is 1."""
        assert self.calc.factorial(1) == 1

    def test_factorial_positive_number(self):
        """Test a typical factorial."""
        assert self.calc.factorial(5) == 120

    def test_factorial_large_number(self):
        """Test a large factorial."""
        assert self.calc.factorial(20) == 2432902008176640000

    def test_factorial_negative_raises_error(self):
        """Test that negative input raises ValueError."""
        with pytest.raises(ValueError, match="negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_non_integer_raises_error(self):
        """Test that a non-integer input raises ValueError."""
        with pytest.raises(ValueError, match="requires an integer"):
            self.calc.factorial(3.5)

    def test_factorial_string_raises_error(self):
        """Test that a string input raises ValueError."""
        with pytest.raises(ValueError, match="requires an integer"):
            self.calc.factorial("5")
