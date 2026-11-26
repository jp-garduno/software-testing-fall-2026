"""Calculator module providing basic arithmetic operations."""


class Calculator:
    """A simple calculator that performs basic arithmetic operations."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        """Return the sum of a and b."""
        result = a + b
        self.history.append(("add", a, b, result))
        return result

    def subtract(self, a, b):
        """Return the difference of a and b."""
        result = a - b
        self.history.append(("subtract", a, b, result))
        return result

    def multiply(self, a, b):
        """Return the product of a and b."""
        result = a * b
        self.history.append(("multiply", a, b, result))
        return result

    def divide(self, a, b):
        """Return the quotient of a divided by b. Raises ValueError on division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        result = a / b
        self.history.append(("divide", a, b, result))
        return result

    def power(self, base, exponent):
        """Return base raised to the power of exponent."""
        result = base**exponent
        self.history.append(("power", base, exponent, result))
        return result

    def get_history(self):
        """Return the full list of past operations."""
        return self.history

    def clear_history(self):
        """Clear the operation history."""
        self.history = []
