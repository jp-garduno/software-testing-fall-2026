"""Calculator implementation for white-box testing exercise 1."""

import math


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract ``b`` from ``a``."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide ``a`` by ``b`` and reject division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Raise ``base`` to ``exponent``."""
        return base**exponent

    def sqrt(self, x):
        """Calculate a square root and reject negative values."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)
