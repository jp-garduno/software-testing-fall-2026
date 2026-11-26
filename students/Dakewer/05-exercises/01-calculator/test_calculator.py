import pytest
from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # ---------- add ----------
    def test_add_positive_numbers(self):
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        assert self.calc.add(-5, 8) == 3

    def test_add_floats(self):
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    # ---------- subtract ----------
    def test_subtract_positive_result(self):
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert self.calc.subtract(4, 10) == -6

    # ---------- multiply ----------
    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(6, 7) == 42

    def test_multiply_by_zero(self):
        assert self.calc.multiply(123, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-4, -5) == 20

    def test_multiply_large_numbers(self):
        assert self.calc.multiply(10**6, 10**6) == 10**12

    # ---------- divide ----------
    def test_divide_normal_case(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_with_decimal_result(self):
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        assert self.calc.divide(-10, -2) == 5

    def test_divide_zero_by_number(self):
        assert self.calc.divide(0, 5) == 0

    # ---------- power ----------
    def test_power_positive_exponent(self):
        assert self.calc.power(2, 10) == 1024

    def test_power_zero_exponent(self):
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -2) == pytest.approx(0.25)

    # ---------- sqrt ----------
    def test_sqrt_positive_number(self):
        assert self.calc.sqrt(16) == pytest.approx(4.0)

    def test_sqrt_zero(self):
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        with pytest.raises(ValueError, match="square root of negative"):
            self.calc.sqrt(-4)

    # ---------- modulo ----------
    def test_modulo_normal_case(self):
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_exact_division(self):
        assert self.calc.modulo(10, 5) == 0

    def test_modulo_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    # ---------- absolute ----------
    def test_absolute_positive(self):
        assert self.calc.absolute(5) == 5

    def test_absolute_negative(self):
        assert self.calc.absolute(-5) == 5

    def test_absolute_zero(self):
        assert self.calc.absolute(0) == 0

    # ---------- factorial ----------
    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_positive(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_non_integer_raises_error(self):
        with pytest.raises(ValueError, match="requires an integer"):
            self.calc.factorial(3.5)

    def test_factorial_negative_raises_error(self):
        with pytest.raises(ValueError, match="not defined for negative"):
            self.calc.factorial(-3)