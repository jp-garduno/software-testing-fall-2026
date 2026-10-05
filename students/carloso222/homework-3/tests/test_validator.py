"""Tests for validator functions."""

# pylint: disable=wrong-import-position

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from validator import (
    in_range,
    is_integer,
    is_number,
    is_positive,
    safe_sqrt_input,
    validate_division,
    validate_operands,
)


def test_is_number_valid():
    assert is_number("3.14") is True
    assert is_number(5) is True


def test_is_number_invalid():
    assert is_number("abc") is False
    assert is_number(None) is False


def test_is_positive_true():
    assert is_positive(5) is True


def test_is_positive_false_for_negative():
    assert is_positive(-5) is False


def test_is_positive_false_for_non_number():
    assert is_positive("abc") is False


def test_is_integer_true():
    assert is_integer(4.0) is True


def test_is_integer_false():
    assert is_integer(4.5) is False


def test_validate_operands_both_valid():
    assert validate_operands(1, 2) == (True, True)


def test_validate_operands_one_invalid():
    assert validate_operands(1, "x") == (True, False)


def test_validate_division_valid():
    assert validate_division(10, 2) is True


def test_validate_division_by_zero():
    assert validate_division(10, 0) is False


def test_in_range_true():
    assert in_range(5, 0, 10) is True


def test_in_range_false():
    assert in_range(15, 0, 10) is False


def test_safe_sqrt_input_valid():
    assert safe_sqrt_input(9) is True


def test_safe_sqrt_input_negative():
    assert safe_sqrt_input(-9) is False


def test_is_number_none():
    assert is_number(None) is False


def test_validate_division_invalid_operand():
    assert validate_division("abc", 2) is False


def test_in_range_non_number():
    assert in_range("abc", 0, 10) is False
