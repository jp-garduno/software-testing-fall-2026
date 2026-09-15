# Exercise 1: Calculator Unit Tests

**Duration**: 45-60 minutes  
**Difficulty**: Beginner  
**Topics**: Unit testing, Jest, edge cases, statement coverage

## Objectives

By completing this exercise, you will:

- Write unit tests for individual methods using Jest
- Test edge cases and error conditions
- Measure statement coverage with Jest
- Understand the basics of test-driven development

## Background

Unit testing is the foundation of white box testing. In this exercise, you'll implement a `Calculator` class and write comprehensive unit tests that verify each method works correctly, including edge cases that might cause errors.

## Part 1: Implementation (15 minutes)

Create a file named `calculator.js` with the following starter code:

```javascript
class Calculator {
  /**
   * A simple calculator with basic arithmetic operations.
   */

  /**
   * Add two numbers.
   */
  add(a, b) {
    return a + b;
  }

  /**
   * Subtract b from a.
   */
  subtract(a, b) {
    return a - b;
  }

  /**
   * Multiply two numbers.
   */
  multiply(a, b) {
    return a * b;
  }

  /**
   * Divide a by b. Throws Error if b is zero.
   */
  divide(a, b) {
    if (b === 0) {
      throw new Error("Cannot divide by zero");
    }
    return a / b;
  }

  /**
   * Raise base to the power of exponent.
   */
  power(base, exponent) {
    return Math.pow(base, exponent);
  }

  /**
   * Calculate square root. Throws Error if x is negative.
   */
  sqrt(x) {
    if (x < 0) {
      throw new Error("Cannot calculate square root of negative number");
    }
    return Math.sqrt(x);
  }
}

module.exports = Calculator;
```

## Part 2: Write Unit Tests (25 minutes)

Create a file named `calculator.test.js` and write comprehensive tests:

```javascript
const Calculator = require("./calculator");

describe("Calculator", () => {
  let calc;

  beforeEach(() => {
    // Create a fresh Calculator instance before each test
    calc = new Calculator();
  });

  // TODO: Write tests for add method
  describe("add", () => {
    test("should add two positive numbers", () => {
      // Replace with your implementation
    });

    test("should add two negative numbers", () => {
      // Replace with your implementation
    });

    test("should add positive and negative numbers", () => {
      // Replace with your implementation
    });
  });

  // TODO: Write tests for subtract method
  describe("subtract", () => {
    test("should subtract resulting in positive number", () => {
      // Replace with your implementation
    });

    test("should subtract resulting in negative number", () => {
      // Replace with your implementation
    });
  });

  // TODO: Write tests for multiply method
  describe("multiply", () => {
    test("should multiply two positive numbers", () => {
      // Replace with your implementation
    });

    test("should multiply by zero", () => {
      // Replace with your implementation
    });

    test("should multiply negative numbers", () => {
      // Replace with your implementation
    });
  });

  // TODO: Write tests for divide method
  describe("divide", () => {
    test("should divide two numbers normally", () => {
      // Replace with your implementation
    });

    test("should throw error when dividing by zero", () => {
      // Hint: Use expect(() => { }).toThrow()
    });

    test("should divide negative numbers", () => {
      // Replace with your implementation
    });
  });

  // TODO: Write tests for power method
  describe("power", () => {
    test("should raise to positive exponent", () => {
      // Replace with your implementation
    });

    test("should handle zero exponent", () => {
      // Replace with your implementation
    });

    test("should handle negative exponent", () => {
      // Replace with your implementation
    });
  });

  // TODO: Write tests for sqrt method
  describe("sqrt", () => {
    test("should calculate square root of positive number", () => {
      // Replace with your implementation
    });

    test("should calculate square root of zero", () => {
      // Replace with your implementation
    });

    test("should throw error for negative number", () => {
      // Hint: Use expect(() => { }).toThrow()
    });
  });
});
```

### Your Tasks

1. **Implement all test methods** - Replace comments with actual test code
2. **Test normal cases** - Verify methods work with typical inputs
3. **Test edge cases** - Zero, negative numbers, large numbers
4. **Test error conditions** - Use `expect().toThrow()` for expected exceptions

### Example Test Implementation

```javascript
test("should add two positive numbers", () => {
  const result = calc.add(5, 3);
  expect(result).toBe(8);
});

test("should throw error when dividing by zero", () => {
  expect(() => {
    calc.divide(10, 0);
  }).toThrow("Cannot divide by zero");
});
```

## Part 3: Run Tests and Measure Coverage (10 minutes)

### Setup Jest

Create `package.json` if you don't have one:

```json
{
  "name": "calculator-tests",
  "version": "1.0.0",
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  },
  "devDependencies": {
    "jest": "^29.0.0"
  }
}
```

Install dependencies:

```bash
npm install
```

### Run Your Tests

```bash
# Run all tests
npm test

# Run a specific test file
npm test calculator.test.js

# Run in watch mode
npm test -- --watch
```

### Measure Statement Coverage

```bash
# Run tests with coverage
npm run test:coverage

# Or directly with Jest
jest --coverage
```

### Understanding Coverage Output

```
----------|---------|----------|---------|---------|-------------------
File      | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
----------|---------|----------|---------|---------|-------------------
All files |     100 |      100 |     100 |     100 |
calculator|     100 |      100 |     100 |     100 |
----------|---------|----------|---------|---------|-------------------
```

- **% Stmts**: Percentage of statements covered
- **% Branch**: Percentage of branches (if/else) covered
- **% Funcs**: Percentage of functions covered
- **% Lines**: Percentage of lines covered
- **Uncovered Line #s**: Line numbers not covered

## Part 4: Additional Challenges (10 minutes)

Add these methods to your `Calculator` class and write tests for them:

```javascript
/**
 * Return remainder of a divided by b.
 */
modulo(a, b) {
  if (b === 0) {
    throw new Error('Cannot divide by zero');
  }
  return a % b;
}

/**
 * Return absolute value of x.
 */
absolute(x) {
  return Math.abs(x);
}

/**
 * Calculate factorial of n. Throws Error if n is negative or not an integer.
 */
factorial(n) {
  if (!Number.isInteger(n)) {
    throw new Error('Factorial requires an integer');
  }
  if (n < 0) {
    throw new Error('Factorial not defined for negative numbers');
  }
  if (n === 0 || n === 1) {
    return 1;
  }
  let result = 1;
  for (let i = 2; i <= n; i++) {
    result *= i;
  }
  return result;
}
```

## Evaluation Criteria

Your solution will be evaluated on:

- **Test Coverage**: 100% statement coverage achieved
- **Edge Cases**: All edge cases tested (zero, negative, large numbers)
- **Error Handling**: Exceptions properly tested with toThrow()
- **Test Quality**: Tests are clear, well-named, and independent
- **Code Organization**: Tests are properly grouped and documented

## Common Mistakes to Avoid

1. **Not testing edge cases** - Always test zero, negative numbers, and boundaries
2. **Testing multiple things in one test** - Each test should verify one specific behavior
3. **Not using toThrow() correctly** - Must use a function wrapper for exception testing
4. **Forgetting to assert** - Every test needs an expectation
5. **Not using beforeEach** - Create fresh instances for test isolation
6. **Magic numbers** - Use meaningful test values that make the test clear

## Tips for Success

- Write test names that describe what they test
- Use the Arrange-Act-Assert pattern in each test
- Run tests frequently as you write them
- Check coverage after each new test to see what's still missing
- Use describe blocks to group related tests
- Use test.each for testing multiple similar cases (advanced)

## Example: Testing Floating Point Results

When testing floating point results, use `toBeCloseTo()`:

```javascript
test("should calculate square root of positive number", () => {
  const result = calc.sqrt(16);
  expect(result).toBeCloseTo(4.0);
});

test("should divide resulting in decimal", () => {
  const result = calc.divide(10, 3);
  expect(result).toBeCloseTo(3.333333, 5);
});
```

## Submission

Submit the following files:

- `calculator.js` - Your Calculator implementation (with additional methods)
- `calculator.test.js` - Your complete test suite
- Screenshot of coverage report showing 100% coverage

## Next Steps

After completing this exercise:

- Move on to [Exercise 2: Shopping Cart](./02-shopping-cart.md) for class testing
- Review [Module Theory: Statement Coverage](../theory/02-statement-coverage.md)
- Learn about branch coverage and why statement coverage alone isn't enough
