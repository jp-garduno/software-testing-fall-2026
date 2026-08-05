# Test Data Management

## Overview

Effective test data management is crucial for maintaining scalable and maintainable test suites. This guide covers strategies for organizing, loading, and managing test data.

## Test Data Sources

### 1. Inline Data

**When to use**: Small datasets, quick tests, data that's closely tied to test logic

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid@", False),
])
def test_email_validation(email, valid):
    assert is_valid_email(email) == valid
```

**Pros**:

- Easy to see data at a glance
- No file I/O overhead
- Good for code reviews

**Cons**:

- Clutters test files
- Hard to maintain large datasets
- Non-technical users can't edit

### 2. CSV Files

**When to use**: Tabular data, simple structure, Excel-friendly

**test_users.csv**:

```csv
username,password,email,role,expected_status
alice,pass123,alice@example.com,admin,201
bob,pass456,bob@example.com,user,201
charlie,,charlie@example.com,user,400
```

**Python**:

```python
import csv
import pytest

def load_csv_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [
            (row['username'], row['password'], row['email'],
             row['role'], int(row['expected_status']))
            for row in reader
        ]

@pytest.mark.parametrize(
    "username,password,email,role,expected",
    load_csv_data('test_data/test_users.csv')
)
def test_create_user(username, password, email, role, expected):
    response = create_user(username, password, email, role)
    assert response.status_code == expected
```

**JavaScript**:

```javascript
const fs = require("fs");
const { parse } = require("csv-parse/sync");

const records = parse(fs.readFileSync("test_data/test_users.csv"), {
  columns: true,
});

test.each(records)(
  "creates user $username",
  ({ username, password, email, role, expected_status }) => {
    const response = createUser(username, password, email, role);
    expect(response.statusCode).toBe(parseInt(expected_status));
  },
);
```

**Pros**:

- Simple format
- Excel/Google Sheets compatible
- Easy for non-programmers
- Lightweight

**Cons**:

- Limited to flat data
- No nested structures
- Type information lost (everything is string)

### 3. JSON Files

**When to use**: Complex nested data, API testing, hierarchical data

**test_api_requests.json**:

```json
[
  {
    "name": "create_user_success",
    "request": {
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "username": "alice",
        "email": "alice@example.com",
        "profile": {
          "age": 25,
          "address": {
            "city": "NYC",
            "country": "USA"
          }
        }
      }
    },
    "expected": {
      "status": 201,
      "body": {
        "id": "uuid",
        "username": "alice"
      }
    }
  }
]
```

**Python**:

```python
import json
import pytest

def load_json_data(filename):
    with open(filename, 'r') as f:
        return json.load(f)

@pytest.mark.parametrize(
    "test_case",
    load_json_data('test_data/test_api_requests.json'),
    ids=lambda tc: tc['name']
)
def test_api_request(test_case):
    response = make_request(
        test_case['request']['method'],
        test_case['request']['endpoint'],
        test_case['request']['body']
    )
    assert response.status_code == test_case['expected']['status']
```

**JavaScript**:

```javascript
const testCases = require("./test_data/test_api_requests.json");

test.each(testCases)("$name", async ({ request, expected }) => {
  const response = await makeRequest(
    request.method,
    request.endpoint,
    request.body,
  );
  expect(response.status).toBe(expected.status);
});
```

**Pros**:

- Supports nested data
- Preserves types (numbers, booleans)
- Standard format
- Good for APIs

**Cons**:

- Harder for non-programmers
- No comments (use YAML for that)
- Can become verbose

### 4. YAML Files

**When to use**: Configuration-like data, need comments, complex scenarios

**test_config.yaml**:

```yaml
# Authentication test scenarios
auth_tests:
  - name: valid_admin_login
    user:
      username: admin
      password: admin123
      role: admin
    expected:
      status: 200
      permissions: [read, write, delete]

  - name: valid_user_login
    user:
      username: user
      password: user123
      role: user
    expected:
      status: 200
      permissions: [read]
```

**Python**:

```python
import yaml
import pytest

def load_yaml_data(filename):
    with open(filename, 'r') as f:
        data = yaml.safe_load(f)
        return data['auth_tests']

@pytest.mark.parametrize(
    "test_case",
    load_yaml_data('test_data/test_config.yaml'),
    ids=lambda tc: tc['name']
)
def test_authentication(test_case):
    response = login(test_case['user']['username'],
                    test_case['user']['password'])
    assert response.status_code == test_case['expected']['status']
```

**Pros**:

- Human-readable
- Supports comments
- Good for config
- Less verbose than JSON

**Cons**:

- Requires yaml library
- Indentation-sensitive
- Less universal than JSON

### 5. Excel Files

**When to use**: Large datasets, business users manage data, multiple test suites

**Python (using openpyxl)**:

```python
import openpyxl
import pytest

def load_excel_data(filename, sheet_name):
    workbook = openpyxl.load_workbook(filename)
    sheet = workbook[sheet_name]

    headers = [cell.value for cell in sheet[1]]
    data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(dict(zip(headers, row)))

    return data

@pytest.mark.parametrize(
    "test_data",
    load_excel_data('test_data.xlsx', 'UserTests'),
    ids=lambda d: d['test_name']
)
def test_from_excel(test_data):
    result = process_user(test_data['username'], test_data['email'])
    assert result == test_data['expected']
```

**Pros**:

- Business users comfortable with Excel
- Multiple sheets for organization
- Can include formulas
- Large dataset support

**Cons**:

- Binary format (not git-friendly)
- Requires additional libraries
- Slower to load
- Can't diff easily

### 6. Database

**When to use**: Production-like data, large datasets, shared test data

**Python**:

```python
import pytest
import sqlite3

def load_test_data_from_db():
    conn = sqlite3.connect('test_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, email, expected_status FROM test_users')
    data = cursor.fetchall()
    conn.close()
    return data

@pytest.mark.parametrize(
    "username,email,expected",
    load_test_data_from_db()
)
def test_user_from_db(username, email, expected):
    result = create_user(username, email)
    assert result.status_code == expected
```

**Pros**:

- Production-like
- Query capabilities
- Large datasets
- Shared across teams

**Cons**:

- Requires database setup
- More complex
- Slower than files
- Need connection management

## Organizing Test Data

### Directory Structure

```
tests/
├── test_users.py
├── test_products.py
└── test_data/
    ├── users/
    │   ├── valid_users.csv
    │   ├── invalid_users.csv
    │   └── edge_cases.json
    ├── products/
    │   ├── product_catalog.json
    │   └── pricing_data.csv
    └── shared/
        ├── countries.json
        └── currencies.json
```

### Naming Conventions

**Good names**:

- `valid_login_credentials.csv`
- `boundary_value_test_cases.json`
- `api_error_responses.yaml`

**Bad names**:

- `data.csv`
- `test.json`
- `stuff.yaml`

### Data File Structure Best Practices

#### Include Metadata

```json
{
  "metadata": {
    "version": "1.0",
    "created": "2026-08-04",
    "description": "Login test scenarios including edge cases",
    "author": "Test Team"
  },
  "test_data": [
    {
      "username": "admin",
      "password": "admin123",
      "expected": "success"
    }
  ]
}
```

#### Use Descriptive Keys

❌ **Bad**:

```json
{ "u": "admin", "p": "pass", "e": 200 }
```

✅ **Good**:

```json
{ "username": "admin", "password": "pass", "expected_status": 200 }
```

## Data Fixtures and Factories

### Pytest Fixtures for Test Data

```python
import pytest

@pytest.fixture
def valid_users():
    return [
        {"username": "alice", "email": "alice@example.com"},
        {"username": "bob", "email": "bob@example.com"},
    ]

@pytest.fixture
def invalid_users():
    return [
        {"username": "", "email": "empty@example.com"},
        {"username": "test", "email": "invalid"},
    ]

def test_with_valid_users(valid_users):
    for user in valid_users:
        assert create_user(user['username'], user['email']) == 201

def test_with_invalid_users(invalid_users):
    for user in invalid_users:
        assert create_user(user['username'], user['email']) == 400
```

### Factory Pattern for Test Data

**Python (using Factory Boy)**:

```python
import factory

class UserFactory(factory.Factory):
    class Meta:
        model = dict

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=80)

# Generate test data
@pytest.mark.parametrize("user", [UserFactory() for _ in range(10)])
def test_create_user(user):
    response = create_user(user['username'], user['email'], user['age'])
    assert response.status_code == 201
```

### Builder Pattern

```python
class TestDataBuilder:
    def __init__(self):
        self.data = {
            'username': 'default_user',
            'email': 'user@example.com',
            'role': 'user'
        }

    def with_username(self, username):
        self.data['username'] = username
        return self

    def with_email(self, email):
        self.data['email'] = email
        return self

    def as_admin(self):
        self.data['role'] = 'admin'
        return self

    def build(self):
        return self.data.copy()

# Usage
test_data = [
    TestDataBuilder().with_username('alice').as_admin().build(),
    TestDataBuilder().with_username('bob').build(),
]

@pytest.mark.parametrize("user_data", test_data)
def test_user(user_data):
    result = create_user(**user_data)
    assert result.status_code == 201
```

## Environment-Specific Test Data

### Loading Based on Environment

```python
import os
import pytest

def get_test_data_file():
    env = os.getenv('TEST_ENV', 'dev')
    return f'test_data_{env}.json'

@pytest.mark.parametrize(
    "test_case",
    load_json_data(get_test_data_file())
)
def test_environment_specific(test_case):
    # Test uses environment-specific data
    pass
```

### Configuration Files

**config.yaml**:

```yaml
environments:
  dev:
    api_url: https://dev.api.example.com
    test_data: test_data_dev.json
  staging:
    api_url: https://staging.api.example.com
    test_data: test_data_staging.json
  prod:
    api_url: https://api.example.com
    test_data: test_data_prod.json
```

## Data Privacy and Security

### Anonymizing Test Data

```python
def anonymize_user_data(users):
    """Remove sensitive information from production data"""
    return [
        {
            'username': f"user_{i}",
            'email': f"user{i}@example.com",
            'role': user['role'],  # Keep non-sensitive data
            # Remove: password, SSN, credit cards, etc.
        }
        for i, user in enumerate(users)
    ]
```

### Using Fake Data

```python
from faker import Faker

fake = Faker()

def generate_test_users(count=10):
    return [
        {
            'username': fake.user_name(),
            'email': fake.email(),
            'address': fake.address(),
            'phone': fake.phone_number(),
        }
        for _ in range(count)
    ]
```

### Secure Sensitive Test Data

❌ **Never commit**:

```python
# test_data.py
API_KEY = "sk_live_12345..."  # DON'T DO THIS!
```

✅ **Use environment variables**:

```python
import os

API_KEY = os.getenv('TEST_API_KEY')

if not API_KEY:
    pytest.skip("TEST_API_KEY not set")
```

## Version Control for Test Data

### What to Track

✅ **Do commit**:

- Small test data files
- JSON/CSV with test cases
- Data generators/factories

❌ **Don't commit**:

- Large binary files (Excel > 1MB)
- Sensitive data
- Generated data files
- Database dumps

### .gitignore for Test Data

```gitignore
# Ignore generated test data
tests/test_data/generated/

# Ignore large files
*.xlsx
*.db

# Ignore sensitive data
*_sensitive.json
*_production.csv
```

### Data Versioning

```json
{
  "version": "2.0",
  "changelog": [
    "2.0: Added new user roles",
    "1.0: Initial test data"
  ],
  "test_data": [...]
}
```

## Best Practices

### 1. Keep Data Files Small

- One file per test suite
- Split large datasets
- Use pagination for DB data

### 2. Document Test Data

```csv
# Purpose: Test email validation with various formats
# Author: Test Team
# Last Updated: 2026-08-04
email,valid,reason
user@example.com,true,Standard valid email
invalid@,false,Missing domain
```

### 3. Make Data Self-Describing

```json
{
  "test_name": "invalid_email_missing_domain",
  "description": "Tests that emails without domains are rejected",
  "input": {
    "email": "user@"
  },
  "expected": {
    "valid": false,
    "error": "Invalid domain"
  }
}
```

### 4. Use Relative Paths

```python
import os

# Get test data relative to test file
TEST_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(TEST_DIR, 'test_data', 'users.json')
```

### 5. Validate Test Data

```python
def validate_test_data(data):
    """Ensure test data has required fields"""
    required_fields = ['username', 'email', 'expected']

    for item in data:
        for field in required_fields:
            if field not in item:
                raise ValueError(f"Missing required field: {field}")

    return data

test_data = validate_test_data(load_json_data('users.json'))
```

## Summary

**Data Source Selection**:

- Inline: Quick, small datasets
- CSV: Tabular, Excel-friendly
- JSON: Complex, nested data
- YAML: Configuration, comments
- Excel: Business users, large datasets
- Database: Production-like, shared

**Organization**:

- Clear directory structure
- Descriptive naming
- Environment-specific data

**Security**:

- Never commit sensitive data
- Use anonymized/fake data
- Environment variables for secrets

**Version Control**:

- Track small files
- Ignore large/generated files
- Document changes

## Next Steps

- [04: Best Practices](./04-best-practices.md) - Data-driven testing patterns and anti-patterns
