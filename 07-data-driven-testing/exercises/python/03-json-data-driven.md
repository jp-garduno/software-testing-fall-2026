# Exercise 3: JSON Data-Driven Testing (Python)

## Objective

Learn to use JSON files for complex, nested test data in data-driven testing.

## Scenario: API Testing

You are testing a REST API with various endpoints. Test data includes request parameters, expected responses, and validation rules.

## Part 1: Product API Testing

**product_api.py**:

```python
class Product:
    def __init__(self, id, name, price, category, in_stock):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
        self.in_stock = in_stock

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "in_stock": self.in_stock
        }

class ProductAPI:
    def __init__(self):
        self.products = {}
        self.next_id = 1

    def create_product(self, name, price, category, in_stock=True):
        """Create a new product"""
        if not name or price < 0:
            return {"status": 400, "error": "Invalid input"}

        product = Product(self.next_id, name, price, category, in_stock)
        self.products[self.next_id] = product
        self.next_id += 1

        return {"status": 201, "data": product.to_dict()}

    def get_product(self, product_id):
        """Get product by ID"""
        if product_id not in self.products:
            return {"status": 404, "error": "Product not found"}

        return {"status": 200, "data": self.products[product_id].to_dict()}

    def search_products(self, category=None, max_price=None):
        """Search products by criteria"""
        results = list(self.products.values())

        if category:
            results = [p for p in results if p.category == category]

        if max_price is not None:
            results = [p for p in results if p.price <= max_price]

        return {
            "status": 200,
            "data": [p.to_dict() for p in results],
            "count": len(results)
        }
```

**test_data/product_api_tests.json**:

```json
{
  "create_product_tests": [
    {
      "name": "create_valid_product",
      "input": {
        "name": "Laptop",
        "price": 999.99,
        "category": "Electronics",
        "in_stock": true
      },
      "expected": {
        "status": 201,
        "data_contains": {
          "name": "Laptop",
          "price": 999.99,
          "category": "Electronics"
        }
      }
    },
    {
      "name": "create_product_invalid_price",
      "input": {
        "name": "Invalid Product",
        "price": -10,
        "category": "Test",
        "in_stock": true
      },
      "expected": {
        "status": 400,
        "error": "Invalid input"
      }
    },
    {
      "name": "create_product_empty_name",
      "input": {
        "name": "",
        "price": 50,
        "category": "Test",
        "in_stock": true
      },
      "expected": {
        "status": 400,
        "error": "Invalid input"
      }
    }
  ],
  "search_product_tests": [
    {
      "name": "search_by_category",
      "setup": [
        { "name": "Laptop", "price": 1000, "category": "Electronics" },
        { "name": "Phone", "price": 500, "category": "Electronics" },
        { "name": "Desk", "price": 300, "category": "Furniture" }
      ],
      "search_params": {
        "category": "Electronics"
      },
      "expected": {
        "status": 200,
        "count": 2
      }
    },
    {
      "name": "search_by_max_price",
      "setup": [
        { "name": "Item1", "price": 100, "category": "Test" },
        { "name": "Item2", "price": 500, "category": "Test" },
        { "name": "Item3", "price": 1000, "category": "Test" }
      ],
      "search_params": {
        "max_price": 500
      },
      "expected": {
        "status": 200,
        "count": 2
      }
    }
  ]
}
```

**test_product_api.py**:

```python
import pytest
import json
import os
from product_api import ProductAPI

def load_json_test_data(filename):
    """Load test data from JSON file"""
    json_path = os.path.join(os.path.dirname(__file__), 'test_data', filename)
    with open(json_path, 'r') as f:
        return json.load(f)

# Load all test data
test_data = load_json_test_data('product_api_tests.json')

@pytest.mark.parametrize(
    "test_case",
    test_data['create_product_tests'],
    ids=lambda tc: tc['name']
)
def test_create_product(test_case):
    """Test product creation with JSON test data"""
    api = ProductAPI()

    # Execute
    result = api.create_product(**test_case['input'])

    # Verify status
    assert result['status'] == test_case['expected']['status']

    # Verify response data if success
    if 'data_contains' in test_case['expected']:
        for key, value in test_case['expected']['data_contains'].items():
            assert result['data'][key] == value

    # Verify error message if failure
    if 'error' in test_case['expected']:
        assert test_case['expected']['error'] in result['error']

@pytest.mark.parametrize(
    "test_case",
    test_data['search_product_tests'],
    ids=lambda tc: tc['name']
)
def test_search_products(test_case):
    """Test product search with JSON test data"""
    api = ProductAPI()

    # Setup: Create products
    for product_data in test_case['setup']:
        api.create_product(**product_data)

    # Execute search
    result = api.search_products(**test_case['search_params'])

    # Verify
    assert result['status'] == test_case['expected']['status']
    assert result['count'] == test_case['expected']['count']
```

## Part 2: User Profile API

### Task

Create JSON test data for a user profile API that handles nested objects.

**test_data/user_profile_tests.json**:

```json
{
  "update_profile_tests": [
    {
      "name": "update_basic_info",
      "user_id": 1,
      "updates": {
        "name": "Alice Updated",
        "email": "alice.new@example.com"
      },
      "expected": {
        "status": 200,
        "updated_fields": ["name", "email"]
      }
    },
    {
      "name": "update_address",
      "user_id": 1,
      "updates": {
        "address": {
          "street": "123 Main St",
          "city": "New York",
          "country": "USA",
          "zipcode": "10001"
        }
      },
      "expected": {
        "status": 200,
        "updated_fields": ["address"]
      }
    },
    {
      "name": "update_preferences",
      "user_id": 1,
      "updates": {
        "preferences": {
          "newsletter": true,
          "notifications": {
            "email": true,
            "sms": false,
            "push": true
          },
          "theme": "dark"
        }
      },
      "expected": {
        "status": 200,
        "updated_fields": ["preferences"]
      }
    }
  ]
}
```

### Requirements

1. Implement `user_profile_api.py` with methods:

   - `create_user(name, email)`
   - `update_profile(user_id, updates)`
   - `get_profile(user_id)`

2. Support nested updates (address, preferences)

3. Create JSON test data with at least 10 test cases

4. Implement tests that verify nested object updates

## Part 3: Validation Rules from JSON

### Task

Load validation rules from JSON and test them dynamically.

**test_data/validation_rules.json**:

```json
{
  "email_validation": {
    "rule": "must_match_regex",
    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
    "test_cases": [
      { "input": "valid@example.com", "expected": true },
      { "input": "invalid@", "expected": false },
      { "input": "@example.com", "expected": false }
    ]
  },
  "password_validation": {
    "rule": "must_meet_criteria",
    "criteria": {
      "min_length": 8,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_number": true,
      "require_special": false
    },
    "test_cases": [
      { "input": "Password123", "expected": true },
      { "input": "pass", "expected": false, "reason": "too_short" },
      { "input": "password123", "expected": false, "reason": "no_uppercase" },
      { "input": "PASSWORD123", "expected": false, "reason": "no_lowercase" }
    ]
  },
  "age_validation": {
    "rule": "must_be_in_range",
    "min": 13,
    "max": 120,
    "test_cases": [
      { "input": 25, "expected": true },
      { "input": 10, "expected": false },
      { "input": 13, "expected": true },
      { "input": 120, "expected": true },
      { "input": 121, "expected": false }
    ]
  }
}
```

**test_validation_rules.py**:

```python
import pytest
import json
import re

def load_validation_rules():
    """Load validation rules from JSON"""
    with open('test_data/validation_rules.json', 'r') as f:
        return json.load(f)

def validate_by_rule(rule_config, input_value):
    """Dynamically validate based on rule configuration"""
    rule_type = rule_config['rule']

    if rule_type == 'must_match_regex':
        pattern = rule_config['pattern']
        return bool(re.match(pattern, str(input_value)))

    elif rule_type == 'must_be_in_range':
        return rule_config['min'] <= input_value <= rule_config['max']

    elif rule_type == 'must_meet_criteria':
        criteria = rule_config['criteria']
        # Implement password criteria validation
        # TODO: Implement
        pass

    return False

# Generate test cases from JSON
validation_rules = load_validation_rules()

def generate_test_cases():
    """Generate pytest parameters from validation rules JSON"""
    test_cases = []

    for field_name, rule_config in validation_rules.items():
        for test_case in rule_config['test_cases']:
            test_cases.append((
                field_name,
                rule_config,
                test_case['input'],
                test_case['expected']
            ))

    return test_cases

@pytest.mark.parametrize(
    "field,rule,input_value,expected",
    generate_test_cases(),
    ids=lambda val: str(val)[:30] if isinstance(val, (str, int)) else ""
)
def test_validation_rules(field, rule, input_value, expected):
    """Test validation rules loaded from JSON"""
    result = validate_by_rule(rule, input_value)
    assert result == expected, f"Validation failed for {field} with input {input_value}"
```

## Expected Output

```bash
$ pytest test_product_api.py -v

test_product_api.py::test_create_product[create_valid_product] PASSED
test_product_api.py::test_create_product[create_product_invalid_price] PASSED
test_product_api.py::test_create_product[create_product_empty_name] PASSED
test_product_api.py::test_search_products[search_by_category] PASSED
test_product_api.py::test_search_products[search_by_max_price] PASSED

==================== 5 passed in 0.05s ====================
```

## Tips

1. Use `json.load()` to parse JSON files
2. Handle nested dictionaries with care
3. Use list comprehensions for filtering test data
4. Validate JSON structure before using
5. Use descriptive test case names in JSON

## Submission

Submit:

- All Python modules
- All test files
- All JSON files in `test_data/` directory
- README documenting JSON structure
- Screenshot of passing tests

## Grading Criteria

- Implementation correctness: 35%
- JSON test data quality: 30%
- Test coverage: 25%
- Code quality: 10%
