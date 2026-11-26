import pytest
from shipping import calculate_shipping

@pytest.mark.parametrize(
    "weight,distance,is_express,expected",
    [
        pytest.param(1, 5, False, 1.00, id="light-short-standard"),
        pytest.param(1, 5, True, 1.50, id="light-short-express"),
        pytest.param(3, 20, False, 3.50, id="medium-medium-standard"),
        pytest.param(3, 20, True, 5.25, id="medium-medium-express"),
        pytest.param(8, 50, False, 9.00, id="heavy-medium-standard"),
        pytest.param(8, 50, True, 13.50, id="heavy-medium-express"),
        pytest.param(10, 100, False, 15.00, id="heavy-long-standard"),
        pytest.param(10, 100, True, 22.50, id="heavy-long-express"),
        pytest.param(0.5, 5, True, 1.13, id="express-rounds-half-up"),
        pytest.param(100000000, 5000000000, False, 1000000000, id="superHeavy-rounds-standard"),
    ],
    #base_cost = weight * 0.5 + distance * 0.1
)
def test_calculate_shipping(weight, distance, is_express, expected):
    assert calculate_shipping(weight, distance, is_express) == expected


@pytest.mark.parametrize(
    "weight,distance",
    [
        pytest.param(-1, 10, id="negative-weight"),
        pytest.param(1, -10, id="negative-distance"),
        pytest.param(0, 10, id="zero-weight"),
        pytest.param(1, 0, id="zero-distance"),
    ],
)
def test_calculate_shipping_rejects_nonpositive_measurements(weight, distance):
    with pytest.raises(ValueError):
        calculate_shipping(weight, distance)