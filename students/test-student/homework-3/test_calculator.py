"""Tests for calculator module"""

import pytest
from src.calculator import add, divide, subtract


def test_add():
    """Test addition"""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0


def test_subtract():
    """Test subtraction"""
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5


def test_divide():
    """Test division"""
    assert divide(10, 2) == 5
    assert divide(9, 3) == 3


def test_divide_by_zero():
    """Test division by zero raises error"""
    with pytest.raises(ValueError):
        divide(10, 0)
