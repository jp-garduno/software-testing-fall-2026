# Parameterized Tests

## Overview

Parameterized tests allow you to run the same test function multiple times with different input values. This is the foundation of data-driven testing.

## Python: pytest.mark.parametrize

### Basic Usage

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square(input, expected):
    assert input ** 2 == expected
```

**Output**:

```
test_math.py::test_square[2-4] PASSED
test_math.py::test_square[3-9] PASSED
test_math.py::test_square[4-16] PASSED
```

### Multiple Parameters

```python
@pytest.mark.parametrize("base,exponent,expected", [
    (2, 2, 4),
    (2, 3, 8),
    (3, 2, 9),
    (5, 0, 1),
])
def test_power(base, exponent, expected):
    assert base ** exponent == expected
```

### Single Parameter (List)

```python
@pytest.mark.parametrize("number", [1, 2, 3, 4, 5])
def test_positive(number):
    assert number > 0
```

### Named Test IDs

```python
@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("invalid", False),
    ("@example.com", False),
], ids=["valid_email", "missing_domain", "missing_local"])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected
```

**Output**:

```
test_email.py::test_email_validation[valid_email] PASSED
test_email.py::test_email_validation[missing_domain] PASSED
test_email.py::test_email_validation[missing_local] PASSED
```

### Complex Objects as Parameters

```python
@pytest.mark.parametrize("user", [
    {"name": "Alice", "age": 25, "role": "admin"},
    {"name": "Bob", "age": 30, "role": "user"},
    {"name": "Charlie", "age": 35, "role": "guest"},
])
def test_user_permissions(user):
    permissions = get_permissions(user)
    if user["role"] == "admin":
        assert "delete" in permissions
    elif user["role"] == "user":
        assert "edit" in permissions
    else:
        assert "view" in permissions
```

### Multiple Parametrize Decorators

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_add(x, y):
    assert x + y >= 2
```

This creates a **cartesian product**: 4 tests total (0+2, 0+3, 1+2, 1+3)

### Using pytest.param for Individual Test Configuration

```python
@pytest.mark.parametrize("value,expected", [
    (5, 25),
    (0, 0),
    pytest.param(-5, 25, marks=pytest.mark.xfail(reason="Negative not supported")),
])
def test_square_positive(value, expected):
    assert square_positive_only(value) == expected
```

### Parametrize with Fixtures

```python
@pytest.fixture
def database():
    db = Database()
    yield db
    db.close()

@pytest.mark.parametrize("user_id", [1, 2, 3])
def test_user_exists(database, user_id):
    assert database.user_exists(user_id)
```

## JavaScript: Jest test.each()

### Basic Usage

```javascript
test.each([
  [2, 4],
  [3, 9],
  [4, 16],
])("square of %i is %i", (input, expected) => {
  expect(input ** 2).toBe(expected);
});
```

**Output**:

```
✓ square of 2 is 4
✓ square of 3 is 9
✓ square of 4 is 16
```

### Table Syntax (Template Literals)

```javascript
test.each`
  base | exponent | expected
  ${2} | ${2}     | ${4}
  ${2} | ${3}     | ${8}
  ${3} | ${2}     | ${9}
  ${5} | ${0}     | ${1}
`(
  "$base raised to $exponent equals $expected",
  ({ base, exponent, expected }) => {
    expect(Math.pow(base, exponent)).toBe(expected);
  },
);
```

### Array of Objects

```javascript
test.each([
  { email: "user@example.com", valid: true },
  { email: "invalid", valid: false },
  { email: "@example.com", valid: false },
])("validates email: $email", ({ email, valid }) => {
  expect(isValidEmail(email)).toBe(valid);
});
```

### Using describe.each()

```javascript
describe.each([
  { name: "Alice", age: 25, role: "admin" },
  { name: "Bob", age: 30, role: "user" },
])("User: $name", (user) => {
  test("has correct permissions", () => {
    const permissions = getPermissions(user);
    if (user.role === "admin") {
      expect(permissions).toContain("delete");
    } else {
      expect(permissions).toContain("view");
    }
  });

  test("has valid age", () => {
    expect(user.age).toBeGreaterThan(0);
  });
});
```

### Single Parameter

```javascript
test.each([1, 2, 3, 4, 5])("number %i is positive", (number) => {
  expect(number).toBeGreaterThan(0);
});
```

### Asynchronous Tests

```javascript
test.each([
  [1, "user1"],
  [2, "user2"],
  [3, "user3"],
])("fetches user %i with name %s", async (id, expectedName) => {
  const user = await fetchUser(id);
  expect(user.name).toBe(expectedName);
});
```

## Loading Data from Files

### Python: CSV Data

```python
import csv
import pytest

def load_test_data(filename):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        return [
            (row['username'], row['password'], row['expected'])
            for row in reader
        ]

@pytest.mark.parametrize(
    "username,password,expected",
    load_test_data('test_login_data.csv')
)
def test_login(username, password, expected):
    result = login(username, password)
    assert result == expected
```

**test_login_data.csv**:

```csv
username,password,expected
admin,admin123,success
user,user123,success
hacker,wrongpass,failure
,empty,error
```

### Python: JSON Data

```python
import json
import pytest

def load_json_test_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return [(item['input'], item['expected']) for item in data]

@pytest.mark.parametrize(
    "input,expected",
    load_json_test_data('test_calculator.json')
)
def test_calculator(input, expected):
    result = calculate(input['operation'], input['a'], input['b'])
    assert result == expected
```

**test_calculator.json**:

```json
[
  {
    "input": { "operation": "add", "a": 2, "b": 3 },
    "expected": 5
  },
  {
    "input": { "operation": "subtract", "a": 5, "b": 3 },
    "expected": 2
  }
]
```

### JavaScript: JSON Data

```javascript
const testData = require("./test_login_data.json");

test.each(testData)(
  "login with username=$username",
  ({ username, password, expected }) => {
    const result = login(username, password);
    expect(result).toBe(expected);
  },
);
```

**test_login_data.json**:

```json
[
  { "username": "admin", "password": "admin123", "expected": "success" },
  { "username": "user", "password": "user123", "expected": "success" },
  { "username": "hacker", "password": "wrongpass", "expected": "failure" }
]
```

### JavaScript: Loading CSV (with csv-parse)

```javascript
const fs = require("fs");
const { parse } = require("csv-parse/sync");

const csvData = fs.readFileSync("test_data.csv", "utf8");
const records = parse(csvData, { columns: true });

test.each(records)(
  "test with $username",
  ({ username, password, expected }) => {
    expect(login(username, password)).toBe(expected);
  },
);
```

## Advanced Patterns

### Conditional Parametrization

```python
import sys
import pytest

test_data = [
    (1, 2),
    (2, 4),
]

if sys.platform == "win32":
    test_data.append((3, 6))  # Windows-specific test

@pytest.mark.parametrize("input,expected", test_data)
def test_platform_specific(input, expected):
    assert input * 2 == expected
```

### Parametrize from Environment

```python
import os
import pytest

# Load test data based on environment
env = os.getenv('TEST_ENV', 'dev')
test_data_file = f'test_data_{env}.json'

@pytest.mark.parametrize(
    "data",
    load_json_test_data(test_data_file)
)
def test_environment_specific(data):
    result = process(data)
    assert result is not None
```

### Combining Multiple Data Sources

```python
basic_tests = [(1, 2), (2, 4)]
edge_cases = [(0, 0), (-1, -2)]
from_file = load_json_test_data('extras.json')

all_test_data = basic_tests + edge_cases + from_file

@pytest.mark.parametrize("input,expected", all_test_data)
def test_comprehensive(input, expected):
    assert input * 2 == expected
```

## Best Practices

### 1. Use Descriptive Test IDs

❌ **Bad**:

```python
@pytest.mark.parametrize("a,b,c", [(1,2,3), (4,5,6)])
def test_something(a, b, c):
    pass
```

✅ **Good**:

```python
@pytest.mark.parametrize("a,b,c", [
    pytest.param(1, 2, 3, id="small_numbers"),
    pytest.param(4, 5, 6, id="medium_numbers"),
])
def test_something(a, b, c):
    pass
```

### 2. Keep Parameter Names Clear

❌ **Bad**:

```python
@pytest.mark.parametrize("x,y,z", [(1,2,3)])
def test_func(x, y, z):
    pass
```

✅ **Good**:

```python
@pytest.mark.parametrize("price,tax_rate,expected_total", [(100, 0.08, 108)])
def test_calculate_total(price, tax_rate, expected_total):
    pass
```

### 3. Group Related Test Data

```python
# Group logically
valid_emails = [
    "user@example.com",
    "test.user@example.co.uk",
]

invalid_emails = [
    "invalid",
    "@example.com",
    "user@",
]

@pytest.mark.parametrize("email", valid_emails)
def test_valid_emails(email):
    assert is_valid_email(email)

@pytest.mark.parametrize("email", invalid_emails)
def test_invalid_emails(email):
    assert not is_valid_email(email)
```

### 4. Don't Overuse Parametrization

❌ **When tests have different logic**:

```python
@pytest.mark.parametrize("type,data", [
    ("login", {"user": "admin"}),
    ("logout", {}),
    ("register", {"user": "new", "email": "new@example.com"}),
])
def test_actions(type, data):
    if type == "login":
        # Different logic
    elif type == "logout":
        # Different logic
    # This is hard to maintain!
```

✅ **Use separate tests**:

```python
def test_login():
    # Login logic

def test_logout():
    # Logout logic

def test_register():
    # Register logic
```

### 5. Use Fixtures with Parametrization

```python
@pytest.fixture
def api_client():
    client = APIClient()
    yield client
    client.close()

@pytest.mark.parametrize("endpoint,expected_status", [
    ("/users", 200),
    ("/products", 200),
    ("/orders", 200),
])
def test_api_endpoints(api_client, endpoint, expected_status):
    response = api_client.get(endpoint)
    assert response.status_code == expected_status
```

## Common Pitfalls

### 1. Shared State Between Tests

❌ **Problematic**:

```python
shared_list = []

@pytest.mark.parametrize("item", [1, 2, 3])
def test_append(item):
    shared_list.append(item)  # Tests affect each other!
    assert len(shared_list) == 1  # This will fail!
```

✅ **Fixed**:

```python
@pytest.mark.parametrize("item", [1, 2, 3])
def test_append(item):
    my_list = []  # Fresh state per test
    my_list.append(item)
    assert len(my_list) == 1
```

### 2. Complex Test Data Inline

❌ **Hard to read**:

```python
@pytest.mark.parametrize("data", [
    {"user": {"name": "Alice", "details": {"age": 25, "address": {"street": "123 Main", "city": "NYC"}}}},
    # More complex nested data...
])
```

✅ **Use external files**:

```python
@pytest.mark.parametrize("data", load_json_data('user_data.json'))
```

## Summary

**Python (pytest)**:

- Use `@pytest.mark.parametrize()`
- Support for IDs, fixtures, multiple decorators
- Easy integration with CSV/JSON

**JavaScript (Jest)**:

- Use `test.each()` or `describe.each()`
- Table syntax for readability
- Works with async tests

**Key Takeaways**:

- Parameterized tests reduce duplication
- Use clear parameter names and IDs
- Load complex data from files
- Don't overuse - sometimes separate tests are clearer

## Next Steps

- [03: Test Data Management](./03-test-data-management.md) - Organizing and managing test data
- [04: Best Practices](./04-best-practices.md) - Patterns and anti-patterns
