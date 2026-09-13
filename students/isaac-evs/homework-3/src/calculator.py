"""Simple calculator utilities with operation history tracking."""


class Calculator:
    """Performs basic arithmetic operations and tracks a history of results."""

    def __init__(self):
        self.history = []

    def add(self, a, b):
        """Return the sum of a and b."""
        result = a + b
        self.history.append(result)
        return result

    def subtract(self, a, b):
        """Return the difference of a and b."""
        result = a - b
        self.history.append(result)
        return result

    def multiply(self, a, b):
        """Return the product of a and b."""
        result = a * b
        self.history.append(result)
        return result

    def divide(self, a, b):
        """Return the quotient of a and b, or None if dividing by zero."""
        try:
            result = a / b
        except ZeroDivisionError:
            result = None
        self.history.append(result)
        return result

    def average(self, numbers=None):
        """Return the average of a list of numbers."""
        if numbers is None:
            numbers = []
        total = 0
        for number in numbers:
            total = total + number
        return total / len(numbers)

    def get_history(self):
        """Return the list of results computed so far."""
        return self.history

    def clear_history(self):
        """Clear the recorded operation history."""
        self.history = []


def calculate_percentage(value, total):
    """Return value as a percentage of total."""
    return (value / total) * 100
