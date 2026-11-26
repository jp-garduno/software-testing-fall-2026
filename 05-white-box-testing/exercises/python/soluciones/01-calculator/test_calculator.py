import pytest
from calculator import Calculator


class TestCalculator:  # pylint: disable=attribute-defined-outside-init
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        a = 1
        b = 2
        expected_result = 3
        result = self.calc.add(a, b)
        assert result == expected_result

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        a = -1
        b = -2
        expected_result = -3
        result = self.calc.add(a, b)
        assert result == expected_result

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        a = -5
        b = 4
        expected_result = -1
        result = self.calc.add(a, b)
        assert result == expected_result

    def test_subtract_positive_result(self):
        a = 5
        b = 3
        expected_result = 2
        result = self.calc.subtract(a, b)
        assert result == expected_result

    def test_subtract_negative_result(self):
        a = 3
        b = 5
        expected_result = -2
        result = self.calc.subtract(a, b)
        assert result == expected_result

    def test_multiply_positive_numbers(self):
        a = 3
        b = 4
        expected_result = 12
        result = self.calc.multiply(a, b)
        assert result == expected_result

    def test_multiply_by_zero(self):
        a = 7
        b = 0
        expected_result = 0
        result = self.calc.multiply(a, b)
        assert result == expected_result

    def test_multiply_negative_numbers(self):
        a = -3
        b = -4
        expected_result = 12
        result = self.calc.multiply(a, b)
        assert result == expected_result

    def test_divide_normal_case(self):
        a = 8
        b = 2
        expected_result = 4
        result = self.calc.divide(a, b)
        assert result == expected_result

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        a = 8
        b = 0
        with pytest.raises(ValueError):
            self.calc.divide(a, b)

    def test_divide_negative_numbers(self):
        a = -8
        b = 2
        expected_result = -4
        result = self.calc.divide(a, b)
        assert result == expected_result

    def test_power_positive_exponent(self):
        base = 2
        exponent = 3
        expected_result = 8
        result = self.calc.power(base, exponent)
        assert result == expected_result

    def test_power_zero_exponent(self):
        base = 5
        exponent = 0
        expected_result = 1
        result = self.calc.power(base, exponent)
        assert result == expected_result

    def test_power_negative_exponent(self):
        base = 2
        exponent = -2
        expected_result = 0.25
        result = self.calc.power(base, exponent)
        assert result == expected_result

    def test_sqrt_positive_number(self):
        number = 9
        expected_result = 3
        result = self.calc.sqrt(number)
        assert result == expected_result

    def test_sqrt_zero(self):
        number = 0
        expected_result = 0
        result = self.calc.sqrt(number)
        assert result == expected_result

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        number = -1
        with pytest.raises(ValueError):
            self.calc.sqrt(number)
