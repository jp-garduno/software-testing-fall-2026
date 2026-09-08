"""Simple calculator module"""


def add(a, b):
    """Add two numbers"""
    return a + b


def subtract(a, b):
    """Subtract b from a"""
    return a - b


def multiply(x, y):
    """Multiply two numbers"""
    return x * y


def divide(numerator, denominator):
    """Divide numerator by denominator"""
    if denominator == 0:
        raise ValueError("Cannot divide by zero")
    return numerator / denominator


def power(base, exponent):
    """Calculate base raised to exponent"""
    return base**exponent
