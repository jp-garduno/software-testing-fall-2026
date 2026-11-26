import pytest
import json
from src.order_calculator import Order

def load_comparison_data():
    with open('test_data/comparison_data.json', 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_comparison_data(), ids=lambda d: d["test_name"])
def test_order_data_driven(data):
    """Same 10 tests using parameterization"""
    order = Order(data["items"], data["customer_type"])
    
    if data["discount_code"]:
        order.apply_discount(data["discount_code"])
        
    order.set_shipping(data["distance_km"], data["is_express"])
    
    assert order.calculate_total()['total'] == pytest.approx(data["expected_total"], rel=1e-2)