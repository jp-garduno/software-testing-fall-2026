from src.calculator import calcular


def test_suma():
    assert calcular("1", 5, 3) == 8


def test_resta():
    assert calcular("2", 10, 4) == 6


def test_multiplicacion():
    assert calcular("3", 5, 5) == 25


def test_division():
    assert calcular("4", 10, 2) == 5


def test_potencia():
    assert calcular("5", 2, 3) == 8


def test_modulo():
    assert calcular("6", 10, 3) == 1


def test_promedio():
    assert calcular("7", 10, 20) == 15


def test_mayor():
    assert calcular("8", 10, 5) == 10


def test_menor():
    assert calcular("9", 10, 5) == 5


def test_porcentaje():
    assert calcular("10", 200, 10) == 20
