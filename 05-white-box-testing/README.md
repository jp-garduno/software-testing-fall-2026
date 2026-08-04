# Module 5: White Box Testing (Unit & Integration Tests)

## 🎯 Learning Objectives

By the end of this module, you will be able to:
- Write effective unit tests for individual functions and classes
- Understand and measure statement, branch, and path coverage
- Use code coverage tools to identify untested code
- Write integration tests for module interactions
- Apply mocking and stubbing techniques
- Achieve meaningful code coverage in real projects

## 📚 Theory Materials

### [1. Introduction to White Box Testing](./theory/01-introduction.md)
- What is white box testing vs black box
- When and why to use white box testing
- Unit testing fundamentals
- Integration testing fundamentals

### [2. Statement Coverage](./theory/02-statement-coverage.md)
- Definition and calculation
- How to achieve 100% statement coverage
- Limitations of statement coverage
- Examples in Python and JavaScript

### [3. Branch Coverage](./theory/03-branch-coverage.md)
- Definition and calculation
- Difference from statement coverage
- Testing all decision outcomes
- Examples and practice

### [4. Path Coverage](./theory/04-path-coverage.md)
- Definition and calculation
- Independent paths
- Cyclomatic complexity
- Why 100% path coverage is often impractical

### [5. Code Coverage Tools and Reports](./theory/05-coverage-tools.md)
- Coverage.py for Python
- Istanbul/NYC for JavaScript
- Reading coverage reports
- Setting coverage thresholds
- Integrating with CI/CD

### [6. Mock-up Testing](./theory/06-mocking.md)
- When and why to use mocks
- Mocks vs stubs vs fakes vs spies
- unittest.mock in Python
- Jest mocking in JavaScript
- Best practices and anti-patterns

## 🛠️ Tools & Setup

### Python
```bash
pip install pytest pytest-cov
```

**Run tests with coverage**:
```bash
pytest --cov=. --cov-report=html
```

### JavaScript/TypeScript
```bash
npm install --save-dev jest @types/jest
```

**Run tests with coverage**:
```bash
npm test -- --coverage
```

## 💻 Practical Exercises

### Python Exercises
- [01-calculator](./python/exercises/01-calculator.md) - Basic unit tests
- [02-shopping-cart](./python/exercises/02-shopping-cart.md) - Class testing
- [03-user-service](./python/exercises/03-user-service.md) - Integration & mocking
- [04-coverage-challenge](./python/exercises/04-coverage-challenge.md) - Achieve 100% coverage

### JavaScript Exercises
- [01-calculator](./javascript/exercises/01-calculator.md) - Basic unit tests
- [02-shopping-cart](./javascript/exercises/02-shopping-cart.md) - Class testing
- [03-user-service](./javascript/exercises/03-user-service.md) - Integration & mocking
- [04-coverage-challenge](./javascript/exercises/04-coverage-challenge.md) - Achieve 100% coverage

## 📝 Homework Assignment

**[Homework 5: White Box Testing & Coverage](./homework/homework-5.md)**

**Due**: End of Week 8

**Objectives**: 
- Write comprehensive unit and integration tests
- Achieve high code coverage (>80%)
- Use mocking for external dependencies
- Generate and analyze coverage reports

---

## 🎯 Self-Assessment Checklist

- [ ] Write unit tests for functions and classes
- [ ] Calculate statement, branch, and path coverage
- [ ] Use coverage tools (Coverage.py, Istanbul)
- [ ] Read and interpret coverage reports
- [ ] Write integration tests
- [ ] Apply mocking techniques
- [ ] Understand coverage limitations

## 🚀 Next Steps

- Complete [Homework 5](./homework/homework-5.md)
- Preview [Module 6: Test Driven Development](../06-test-driven-development/README.md)
- Prepare for Exam 2 (Week 11)
