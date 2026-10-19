def test_empty_string_returns_zero():
    calculator = StringCalculator()
    assert calculator.add("") == 0

class StringCalculator:
    def add(self, numbers: str) -> int:
        return 0