# Scenario 2: Date Validation Function

## Requirements

A date validation function accepts dates in `MM/DD/YYYY` format:

- **Month**: 01-12
- **Day**: 01-31 (varies by month)
- **Year**: 1900-2100
- **Format**: Must be `MM/DD/YYYY` with slashes

---

## Part A: Identify Partitions

### Month

- Valid: 01-12
- Invalid: < 01
- Invalid: > 12
- Invalid: Non-numeric

### Day

- Valid for 31-day months: 01-31
- Valid for 30-day months: 01-30
- Valid for February (non-leap): 01-28
- Valid for February (leap year): 01-29
- Invalid: < 01
- Invalid: > 31 for 31-day months
- Invalid: > 30 for 30-day months
- Invalid: > 28 for February in a non-leap year
- Invalid: > 29 for February in a leap year

### Year

- Valid: 1900-2100
- Invalid: < 1900
- Invalid: > 2100
- Invalid: Non-numeric

### Format

- Valid: `MM/DD/YYYY`
- Invalid: Wrong separator (`-`, `.`)
- Invalid: Missing separator
- Invalid: Wrong order (`DD/MM/YYYY`)


---

## Part B: Partition Table

| Partition | Description | Type | Example |
| --- | --- | --- | --- |
| P1 | Valid date - 31-day month | Valid | `01/15/2025` |
| P2 | Valid date - 30-day month | Valid | `04/20/2025` |
| P3 | Valid date - February non-leap | Valid | `02/15/2025` |
| P4 | Valid date - February 29 leap year | Valid | `02/29/2024` |
| P5 | Month below minimum (< 01) | Invalid | `00/15/2025` |
| P6 | Month above maximum (> 12) | Invalid | `13/15/2025` |
| P7 | Month is non-numeric | Invalid | `AA/15/2025` |
| P8 | Day below minimum (< 01) | Invalid | `01/00/2025` |
| P9 | Day above maximum for 31-day month | Invalid | `01/32/2025` |
| P10 | Day above maximum for 30-day month | Invalid | `04/31/2025` |
| P11 | Day above maximum for February non-leap | Invalid | `02/29/2025` |
| P12 | Day above maximum for February leap year | Invalid | `02/30/2024` |
| P13 | Year below minimum (< 1900) | Invalid | `01/15/1899` |
| P14 | Year above maximum (> 2100) | Invalid | `01/15/2101` |
| P15 | Year is non-numeric | Invalid | `01/15/ABCD` |
| P16 | Wrong separator | Invalid | `01-15-2025` |
| P17 | Missing separator | Invalid | `01152025` |
| P18 | Wrong order (`DD/MM/YYYY`) | Invalid | `15/01/2025` |

---

## Part C: Implementation

```python
def validate_date(date_string):
    """
    Validates date in MM/DD/YYYY format.

    Returns: (is_valid: bool, message: str)
    """

    # The value must contain exactly two "/" separators.
    parts = date_string.split("/")

    if len(parts) != 3:
        return False, "Invalid format. Use MM/DD/YYYY"

    month_text, day_text, year_text = parts

    # Each part must have the required number of characters.
    if len(month_text) != 2 or len(day_text) != 2 or len(year_text) != 4:
        return False, "Invalid format. Use MM/DD/YYYY"

    # Month must be numeric.
    if not month_text.isdigit():
        return False, "Month must be numeric"

    # Day must be numeric.
    if not day_text.isdigit():
        return False, "Day must be numeric"

    # Year must be numeric.
    if not year_text.isdigit():
        return False, "Year must be numeric"

    month = int(month_text)
    day = int(day_text)
    year = int(year_text)

    # Validate month.
    if month < 1 or month > 12:
        return False, "Month must be between 01 and 12"

    # Validate year.
    if year < 1900 or year > 2100:
        return False, "Year must be between 1900 and 2100"

    # Validate minimum day.
    if day < 1:
        return False, "Day must be at least 01"

    # Determine whether the year is a leap year.
    is_leap_year = (
        year % 400 == 0
        or (year % 4 == 0 and year % 100 != 0)
    )

    # Determine the maximum valid day for the selected month.
    if month == 2:
        max_day = 29 if is_leap_year else 28
    elif month in (4, 6, 9, 11):
        max_day = 30
    else:
        max_day = 31

    if day > max_day:
        return False, f"Day must be between 01 and {max_day:02d} for this month"

    return True, "Valid date"


def test_valid_31_day_month():
    """P1: Valid date in 31-day month"""
    valid, msg = validate_date("01/15/2025")

    assert valid == True


def test_valid_30_day_month():
    """P2: Valid date in 30-day month"""
    valid, msg = validate_date("04/20/2025")

    assert valid == True


def test_valid_february_non_leap():
    """P3: Valid February date in a non-leap year"""
    valid, msg = validate_date("02/15/2025")

    assert valid == True


def test_february_leap_year():
    """P4: February 29 in leap year"""
    valid, msg = validate_date("02/29/2024")

    assert valid == True


def test_month_below_minimum():
    """P5: Invalid month below 01"""
    valid, msg = validate_date("00/15/2025")

    assert valid == False


def test_month_above_maximum():
    """P6: Invalid month above 12"""
    valid, msg = validate_date("13/15/2025")

    assert valid == False


def test_month_non_numeric():
    """P7: Invalid non-numeric month"""
    valid, msg = validate_date("AA/15/2025")

    assert valid == False


def test_day_below_minimum():
    """P8: Invalid day below 01"""
    valid, msg = validate_date("01/00/2025")

    assert valid == False


def test_day_above_31():
    """P9: Invalid day above 31 in a 31-day month"""
    valid, msg = validate_date("01/32/2025")

    assert valid == False


def test_day_above_30_day_month():
    """P10: Invalid day 31 in a 30-day month"""
    valid, msg = validate_date("04/31/2025")

    assert valid == False


def test_february_non_leap_invalid_day():
    """P11: Invalid February 29 in a non-leap year"""
    valid, msg = validate_date("02/29/2025")

    assert valid == False


def test_february_leap_invalid_day():
    """P12: Invalid February 30 in a leap year"""
    valid, msg = validate_date("02/30/2024")

    assert valid == False


def test_year_below_minimum():
    """P13: Invalid year below 1900"""
    valid, msg = validate_date("01/15/1899")

    assert valid == False


def test_year_above_maximum():
    """P14: Invalid year above 2100"""
    valid, msg = validate_date("01/15/2101")

    assert valid == False


def test_year_non_numeric():
    """P15: Invalid non-numeric year"""
    valid, msg = validate_date("01/15/ABCD")

    assert valid == False


def test_wrong_separator():
    """P16: Invalid separator"""
    valid, msg = validate_date("01-15-2025")

    assert valid == False


def test_missing_separator():
    """P17: Missing separators"""
    valid, msg = validate_date("01152025")

    assert valid == False


def test_wrong_order():
    """P18: Date written as DD/MM/YYYY"""
    valid, msg = validate_date("15/01/2025")

    assert valid == False
```

---
