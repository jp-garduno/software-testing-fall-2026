"""Tests for the Calculator class."""

# pylint: disable=wrong-import-position,redefined-outer-name

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from calculator import Calculator


@pytest.fixture
def calc():
    """Provide a fresh Calculator instance for each test."""
    return Calculator()


def test_add_positive_numbers(calc):
    assert calc.add(2, 3) == 5


def test_add_negative_numbers(calc):
    assert calc.add(-2, -3) == -5


def test_subtract_numbers(calc):
    assert calc.subtract(10, 4) == 6


def test_multiply_numbers(calc):
    assert calc.multiply(3, 4) == 12


def test_multiply_by_zero(calc):
    assert calc.multiply(5, 0) == 0


def test_divide_numbers(calc):
    assert calc.divide(10, 2) == 5


def test_divide_by_zero_raises_error(calc):
    with pytest.raises(ValueError):
        calc.divide(10, 0)


def test_power_numbers(calc):
    assert calc.power(2, 3) == 8


def test_power_zero_exponent(calc):
    assert calc.power(5, 0) == 1


def test_history_records_operations(calc):
    calc.add(1, 1)
    calc.subtract(5, 2)
    assert len(calc.get_history()) == 2


def test_clear_history(calc):
    calc.add(1, 1)
    calc.clear_history()
    assert calc.get_history() == []
