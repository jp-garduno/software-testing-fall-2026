# Exercise 2: Equivalence Partitioning

**Module**: 4 - Black Box Testing  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice applying equivalence partitioning to systematically reduce test cases.

By completing this exercise, you will:

- Identify valid and invalid equivalence classes
- Choose representative values from each partition
- Design test cases based on partitions
- Calculate partition coverage

---

## Instructions

For each scenario:

1. **Identify equivalence classes** (both valid and invalid)
2. **Document partitions** in a table
3. **Choose test values** (one per partition)
4. **Create test cases**
5. **Implement tests** in Python or JavaScript

---

## Scenario 1: Credit Card Validation

### Requirements

A credit card validator accepts card numbers with these rules:

- **Length**: 13-19 digits
- **Format**: Digits only (no spaces, dashes, letters)
- **Valid card types**:
  - Visa: Starts with 4
  - Mastercard: Starts with 51-55
  - Amex: Starts with 34 or 37

### Part A: Identify Partitions

Create a table like this:

| Partition ID | Description                                     | Type  | Example Values   |
| ------------ | ----------------------------------------------- | ----- | ---------------- |
| P1           | Valid Visa (starts with 4, 13-19 digits)        | Valid | 4532015112830366 |
| P2           | Valid Mastercard (starts with 51-55, 16 digits) | Valid | 5425233430109903 |
| ...          | ...                                             | ...   | ...              |

**Complete the table** with ALL partitions (valid and invalid):

- Valid Visa
- Valid Mastercard
- Valid Amex
- Too short (< 13 digits)
- Too long (> 19 digits)
- Invalid starting digits
- Contains non-numeric characters
- Empty string

### Part B: Create Test Cases

For each partition, write a test case:

```markdown
**Test Case ID**: TC_CC_001
**Partition**: P1 (Valid Visa)
**Input**: 4532015112830366
**Expected**: Valid - "Visa card accepted"
```

### Part C: Implementation

Implement in **Python**:

```python
def validate_credit_card(card_number):
    """
    Validates credit card number.
    Returns: (is_valid: bool, message: str, card_type: str)
    """
    # TODO: Implement validation logic
    pass

def test_valid_visa():
    """P1: Valid Visa card"""
    valid, msg, card_type = validate_credit_card("4532015112830366")
    assert valid == True
    assert card_type == "Visa"

def test_valid_mastercard():
    """P2: Valid Mastercard"""
    valid, msg, card_type = validate_credit_card("5425233430109903")
    assert valid == True
    assert card_type == "Mastercard"

def test_too_short():
    """P4: Too short"""
    valid, msg, card_type = validate_credit_card("123456789")
    assert valid == False
    assert "at least 13 digits" in msg.lower()

# TODO: Implement remaining test cases for all partitions
```

**OR** in **JavaScript**:

```javascript
function validateCreditCard(cardNumber) {
  /**
   * Validates credit card number.
   * Returns: { valid: boolean, message: string, cardType: string }
   */
  // TODO: Implement validation logic
}

describe("Credit Card Validation - Equivalence Partitioning", () => {
  test("P1: Valid Visa card", () => {
    const result = validateCreditCard("4532015112830366");
    expect(result.valid).toBe(true);
    expect(result.cardType).toBe("Visa");
  });

  test("P2: Valid Mastercard", () => {
    const result = validateCreditCard("5425233430109903");
    expect(result.valid).toBe(true);
    expect(result.cardType).toBe("Mastercard");
  });

  test("P4: Too short (< 13 digits)", () => {
    const result = validateCreditCard("123456789");
    expect(result.valid).toBe(false);
    expect(result.message.toLowerCase()).toContain("at least 13 digits");
  });

  // TODO: Implement remaining test cases
});
```

---

## Scenario 2: Date Validation Function

### Requirements

A date validation function accepts dates in MM/DD/YYYY format:

- **Month**: 01-12
- **Day**: 01-31 (varies by month)
- **Year**: 1900-2100
- **Format**: Must be MM/DD/YYYY with slashes

### Part A: Identify Partitions

Consider these dimensions:

**Month**:

- Valid: 01-12
- Invalid: < 01
- Invalid: > 12
- Invalid: Non-numeric

**Day**:

- Valid for 31-day months: 01-31
- Valid for 30-day months: 01-30
- Valid for February (non-leap): 01-28
- Valid for February (leap year): 01-29
- Invalid: < 01
- Invalid: > 31 (or month maximum)

**Year**:

- Valid: 1900-2100
- Invalid: < 1900
- Invalid: > 2100
- Invalid: Non-numeric

**Format**:

- Valid: MM/DD/YYYY
- Invalid: Wrong separator (-, .)
- Invalid: Missing separator
- Invalid: Wrong order (DD/MM/YYYY)

### Part B: Create Partition Table

| Partition | Description                        | Type  | Example    |
| --------- | ---------------------------------- | ----- | ---------- |
| P1        | Valid date - 31-day month          | Valid | 01/15/2025 |
| P2        | Valid date - 30-day month          | Valid | 04/20/2025 |
| P3        | Valid date - February non-leap     | Valid | 02/15/2025 |
| P4        | Valid date - February 29 leap year | Valid | 02/29/2024 |
| ...       | ...                                | ...   | ...        |

**Complete the table** with all partitions.

### Part C: Implementation

```python
def validate_date(date_string):
    """
    Validates date in MM/DD/YYYY format.
    Returns: (is_valid: bool, message: str)
    """
    # TODO: Implement
    pass

def test_valid_31_day_month():
    """P1: Valid date in 31-day month"""
    valid, msg = validate_date("01/15/2025")
    assert valid == True

def test_valid_30_day_month():
    """P2: Valid date in 30-day month"""
    valid, msg = validate_date("04/20/2025")
    assert valid == True

def test_february_leap_year():
    """P4: February 29 in leap year"""
    valid, msg = validate_date("02/29/2024")
    assert valid == True

def test_february_non_leap():
    """Invalid: February 29 in non-leap year"""
    valid, msg = validate_date("02/29/2025")
    assert valid == False

def test_invalid_month():
    """Invalid: Month > 12"""
    valid, msg = validate_date("13/15/2025")
    assert valid == False

# TODO: Complete all test cases
```

---

## Scenario 3: Flight Booking Eligibility

### Requirements

Flight booking system checks passenger eligibility:

- **Age**: 0-11 (Child), 12-17 (Teen), 18-64 (Adult), 65+ (Senior)
- **Ticket Class**: Economy, Business, First
- **Baggage**: 0-2 checked bags
- **Frequent Flyer Status**: None, Silver, Gold, Platinum

**Rules**:

- Children < 2 years: Must have adult, free ticket
- Children 2-11: Discounted ticket (50% off)
- Teens 12-17: Full price unless accompanied by adult (10% discount)
- Seniors 65+: 15% discount
- First class: 2 free checked bags
- Business class: 1 free checked bag
- Economy: $30 per bag
- Gold/Platinum: +1 free bag

### Part A: Identify Partitions

For **each input**, identify partitions:

**Age**:
| Partition | Range | Type | Example |
|-----------|-------|------|---------|
| P1 | 0-1 (Infant) | Valid | 1 |
| P2 | 2-11 (Child) | Valid | 8 |
| P3 | 12-17 (Teen) | Valid | 15 |
| ... | ... | ... | ... |

**Ticket Class**:
| Partition | Value | Type |
|-----------|-------|------|
| P_TC1 | Economy | Valid |
| ... | ... | ... |

**Complete for all inputs.**

### Part B: Design Test Cases

Create test cases covering all partitions:

```javascript
describe("Flight Booking Eligibility", () => {
  test("Infant (age 1) with adult - should be free", () => {
    const result = calculatePrice({
      age: 1,
      ticketClass: "Economy",
      withAdult: true,
      bags: 0,
    });
    expect(result.price).toBe(0);
    expect(result.requiresAdult).toBe(true);
  });

  test("Child (age 8) - 50% discount", () => {
    const result = calculatePrice({
      age: 8,
      ticketClass: "Economy",
      basePrice: 200,
    });
    expect(result.price).toBe(100);
  });

  test("Teen (age 15) with adult - 10% discount", () => {
    const result = calculatePrice({
      age: 15,
      ticketClass: "Economy",
      withAdult: true,
      basePrice: 200,
    });
    expect(result.price).toBe(180);
  });

  // TODO: Complete all age categories
});
```

---

## Scenario 4: URL Validator

### Requirements

URL validator checks:

- **Protocol**: http:// or https:// (required)
- **Domain**: Valid domain name (letters, numbers, hyphens, dots)
- **TLD**: 2-6 characters (.com, .org, .io, .museum)
- **Path**: Optional, starts with /
- **Query params**: Optional, starts with ?
- **Fragment**: Optional, starts with #

**Valid examples**:

- https://example.com
- http://sub.example.co.uk/path?query=1#section
- https://my-site.io

**Invalid examples**:

- example.com (no protocol)
- ftp://example.com (wrong protocol)
- https://example (no TLD)
- https://example..com (double dot)

### Your Task

1. **Identify all partitions** for each component
2. **Create partition table**
3. **Write test cases** (minimum 15 test cases)
4. **Implement validator and tests** in Python OR JavaScript

---

## Scenario 5: Password Strength Checker

### Requirements

Password strength checker evaluates passwords:

**Weak**:

- < 8 characters, OR
- Only lowercase letters, OR
- Only numbers

**Medium**:

- 8-12 characters, AND
- Mix of letters and numbers, OR
- 12+ characters with only letters

**Strong**:

- 12+ characters, AND
- Uppercase + lowercase + digits, AND
- At least one special character (@#$%^&\*)

### Your Task

1. **Identify partitions** for each strength level
2. **Create test cases** for each partition
3. **Implement checker** and tests

```python
def check_password_strength(password):
    """
    Returns: 'weak', 'medium', or 'strong'
    """
    # TODO: Implement
    pass

def test_weak_too_short():
    """Weak: < 8 characters"""
    assert check_password_strength("Pass1") == "weak"

def test_weak_only_lowercase():
    """Weak: Only lowercase letters"""
    assert check_password_strength("password") == "weak"

def test_medium_letters_and_numbers():
    """Medium: 8-12 chars, letters + numbers"""
    assert check_password_strength("password123") == "medium"

def test_strong_all_requirements():
    """Strong: 12+ chars, mixed case, digit, special"""
    assert check_password_strength("SecurePass123!") == "strong"

# TODO: Complete all partitions
```

---

## Deliverables

Submit a document or repository containing:

1. **Partition Tables** for all 5 scenarios
2. **Test Case Documentation** with:
   - Test case ID
   - Partition reference
   - Input values
   - Expected results
3. **Implementation** (Python or JavaScript):
   - Validation/checker functions
   - Test cases using pytest or Jest
   - All tests passing
4. **Coverage Report**:
   - Total partitions identified
   - Total partitions tested
   - Coverage percentage

---

## Evaluation Criteria

| Criteria                     | Points | Description                                 |
| ---------------------------- | ------ | ------------------------------------------- |
| **Partition Identification** | 25     | All valid and invalid partitions identified |
| **Test Case Design**         | 25     | Representative values chosen correctly      |
| **Implementation**           | 30     | Code works correctly for all partitions     |
| **Coverage**                 | 10     | High partition coverage (>90%)              |
| **Documentation**            | 10     | Clear partition tables and test cases       |

**Total**: 100 points

---

## Tips

1. **Start with requirements**: Read carefully to identify all conditions
2. **List all inputs**: Each input may have multiple partitions
3. **Both valid and invalid**: Don't forget invalid partitions
4. **One value per partition**: No need to test multiple values from same partition
5. **Edge cases vs EP**: EP focuses on typical values, not boundaries

---

## Common Mistakes

❌ Testing multiple values from same partition  
✅ One representative value per partition

❌ Overlapping partitions (e.g., 0-10 and 10-20)  
✅ Clear boundaries (0-10 and 11-20)

❌ Only testing valid partitions  
✅ Test both valid AND invalid partitions

❌ Missing edge cases  
✅ Combine EP with BVA (next exercise) for complete coverage

---

## Bonus Challenge

Combine **Equivalence Partitioning** with **Boundary Value Analysis**:

For **Scenario 2 (Date Validation)**, identify:

1. Equivalence classes
2. Boundary values for each partition
3. Test both partition representatives AND boundary values

Example:

- **Partition**: Valid month (01-12)
  - **Representative**: 06 (middle)
  - **Boundaries**: 01 (min), 12 (max)
- **Partition**: Invalid month (< 01)
  - **Representative**: -5
  - **Boundary**: 00 (just below valid)

---

## Next Steps

After completing this exercise:

1. Review [Theory: Equivalence Partitioning](../theory/02-equivalence-partitioning.md)
2. Move to [Exercise 3: Boundary Value Analysis](./03-boundary-value-analysis.md)
3. Compare your partitions with classmates
4. Practice combining EP with BVA for comprehensive coverage

---

**Remember: Equivalence Partitioning helps you test smarter, not harder!** 🎯
