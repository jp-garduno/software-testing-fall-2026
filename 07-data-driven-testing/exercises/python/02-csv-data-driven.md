# Exercise 2: CSV Data-Driven Testing (Python)

## Objective

Learn to load test data from CSV files and use it in parameterized tests.

## Scenario: User Registration Validation

You are testing a user registration system that validates various user inputs. Test data is stored in CSV files for easy management.

## Part 1: Email Validation

### Task

Create a system to validate email addresses using test data from a CSV file.

**email_validator.py**:

```python
import re

def is_valid_email(email):
    """
    Validate email format

    Rules:
    - Must contain exactly one @
    - Must have local part before @
    - Must have domain after @
    - Domain must contain at least one dot
    - No spaces allowed
    """
    if not email or ' ' in email:
        return False

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**test_data/emails.csv**:

```csv
email,valid,reason
user@example.com,True,Standard valid email
test.user@example.co.uk,True,Multiple dots in domain
user+tag@example.com,True,Plus sign in local part
user_name@example.com,True,Underscore in local part
invalid@,False,Missing domain
@example.com,False,Missing local part
user@example,False,Missing TLD
user example@test.com,False,Space in email
user@@example.com,False,Double at sign
,False,Empty email
user@.com,False,Domain starts with dot
user@example..com,False,Consecutive dots in domain
```

**test_email_validator.py**:

```python
import pytest
import csv
import os

from email_validator import is_valid_email

def load_email_test_data():
    """Load test data from CSV file"""
    test_data = []
    csv_path = os.path.join(os.path.dirname(__file__), 'test_data', 'emails.csv')

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append((
                row['email'],
                row['valid'] == 'True',
                row['reason']
            ))

    return test_data

@pytest.mark.parametrize(
    "email,expected,reason",
    load_email_test_data(),
    ids=lambda val: val if isinstance(val, str) and len(val) < 30 else str(val)[:30]
)
def test_email_validation(email, expected, reason):
    """Test email validation with data from CSV"""
    result = is_valid_email(email)
    assert result == expected, f"Failed for: {reason}"
```

### Requirements

1. Implement the `is_valid_email()` function
2. Create the CSV file with at least 12 test cases
3. Implement the test that loads data from CSV
4. All tests should pass

## Part 2: Password Strength Validation

### Task

Test password strength validation using CSV data.

**password_validator.py**:

```python
def check_password_strength(password):
    """
    Check password strength

    Returns:
        str: "weak", "medium", or "strong"

    Rules:
    - Weak: < 8 characters
    - Medium: >= 8 characters, has letters and numbers
    - Strong: >= 12 characters, has letters, numbers, and special characters
    """
    if len(password) < 8:
        return "weak"

    has_letter = any(c.isalpha() for c in password)
    has_number = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if len(password) >= 12 and has_letter and has_number and has_special:
        return "strong"
    elif has_letter and has_number:
        return "medium"
    else:
        return "weak"
```

**test_data/passwords.csv**:

```csv
password,strength,reason
abc,weak,Too short
password123,medium,8+ chars with letters and numbers
P@ssw0rd!2023,strong,12+ chars with all character types
12345678,weak,Only numbers
abcdefgh,weak,Only letters
Pass1234,medium,Exactly 8 chars with letters and numbers
MyP@ssw0rd123!,strong,Long with all types
```

### Requirements

1. Create `passwords.csv` with at least 10 test cases
2. Implement `test_password_strength.py` that loads CSV data
3. Test all password strength levels
4. Include edge cases

## Part 3: User Registration Data

### Task

Test complete user registration validation using CSV data.

**user_validator.py**:

```python
def validate_user_registration(username, email, age, country):
    """
    Validate user registration data

    Returns:
        tuple: (is_valid: bool, errors: list)

    Rules:
    - Username: 3-20 characters, alphanumeric only
    - Email: valid format
    - Age: 13-120
    - Country: 2-letter country code (uppercase)
    """
    errors = []

    # Username validation
    if not username or len(username) < 3 or len(username) > 20:
        errors.append("Username must be 3-20 characters")
    elif not username.isalnum():
        errors.append("Username must be alphanumeric")

    # Email validation
    if not email or '@' not in email:
        errors.append("Invalid email format")

    # Age validation
    try:
        age_int = int(age)
        if age_int < 13 or age_int > 120:
            errors.append("Age must be between 13 and 120")
    except (ValueError, TypeError):
        errors.append("Age must be a number")

    # Country validation
    if not country or len(country) != 2 or not country.isupper():
        errors.append("Country must be 2-letter code (uppercase)")

    return (len(errors) == 0, errors)
```

**test_data/user_registrations.csv**:

```csv
username,email,age,country,valid,expected_errors
alice123,alice@example.com,25,US,True,[]
ab,bob@example.com,30,US,False,Username must be 3-20 characters
user!@#,test@example.com,20,US,False,Username must be alphanumeric
validuser,invalid-email,25,US,False,Invalid email format
testuser,test@example.com,10,US,False,Age must be between 13 and 120
gooduser,good@example.com,25,us,False,Country must be 2-letter code (uppercase)
```

### Requirements

1. Create comprehensive CSV with at least 15 test cases
2. Test valid registrations
3. Test each validation rule failing individually
4. Test multiple validation failures
5. Implement tests that verify both `is_valid` and `errors` list

**test_user_validator.py**:

```python
import pytest
import csv
import ast
from user_validator import validate_user_registration

def load_user_test_data():
    """Load user registration test data from CSV"""
    # TODO: Implement
    pass

@pytest.mark.parametrize(
    "username,email,age,country,expected_valid,expected_errors",
    load_user_test_data(),
    ids=lambda val: str(val)[:20] if isinstance(val, str) else ""
)
def test_user_registration(username, email, age, country, expected_valid, expected_errors):
    """Test user registration validation"""
    is_valid, errors = validate_user_registration(username, email, age, country)

    assert is_valid == expected_valid, f"Validation result mismatch for {username}"

    if not expected_valid:
        # Check that expected errors are present
        for expected_error in expected_errors:
            assert any(expected_error in error for error in errors), \
                f"Expected error '{expected_error}' not found in {errors}"
```

## Part 4: CSV Data Management

### Bonus Task

Create a helper module for CSV test data management.

**csv_test_helper.py**:

```python
import csv
import os
from typing import List, Dict

class CSVTestDataLoader:
    """Helper class for loading test data from CSV files"""

    def __init__(self, data_dir='test_data'):
        self.data_dir = data_dir

    def load(self, filename: str) -> List[Dict]:
        """Load CSV file and return list of dictionaries"""
        filepath = os.path.join(self.data_dir, filename)

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Test data file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)

    def convert_types(self, data: List[Dict], type_map: Dict[str, type]) -> List[tuple]:
        """Convert CSV string data to specified types"""
        result = []

        for row in data:
            converted = []
            for key, target_type in type_map.items():
                value = row.get(key)

                if target_type == bool:
                    converted.append(value == 'True')
                elif target_type == int:
                    converted.append(int(value))
                elif target_type == float:
                    converted.append(float(value))
                elif target_type == list:
                    # Parse list from string representation
                    import ast
                    converted.append(ast.literal_eval(value))
                else:
                    converted.append(value)

            result.append(tuple(converted))

        return result

# Usage example
loader = CSVTestDataLoader()
data = loader.load('emails.csv')
typed_data = loader.convert_types(data, {
    'email': str,
    'valid': bool,
    'reason': str
})
```

## Expected Output

```bash
$ pytest test_email_validator.py -v

test_email_validator.py::test_email_validation[user@example.com] PASSED
test_email_validator.py::test_email_validation[test.user@example.co.uk] PASSED
test_email_validator.py::test_email_validation[invalid@] PASSED
...

==================== 12 passed in 0.03s ====================

$ pytest test_password_strength.py -v
...
==================== 10 passed in 0.02s ====================

$ pytest test_user_validator.py -v
...
==================== 15 passed in 0.04s ====================
```

## Tips

1. Use `os.path.join()` for cross-platform file paths
2. Use `encoding='utf-8'` when opening CSV files
3. Convert string types from CSV to appropriate Python types
4. Use `csv.DictReader` for easier column access
5. Handle empty/missing values in CSV

## Submission

Submit:

- All Python modules (`*_validator.py`)
- All test files (`test_*.py`)
- All CSV files in `test_data/` directory
- README explaining your test data structure
- Screenshot of all tests passing

## Grading Criteria

- Correct implementation: 30%
- CSV data quality (comprehensive cases): 30%
- Test implementation: 25%
- Code organization: 10%
- Documentation: 5%
