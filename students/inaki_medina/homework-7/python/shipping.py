import math
import numbers
from decimal import Decimal, ROUND_HALF_UP, localcontext

__all__ = [
    "InvalidInputError",
    "DivisionByZeroError",
    "add",
    "subtract",
    "multiply",
    "divide",
    "reverse_string",
    "is_palindrome",
    "count_vowels",
    "capitalize_words",
    "calculate_shipping",
]

_WEIGHT_RATE = Decimal("0.5")
_DISTANCE_RATE = Decimal("0.1")
_EXPRESS_MULTIPLIER = Decimal("1.5")
_CENT = Decimal("0.01")

# Enough digits to hold any float exactly-enough before converting back.
_DECIMAL_PRECISION = 60

class InvalidInputError(TypeError, ValueError):
    """An argument has the wrong type. Catchable as TypeError or ValueError."""


class DivisionByZeroError(ValueError, ZeroDivisionError):
    """Division by zero. Catchable as ValueError or ZeroDivisionError."""


def _require_number(value, name):
    """Accept real numbers (int, float, Fraction, Decimal); reject bool and the rest."""
    if isinstance(value, bool) or not isinstance(value, (numbers.Real, Decimal)):
        raise InvalidInputError(
            f"{name} must be a number, got {type(value).__name__}"
        )
    if isinstance(value, Decimal) and value.is_snan():
        raise InvalidInputError(f"{name} must not be a signaling NaN")


def _is_finite(value):
    if isinstance(value, Decimal):
        return value.is_finite()
    if isinstance(value, numbers.Rational):
        # math.isfinite() would overflow on huge ints; rationals are always finite.
        return True
    return math.isfinite(value)


def _to_decimal(value):
    """Convert a finite number to Decimal using its shortest representation."""
    if isinstance(value, Decimal):
        return value
    if isinstance(value, numbers.Integral):
        return Decimal(int(value))
    if isinstance(value, numbers.Rational):
        return Decimal(int(value.numerator)) / Decimal(int(value.denominator))
    # repr() gives the shortest string that round-trips, so 0.1 -> Decimal("0.1").
    return Decimal(repr(float(value)))


def _require_flag(value, name):
    """Accept True/False (and 1/0); reject truthy strings like "no"."""
    if isinstance(value, bool):
        return value
    if isinstance(value, numbers.Integral) and value in (0, 1):
        return bool(value)
    raise InvalidInputError(f"{name} must be a boolean, got {value!r}")


def calculate_shipping(weight, distance, is_express=False):
    """
    Calculate shipping cost

    Args:
        weight: Package weight in kg
        distance: Distance in km
        is_express: Boolean for express shipping

    Returns:
        Shipping cost in dollars, rounded half-up to the cent
    """
    _require_number(weight, "weight")
    _require_number(distance, "distance")
    is_express = _require_flag(is_express, "is_express")

    if not _is_finite(weight) or not _is_finite(distance):
        raise ValueError("Weight and distance must be positive finite numbers")
    if weight <= 0 or distance <= 0:
        raise ValueError("Weight and distance must be positive")

    with localcontext() as ctx:
        ctx.prec = _DECIMAL_PRECISION
        base_cost = (_to_decimal(weight) * _WEIGHT_RATE
                     + _to_decimal(distance) * _DISTANCE_RATE)

        if is_express:
            base_cost *= _EXPRESS_MULTIPLIER

        # Make room for every integer digit plus the two decimals.
        ctx.prec = max(ctx.prec, base_cost.adjusted() + 3)
        cost = base_cost.quantize(_CENT, rounding=ROUND_HALF_UP)

    result = float(cost)
    if math.isinf(result):
        raise OverflowError("Shipping cost is too large to represent")
    return result
