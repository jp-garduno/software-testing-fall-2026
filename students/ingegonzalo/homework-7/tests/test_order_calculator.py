import pytest

from data_loader import load_order_cases, run_order_case
from src.order_calculator import Order


@pytest.mark.parametrize("case", load_order_cases())
def test_order_calculation(case):
    """Cada fila de order_calculations.csv es un test independiente."""
    result = run_order_case(case)
    assert result == pytest.approx(case["expected"], abs=0.01)


def test_csv_has_minimum_cases():
    assert len(load_order_cases()) >= 25


# --- Casos de error que no caben en el CSV (esperan excepcion) ---
@pytest.mark.parametrize(
    "item",
    [
        {"name": "Bad", "price": -1, "quantity": 1, "weight": 0},
        {"name": "Bad", "price": 1, "quantity": -1, "weight": 0},
        {"name": "Bad", "price": 1, "quantity": 1, "weight": -1},
    ],
    ids=["negative_price", "negative_quantity", "negative_weight"],
)
def test_negative_values_rejected(item):
    with pytest.raises(ValueError):
        Order([item])


def test_invalid_customer_type_rejected():
    with pytest.raises(ValueError):
        Order([], customer_type="vip")


def test_negative_distance_rejected():
    with pytest.raises(ValueError):
        Order([]).set_shipping(-5)


# --- Valor de retorno de apply_discount ---
@pytest.mark.parametrize(
    "code,customer,price,expected",
    [
        ("SAVE10", "regular", 50, True),
        ("SAVE10", "regular", 49.99, False),
        ("SAVE20", "regular", 100, True),
        ("SAVE20", "regular", 99.99, False),
        ("FREESHIP", "regular", 1, True),
        ("NEWUSER", "new", 1, True),
        ("NEWUSER", "regular", 1, False),
        ("BOGUS", "regular", 500, False),
    ],
)
def test_apply_discount_return_value(code, customer, price, expected):
    order = Order([{"name": "X", "price": price, "quantity": 1, "weight": 0}], customer)
    assert order.apply_discount(code) is expected