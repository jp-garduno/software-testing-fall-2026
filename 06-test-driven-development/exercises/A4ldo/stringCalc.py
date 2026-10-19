import numbers


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

class StringCalculator:
    def add(self, numbers: str) -> int:
        if numbers == "":
            return 0
        parts = numbers.split(",")
        return sum(int(part) for part in parts)
