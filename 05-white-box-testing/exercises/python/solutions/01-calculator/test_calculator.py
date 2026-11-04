"""Reference test suite for Exercise 1: Calculator Unit Tests (Module 05 - White Box Testing)."""

# pylint: disable=attribute-defined-outside-init,too-many-public-methods
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

    def test_add_zero_returns_same_number(self):
        """Test that zero is the identity element for addition."""
        assert self.calc.add(7, 0) == 7

    def test_add_floats(self):
        """Test adding floating point numbers."""
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    def test_add_large_numbers(self):
        """Test adding very large integers (Python ints do not overflow)."""
        assert self.calc.add(10**20, 10**20) == 2 * 10**20

    # subtract

    def test_subtract_positive_result(self):
        """Test subtraction that yields a positive result."""
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        """Test subtraction that yields a negative result."""
        assert self.calc.subtract(4, 10) == -6

    def test_subtract_same_numbers_returns_zero(self):
        """Test subtracting a number from itself."""
        assert self.calc.subtract(9, 9) == 0

    def test_subtract_negative_number(self):
        """Test that subtracting a negative number adds its magnitude."""
        assert self.calc.subtract(5, -3) == 8

    # multiply

    def test_multiply_positive_numbers(self):
        """Test multiplying two positive numbers."""
        assert self.calc.multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        """Test that multiplying by zero returns zero."""
        assert self.calc.multiply(123, 0) == 0

    def test_multiply_negative_numbers(self):
        """Test that multiplying two negatives yields a positive."""
        assert self.calc.multiply(-4, -5) == 20

    def test_multiply_mixed_signs(self):
        """Test that multiplying numbers of different sign yields a negative."""
        assert self.calc.multiply(-4, 5) == -20

    def test_multiply_by_one_returns_same_number(self):
        """Test that one is the identity element for multiplication."""
        assert self.calc.multiply(42, 1) == 42

    # divide

    def test_divide_normal_case(self):
        """Test exact division."""
        assert self.calc.divide(10, 2) == 5

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        """Test dividing two negative numbers yields a positive."""
        assert self.calc.divide(-10, -2) == 5

    def test_divide_mixed_signs(self):
        """Test dividing numbers of different sign yields a negative."""
        assert self.calc.divide(-10, 2) == -5

    def test_divide_with_decimal_result(self):
        """Test division resulting in decimal."""
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_zero_by_number_returns_zero(self):
        """Test that zero divided by a non-zero number is zero."""
        assert self.calc.divide(0, 5) == 0

    def test_divide_by_float_zero_raises_error(self):
        """Test that 0.0 is also treated as zero (0.0 == 0 is True)."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0.0)

    # power

    def test_power_positive_exponent(self):
        """Test raising a number to a positive exponent."""
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        """Test that any number to the power of zero is one."""
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        """Test that a negative exponent yields the reciprocal."""
        assert self.calc.power(2, -2) == pytest.approx(0.25)

    def test_power_zero_base(self):
        """Test that zero to a positive exponent is zero."""
        assert self.calc.power(0, 5) == 0

    def test_power_negative_base_odd_exponent(self):
        """Test that a negative base with an odd exponent stays negative."""
        assert self.calc.power(-2, 3) == -8

    def test_power_fractional_exponent(self):
        """Test that exponent 0.5 behaves like a square root."""
        assert self.calc.power(9, 0.5) == pytest.approx(3.0)

    # sqrt

    def test_sqrt_positive_number(self):
        """Test square root of a positive number."""
        assert self.calc.sqrt(16) == pytest.approx(4.0)

    def test_sqrt_zero(self):
        """Test that the square root of zero is zero (boundary value)."""
        assert self.calc.sqrt(0) == 0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Cannot calculate square root of negative number"
        ):
            self.calc.sqrt(-1)

    def test_sqrt_non_perfect_square(self):
        """Test square root of a non-perfect square."""
        assert self.calc.sqrt(2) == pytest.approx(1.414213, rel=1e-5)

    def test_sqrt_small_negative_raises_error(self):
        """Test the boundary just below zero."""
        with pytest.raises(ValueError):
            self.calc.sqrt(-0.0001)

    # modulo (Part 4)

    def test_modulo_normal_case(self):
        """Test remainder of an integer division."""
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_exact_division_returns_zero(self):
        """Test that exact division leaves no remainder."""
        assert self.calc.modulo(10, 5) == 0

    def test_modulo_by_zero_raises_error(self):
        """Test that modulo by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    def test_modulo_negative_dividend(self):
        """Test that Python's modulo takes the sign of the divisor."""
        assert self.calc.modulo(-10, 3) == 2

    # absolute (Part 4)

    def test_absolute_positive_number(self):
        """Test that a positive number is unchanged."""
        assert self.calc.absolute(5) == 5

    def test_absolute_negative_number(self):
        """Test that a negative number becomes positive."""
        assert self.calc.absolute(-5) == 5

    def test_absolute_zero(self):
        """Test that the absolute value of zero is zero."""
        assert self.calc.absolute(0) == 0

    def test_absolute_negative_float(self):
        """Test absolute value of a negative float."""
        assert self.calc.absolute(-3.5) == pytest.approx(3.5)

    # factorial (Part 4)

    def test_factorial_zero_returns_one(self):
        """Test that 0! is 1."""
        assert self.calc.factorial(0) == 1

    def test_factorial_one_returns_one(self):
        """Test that 1! is 1."""
        assert self.calc.factorial(1) == 1

    def test_factorial_positive_number(self):
        """Test factorial of a number that runs the loop."""
        assert self.calc.factorial(5) == 120

    def test_factorial_large_number(self):
        """Test factorial of a large number (Python ints do not overflow)."""
        assert self.calc.factorial(20) == 2432902008176640000

    def test_factorial_negative_raises_error(self):
        """Test that factorial of a negative number raises ValueError."""
        with pytest.raises(
            ValueError, match="Factorial not defined for negative numbers"
        ):
            self.calc.factorial(-1)

    def test_factorial_float_raises_error(self):
        """Test that factorial of a non-integer raises ValueError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(3.5)

    def test_factorial_string_raises_error(self):
        """Test that factorial of a string raises ValueError."""
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial("5")

    # Parametrized example (advanced tip from the exercise)

    @pytest.mark.parametrize(
        "a, b, expected",
        [
            (1, 1, 2),
            (-1, 1, 0),
            (0, 0, 0),
            (2.5, 2.5, 5.0),
        ],
    )
    def test_add_parametrized(self, a, b, expected):
        """Test several add cases with a single parametrized test."""
        assert self.calc.add(a, b) == pytest.approx(expected)
