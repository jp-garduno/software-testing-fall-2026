"""Unit tests for the Calculator class covering all operations, edge cases, and exceptions."""
import pytest
from calculator import Calculator


class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # Tests for add method
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-4, -6) == -10

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(10, -3) == 7
        assert self.calc.add(-8, 5) == -3

    def test_add_zero(self):
        """Test adding zero."""
        assert self.calc.add(7, 0) == 7
        assert self.calc.add(0, 0) == 0

    def test_add_floats(self):
        """Test adding floating-point numbers."""
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    # Tests for subtract method
    def test_subtract_positive_result(self):
        """Test subtracting yielding a positive result."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Test subtracting yielding a negative result."""
        assert self.calc.subtract(3, 8) == -5

    def test_subtract_zero(self):
        """Test subtracting zero and subtracting from zero."""
        assert self.calc.subtract(5, 0) == 5
        assert self.calc.subtract(0, 5) == -5

    def test_subtract_negative_numbers(self):
        """Test subtracting negative numbers."""
        assert self.calc.subtract(-5, -2) == -3
        assert self.calc.subtract(-5, 2) == -7

    # Tests for multiply method
    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert self.calc.multiply(6, 7) == 42

    def test_multiply_by_zero(self):
        """Test multiplying by zero."""
        assert self.calc.multiply(10, 0) == 0
        assert self.calc.multiply(0, 5) == 0

    def test_multiply_negative_numbers(self):
        """Test multiplying negative numbers."""
        assert self.calc.multiply(-3, 4) == -12
        assert self.calc.multiply(-4, -5) == 20

    def test_multiply_floats(self):
        """Test multiplying floating-point numbers."""
        assert self.calc.multiply(2.5, 4.0) == pytest.approx(10.0)

    # Tests for divide method
    def test_divide_normal_case(self):
        """Test normal division resulting in whole number."""
        assert self.calc.divide(20, 4) == 5.0

    def test_divide_with_decimal_result(self):
        """Test division resulting in repeating decimal."""
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test division involving negative numbers."""
        assert self.calc.divide(-15, 3) == -5.0
        assert self.calc.divide(15, -3) == -5.0
        assert self.calc.divide(-15, -3) == 5.0

    # Tests for power method
    def test_power_positive_exponent(self):
        """Test raising base to positive exponent."""
        assert self.calc.power(2, 3) == 8
        assert self.calc.power(5, 2) == 25

    def test_power_zero_exponent(self):
        """Test raising base to zero exponent."""
        assert self.calc.power(10, 0) == 1
        assert self.calc.power(0, 0) == 1

    def test_power_negative_exponent(self):
        """Test raising base to negative exponent."""
        assert self.calc.power(2, -1) == pytest.approx(0.5)
        assert self.calc.power(4, -2) == pytest.approx(0.0625)

    # Tests for sqrt method
    def test_sqrt_positive_number(self):
        """Test square root of a positive number."""
        assert self.calc.sqrt(16) == pytest.approx(4.0)
        assert self.calc.sqrt(2) == pytest.approx(1.4142135, rel=1e-5)

    def test_sqrt_zero(self):
        """Test square root of zero."""
        assert self.calc.sqrt(0) == 0.0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.sqrt(-9)

    # Tests for modulo method (Part 4)
    def test_modulo_normal(self):
        """Test modulo remainder calculation."""
        assert self.calc.modulo(10, 3) == 1
        assert self.calc.modulo(14, 5) == 4

    def test_modulo_exact_division(self):
        """Test modulo when evenly divisible."""
        assert self.calc.modulo(12, 4) == 0

    def test_modulo_by_zero_raises_error(self):
        """Test modulo with zero divisor raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(8, 0)

    # Tests for absolute method (Part 4)
    def test_absolute_positive(self):
        """Test absolute value of a positive number."""
        assert self.calc.absolute(15) == 15

    def test_absolute_negative(self):
        """Test absolute value of a negative number."""
        assert self.calc.absolute(-23) == 23

    def test_absolute_zero(self):
        """Test absolute value of zero."""
        assert self.calc.absolute(0) == 0

    # Tests for factorial method (Part 4)
    def test_factorial_zero_and_one(self):
        """Test factorial of 0 and 1."""
        assert self.calc.factorial(0) == 1
        assert self.calc.factorial(1) == 1

    def test_factorial_positive_numbers(self):
        """Test factorial of typical positive integers."""
        assert self.calc.factorial(2) == 2
        assert self.calc.factorial(5) == 120
        assert self.calc.factorial(6) == 720

    def test_factorial_negative_raises_error(self):
        """Test factorial with negative integer raises ValueError."""
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            self.calc.factorial(-3)

    def test_factorial_non_integer_raises_error(self):
        """Test factorial with non-integer type raises ValueError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(3.5)
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial("5")
