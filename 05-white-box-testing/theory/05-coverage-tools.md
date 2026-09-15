# Coverage Tools

**Module**: 5 - White Box Testing  
**Topic**: Measuring and Reporting Code Coverage  
**Reading Time**: 28 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Install and configure Coverage.py for Python projects
- Use Istanbul/NYC with Jest for JavaScript coverage
- Generate and interpret HTML coverage reports
- Set coverage thresholds in pytest and Jest
- Integrate coverage into CI/CD pipelines
- Add coverage badges to your README
- Use coverage reports to identify untested code

---

## Why Use Coverage Tools?

### Manual Coverage Tracking is Hard

Without tools, tracking which lines are executed is:

- Time-consuming
- Error-prone
- Doesn't scale

### Coverage Tools Automate Everything

Coverage tools automatically:

1. **Instrument** code (add tracking)
2. **Monitor** execution during tests
3. **Report** what was and wasn't covered
4. **Generate** visualizations (HTML reports)
5. **Enforce** minimum thresholds

---

## Python: Coverage.py

### What is Coverage.py?

**Coverage.py** is the standard code coverage tool for Python.

- Works with pytest, unittest, nose
- Measures statement and branch coverage
- Generates HTML, XML, JSON reports
- Integrates with CI/CD

### Installation

```bash
# Install coverage.py
pip install coverage

# Or install with pytest plugin
pip install pytest-cov
```

### Basic Usage

#### Method 1: Using `coverage` command

```bash
# Run tests with coverage
coverage run -m pytest

# Show coverage report in terminal
coverage report

# Generate HTML report
coverage html

# Open in browser
open htmlcov/index.html
```

#### Method 2: Using `pytest-cov` plugin

```bash
# Run pytest with coverage
pytest --cov=src

# With HTML report
pytest --cov=src --cov-report=html

# With terminal report
pytest --cov=src --cov-report=term

# With missing lines shown
pytest --cov=src --cov-report=term-missing
```

### Example Project Structure

```
my_project/
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   └── validator.py
├── tests/
│   ├── __init__.py
│   ├── test_calculator.py
│   └── test_validator.py
├── pytest.ini
└── .coveragerc
```

### Configuration: `.coveragerc`

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = htmlcov

[coverage:run]
branch = True
```

### Configuration: `pytest.ini`

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

addopts =
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

---

## Python Coverage Example

### Code to Test

```python
# src/calculator.py
class Calculator:
    def add(self, a, b):
        """Add two numbers"""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a"""
        return a - b

    def divide(self, a, b):
        """Divide a by b"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, base, exponent):
        """Raise base to exponent"""
        if exponent < 0:
            raise ValueError("Negative exponents not supported")

        result = 1
        for _ in range(exponent):
            result *= base
        return result
```

### Tests

```python
# tests/test_calculator.py
import pytest
from src.calculator import Calculator

class TestCalculator:
    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_subtract(self):
        assert self.calc.subtract(5, 3) == 2

    def test_divide(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)

    # Note: power() method not tested yet!
```

### Running Coverage

```bash
$ pytest --cov=src --cov-report=term-missing

=========== test session starts ===========
collected 4 items

tests/test_calculator.py ....           [100%]

---------- coverage: platform linux ----------
Name                    Stmts   Miss  Cover   Missing
-----------------------------------------------------
src/__init__.py             0      0   100%
src/calculator.py          14      6    57%   19-25
-----------------------------------------------------
TOTAL                      14      6    57%
```

**Interpretation**:

- `calculator.py` has 57% coverage
- Lines 19-25 not covered (the `power()` method)

### Adding Missing Tests

```python
# tests/test_calculator.py (continued)
def test_power(self):
    assert self.calc.power(2, 3) == 8
    assert self.calc.power(5, 0) == 1

def test_power_negative_exponent(self):
    with pytest.raises(ValueError, match="Negative exponents"):
        self.calc.power(2, -1)
```

### New Coverage Report

```bash
$ pytest --cov=src --cov-report=term-missing

Name                    Stmts   Miss  Cover
-------------------------------------------
src/__init__.py             0      0   100%
src/calculator.py          14      0   100%
-------------------------------------------
TOTAL                      14      0   100%
```

**100% coverage achieved!**

---

## Python: HTML Coverage Reports

### Generating HTML Reports

```bash
# Generate HTML report
pytest --cov=src --cov-report=html

# Open in browser
open htmlcov/index.html
```

### HTML Report Structure

```
htmlcov/
├── index.html          # Main page with summary
├── calculator_py.html  # Annotated source code
├── validator_py.html
└── style.css
```

### Reading HTML Reports

**Main Page (index.html)**:

```
Module              Statements   Missing   Excluded   Coverage
─────────────────────────────────────────────────────────────
src/calculator.py   14           0         0          100%
src/validator.py    20           5         0          75%
─────────────────────────────────────────────────────────────
TOTAL               34           5         0          85%
```

**Annotated Source (calculator_py.html)**:

```python
 1 class Calculator:                       # ✓ Covered
 2     def add(self, a, b):                # ✓ Covered
 3         return a + b                    # ✓ Covered
 4
 5     def divide(self, a, b):             # ✓ Covered
 6         if b == 0:                      # ✓ Covered
 7             raise ValueError(...)        # ✓ Covered
 8         return a / b                    # ✓ Covered
 9
10     def unused_method(self):            # ✗ Not covered
11         return "never called"           # ✗ Not covered
```

**Color coding**:

- **Green**: Covered lines
- **Red**: Not covered
- **Yellow**: Partially covered (some branches not tested)

---

## JavaScript: Istanbul/NYC with Jest

### What is Istanbul/NYC?

**Istanbul** (now **NYC**) is the standard coverage tool for JavaScript.

- Built into Jest
- Measures statement, branch, function, line coverage
- Generates HTML reports
- Works with all major test frameworks

### Installation

```bash
# Jest includes coverage by default
npm install --save-dev jest

# Or install NYC separately
npm install --save-dev nyc
```

### Basic Usage with Jest

```bash
# Run tests with coverage
npm test -- --coverage

# Or add to package.json
npm run test:coverage
```

### Configuration: `package.json`

```json
{
  "name": "my-project",
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage",
    "test:watch": "jest --watch"
  },
  "jest": {
    "collectCoverageFrom": [
      "src/**/*.{js,jsx}",
      "!src/**/*.test.js",
      "!src/index.js"
    ],
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    },
    "coverageReporters": ["text", "html", "lcov"]
  }
}
```

### Configuration: `jest.config.js`

```javascript
// jest.config.js
module.exports = {
  collectCoverage: true,
  collectCoverageFrom: [
    "src/**/*.{js,jsx,ts,tsx}",
    "!src/**/*.test.{js,jsx,ts,tsx}",
    "!src/index.js",
    "!src/**/*.d.ts",
  ],
  coverageDirectory: "coverage",
  coverageReporters: ["text", "html", "lcov", "json"],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testEnvironment: "node",
};
```

---

## JavaScript Coverage Example

### Code to Test

```javascript
// src/userService.js
class UserService {
  validateEmail(email) {
    if (!email) {
      return false;
    }

    if (!email.includes("@")) {
      return false;
    }

    const parts = email.split("@");
    if (parts.length !== 2) {
      return false;
    }

    return true;
  }

  calculateAge(birthYear) {
    const currentYear = new Date().getFullYear();

    if (birthYear < 1900 || birthYear > currentYear) {
      throw new Error("Invalid birth year");
    }

    return currentYear - birthYear;
  }

  formatName(firstName, lastName) {
    if (!firstName || !lastName) {
      return "";
    }

    return `${firstName} ${lastName}`;
  }
}

module.exports = UserService;
```

### Tests

```javascript
// src/userService.test.js
const UserService = require("./userService");

describe("UserService", () => {
  let service;

  beforeEach(() => {
    service = new UserService();
  });

  describe("validateEmail", () => {
    test("returns false for empty email", () => {
      expect(service.validateEmail("")).toBe(false);
    });

    test("returns false for email without @", () => {
      expect(service.validateEmail("invalidemail")).toBe(false);
    });

    test("returns true for valid email", () => {
      expect(service.validateEmail("user@example.com")).toBe(true);
    });
  });

  describe("calculateAge", () => {
    test("calculates age correctly", () => {
      const age = service.calculateAge(2000);
      expect(age).toBeGreaterThan(20);
    });

    test("throws error for invalid birth year", () => {
      expect(() => service.calculateAge(1800)).toThrow("Invalid birth year");
    });
  });

  // Note: formatName() not tested yet!
});
```

### Running Coverage

```bash
$ npm test -- --coverage

PASS  src/userService.test.js
  UserService
    validateEmail
      ✓ returns false for empty email
      ✓ returns false for email without @
      ✓ returns true for valid email
    calculateAge
      ✓ calculates age correctly
      ✓ throws error for invalid birth year

--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |   77.78 |    83.33 |   66.67 |   77.78 |
 userService.js     |   77.78 |    83.33 |   66.67 |   77.78 |
--------------------|---------|----------|---------|---------|
```

**Interpretation**:

- Statement coverage: 77.78%
- Branch coverage: 83.33%
- Function coverage: 66.67% (formatName not tested)
- Line coverage: 77.78%

### Adding Missing Tests

```javascript
// src/userService.test.js (continued)
describe("formatName", () => {
  test("formats name correctly", () => {
    expect(service.formatName("John", "Doe")).toBe("John Doe");
  });

  test("returns empty string for missing firstName", () => {
    expect(service.formatName("", "Doe")).toBe("");
  });

  test("returns empty string for missing lastName", () => {
    expect(service.formatName("John", "")).toBe("");
  });
});
```

### New Coverage Report

```bash
--------------------|---------|----------|---------|---------|
File                | % Stmts | % Branch | % Funcs | % Lines |
--------------------|---------|----------|---------|---------|
All files           |     100 |      100 |     100 |     100 |
 userService.js     |     100 |      100 |     100 |     100 |
--------------------|---------|----------|---------|---------|
```

**100% coverage achieved!**

---

## JavaScript: HTML Coverage Reports

### Generating HTML Reports

```bash
# Generate HTML report
npm test -- --coverage --coverageReporters=html

# Open in browser
open coverage/index.html
```

### HTML Report Structure

```
coverage/
├── index.html              # Main summary
├── lcov-report/
│   ├── index.html
│   ├── userService.js.html # Annotated source
│   └── style.css
└── lcov.info
```

### Reading Jest HTML Reports

**Main Page**:

```
File              % Stmts   % Branch   % Funcs   % Lines   Uncovered Lines
─────────────────────────────────────────────────────────────────────────
All files         100       100        100       100
  userService.js  100       100        100       100
```

**Annotated Source**:

```javascript
 1   class UserService {                     // ✓
 2     validateEmail(email) {                // ✓
 3       if (!email) {                       // ✓
 4         return false;                     // ✓
 5       }
 6       if (!email.includes('@')) {         // ✓
 7         return false;                     // ✓
 8       }
 9       return true;                        // ✓
10     }
11
12     unusedMethod() {                      // ✗ Not covered
13       return 'never called';              // ✗ Not covered
14     }
15   }
```

---

## Setting Coverage Thresholds

### Why Set Thresholds?

Coverage thresholds:

- **Prevent** coverage from decreasing
- **Enforce** minimum quality standards
- **Fail** builds automatically if coverage drops

### Python: pytest Thresholds

#### Method 1: Command Line

```bash
# Fail if coverage below 80%
pytest --cov=src --cov-fail-under=80
```

#### Method 2: pytest.ini

```ini
# pytest.ini
[tool:pytest]
addopts =
    --cov=src
    --cov-fail-under=80
```

#### Method 3: .coveragerc

```ini
# .coveragerc
[report]
fail_under = 80
```

### Python: Branch Coverage Threshold

```ini
# .coveragerc
[run]
branch = True

[report]
fail_under = 85
show_missing = True
```

```bash
# Run with branch coverage
pytest --cov=src --cov-branch --cov-fail-under=85
```

### JavaScript: Jest Thresholds

#### In package.json

```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

#### Per-Directory Thresholds

```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      },
      "./src/critical/": {
        "branches": 95,
        "functions": 95,
        "lines": 95,
        "statements": 95
      },
      "./src/utils/": {
        "branches": 70,
        "functions": 70,
        "lines": 70,
        "statements": 70
      }
    }
  }
}
```

### Example: Build Failure

```bash
$ npm test

FAIL  src/calculator.test.js
  ● Test suite failed to run

    Jest: "global" coverage threshold for branches (80%) not met: 75%
    Jest: "global" coverage threshold for functions (80%) not met: 78%

Test Suites: 1 failed, 0 passed, 1 total
```

---

## CI/CD Integration

### GitHub Actions: Python

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=src --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### GitHub Actions: JavaScript

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"

      - name: Install dependencies
        run: npm ci

      - name: Run tests with coverage
        run: npm run test:coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
```

### Failing Builds on Low Coverage

```yaml
# Python
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-fail-under=80 --cov-report=term

# JavaScript (already configured in jest.config.js)
- name: Run tests with coverage
  run: npm test -- --coverage
```

---

## Coverage Badges

### What are Coverage Badges?

Badges show coverage percentage in your README:

![Coverage Badge](https://img.shields.io/badge/coverage-95%25-brightgreen)

### Using Codecov

1. **Sign up** at [codecov.io](https://codecov.io)
2. **Connect** your GitHub repository
3. **Add** badge to README:

```markdown
# My Project

[![codecov](https://codecov.io/gh/username/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/username/repo)
```

### Using Coveralls

1. **Sign up** at [coveralls.io](https://coveralls.io)
2. **Add to CI**:

```yaml
- name: Upload to Coveralls
  uses: coverallsapp/github-action@v2
```

3. **Add badge**:

```markdown
[![Coverage Status](https://coveralls.io/repos/github/username/repo/badge.svg?branch=main)](https://coveralls.io/github/username/repo?branch=main)
```

### Self-Hosted Badge

Generate badge from coverage data:

```python
# Python script to generate badge
coverage = 85.5
color = "brightgreen" if coverage >= 80 else "orange" if coverage >= 60 else "red"
badge = f"https://img.shields.io/badge/coverage-{coverage}%25-{color}"
```

---

## Coverage Tools Comparison

### Python: Coverage.py

**Pros**:

- ✅ Standard tool for Python
- ✅ Works with all test frameworks
- ✅ Excellent HTML reports
- ✅ Branch coverage support
- ✅ Easy CI/CD integration

**Cons**:

- ❌ No built-in complexity metrics
- ❌ No incremental coverage (changed files only)

### JavaScript: Istanbul/NYC

**Pros**:

- ✅ Built into Jest
- ✅ Four coverage metrics (statement, branch, function, line)
- ✅ Beautiful HTML reports
- ✅ Per-directory thresholds

**Cons**:

- ❌ Configuration can be complex
- ❌ Slower test execution

---

## Best Practices

### 1. Don't Obsess Over 100%

```python
# Some code is okay to skip
def __repr__(self):
    return f"User({self.email})"  # Low value to test

def main():  # pragma: no cover
    # Often skipped in coverage
    app.run()
```

**Exclude from coverage**:

```ini
# .coveragerc
[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if __name__ == .__main__.:
```

### 2. Focus on Critical Code

Higher thresholds for important code:

```json
{
  "coverageThreshold": {
    "./src/payment/": {
      "branches": 95,
      "functions": 95
    },
    "./src/ui/": {
      "branches": 70,
      "functions": 70
    }
  }
}
```

### 3. Run Coverage Locally

```bash
# Before pushing
npm run test:coverage

# Check report
open coverage/index.html
```

### 4. Track Coverage Over Time

Use tools like Codecov to see trends:

```
Coverage trend:
Week 1: 75%
Week 2: 78% ↑
Week 3: 82% ↑
Week 4: 85% ↑
```

### 5. Ignore Generated/Vendor Code

```ini
# Python .coveragerc
[run]
omit =
    */migrations/*
    */venv/*
    */vendor/*
    */tests/*
```

```json
// JavaScript jest.config.js
{
  "collectCoverageFrom": ["src/**/*.js", "!src/vendor/**", "!src/**/*.test.js"]
}
```

---

## Common Mistakes

### 1. Gaming the Metrics

❌ **Bad**: Tests that don't actually verify behavior

```python
def test_useless():
    calculator.add(2, 3)  # No assertion! Just for coverage
```

✅ **Good**: Meaningful tests

```python
def test_add():
    result = calculator.add(2, 3)
    assert result == 5
```

### 2. Ignoring Coverage Reports

❌ **Bad**: Running coverage but never looking at reports

✅ **Good**: Regularly review HTML reports to find gaps

### 3. Setting Unrealistic Thresholds

❌ **Bad**: Requiring 100% coverage on everything

✅ **Good**: Reasonable thresholds (80-90%) with exceptions

---

## Summary

**Python Coverage Tools**:

- Use **Coverage.py** or **pytest-cov**
- Configure in `.coveragerc` or `pytest.ini`
- Run: `pytest --cov=src --cov-report=html`
- Set thresholds: `--cov-fail-under=80`

**JavaScript Coverage Tools**:

- Use **Jest** (includes Istanbul/NYC)
- Configure in `jest.config.js` or `package.json`
- Run: `npm test -- --coverage`
- Set thresholds in `coverageThreshold`

**HTML Reports**:

- Visual, color-coded
- Show exactly which lines not covered
- Essential for finding gaps

**CI/CD Integration**:

- Run coverage on every commit
- Fail builds if coverage drops
- Upload to Codecov/Coveralls
- Add badges to README

**Best Practices**:

- Aim for 80-90% coverage
- Higher for critical code
- Don't obsess over 100%
- Review reports regularly
- Track trends over time

---

## Practice Exercises

1. **Set Up Coverage**: For a project you're working on, set up coverage reporting with:

   - Python: pytest-cov
   - JavaScript: Jest coverage
   - Generate HTML report and identify uncovered lines

2. **Configure Thresholds**: Add coverage thresholds to your project:

   - Global: 80%
   - Critical directory: 90%
   - Make sure tests pass

3. **CI/CD Integration**: Create a GitHub Actions workflow that:

   - Runs tests with coverage
   - Fails if coverage < 80%
   - Uploads results to Codecov
   - Adds badge to README

4. **Improve Coverage**: Take a project with < 80% coverage and:
   - Generate HTML report
   - Identify uncovered lines
   - Write tests to reach 80%
   - Document what you skipped and why

---

## Next Steps

- Read [06-mocking.md](./06-mocking.md) to learn about isolating dependencies in tests
- Practice with [Exercise 5: Coverage Tools](../exercises/05-coverage-tools.md)
- Set up coverage for your team project
