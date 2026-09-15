# Exercise 1: Basic Parametrization (JavaScript)

## Objective

Learn to write parameterized tests using Jest's `test.each()`.

## Part 1: Simple Parametrization

**calculator.js**:

```javascript
function add(a, b) {
  return a + b;
}

function subtract(a, b) {
  return a - b;
}

function multiply(a, b) {
  return a * b;
}

function divide(a, b) {
  if (b === 0) {
    throw new Error("Cannot divide by zero");
  }
  return a / b;
}

module.exports = { add, subtract, multiply, divide };
```

**calculator.test.js**:

```javascript
const { add, subtract, multiply, divide } = require("./calculator");

// TODO: Implement parameterized tests

test.each([
  // Add your test cases here
  [2, 3, 5],
  [-1, 1, 0],
  [0, 0, 0],
])("add(%i, %i) should equal %i", (a, b, expected) => {
  expect(add(a, b)).toBe(expected);
});

// TODO: Implement test.each for subtract, multiply, divide
```

### Requirements

1. Test each function with at least 5 different inputs
2. Test division by zero with `expect().toThrow()`
3. Use descriptive test names

## Part 2: Table Syntax

```javascript
test.each`
  a     | b    | expected
  ${2}  | ${3} | ${5}
  ${1}  | ${1} | ${2}
  ${-1} | ${1} | ${0}
`("$a + $b equals $expected", ({ a, b, expected }) => {
  expect(add(a, b)).toBe(expected);
});
```

## Part 3: Object Arrays

**stringOps.js**:

```javascript
function reverseString(str) {
  return str.split("").reverse().join("");
}

function isPalindrome(str) {
  const cleaned = str.toLowerCase().replace(/\s/g, "");
  return cleaned === cleaned.split("").reverse().join("");
}

function countVowels(str) {
  return (str.match(/[aeiou]/gi) || []).length;
}

module.exports = { reverseString, isPalindrome, countVowels };
```

**stringOps.test.js**:

```javascript
const { reverseString, isPalindrome, countVowels } = require("./stringOps");

test.each([
  { input: "hello", expected: "olleh" },
  { input: "world", expected: "dlrow" },
  { input: "", expected: "" },
  { input: "a", expected: "a" },
])("reverseString($input) should return $expected", ({ input, expected }) => {
  expect(reverseString(input)).toBe(expected);
});

// TODO: Implement tests for isPalindrome and countVowels
```

## Expected Output

```bash
$ npm test

 PASS  ./calculator.test.js
  ✓ add(2, 3) should equal 5
  ✓ add(-1, 1) should equal 0
  ✓ add(0, 0) should equal 0
  ...

Test Suites: 1 passed, 1 total
Tests:       20 passed, 20 total
```

## Grading

- Implementation: 40%
- Test coverage: 30%
- Use of parametrization: 20%
- Code quality: 10%
