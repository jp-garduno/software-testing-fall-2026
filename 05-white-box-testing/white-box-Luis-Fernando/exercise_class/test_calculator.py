import pytest
from calculator import Calculator

class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(-5, 3) == -2

    def test_subtract_positive_result(self):
        assert self.calc.subtract(8, 3) == 5

    def test_subtract_negative_result(self):
        assert self.calc.subtract(3, 8) == -5

    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(4, 3) == 12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(7, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-4, -3) == 12

    def test_divide_normal_case(self):
        assert self.calc.divide(7, 2) == 3.5

    @pytest.mark.parametrize("numerator", [10, 0, -10])
    @pytest.mark.parametrize("denominator", [0, 0.0, -0.0])
    def test_divide_by_zero_raises_error(self, numerator, denominator):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="^Cannot divide by zero$"):
            self.calc.divide(numerator, denominator)

    @pytest.mark.parametrize("a, b, expected", [(-8, -2, 4), (-8, 2, -4), (8, -2, -4)])
    def test_divide_negative_numbers(self, a, b, expected):
        assert self.calc.divide(a, b) == expected

    def test_power_positive_exponent(self):
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -3) == 0.125

    def test_sqrt_positive_number(self):
        assert self.calc.sqrt(25) == 5

    def test_sqrt_zero(self):
        assert self.calc.sqrt(0) == 0

    @pytest.mark.parametrize("value", [-1, -0.001, -1000000])
    def test_sqrt_negative_raises_error(self, value):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="^Cannot calculate square root of negative number$"):
            self.calc.sqrt(value)

    @pytest.mark.parametrize("a, b, expected", [(0, 5, 5), (5, 0, 5), (5, -5, 0), (10**20, 1, 100000000000000000001)])
    def test_add_edge_cases(self, a, b, expected):
        assert self.calc.add(a, b) == expected

    def test_add_decimals(self):
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    @pytest.mark.parametrize("a, b, expected", [(5, 5, 0), (0, 5, -5), (5, 0, 5), (-5, -3, -2), (5, -3, 8)])
    def test_subtract_edge_cases(self, a, b, expected):
        assert self.calc.subtract(a, b) == expected

    def test_subtract_decimals(self):
        assert self.calc.subtract(0.3, 0.1) == pytest.approx(0.2)

    @pytest.mark.parametrize("a, b, expected", [(-4, 3, -12), (4, -3, -12), (0, 7, 0), (7, 1, 7), (10**10, 10**10, 10**20)])
    def test_multiply_edge_cases(self, a, b, expected):
        assert self.calc.multiply(a, b) == expected

    def test_multiply_decimals(self):
        assert self.calc.multiply(0.1, 0.2) == pytest.approx(0.02)

    def test_divide_zero_numerator(self):
        assert self.calc.divide(0, 5) == 0

    def test_divide_decimals(self):
        assert self.calc.divide(0.3, 0.1) == pytest.approx(3)

    @pytest.mark.parametrize("base, exponent, expected", [(0, 3, 0), (0, 0, 1), (-2, 3, -8), (-2, 2, 4), (9, 0.5, 3), (10, 20, 10**20)])
    def test_power_edge_cases(self, base, exponent, expected):
        assert self.calc.power(base, exponent) == expected

    def test_power_zero_base_negative_exponent_raises_error(self):
        with pytest.raises(ZeroDivisionError):
            self.calc.power(0, -1)

    @pytest.mark.parametrize("value, expected", [(2, 1.4142135623730951), (0.25, 0.5), (10**20, 10**10)])
    def test_sqrt_edge_cases(self, value, expected):
        assert self.calc.sqrt(value) == pytest.approx(expected)
