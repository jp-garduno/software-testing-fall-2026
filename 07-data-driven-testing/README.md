# Module 7: Data Driven Testing

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Understand the benefits of data-driven testing
- Write parameterized tests in Python and JavaScript
- Manage test data effectively (CSV, JSON, Excel)
- Separate test logic from test data
- Scale test suites efficiently
- Use data-driven approaches for API and UI testing

## 📚 Theory Materials

### [1. Introduction to Data-Driven Testing](./theory/01-introduction.md)

- What is data-driven testing
- Benefits: reusability, maintainability, scalability
- When to use data-driven testing
- Data-driven vs keyword-driven vs hybrid

### [2. Parameterized Tests](./theory/02-parameterized-tests.md)

- pytest.mark.parametrize in Python
- Jest test.each() in JavaScript
- Multiple parameter sets
- Naming parameterized tests

### [3. Test Data Management](./theory/03-test-data-management.md)

- Test data sources (CSV, JSON, Excel, databases)
- Loading and parsing test data
- Test data organization
- Data fixtures and factories

### [4. Best Practices](./theory/04-best-practices.md)

- Separating data from tests
- Data-driven test design patterns
- Handling test data dependencies
- Data privacy in testing

## 🛠️ Tools & Frameworks

### Python

```bash
pip install pytest parameterized
```

**Example Parameterized Test**:

```python
import pytest

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (3, 4),
])
def test_increment(input, expected):
    assert input + 1 == expected
```

### JavaScript/TypeScript

```bash
npm install --save-dev jest
```

**Example Parameterized Test**:

```javascript
test.each([
  [1, 2],
  [2, 3],
  [3, 4],
])("increment %i equals %i", (input, expected) => {
  expect(input + 1).toBe(expected);
});
```

## 💻 Practical Exercises

### Python Exercises

- [01-basic-parametrization](./python/exercises/01-basic-parametrization.md)
- [02-csv-data-driven](./python/exercises/02-csv-data-driven.md)
- [03-json-data-driven](./python/exercises/03-json-data-driven.md)
- [04-api-data-driven](./python/exercises/04-api-data-driven.md)

### JavaScript Exercises

- [01-basic-parametrization](./javascript/exercises/01-basic-parametrization.md)
- [02-json-data-driven](./javascript/exercises/02-json-data-driven.md)
- [03-api-data-driven](./javascript/exercises/03-api-data-driven.md)

## 📝 Homework Assignment

**[Homework 7: Data-Driven Test Suite](./homework/homework-7.md)**

**Due**: End of Week 13

**Objectives**:

- Create data-driven tests for a complex system
- Use external data files (CSV/JSON)
- Demonstrate parameterized testing
- Compare coverage with traditional tests

## 📊 Data Sources Example

### CSV Format (`test_data.csv`):

```csv
username,password,expected_result
valid_user,valid_pass,success
invalid_user,valid_pass,failure
valid_user,invalid_pass,failure
,valid_pass,error
valid_user,,error
```

### JSON Format (`test_data.json`):

```json
[
  {
    "username": "valid_user",
    "password": "valid_pass",
    "expected_result": "success"
  },
  {
    "username": "invalid_user",
    "password": "valid_pass",
    "expected_result": "failure"
  }
]
```

## 🎯 Self-Assessment Checklist

- [ ] Write parameterized tests in Python
- [ ] Write parameterized tests in JavaScript
- [ ] Load test data from CSV files
- [ ] Load test data from JSON files
- [ ] Separate test data from test logic
- [ ] Scale test suites with data-driven approach
- [ ] Understand when to use data-driven testing

## 🚀 Next Steps

- Complete [Homework 7](./homework/homework-7.md)
- Preview [Module 8: System Level Testing](../08-system-level-testing/README.md)
- Continue working on Team Project Milestone 5
