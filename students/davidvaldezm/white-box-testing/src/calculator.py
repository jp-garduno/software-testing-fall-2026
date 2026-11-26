"""A small calculator used to practice unit testing."""

import math


class Calculator:
    """Provide basic arithmetic operations."""

    def add(self, first_number, second_number):
        """Return the sum of two numbers."""
        return first_number + second_number

    def subtract(self, first_number, second_number):
        """Return the result of subtracting the second number from the first."""
        return first_number - second_number

    def multiply(self, first_number, second_number):
        """Return the product of two numbers."""
        return first_number * second_number

    def divide(self, dividend, divisor):
        """Return a quotient, rejecting division by zero."""
        if divisor == 0:
            raise ValueError("Cannot divide by zero")
        return dividend / divisor

    def power(self, base, exponent):
        """Return ``base`` raised to ``exponent``."""
        return base**exponent

    def sqrt(self, value):
        """Return the square root of a non-negative number."""
        if value < 0:
            raise ValueError("Cannot calculate square root of negative number")
        return math.sqrt(value)

