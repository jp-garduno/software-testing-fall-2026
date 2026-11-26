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
        result = self.calc.add(5, 3)
        assert result == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = self.calc.add(-5, -3)
        assert result == -8

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        result = self.calc.add(10, -4)
        assert result == 6

    def test_add_zero(self):
        """Test that adding zero returns the same number."""
        result = self.calc.add(7, 0)
        assert result == 7

    def test_add_floats(self):
        """Test adding floating point numbers."""
        result = self.calc.add(0.1, 0.2)
        assert result == pytest.approx(0.3)

    def test_add_large_numbers(self):
        """Test adding very large integers."""
        result = self.calc.add(10**18, 10**18)
        assert result == 2 * 10**18

    # ---------- subtract ----------
    def test_subtract_positive_result(self):
        """Test subtraction that yields a positive result."""
        result = self.calc.subtract(10, 4)
        assert result == 6

    def test_subtract_negative_result(self):
        """Test subtraction that yields a negative result."""
        result = self.calc.subtract(4, 10)
        assert result == -6

    def test_subtract_same_numbers(self):
        """Test subtracting a number from itself gives zero."""
        result = self.calc.subtract(5, 5)
        assert result == 0

    def test_subtract_negative_numbers(self):
        """Test subtracting a negative number adds its magnitude."""
        result = self.calc.subtract(-3, -8)
        assert result == 5

    # ---------- multiply ----------
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        result = self.calc.multiply(6, 7)
        assert result == 42

    def test_multiply_by_zero(self):
        """Test that multiplying by zero gives zero."""
        result = self.calc.multiply(123, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        """Test that multiplying two negatives gives a positive."""
        result = self.calc.multiply(-4, -5)
        assert result == 20

    def test_multiply_mixed_signs(self):
        """Test that multiplying numbers of opposite sign gives a negative."""
        result = self.calc.multiply(-4, 5)
        assert result == -20

    def test_multiply_large_numbers(self):
        """Test multiplying large integers."""
        result = self.calc.multiply(10**10, 10**10)
        assert result == 10**20

    # ---------- divide ----------
    def test_divide_normal_case(self):
        """Test exact division of two positive numbers."""
        result = self.calc.divide(10, 2)
        assert result == 5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test that dividing two negatives gives a positive."""
        result = self.calc.divide(-10, -2)
        assert result == 5

    def test_divide_mixed_signs(self):
        """Test that dividing numbers of opposite sign gives a negative."""
        result = self.calc.divide(-10, 2)
        assert result == -5

    def test_divide_with_decimal_result(self):
        """Test division resulting in a decimal."""
        result = self.calc.divide(10, 3)
        assert result == pytest.approx(3.333333, rel=1e-5)

    def test_divide_zero_by_number(self):
        """Test that zero divided by a number is zero."""
        result = self.calc.divide(0, 5)
        assert result == 0

    # ---------- power ----------
    def test_power_positive_exponent(self):
        """Test raising to a positive exponent."""
        result = self.calc.power(2, 10)
        assert result == 1024

    def test_power_zero_exponent(self):
        """Test that any number to the power of zero is one."""
        result = self.calc.power(99, 0)
        assert result == 1

    def test_power_negative_exponent(self):
        """Test raising to a negative exponent gives a fraction."""
        result = self.calc.power(2, -2)
        assert result == pytest.approx(0.25)

    def test_power_negative_base_odd_exponent(self):
        """Test negative base with odd exponent stays negative."""
        result = self.calc.power(-3, 3)
        assert result == -27

    def test_power_fractional_exponent(self):
        """Test fractional exponent behaves as a root."""
        result = self.calc.power(9, 0.5)
        assert result == pytest.approx(3.0)

    # ---------- sqrt ----------
    def test_sqrt_positive_number(self):
        """Test square root of a perfect square."""
        result = self.calc.sqrt(16)
        assert result == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test that square root of zero is zero."""
        result = self.calc.sqrt(0)
        assert result == 0

    def test_sqrt_non_perfect_square(self):
        """Test square root of a non-perfect square."""
        result = self.calc.sqrt(2)
        assert result == pytest.approx(math.sqrt(2))

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            self.calc.sqrt(-1)

    # ---------- modulo ----------
    def test_modulo_normal_case(self):
        """Test remainder of a positive division."""
        result = self.calc.modulo(10, 3)
        assert result == 1

    def test_modulo_exact_division(self):
        """Test remainder is zero when division is exact."""
        result = self.calc.modulo(12, 4)
        assert result == 0

    def test_modulo_negative_dividend(self):
        """Test Python's modulo takes the sign of the divisor."""
        result = self.calc.modulo(-10, 3)
        assert result == 2

    def test_modulo_by_zero_raises_error(self):
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    # ---------- absolute ----------
    def test_absolute_positive_number(self):
        """Test absolute value of a positive number is unchanged."""
        result = self.calc.absolute(5)
        assert result == 5

    def test_absolute_negative_number(self):
        """Test absolute value of a negative number is positive."""
        result = self.calc.absolute(-5)
        assert result == 5

    def test_absolute_zero(self):
        """Test absolute value of zero is zero."""
        result = self.calc.absolute(0)
        assert result == 0

    def test_absolute_negative_float(self):
        """Test absolute value of a negative float."""
        result = self.calc.absolute(-2.5)
        assert result == pytest.approx(2.5)

    # ---------- factorial ----------
    def test_factorial_zero(self):
        """Test that 0! is 1."""
        result = self.calc.factorial(0)
        assert result == 1

    def test_factorial_one(self):
        """Test that 1! is 1."""
        result = self.calc.factorial(1)
        assert result == 1

    def test_factorial_positive_number(self):
        """Test factorial of a small positive integer."""
        result = self.calc.factorial(5)
        assert result == 120

    def test_factorial_large_number(self):
        """Test factorial of a larger integer matches math.factorial."""
        result = self.calc.factorial(20)
        assert result == math.factorial(20)

    def test_factorial_negative_raises_error(self):
        """Test that factorial of a negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Factorial not defined for negative numbers"
        ):
            self.calc.factorial(-3)

    def test_factorial_float_raises_error(self):
        """Test that factorial of a non-integer raises ValueError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(3.5)

    def test_factorial_string_raises_error(self):
        """Test that factorial of a string raises ValueError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial("5")

    # ---------- parametrize (advanced) ----------
    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 1, 2),
            (0, 0, 0),
            (-1, 1, 0),
            (100, 200, 300),
        ],
    )
    def test_add_parametrized(self, a, b, expected):
        """Test add with multiple input combinations."""
        assert self.calc.add(a, b) == expected
