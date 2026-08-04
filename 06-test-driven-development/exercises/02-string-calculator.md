# Exercise 2: String Calculator Kata

**Module**: 6 - Test Driven Development  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice TDD with progressive requirements and exception handling.

By completing this exercise, you will:

- Handle evolving requirements through TDD
- Practice exception-driven development
- Work with string parsing and validation
- Make design decisions guided by tests
- Refactor complex logic safely

---

## Problem Description

Create a simple String Calculator with an `add()` method that takes a string of numbers and returns their sum.

This kata has **progressive requirements** - implement them one at a time using TDD!

---

## Why String Calculator?

This kata is famous because it:

- **Builds complexity gradually**: Each requirement adds new behavior
- **Real-world scenario**: Parsing user input is common
- **Forces design decisions**: How to structure code?
- **Teaches exception handling**: How to test error cases?
- **Multiple solutions**: No single "right" answer

Created by Roy Osherove, this is one of the most popular TDD katas worldwide.

---

## Progressive Requirements

Implement these requirements **IN ORDER**. Complete each one before moving to the next!

### Requirement 1: Empty String Returns 0

**Method signature**: `add(numbers: str) -> int`

```python
add("") → 0
```

### Requirement 2: Single Number Returns the Number

```python
add("1") → 1
add("5") → 5
```

### Requirement 3: Two Numbers Separated by Comma

```python
add("1,2") → 3
add("5,10") → 15
```

### Requirement 4: Handle Unknown Amount of Numbers

```python
add("1,2,3") → 6
add("1,2,3,4,5") → 15
```

### Requirement 5: Handle Newline as Delimiter

```python
add("1\n2,3") → 6
add("1\n2\n3") → 6
```

### Requirement 6: Custom Delimiters

Support custom delimiter specification: `//[delimiter]\n[numbers]`

```python
add("//;\n1;2") → 3
add("//|\n1|2|3") → 6
add("//*\n1*2*3") → 6
```

### Requirement 7: Negative Numbers Throw Exception

```python
add("-1,2") → raises exception "negatives not allowed: -1"
add("1,-2,-3") → raises exception "negatives not allowed: -2, -3"
```

### Requirement 8: Numbers Greater Than 1000 Are Ignored

```python
add("2,1001") → 2
add("1000,1001,2") → 1002
```

### Requirement 9: Delimiters of Any Length

```python
add("//[***]\n1***2***3") → 6
add("//[---]\n1---2---3") → 6
```

### Requirement 10: Multiple Delimiters

```python
add("//[*][%]\n1*2%3") → 6
add("//[**][%%]\n1**2%%3") → 6
```

---

## Step-by-Step TDD Guide

### Step 1: Empty String

**Test First**:

```python
# Python
def test_empty_string_returns_zero():
    calculator = StringCalculator()
    assert calculator.add("") == 0
```

```javascript
// JavaScript
test("empty string returns 0", () => {
  const calculator = new StringCalculator();
  expect(calculator.add("")).toBe(0);
});
```

**Implementation**:

```python
class StringCalculator:
    def add(self, numbers: str) -> int:
        return 0
```

```javascript
class StringCalculator {
  add(numbers) {
    return 0;
  }
}
```

---

### Step 2: Single Number

**Test First**:

```python
def test_single_number_returns_itself():
    calculator = StringCalculator()
    assert calculator.add("1") == 1
    assert calculator.add("5") == 5
```

```javascript
test("single number returns itself", () => {
  const calculator = new StringCalculator();
  expect(calculator.add("1")).toBe(1);
  expect(calculator.add("5")).toBe(5);
});
```

**Implementation**:

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0
    return int(numbers)
```

```javascript
add(numbers) {
  if (numbers === "") {
    return 0;
  }
  return parseInt(numbers);
}
```

---

### Step 3: Two Numbers

**Test First**:

```python
def test_two_numbers_comma_separated():
    calculator = StringCalculator()
    assert calculator.add("1,2") == 3
    assert calculator.add("5,10") == 15
```

```javascript
test("two numbers separated by comma", () => {
  const calculator = new StringCalculator();
  expect(calculator.add("1,2")).toBe(3);
  expect(calculator.add("5,10")).toBe(15);
});
```

**Implementation**:

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0
    if "," in numbers:
        parts = numbers.split(",")
        return int(parts[0]) + int(parts[1])
    return int(numbers)
```

```javascript
add(numbers) {
  if (numbers === "") {
    return 0;
  }
  if (numbers.includes(",")) {
    const parts = numbers.split(",");
    return parseInt(parts[0]) + parseInt(parts[1]);
  }
  return parseInt(numbers);
}
```

---

### Step 4: Unknown Amount of Numbers

**Test First**:

```python
def test_handles_multiple_numbers():
    calculator = StringCalculator()
    assert calculator.add("1,2,3") == 6
    assert calculator.add("1,2,3,4,5") == 15
```

**Implementation** (Refactor to use loop):

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0
    parts = numbers.split(",")
    return sum(int(part) for part in parts)
```

```javascript
add(numbers) {
  if (numbers === "") {
    return 0;
  }
  const parts = numbers.split(",");
  return parts.reduce((sum, part) => sum + parseInt(part), 0);
}
```

---

### Step 5: Newline Delimiter

**Test First**:

```python
def test_handles_newline_delimiter():
    calculator = StringCalculator()
    assert calculator.add("1\n2,3") == 6
    assert calculator.add("1\n2\n3") == 6
```

**Implementation**:

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0
    # Replace newlines with commas
    numbers = numbers.replace("\n", ",")
    parts = numbers.split(",")
    return sum(int(part) for part in parts)
```

```javascript
add(numbers) {
  if (numbers === "") {
    return 0;
  }
  numbers = numbers.replace(/\n/g, ",");
  const parts = numbers.split(",");
  return parts.reduce((sum, part) => sum + parseInt(part), 0);
}
```

---

### Step 6: Custom Delimiters

**Test First**:

```python
def test_custom_delimiter():
    calculator = StringCalculator()
    assert calculator.add("//;\n1;2") == 3
    assert calculator.add("//|\n1|2|3") == 6
```

**Implementation**:

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0

    delimiter = ","

    # Check for custom delimiter
    if numbers.startswith("//"):
        delimiter_end = numbers.index("\n")
        delimiter = numbers[2:delimiter_end]
        numbers = numbers[delimiter_end + 1:]

    # Replace newlines and custom delimiters with commas
    numbers = numbers.replace("\n", ",")
    if delimiter != ",":
        numbers = numbers.replace(delimiter, ",")

    parts = numbers.split(",")
    return sum(int(part) for part in parts)
```

```javascript
add(numbers) {
  if (numbers === "") {
    return 0;
  }

  let delimiter = ",";

  // Check for custom delimiter
  if (numbers.startsWith("//")) {
    const delimiterEnd = numbers.indexOf("\n");
    delimiter = numbers.substring(2, delimiterEnd);
    numbers = numbers.substring(delimiterEnd + 1);
  }

  // Replace newlines and custom delimiter
  numbers = numbers.replace(/\n/g, ",");
  if (delimiter !== ",") {
    const delimiterRegex = new RegExp(
      delimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"),
      "g"
    );
    numbers = numbers.replace(delimiterRegex, ",");
  }

  const parts = numbers.split(",");
  return parts.reduce((sum, part) => sum + parseInt(part), 0);
}
```

---

### Step 7: Negative Numbers

**Test First**:

```python
def test_negative_numbers_throw_exception():
    calculator = StringCalculator()

    with pytest.raises(ValueError, match="negatives not allowed: -1"):
        calculator.add("-1,2")

    with pytest.raises(ValueError, match="negatives not allowed: -2, -3"):
        calculator.add("1,-2,-3")
```

```javascript
test("negative numbers throw exception", () => {
  const calculator = new StringCalculator();

  expect(() => calculator.add("-1,2")).toThrow("negatives not allowed: -1");
  expect(() => calculator.add("1,-2,-3")).toThrow(
    "negatives not allowed: -2, -3",
  );
});
```

**Implementation**:

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0

    delimiter = ","

    if numbers.startswith("//"):
        delimiter_end = numbers.index("\n")
        delimiter = numbers[2:delimiter_end]
        numbers = numbers[delimiter_end + 1:]

    numbers = numbers.replace("\n", ",")
    if delimiter != ",":
        numbers = numbers.replace(delimiter, ",")

    parts = numbers.split(",")
    int_parts = [int(part) for part in parts]

    # Check for negatives
    negatives = [n for n in int_parts if n < 0]
    if negatives:
        neg_str = ", ".join(map(str, negatives))
        raise ValueError(f"negatives not allowed: {neg_str}")

    return sum(int_parts)
```

---

### Step 8: Ignore Numbers > 1000

**Test First**:

```python
def test_ignores_numbers_greater_than_1000():
    calculator = StringCalculator()
    assert calculator.add("2,1001") == 2
    assert calculator.add("1000,1001,2") == 1002
```

**Implementation** (Add filter):

```python
def add(self, numbers: str) -> int:
    # ... (previous parsing code)

    int_parts = [int(part) for part in parts]

    # Check for negatives
    negatives = [n for n in int_parts if n < 0]
    if negatives:
        neg_str = ", ".join(map(str, negatives))
        raise ValueError(f"negatives not allowed: {neg_str}")

    # Ignore numbers > 1000
    valid_numbers = [n for n in int_parts if n <= 1000]

    return sum(valid_numbers)
```

---

### Step 9: Delimiters of Any Length

**Test First**:

```python
def test_delimiter_any_length():
    calculator = StringCalculator()
    assert calculator.add("//[***]\n1***2***3") == 6
    assert calculator.add("//[---]\n1---2---3") == 6
```

**Implementation** (Update delimiter parsing):

```python
def add(self, numbers: str) -> int:
    if numbers == "":
        return 0

    delimiter = ","

    if numbers.startswith("//"):
        delimiter_end = numbers.index("\n")
        delimiter_spec = numbers[2:delimiter_end]

        # Check for bracket notation
        if delimiter_spec.startswith("[") and delimiter_spec.endswith("]"):
            delimiter = delimiter_spec[1:-1]
        else:
            delimiter = delimiter_spec

        numbers = numbers[delimiter_end + 1:]

    # ... rest of code
```

---

### Step 10: Multiple Delimiters

**Test First**:

```python
def test_multiple_delimiters():
    calculator = StringCalculator()
    assert calculator.add("//[*][%]\n1*2%3") == 6
    assert calculator.add("//[**][%%]\n1**2%%3") == 6
```

**Implementation**:

```python
import re

def add(self, numbers: str) -> int:
    if numbers == "":
        return 0

    delimiters = [","]

    if numbers.startswith("//"):
        delimiter_end = numbers.index("\n")
        delimiter_spec = numbers[2:delimiter_end]

        # Parse multiple delimiters in brackets
        bracket_pattern = r'\[([^\]]+)\]'
        matches = re.findall(bracket_pattern, delimiter_spec)

        if matches:
            delimiters = matches
        else:
            delimiters = [delimiter_spec]

        numbers = numbers[delimiter_end + 1:]

    # Replace all delimiters with commas
    numbers = numbers.replace("\n", ",")
    for delimiter in delimiters:
        numbers = numbers.replace(delimiter, ",")

    parts = [part for part in numbers.split(",") if part]
    int_parts = [int(part) for part in parts]

    # Check for negatives
    negatives = [n for n in int_parts if n < 0]
    if negatives:
        neg_str = ", ".join(map(str, negatives))
        raise ValueError(f"negatives not allowed: {neg_str}")

    # Ignore numbers > 1000
    valid_numbers = [n for n in int_parts if n <= 1000]

    return sum(valid_numbers)
```

---

## Complete Solution Templates

### Python (pytest)

```python
import re
import pytest


class StringCalculator:
    def add(self, numbers: str) -> int:
        """
        Adds numbers from a string.

        Args:
            numbers: String containing numbers to add

        Returns:
            Sum of valid numbers

        Raises:
            ValueError: If negative numbers are provided
        """
        if numbers == "":
            return 0

        delimiters = [","]

        # Parse custom delimiter(s)
        if numbers.startswith("//"):
            delimiter_end = numbers.index("\n")
            delimiter_spec = numbers[2:delimiter_end]

            # Multiple delimiters in brackets
            bracket_pattern = r'\[([^\]]+)\]'
            matches = re.findall(bracket_pattern, delimiter_spec)

            if matches:
                delimiters = matches
            else:
                delimiters = [delimiter_spec]

            numbers = numbers[delimiter_end + 1:]

        # Replace all delimiters with commas
        numbers = numbers.replace("\n", ",")
        for delimiter in delimiters:
            numbers = numbers.replace(delimiter, ",")

        # Parse numbers
        parts = [part for part in numbers.split(",") if part]
        int_parts = [int(part) for part in parts]

        # Check for negatives
        negatives = [n for n in int_parts if n < 0]
        if negatives:
            neg_str = ", ".join(map(str, negatives))
            raise ValueError(f"negatives not allowed: {neg_str}")

        # Ignore numbers > 1000
        valid_numbers = [n for n in int_parts if n <= 1000]

        return sum(valid_numbers)


# Tests
class TestStringCalculator:
    def test_empty_string_returns_zero(self):
        calc = StringCalculator()
        assert calc.add("") == 0

    def test_single_number(self):
        calc = StringCalculator()
        assert calc.add("1") == 1
        assert calc.add("5") == 5

    def test_two_numbers(self):
        calc = StringCalculator()
        assert calc.add("1,2") == 3
        assert calc.add("5,10") == 15

    def test_multiple_numbers(self):
        calc = StringCalculator()
        assert calc.add("1,2,3") == 6
        assert calc.add("1,2,3,4,5") == 15

    def test_newline_delimiter(self):
        calc = StringCalculator()
        assert calc.add("1\n2,3") == 6
        assert calc.add("1\n2\n3") == 6

    def test_custom_delimiter(self):
        calc = StringCalculator()
        assert calc.add("//;\n1;2") == 3
        assert calc.add("//|\n1|2|3") == 6

    def test_negative_numbers_throw_exception(self):
        calc = StringCalculator()

        with pytest.raises(ValueError, match="negatives not allowed: -1"):
            calc.add("-1,2")

        with pytest.raises(ValueError, match=r"negatives not allowed: -2, -3"):
            calc.add("1,-2,-3")

    def test_ignore_numbers_greater_than_1000(self):
        calc = StringCalculator()
        assert calc.add("2,1001") == 2
        assert calc.add("1000,1001,2") == 1002

    def test_delimiter_any_length(self):
        calc = StringCalculator()
        assert calc.add("//[***]\n1***2***3") == 6
        assert calc.add("//[---]\n1---2---3") == 6

    def test_multiple_delimiters(self):
        calc = StringCalculator()
        assert calc.add("//[*][%]\n1*2%3") == 6
        assert calc.add("//[**][%%]\n1**2%%3") == 6
```

### JavaScript (Jest)

```javascript
class StringCalculator {
  add(numbers) {
    if (numbers === "") {
      return 0;
    }

    let delimiters = [","];

    // Parse custom delimiter(s)
    if (numbers.startsWith("//")) {
      const delimiterEnd = numbers.indexOf("\n");
      const delimiterSpec = numbers.substring(2, delimiterEnd);

      // Multiple delimiters in brackets
      const bracketPattern = /\[([^\]]+)\]/g;
      const matches = [...delimiterSpec.matchAll(bracketPattern)];

      if (matches.length > 0) {
        delimiters = matches.map((m) => m[1]);
      } else {
        delimiters = [delimiterSpec];
      }

      numbers = numbers.substring(delimiterEnd + 1);
    }

    // Replace all delimiters with commas
    numbers = numbers.replace(/\n/g, ",");
    delimiters.forEach((delimiter) => {
      const escapedDelimiter = delimiter.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      numbers = numbers.replace(new RegExp(escapedDelimiter, "g"), ",");
    });

    // Parse numbers
    const parts = numbers.split(",").filter((p) => p !== "");
    const intParts = parts.map((p) => parseInt(p));

    // Check for negatives
    const negatives = intParts.filter((n) => n < 0);
    if (negatives.length > 0) {
      throw new Error(`negatives not allowed: ${negatives.join(", ")}`);
    }

    // Ignore numbers > 1000
    const validNumbers = intParts.filter((n) => n <= 1000);

    return validNumbers.reduce((sum, n) => sum + n, 0);
  }
}

describe("StringCalculator", () => {
  let calc;

  beforeEach(() => {
    calc = new StringCalculator();
  });

  test("empty string returns 0", () => {
    expect(calc.add("")).toBe(0);
  });

  test("single number returns itself", () => {
    expect(calc.add("1")).toBe(1);
    expect(calc.add("5")).toBe(5);
  });

  test("two numbers comma separated", () => {
    expect(calc.add("1,2")).toBe(3);
    expect(calc.add("5,10")).toBe(15);
  });

  test("handles multiple numbers", () => {
    expect(calc.add("1,2,3")).toBe(6);
    expect(calc.add("1,2,3,4,5")).toBe(15);
  });

  test("handles newline delimiter", () => {
    expect(calc.add("1\n2,3")).toBe(6);
    expect(calc.add("1\n2\n3")).toBe(6);
  });

  test("custom delimiter", () => {
    expect(calc.add("//;\n1;2")).toBe(3);
    expect(calc.add("//|\n1|2|3")).toBe(6);
  });

  test("negative numbers throw exception", () => {
    expect(() => calc.add("-1,2")).toThrow("negatives not allowed: -1");
    expect(() => calc.add("1,-2,-3")).toThrow("negatives not allowed: -2, -3");
  });

  test("ignores numbers greater than 1000", () => {
    expect(calc.add("2,1001")).toBe(2);
    expect(calc.add("1000,1001,2")).toBe(1002);
  });

  test("delimiter of any length", () => {
    expect(calc.add("//[***]\n1***2***3")).toBe(6);
    expect(calc.add("//[---]\n1---2---3")).toBe(6);
  });

  test("multiple delimiters", () => {
    expect(calc.add("//[*][%]\n1*2%3")).toBe(6);
    expect(calc.add("//[**][%%]\n1**2%%3")).toBe(6);
  });
});

module.exports = StringCalculator;
```

---

## Evaluation Criteria

| Criteria               | Points | Description                              |
| ---------------------- | ------ | ---------------------------------------- |
| **TDD Process**        | 25     | Tests written before each requirement    |
| **All Requirements**   | 30     | All 10 requirements implemented          |
| **Exception Handling** | 15     | Negative numbers throw proper exceptions |
| **Code Quality**       | 20     | Clean, well-structured, readable         |
| **Test Coverage**      | 10     | Comprehensive test suite                 |

**Total**: 100 points

---

## Common Mistakes

❌ **Implementing multiple requirements at once**  
✅ One requirement at a time, test-first

❌ **Not refactoring regularly**  
✅ Refactor after each green test

❌ **Hard-coding test values**  
✅ Generic solution that works for all inputs

❌ **Poor error messages**  
✅ Clear, informative exception messages

❌ **Ignoring edge cases**  
✅ Test empty strings, single delimiters, multiple negatives

---

## Tips for Success

1. **Read Only One Requirement**: Don't peek ahead
2. **Write Failing Test First**: RED → GREEN → REFACTOR
3. **Simplest Implementation**: Don't over-engineer
4. **Refactor Often**: Keep code clean
5. **Test Edge Cases**: Empty strings, single values, boundaries
6. **Use Regex Wisely**: Helps with parsing
7. **Meaningful Test Names**: Describe behavior clearly

---

## Bonus Challenges

### Challenge 1: Performance Optimization

Benchmark your solution with 10,000 numbers. Optimize if needed.

### Challenge 2: Error Handling

Add more validation:

- Non-numeric input throws exception
- Malformed delimiter syntax
- Missing newline after delimiter spec

### Challenge 3: Logging

Add logging for debugging:

- Log parsed delimiters
- Log filtered numbers
- Log final sum

---

## Deliverables

1. **Complete implementation** with all 10 requirements
2. **Full test suite** with all tests passing
3. **Git history** showing TDD progression
4. **Refactoring notes** documenting major refactors
5. **Reflection** (1 page) on challenges and learnings

---

## Next Steps

1. Complete [Exercise 3: Bowling Game Kata](./03-bowling-game.md)
2. Review [Theory: Refactoring with Confidence](../theory/03-refactoring.md)
3. Read Roy Osherove's original [String Calculator Kata](http://osherove.com/tdd-kata-1/)
4. Try the kata again in half the time

---

**String Calculator teaches you that requirements change - TDD helps you adapt!**
