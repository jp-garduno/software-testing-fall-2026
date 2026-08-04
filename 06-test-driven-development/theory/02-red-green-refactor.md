# Red-Green-Refactor Cycle

**Module**: 6 - Test-Driven Development  
**Topic**: Mastering the Core TDD Workflow  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand each phase of the Red-Green-Refactor cycle in depth
- Write failing tests that fail for the right reason
- Implement the simplest code to make tests pass
- Refactor code safely with confidence
- Maintain a quick cycle rhythm (minutes, not hours)
- Apply the triangulation technique
- Follow TDD progression in real-world examples
- Practice the String Calculator kata step-by-step

---

## The Red-Green-Refactor Cycle

### The Core of TDD

The Red-Green-Refactor cycle is the heartbeat of TDD:

```
┌─────────┐
│   RED   │  Write a failing test
└────┬────┘
     │
     ▼
┌─────────┐
│  GREEN  │  Make it pass (simplest way)
└────┬────┘
     │
     ▼
┌─────────┐
│ REFACTOR│  Improve the code
└────┬────┘
     │
     └─────► REPEAT
```

**Each phase has a specific purpose and mindset.**

---

## RED Phase: Write a Failing Test

### Purpose

- Define what you want the code to do
- Specify the behavior, not the implementation
- See the test fail for the RIGHT REASON

### Rules

1. **Write the smallest possible test** - Test one thing
2. **Make it fail** - Run it and watch it fail
3. **Fail for the right reason** - "Function not found" not "Wrong result"

### RED Phase Mindset

> "What should this code do? What's the simplest example?"

### Example: RED Phase (Python)

```python
# test_password_validator.py
import pytest

def test_rejects_empty_password():
    """Test doesn't exist yet"""
    validator = PasswordValidator()
    result = validator.validate("")
    assert result.is_valid == False

# Run test → FAILS
# Error: NameError: name 'PasswordValidator' is not defined
# ✅ GOOD! Failed for the right reason (class doesn't exist)
```

### Example: RED Phase (JavaScript)

```javascript
// passwordValidator.test.js
test("rejects empty password", () => {
  const validator = new PasswordValidator();
  const result = validator.validate("");
  expect(result.isValid).toBe(false);
});

// Run test → FAILS
// Error: PasswordValidator is not defined
// ✅ GOOD! Failed for the right reason
```

### Why Watch It Fail?

**Always watch the test fail before writing code!**

Reasons:

1. **Verify test works** - A test that never fails might be broken
2. **See the error message** - Understand what's missing
3. **Confirm right failure** - Should fail because feature missing, not typo
4. **Build confidence** - Know the test is actually testing something

### Bad RED Phase

```python
# ❌ BAD: Test passes immediately (why?)
def test_something():
    result = some_function()
    assert result is not None  # Always True if no exception!

# ❌ BAD: Test is too big
def test_entire_user_flow():
    user = create_user()
    login(user)
    update_profile(user)
    logout(user)
    # Testing too much at once!
```

### Good RED Phase

```python
# ✅ GOOD: Simple, focused test
def test_create_user_returns_user_object():
    user = create_user("alice@example.com")
    assert user.email == "alice@example.com"

# ✅ GOOD: Clear expectation
def test_login_with_invalid_password_returns_false():
    result = login("alice@example.com", "wrong_password")
    assert result == False
```

---

## GREEN Phase: Make It Pass

### Purpose

- Write the **simplest** code to make the test pass
- Don't worry about perfection
- Don't write extra features
- Just make the red turn green

### Rules

1. **Simplest code possible** - Even if it seems "dumb"
2. **No extra features** - Only what the test requires
3. **Fake it if needed** - Return hardcoded values to start
4. **Run test** - Verify it passes

### GREEN Phase Mindset

> "What's the SIMPLEST thing I can do to make this pass?"

### Fake It Till You Make It

Start with the simplest possible implementation:

**Test**:

```python
def test_add_two_numbers():
    assert add(2, 3) == 5
```

**Green - Fake It**:

```python
def add(a, b):
    return 5  # Fake it! Returns exactly what test expects
```

This seems silly, but it:

- Makes test pass
- Lets you move forward
- Will be improved by next test

**Next Test (forces real implementation)**:

```python
def test_add_different_numbers():
    assert add(1, 1) == 2
    assert add(5, 7) == 12
```

**Green - Real Implementation**:

```python
def add(a, b):
    return a + b  # Now we need real logic
```

### Example: GREEN Phase (Python)

```python
# RED: test_password_validator.py
def test_rejects_empty_password():
    validator = PasswordValidator()
    result = validator.validate("")
    assert result.is_valid == False

# GREEN: password_validator.py
class ValidationResult:
    def __init__(self, is_valid):
        self.is_valid = is_valid

class PasswordValidator:
    def validate(self, password):
        return ValidationResult(False)  # Fake it!

# Run test → PASSES ✅
# Yes, we're always returning False. Next test will fix it.
```

### Example: GREEN Phase (JavaScript)

```javascript
// RED: test
test("accepts password with 8 characters", () => {
  const validator = new PasswordValidator();
  const result = validator.validate("password");
  expect(result.isValid).toBe(true);
});

// GREEN: code
class ValidationResult {
  constructor(isValid) {
    this.isValid = isValid;
  }
}

class PasswordValidator {
  validate(password) {
    if (password.length >= 8) {
      return new ValidationResult(true);
    }
    return new ValidationResult(false);
  }
}

// Run test → PASSES ✅
```

### Why Start Simple?

**Benefits of simple implementations**:

1. **Quick feedback** - Get to green fast
2. **Incremental progress** - Small steps reduce errors
3. **Forces next test** - Fake implementations make you write better tests
4. **Prevents over-engineering** - Only build what tests require

### Bad GREEN Phase

```python
# ❌ BAD: Over-engineering
def test_add_two_numbers():
    assert add(2, 3) == 5

def add(a, b):
    # Way too much for one test!
    if not isinstance(a, (int, float)):
        raise TypeError("a must be numeric")
    if not isinstance(b, (int, float)):
        raise TypeError("b must be numeric")
    if a < 0 or b < 0:
        raise ValueError("Negative numbers not allowed")
    result = a + b
    if result > 1000000:
        raise OverflowError("Result too large")
    return result
```

### Good GREEN Phase

```python
# ✅ GOOD: Minimal implementation
def test_add_two_numbers():
    assert add(2, 3) == 5

def add(a, b):
    return a + b  # That's it!

# Add validation ONLY when tests require it
```

---

## REFACTOR Phase: Improve the Code

### Purpose

- Clean up the code WITHOUT changing behavior
- Remove duplication
- Improve readability
- Improve design
- **Tests must still pass!**

### Rules

1. **Run tests constantly** - After each small change
2. **Don't change behavior** - Only change structure
3. **Small steps** - One refactoring at a time
4. **Stop if tests fail** - Undo and try again

### REFACTOR Phase Mindset

> "Can I make this clearer? Can I remove duplication? Can I simplify?"

### What to Refactor

**Code smells to fix**:

- Duplication
- Long methods
- Magic numbers
- Unclear names
- Complex conditionals
- Poor structure

### Example: REFACTOR Phase (Python)

**Before Refactoring**:

```python
def validate_password(password):
    if len(password) < 8:
        return False, "Password too short"
    if not any(c.isupper() for c in password):
        return False, "Need uppercase"
    if not any(c.islower() for c in password):
        return False, "Need lowercase"
    if not any(c.isdigit() for c in password):
        return False, "Need number"
    return True, "Valid"
```

**After Refactoring**:

```python
class PasswordValidator:
    MIN_LENGTH = 8

    def validate(self, password):
        if not self._has_min_length(password):
            return ValidationResult(False, "Password too short")
        if not self._has_uppercase(password):
            return ValidationResult(False, "Need uppercase")
        if not self._has_lowercase(password):
            return ValidationResult(False, "Need lowercase")
        if not self._has_digit(password):
            return ValidationResult(False, "Need number")
        return ValidationResult(True, "Valid")

    def _has_min_length(self, password):
        return len(password) >= self.MIN_LENGTH

    def _has_uppercase(self, password):
        return any(c.isupper() for c in password)

    def _has_lowercase(self, password):
        return any(c.islower() for c in password)

    def _has_digit(self, password):
        return any(c.isdigit() for c in password)

# Run tests → STILL PASS ✅
```

### Example: REFACTOR Phase (JavaScript)

**Before Refactoring**:

```javascript
function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
    if (items[i].discount) {
      total -= items[i].price * items[i].quantity * items[i].discount;
    }
  }
  return total;
}
```

**After Refactoring**:

```javascript
function calculateTotal(items) {
  return items.reduce((total, item) => {
    return total + calculateItemTotal(item);
  }, 0);
}

function calculateItemTotal(item) {
  const subtotal = item.price * item.quantity;
  const discount = item.discount || 0;
  return subtotal * (1 - discount);
}

// Run tests → STILL PASS ✅
```

### Common Refactorings

**1. Extract Method**

```python
# Before
def process_order(order):
    total = sum(item.price * item.quantity for item in order.items)
    tax = total * 0.08
    shipping = 10 if total < 50 else 0
    return total + tax + shipping

# After
def process_order(order):
    subtotal = calculate_subtotal(order.items)
    tax = calculate_tax(subtotal)
    shipping = calculate_shipping(subtotal)
    return subtotal + tax + shipping

def calculate_subtotal(items):
    return sum(item.price * item.quantity for item in items)

def calculate_tax(amount):
    return amount * 0.08

def calculate_shipping(amount):
    return 0 if amount >= 50 else 10
```

**2. Remove Duplication**

```javascript
// Before
function validateEmail(email) {
  if (email.includes("@") && email.includes(".")) {
    return true;
  }
  return false;
}

function validatePhone(phone) {
  if (phone.length === 10 && /^\d+$/.test(phone)) {
    return true;
  }
  return false;
}

// After
function validateEmail(email) {
  return email.includes("@") && email.includes(".");
}

function validatePhone(phone) {
  return phone.length === 10 && /^\d+$/.test(phone);
}
```

**3. Rename for Clarity**

```python
# Before
def calc(x, y, z):
    return x * y * z

# After
def calculate_box_volume(length, width, height):
    return length * width * height
```

### When to Refactor

**After each passing test**:

```
Write test → RED → Write code → GREEN → Refactor → REPEAT
```

**Don't refactor**:

- When tests are RED (fix test first)
- When adding new features (refactor separately)
- When you're not sure (make it work first)

---

## The Cycle Rhythm

### How Long Should Each Phase Take?

**Target**: 30-60 seconds per cycle

```
RED:      10-15 seconds (write simple test)
GREEN:    20-30 seconds (simple code)
REFACTOR: 10-20 seconds (small improvement)
──────────────────────────
TOTAL:    40-65 seconds
```

**If taking longer**:

- Your tests are too big (break them down)
- Your steps are too large (smaller increments)
- You're over-thinking (simplify)

### Example: 5-Minute Session

```
0:00 - Write test for add()
0:15 - Run test (RED)
0:20 - Implement add()
0:35 - Run test (GREEN)
0:45 - Extract constant, rename variable
1:00 - Run tests (still GREEN)

1:00 - Write test for subtract()
1:15 - Run test (RED)
1:20 - Implement subtract()
1:35 - Run test (GREEN)
1:45 - No refactoring needed

1:45 - Write test for multiply()
2:00 - Run test (RED)
2:05 - Implement multiply()
2:20 - Run test (GREEN)
2:30 - Extract calculation logic

... continues ...
```

**In 5 minutes**: 6-8 complete cycles

---

## Triangulation Technique

### What is Triangulation?

**Triangulation**: Use multiple specific examples to force a general solution.

### Why Triangulate?

- Forces you to write real logic (not fake it)
- Reveals patterns
- Ensures correctness

### Example: Triangulation (Python)

**First Test (can fake it)**:

```python
def test_calculate_discount_10_percent():
    discount = calculate_discount(price=100, percentage=10)
    assert discount == 10

def calculate_discount(price, percentage):
    return 10  # Fake it!
```

**Second Test (triangulation)**:

```python
def test_calculate_discount_different_values():
    assert calculate_discount(price=100, percentage=10) == 10
    assert calculate_discount(price=200, percentage=15) == 30
    assert calculate_discount(price=50, percentage=20) == 10

def calculate_discount(price, percentage):
    return price * percentage / 100  # Now we need real formula
```

### Example: Triangulation (JavaScript)

```javascript
// First test
test("isPalindrome returns true for 'racecar'", () => {
  expect(isPalindrome("racecar")).toBe(true);
});

// Could fake it:
function isPalindrome(str) {
  return true; // Passes!
}

// Triangulate with second test
test("isPalindrome returns false for 'hello'", () => {
  expect(isPalindrome("hello")).toBe(false);
});

// Now must implement real logic
function isPalindrome(str) {
  return str === str.split("").reverse().join("");
}
```

---

## Complete Example: String Calculator Kata

### Requirements

Create a `StringCalculator` with an `add` method:

- Empty string returns 0
- Single number returns that number
- Two numbers returns their sum
- Handle any amount of numbers
- Handle newlines as delimiters
- Handle custom delimiters

### Python Implementation (Step-by-Step TDD)

**Cycle 1: Empty String**

```python
# RED
def test_empty_string_returns_zero():
    calculator = StringCalculator()
    assert calculator.add("") == 0

# GREEN
class StringCalculator:
    def add(self, numbers):
        return 0

# Tests pass ✅
```

**Cycle 2: Single Number**

```python
# RED
def test_single_number_returns_value():
    calculator = StringCalculator()
    assert calculator.add("1") == 1
    assert calculator.add("5") == 5

# GREEN
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0
        return int(numbers)

# Tests pass ✅
```

**Cycle 3: Two Numbers**

```python
# RED
def test_two_numbers_returns_sum():
    calculator = StringCalculator()
    assert calculator.add("1,2") == 3
    assert calculator.add("5,10") == 15

# GREEN
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0
        if "," in numbers:
            parts = numbers.split(",")
            return int(parts[0]) + int(parts[1])
        return int(numbers)

# Tests pass ✅
```

**Cycle 4: Multiple Numbers**

```python
# RED
def test_multiple_numbers_returns_sum():
    calculator = StringCalculator()
    assert calculator.add("1,2,3") == 6
    assert calculator.add("1,2,3,4,5") == 15

# GREEN
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0
        parts = numbers.split(",")
        return sum(int(part) for part in parts)

# Tests pass ✅
```

**Cycle 5: Handle Newlines**

```python
# RED
def test_handles_newlines():
    calculator = StringCalculator()
    assert calculator.add("1\n2,3") == 6

# GREEN
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0
        numbers = numbers.replace("\n", ",")
        parts = numbers.split(",")
        return sum(int(part) for part in parts)

# Tests pass ✅
```

**Cycle 6: Custom Delimiter**

```python
# RED
def test_custom_delimiter():
    calculator = StringCalculator()
    assert calculator.add("//;\n1;2") == 3
    assert calculator.add("//|\n1|2|3") == 6

# GREEN
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0

        delimiter = ","
        if numbers.startswith("//"):
            delimiter = numbers[2]
            numbers = numbers.split("\n", 1)[1]

        numbers = numbers.replace("\n", delimiter)
        parts = numbers.split(delimiter)
        return sum(int(part) for part in parts)

# Tests pass ✅

# REFACTOR
class StringCalculator:
    def add(self, numbers):
        if numbers == "":
            return 0

        delimiter, numbers = self._parse_delimiter(numbers)
        numbers = numbers.replace("\n", delimiter)
        return sum(int(n) for n in numbers.split(delimiter))

    def _parse_delimiter(self, numbers):
        if numbers.startswith("//"):
            delimiter = numbers[2]
            numbers = numbers.split("\n", 1)[1]
            return delimiter, numbers
        return ",", numbers

# Tests still pass ✅
```

### JavaScript Implementation (Step-by-Step TDD)

**Complete Implementation**:

```javascript
// stringCalculator.test.js
describe("StringCalculator", () => {
  let calculator;

  beforeEach(() => {
    calculator = new StringCalculator();
  });

  test("empty string returns 0", () => {
    expect(calculator.add("")).toBe(0);
  });

  test("single number returns value", () => {
    expect(calculator.add("1")).toBe(1);
    expect(calculator.add("5")).toBe(5);
  });

  test("two numbers returns sum", () => {
    expect(calculator.add("1,2")).toBe(3);
    expect(calculator.add("5,10")).toBe(15);
  });

  test("multiple numbers returns sum", () => {
    expect(calculator.add("1,2,3")).toBe(6);
    expect(calculator.add("1,2,3,4,5")).toBe(15);
  });

  test("handles newlines as delimiters", () => {
    expect(calculator.add("1\n2,3")).toBe(6);
    expect(calculator.add("1\n2\n3")).toBe(6);
  });

  test("supports custom delimiter", () => {
    expect(calculator.add("//;\n1;2")).toBe(3);
    expect(calculator.add("//|\n1|2|3")).toBe(6);
  });
});

// stringCalculator.js
class StringCalculator {
  add(numbers) {
    if (numbers === "") {
      return 0;
    }

    const { delimiter, nums } = this._parseDelimiter(numbers);
    const normalizedNums = nums.replace(/\n/g, delimiter);
    const parts = normalizedNums.split(delimiter);

    return parts.reduce((sum, num) => sum + parseInt(num, 10), 0);
  }

  _parseDelimiter(numbers) {
    if (numbers.startsWith("//")) {
      const delimiter = numbers[2];
      const nums = numbers.split("\n").slice(1).join("\n");
      return { delimiter, nums };
    }
    return { delimiter: ",", nums: numbers };
  }
}

module.exports = StringCalculator;
```

---

## Commit History Showing TDD Progression

### Git Commits During TDD

Good practice: Commit after each passing test

```bash
git commit -m "RED: Add test for empty string"
git commit -m "GREEN: Return 0 for empty string"

git commit -m "RED: Add test for single number"
git commit -m "GREEN: Parse and return single number"

git commit -m "RED: Add test for two numbers"
git commit -m "GREEN: Split and sum two numbers"

git commit -m "RED: Add test for multiple numbers"
git commit -m "GREEN: Handle any amount of numbers"
git commit -m "REFACTOR: Use sum() for cleaner code"

git commit -m "RED: Add test for newlines"
git commit -m "GREEN: Replace newlines with commas"

git commit -m "RED: Add test for custom delimiter"
git commit -m "GREEN: Parse custom delimiter"
git commit -m "REFACTOR: Extract delimiter parsing method"
```

**Benefits**:

- Clear history of development
- Easy to see progression
- Can revert to any point
- Documents thought process

---

## Common Mistakes in the Cycle

### Mistake 1: Skipping RED

```python
# ❌ BAD: Writing code before test fails
def test_add():
    assert add(2, 3) == 5

def add(a, b):
    return a + b

# Never saw it fail!
```

### Mistake 2: Too Much GREEN

```python
# ❌ BAD: Implementing too much
def test_add():
    assert add(2, 3) == 5

def add(a, b):
    # Way too much!
    if not isinstance(a, (int, float)):
        raise TypeError()
    if not isinstance(b, (int, float)):
        raise TypeError()
    result = a + b
    logging.info(f"Added {a} + {b} = {result}")
    return result
```

### Mistake 3: Skipping REFACTOR

```python
# ❌ BAD: Accumulating technical debt
def validate_user(name, email, age, password):
    if name == "" or name is None or len(name) < 2 or len(name) > 50:
        return False
    if email == "" or email is None or "@" not in email or "." not in email:
        return False
    if age < 0 or age > 150 or not isinstance(age, int):
        return False
    if len(password) < 8 or not any(c.isupper() for c in password):
        return False
    return True

# Should refactor into separate validation methods!
```

### Mistake 4: Refactoring While RED

```python
# ❌ BAD: Test is failing, but you start refactoring
def test_something():
    assert foo() == 42  # FAILS

# Don't refactor now! Fix the test first!
```

---

## Tips for Mastering the Cycle

### 1. Keep Tests Small

One assertion per test (when possible):

```python
# ✅ GOOD
def test_empty_list_has_length_zero():
    assert len([]) == 0

def test_empty_list_is_falsy():
    assert not []

# ❌ BAD (testing multiple things)
def test_empty_list():
    assert len([]) == 0
    assert not []
    assert str([]) == "[]"
```

### 2. Keep Code Changes Small

Make the smallest change to get to green:

```python
# Test fails
def test_is_even():
    assert is_even(2) == True

# ✅ GOOD: Minimal change
def is_even(n):
    return True  # Just make it pass!

# Next test will force real implementation
def test_is_even_with_odd():
    assert is_even(3) == False

# Now implement for real
def is_even(n):
    return n % 2 == 0
```

### 3. Refactor Confidently

Tests give you safety net:

```python
# Before refactoring: Run tests ✅
# Refactor code
# After refactoring: Run tests ✅
# If tests fail: Undo and try again
```

### 4. Take Breaks Between Phases

Mental context switch:

- **RED**: Think like a user (what should it do?)
- **GREEN**: Think like a pragmatist (simplest solution?)
- **REFACTOR**: Think like a craftsperson (how can I improve?)

---

## Key Takeaways

1. **RED**: Write failing test, watch it fail for right reason
2. **GREEN**: Simplest code to pass, fake it if needed
3. **REFACTOR**: Improve code without changing behavior
4. **Rhythm**: 30-60 seconds per cycle
5. **Triangulation**: Multiple examples force general solution
6. **Always run tests**: After each small change
7. **Commit often**: Document TDD progression
8. **Small steps**: Tiny increments reduce errors
9. **Don't skip phases**: Each phase has a purpose
10. **Tests are safety net**: Refactor with confidence

---

## Practice Exercises

### Exercise 1: FizzBuzz (Again)

Implement FizzBuzz using strict Red-Green-Refactor:

- Write one test
- Watch it fail
- Write minimal code
- Watch it pass
- Refactor
- Repeat

Time yourself. Aim for 60 seconds per cycle.

### Exercise 2: String Calculator

Complete the String Calculator kata:

- Follow each cycle shown in this document
- Add negative number validation (throw exception)
- Add support for numbers > 1000 (should be ignored)
- Commit after each green phase

### Exercise 3: Bowling Score

Calculate bowling score using TDD:

- Start with simplest test (all gutter balls)
- Add test for all ones
- Add test for one spare
- Add test for one strike
- Handle 10th frame special cases

### Exercise 4: Refactoring Practice

Take this code and refactor it while keeping tests green:

```python
def process(items, tax_rate, discount_code):
    total = 0
    for item in items:
        total += item["price"] * item["quantity"]
    if discount_code == "SAVE10":
        total = total * 0.9
    elif discount_code == "SAVE20":
        total = total * 0.8
    elif discount_code == "SAVE30":
        total = total * 0.7
    total = total * (1 + tax_rate)
    return total
```

---

## Next Steps

Now that you've mastered the Red-Green-Refactor cycle, learn:

1. **[TDD Best Practices](./03-tdd-best-practices.md)** - How to do TDD excellently
2. **[TDD Anti-Patterns](./04-tdd-anti-patterns.md)** - Mistakes to avoid

---

## Additional Resources

- [String Calculator Kata](http://osherove.com/tdd-kata-1/)
- [Bowling Game Kata](http://butunclebob.com/ArticleS.UncleBob.TheBowlingGameKata)
- [TDD by Example - Kent Beck](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)
- [Refactoring - Martin Fowler](https://refactoring.com/)

---

**Remember**: The cycle should be fast and rhythmic. Red-Green-Refactor is a dance, not a marathon! 💃
