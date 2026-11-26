import pytest
from calculator import Calculator

class TestCalculator:
    """Test suite for Calculator class."""

    def setup_method(self):
        """Create a fresh Calculator instance before each test."""
        self.calc = Calculator()

    # --- ADD TESTS ---
    def test_add_positive_numbers(self):
        """Test adding two positive numbers."""
        assert self.calc.add(5, 3) == 8

    def test_add_negative_numbers(self):
        """Test adding two negative numbers."""
        assert self.calc.add(-5, -7) == -12

    def test_add_mixed_numbers(self):
        """Test adding positive and negative numbers."""
        assert self.calc.add(-5, 10) == 5

    # --- SUBTRACT TESTS ---
    def test_subtract_positive_result(self):
        assert self.calc.subtract(10, 4) == 6

    def test_subtract_negative_result(self):
        assert self.calc.subtract(4, 10) == -6

    # --- MULTIPLY TESTS ---
    def test_multiply_positive_numbers(self):
        assert self.calc.multiply(4, 3) == 12

    def test_multiply_by_zero(self):
        assert self.calc.multiply(5, 0) == 0

    def test_multiply_negative_numbers(self):
        assert self.calc.multiply(-4, 3) == -12
        assert self.calc.multiply(-4, -3) == 12

    # --- DIVIDE TESTS ---
    def test_divide_normal_case(self):
        assert self.calc.divide(10, 2) == 5.0
        # Uso de pytest.approx para decimales
        assert self.calc.divide(10, 3) == pytest.approx(3.333333, rel=1e-5)

    def test_divide_by_zero_raises_error(self):
        """Test that dividing by zero raises ValueError."""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    def test_divide_negative_numbers(self):
        assert self.calc.divide(-10, 2) == -5.0

    # --- POWER TESTS ---
    def test_power_positive_exponent(self):
        assert self.calc.power(2, 3) == 8

    def test_power_zero_exponent(self):
        assert self.calc.power(5, 0) == 1

    def test_power_negative_exponent(self):
        assert self.calc.power(2, -1) == 0.5

    # --- SQRT TESTS ---
    def test_sqrt_positive_number(self):
        assert self.calc.sqrt(16) == 4.0

    def test_sqrt_zero(self):
        assert self.calc.sqrt(0) == 0.0

    def test_sqrt_negative_raises_error(self):
        """Test that sqrt of negative number raises ValueError."""
        with pytest.raises(ValueError, match="Cannot calculate square root of negative number"):
            self.calc.sqrt(-4)

    # --- MODULO TESTS (Part 4) ---
    def test_modulo_normal_case(self):
        assert self.calc.modulo(10, 3) == 1

    def test_modulo_by_zero_raises_error(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.modulo(10, 0)

    # --- ABSOLUTE TESTS (Part 4) ---
    def test_absolute_positive_and_zero(self):
        assert self.calc.absolute(5) == 5
        assert self.calc.absolute(0) == 0

    def test_absolute_negative(self):
        assert self.calc.absolute(-15) == 15

    # --- FACTORIAL TESTS (Part 4) ---
    def test_factorial_normal_case(self):
        assert self.calc.factorial(5) == 120

    def test_factorial_zero_or_one(self):
        assert self.calc.factorial(0) == 1
        assert self.calc.factorial(1) == 1

    def test_factorial_negative_raises_error(self):
        with pytest.raises(ValueError, match="Factorial not defined for negative numbers"):
            self.calc.factorial(-3)

    def test_factorial_non_integer_raises_error(self):
        with pytest.raises(ValueError, match="Factorial requires an integer"):
            self.calc.factorial(5.5)