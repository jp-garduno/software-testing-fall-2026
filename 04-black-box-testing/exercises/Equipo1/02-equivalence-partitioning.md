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

| Partition ID | Description                                                    | Type    | Example Values         |
| ------------ | -------------------------------------------------------------- | ------- | ---------------------- |
| P1           | Valid Visa: starts with 4 and contains 13-19 digits            | Valid   | `4532015112830366`     |
| P2           | Valid Mastercard: starts with 51-55 and contains 13-19 digits | Valid   | `5425233430109903`     |
| P3           | Valid Amex: starts with 34 or 37 and contains 13-19 digits    | Valid   | `378282246310005`      |
| P4           | Too short: fewer than 13 digits                                | Invalid | `412345678901`         |
| P5           | Too long: more than 19 digits                                  | Invalid | `41234567890123456789` |
| P6           | Invalid starting digits, with 13-19 numeric digits             | Invalid | `6123456789012345`     |
| P7           | Contains non-numeric characters                                 | Invalid | `4A3215112830366`      |
| P8           | Empty string                                                    | Invalid | `""`                   |

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

#### TC_CC_001: Valid Visa

**Test Case ID**: TC_CC_001
**Partition**: P1 (Valid Visa)
**Input**: 4532015112830366
**Expected**: Valid - "Visa card accepted"

#### TC_CC_002: Valid Mastercard

**Test Case ID**: TC_CC_002
**Partition**: P2 (Valid Mastercard)
**Input**: 5425233430109903
**Expected**: Valid - "Mastercard card accepted"

#### TC_CC_003: Valid Amex

**Test Case ID**: TC_CC_003
**Partition**: P3 (Valid Amex)
**Input**: 378282246310005
**Expected**: Valid - "Amex card accepted"

#### TC_CC_004: Too short

**Test Case ID**: TC_CC_004
**Partition**: P4 (Too short: fewer than 13 digits)
**Input**: 412345678901
**Expected**: Invalid - "Card number must contain at least 13 digits"

#### TC_CC_005: Too long

**Test Case ID**: TC_CC_005
**Partition**: P5 (Too long: more than 19 digits)
**Input**: 41234567890123456789
**Expected**: Invalid - "Card number must contain at most 19 digits"

#### TC_CC_006: Invalid starting digits

**Test Case ID**: TC_CC_006
**Partition**: P6 (Invalid starting digits)
**Input**: 6123456789012345
**Expected**: Invalid - "Unsupported card type"

#### TC_CC_007: Non-numeric characters

**Test Case ID**: TC_CC_007
**Partition**: P7 (Contains non-numeric characters)
**Input**: 4A3215112830366
**Expected**: Invalid - "Card number must contain digits only"

#### TC_CC_008: Empty string

**Test Case ID**: TC_CC_008
**Partition**: P8 (Empty string)
**Input**: ""
**Expected**: Invalid - "Card number cannot be empty"

### Part C: Implementation

Implement in **Python**:

```python
def validate_credit_card(card_number):
    """
    Validates credit card number.
    Returns: (is_valid: bool, message: str, card_type: str)
    """
    if card_number == "":
        return False, "Card number cannot be empty", ""

    if not card_number.isdigit():
        return False, "Card number must contain digits only", ""

    if len(card_number) < 13:
        return False, "Card number must contain at least 13 digits", ""

    if len(card_number) > 19:
        return False, "Card number must contain at most 19 digits", ""

    if card_number.startswith("4"):
        return True, "Visa card accepted", "Visa"

    if card_number[:2] in {str(number) for number in range(51, 56)}:
        return True, "Mastercard card accepted", "Mastercard"

    if card_number[:2] in {"34", "37"}:
        return True, "Amex card accepted", "Amex"

    return False, "Unsupported card type", ""

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
    valid, msg, card_type = validate_credit_card("412345678901")
    assert valid is False
    assert "at least 13 digits" in msg.lower()

def test_valid_amex():
    """P3: Valid Amex card"""
    valid, msg, card_type = validate_credit_card("378282246310005")
    assert valid is True
    assert card_type == "Amex"

def test_too_long():
    """P5: Too long"""
    valid, msg, card_type = validate_credit_card("41234567890123456789")
    assert valid is False
    assert "at most 19 digits" in msg.lower()

def test_invalid_starting_digits():
    """P6: Invalid starting digits"""
    valid, msg, card_type = validate_credit_card("6123456789012345")
    assert valid is False
    assert "unsupported card type" in msg.lower()

def test_non_numeric_characters():
    """P7: Contains non-numeric characters"""
    valid, msg, card_type = validate_credit_card("4A3215112830366")
    assert valid is False
    assert "digits only" in msg.lower()

def test_empty_string():
    """P8: Empty string"""
    valid, msg, card_type = validate_credit_card("")
    assert valid is False
    assert "cannot be empty" in msg.lower()
```
