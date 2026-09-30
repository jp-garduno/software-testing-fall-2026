import pytest
from calculator import Calculator

class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # add
    def test_add_positive_numbers(self):
        assert self.calc.add(2, 3) == 5

    def test_add_negative_numbers(self):
        assert self.calc.add(-2, -3) == -5

    def test_add_mixed_numbers(self):
        assert self.calc.add(-2, 3) == 1

    # subtract
    def test_subtract_positive_result(self):
        assert self.calc.subtract(5, 2) == 3

    def test_subtract_negative_result(self):
        assert self.calc.subtract(2, 5) == -3

    # multiply
    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(2, 3) == 6

    def test_multiply_by_zero(self):
        assert self.calc.multiply(2, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-2, 3) == -6

    # divide
    def test_divide_normal_case(self):
        assert self.calc.divide(6, 2) == 3

    def test_divide_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        assert self.calc.divide(-6, 2) == -3

    def test_divide_with_decimal_result(self):
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    # power
    def test_power_positive_exponent(self):
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        assert self.calc.power(2, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -1) == 0.5

    # sqrt
    def test_sqrt_positive_number(self):
        assert self.calc.sqrt(16) == 4.0

    def test_sqrt_zero(self):
        assert self.calc.sqrt(0) == 0.0

    def test_sqrt_negative_raises_error(self):
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.sqrt(-1)

    # modulo
    def test_modulo_normal_case(self):
        assert self.calc.modulo(5, 2) == 1

    def test_modulo_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(5, 0)

    # absolute
    def test_absolute_positive(self):
        assert self.calc.absolute(5) == 5

    def test_absolute_negative(self):
        assert self.calc.absolute(-5) == 5

    # factorial
    def test_factorial_normal_case(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_zero(self):
        assert self.calc.factorial(0) == 1

    def test_factorial_one(self):
        assert self.calc.factorial(1) == 1

    def test_factorial_negative_raises_error(self):
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            self.calc.factorial(-1)

    def test_factorial_non_integer_raises_error(self):
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(2.5)
