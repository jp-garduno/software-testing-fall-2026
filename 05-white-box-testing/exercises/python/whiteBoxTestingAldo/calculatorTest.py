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
        result = self.calc.add(2, 3)
        assert result == 5

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        result = self.calc.add(-2, -3)
        assert result == -5

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        result = self.calc.add(2, -3)
        assert result == -1

    # TODO: Write tests for subtract method
    def test_subtract_positive_result(self):
        result = self.calc.subtract(5, 3)
        assert result == 2

    def test_subtract_negative_result(self):
        result = self.calc.subtract(3, 5)
        assert result == -2

    # TODO: Write tests for multiply method
    def test_multiply_positive_numbers(self):
        result = self.calc.multiply(2, 3)
        assert result == 6

    def test_multiply_by_zero(self):
        result = self.calc.multiply(2, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        result = self.calc.multiply(-2, -3)
        assert result == 6

    # TODO: Write tests for divide method
    def test_divide_normal_case(self):
        result = self.calc.divide(6, 2)
        assert result == 3

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError):
            self.calc.divide(6, 0)

    def test_divide_negative_numbers(self):
        result = self.calc.divide(-6, -2)
        assert result == 3

    # TODO: Write tests for power method
    def test_power_positive_exponent(self):
        result = self.calc.power(2, 3)
        assert result == 8

    def test_power_zero_exponent(self):
        result = self.calc.power(2, 0)
        assert result == 1

    def test_power_negative_exponent(self):
        result = self.calc.power(2, -3)
        assert result == 0.125

    # TODO: Write tests for sqrt method
    def test_sqrt_positive_number(self):
        result = self.calc.sqrt(4)
        assert result == 2

    def test_sqrt_zero(self):
        result = self.calc.sqrt(0)
        assert result == 0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError):
            self.calc.sqrt(-4)