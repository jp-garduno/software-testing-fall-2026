# Statement Coverage

**Module**: 5 - White Box Testing  
**Topic**: Measuring Test Completeness at the Line Level  
**Reading Time**: 28 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Define statement coverage and calculate it
- Identify uncovered statements in code
- Write tests to achieve high statement coverage
- Understand why 100% statement coverage doesn't guarantee bug-free code
- Use coverage tools to measure statement coverage
- Interpret coverage reports

---

## What is Statement Coverage?

**Statement coverage** (also called **line coverage**) measures the percentage of executable statements in your code that are executed by your tests.

### Formula

```
Statement Coverage = (Executed Statements / Total Statements) × 100%
```

### Simple Example

```python
def is_positive(number):         # Line 1
    if number > 0:               # Line 2
        return True              # Line 3
    return False                 # Line 4
```

**Total statements**: 3 (lines 2, 3, 4)

**Test 1**: `is_positive(5)`

- Executes: Line 2 ✓, Line 3 ✓
- Coverage: 2/3 = 66.7%

**Test 2**: `is_positive(-5)`

- Executes: Line 2 ✓, Line 4 ✓
- Coverage: 2/3 = 66.7%

**Both tests together**:

- Executes: Line 2 ✓, Line 3 ✓, Line 4 ✓
- Coverage: 3/3 = **100%**

---

## How to Calculate Statement Coverage

### Step 1: Identify Executable Statements

Not all lines are executable statements:

```python
def calculate_discount(price, discount_rate):  # Not counted (function def)
    """Calculate discounted price"""           # Not counted (docstring)

    # Validate inputs                          # Not counted (comment)
    if price < 0:                              # Statement 1
        raise ValueError("Invalid price")      # Statement 2

    if discount_rate < 0 or discount_rate > 1: # Statement 3
        raise ValueError("Invalid discount")   # Statement 4

    discount = price * discount_rate           # Statement 5
    final_price = price - discount             # Statement 6
    return final_price                         # Statement 7
```

**Total executable statements**: 7

### Step 2: Run Tests and Track Execution

**Test 1**: `calculate_discount(100, 0.2)`

```python
def test_valid_discount():
    result = calculate_discount(100, 0.2)
    assert result == 80

# Executes: Lines 1, 3, 5, 6, 7
# Coverage: 5/7 = 71.4%
```

**Test 2**: `calculate_discount(-50, 0.2)`

```python
def test_negative_price():
    with pytest.raises(ValueError, match="Invalid price"):
        calculate_discount(-50, 0.2)

# Executes: Lines 1, 2
# Coverage: 2/7 = 28.6%
```

**Test 3**: `calculate_discount(100, 1.5)`

```python
def test_invalid_discount_rate():
    with pytest.raises(ValueError, match="Invalid discount"):
        calculate_discount(100, 1.5)

# Executes: Lines 1, 3, 4
# Coverage: 3/7 = 42.9%
```

### Step 3: Calculate Total Coverage

**All three tests together**:

- Execute: Lines 1, 2, 3, 4, 5, 6, 7
- Coverage: 7/7 = **100%**

---

## Visualizing Statement Coverage

### Coverage Report Format

```
Function: calculate_discount
─────────────────────────────────────────
Line | Code                              | Covered
─────────────────────────────────────────
  1  | def calculate_discount(...):      | -
  2  |     """docstring"""               | -
  3  |     if price < 0:                 | ✓
  4  |         raise ValueError(...)     | ✓
  5  |     if discount_rate < 0 or ...:  | ✓
  6  |         raise ValueError(...)     | ✓
  7  |     discount = price * ...        | ✓
  8  |     final_price = price - ...     | ✓
  9  |     return final_price            | ✓
─────────────────────────────────────────
Statement Coverage: 7/7 = 100%
```

### Color-Coded Visualization

```python
def process_order(order):
    if order.status == "pending":        # Green (covered)
        validate_order(order)            # Green (covered)
        charge_payment(order)            # Green (covered)
        return True                      # Green (covered)
    elif order.status == "cancelled":    # Red (not covered)
        refund_payment(order)            # Red (not covered)
        return False                     # Red (not covered)
    return None                          # Yellow (partially covered)
```

- **Green**: Executed by tests
- **Red**: Never executed
- **Yellow**: Partially executed (for multi-condition lines)

---

## Complete Example: Python

### Code to Test

```python
# user_service.py
class UserService:
    def __init__(self, database):
        self.db = database

    def create_user(self, email, age):
        # Validate email
        if not email or "@" not in email:
            raise ValueError("Invalid email format")

        # Validate age
        if age < 0:
            raise ValueError("Age cannot be negative")

        if age < 18:
            user_type = "minor"
        else:
            user_type = "adult"

        # Check if user exists
        if self.db.user_exists(email):
            raise ValueError("User already exists")

        # Create user
        user = self.db.create_user(email, age, user_type)
        return user
```

### Tests with Coverage Analysis

```python
# test_user_service.py
import pytest
from unittest.mock import Mock

def test_create_adult_user():
    """Test 1: Valid adult user"""
    # Arrange
    mock_db = Mock()
    mock_db.user_exists.return_value = False
    mock_db.create_user.return_value = {"email": "test@example.com", "age": 25}
    service = UserService(mock_db)

    # Act
    user = service.create_user("test@example.com", 25)

    # Assert
    assert user["age"] == 25
    mock_db.create_user.assert_called_once_with("test@example.com", 25, "adult")

# Lines executed: email validation (passed), age validation (passed),
#                 age >= 18 branch, user_exists check, create_user
# Coverage so far: ~70%

def test_create_minor_user():
    """Test 2: Valid minor user"""
    mock_db = Mock()
    mock_db.user_exists.return_value = False
    mock_db.create_user.return_value = {"email": "kid@example.com", "age": 15}
    service = UserService(mock_db)

    user = service.create_user("kid@example.com", 15)

    assert user["age"] == 15
    mock_db.create_user.assert_called_once_with("kid@example.com", 15, "minor")

# New lines executed: age < 18 branch
# Coverage so far: ~80%

def test_invalid_email():
    """Test 3: Invalid email format"""
    mock_db = Mock()
    service = UserService(mock_db)

    with pytest.raises(ValueError, match="Invalid email format"):
        service.create_user("invalidemail", 25)

# New lines executed: email validation failure path
# Coverage so far: ~85%

def test_negative_age():
    """Test 4: Negative age"""
    mock_db = Mock()
    service = UserService(mock_db)

    with pytest.raises(ValueError, match="Age cannot be negative"):
        service.create_user("test@example.com", -5)

# New lines executed: negative age validation path
# Coverage so far: ~92%

def test_user_already_exists():
    """Test 5: Duplicate user"""
    mock_db = Mock()
    mock_db.user_exists.return_value = True
    service = UserService(mock_db)

    with pytest.raises(ValueError, match="User already exists"):
        service.create_user("existing@example.com", 25)

# New lines executed: user exists check failure path
# Coverage: 100% ✓
```

### Coverage Report

```
Name                Stmts   Miss  Cover
─────────────────────────────────────────
user_service.py        14      0   100%
test_user_service.py   45      0   100%
─────────────────────────────────────────
TOTAL                  59      0   100%
```

---

## Complete Example: JavaScript

### Code to Test

```javascript
// userService.js
class UserService {
  constructor(database) {
    this.db = database;
  }

  createUser(email, age) {
    // Validate email
    if (!email || !email.includes("@")) {
      throw new Error("Invalid email format");
    }

    // Validate age
    if (age < 0) {
      throw new Error("Age cannot be negative");
    }

    let userType;
    if (age < 18) {
      userType = "minor";
    } else {
      userType = "adult";
    }

    // Check if user exists
    if (this.db.userExists(email)) {
      throw new Error("User already exists");
    }

    // Create user
    const user = this.db.createUser(email, age, userType);
    return user;
  }
}

module.exports = UserService;
```

### Tests with Coverage

```javascript
// userService.test.js
const UserService = require("./userService");

describe("UserService", () => {
  test("creates adult user successfully", () => {
    // Arrange
    const mockDb = {
      userExists: jest.fn().mockReturnValue(false),
      createUser: jest
        .fn()
        .mockReturnValue({ email: "test@example.com", age: 25 }),
    };
    const service = new UserService(mockDb);

    // Act
    const user = service.createUser("test@example.com", 25);

    // Assert
    expect(user.age).toBe(25);
    expect(mockDb.createUser).toHaveBeenCalledWith(
      "test@example.com",
      25,
      "adult",
    );
  });

  test("creates minor user successfully", () => {
    const mockDb = {
      userExists: jest.fn().mockReturnValue(false),
      createUser: jest
        .fn()
        .mockReturnValue({ email: "kid@example.com", age: 15 }),
    };
    const service = new UserService(mockDb);

    const user = service.createUser("kid@example.com", 15);

    expect(user.age).toBe(15);
    expect(mockDb.createUser).toHaveBeenCalledWith(
      "kid@example.com",
      15,
      "minor",
    );
  });

  test("throws error for invalid email", () => {
    const mockDb = {};
    const service = new UserService(mockDb);

    expect(() => {
      service.createUser("invalidemail", 25);
    }).toThrow("Invalid email format");
  });

  test("throws error for negative age", () => {
    const mockDb = {};
    const service = new UserService(mockDb);

    expect(() => {
      service.createUser("test@example.com", -5);
    }).toThrow("Age cannot be negative");
  });

  test("throws error for existing user", () => {
    const mockDb = {
      userExists: jest.fn().mockReturnValue(true),
    };
    const service = new UserService(mockDb);

    expect(() => {
      service.createUser("existing@example.com", 25);
    }).toThrow("User already exists");
  });
});
```

### Coverage Report (Jest)

```
─────────────────────────────────────────────────────
File             | % Stmts | % Branch | % Funcs | % Lines
─────────────────────────────────────────────────────
userService.js   |   100   |   100    |   100   |   100
─────────────────────────────────────────────────────
```

---

## Identifying Uncovered Statements

### Strategy 1: Look at Coverage Reports

Most coverage tools highlight uncovered lines:

```python
def process_payment(amount, method):
    if amount <= 0:                      # ✓ Covered
        raise ValueError("Invalid")       # ✓ Covered

    if method == "credit_card":          # ✓ Covered
        charge_credit_card(amount)       # ✓ Covered
    elif method == "paypal":             # ✓ Covered
        charge_paypal(amount)            # ✓ Covered
    elif method == "bitcoin":            # ✗ NOT COVERED
        charge_bitcoin(amount)           # ✗ NOT COVERED
    else:                                # ✗ NOT COVERED
        raise ValueError("Unknown")      # ✗ NOT COVERED
```

**Missing test**: Need to test `bitcoin` method and unknown method!

### Strategy 2: Trace Through Code Paths

For each conditional, ask: "Do I have tests for both outcomes?"

```python
def get_discount(customer):
    if customer.is_premium:              # Test both True and False?
        discount = 0.20                  # Test this path?
    else:
        discount = 0.10                  # Test this path?

    if customer.total_purchases > 1000:  # Test both True and False?
        discount += 0.05                 # Test this path?

    return discount
```

**Needed tests**:

1. Premium customer, high purchases → 0.25
2. Premium customer, low purchases → 0.20
3. Regular customer, high purchases → 0.15
4. Regular customer, low purchases → 0.10

### Strategy 3: Code Review Checklist

- [ ] Every `if` branch tested?
- [ ] Every `else` and `elif` tested?
- [ ] Every `return` statement reached?
- [ ] Every exception raised tested?
- [ ] Every function/method called at least once?

---

## Achieving 100% Statement Coverage

### Example: Incomplete Coverage

```python
def grade_score(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

# Only one test
def test_grade_a():
    assert grade_score(95) == "A"

# Coverage: 2/10 statements = 20%
```

### Achieving 100% Coverage

```python
def test_grade_a():
    assert grade_score(95) == "A"

def test_grade_b():
    assert grade_score(85) == "B"

def test_grade_c():
    assert grade_score(75) == "C"

def test_grade_d():
    assert grade_score(65) == "D"

def test_grade_f():
    assert grade_score(55) == "F"

# Coverage: 10/10 statements = 100%
```

### Complex Example: Nested Conditions

```python
def can_vote(age, citizenship, registered):
    if age < 18:
        return False

    if not citizenship:
        return False

    if not registered:
        return False

    return True

# Tests for 100% statement coverage
def test_underage():
    assert can_vote(16, True, True) == False

def test_not_citizen():
    assert can_vote(25, False, True) == False

def test_not_registered():
    assert can_vote(25, True, False) == False

def test_eligible():
    assert can_vote(25, True, True) == True

# Coverage: 100%
```

---

## Why 100% Statement Coverage ≠ Bug-Free

### Problem 1: Missing Logic

```python
def divide(a, b):
    result = a / b
    return result

# Test achieves 100% statement coverage
def test_divide():
    assert divide(10, 2) == 5

# But this crashes! (ZeroDivisionError)
# divide(10, 0)
```

**Issue**: Code doesn't handle division by zero, but test still covers all statements.

### Problem 2: Missing Boundary Cases

```python
def get_age_group(age):
    if age < 18:
        return "minor"
    else:
        return "adult"

# Test achieves 100% statement coverage
def test_minor():
    assert get_age_group(10) == "minor"

def test_adult():
    assert get_age_group(25) == "adult"

# But what about:
# get_age_group(18)   # Boundary
# get_age_group(-1)   # Invalid
# get_age_group(200)  # Unrealistic
```

**Issue**: 100% coverage but missing important test cases.

### Problem 3: Wrong Logic

```python
def calculate_discount(price, customer_level):
    # BUG: Should be customer_level >= 3, not > 3
    if customer_level > 3:
        discount = price * 0.20
    else:
        discount = price * 0.10
    return price - discount

# Test achieves 100% statement coverage
def test_high_level_discount():
    result = calculate_discount(100, 4)
    assert result == 80  # Passes

def test_low_level_discount():
    result = calculate_discount(100, 2)
    assert result == 90  # Passes

# But customer_level = 3 gets wrong discount!
# calculate_discount(100, 3)  # Returns 90, should be 80
```

**Issue**: 100% coverage but wrong business logic.

### Problem 4: Unchecked Return Values

```python
def save_user(user):
    db.insert(user)
    return True

# Test achieves 100% statement coverage
def test_save_user():
    user = {"name": "Alice"}
    result = save_user(user)
    assert result == True

# But doesn't verify that user was actually saved!
# db.get_user("Alice")  # Might return None
```

**Issue**: Test covers code but doesn't verify correctness.

---

## Statement Coverage Best Practices

### 1. Aim for High Coverage (80-90%+)

```python
# Coverage report
Name                Stmts   Miss  Cover
─────────────────────────────────────────
src/auth.py            50      2    96%   ← Excellent
src/utils.py           30     15    50%   ← Needs work
src/api.py             40      0   100%   ← Great
─────────────────────────────────────────
TOTAL                 120     17    86%   ← Good overall
```

### 2. Focus on Critical Code First

Prioritize coverage for:

- Business logic
- Security-critical code
- Data validation
- Error handling

Lower priority:

- Simple getters/setters
- Configuration code
- UI presentation logic

### 3. Don't Aim for 100% Everywhere

Some code is hard to test:

```python
# Low value to test
def __repr__(self):
    return f"User({self.email})"

# Hard to test (external dependency)
def send_email(to, subject, body):
    smtp_server.connect()
    smtp_server.send(to, subject, body)
    smtp_server.disconnect()
```

### 4. Combine with Other Coverage Metrics

Statement coverage alone is insufficient. Also use:

- **Branch coverage** (next topic)
- **Path coverage**
- **Condition coverage**
- **Integration tests**

---

## Practical Example: Increasing Coverage

### Initial Code with Low Coverage

```python
# shopping_cart.py
class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")

        # Check if item already in cart
        for cart_item in self.items:
            if cart_item["name"] == item.name:
                cart_item["quantity"] += quantity
                return

        # Add new item
        self.items.append({
            "name": item.name,
            "price": item.price,
            "quantity": quantity
        })

    def total(self):
        return sum(item["price"] * item["quantity"] for item in self.items)

    def apply_discount(self, code):
        if code == "SAVE10":
            return self.total() * 0.9
        elif code == "SAVE20":
            return self.total() * 0.8
        else:
            return self.total()

# Initial test (low coverage)
def test_add_item():
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item)
    assert len(cart.items) == 1

# Coverage: ~30%
```

### Adding Tests to Increase Coverage

```python
# test_shopping_cart.py
from unittest.mock import Mock
import pytest

def test_add_item_new_item():
    """Test adding a new item"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item)

    assert len(cart.items) == 1
    assert cart.items[0]["name"] == "Laptop"
    assert cart.items[0]["quantity"] == 1

def test_add_item_with_quantity():
    """Test adding item with specific quantity"""
    cart = ShoppingCart()
    item = Mock(name="Mouse", price=20)
    cart.add_item(item, quantity=3)

    assert cart.items[0]["quantity"] == 3

def test_add_item_existing_item():
    """Test adding same item twice increases quantity"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item, quantity=1)
    cart.add_item(item, quantity=2)

    assert len(cart.items) == 1  # Still one item type
    assert cart.items[0]["quantity"] == 3  # Quantity increased

def test_add_item_zero_quantity():
    """Test that zero quantity raises error"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(item, quantity=0)

def test_add_item_negative_quantity():
    """Test that negative quantity raises error"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)

    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_item(item, quantity=-1)

def test_total_empty_cart():
    """Test total of empty cart"""
    cart = ShoppingCart()
    assert cart.total() == 0

def test_total_single_item():
    """Test total with one item"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item, quantity=2)
    assert cart.total() == 2000

def test_total_multiple_items():
    """Test total with multiple items"""
    cart = ShoppingCart()
    item1 = Mock(name="Laptop", price=1000)
    item2 = Mock(name="Mouse", price=20)
    cart.add_item(item1, quantity=1)
    cart.add_item(item2, quantity=3)
    assert cart.total() == 1060

def test_apply_discount_save10():
    """Test SAVE10 discount code"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item)
    assert cart.apply_discount("SAVE10") == 900

def test_apply_discount_save20():
    """Test SAVE20 discount code"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item)
    assert cart.apply_discount("SAVE20") == 800

def test_apply_discount_invalid_code():
    """Test invalid discount code returns full price"""
    cart = ShoppingCart()
    item = Mock(name="Laptop", price=1000)
    cart.add_item(item)
    assert cart.apply_discount("INVALID") == 1000

# Coverage: 100% ✓
```

---

## Common Mistakes

### 1. Confusing Statement Coverage with Test Quality

❌ **Wrong thinking**: "100% coverage = perfect tests"  
✅ **Right thinking**: "100% coverage = all code executed, but need good assertions too"

### 2. Writing Tests Just for Coverage

❌ **Bad**: Test that doesn't verify behavior

```python
def test_useless():
    process_order()  # No assertion, just for coverage
```

✅ **Good**: Test that verifies correctness

```python
def test_process_order():
    order = create_test_order()
    result = process_order(order)
    assert result.status == "completed"
    assert result.confirmation_sent == True
```

### 3. Ignoring Unreachable Code

```python
def process_value(value):
    if value > 0:
        return "positive"
        print("This never runs!")  # Unreachable - should be removed
    return "non-positive"
```

**Fix**: Remove dead code instead of trying to cover it.

---

## Summary

**Statement Coverage**:

- Measures percentage of statements executed by tests
- Formula: (Executed / Total) × 100%
- Aim for 80-90%+ on critical code

**How to Achieve High Coverage**:

1. Test all conditional branches
2. Test error cases
3. Test edge cases
4. Use coverage reports to find gaps

**Important Reminders**:

- 100% statement coverage ≠ bug-free code
- Coverage is necessary but not sufficient
- Combine with branch coverage, integration tests
- Focus on quality tests, not just coverage numbers

---

## Practice Exercises

1. **Calculate Coverage**: For this function, calculate statement coverage for each test:

```python
def classify_temperature(temp):
    if temp < 0:
        return "freezing"
    elif temp < 20:
        return "cold"
    elif temp < 30:
        return "warm"
    else:
        return "hot"

# Test 1: classify_temperature(25)
# Test 2: classify_temperature(-5)
# Test 3: Both tests together
```

2. **Identify Gaps**: Find the uncovered statements and write tests to achieve 100% coverage:

```python
def validate_password(password):
    if len(password) < 8:
        return False, "Too short"
    if not any(c.isupper() for c in password):
        return False, "No uppercase"
    if not any(c.isdigit() for c in password):
        return False, "No digit"
    return True, "Valid"

# Current test
def test_valid_password():
    valid, msg = validate_password("Password123")
    assert valid == True
```

3. **Coverage vs Quality**: This test achieves 100% statement coverage. What's wrong with it?

```python
def transfer_money(from_account, to_account, amount):
    from_account.balance -= amount
    to_account.balance += amount
    return True

def test_transfer():
    acc1 = Account(balance=100)
    acc2 = Account(balance=50)
    result = transfer_money(acc1, acc2, 30)
    assert result == True  # What's missing?
```

---

## Next Steps

- Read [03-branch-coverage.md](./03-branch-coverage.md) to learn about testing decision points
- Practice with [Exercise 2: Statement Coverage](../exercises/02-statement-coverage.md)
- Set up coverage tools (covered in [05-coverage-tools.md](./05-coverage-tools.md))
