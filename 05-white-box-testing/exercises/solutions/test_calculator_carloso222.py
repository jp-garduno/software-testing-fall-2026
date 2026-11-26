# pylint: disable=too-many-public-methods, attribute-defined-outside-init
import pytest
from calculator_carloso222 import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # ADD

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

    def test_add_large_numbers(self):
        """Test adding large numbers."""
        result = self.calc.add(1_000_000, 2_000_000)
        assert result == 3_000_000

    # SUBTRACT

    def test_subtract_positive_result(self):
        """Test subtraction resulting in a positive number."""
        result = self.calc.subtract(10, 4)
        assert result == 6

    def test_subtract_negative_result(self):
        """Test subtraction resulting in a negative number."""
        result = self.calc.subtract(4, 10)
        assert result == -6

    def test_subtract_zero(self):
        """Test subtracting equal numbers."""
        result = self.calc.subtract(5, 5)
        assert result == 0

    # MULTIPLY

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        result = self.calc.multiply(4, 3)
        assert result == 12

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        result = self.calc.multiply(10, 0)
        assert result == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers."""
        result = self.calc.multiply(-4, -3)
        assert result == 12

    def test_multiply_positive_and_negative(self):
        """Test multiplying positive and negative numbers."""
        result = self.calc.multiply(4, -3)
        assert result == -12

    # DIVIDE

    def test_divide_normal_case(self):
        """Test normal division."""
        result = self.calc.divide(10, 2)
        assert result == 5

    def test_divide_with_decimal_result(self):
        """Test division with floating point result."""
        result = self.calc.divide(10, 3)
        assert result == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(
            ValueError,
            match="Cannot divide by zero",
        ):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test division using negative numbers."""
        result = self.calc.divide(-10, 2)
        assert result == -5

    # POWER

    def test_power_positive_exponent(self):
        """Test positive exponent."""
        result = self.calc.power(2, 3)
        assert result == 8

    def test_power_zero_exponent(self):
        """Test zero exponent."""
        result = self.calc.power(5, 0)
        assert result == 1

    def test_power_negative_exponent(self):
        """Test negative exponent."""
        result = self.calc.power(2, -2)
        assert result == pytest.approx(0.25)

    def test_power_large_number(self):
        """Test a larger exponent."""
        result = self.calc.power(10, 6)
        assert result == 1_000_000

    # SQUARE ROOT

    def test_sqrt_positive_number(self):
        """Test square root of positive number."""
        result = self.calc.sqrt(16)
        assert result == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test square root of zero."""
        result = self.calc.sqrt(0)
        assert result == pytest.approx(0.0)

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(
            ValueError,
            match="Cannot calculate square root of negative number",
        ):
            self.calc.sqrt(-4)

    # MODULO

    def test_modulo_normal_case(self):
        """Test modulo operation."""
        result = self.calc.modulo(10, 3)
        assert result == 1

    def test_modulo_exact_division(self):
        """Test modulo when there is no remainder."""
        result = self.calc.modulo(10, 2)
        assert result == 0

    def test_modulo_by_zero_raises_error(self):
        """Test modulo by zero."""
        with pytest.raises(
            ValueError,
            match="Cannot divide by zero",
        ):
            self.calc.modulo(10, 0)

    # ABSOLUTE

    def test_absolute_positive_number(self):
        """Test absolute value of positive number."""
        result = self.calc.absolute(5)
        assert result == 5

    def test_absolute_negative_number(self):
        """Test absolute value of negative number."""
        result = self.calc.absolute(-5)
        assert result == 5

    def test_absolute_zero(self):
        """Test absolute value of zero."""
        result = self.calc.absolute(0)
        assert result == 0

    # FACTORIAL

    def test_factorial_positive_number(self):
        """Test factorial of positive integer."""
        result = self.calc.factorial(5)
        assert result == 120

    def test_factorial_zero(self):
        """Test factorial of zero."""
        result = self.calc.factorial(0)
        assert result == 1

    def test_factorial_one(self):
        """Test factorial of one."""
        result = self.calc.factorial(1)
        assert result == 1

    def test_factorial_large_number(self):
        """Test factorial of a larger integer."""
        result = self.calc.factorial(10)
        assert result == 3_628_800

    def test_factorial_negative_raises_error(self):
        """Test factorial with negative number."""
        with pytest.raises(
            ValueError,
            match="Factorial not defined for negative numbers",
        ):
            self.calc.factorial(-5)

    def test_factorial_decimal_raises_error(self):
        """Test factorial with non-integer value."""
        with pytest.raises(
            ValueError,
            match="Factorial requires an integer",
        ):
            self.calc.factorial(5.5)
