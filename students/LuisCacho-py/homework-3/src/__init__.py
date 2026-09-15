"""Homework 3 - Static Testing Setup.

This package provides calculator, validator, and statistics utilities
used for demonstrating static testing infrastructure.
"""

from .calculator import Calculator
from .statistics_utils import mean, median, mode, std_dev, summary, variance
from .validator import (
    validate_age,
    validate_credit_card,
    validate_email,
    validate_password,
    validate_phone,
    validate_url,
)

__all__ = [
    "Calculator",
    "mean",
    "median",
    "mode",
    "std_dev",
    "summary",
    "variance",
    "validate_age",
    "validate_credit_card",
    "validate_email",
    "validate_password",
    "validate_phone",
    "validate_url",
]
