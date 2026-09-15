# Introduction to Data-Driven Testing

## What is Data-Driven Testing?

**Data-Driven Testing (DDT)** is a testing approach where test logic is separated from test data. The same test script runs multiple times with different sets of input data and expected results.

### Traditional Testing vs Data-Driven Testing

**Traditional Approach**:

```python
def test_login_valid_user():
    assert login("admin", "admin123") == "success"

def test_login_invalid_user():
    assert login("baduser", "admin123") == "failure"

def test_login_invalid_password():
    assert login("admin", "wrongpass") == "failure"

def test_login_empty_username():
    assert login("", "admin123") == "error"
```

**Data-Driven Approach**:

```python
@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", "success"),
    ("baduser", "admin123", "failure"),
    ("admin", "wrongpass", "failure"),
    ("", "admin123", "error"),
])
def test_login(username, password, expected):
    assert login(username, password) == expected
```

## Benefits of Data-Driven Testing

### 1. **Reduced Code Duplication**

- Write test logic once
- Execute with multiple data sets
- Easier to maintain

### 2. **Increased Test Coverage**

- Test many scenarios with minimal code
- Easy to add new test cases (just add data)
- Comprehensive edge case testing

### 3. **Better Maintainability**

- Change test logic in one place
- Update test data independently
- Non-programmers can manage test data

### 4. **Scalability**

- Add hundreds of test cases without writing new tests
- Leverage external data sources
- Parallel test execution

### 5. **Separation of Concerns**

- Test logic (how to test)
- Test data (what to test)
- Clear separation makes tests easier to understand

## When to Use Data-Driven Testing

### ✅ Good Use Cases

1. **Input Validation**

   - Testing multiple valid/invalid inputs
   - Boundary value testing with many boundaries
   - Format validation (emails, phone numbers, etc.)

2. **Calculation Testing**

   - Mathematical operations with various inputs
   - Currency conversions
   - Tax calculations, discounts, etc.

3. **API Testing**

   - Multiple request/response scenarios
   - Different parameter combinations
   - Error handling with various inputs

4. **Form Validation**

   - Registration forms
   - Login credentials
   - Search functionality

5. **Cross-Browser/Cross-Platform Testing**
   - Same tests on different browsers
   - Same tests on different OS versions
   - Same tests with different configurations

### ❌ Not Ideal For

1. **Complex Business Logic**

   - Tests requiring different setups
   - Tests with unique validation logic per case

2. **Workflow Testing**

   - Multi-step processes that differ significantly
   - Tests requiring different sequences

3. **Visual Testing**

   - UI appearance checks
   - Layout verification

4. **Exploratory Testing**
   - Ad-hoc testing scenarios
   - Tests that evolve during execution

## Data-Driven vs Other Approaches

### Data-Driven Testing

- **Focus**: Separate test data from test logic
- **Best for**: Testing same functionality with different inputs
- **Example**: Login with 100 different username/password combinations

### Keyword-Driven Testing

- **Focus**: Use keywords/actions to build tests
- **Best for**: Non-programmers creating tests
- **Example**: "Navigate | Login | Enter_Username | Enter_Password | Click_Submit"

### Hybrid Testing

- **Focus**: Combination of data-driven and keyword-driven
- **Best for**: Complex test frameworks
- **Example**: Keywords + external data files

## Real-World Example: E-Commerce Checkout

### Scenario

Test a checkout process with different:

- Product quantities (1, 5, 10, 100)
- Discount codes (valid, invalid, expired)
- Shipping methods (standard, express, overnight)
- Payment methods (credit card, PayPal, Apple Pay)

### Traditional Approach

Would require: 4 × 3 × 3 × 3 = **108 separate test functions**

### Data-Driven Approach

**One test function + 108 rows of data**

```python
@pytest.mark.parametrize("quantity,discount,shipping,payment,expected_total", [
    (1, "SAVE10", "standard", "credit_card", 9.99),
    (5, "SAVE10", "express", "paypal", 54.99),
    # ... 106 more rows
])
def test_checkout(quantity, discount, shipping, payment, expected_total):
    result = checkout(quantity, discount, shipping, payment)
    assert result.total == expected_total
```

## Data Sources for Data-Driven Testing

### 1. **Inline Data**

- Hard-coded in test file
- Good for small datasets
- Easy to see data at a glance

### 2. **CSV Files**

- Spreadsheet-friendly
- Easy to edit
- Good for medium datasets

### 3. **JSON Files**

- Structured data
- Complex nested data
- Good for API testing

### 4. **Excel Files**

- Non-technical users can edit
- Multiple sheets for organization
- Good for large datasets

### 5. **Databases**

- Production-like data
- Large datasets
- Dynamic data

### 6. **YAML/XML Files**

- Configuration-like data
- Hierarchical data
- Good for complex scenarios

## Example: Data Sources in Action

### Inline Data

```python
@pytest.mark.parametrize("email,valid", [
    ("user@example.com", True),
    ("invalid.email", False),
    ("@example.com", False),
])
def test_email_validation(email, valid):
    assert is_valid_email(email) == valid
```

### CSV File (`test_emails.csv`)

```csv
email,valid
user@example.com,True
invalid.email,False
@example.com,False
```

```python
import csv
import pytest

def load_csv_data(filename):
    with open(filename) as f:
        reader = csv.DictReader(f)
        return [(row['email'], row['valid'] == 'True') for row in reader]

@pytest.mark.parametrize("email,valid", load_csv_data('test_emails.csv'))
def test_email_validation(email, valid):
    assert is_valid_email(email) == valid
```

### JSON File (`test_emails.json`)

```json
[
  { "email": "user@example.com", "valid": true },
  { "email": "invalid.email", "valid": false },
  { "email": "@example.com", "valid": false }
]
```

```python
import json
import pytest

def load_json_data(filename):
    with open(filename) as f:
        data = json.load(f)
        return [(item['email'], item['valid']) for item in data]

@pytest.mark.parametrize("email,valid", load_json_data('test_emails.json'))
def test_email_validation(email, valid):
    assert is_valid_email(email) == valid
```

## Key Concepts

### Test Data Independence

Test data should be:

- **Independent**: Each test case can run standalone
- **Reusable**: Data can be used across multiple tests
- **Maintainable**: Easy to update without code changes
- **Versioned**: Track changes to test data

### Test Data Coverage

Consider:

- **Valid data**: Expected successful scenarios
- **Invalid data**: Expected failures
- **Boundary values**: Edge cases
- **Special characters**: Unicode, SQL injection attempts
- **Empty/null values**: Missing data scenarios

### Test Result Analysis

Data-driven tests provide:

- Clear pass/fail for each dataset
- Easy identification of problematic inputs
- Patterns in failures
- Coverage metrics per data category

## Best Practices

1. **Start Small**: Begin with inline data, scale to files
2. **Name Your Data**: Use descriptive parameter names
3. **Document Data**: Explain what each dataset tests
4. **Keep Data Simple**: One concern per dataset
5. **Separate Concerns**: Logic vs data
6. **Version Control**: Track test data changes
7. **Review Data**: Regularly audit test data relevance

## Common Pitfalls

### ❌ Over-Parametrization

```python
# Too many parameters make tests hard to understand
@pytest.mark.parametrize("a,b,c,d,e,f,g,h,i,j,expected", [...])
def test_complex(a,b,c,d,e,f,g,h,i,j,expected):
    # What does this test?
    pass
```

### ✅ Better Approach

```python
# Group related parameters
@pytest.mark.parametrize("user_data,cart_data,expected", [
    ({"name": "Alice", "age": 25}, {"items": 2}, "success"),
])
def test_checkout(user_data, cart_data, expected):
    # Clear intent
    pass
```

### ❌ Test Data in Code

```python
# Hard to maintain
@pytest.mark.parametrize("data", [
    {"very": {"deeply": {"nested": {"data": {"structure": "here"}}}}},
])
```

### ✅ Better Approach

```python
# Use external files for complex data
@pytest.mark.parametrize("data", load_json_data('complex_data.json'))
```

## Summary

Data-Driven Testing:

- ✅ Separates test logic from test data
- ✅ Reduces code duplication
- ✅ Increases test coverage
- ✅ Improves maintainability
- ✅ Scales efficiently

**Remember**: DDT is a tool, not a silver bullet. Use it when you have multiple similar test scenarios with different inputs.

## Next Steps

- [02: Parameterized Tests](./02-parameterized-tests.md) - Learn pytest.mark.parametrize and Jest test.each()
- [03: Test Data Management](./03-test-data-management.md) - Managing external test data
- [04: Best Practices](./04-best-practices.md) - DDT patterns and anti-patterns
