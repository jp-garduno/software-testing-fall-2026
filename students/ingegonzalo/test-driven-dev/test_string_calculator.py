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

def test_newline_as_delimiter():
    assert add("1\n2,3") == 6
    assert add("1\n2\n3") == 6

def test_custom_single_char_delimiter():
    assert add("//;\n1;2") == 3
    assert add("//|\n1|2|3") == 6
    assert add("//*\n1*2*3") == 6

def test_negative_numbers_raise_exception():
    with pytest.raises(ValueError, match="negatives not allowed: -1"):
        add("-1,2")
    with pytest.raises(ValueError, match="negatives not allowed: -2, -3"):
        add("1,-2,-3")

def test_numbers_greater_than_1000_are_ignored():
    assert add("2,1001") == 2
    assert add("1000,1001,2") == 1002

def test_delimiters_of_any_length():
    assert add("//[***]\n1***2***3") == 6
    assert add("//[---]\n1---2---3") == 6