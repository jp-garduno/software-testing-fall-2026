"""Unit tests for Calculator (exercise 1)."""

import pytest

from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # add
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-5, -3) == -8

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(5, -3) == 2

    def test_add_large_numbers(self):
        """Test adding very large numbers."""
        assert self.calc.add(10**18, 10**18) == 2 * 10**18

    def test_add_floats(self):
        """Test adding floats uses approximate comparison."""
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    # subtract
    def test_subtract_positive_result(self):
        """Test subtraction with a positive result."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Test subtraction with a negative result."""
        assert self.calc.subtract(4, 10) == -6

    # multiply
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert self.calc.multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert self.calc.multiply(7, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying two negative numbers gives a positive."""
        assert self.calc.multiply(-4, -5) == 20

    # divide
    def test_divide_normal_case(self):
        """Test regular division."""
        assert self.calc.divide(10, 2) == 5

    def test_divide_with_decimal_result(self):
        """Test division resulting in decimal."""
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test dividing two negative numbers gives a positive."""
        assert self.calc.divide(-10, -2) == 5

    def test_divide_zero_by_number(self):
        """Test dividing zero by a non-zero number."""
        assert self.calc.divide(0, 5) == 0

    # power
    def test_power_positive_exponent(self):
        """Test power with a positive exponent."""
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test any number to the power of zero is one."""
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test power with a negative exponent."""
        assert self.calc.power(2, -2) == pytest.approx(0.25)

    # sqrt
    def test_sqrt_positive_number(self):
        """Test square root of a positive number."""
        assert self.calc.sqrt(16) == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="square root of negative"):
            self.calc.sqrt(-1)

    # modulo
    def test_modulo_normal_case(self):
        """Test remainder of a regular division."""
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_exact_division(self):
        """Test remainder is zero when evenly divisible."""
        assert self.calc.modulo(9, 3) == 0

    def test_modulo_by_zero_raises_error(self):
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    # absolute
    def test_absolute_negative_number(self):
        """Test absolute value of a negative number."""
        assert self.calc.absolute(-7) == 7

    def test_absolute_positive_number(self):
        """Test absolute value of a positive number."""
        assert self.calc.absolute(7) == 7

    def test_absolute_zero(self):
        """Test absolute value of zero."""
        assert self.calc.absolute(0) == 0

    # factorial
    def test_factorial_zero(self):
        """Test factorial of 0 is 1."""
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        """Test factorial of 1 is 1."""
        assert self.calc.factorial(1) == 1

    def test_factorial_positive_number(self):
        """Test factorial of a regular positive number."""
        assert self.calc.factorial(5) == 120

    def test_factorial_negative_raises_error(self):
        """Test that factorial of a negative number raises ValueError."""
        with pytest.raises(ValueError, match="negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_non_integer_raises_error(self):
        """Test that factorial of a non-integer raises ValueError."""
        with pytest.raises(ValueError, match="requires an integer"):
            self.calc.factorial(2.5)
