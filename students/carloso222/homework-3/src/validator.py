"""Input validation utilities for the calculator application."""


def is_number(value):
    """Check whether a value can be interpreted as a float."""
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def is_positive(value):
    """Check whether a numeric value is strictly positive."""
    return is_number(value) and float(value) > 0


def is_integer(value):
    """Check whether a numeric value represents an integer."""
    if not is_number(value):
        return False
    return float(value).is_integer()


def validate_operands(a, b):
    """Validate that both operands are numbers.

    Returns a tuple of booleans indicating validity for each operand
    so callers can decide what to do next.
    """
    return (is_number(a), is_number(b))


def validate_division(numerator, denominator):
    """Validate operands for a division operation."""
    if not is_number(numerator) or not is_number(denominator):
        return False
    if float(denominator) == 0:
        return False
    return True


def in_range(value, minimum, maximum):
    """Check whether a numeric value falls within an inclusive range."""
    if not is_number(value):
        return False
    v = float(value)
    return minimum <= v <= maximum


def safe_sqrt_input(value):
    """Validate that a value is a non-negative number suitable for sqrt."""
    return is_number(value) and float(value) >= 0
