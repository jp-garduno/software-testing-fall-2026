import pytest
import json
from src.customer_validator import CustomerValidator

def load_customer_test_data():
    """Load test data from JSON"""
    with open('test_data/customer_validation.json', 'r') as f:
        data = json.load(f)
        return [(item['test_name'], item['customer'], item['expected']) for item in data]

@pytest.mark.parametrize(
    "test_name, customer, expected", 
    load_customer_test_data(),
    ids=lambda val: val if isinstance(val, str) else ""
)
def test_customer_validation(test_name, customer, expected):
    """Test customer validation with data from JSON"""
    validator = CustomerValidator()
    result = validator.validate(customer)
    
    assert result['is_valid'] == expected['is_valid'], f"{test_name}: Validation status mismatch"
    assert set(result['errors']) == set(expected['errors']), f"{test_name}: Error messages mismatch"