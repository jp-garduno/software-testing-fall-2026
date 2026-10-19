import pytest
from string_calculator import add

def test_empty_string_returns_zero():
    assert add("") == 0

def test_single_number_returns_the_number():
    assert add("1") == 1
    assert add("5") == 5

def test_two_numbers_separated_by_comma():
    assert add("1,2") == 3
    assert add("5,10") == 15

def test_unknown_amount_of_numbers():
    assert add("1,2,3") == 6
    assert add("1,2,3,4,5") == 15