# Data-Driven Testing: Best Practices

## Design Patterns

### 1. Separate Data from Logic

✅ **Good: Clear Separation**

```python
# test_calculator.py
@pytest.mark.parametrize("a,b,expected", load_json_data('test_data/calculator.json'))
def test_add(a, b, expected):
    assert add(a, b) == expected

# test_data/calculator.json
[
    {"a": 2, "b": 3, "expected": 5},
    {"a": -1, "b": 1, "expected": 0}
]
```

❌ **Bad: Mixed Logic and Data**

```python
def test_add():
    test_cases = [(2, 3, 5), (-1, 1, 0)]
    for a, b, expected in test_cases:
        if a < 0:
            # Special logic for negative numbers
            result = special_add(a, b)
        else:
            result = add(a, b)
        assert result == expected
```

### 2. Single Responsibility Per Test

✅ **Good: One Concern**

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid", False),
])
def test_email_format(email, valid):
    assert is_valid_email(email) == valid

@pytest.mark.parametrize("email,deliverable", [
    ("user@gmail.com", True),
    ("user@fake-domain-xyz.com", False),
])
def test_email_deliverability(email, deliverable):
    assert can_deliver_to(email) == deliverable
```

❌ **Bad: Multiple Concerns**

```python
@pytest.mark.parametrize("email,format_valid,deliverable", [
    ("user@gmail.com", True, True),
    ("invalid", False, False),
])
def test_email_everything(email, format_valid, deliverable):
    assert is_valid_email(email) == format_valid
    assert can_deliver_to(email) == deliverable  # Different concern!
```

### 3. Use Page Object Pattern (UI Testing)

✅ **Good: Reusable Page Objects**

```python
# pages/login_page.py
class LoginPage:
    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_submit()
        return self.get_result()

# test_login.py
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", "success"),
    ("user", "wrong", "failure"),
])
def test_login(username, password, expected, login_page):
    result = login_page.login(username, password)
    assert result == expected
```

### 4. Data Builders for Complex Objects

```python
class UserBuilder:
    def __init__(self):
        self.user = {
            "username": "default",
            "email": "default@example.com",
            "role": "user",
            "active": True
        }

    def with_username(self, username):
        self.user["username"] = username
        return self

    def as_admin(self):
        self.user["role"] = "admin"
        return self

    def inactive(self):
        self.user["active"] = False
        return self

    def build(self):
        return self.user.copy()

# Test data generation
test_users = [
    UserBuilder().with_username("alice").as_admin().build(),
    UserBuilder().with_username("bob").build(),
    UserBuilder().with_username("inactive_user").inactive().build(),
]

@pytest.mark.parametrize("user", test_users)
def test_user_creation(user):
    response = create_user(**user)
    assert response.status_code == 201
```

## Naming Conventions

### Test Names

✅ **Good: Descriptive Names**

```python
@pytest.mark.parametrize("age,discount", [
    (65, 0.10),  # Senior discount
    (5, 0.50),   # Child discount
    (30, 0),     # No discount
], ids=["senior_discount", "child_discount", "no_discount"])
def test_age_based_discount(age, discount):
    assert calculate_discount(age) == discount
```

❌ **Bad: Generic Names**

```python
@pytest.mark.parametrize("x,y", [(65, 0.10), (5, 0.50), (30, 0)])
def test_discount(x, y):
    assert calculate_discount(x) == y
```

### Data File Names

✅ **Good**:

- `valid_credit_cards.csv`
- `boundary_value_test_cases.json`
- `api_error_responses.yaml`
- `login_credentials_success.csv`

❌ **Bad**:

- `data.csv`
- `test1.json`
- `stuff.yaml`
- `temp.csv`

### Parameter Names

✅ **Good**:

```python
@pytest.mark.parametrize("price,tax_rate,expected_total", [...])
def test_calculate_total(price, tax_rate, expected_total):
    pass
```

❌ **Bad**:

```python
@pytest.mark.parametrize("x,y,z", [...])
def test_calc(x, y, z):
    pass
```

## Data Organization

### Group Related Data

```python
# valid_logins.csv
username,password,expected
admin,admin123,success
user,user123,success

# invalid_logins.csv
username,password,expected
hacker,wrongpass,failure
,empty,error
admin,,error

@pytest.mark.parametrize("username,password,expected",
                         load_csv_data('test_data/valid_logins.csv'))
def test_valid_logins(username, password, expected):
    assert login(username, password) == expected

@pytest.mark.parametrize("username,password,expected",
                         load_csv_data('test_data/invalid_logins.csv'))
def test_invalid_logins(username, password, expected):
    assert login(username, password) == expected
```

### Use Hierarchical Structure

```
test_data/
├── authentication/
│   ├── valid_credentials.json
│   ├── invalid_credentials.json
│   └── edge_cases.json
├── products/
│   ├── valid_products.csv
│   ├── out_of_stock.csv
│   └── pricing_tiers.json
└── shared/
    ├── countries.json
    └── currencies.json
```

## Error Handling

### Handle Missing Data Gracefully

```python
def load_test_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)

        # Validate data structure
        if not isinstance(data, list):
            raise ValueError(f"Expected list, got {type(data)}")

        return data

    except FileNotFoundError:
        pytest.fail(f"Test data file not found: {filename}")

    except json.JSONDecodeError as e:
        pytest.fail(f"Invalid JSON in {filename}: {e}")
```

### Validate Data Schema

```python
from jsonschema import validate, ValidationError

schema = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["username", "password", "expected"],
        "properties": {
            "username": {"type": "string"},
            "password": {"type": "string"},
            "expected": {"type": "string"}
        }
    }
}

def load_validated_data(filename):
    data = load_json_data(filename)
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        pytest.fail(f"Invalid data structure: {e.message}")
    return data
```

### Meaningful Error Messages

✅ **Good**:

```python
@pytest.mark.parametrize("price,discount,expected", test_data)
def test_discount_calculation(price, discount, expected):
    result = calculate_discounted_price(price, discount)
    assert result == expected, \
        f"Failed for price=${price}, discount={discount*100}%. " \
        f"Expected ${expected}, got ${result}"
```

❌ **Bad**:

```python
def test_discount(price, discount, expected):
    assert calculate_discounted_price(price, discount) == expected  # What failed?
```

## Performance Optimization

### Lazy Loading for Large Datasets

```python
def load_large_dataset():
    """Generator to avoid loading all data at once"""
    with open('large_test_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield (row['input'], row['expected'])

@pytest.mark.parametrize("input,expected", load_large_dataset())
def test_with_large_dataset(input, expected):
    assert process(input) == expected
```

### Cache Loaded Data

```python
import functools

@functools.lru_cache(maxsize=None)
def load_test_data_cached(filename):
    """Load once, reuse for all tests"""
    with open(filename, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_test_data_cached('test_data.json'))
def test_something(data):
    pass
```

### Limit Test Data Size

```python
# Load only first N test cases for quick feedback
def load_test_data(filename, limit=None):
    data = load_json_data(filename)
    if limit and os.getenv('QUICK_TEST'):
        return data[:limit]
    return data

# Run with: QUICK_TEST=1 pytest test_file.py
@pytest.mark.parametrize("data", load_test_data('large_dataset.json', limit=10))
def test_quick(data):
    pass
```

## Maintainability

### Document Test Data

```json
{
  "_comment": "Login test scenarios",
  "_author": "Test Team",
  "_last_updated": "2026-08-04",
  "_description": "Covers valid, invalid, and edge case login scenarios",
  "test_cases": [
    {
      "name": "valid_admin_login",
      "description": "Admin user with correct credentials",
      "username": "admin",
      "password": "admin123",
      "expected": "success"
    }
  ]
}
```

### Use Constants for Reusable Values

```python
# test_constants.py
VALID_EMAIL = "user@example.com"
INVALID_EMAIL = "not-an-email"
ADMIN_ROLE = "admin"
USER_ROLE = "user"

# test_users.py
from test_constants import VALID_EMAIL, ADMIN_ROLE

test_data = [
    {"email": VALID_EMAIL, "role": ADMIN_ROLE, "expected": 201},
]
```

### Version Test Data

```json
{
  "version": "2.0",
  "changelog": [
    "2.0: Added new user roles (admin, moderator, guest)",
    "1.1: Fixed email validation test cases",
    "1.0: Initial test data"
  ],
  "test_cases": [...]
}
```

## Testing Strategies

### Equivalence Partitioning with DDT

```python
# Group test data by equivalence classes
valid_ages = [18, 25, 30, 65]  # All should behave the same
invalid_ages = [-1, 0, 17]      # All should fail
boundary_ages = [17, 18, 64, 65]  # Test boundaries

@pytest.mark.parametrize("age", valid_ages)
def test_valid_age(age):
    assert is_valid_age(age)

@pytest.mark.parametrize("age", invalid_ages)
def test_invalid_age(age):
    assert not is_valid_age(age)

@pytest.mark.parametrize("age", boundary_ages)
def test_boundary_age(age):
    result = is_valid_age(age)
    assert result == (age >= 18)
```

### Combinatorial Testing

```python
from itertools import product

# Test all combinations
browsers = ['chrome', 'firefox', 'safari']
devices = ['desktop', 'mobile', 'tablet']
locales = ['en', 'es', 'fr']

test_combinations = list(product(browsers, devices, locales))

@pytest.mark.parametrize("browser,device,locale", test_combinations)
def test_compatibility(browser, device, locale):
    result = render_page(browser, device, locale)
    assert result.status == 200
```

### Risk-Based Test Data Selection

```python
# Prioritize high-risk scenarios
high_risk_data = load_json_data('high_risk_scenarios.json')
medium_risk_data = load_json_data('medium_risk_scenarios.json')
low_risk_data = load_json_data('low_risk_scenarios.json')

# Always run high risk
@pytest.mark.critical
@pytest.mark.parametrize("data", high_risk_data)
def test_critical_scenarios(data):
    pass

# Run medium risk in CI
@pytest.mark.parametrize("data", medium_risk_data)
def test_important_scenarios(data):
    pass

# Run low risk nightly
@pytest.mark.slow
@pytest.mark.parametrize("data", low_risk_data)
def test_comprehensive_scenarios(data):
    pass
```

## Common Anti-Patterns

### ❌ Anti-Pattern 1: Over-Parameterization

```python
# Too many parameters - hard to understand
@pytest.mark.parametrize("a,b,c,d,e,f,g,h,expected", [
    (1,2,3,4,5,6,7,8,36),
])
def test_complex(a,b,c,d,e,f,g,h,expected):
    pass
```

✅ **Better**:

```python
@pytest.mark.parametrize("values,expected", [
    ([1,2,3,4,5,6,7,8], 36),
])
def test_sum(values, expected):
    assert sum(values) == expected
```

### ❌ Anti-Pattern 2: Logic in Tests

```python
@pytest.mark.parametrize("value,expected", [(1,2), (2,4), (3,6)])
def test_with_logic(value, expected):
    if value < 2:
        result = special_calc(value)
    else:
        result = normal_calc(value)
    assert result == expected
```

✅ **Better**:

```python
@pytest.mark.parametrize("value,expected", [(1,2)])
def test_special_case(value, expected):
    assert special_calc(value) == expected

@pytest.mark.parametrize("value,expected", [(2,4), (3,6)])
def test_normal_case(value, expected):
    assert normal_calc(value) == expected
```

### ❌ Anti-Pattern 3: Shared Mutable State

```python
results = []  # Shared state!

@pytest.mark.parametrize("value", [1,2,3])
def test_append(value):
    results.append(value)
    assert len(results) == 1  # Will fail!
```

✅ **Better**:

```python
@pytest.mark.parametrize("value", [1,2,3])
def test_append(value):
    results = []  # Fresh state per test
    results.append(value)
    assert len(results) == 1
```

### ❌ Anti-Pattern 4: Ignoring Failed Data

```python
@pytest.mark.parametrize("data", test_data)
def test_something(data):
    try:
        result = process(data)
        assert result == data['expected']
    except Exception:
        pass  # DON'T hide failures!
```

✅ **Better**:

```python
@pytest.mark.parametrize("data", test_data)
def test_something(data):
    result = process(data)
    assert result == data['expected']  # Let it fail properly
```

## CI/CD Integration

### Parallel Execution

```python
# pytest.ini
[pytest]
addopts = -n auto  # Run tests in parallel

# Or with specific count
# pytest -n 4 test_file.py
```

### Test Markers for Selective Execution

```python
@pytest.mark.smoke
@pytest.mark.parametrize("data", critical_test_data)
def test_critical(data):
    pass

@pytest.mark.regression
@pytest.mark.parametrize("data", full_test_data)
def test_comprehensive(data):
    pass

# Run only smoke tests
# pytest -m smoke

# Run everything except slow tests
# pytest -m "not slow"
```

### Environment-Specific Data

```python
import os

env = os.getenv('TEST_ENV', 'dev')
test_data = load_json_data(f'test_data_{env}.json')

@pytest.mark.parametrize("data", test_data)
def test_environment_specific(data):
    pass
```

## Summary

**Design Patterns**:

- Separate data from logic
- Single responsibility per test
- Use builders for complex data
- Page Object Pattern for UI

**Best Practices**:

- Descriptive names
- Group related data
- Validate data structure
- Handle errors gracefully
- Cache loaded data
- Document test data
- Version control

**Avoid**:

- Over-parameterization
- Logic in tests
- Shared mutable state
- Hiding failures
- Hardcoding sensitive data

**Remember**: Data-driven testing is about efficiency and maintainability. If adding data-driven testing makes tests harder to understand, reconsider your approach.

## Next Steps

- Complete [Homework 7](../homework/homework-7.md)
- Practice with [exercises](../exercises/)
- Preview [Module 8: System Level Testing](../../08-system-level-testing/README.md)
