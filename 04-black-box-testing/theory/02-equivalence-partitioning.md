# Equivalence Partitioning

**Module**: 4 - Black Box Testing  
**Topic**: Systematic Test Case Reduction  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand the concept of equivalence classes
- Identify valid and invalid partitions
- Reduce test cases systematically
- Apply equivalence partitioning to real-world scenarios
- Calculate partition coverage

---

## What is Equivalence Partitioning?

**Equivalence Partitioning (EP)** is a black-box testing technique that divides input data into logical groups (partitions) where all values in a partition are expected to be treated the same by the system.

### The Core Idea

If one value in a partition works correctly, all values in that partition should work correctly.

**Instead of testing**:

- Age: 1, 2, 3, ..., 100 (100 test cases)

**Test**:

- Age: One value from each partition (3-5 test cases)

---

## Why Use Equivalence Partitioning?

### Problem: Too Many Possible Inputs

Example: Password length validation (6-20 characters)

**Without EP**: Test all lengths 1, 2, 3, ..., 100 = 100 test cases  
**With EP**: Test 3 partitions = 3 test cases

### Benefits

1. **Reduces test cases** without losing coverage
2. **Systematic approach** to test design
3. **Finds bugs efficiently** by testing representative values
4. **Easy to document** and explain
5. **Works with any input type** (numbers, strings, dates, etc.)

---

## Types of Partitions

### 1. Valid Equivalence Classes

Partitions with **valid** inputs that the system should accept.

**Example**: Age for adult content (must be 18+)

- **Valid**: 18-120 (any age from 18 to 120)

### 2. Invalid Equivalence Classes

Partitions with **invalid** inputs that the system should reject.

**Example**: Age for adult content

- **Invalid**: < 18 (any age below 18)
- **Invalid**: > 120 (unrealistic ages)
- **Invalid**: Non-numeric (letters, symbols)
- **Invalid**: Empty (no input)

---

## How to Identify Equivalence Classes

### Step 1: Analyze Requirements

Read specifications carefully to identify:

- Input ranges
- Valid values
- Invalid values
- Special conditions

### Step 2: Identify Partitions

For each input, determine:

1. **Valid partitions**: Acceptable values
2. **Invalid partitions**: Unacceptable values

### Step 3: Choose Test Values

Select **one representative value** from each partition.

---

## Example 1: Simple Numeric Range

**Requirement**: Discount code accepts values between 10 and 50 (inclusive)

### Partitions

| Partition ID | Description          | Type    | Example Values   |
| ------------ | -------------------- | ------- | ---------------- |
| P1           | Below minimum (< 10) | Invalid | -5, 0, 5, 9      |
| P2           | Valid range (10-50)  | Valid   | 10, 25, 50       |
| P3           | Above maximum (> 50) | Invalid | 51, 75, 100, 999 |

### Test Cases

| Test Case | Partition | Input Value | Expected Result                    |
| --------- | --------- | ----------- | ---------------------------------- |
| TC1       | P1        | 5           | Error: "Value must be at least 10" |
| TC2       | P2        | 30          | Success: Discount applied          |
| TC3       | P3        | 60          | Error: "Value cannot exceed 50"    |

**3 test cases** instead of testing all values from -1000 to 1000!

---

## Example 2: String Validation

**Requirement**: Username must be 5-15 characters, letters and numbers only

### Partitions

| Partition | Description           | Type    | Test Value              |
| --------- | --------------------- | ------- | ----------------------- |
| P1        | Too short (< 5 chars) | Invalid | "abc", "jo"             |
| P2        | Valid length (5-15)   | Valid   | "john5", "user123"      |
| P3        | Too long (> 15 chars) | Invalid | "verylongusername123"   |
| P4        | Invalid characters    | Invalid | "user@123", "user name" |
| P5        | Empty string          | Invalid | ""                      |

### Test Cases

```python
import pytest

def validate_username(username):
    if len(username) < 5:
        return False, "Username must be at least 5 characters"
    if len(username) > 15:
        return False, "Username cannot exceed 15 characters"
    if not username.isalnum():
        return False, "Username must contain only letters and numbers"
    return True, "Valid username"

# Test cases based on equivalence partitions
def test_username_too_short():
    """P1: Too short"""
    valid, message = validate_username("abc")
    assert not valid
    assert "at least 5 characters" in message

def test_username_valid():
    """P2: Valid length and format"""
    valid, message = validate_username("john123")
    assert valid
    assert message == "Valid username"

def test_username_too_long():
    """P3: Too long"""
    valid, message = validate_username("verylongusername123")
    assert not valid
    assert "cannot exceed 15" in message

def test_username_invalid_chars():
    """P4: Invalid characters"""
    valid, message = validate_username("user@name")
    assert not valid
    assert "only letters and numbers" in message

def test_username_empty():
    """P5: Empty string"""
    valid, message = validate_username("")
    assert not valid
```

---

## Example 3: Multiple Input Fields

**Requirement**: Flight booking requires:

- Number of passengers: 1-9
- Ticket class: Economy, Business, First
- Age category: Child (0-11), Teen (12-17), Adult (18+)

### Partitions for Each Input

**Passengers**:

| Partition | Range       | Type    | Test Value |
| --------- | ----------- | ------- | ---------- |
| P1        | < 1         | Invalid | 0, -1      |
| P2        | 1-9 (valid) | Valid   | 1, 5, 9    |
| P3        | > 9         | Invalid | 10, 20     |

**Ticket Class**:

| Partition | Value    | Type    |
| --------- | -------- | ------- |
| P4        | Economy  | Valid   |
| P5        | Business | Valid   |
| P6        | First    | Valid   |
| P7        | Other    | Invalid |

**Age Category**:

| Partition | Range        | Type    | Test Value |
| --------- | ------------ | ------- | ---------- |
| P8        | < 0          | Invalid | -1         |
| P9        | 0-11 (Child) | Valid   | 5          |
| P10       | 12-17 (Teen) | Valid   | 15         |
| P11       | 18+ (Adult)  | Valid   | 25         |

### Combined Test Cases

You need to test **at least one value from each partition** for thorough coverage:

```python
def test_flight_booking_valid():
    """Valid booking with typical values"""
    result = book_flight(passengers=2, ticket_class="Economy", age=25)
    assert result.success == True

def test_flight_booking_invalid_passengers():
    """Invalid: 0 passengers"""
    result = book_flight(passengers=0, ticket_class="Economy", age=25)
    assert result.success == False
    assert "at least 1 passenger" in result.error

def test_flight_booking_child():
    """Valid: Child passenger"""
    result = book_flight(passengers=1, ticket_class="Economy", age=8)
    assert result.success == True
    assert result.discount_applied == "Child discount"
```

---

## Choosing Test Values

### Best Practices

1. **Pick typical values** from valid partitions
2. **Pick boundary-adjacent values** from invalid partitions
3. **One value per partition** is usually sufficient
4. **Document why you chose each value**

### Example: Age 18-65

**Good Test Values**:

- Valid: 30 (mid-range)
- Invalid (below): 17 (just below minimum)
- Invalid (above): 66 (just above maximum)

**Poor Test Values**:

- Valid: 18 (boundary, not typical - use BVA for this)
- Invalid (below): -100 (too extreme)

---

## Advanced: Partitioning Complex Rules

### Rule-Based Partitions

**Requirement**: Password must contain:

- At least 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (@#$%^&\*)

### Partitions

| Partition | Description            | Type    | Example       |
| --------- | ---------------------- | ------- | ------------- |
| P1        | Meets all requirements | Valid   | "Pass123@"    |
| P2        | Too short              | Invalid | "Pa1@"        |
| P3        | No uppercase           | Invalid | "pass123@"    |
| P4        | No lowercase           | Invalid | "PASS123@"    |
| P5        | No digit               | Invalid | "Password@"   |
| P6        | No special char        | Invalid | "Password123" |
| P7        | Empty                  | Invalid | ""            |

```javascript
// JavaScript/Jest example
describe("Password Validation", () => {
  test("P1: Valid password with all requirements", () => {
    expect(validatePassword("Pass123@")).toBe(true);
  });

  test("P2: Invalid - too short", () => {
    expect(validatePassword("Pa1@")).toBe(false);
  });

  test("P3: Invalid - no uppercase", () => {
    expect(validatePassword("pass123@")).toBe(false);
  });

  test("P4: Invalid - no lowercase", () => {
    expect(validatePassword("PASS123@")).toBe(false);
  });

  test("P5: Invalid - no digit", () => {
    expect(validatePassword("Password@")).toBe(false);
  });

  test("P6: Invalid - no special character", () => {
    expect(validatePassword("Password123")).toBe(false);
  });

  test("P7: Invalid - empty string", () => {
    expect(validatePassword("")).toBe(false);
  });
});
```

---

## Calculating Coverage

### Partition Coverage Formula

```
Partition Coverage = (Tested Partitions / Total Partitions) × 100%
```

**Example**:

- Total partitions: 7 (P1-P7)
- Tested partitions: 7
- Coverage: 100%

**Incomplete Example**:

- Total partitions: 7
- Tested partitions: 3 (only tested P1, P2, P3)
- Coverage: 43%

### Aim for 100% Partition Coverage

Test **at least one value** from **every partition** (valid and invalid).

---

## Equivalence Partitioning with Multiple Conditions

### Scenario: Loan Eligibility

**Requirements**:

- Age: 21-65
- Credit score: 600-850
- Income: >= $30,000
- Approved if ALL conditions met

### Partitions

**Age**:

- Invalid: < 21
- Valid: 21-65
- Invalid: > 65

**Credit Score**:

- Invalid: < 600
- Valid: 600-850
- Invalid: > 850

**Income**:

- Invalid: < $30,000
- Valid: >= $30,000

### Test Cases (Sample)

| TC  | Age | Credit | Income  | Expected        |
| --- | --- | ------ | ------- | --------------- |
| 1   | 30  | 700    | $50,000 | Approved        |
| 2   | 18  | 700    | $50,000 | Denied (age)    |
| 3   | 30  | 550    | $50,000 | Denied (credit) |
| 4   | 30  | 700    | $20,000 | Denied (income) |

---

## Common Mistakes

### 1. Testing Too Many Values from Same Partition

❌ **Wrong**: Test ages 25, 30, 35, 40, 45 (all from same valid partition)  
✅ **Right**: Test one value from valid partition (e.g., 30)

### 2. Ignoring Invalid Partitions

❌ **Wrong**: Only test valid inputs  
✅ **Right**: Test both valid AND invalid partitions

### 3. Overlapping Partitions

❌ **Wrong**:

- P1: 0-10
- P2: 10-20 (overlaps at 10)

✅ **Right**:

- P1: 0-9
- P2: 10-20

### 4. Missing Edge Cases

EP focuses on typical values, not boundaries.  
**Combine with Boundary Value Analysis** (next topic) for complete coverage.

---

## Equivalence Partitioning Checklist

Before finalizing your partitions:

- [ ] All valid inputs covered by at least one partition
- [ ] All invalid inputs covered by at least one partition
- [ ] No overlapping partitions
- [ ] Each partition is clearly defined
- [ ] At least one test case per partition
- [ ] Test values are representative of each partition
- [ ] Invalid partitions include all error conditions

---

## Real-World Example: Credit Card Validation

**Requirement**: Validate credit card number

- Length: 13-19 digits
- Must pass Luhn algorithm
- Must start with valid IIN (Issuer Identification Number)

### Partitions

| Partition | Description                     | Type    | Example              |
| --------- | ------------------------------- | ------- | -------------------- |
| P1        | Valid Visa (starts with 4)      | Valid   | 4532015112830366     |
| P2        | Valid Mastercard (starts 51-55) | Valid   | 5425233430109903     |
| P3        | Valid Amex (starts 34/37)       | Valid   | 371449635398431      |
| P4        | Too short (< 13 digits)         | Invalid | 123456789            |
| P5        | Too long (> 19 digits)          | Invalid | 12345678901234567890 |
| P6        | Fails Luhn check                | Invalid | 4532015112830367     |
| P7        | Invalid IIN                     | Invalid | 9999999999999999     |
| P8        | Non-numeric                     | Invalid | "abcd-1234-5678"     |

```python
def test_credit_card_validation():
    # P1: Valid Visa
    assert validate_card("4532015112830366") == True

    # P2: Valid Mastercard
    assert validate_card("5425233430109903") == True

    # P3: Valid Amex
    assert validate_card("371449635398431") == True

    # P4: Too short
    assert validate_card("123456789") == False

    # P5: Too long
    assert validate_card("12345678901234567890") == False

    # P6: Fails Luhn check
    assert validate_card("4532015112830367") == False

    # P7: Invalid IIN
    assert validate_card("9999999999999999") == False

    # P8: Non-numeric
    assert validate_card("abcd-1234-5678") == False
```

---

## Summary

**Equivalence Partitioning** helps you:

1. **Reduce test cases** by grouping similar inputs
2. **Increase efficiency** without losing coverage
3. **Find bugs systematically** by testing representative values

**Key Steps**:

1. Identify input conditions
2. Divide into valid and invalid partitions
3. Choose one representative value per partition
4. Create test cases for all partitions

**Remember**: EP focuses on **typical values**. Combine with **Boundary Value Analysis** for edge cases!

---

## Practice Exercises

Apply equivalence partitioning to these scenarios:

1. **Email validation**: username@domain.extension
2. **Shipping calculator**: Weight (1-50 kg), Destination (Domestic/International)
3. **Grade calculator**: Score (0-100) → Grade (A, B, C, D, F)
4. **Hotel booking**: Check-in date, Check-out date, Number of guests (1-4)

Document your partitions and test cases!

---

## Next Steps

- Read [03-boundary-value-analysis.md](./03-boundary-value-analysis.md) to learn about testing edge cases
- Practice with [Exercise 2: Equivalence Partitioning](../exercises/02-equivalence-partitioning.md)
- Combine EP with BVA for comprehensive test coverage
