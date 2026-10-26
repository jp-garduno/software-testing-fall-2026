import re

import pytest


def test_empty_string_returns_zero():
    calculator = StringCalculator()
    assert calculator.add("") == 0


def test_single_number_returns_itself():
    calculator = StringCalculator()
    assert calculator.add("1") == 1
    assert calculator.add("5") == 5


def test_two_numbers_comma_separated():
    calculator = StringCalculator()
    assert calculator.add("1,2") == 3
    assert calculator.add("5,10") == 15


def test_handles_multiple_numbers():
    calculator = StringCalculator()
    assert calculator.add("1,2,3") == 6
    assert calculator.add("1,2,3,4,5") == 15


def test_newline_delimiter():
    calc = StringCalculator()
    assert calc.add("1\n2,3") == 6
    assert calc.add("1\n2\n3") == 6


def test_custom_delimiter():
    calc = StringCalculator()
    assert calc.add("//;\n1;2") == 3
    assert calc.add("//|\n1|2|3") == 6


def test_negative_numbers_throw_exception():
    calc = StringCalculator()

    with pytest.raises(ValueError, match="negatives not allowed: -1"):
        calc.add("-1,2")

    with pytest.raises(ValueError, match=r"negatives not allowed: -2, -3"):
        calc.add("1,-2,-3")


def test_ignore_numbers_greater_than_1000():
    calc = StringCalculator()
    assert calc.add("2,1001") == 2
    assert calc.add("1000,1001,2") == 1002


def test_delimiter_any_length():
    calc = StringCalculator()
    assert calc.add("//[***]\n1***2***3") == 6
    assert calc.add("//[---]\n1---2---3") == 6


def test_multiple_delimiters():
    calc = StringCalculator()
    assert calc.add("//[*][%]\n1*2%3") == 6
    assert calc.add("//[**][%%]\n1**2%%3") == 6


class StringCalculator:
    def add(self, numbers: str) -> int:
        if numbers == "":
            return 0

        delimiters = [","]

        if numbers.startswith("//"):
            delimiter_end = numbers.index("\n")
            delimiter_spec = numbers[2:delimiter_end]

            bracket_pattern = r"\[([^\]]+)\]"
            matches = re.findall(bracket_pattern, delimiter_spec)

            if matches:
                delimiters = matches
            else:
                delimiters = [delimiter_spec]

            numbers = numbers[delimiter_end + 1 :]

        numbers = numbers.replace("\n", ",")
        for delimiter in delimiters:
            numbers = numbers.replace(delimiter, ",")

        parts = [part for part in numbers.split(",") if part]
        int_parts = [int(part) for part in parts]

        negatives = [n for n in int_parts if n < 0]
        if negatives:
            neg_str = ", ".join(map(str, negatives))
            raise ValueError(f"negatives not allowed: {neg_str}")

        valid_numbers = [n for n in int_parts if n <= 1000]

        return sum(valid_numbers)

calc = StringCalculator()

calc.add("//;\n1;2\n3") 
calc.add("//;\n-1;2;")
calc.add("1001,-1")
calc.add("-1001")
calc.add("1001")
calc.add("//[*][%][#]\n1*2%3#4")
calc.add("//;n")
calc.add("//-\n-1-2")
calc.add("1,\n2")
calc.add("a,1")
calc.add("1.5,2")
calc.add("//;1;2")
