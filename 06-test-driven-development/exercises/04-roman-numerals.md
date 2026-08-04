# Exercise 4: Roman Numerals Kata

**Module**: 6 - Test Driven Development  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice TDD with algorithmic thinking and bidirectional conversion.

By completing this exercise, you will:

- Handle pattern-based algorithms with TDD
- Implement bidirectional conversions (to/from)
- Discover algorithms through testing
- Practice transformation priority premise
- Build comprehensive test suites

---

## Problem Description

Convert integers to Roman numerals and vice versa.

Roman numerals use seven symbols:

| Symbol | Value |
| ------ | ----- |
| I      | 1     |
| V      | 5     |
| X      | 10    |
| L      | 50    |
| C      | 100   |
| D      | 500   |
| M      | 1000  |

### Conversion Rules

1. **Additive**: Symbols are added from left to right

   - `VI` = 5 + 1 = 6
   - `XX` = 10 + 10 = 20
   - `MDCLXVI` = 1000 + 500 + 100 + 50 + 10 + 5 + 1 = 1666

2. **Subtractive**: Smaller value before larger means subtraction

   - `IV` = 5 - 1 = 4
   - `IX` = 10 - 1 = 9
   - `XL` = 50 - 10 = 40
   - `XC` = 100 - 10 = 90
   - `CD` = 500 - 100 = 400
   - `CM` = 1000 - 100 = 900

3. **Subtractive Pairs** (only these are valid):
   - I can precede V or X
   - X can precede L or C
   - C can precede D or M

### Examples

```
1 → "I"
4 → "IV"
5 → "V"
9 → "IX"
27 → "XXVII"
48 → "XLVIII"
59 → "LIX"
93 → "XCIII"
141 → "CXLI"
163 → "CLXIII"
402 → "CDII"
575 → "DLXXV"
1994 → "MCMXCIV"
3999 → "MMMCMXCIX"
```

### Constraints

- Valid input range: 1-3999
- Roman numerals don't represent zero or negative numbers
- No more than 3 consecutive identical symbols (except M)

---

## Why Roman Numerals?

This kata is excellent for TDD because:

- **Pattern discovery**: Algorithm emerges from tests
- **Bidirectional**: Two functions, similar patterns
- **Edge cases**: Subtractive notation is tricky
- **No obvious solution**: Tests guide you to the answer
- **Refactoring opportunities**: Multiple ways to implement

---

## Part 1: Integer to Roman

### Step-by-Step TDD Guide

#### Step 1: Convert 1

**Test First**:

```python
def test_converts_1_to_I():
    assert to_roman(1) == "I"
```

```javascript
test("converts 1 to I", () => {
  expect(toRoman(1)).toBe("I");
});
```

**Simplest Implementation**:

```python
def to_roman(num):
    return "I"
```

```javascript
function toRoman(num) {
  return "I";
}
```

---

#### Step 2: Convert 2 and 3

**Test First**:

```python
def test_converts_2_to_II():
    assert to_roman(2) == "II"

def test_converts_3_to_III():
    assert to_roman(3) == "III"
```

**Implementation**:

```python
def to_roman(num):
    return "I" * num
```

```javascript
function toRoman(num) {
  return "I".repeat(num);
}
```

---

#### Step 3: Convert 5

**Test First**:

```python
def test_converts_5_to_V():
    assert to_roman(5) == "V"
```

**Implementation**:

```python
def to_roman(num):
    if num >= 5:
        return "V" + "I" * (num - 5)
    return "I" * num
```

```javascript
function toRoman(num) {
  if (num >= 5) {
    return "V" + "I".repeat(num - 5);
  }
  return "I".repeat(num);
}
```

---

#### Step 4: Convert 4 (Subtractive!)

**Test First**:

```python
def test_converts_4_to_IV():
    assert to_roman(4) == "IV"
```

**Implementation**:

```python
def to_roman(num):
    if num >= 5:
        return "V" + "I" * (num - 5)
    if num == 4:
        return "IV"
    return "I" * num
```

---

#### Step 5: Convert 10

**Test First**:

```python
def test_converts_10_to_X():
    assert to_roman(10) == "X"
```

**Implementation** (Pattern emerging):

```python
def to_roman(num):
    result = ""

    if num >= 10:
        result += "X"
        num -= 10

    if num >= 5:
        result += "V"
        num -= 5

    if num == 4:
        result += "IV"
        num -= 4

    if num >= 1:
        result += "I" * num

    return result
```

---

#### Step 6: Refactor with Lookup Table

**Better approach** (after more tests):

```python
def to_roman(num):
    """Convert integer to Roman numeral."""
    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]

    result = ""

    for value, numeral in values:
        count = num // value
        if count:
            result += numeral * count
            num -= value * count

    return result
```

```javascript
function toRoman(num) {
  const values = [
    [1000, "M"],
    [900, "CM"],
    [500, "D"],
    [400, "CD"],
    [100, "C"],
    [90, "XC"],
    [50, "L"],
    [40, "XL"],
    [10, "X"],
    [9, "IX"],
    [5, "V"],
    [4, "IV"],
    [1, "I"],
  ];

  let result = "";

  for (const [value, numeral] of values) {
    const count = Math.floor(num / value);
    if (count) {
      result += numeral.repeat(count);
      num -= value * count;
    }
  }

  return result;
}
```

---

### Test Progression for to_roman()

Add these tests one at a time:

```python
def test_converts_1_to_I():
    assert to_roman(1) == "I"

def test_converts_2_to_II():
    assert to_roman(2) == "II"

def test_converts_3_to_III():
    assert to_roman(3) == "III"

def test_converts_4_to_IV():
    assert to_roman(4) == "IV"

def test_converts_5_to_V():
    assert to_roman(5) == "V"

def test_converts_6_to_VI():
    assert to_roman(6) == "VI"

def test_converts_9_to_IX():
    assert to_roman(9) == "IX"

def test_converts_10_to_X():
    assert to_roman(10) == "X"

def test_converts_27_to_XXVII():
    assert to_roman(27) == "XXVII"

def test_converts_40_to_XL():
    assert to_roman(40) == "XL"

def test_converts_48_to_XLVIII():
    assert to_roman(48) == "XLVIII"

def test_converts_50_to_L():
    assert to_roman(50) == "L"

def test_converts_90_to_XC():
    assert to_roman(90) == "XC"

def test_converts_100_to_C():
    assert to_roman(100) == "C"

def test_converts_400_to_CD():
    assert to_roman(400) == "CD"

def test_converts_500_to_D():
    assert to_roman(500) == "D"

def test_converts_900_to_CM():
    assert to_roman(900) == "CM"

def test_converts_1000_to_M():
    assert to_roman(1000) == "M"

def test_converts_1994_to_MCMXCIV():
    assert to_roman(1994) == "MCMXCIV"

def test_converts_3999_to_MMMCMXCIX():
    assert to_roman(3999) == "MMMCMXCIX"
```

---

## Part 2: Roman to Integer

Now implement the reverse: `from_roman()`

### Step-by-Step TDD Guide

#### Step 1: Convert "I"

**Test First**:

```python
def test_converts_I_to_1():
    assert from_roman("I") == 1
```

**Implementation**:

```python
def from_roman(roman):
    return 1
```

---

#### Step 2: Convert "II" and "III"

**Test First**:

```python
def test_converts_II_to_2():
    assert from_roman("II") == 2

def test_converts_III_to_3():
    assert from_roman("III") == 3
```

**Implementation**:

```python
def from_roman(roman):
    return len(roman)
```

---

#### Step 3: Convert "V"

**Test First**:

```python
def test_converts_V_to_5():
    assert from_roman("V") == 5
```

**Implementation**:

```python
def from_roman(roman):
    values = {"I": 1, "V": 5}

    total = 0
    for char in roman:
        total += values[char]

    return total
```

---

#### Step 4: Convert "IV" (Subtractive!)

**Test First**:

```python
def test_converts_IV_to_4():
    assert from_roman("IV") == 4
```

**Implementation** (Look-ahead logic):

```python
def from_roman(roman):
    values = {"I": 1, "V": 5, "X": 10, "L": 50,
              "C": 100, "D": 500, "M": 1000}

    total = 0
    i = 0

    while i < len(roman):
        if i + 1 < len(roman) and values[roman[i]] < values[roman[i + 1]]:
            # Subtractive case
            total += values[roman[i + 1]] - values[roman[i]]
            i += 2
        else:
            total += values[roman[i]]
            i += 1

    return total
```

```javascript
function fromRoman(roman) {
  const values = {
    I: 1,
    V: 5,
    X: 10,
    L: 50,
    C: 100,
    D: 500,
    M: 1000,
  };

  let total = 0;
  let i = 0;

  while (i < roman.length) {
    if (i + 1 < roman.length && values[roman[i]] < values[roman[i + 1]]) {
      // Subtractive case
      total += values[roman[i + 1]] - values[roman[i]];
      i += 2;
    } else {
      total += values[roman[i]];
      i += 1;
    }
  }

  return total;
}
```

---

### Test Progression for from_roman()

```python
def test_converts_I_to_1():
    assert from_roman("I") == 1

def test_converts_II_to_2():
    assert from_roman("II") == 2

def test_converts_III_to_3():
    assert from_roman("III") == 3

def test_converts_IV_to_4():
    assert from_roman("IV") == 4

def test_converts_V_to_5():
    assert from_roman("V") == 5

def test_converts_VI_to_6():
    assert from_roman("VI") == 6

def test_converts_IX_to_9():
    assert from_roman("IX") == 9

def test_converts_X_to_10():
    assert from_roman("X") == 10

def test_converts_XXVII_to_27():
    assert from_roman("XXVII") == 27

def test_converts_XLVIII_to_48():
    assert from_roman("XLVIII") == 48

def test_converts_XCIII_to_93():
    assert from_roman("XCIII") == 93

def test_converts_MCMXCIV_to_1994():
    assert from_roman("MCMXCIV") == 1994

def test_converts_MMMCMXCIX_to_3999():
    assert from_roman("MMMCMXCIX") == 3999
```

---

## Part 3: Bidirectional Testing

Test round-trip conversions:

```python
def test_round_trip_conversions():
    """Test that to_roman and from_roman are inverses"""
    test_values = [1, 4, 5, 9, 27, 48, 93, 141, 402, 575, 1994, 3999]

    for num in test_values:
        roman = to_roman(num)
        back_to_num = from_roman(roman)
        assert back_to_num == num, f"{num} → {roman} → {back_to_num}"

def test_all_numbers_1_to_3999():
    """Comprehensive round-trip test"""
    for num in range(1, 4000):
        roman = to_roman(num)
        back = from_roman(roman)
        assert back == num, f"Failed at {num}"
```

```javascript
test("round trip conversions", () => {
  const testValues = [1, 4, 5, 9, 27, 48, 93, 141, 402, 575, 1994, 3999];

  for (const num of testValues) {
    const roman = toRoman(num);
    const backToNum = fromRoman(roman);
    expect(backToNum).toBe(num);
  }
});

test("all numbers 1 to 3999", () => {
  for (let num = 1; num <= 3999; num++) {
    const roman = toRoman(num);
    const back = fromRoman(roman);
    expect(back).toBe(num);
  }
});
```

---

## Complete Solution

### Python (pytest)

```python
def to_roman(num: int) -> str:
    """
    Convert integer to Roman numeral.

    Args:
        num: Integer from 1 to 3999

    Returns:
        Roman numeral string

    Raises:
        ValueError: If num is out of range
    """
    if not 1 <= num <= 3999:
        raise ValueError("Number must be between 1 and 3999")

    values = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]

    result = ""

    for value, numeral in values:
        count = num // value
        if count:
            result += numeral * count
            num -= value * count

    return result


def from_roman(roman: str) -> int:
    """
    Convert Roman numeral to integer.

    Args:
        roman: Roman numeral string

    Returns:
        Integer value

    Raises:
        ValueError: If roman numeral is invalid
    """
    values = {
        "I": 1,
        "V": 5,
        "X": 10,
        "L": 50,
        "C": 100,
        "D": 500,
        "M": 1000
    }

    if not roman:
        raise ValueError("Roman numeral cannot be empty")

    # Validate characters
    for char in roman:
        if char not in values:
            raise ValueError(f"Invalid Roman numeral character: {char}")

    total = 0
    i = 0

    while i < len(roman):
        if i + 1 < len(roman) and values[roman[i]] < values[roman[i + 1]]:
            # Subtractive case
            total += values[roman[i + 1]] - values[roman[i]]
            i += 2
        else:
            total += values[roman[i]]
            i += 1

    return total


# Tests
import pytest

class TestRomanNumerals:
    # to_roman tests
    def test_to_roman_1_to_3(self):
        assert to_roman(1) == "I"
        assert to_roman(2) == "II"
        assert to_roman(3) == "III"

    def test_to_roman_subtractive_4(self):
        assert to_roman(4) == "IV"

    def test_to_roman_5_to_8(self):
        assert to_roman(5) == "V"
        assert to_roman(6) == "VI"
        assert to_roman(7) == "VII"
        assert to_roman(8) == "VIII"

    def test_to_roman_9(self):
        assert to_roman(9) == "IX"

    def test_to_roman_tens(self):
        assert to_roman(10) == "X"
        assert to_roman(20) == "XX"
        assert to_roman(30) == "XXX"
        assert to_roman(40) == "XL"
        assert to_roman(50) == "L"
        assert to_roman(90) == "XC"

    def test_to_roman_hundreds(self):
        assert to_roman(100) == "C"
        assert to_roman(400) == "CD"
        assert to_roman(500) == "D"
        assert to_roman(900) == "CM"

    def test_to_roman_thousands(self):
        assert to_roman(1000) == "M"
        assert to_roman(2000) == "MM"
        assert to_roman(3000) == "MMM"

    def test_to_roman_complex(self):
        assert to_roman(27) == "XXVII"
        assert to_roman(48) == "XLVIII"
        assert to_roman(93) == "XCIII"
        assert to_roman(141) == "CXLI"
        assert to_roman(163) == "CLXIII"
        assert to_roman(402) == "CDII"
        assert to_roman(575) == "DLXXV"
        assert to_roman(1994) == "MCMXCIV"
        assert to_roman(3999) == "MMMCMXCIX"

    def test_to_roman_invalid_range(self):
        with pytest.raises(ValueError):
            to_roman(0)
        with pytest.raises(ValueError):
            to_roman(4000)

    # from_roman tests
    def test_from_roman_basic(self):
        assert from_roman("I") == 1
        assert from_roman("II") == 2
        assert from_roman("III") == 3

    def test_from_roman_subtractive(self):
        assert from_roman("IV") == 4
        assert from_roman("IX") == 9
        assert from_roman("XL") == 40
        assert from_roman("XC") == 90
        assert from_roman("CD") == 400
        assert from_roman("CM") == 900

    def test_from_roman_complex(self):
        assert from_roman("XXVII") == 27
        assert from_roman("XLVIII") == 48
        assert from_roman("XCIII") == 93
        assert from_roman("MCMXCIV") == 1994
        assert from_roman("MMMCMXCIX") == 3999

    def test_from_roman_invalid(self):
        with pytest.raises(ValueError):
            from_roman("")
        with pytest.raises(ValueError):
            from_roman("ABC")

    # Round-trip tests
    def test_round_trip(self):
        test_values = [1, 4, 5, 9, 27, 48, 93, 141, 402, 575, 1994, 3999]
        for num in test_values:
            roman = to_roman(num)
            back = from_roman(roman)
            assert back == num

    def test_all_numbers(self):
        """Comprehensive test"""
        for num in range(1, 4000):
            roman = to_roman(num)
            back = from_roman(roman)
            assert back == num
```

---

## Evaluation Criteria

| Criteria         | Points | Description                               |
| ---------------- | ------ | ----------------------------------------- |
| **TDD Process**  | 20     | Tests written first, incremental progress |
| **to_roman()**   | 25     | Correct integer to Roman conversion       |
| **from_roman()** | 25     | Correct Roman to integer conversion       |
| **Edge Cases**   | 15     | Handles subtractive notation correctly    |
| **Code Quality** | 15     | Clean, readable, well-structured          |

**Total**: 100 points

---

## Common Mistakes

❌ **Hard-coding all values**  
✅ Use lookup table pattern

❌ **Forgetting subtractive cases**  
✅ Test 4, 9, 40, 90, 400, 900 explicitly

❌ **Wrong order in lookup table**  
✅ Order matters! Largest values first

❌ **Not testing round-trips**  
✅ Verify to/from are inverses

❌ **Poor validation**  
✅ Handle invalid input gracefully

---

## Tips for Success

1. **Start Simple**: Begin with 1, 2, 3
2. **Test Subtractives Early**: Don't avoid 4 and 9
3. **Lookup Table**: Discovered through refactoring
4. **Order Matters**: Process largest values first
5. **Round-trip Tests**: Powerful validation
6. **Bidirectional Thinking**: Both directions use similar logic
7. **Comprehensive Testing**: Test all subtractive pairs

---

## Bonus Challenges

### Challenge 1: Validation

Add strict validation:

```python
def is_valid_roman(roman: str) -> bool:
    """Check if Roman numeral is properly formed"""
    # No more than 3 consecutive I, X, C, M
    # Proper subtractive pairs only
    # No invalid combinations like "IC" or "XM"
    pass
```

### Challenge 2: Alternative Implementation

Try using recursion:

```python
def to_roman_recursive(num: int) -> str:
    """Recursive implementation"""
    if num == 0:
        return ""
    # Find largest value that fits
    # Return numeral + recursive call
    pass
```

### Challenge 3: Performance

Benchmark both implementations with all values 1-3999. Which is faster?

---

## Deliverables

1. **Both functions** (`to_roman` and `from_roman`) with all tests passing
2. **Comprehensive test suite** including round-trip tests
3. **Git history** showing TDD progression
4. **Performance comparison** (bonus)
5. **Reflection** (1 page) on algorithm discovery process

---

## Resources

- [Roman Numerals on Wikipedia](https://en.wikipedia.org/wiki/Roman_numerals)
- [TDD Transformation Priority Premise](https://blog.cleancoder.com/uncle-bob/2013/05/27/TheTransformationPriorityPremise.html) - Uncle Bob
- [Roman Numerals Kata](http://codingdojo.org/kata/RomanNumerals/)

---

## Next Steps

1. Complete [Exercise 5: Bank Account Kata](./05-bank-account.md)
2. Review [Theory: Test Data Strategies](../theory/05-test-data.md)
3. Try implementing with different algorithms
4. Explore the Transformation Priority Premise

---

**Roman Numerals shows how TDD helps discover elegant algorithms through testing!**
