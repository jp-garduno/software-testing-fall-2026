# Exercise 1: FizzBuzz Kata

**Module**: 6 - Test Driven Development  
**Difficulty**: Beginner  
**Time**: 30-45 minutes

---

## 🎯 Objectives

Master the TDD cycle by implementing the classic FizzBuzz kata.

By completing this exercise, you will:

- Practice the Red-Green-Refactor cycle
- Write tests before implementation
- Take small, incremental steps
- Experience the rhythm of TDD
- Build confidence in test-first development

---

## Problem Description

Write a program that prints the numbers from 1 to 100. But for multiples of three, print "Fizz" instead of the number, and for multiples of five, print "Buzz". For numbers which are multiples of both three and five, print "FizzBuzz".

### Rules

1. If the number is divisible by 3, return "Fizz"
2. If the number is divisible by 5, return "Buzz"
3. If the number is divisible by both 3 and 5, return "FizzBuzz"
4. Otherwise, return the number as a string

### Examples

```
fizzbuzz(1) → "1"
fizzbuzz(2) → "2"
fizzbuzz(3) → "Fizz"
fizzbuzz(4) → "4"
fizzbuzz(5) → "Buzz"
fizzbuzz(15) → "FizzBuzz"
fizzbuzz(30) → "FizzBuzz"
```

---

## Why FizzBuzz?

FizzBuzz is the perfect introductory kata because:

- **Simple rules**: Easy to understand
- **Clear requirements**: No ambiguity
- **Natural progression**: Requirements build on each other
- **Quick completion**: Can finish in 30-45 minutes
- **Instant feedback**: Tests clearly pass or fail

---

## The TDD Cycle

Remember the three phases:

1. **RED**: Write a failing test
2. **GREEN**: Write the simplest code to make it pass
3. **REFACTOR**: Improve the code without changing behavior

**Important**: Never write production code without a failing test first!

---

## Step-by-Step TDD Instructions

Follow these steps exactly. Do NOT skip ahead!

### Step 1: Simplest Case - Return "1"

**Test First**:

```python
# Python
def test_returns_one():
    assert fizzbuzz(1) == "1"
```

```javascript
// JavaScript
test("returns 1 for input 1", () => {
  expect(fizzbuzz(1)).toBe("1");
});
```

**Run the test**: It should FAIL (RED) because `fizzbuzz` doesn't exist yet.

**Simplest Implementation**:

```python
# Python
def fizzbuzz(n):
    return "1"
```

```javascript
// JavaScript
function fizzbuzz(n) {
  return "1";
}
```

**Run the test**: It should PASS (GREEN).

**Refactor**: Nothing to refactor yet.

---

### Step 2: Return the Number as String

**Test First**:

```python
def test_returns_two():
    assert fizzbuzz(2) == "2"
```

```javascript
test("returns 2 for input 2", () => {
  expect(fizzbuzz(2)).toBe("2");
});
```

**Run the test**: It should FAIL (RED).

**Implementation**:

```python
def fizzbuzz(n):
    return str(n)
```

```javascript
function fizzbuzz(n) {
  return n.toString();
}
```

**Run ALL tests**: Both should PASS (GREEN).

**Refactor**: Code is simple, nothing to refactor.

---

### Step 3: Multiples of 3 Return "Fizz"

**Test First**:

```python
def test_returns_fizz_for_three():
    assert fizzbuzz(3) == "Fizz"
```

```javascript
test("returns Fizz for 3", () => {
  expect(fizzbuzz(3)).toBe("Fizz");
});
```

**Run the test**: It should FAIL (RED).

**Implementation**:

```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    return str(n)
```

```javascript
function fizzbuzz(n) {
  if (n % 3 === 0) {
    return "Fizz";
  }
  return n.toString();
}
```

**Run ALL tests**: All should PASS (GREEN).

**Refactor**: Consider adding another test for multiples of 3:

```python
def test_returns_fizz_for_six():
    assert fizzbuzz(6) == "Fizz"
```

---

### Step 4: Multiples of 5 Return "Buzz"

**Test First**:

```python
def test_returns_buzz_for_five():
    assert fizzbuzz(5) == "Buzz"
```

```javascript
test("returns Buzz for 5", () => {
  expect(fizzbuzz(5)).toBe("Buzz");
});
```

**Run the test**: It should FAIL (RED).

**Implementation**:

```python
def fizzbuzz(n):
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

```javascript
function fizzbuzz(n) {
  if (n % 3 === 0) {
    return "Fizz";
  }
  if (n % 5 === 0) {
    return "Buzz";
  }
  return n.toString();
}
```

**Run ALL tests**: All should PASS (GREEN).

**Refactor**: Add test for another multiple of 5:

```python
def test_returns_buzz_for_ten():
    assert fizzbuzz(10) == "Buzz"
```

---

### Step 5: Multiples of Both 3 and 5 Return "FizzBuzz"

**Test First**:

```python
def test_returns_fizzbuzz_for_fifteen():
    assert fizzbuzz(15) == "FizzBuzz"
```

```javascript
test("returns FizzBuzz for 15", () => {
  expect(fizzbuzz(15)).toBe("FizzBuzz");
});
```

**Run the test**: It should FAIL (RED) - it returns "Fizz" instead.

**Implementation** (Fix the order!):

```python
def fizzbuzz(n):
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

```javascript
function fizzbuzz(n) {
  if (n % 3 === 0 && n % 5 === 0) {
    return "FizzBuzz";
  }
  if (n % 3 === 0) {
    return "Fizz";
  }
  if (n % 5 === 0) {
    return "Buzz";
  }
  return n.toString();
}
```

**Run ALL tests**: All should PASS (GREEN).

**Refactor**: Consider this alternative:

```python
def fizzbuzz(n):
    if n % 15 == 0:  # More efficient
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)
```

Or a different approach:

```python
def fizzbuzz(n):
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    return result if result else str(n)
```

**Run ALL tests**: Should still PASS after refactoring.

---

## Complete Test Suite

Here's what your final test suite should look like:

### Python (pytest)

```python
import pytest

def fizzbuzz(n):
    """
    Returns FizzBuzz string for given number.
    """
    if n % 15 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)


def test_returns_one():
    assert fizzbuzz(1) == "1"


def test_returns_two():
    assert fizzbuzz(2) == "2"


def test_returns_fizz_for_three():
    assert fizzbuzz(3) == "Fizz"


def test_returns_fizz_for_six():
    assert fizzbuzz(6) == "Fizz"


def test_returns_fizz_for_nine():
    assert fizzbuzz(9) == "Fizz"


def test_returns_buzz_for_five():
    assert fizzbuzz(5) == "Buzz"


def test_returns_buzz_for_ten():
    assert fizzbuzz(10) == "Buzz"


def test_returns_buzz_for_twenty():
    assert fizzbuzz(20) == "Buzz"


def test_returns_fizzbuzz_for_fifteen():
    assert fizzbuzz(15) == "FizzBuzz"


def test_returns_fizzbuzz_for_thirty():
    assert fizzbuzz(30) == "FizzBuzz"


def test_returns_fizzbuzz_for_fortyfive():
    assert fizzbuzz(45) == "FizzBuzz"


def test_returns_number_for_non_multiple():
    assert fizzbuzz(7) == "7"
    assert fizzbuzz(11) == "11"
    assert fizzbuzz(13) == "13"
```

### JavaScript (Jest)

```javascript
function fizzbuzz(n) {
  if (n % 15 === 0) {
    return "FizzBuzz";
  }
  if (n % 3 === 0) {
    return "Fizz";
  }
  if (n % 5 === 0) {
    return "Buzz";
  }
  return n.toString();
}

describe("FizzBuzz Kata", () => {
  test("returns 1 for input 1", () => {
    expect(fizzbuzz(1)).toBe("1");
  });

  test("returns 2 for input 2", () => {
    expect(fizzbuzz(2)).toBe("2");
  });

  test("returns Fizz for 3", () => {
    expect(fizzbuzz(3)).toBe("Fizz");
  });

  test("returns Fizz for 6", () => {
    expect(fizzbuzz(6)).toBe("Fizz");
  });

  test("returns Fizz for 9", () => {
    expect(fizzbuzz(9)).toBe("Fizz");
  });

  test("returns Buzz for 5", () => {
    expect(fizzbuzz(5)).toBe("Buzz");
  });

  test("returns Buzz for 10", () => {
    expect(fizzbuzz(10)).toBe("Buzz");
  });

  test("returns Buzz for 20", () => {
    expect(fizzbuzz(20)).toBe("Buzz");
  });

  test("returns FizzBuzz for 15", () => {
    expect(fizzbuzz(15)).toBe("FizzBuzz");
  });

  test("returns FizzBuzz for 30", () => {
    expect(fizzbuzz(30)).toBe("FizzBuzz");
  });

  test("returns FizzBuzz for 45", () => {
    expect(fizzbuzz(45)).toBe("FizzBuzz");
  });

  test("returns number as string for non-multiples", () => {
    expect(fizzbuzz(7)).toBe("7");
    expect(fizzbuzz(11)).toBe("11");
    expect(fizzbuzz(13)).toBe("13");
  });
});

module.exports = fizzbuzz;
```

---

## Running Your Tests

### Python

```bash
# Run tests
pytest test_fizzbuzz.py -v

# Run with coverage
pytest test_fizzbuzz.py --cov=. --cov-report=term-missing
```

### JavaScript

```bash
# Run tests
npm test fizzbuzz.test.js

# Run with coverage
npm test -- --coverage fizzbuzz.test.js
```

---

## Evaluation Criteria

Your solution will be evaluated on:

| Criteria               | Points | Description                                     |
| ---------------------- | ------ | ----------------------------------------------- |
| **Followed TDD Cycle** | 30     | Tests written before implementation             |
| **Small Steps**        | 20     | Incremental progress, no big jumps              |
| **All Tests Pass**     | 20     | Complete test suite passes                      |
| **Code Quality**       | 15     | Clean, readable, well-refactored                |
| **Test Coverage**      | 15     | Edge cases covered (1, 3, 5, 15, non-multiples) |

**Total**: 100 points

---

## Common Mistakes to Avoid

❌ **Writing all tests at once**  
✅ Write one test, make it pass, then write next test

❌ **Writing implementation before tests**  
✅ Always RED → GREEN → REFACTOR

❌ **Implementing more than needed**  
✅ Write simplest code to pass current test

❌ **Not running tests frequently**  
✅ Run tests after every code change

❌ **Skipping the refactor step**  
✅ Clean up code while tests are green

❌ **Testing the same behavior multiple times**  
✅ Each test should verify different behavior

---

## Tips for Success

1. **Start Simple**: Begin with `fizzbuzz(1) == "1"`
2. **One Test at a Time**: Write test, watch it fail, make it pass
3. **Baby Steps**: Don't jump ahead to complex cases
4. **Run Tests Often**: After every change
5. **Refactor Fearlessly**: Tests protect you
6. **Delete Dead Code**: If test passes without it, remove it
7. **Read Error Messages**: They tell you what to do next
8. **Commit After Each Step**: Version control your progress

---

## Bonus Challenges

After completing the basic kata, try these extensions:

### Challenge 1: FizzBuzzBazz

Add a new rule: If divisible by 7, return "Bazz"

- 7 → "Bazz"
- 21 → "FizzBazz" (divisible by 3 and 7)
- 35 → "BuzzBazz" (divisible by 5 and 7)
- 105 → "FizzBuzzBazz" (divisible by 3, 5, and 7)

### Challenge 2: Configurable FizzBuzz

Make it configurable:

```python
def fizzbuzz(n, rules=None):
    if rules is None:
        rules = {3: "Fizz", 5: "Buzz"}
    # Implement configurable version
```

### Challenge 3: FizzBuzz Range

Generate FizzBuzz for a range:

```python
def fizzbuzz_range(start, end):
    """Returns list of FizzBuzz values from start to end"""
    return [fizzbuzz(n) for n in range(start, end + 1)]
```

Test with:

```python
def test_fizzbuzz_range():
    result = fizzbuzz_range(1, 15)
    expected = ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8",
                "Fizz", "Buzz", "11", "Fizz", "13", "14", "FizzBuzz"]
    assert result == expected
```

---

## Reflection Questions

After completing the kata, answer these:

1. **Did you feel the TDD rhythm?** (Red → Green → Refactor)
2. **What was the hardest part?** Writing tests first? Simplest implementation?
3. **How many times did you refactor?** What did you improve?
4. **Did any tests catch bugs?** When did they help?
5. **Would you have written the same code without tests?**

---

## Deliverables

Submit:

1. **Complete implementation** with all tests passing
2. **Git commit history** showing TDD progression (one commit per test)
3. **Test coverage report** (should be 100%)
4. **Brief reflection** (2-3 paragraphs) on your TDD experience

---

## Next Steps

After mastering FizzBuzz:

1. Practice [Exercise 2: String Calculator Kata](./02-string-calculator.md)
2. Review [Theory: TDD Cycle](../theory/01-tdd-cycle.md)
3. Read about [Red-Green-Refactor](../theory/02-red-green-refactor.md)
4. Try FizzBuzz again in 15 minutes to internalize the pattern

---

## Resources

- [TDD by Example](https://www.oreilly.com/library/view/test-driven-development/0321146530/) - Kent Beck
- [FizzBuzz in TDD Explained](http://www.codekatas.org/catas/kata-fizzbuzz) - Dave Thomas
- [Why FizzBuzz?](https://blog.codinghorror.com/why-cant-programmers-program/)

---

**Remember: TDD is not about testing, it's about design. The tests are a happy side effect!**
