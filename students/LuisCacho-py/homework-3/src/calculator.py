"""Calculator module providing basic arithmetic operations.

This module implements a simple but complete calculator that supports
addition, subtraction, multiplication, division, power, and modulo.
"""


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    def __init__(self):
        """Initialize the calculator with an empty history."""
        self.history = []

    def add(self, a, b):
        """Return the sum of two numbers.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The sum a + b.
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a, b):
        """Return the difference of two numbers.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The difference a - b.
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a, b):
        """Return the product of two numbers.

        Args:
            a: First operand.
            b: Second operand.

        Returns:
            The product a * b.
        """
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a, b):
        """Return the quotient of two numbers.

        Args:
            a: Dividend.
            b: Divisor (must not be zero).

        Returns:
            The quotient a / b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, base, exponent):
        """Return base raised to the power of exponent.

        Args:
            base: The base number.
            exponent: The exponent.

        Returns:
            base ** exponent.
        """
        result = base**exponent
        self.history.append(f"{base} ** {exponent} = {result}")
        return result

    def modulo(self, a, b):
        """Return the remainder of a divided by b.

        Args:
            a: Dividend.
            b: Divisor (must not be zero).

        Returns:
            a % b.

        Raises:
            ValueError: If b is zero.
        """
        if b == 0:
            raise ValueError("Modulo by zero is not allowed")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        return result

    def clear_history(self):
        """Clear the operation history."""
        self.history = []

    def get_history(self):
        """Return a copy of the operation history.

        Returns:
            A list of strings representing past operations.
        """
        return list(self.history)
