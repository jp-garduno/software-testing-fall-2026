# Branch Coverage

**Module**: 5 - White Box Testing  
**Topic**: Testing All Decision Outcomes  
**Reading Time**: 28 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Define branch coverage and distinguish it from statement coverage
- Identify all branches in code (if/else, switch, loops, ternary operators)
- Calculate branch coverage percentage
- Write tests to achieve 100% branch coverage
- Understand why branch coverage is stronger than statement coverage
- Apply short-circuit evaluation testing

---

## What is Branch Coverage?

**Branch coverage** measures whether each possible branch (outcome) of every decision point has been executed by your tests.

### Decision Points

A **decision point** is any place in code where execution can follow different paths:

- `if` statements
- `else` and `elif` clauses
- `switch`/`case` statements
- Ternary operators (`? :`)
- Logical operators (`&&`, `||`, `and`, `or`)
- Loop conditions

### Formula

```
Branch Coverage = (Executed Branches / Total Branches) × 100%
```

---

## Branch vs Statement Coverage

### Key Difference

**Statement coverage** asks: "Was this line executed?"  
**Branch coverage** asks: "Were both True and False outcomes tested?"

### Example Showing the Difference

```python
def check_eligibility(age):
    if age >= 18:
        return "eligible"
    return "not eligible"

# Test 1: Only tests one branch
def test_eligible():
    result = check_eligibility(25)
    assert result == "eligible"
```

**Statement Coverage**:

- Line 1: `if age >= 18:` ✓ Executed
- Line 2: `return "eligible"` ✓ Executed
- Line 3: `return "not eligible"` ✗ NOT executed
- Coverage: 2/3 = 66.7%

**Branch Coverage**:

- True branch (age >= 18): ✓ Tested
- False branch (age < 18): ✗ NOT tested
- Coverage: 1/2 = 50%

### Achieving 100% Branch Coverage

```python
def test_eligible():
    result = check_eligibility(25)
    assert result == "eligible"

def test_not_eligible():
    result = check_eligibility(15)
    assert result == "not eligible"
```

Now:

- **Statement Coverage**: 3/3 = 100%
- **Branch Coverage**: 2/2 = 100%

---

## Why Branch Coverage is Stronger

### Example: Hidden Bug

```python
def calculate_shipping(weight, is_express):
    cost = weight * 5
    if is_express:
        cost = cost + 10
    return cost

# Test with 100% statement coverage
def test_shipping():
    cost = calculate_shipping(2, True)
    assert cost == 20  # 2*5 + 10 = 20
```

**Statement Coverage**: 100% (all lines executed)  
**Branch Coverage**: 50% (only True branch tested)

**Hidden Bug**: What if `is_express` is `False`?

```python
# This would have caught the bug
def test_shipping_standard():
    cost = calculate_shipping(2, False)
    assert cost == 10  # Would catch if logic was wrong
```

**Branch coverage forces you to test both outcomes**, finding bugs that statement coverage misses.

---

## Identifying Branches

### 1. If Statements

```python
if condition:
    # Branch 1: True
    do_something()
else:
    # Branch 2: False
    do_something_else()

# Total branches: 2
```

**Without `else`**:

```python
if condition:
    # Branch 1: True
    do_something()
# Branch 2: False (implicit - falls through)

# Total branches: 2
```

### 2. Elif Chains

```python
if score >= 90:
    # Branch 1
    grade = "A"
elif score >= 80:
    # Branch 2
    grade = "B"
elif score >= 70:
    # Branch 3
    grade = "C"
else:
    # Branch 4
    grade = "F"

# Total branches: 4
```

### 3. Ternary Operators

```python
# Python
result = "pass" if score >= 60 else "fail"
# Total branches: 2 (True and False)

// JavaScript
const result = score >= 60 ? "pass" : "fail";
// Total branches: 2
```

### 4. Switch/Case Statements

```javascript
// JavaScript
switch (day) {
  case "Monday":
    return "Start of week"; // Branch 1
  case "Friday":
    return "End of week"; // Branch 2
  case "Saturday":
  case "Sunday":
    return "Weekend"; // Branch 3
  default:
    return "Midweek"; // Branch 4
}

// Total branches: 4
```

### 5. Logical Operators (Short-Circuit)

```python
# Python
if user.is_admin() and user.is_active():
    grant_access()

# Branches:
# 1. is_admin() returns False → second condition not evaluated
# 2. is_admin() returns True AND is_active() returns False
# 3. Both return True
# Total branches: 3 (not 2!)
```

```javascript
// JavaScript
if (user.isAdmin() && user.isActive()) {
  grantAccess();
}

// Same 3 branches as Python
```

### 6. Loop Conditions

```python
while condition:
    process()

# Branches:
# 1. Enter loop (condition True)
# 2. Skip loop (condition False)
# Total branches: 2
```

---

## Calculating Branch Coverage

### Example 1: Simple Function

```python
def get_discount(is_member, purchase_amount):
    discount = 0

    if is_member:                    # Decision 1: 2 branches
        discount = 0.10

    if purchase_amount > 100:        # Decision 2: 2 branches
        discount += 0.05

    return discount

# Total branches: 4 (2 + 2)
```

**Test 1**: `get_discount(True, 150)`

- Decision 1: True branch ✓
- Decision 2: True branch ✓
- Coverage: 2/4 = 50%

**Test 2**: `get_discount(False, 50)`

- Decision 1: False branch ✓
- Decision 2: False branch ✓
- Coverage: 4/4 = 100%

### Example 2: Multiple Conditions

```python
def can_drive(age, has_license, has_insurance):
    if age < 16:                     # Decision 1: 2 branches
        return False

    if not has_license:              # Decision 2: 2 branches
        return False

    if not has_insurance:            # Decision 3: 2 branches
        return False

    return True

# Total branches: 6 (2 + 2 + 2)
```

**Tests for 100% branch coverage**:

```python
def test_too_young():
    assert can_drive(15, True, True) == False  # Decision 1: True branch

def test_no_license():
    assert can_drive(18, False, True) == False  # Decision 2: True branch

def test_no_insurance():
    assert can_drive(18, True, False) == False  # Decision 3: True branch

def test_can_drive():
    assert can_drive(18, True, True) == True  # All False branches

# Coverage: 6/6 = 100%
```

---

## Complete Example: Python

### Code to Test

```python
# payment_processor.py
class PaymentProcessor:
    def process_payment(self, amount, method, user):
        # Validate amount
        if amount <= 0:
            raise ValueError("Amount must be positive")

        # Check user status
        if not user.is_active:
            raise ValueError("User account is inactive")

        # Apply discount for premium users
        final_amount = amount
        if user.is_premium:
            final_amount = amount * 0.9

        # Process based on method
        if method == "credit_card":
            if amount > user.credit_limit:
                raise ValueError("Exceeds credit limit")
            return self._charge_credit_card(final_amount)
        elif method == "paypal":
            return self._charge_paypal(final_amount)
        elif method == "bank_transfer":
            if amount < 100:
                raise ValueError("Minimum $100 for bank transfer")
            return self._charge_bank(final_amount)
        else:
            raise ValueError("Invalid payment method")

    def _charge_credit_card(self, amount):
        return {"status": "success", "method": "credit_card", "amount": amount}

    def _charge_paypal(self, amount):
        return {"status": "success", "method": "paypal", "amount": amount}

    def _charge_bank(self, amount):
        return {"status": "success", "method": "bank_transfer", "amount": amount}
```

### Tests for 100% Branch Coverage

```python
# test_payment_processor.py
import pytest
from unittest.mock import Mock

def create_user(is_active=True, is_premium=False, credit_limit=1000):
    user = Mock()
    user.is_active = is_active
    user.is_premium = is_premium
    user.credit_limit = credit_limit
    return user

class TestPaymentProcessor:
    def setup_method(self):
        self.processor = PaymentProcessor()

    # Branch 1: amount <= 0 (True)
    def test_negative_amount(self):
        user = create_user()
        with pytest.raises(ValueError, match="Amount must be positive"):
            self.processor.process_payment(-10, "credit_card", user)

    # Branch 2: amount > 0 (False of branch 1)
    # Branch 3: user.is_active (False)
    def test_inactive_user(self):
        user = create_user(is_active=False)
        with pytest.raises(ValueError, match="User account is inactive"):
            self.processor.process_payment(100, "credit_card", user)

    # Branch 4: user.is_active (True)
    # Branch 5: user.is_premium (True)
    def test_premium_user_discount(self):
        user = create_user(is_premium=True)
        result = self.processor.process_payment(100, "paypal", user)
        assert result["amount"] == 90  # 10% discount

    # Branch 6: user.is_premium (False)
    # Branch 7: method == "credit_card" (True)
    # Branch 8: amount > credit_limit (False)
    def test_credit_card_within_limit(self):
        user = create_user(credit_limit=500)
        result = self.processor.process_payment(400, "credit_card", user)
        assert result["status"] == "success"
        assert result["method"] == "credit_card"

    # Branch 9: amount > credit_limit (True)
    def test_credit_card_exceeds_limit(self):
        user = create_user(credit_limit=500)
        with pytest.raises(ValueError, match="Exceeds credit limit"):
            self.processor.process_payment(600, "credit_card", user)

    # Branch 10: method == "paypal" (True)
    def test_paypal_payment(self):
        user = create_user()
        result = self.processor.process_payment(100, "paypal", user)
        assert result["status"] == "success"
        assert result["method"] == "paypal"

    # Branch 11: method == "bank_transfer" (True)
    # Branch 12: amount < 100 (False)
    def test_bank_transfer_above_minimum(self):
        user = create_user()
        result = self.processor.process_payment(200, "bank_transfer", user)
        assert result["status"] == "success"
        assert result["method"] == "bank_transfer"

    # Branch 13: amount < 100 (True)
    def test_bank_transfer_below_minimum(self):
        user = create_user()
        with pytest.raises(ValueError, match="Minimum $100"):
            self.processor.process_payment(50, "bank_transfer", user)

    # Branch 14: Invalid payment method (else clause)
    def test_invalid_payment_method(self):
        user = create_user()
        with pytest.raises(ValueError, match="Invalid payment method"):
            self.processor.process_payment(100, "bitcoin", user)

# Branch Coverage: 14/14 = 100%
```

---

## Complete Example: JavaScript

### Code to Test

```javascript
// userValidator.js
class UserValidator {
  validateRegistration(username, email, age, termsAccepted) {
    // Validate username
    if (!username || username.length < 3) {
      return { valid: false, error: "Username too short" };
    }

    if (username.length > 20) {
      return { valid: false, error: "Username too long" };
    }

    // Validate email
    if (!email || !email.includes("@")) {
      return { valid: false, error: "Invalid email" };
    }

    // Validate age
    if (age < 13) {
      return { valid: false, error: "Must be 13 or older" };
    }

    // Check terms
    if (!termsAccepted) {
      return { valid: false, error: "Must accept terms" };
    }

    // Check if minor
    let accountType;
    if (age < 18) {
      accountType = "minor";
    } else {
      accountType = "adult";
    }

    return { valid: true, accountType };
  }
}

module.exports = UserValidator;
```

### Tests for 100% Branch Coverage

```javascript
// userValidator.test.js
const UserValidator = require("./userValidator");

describe("UserValidator", () => {
  let validator;

  beforeEach(() => {
    validator = new UserValidator();
  });

  // Branch 1: username.length < 3 (True)
  test("rejects username shorter than 3 characters", () => {
    const result = validator.validateRegistration(
      "ab",
      "test@example.com",
      20,
      true,
    );
    expect(result.valid).toBe(false);
    expect(result.error).toBe("Username too short");
  });

  // Branch 2: username.length < 3 (False)
  // Branch 3: username.length > 20 (True)
  test("rejects username longer than 20 characters", () => {
    const result = validator.validateRegistration(
      "thisusernameiswaytoolong",
      "test@example.com",
      20,
      true,
    );
    expect(result.valid).toBe(false);
    expect(result.error).toBe("Username too long");
  });

  // Branch 4: username.length > 20 (False)
  // Branch 5: !email.includes('@') (True)
  test("rejects invalid email format", () => {
    const result = validator.validateRegistration(
      "john",
      "invalidemail",
      20,
      true,
    );
    expect(result.valid).toBe(false);
    expect(result.error).toBe("Invalid email");
  });

  // Branch 6: email.includes('@') (False - valid email)
  // Branch 7: age < 13 (True)
  test("rejects users under 13", () => {
    const result = validator.validateRegistration(
      "john",
      "john@example.com",
      10,
      true,
    );
    expect(result.valid).toBe(false);
    expect(result.error).toBe("Must be 13 or older");
  });

  // Branch 8: age >= 13 (False of branch 7)
  // Branch 9: !termsAccepted (True)
  test("rejects when terms not accepted", () => {
    const result = validator.validateRegistration(
      "john",
      "john@example.com",
      20,
      false,
    );
    expect(result.valid).toBe(false);
    expect(result.error).toBe("Must accept terms");
  });

  // Branch 10: termsAccepted (False of branch 9)
  // Branch 11: age < 18 (True)
  test("creates minor account for users under 18", () => {
    const result = validator.validateRegistration(
      "john",
      "john@example.com",
      15,
      true,
    );
    expect(result.valid).toBe(true);
    expect(result.accountType).toBe("minor");
  });

  // Branch 12: age >= 18 (False of branch 11)
  test("creates adult account for users 18 and over", () => {
    const result = validator.validateRegistration(
      "john",
      "john@example.com",
      25,
      true,
    );
    expect(result.valid).toBe(true);
    expect(result.accountType).toBe("adult");
  });
});

// Branch Coverage: 12/12 = 100%
```

---

## Short-Circuit Evaluation

### What is Short-Circuit Evaluation?

Logical operators (`and`, `or`, `&&`, `||`) may not evaluate all conditions:

**Python**:

```python
if condition1 and condition2:
    do_something()
```

- If `condition1` is `False`, `condition2` is **never evaluated**
- Creates an extra branch!

**JavaScript**:

```javascript
if (condition1 && condition2) {
  doSomething();
}
```

- Same behavior as Python

### Example with Short-Circuit

```python
def process_user(user):
    if user is not None and user.is_active:
        return "processing"
    return "skipped"

# Three branches exist:
# 1. user is None → short-circuits, doesn't check is_active
# 2. user is not None AND is_active is False
# 3. user is not None AND is_active is True
```

### Tests for Short-Circuit Branches

```python
def test_user_is_none():
    """Branch 1: Short-circuit on None"""
    result = process_user(None)
    assert result == "skipped"

def test_user_inactive():
    """Branch 2: User exists but inactive"""
    user = Mock(is_active=False)
    result = process_user(user)
    assert result == "skipped"

def test_user_active():
    """Branch 3: Both conditions True"""
    user = Mock(is_active=True)
    result = process_user(user)
    assert result == "processing"

# Branch Coverage: 3/3 = 100%
```

### JavaScript Example

```javascript
function processUser(user) {
  if (user && user.isActive) {
    return "processing";
  }
  return "skipped";
}

describe("processUser", () => {
  test("returns skipped when user is null", () => {
    expect(processUser(null)).toBe("skipped");
  });

  test("returns skipped when user is inactive", () => {
    const user = { isActive: false };
    expect(processUser(user)).toBe("skipped");
  });

  test("returns processing when user is active", () => {
    const user = { isActive: true };
    expect(processUser(user)).toBe("processing");
  });
});
```

### Complex Short-Circuit Example

```python
def can_access(user, resource):
    if user.is_admin or (user.is_owner and resource.is_public):
        return True
    return False

# Branches:
# 1. user.is_admin = True (short-circuits, doesn't check rest)
# 2. user.is_admin = False AND user.is_owner = False
# 3. user.is_admin = False AND user.is_owner = True AND is_public = False
# 4. user.is_admin = False AND user.is_owner = True AND is_public = True
# Total: 4 branches
```

**Tests**:

```python
def test_admin_access():
    user = Mock(is_admin=True, is_owner=False)
    resource = Mock(is_public=False)
    assert can_access(user, resource) == True

def test_not_owner():
    user = Mock(is_admin=False, is_owner=False)
    resource = Mock(is_public=True)
    assert can_access(user, resource) == False

def test_owner_private_resource():
    user = Mock(is_admin=False, is_owner=True)
    resource = Mock(is_public=False)
    assert can_access(user, resource) == False

def test_owner_public_resource():
    user = Mock(is_admin=False, is_owner=True)
    resource = Mock(is_public=True)
    assert can_access(user, resource) == True
```

---

## Branch Coverage vs Statement Coverage

### Example Showing the Gap

```python
def calculate_price(base_price, is_member, quantity):
    price = base_price * quantity

    if is_member and quantity > 10:
        price = price * 0.8  # 20% discount

    return price

# Test 1: Achieves 100% statement coverage
def test_with_discount():
    result = calculate_price(10, True, 15)
    assert result == 120  # 10 * 15 * 0.8

# Statement coverage: 100% (all lines executed)
# Branch coverage: 50% (only True branch tested)
```

**Missing tests for branch coverage**:

```python
def test_not_member():
    """is_member = False → short-circuit"""
    result = calculate_price(10, False, 15)
    assert result == 150

def test_low_quantity():
    """quantity <= 10 → discount not applied"""
    result = calculate_price(10, True, 5)
    assert result == 50

# Now branch coverage: 100%
```

---

## Achieving 100% Branch Coverage

### Strategy 1: Test Each Decision Outcome

For every `if`, test both:

- Condition is True
- Condition is False

### Strategy 2: Use Coverage Tools

Coverage tools can show branch coverage:

```
Name                  Stmts   Miss Branch BrPart  Cover
──────────────────────────────────────────────────────
payment.py               24      0     12      0   100%
user_service.py          18      2      8      1    89%
──────────────────────────────────────────────────────
TOTAL                    42      2     20      1    94%
```

- **Branch**: Total branches
- **BrPart**: Partially covered branches (one outcome not tested)

### Strategy 3: Checklist Method

For each function:

- [ ] Every `if` tested True and False
- [ ] Every `elif` tested
- [ ] Every `else` tested
- [ ] Ternary operators tested both ways
- [ ] Loop tested entering and skipping
- [ ] Short-circuit operators tested all paths

### Example: Complete Branch Coverage

```python
def get_shipping_cost(weight, destination, is_express):
    # Base cost
    if weight <= 0:
        raise ValueError("Invalid weight")

    cost = weight * 5

    # Destination multiplier
    if destination == "international":
        cost = cost * 2
    elif destination == "remote":
        cost = cost * 1.5
    # else: domestic (no change)

    # Express shipping
    if is_express:
        cost = cost + 20

    return cost

# Tests for 100% branch coverage
def test_invalid_weight():
    with pytest.raises(ValueError):
        get_shipping_cost(0, "domestic", False)

def test_domestic_standard():
    assert get_shipping_cost(10, "domestic", False) == 50

def test_domestic_express():
    assert get_shipping_cost(10, "domestic", True) == 70

def test_international_standard():
    assert get_shipping_cost(10, "international", False) == 100

def test_international_express():
    assert get_shipping_cost(10, "international", True) == 120

def test_remote_standard():
    assert get_shipping_cost(10, "remote", False) == 75

def test_remote_express():
    assert get_shipping_cost(10, "remote", True) == 95

# Branch coverage: 100%
```

---

## Common Mistakes

### 1. Forgetting the Implicit Else

```python
def process(value):
    if value > 0:
        return "positive"
    # Implicit else: returns None

# Need test for value <= 0!
def test_non_positive():
    result = process(0)
    assert result is None
```

### 2. Not Testing All elif Branches

```python
def categorize(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    # Need tests for ALL branches
```

### 3. Ignoring Short-Circuit Logic

```python
if user and user.is_active:
    pass

# Need 3 tests:
# 1. user is None
# 2. user exists, is_active False
# 3. user exists, is_active True
```

---

## Branch Coverage Best Practices

### 1. Aim for 100% on Critical Code

For security, payments, data validation:

```python
# This should have 100% branch coverage
def authorize_transaction(user, amount):
    if not user.is_authenticated:
        raise AuthError("Not authenticated")

    if amount > user.balance:
        raise InsufficientFunds("Not enough balance")

    if amount > 10000:
        if not user.has_two_factor:
            raise SecurityError("2FA required")

    return approve_transaction(user, amount)
```

### 2. Document Untested Branches

If you can't test a branch, document why:

```python
def process_file(filename):
    try:
        with open(filename) as f:
            return f.read()
    except FileNotFoundError:  # Tested
        return None
    except PermissionError:    # Hard to test - OS dependent
        return None            # Marked as untested in coverage
```

### 3. Use Branch Coverage in CI/CD

```yaml
# .github/workflows/test.yml
- name: Run tests with coverage
  run: pytest --cov --cov-branch --cov-fail-under=90
```

Fail builds if branch coverage drops below threshold.

---

## Summary

**Branch Coverage**:

- Tests both True and False outcomes of every decision
- Formula: (Tested Branches / Total Branches) × 100%
- Stronger than statement coverage

**Key Concepts**:

- Every `if`, `elif`, `else` creates branches
- Ternary operators have 2 branches
- Short-circuit operators create extra branches
- Loops have 2 branches (enter/skip)

**How to Achieve 100%**:

1. Test every condition as True and False
2. Use coverage tools to find gaps
3. Pay attention to short-circuit evaluation
4. Test all `elif` and `else` clauses

**Remember**: Branch coverage is necessary but not sufficient. Combine with:

- Statement coverage
- Path coverage
- Integration tests
- Edge case testing

---

## Practice Exercises

1. **Calculate Branch Coverage**: How many branches does this function have? What tests are needed for 100% coverage?

```python
def calculate_tax(income, is_married, has_children):
    tax_rate = 0.20

    if income < 50000:
        tax_rate = 0.10
    elif income < 100000:
        tax_rate = 0.15

    if is_married:
        tax_rate = tax_rate - 0.02

    if has_children and income < 80000:
        tax_rate = tax_rate - 0.01

    return income * tax_rate
```

2. **Find Missing Branches**: This test suite has 80% branch coverage. Which branches are missing?

```python
def validate_order(items, customer):
    if not items:
        return False, "Empty order"

    if customer.is_blocked:
        return False, "Customer blocked"

    total = sum(item.price for item in items)

    if total > customer.credit_limit:
        return False, "Exceeds limit"

    return True, "Valid"

# Existing tests
def test_valid_order():
    items = [Mock(price=10), Mock(price=20)]
    customer = Mock(is_blocked=False, credit_limit=100)
    valid, msg = validate_order(items, customer)
    assert valid == True

def test_empty_order():
    valid, msg = validate_order([], Mock())
    assert valid == False
```

3. **Short-Circuit Testing**: Write tests for 100% branch coverage including short-circuit paths:

```python
def can_edit(user, document):
    if user.is_admin or (user.id == document.owner_id and not document.is_locked):
        return True
    return False
```

---

## Next Steps

- Read [04-path-coverage.md](./04-path-coverage.md) to learn about testing execution paths
- Practice with [Exercise 3: Branch Coverage](../exercises/03-branch-coverage.md)
- Set up branch coverage reporting in [05-coverage-tools.md](./05-coverage-tools.md)
