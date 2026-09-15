# Boundary Value Analysis

**Module**: 4 - Black Box Testing  
**Topic**: Testing at the Edges  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand why boundaries are where bugs hide
- Identify boundaries in requirements
- Apply BVA to numeric and non-numeric inputs
- Combine BVA with Equivalence Partitioning
- Design comprehensive boundary test cases

---

## What is Boundary Value Analysis?

**Boundary Value Analysis (BVA)** is a black-box testing technique that focuses on testing values at the **edges** (boundaries) of valid input ranges.

### The Core Principle

**Bugs love boundaries.** Most errors occur at the extremes of input ranges, not in the middle.

**Example**: Age validation (18-65)

- ❌ **Equivalence Partitioning alone**: Test age = 40 (middle of range)
- ✅ **BVA**: Test ages = 17, 18, 65, 66 (at and around boundaries)

---

## Why Test Boundaries?

### Common Boundary Bugs

1. **Off-by-one errors**

   ```python
   # Bug: Should be <=, not <
   if age < 65:  # 65-year-olds incorrectly rejected!
       return "valid"
   ```

2. **Incorrect operators**

   ```javascript
   // Bug: Should be >, not >=
   if (score >= 60) {
     // Score of 60 incorrectly passes
     return "pass";
   }
   ```

3. **Edge case handling**
   ```python
   # Bug: Empty list not handled
   def get_average(numbers):
       return sum(numbers) / len(numbers)  # ZeroDivisionError if empty!
   ```

### Real-World Impact

**Knight Capital Loss (2012)**: A boundary condition bug in trading software caused a $440 million loss in 45 minutes.

**Ariane 5 Explosion (1996)**: Integer overflow (boundary error) destroyed a $370 million rocket.

---

## Types of Boundaries

### 1. Numeric Boundaries

**Range: 10 to 50**

Test these values:

- **Below boundary**: 9 (just before minimum)
- **At lower boundary**: 10 (minimum valid)
- **Just above lower**: 11 (first value inside)
- **At upper boundary**: 50 (maximum valid)
- **Just above upper**: 51 (first invalid value)

### 2. String Length Boundaries

**Username: 5-15 characters**

Test these lengths:

- 4 characters (too short)
- 5 characters (minimum valid)
- 6 characters (just above minimum)
- 14 characters (just below maximum)
- 15 characters (maximum valid)
- 16 characters (too long)

### 3. Array/Collection Boundaries

**Shopping cart: 1-10 items**

Test these scenarios:

- 0 items (empty)
- 1 item (minimum)
- 2 items (just above minimum)
- 9 items (just below maximum)
- 10 items (maximum)
- 11 items (over maximum)

---

## BVA Strategy: The 5-Point Method

For any range with **minimum** and **maximum** values:

1. **Min - 1**: Just below the minimum
2. **Min**: At the minimum boundary
3. **Mid**: Typical value (from EP)
4. **Max**: At the maximum boundary
5. **Max + 1**: Just above the maximum

**Example**: Discount percentage (0-100)

```python
def test_discount_boundaries():
    # Min - 1: Invalid
    assert validate_discount(-1) == False

    # Min: Valid boundary
    assert validate_discount(0) == True

    # Mid: Typical value (from EP)
    assert validate_discount(50) == True

    # Max: Valid boundary
    assert validate_discount(100) == True

    # Max + 1: Invalid
    assert validate_discount(101) == False
```

---

## Example 1: Age Validation (18-65)

### Requirement

User age must be between 18 and 65 (inclusive) for account creation.

### Boundary Values

| Test Case | Value | Type               | Expected Result |
| --------- | ----- | ------------------ | --------------- |
| TC1       | 17    | Below minimum      | Rejected        |
| TC2       | 18    | At minimum         | Accepted        |
| TC3       | 19    | Just above minimum | Accepted        |
| TC4       | 40    | Middle (EP)        | Accepted        |
| TC5       | 64    | Just below maximum | Accepted        |
| TC6       | 65    | At maximum         | Accepted        |
| TC7       | 66    | Above maximum      | Rejected        |

### Python Implementation

```python
def validate_age(age):
    if age < 18:
        return False, "Must be at least 18 years old"
    if age > 65:
        return False, "Maximum age is 65"
    return True, "Valid age"

def test_age_boundaries():
    """Test age validation boundaries"""

    # Below minimum
    valid, msg = validate_age(17)
    assert not valid
    assert "at least 18" in msg

    # At minimum boundary
    valid, msg = validate_age(18)
    assert valid

    # Just above minimum
    valid, msg = validate_age(19)
    assert valid

    # Typical value (EP)
    valid, msg = validate_age(40)
    assert valid

    # Just below maximum
    valid, msg = validate_age(64)
    assert valid

    # At maximum boundary
    valid, msg = validate_age(65)
    assert valid

    # Above maximum
    valid, msg = validate_age(66)
    assert not valid
    assert "Maximum age is 65" in msg
```

---

## Example 2: String Length (Password 8-20 characters)

### Requirement

Password must be between 8 and 20 characters (inclusive).

### Boundary Test Cases

```javascript
describe("Password Length Validation", () => {
  const passwords = {
    tooShort: "Pass12@", // 7 chars
    minLength: "Pass123@", // 8 chars (minimum)
    justAboveMin: "Pass1234@", // 9 chars
    typical: "Password123@", // 12 chars
    justBelowMax: "Pass123456789012@", // 19 chars
    maxLength: "Pass1234567890123@", // 20 chars (maximum)
    tooLong: "Pass12345678901234@", // 21 chars
  };

  test("TC1: Below minimum (7 chars) - should fail", () => {
    expect(validatePassword(passwords.tooShort)).toBe(false);
  });

  test("TC2: At minimum (8 chars) - should pass", () => {
    expect(validatePassword(passwords.minLength)).toBe(true);
  });

  test("TC3: Just above minimum (9 chars) - should pass", () => {
    expect(validatePassword(passwords.justAboveMin)).toBe(true);
  });

  test("TC4: Typical length (12 chars) - should pass", () => {
    expect(validatePassword(passwords.typical)).toBe(true);
  });

  test("TC5: Just below maximum (19 chars) - should pass", () => {
    expect(validatePassword(passwords.justBelowMax)).toBe(true);
  });

  test("TC6: At maximum (20 chars) - should pass", () => {
    expect(validatePassword(passwords.maxLength)).toBe(true);
  });

  test("TC7: Above maximum (21 chars) - should fail", () => {
    expect(validatePassword(passwords.tooLong)).toBe(false);
  });
});
```

---

## Example 3: Multiple Boundaries (Loan Amount)

### Requirement

Loan amount must be:

- Minimum: $1,000
- Maximum: $100,000
- Must be multiple of $100

### Boundary Values

| Test Case | Amount   | Type                | Expected |
| --------- | -------- | ------------------- | -------- |
| TC1       | $900     | Below minimum       | Invalid  |
| TC2       | $1,000   | At minimum          | Valid    |
| TC3       | $1,100   | Just above minimum  | Valid    |
| TC4       | $50,000  | Middle              | Valid    |
| TC5       | $99,900  | Just below maximum  | Valid    |
| TC6       | $100,000 | At maximum          | Valid    |
| TC7       | $100,100 | Above maximum       | Invalid  |
| TC8       | $1,050   | Not multiple of 100 | Invalid  |

```python
def validate_loan_amount(amount):
    if amount < 1000:
        return False, "Minimum loan is $1,000"
    if amount > 100000:
        return False, "Maximum loan is $100,000"
    if amount % 100 != 0:
        return False, "Amount must be multiple of $100"
    return True, "Valid loan amount"

def test_loan_boundaries():
    # Below minimum
    assert validate_loan_amount(900)[0] == False

    # At minimum
    assert validate_loan_amount(1000)[0] == True

    # Just above minimum
    assert validate_loan_amount(1100)[0] == True

    # Middle
    assert validate_loan_amount(50000)[0] == True

    # Just below maximum
    assert validate_loan_amount(99900)[0] == True

    # At maximum
    assert validate_loan_amount(100000)[0] == True

    # Above maximum
    assert validate_loan_amount(100100)[0] == False

    # Not multiple of 100
    assert validate_loan_amount(1050)[0] == False
```

---

## Combining BVA with Equivalence Partitioning

### Strategy

1. **Use EP** to identify partitions
2. **Use BVA** to test boundaries between partitions
3. **Use EP** to pick one typical value from middle of valid partition

### Example: Grade Calculator

**Requirement**:

- 90-100: A
- 80-89: B
- 70-79: C
- 60-69: D
- 0-59: F

#### Step 1: Identify Partitions (EP)

- P1: 90-100 (A)
- P2: 80-89 (B)
- P3: 70-79 (C)
- P4: 60-69 (D)
- P5: 0-59 (F)
- P6: < 0 (Invalid)
- P7: > 100 (Invalid)

#### Step 2: Identify Boundaries (BVA)

Test **at and around** each partition boundary:

| Boundary Between | Test Values  | Expected Grades |
| ---------------- | ------------ | --------------- |
| Invalid / F      | -1, 0, 1     | Invalid, F, F   |
| F / D            | 59, 60, 61   | F, D, D         |
| D / C            | 69, 70, 71   | D, C, C         |
| C / B            | 79, 80, 81   | C, B, B         |
| B / A            | 89, 90, 91   | B, A, A         |
| A / Invalid      | 99, 100, 101 | A, A, Invalid   |

#### Step 3: Add Typical Values (EP)

- F: 30 (middle of 0-59)
- D: 65 (middle of 60-69)
- C: 75
- B: 85
- A: 95

### Complete Test Suite

```python
def calculate_grade(score):
    if score < 0 or score > 100:
        return None, "Invalid score"
    if score >= 90:
        return 'A', "Excellent"
    if score >= 80:
        return 'B', "Good"
    if score >= 70:
        return 'C', "Satisfactory"
    if score >= 60:
        return 'D', "Pass"
    return 'F', "Fail"

def test_grade_boundaries_and_typical():
    # Boundary: Invalid / F
    assert calculate_grade(-1)[0] == None  # Invalid
    assert calculate_grade(0)[0] == 'F'    # At boundary
    assert calculate_grade(1)[0] == 'F'    # Just above

    # Typical: F
    assert calculate_grade(30)[0] == 'F'

    # Boundary: F / D
    assert calculate_grade(59)[0] == 'F'   # Just before
    assert calculate_grade(60)[0] == 'D'   # At boundary
    assert calculate_grade(61)[0] == 'D'   # Just after

    # Typical: D
    assert calculate_grade(65)[0] == 'D'

    # Boundary: D / C
    assert calculate_grade(69)[0] == 'D'
    assert calculate_grade(70)[0] == 'C'
    assert calculate_grade(71)[0] == 'C'

    # Typical: C
    assert calculate_grade(75)[0] == 'C'

    # Boundary: C / B
    assert calculate_grade(79)[0] == 'C'
    assert calculate_grade(80)[0] == 'B'
    assert calculate_grade(81)[0] == 'B'

    # Typical: B
    assert calculate_grade(85)[0] == 'B'

    # Boundary: B / A
    assert calculate_grade(89)[0] == 'B'
    assert calculate_grade(90)[0] == 'A'
    assert calculate_grade(91)[0] == 'A'

    # Typical: A
    assert calculate_grade(95)[0] == 'A'

    # Boundary: A / Invalid
    assert calculate_grade(99)[0] == 'A'
    assert calculate_grade(100)[0] == 'A'  # At boundary
    assert calculate_grade(101)[0] == None # Invalid
```

---

## Non-Numeric Boundaries

BVA isn't just for numbers!

### 1. Date Boundaries

**Requirement**: Event date must be within next 30 days

```python
from datetime import datetime, timedelta

def test_date_boundaries():
    today = datetime.now()

    # Yesterday (invalid - past)
    yesterday = today - timedelta(days=1)
    assert validate_event_date(yesterday) == False

    # Today (boundary - valid)
    assert validate_event_date(today) == True

    # Tomorrow (just above minimum)
    tomorrow = today + timedelta(days=1)
    assert validate_event_date(tomorrow) == True

    # Day 29 (just below maximum)
    day_29 = today + timedelta(days=29)
    assert validate_event_date(day_29) == True

    # Day 30 (boundary - valid)
    day_30 = today + timedelta(days=30)
    assert validate_event_date(day_30) == True

    # Day 31 (invalid - too far)
    day_31 = today + timedelta(days=31)
    assert validate_event_date(day_31) == False
```

### 2. Array Length Boundaries

**Requirement**: Shopping cart must have 1-10 items

```javascript
describe("Cart Item Count Boundaries", () => {
  test("Empty cart (0 items) - should reject", () => {
    expect(validateCart([])).toBe(false);
  });

  test("1 item (minimum) - should accept", () => {
    expect(validateCart([item1])).toBe(true);
  });

  test("2 items (just above min) - should accept", () => {
    expect(validateCart([item1, item2])).toBe(true);
  });

  test("5 items (typical) - should accept", () => {
    expect(validateCart(Array(5).fill(item))).toBe(true);
  });

  test("9 items (just below max) - should accept", () => {
    expect(validateCart(Array(9).fill(item))).toBe(true);
  });

  test("10 items (maximum) - should accept", () => {
    expect(validateCart(Array(10).fill(item))).toBe(true);
  });

  test("11 items (over maximum) - should reject", () => {
    expect(validateCart(Array(11).fill(item))).toBe(false);
  });
});
```

### 3. File Size Boundaries

**Requirement**: Upload file size 1 MB - 50 MB

```python
def test_file_size_boundaries():
    MB = 1024 * 1024  # bytes in 1 MB

    # 0.9 MB (below minimum)
    assert validate_file_size(0.9 * MB) == False

    # 1 MB (minimum)
    assert validate_file_size(1 * MB) == True

    # 1.1 MB (just above minimum)
    assert validate_file_size(1.1 * MB) == True

    # 25 MB (typical)
    assert validate_file_size(25 * MB) == True

    # 49.9 MB (just below maximum)
    assert validate_file_size(49.9 * MB) == True

    # 50 MB (maximum)
    assert validate_file_size(50 * MB) == True

    # 50.1 MB (above maximum)
    assert validate_file_size(50.1 * MB) == False
```

---

## Two-Boundary vs Three-Boundary Values

### Two-Boundary Value Testing

Test **at** the boundaries only:

- Minimum value
- Maximum value

**Example**: Range 10-50

- Test: 10, 50

### Three-Boundary Value Testing (Most Common)

Test **at and around** boundaries:

- Just before minimum
- At minimum
- At maximum
- Just after maximum

**Example**: Range 10-50

- Test: 9, 10, 50, 51

### Five-Point Testing (Comprehensive)

Include typical middle value:

- Just before minimum
- At minimum
- Middle (typical)
- At maximum
- Just after maximum

**Example**: Range 10-50

- Test: 9, 10, 30, 50, 51

**Choose based on risk and time available.**

---

## Common BVA Mistakes

### 1. Missing "Just Before/After" Values

❌ **Wrong**: Only test 10 and 50 (the boundaries)  
✅ **Right**: Test 9, 10, 50, 51 (at and around boundaries)

### 2. Confusing Inclusive vs Exclusive

**Inclusive boundary** (10-50 inclusive):

- 10 is valid, 9 is invalid
- 50 is valid, 51 is invalid

**Exclusive boundary** (10 < x < 50):

- 10 is invalid, 11 is valid
- 50 is invalid, 49 is valid

### 3. Ignoring Invalid Boundaries

Always test **both sides** of a boundary (valid and invalid).

### 4. Not Combining with EP

BVA alone misses bugs in the middle of ranges.  
**Always use BVA + EP together.**

---

## BVA Checklist

Before finalizing boundary tests:

- [ ] Identified all minimum and maximum values
- [ ] Tested values just before minimum
- [ ] Tested values at minimum boundary
- [ ] Tested values just after minimum
- [ ] Tested typical value from middle (EP)
- [ ] Tested values just before maximum
- [ ] Tested values at maximum boundary
- [ ] Tested values just after maximum
- [ ] Documented whether boundaries are inclusive/exclusive
- [ ] Combined BVA with EP for complete coverage

---

## Summary

**Boundary Value Analysis** helps you:

1. **Find bugs where they hide** - at the edges
2. **Test critical values** systematically
3. **Catch off-by-one errors** before production

**Key Strategy**:

- Test **at** boundaries (min, max)
- Test **just before** boundaries (min-1, max+1)
- Test **just after** boundaries (min+1, max-1)
- Combine with **Equivalence Partitioning** for typical values

**Remember**: Most bugs occur at boundaries, not in the middle!

---

## Practice Exercises

Apply BVA to these scenarios:

1. **Temperature thermostat**: 60-80°F
2. **Product quantity**: 1-999 items
3. **Meeting duration**: 15-240 minutes
4. **Student enrollment**: 10-30 students per class

Document all boundary values and create test cases!

---

## Next Steps

- Read [04-decision-tables.md](./04-decision-tables.md) for complex business logic testing
- Practice with [Exercise 3: Boundary Value Analysis](../exercises/03-boundary-value-analysis.md)
- Combine EP + BVA in your test designs
