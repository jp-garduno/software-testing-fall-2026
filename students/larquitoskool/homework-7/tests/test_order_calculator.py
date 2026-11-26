import pytest
import csv
import json
from src.order_calculator import Order

def load_order_test_data():
    """Load test data from CSV"""
    test_data = []
    with open('test_data/order_calculations.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse items JSON string
            items = json.loads(row['items'].replace("'", '"'))
            test_data.append((
                row['test_name'],
                items,
                row['customer_type'],
                row['discount_code'] if row['discount_code'] != 'NONE' else None,
                float(row['distance_km']),
                row['is_express'] == 'true',
                float(row['expected_subtotal']),
                float(row['expected_discount']),
                float(row['expected_tax']),
                float(row['expected_shipping']),
                float(row['expected_total'])
            ))
    return test_data

@pytest.mark.parametrize(
    "test_name,items,customer_type,discount_code,distance,is_express,"
    "exp_subtotal,exp_discount,exp_tax,exp_shipping,exp_total",
    load_order_test_data(),
    ids=lambda val: val if isinstance(val, str) and len(val) < 30 else ""
)
def test_order_calculation(test_name, items, customer_type, discount_code,
                           distance, is_express, exp_subtotal, exp_discount,
                           exp_tax, exp_shipping, exp_total):
    """Test order calculations with data from CSV"""
    # Create order
    order = Order(items, customer_type)

    # Apply discount if provided
    if discount_code:
        order.apply_discount(discount_code)

    # Set shipping
    order.set_shipping(distance, is_express)

    # Calculate
    result = order.calculate_total()

    # Verify all components
    assert result['subtotal'] == pytest.approx(exp_subtotal, rel=1e-2), \
        f"{test_name}: Subtotal mismatch"
    assert result['discount'] == pytest.approx(exp_discount, rel=1e-2), \
        f"{test_name}: Discount mismatch"
    assert result['tax'] == pytest.approx(exp_tax, rel=1e-2), \
        f"{test_name}: Tax mismatch"
    assert result['shipping'] == pytest.approx(exp_shipping, rel=1e-2), \
        f"{test_name}: Shipping mismatch"
    assert result['total'] == pytest.approx(exp_total, rel=1e-2), \
        f"{test_name}: Total mismatch"