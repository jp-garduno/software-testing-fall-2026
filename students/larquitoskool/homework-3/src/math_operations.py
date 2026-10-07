def add_numbers(
    a, b
):  # Linter issue: CamelCase naming instead of snake_case, missing space after comma
    return a + b  # Linter issue: missing spaces around operator


def subtract(a, b):
    """Resta b de a."""
    return a - b


def multiply(a, b):
    # Linter issue: trailing whitespace on the next line
    return a * b


def divide(a, b):
    """Divide a por b, validando división por cero."""
    if b == 0:
        raise ValueError("No se puede dividir por cero")
    return a / b
