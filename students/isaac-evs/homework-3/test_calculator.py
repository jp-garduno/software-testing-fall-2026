from src.calculator import Calculator, calculate_percentage


def test_add_returns_sum():
    calc = Calculator()
    assert calc.add(2, 3) == 5


def test_subtract_returns_difference():
    calc = Calculator()
    assert calc.subtract(5, 3) == 2


def test_multiply_returns_product():
    calc = Calculator()
    assert calc.multiply(4, 3) == 12


def test_divide_returns_quotient():
    calc = Calculator()
    assert calc.divide(10, 2) == 5


def test_divide_by_zero_returns_none():
    calc = Calculator()
    assert calc.divide(10, 0) is None


def test_average_of_numbers():
    calc = Calculator()
    assert calc.average([2, 4, 6]) == 4


def test_history_tracks_operations():
    calc = Calculator()
    calc.add(1, 1)
    calc.subtract(5, 2)
    assert calc.get_history() == [2, 3]


def test_clear_history_empties_list():
    calc = Calculator()
    calc.add(1, 1)
    calc.clear_history()
    assert calc.get_history() == []


def test_calculate_percentage():
    assert calculate_percentage(50, 200) == 25.0
