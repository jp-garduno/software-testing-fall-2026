"""Calculator class used in white box testing exercise 1."""

import math


class Calculator:
    """A simple calculator with basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b

    def divide(self, a, b):
        """Divide a by b. Raises ValueError if b is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Raise base to the power of exponent."""
        return base**exponent

    def sqrt(self, x):
        """Calculate square root. Raises ValueError if x is negative."""
        if x < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(x)

    def modulo(self, a, b):
        """Return remainder of a divided by b."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a % b

    def absolute(self, x):
        """Return absolute value of x."""
        return abs(x)

    def factorial(self, n):
        """Calculate factorial of n. Raises ValueError if n is negative or not an integer."""
        if not isinstance(n, int):
            raise ValueError("Factorial requires an integer")
        if n < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if n == 0 or n == 1:
            return 1
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
