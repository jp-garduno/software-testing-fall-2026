# Path Coverage

**Module**: 5 - White Box Testing  
**Topic**: Testing Independent Execution Paths  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Define path coverage and distinguish it from branch coverage
- Calculate cyclomatic complexity for functions
- Identify independent paths in code
- Understand the path explosion problem
- Know when path coverage is practical vs. impractical
- Use basis path testing techniques
- Understand the relationship between complexity and testability

---

## What is Path Coverage?

**Path coverage** measures whether every possible execution path through a program has been tested.

### Definition

A **path** is a unique sequence of statements from the entry point to the exit point of a function.

### Simple Example

```python
def classify_number(n):
    if n > 0:                # Decision 1
        if n % 2 == 0:       # Decision 2
            return "positive even"
        else:
            return "positive odd"
    else:
        return "non-positive"
```

**Possible Paths**:

1. `n > 0` (False) → return "non-positive"
2. `n > 0` (True) → `n % 2 == 0` (True) → return "positive even"
3. `n > 0` (True) → `n % 2 == 0` (False) → return "positive odd"

**Total paths**: 3

### Visualizing Paths

```
Start
  │
  ├─ n > 0?
  │   ├─ YES ─ n % 2 == 0?
  │   │        ├─ YES → "positive even"    (Path 2)
  │   │        └─ NO  → "positive odd"     (Path 3)
  │   │
  │   └─ NO → "non-positive"               (Path 1)
  │
End
```

---

## Path Coverage vs Branch Coverage

### Key Difference

- **Branch coverage**: Tests each decision outcome
- **Path coverage**: Tests each unique sequence of decisions

### Example Showing the Difference

```python
def discount_calculator(is_member, quantity):
    discount = 0

    if is_member:          # Decision 1
        discount += 10

    if quantity > 5:       # Decision 2
        discount += 5

    return discount
```

**Branches**: 4 (2 decisions × 2 outcomes each)

1. `is_member` True
2. `is_member` False
3. `quantity > 5` True
4. `quantity > 5` False

**Paths**: 4 (all combinations)

1. `is_member` False, `quantity > 5` False → discount = 0
2. `is_member` False, `quantity > 5` True → discount = 5
3. `is_member` True, `quantity > 5` False → discount = 10
4. `is_member` True, `quantity > 5` True → discount = 15

### Branch Coverage Without Path Coverage

```python
# Test 1: Branch coverage = 100%
def test_member_high_quantity():
    assert discount_calculator(True, 10) == 15

def test_non_member_low_quantity():
    assert discount_calculator(False, 2) == 0

# All 4 branches tested, but only 2 out of 4 paths tested!
# Missing paths:
# - is_member True, quantity <= 5
# - is_member False, quantity > 5
```

**100% branch coverage ≠ 100% path coverage**

---

## Cyclomatic Complexity

### Definition

**Cyclomatic complexity** (also called **McCabe complexity**) measures the number of independent paths through code.

### Formula

```
Cyclomatic Complexity = E - N + 2P

Where:
E = Number of edges in the control flow graph
N = Number of nodes
P = Number of connected components (usually 1)
```

### Simplified Formula

For most functions:

```
Cyclomatic Complexity = Number of decision points + 1
```

**Decision points**: `if`, `elif`, `while`, `for`, `case`, `&&`, `||`, `?:`

### Example Calculations

**Example 1**: No decisions

```python
def add(a, b):
    result = a + b
    return result

# Complexity: 0 decisions + 1 = 1
```

**Example 2**: One if statement

```python
def absolute(n):
    if n < 0:
        return -n
    return n

# Complexity: 1 decision + 1 = 2
```

**Example 3**: Multiple decisions

```python
def grade_calculator(score):
    if score >= 90:        # Decision 1
        return "A"
    elif score >= 80:      # Decision 2
        return "B"
    elif score >= 70:      # Decision 3
        return "C"
    elif score >= 60:      # Decision 4
        return "D"
    else:
        return "F"

# Complexity: 4 decisions + 1 = 5
# Need 5 tests for full path coverage
```

**Example 4**: Nested conditions

```python
def shipping_cost(weight, is_international):
    if weight > 0:                    # Decision 1
        if is_international:          # Decision 2
            return weight * 10
        else:
            return weight * 5
    return 0

# Complexity: 2 decisions + 1 = 3
```

---

## Identifying Independent Paths

### Method 1: Control Flow Graph

**Code**:

```python
def login(username, password):
    if not username:           # Node 1
        return "No username"   # Node 2

    if not password:           # Node 3
        return "No password"   # Node 4

    if authenticate(username, password):  # Node 5
        return "Success"       # Node 6
    else:
        return "Failed"        # Node 7
```

**Control Flow Graph**:

```
Start
  │
  1. if not username
  │   ├─ True → 2. return "No username"
  │   │
  │   └─ False → 3. if not password
  │               ├─ True → 4. return "No password"
  │               │
  │               └─ False → 5. if authenticate()
  │                           ├─ True → 6. return "Success"
  │                           └─ False → 7. return "Failed"
End
```

**Independent Paths**:

1. Start → 1 (True) → 2 → End
2. Start → 1 (False) → 3 (True) → 4 → End
3. Start → 1 (False) → 3 (False) → 5 (True) → 6 → End
4. Start → 1 (False) → 3 (False) → 5 (False) → 7 → End

**Cyclomatic Complexity**: 3 decisions + 1 = **4 paths**

### Method 2: Basis Path Testing

Identify a **baseline path**, then vary one condition at a time.

**Code**:

```python
def calculate_discount(price, is_member, quantity):
    discount = 0

    if price < 100:         # Decision 1
        return 0

    if is_member:           # Decision 2
        discount += 10

    if quantity > 5:        # Decision 3
        discount += 5

    return discount
```

**Basis Paths**:

1. **Baseline**: All conditions False → price >= 100, not member, quantity <= 5
2. **Vary D1**: price < 100 (exit early)
3. **Vary D2**: price >= 100, is_member = True, quantity <= 5
4. **Vary D3**: price >= 100, not member, quantity > 5

**Cyclomatic Complexity**: 3 decisions + 1 = **4 paths**

### Tests for Independent Paths

```python
def test_baseline():
    """Path 1: price >= 100, not member, low quantity"""
    assert calculate_discount(150, False, 3) == 0

def test_price_too_low():
    """Path 2: price < 100"""
    assert calculate_discount(50, True, 10) == 0

def test_member_discount():
    """Path 3: price >= 100, is_member"""
    assert calculate_discount(150, True, 3) == 10

def test_quantity_discount():
    """Path 4: price >= 100, high quantity"""
    assert calculate_discount(150, False, 10) == 5

# Optional: Test combination (not required for basis path testing)
def test_both_discounts():
    assert calculate_discount(150, True, 10) == 15
```

---

## The Path Explosion Problem

### What is Path Explosion?

As code complexity increases, the number of paths grows **exponentially**.

### Example: Multiple Independent Conditions

```python
def complex_function(a, b, c, d, e):
    result = 0

    if a:          # Decision 1
        result += 1

    if b:          # Decision 2
        result += 2

    if c:          # Decision 3
        result += 4

    if d:          # Decision 4
        result += 8

    if e:          # Decision 5
        result += 16

    return result

# Number of paths = 2^5 = 32 paths!
# Need 32 tests for 100% path coverage
```

### Loop Multiplies Paths

```python
def process_list(items):
    total = 0
    for item in items:     # Loop creates many paths
        if item > 0:       # Decision inside loop
            total += item
        else:
            total -= item
    return total

# For list of 3 items: 2^3 = 8 paths
# For list of 10 items: 2^10 = 1024 paths!
# For list of 20 items: 2^20 = 1,048,576 paths!!
```

### Realistic Example

```python
def validate_registration(user):
    # 10 validation checks
    if not user.email:           # Decision 1
        return False
    if not user.password:        # Decision 2
        return False
    if len(user.password) < 8:   # Decision 3
        return False
    if not user.age:             # Decision 4
        return False
    if user.age < 13:            # Decision 5
        return False
    if not user.country:         # Decision 6
        return False
    if not user.agreed_to_terms: # Decision 7
        return False
    if user.email in banned_list: # Decision 8
        return False
    if not validate_email(user.email):  # Decision 9
        return False
    if profanity_check(user.username):  # Decision 10
        return False
    return True

# Cyclomatic complexity: 10 + 1 = 11
# But potential paths with all combinations: 2^10 = 1,024!
```

---

## When to Use Path Coverage

### ✅ Use Path Coverage When:

1. **Functions are small and simple** (cyclomatic complexity < 10)
2. **Safety-critical code** (medical devices, aerospace)
3. **Security-critical code** (authentication, encryption)
4. **Financial calculations** (payments, tax calculations)

### ❌ Don't Use Path Coverage When:

1. **Functions are complex** (cyclomatic complexity > 10)
2. **Contains loops** (path explosion)
3. **Many independent conditions** (exponential paths)
4. **UI/presentation logic** (low risk)

### Alternative: Basis Path Testing

Instead of testing **all paths**, test **independent paths** (cyclomatic complexity).

**Benefit**: Linear growth (complexity 10 = 10 tests) instead of exponential (2^10 = 1024 tests)

---

## Complete Example: Python

### Code to Test

```python
# insurance_calculator.py
class InsuranceCalculator:
    def calculate_premium(self, age, smoker, pre_existing, coverage_amount):
        """Calculate insurance premium"""

        # Base rate
        if coverage_amount <= 0:
            raise ValueError("Coverage must be positive")

        base_rate = coverage_amount * 0.01

        # Age adjustment
        if age < 18:
            raise ValueError("Must be 18 or older")
        elif age < 30:
            multiplier = 1.0
        elif age < 50:
            multiplier = 1.5
        else:
            multiplier = 2.0

        premium = base_rate * multiplier

        # Risk factors
        if smoker:
            premium = premium * 1.5

        if pre_existing:
            premium = premium * 1.3

        return round(premium, 2)
```

### Calculate Cyclomatic Complexity

**Decisions**:

1. `coverage_amount <= 0`
2. `age < 18`
3. `age < 30`
4. `age < 50`
5. `smoker`
6. `pre_existing`

**Cyclomatic Complexity**: 6 + 1 = **7**

Need **7 tests** for basis path coverage.

### Tests Using Basis Path Testing

```python
# test_insurance_calculator.py
import pytest

class TestInsuranceCalculator:
    def setup_method(self):
        self.calc = InsuranceCalculator()

    def test_invalid_coverage(self):
        """Path 1: coverage_amount <= 0"""
        with pytest.raises(ValueError, match="Coverage must be positive"):
            self.calc.calculate_premium(25, False, False, 0)

    def test_underage(self):
        """Path 2: age < 18"""
        with pytest.raises(ValueError, match="Must be 18 or older"):
            self.calc.calculate_premium(15, False, False, 100000)

    def test_young_non_smoker_no_conditions(self):
        """Path 3: age 18-29, no risk factors (baseline)"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 1.0
        # premium = 1000
        result = self.calc.calculate_premium(25, False, False, 100000)
        assert result == 1000.0

    def test_middle_age_range(self):
        """Path 4: age 30-49"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 1.5
        # premium = 1500
        result = self.calc.calculate_premium(40, False, False, 100000)
        assert result == 1500.0

    def test_senior_age_range(self):
        """Path 5: age 50+"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 2.0
        # premium = 2000
        result = self.calc.calculate_premium(60, False, False, 100000)
        assert result == 2000.0

    def test_smoker_surcharge(self):
        """Path 6: smoker = True"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 1.0
        # smoker = 1.5
        # premium = 1500
        result = self.calc.calculate_premium(25, True, False, 100000)
        assert result == 1500.0

    def test_pre_existing_condition(self):
        """Path 7: pre_existing = True"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 1.0
        # pre_existing = 1.3
        # premium = 1300
        result = self.calc.calculate_premium(25, False, True, 100000)
        assert result == 1300.0

    # Optional: Test combination of risk factors
    def test_all_risk_factors(self):
        """Combination: age 60+, smoker, pre-existing"""
        # base = 100000 * 0.01 = 1000
        # multiplier = 2.0 (age)
        # smoker = 1.5
        # pre_existing = 1.3
        # premium = 1000 * 2.0 * 1.5 * 1.3 = 3900
        result = self.calc.calculate_premium(60, True, True, 100000)
        assert result == 3900.0
```

---

## Complete Example: JavaScript

### Code to Test

```javascript
// shippingCalculator.js
class ShippingCalculator {
  calculateCost(weight, distance, priority, insurance) {
    // Validate inputs
    if (weight <= 0) {
      throw new Error("Weight must be positive");
    }

    if (distance <= 0) {
      throw new Error("Distance must be positive");
    }

    // Base cost
    let cost = weight * 2;

    // Distance zones
    if (distance < 100) {
      cost = cost * 1.0;
    } else if (distance < 500) {
      cost = cost * 1.5;
    } else {
      cost = cost * 2.0;
    }

    // Priority shipping
    if (priority) {
      cost = cost + 20;
    }

    // Insurance
    if (insurance) {
      cost = cost + 10;
    }

    return Math.round(cost * 100) / 100;
  }
}

module.exports = ShippingCalculator;
```

### Calculate Cyclomatic Complexity

**Decisions**:

1. `weight <= 0`
2. `distance <= 0`
3. `distance < 100`
4. `distance < 500`
5. `priority`
6. `insurance`

**Cyclomatic Complexity**: 6 + 1 = **7**

### Tests Using Basis Path Testing

```javascript
// shippingCalculator.test.js
const ShippingCalculator = require("./shippingCalculator");

describe("ShippingCalculator", () => {
  let calculator;

  beforeEach(() => {
    calculator = new ShippingCalculator();
  });

  test("throws error for invalid weight", () => {
    expect(() => {
      calculator.calculateCost(0, 100, false, false);
    }).toThrow("Weight must be positive");
  });

  test("throws error for invalid distance", () => {
    expect(() => {
      calculator.calculateCost(10, 0, false, false);
    }).toThrow("Distance must be positive");
  });

  test("calculates cost for short distance, no extras (baseline)", () => {
    // weight=10, distance=50 (<100), no priority, no insurance
    // cost = 10 * 2 * 1.0 = 20
    const cost = calculator.calculateCost(10, 50, false, false);
    expect(cost).toBe(20);
  });

  test("calculates cost for medium distance", () => {
    // weight=10, distance=300 (100-500), no extras
    // cost = 10 * 2 * 1.5 = 30
    const cost = calculator.calculateCost(10, 300, false, false);
    expect(cost).toBe(30);
  });

  test("calculates cost for long distance", () => {
    // weight=10, distance=600 (>500), no extras
    // cost = 10 * 2 * 2.0 = 40
    const cost = calculator.calculateCost(10, 600, false, false);
    expect(cost).toBe(40);
  });

  test("adds priority shipping fee", () => {
    // weight=10, distance=50, priority=true, no insurance
    // cost = 10 * 2 * 1.0 + 20 = 40
    const cost = calculator.calculateCost(10, 50, true, false);
    expect(cost).toBe(40);
  });

  test("adds insurance fee", () => {
    // weight=10, distance=50, no priority, insurance=true
    // cost = 10 * 2 * 1.0 + 10 = 30
    const cost = calculator.calculateCost(10, 50, false, true);
    expect(cost).toBe(30);
  });

  // Optional: Test combination
  test("calculates cost with all options", () => {
    // weight=10, distance=600, priority, insurance
    // cost = 10 * 2 * 2.0 + 20 + 10 = 70
    const cost = calculator.calculateCost(10, 600, true, true);
    expect(cost).toBe(70);
  });
});
```

---

## Reducing Complexity

### Problem: High Cyclomatic Complexity

```python
def process_transaction(amount, user, payment_method, promo_code):
    # Complexity = 8
    if amount <= 0:
        raise ValueError("Invalid amount")

    if not user.is_active:
        raise ValueError("User inactive")

    if user.balance < amount:
        raise ValueError("Insufficient funds")

    if payment_method == "credit_card":
        if not user.has_credit_card:
            raise ValueError("No credit card")
        charge_credit_card(user, amount)
    elif payment_method == "paypal":
        if not user.has_paypal:
            raise ValueError("No PayPal")
        charge_paypal(user, amount)
    elif payment_method == "bank":
        charge_bank(user, amount)
    else:
        raise ValueError("Invalid payment method")

    if promo_code:
        apply_discount(user, promo_code)

    return True
```

### Solution: Refactor into Smaller Functions

```python
def process_transaction(amount, user, payment_method, promo_code):
    # Complexity = 3
    validate_transaction(amount, user)
    charge_payment(user, amount, payment_method)

    if promo_code:
        apply_discount(user, promo_code)

    return True

def validate_transaction(amount, user):
    # Complexity = 3
    if amount <= 0:
        raise ValueError("Invalid amount")

    if not user.is_active:
        raise ValueError("User inactive")

    if user.balance < amount:
        raise ValueError("Insufficient funds")

def charge_payment(user, amount, payment_method):
    # Complexity = 3
    if payment_method == "credit_card":
        charge_credit_card(user, amount)
    elif payment_method == "paypal":
        charge_paypal(user, amount)
    elif payment_method == "bank":
        charge_bank(user, amount)
    else:
        raise ValueError("Invalid payment method")
```

**Benefits**:

- Lower complexity per function
- Easier to test
- More maintainable
- Better separation of concerns

---

## Complexity Guidelines

### Cyclomatic Complexity Thresholds

| Complexity | Risk      | Recommendation                            |
| ---------- | --------- | ----------------------------------------- |
| 1-5        | Low       | Simple function, easy to test             |
| 6-10       | Medium    | Moderate complexity, acceptable           |
| 11-20      | High      | Consider refactoring                      |
| 21+        | Very High | Refactor! Too complex to test effectively |

### Example: Too Complex

```python
def calculate_tax(income, state, filing_status, dependents,
                  deductions, credits, age, disability):
    # Cyclomatic complexity = 25+
    # TOO COMPLEX!
    if state == "CA":
        if filing_status == "single":
            if income < 50000:
                # ... many more conditions
                pass
    # ... 100+ more lines
```

**Fix**: Break into smaller functions with clear responsibilities.

---

## Common Mistakes

### 1. Trying to Test All Paths in Complex Code

❌ **Bad**: Attempting 2^20 tests

```python
# 20 independent conditions = 1,048,576 paths!
def complex_validation(data):
    if check1(data):
        pass
    if check2(data):
        pass
    # ... 18 more conditions
```

✅ **Good**: Refactor or use basis path testing (20 tests, not 1M)

### 2. Ignoring Unreachable Paths

```python
def example(x):
    if x > 10:
        return "big"
    if x > 5:        # When x > 10, this is never reached
        return "medium"
    return "small"

# Unreachable path: x > 10 AND x > 5 (already returned)
```

**Fix**: Simplify logic to remove unreachable paths.

### 3. Confusing Branch Coverage with Path Coverage

- **Branch coverage**: Test each decision outcome
- **Path coverage**: Test each unique path through code

They are NOT the same!

---

## Summary

**Path Coverage**:

- Tests every unique execution path
- Formula: Based on cyclomatic complexity
- Strongest form of coverage but often impractical

**Cyclomatic Complexity**:

- Measures number of independent paths
- Formula: Number of decisions + 1
- Aim for < 10 per function

**Basis Path Testing**:

- Practical alternative to full path coverage
- Test one path for each unit of complexity
- Linear growth instead of exponential

**When to Use**:

- ✅ Small, critical functions
- ✅ Safety/security-critical code
- ❌ Complex functions (refactor instead)
- ❌ Functions with loops

**Best Practices**:

1. Keep functions simple (complexity < 10)
2. Use basis path testing for complex code
3. Refactor high-complexity functions
4. Combine with branch/statement coverage

---

## Practice Exercises

1. **Calculate Cyclomatic Complexity**: What is the cyclomatic complexity? How many tests needed for basis path coverage?

```python
def process_order(order, inventory, user):
    if not order.items:
        return False

    if not user.is_authenticated:
        return False

    for item in order.items:
        if not inventory.has_stock(item):
            return False

        if item.price > user.credit_limit:
            return False

    if order.total > 10000 and not user.verified:
        return False

    return True
```

2. **Identify Independent Paths**: List all independent paths through this function:

```python
def calculate_grade(score, extra_credit, late_penalty):
    if score < 0:
        return "Invalid"

    final_score = score

    if extra_credit > 0:
        final_score += extra_credit

    if late_penalty:
        final_score -= 10

    if final_score >= 90:
        return "A"
    elif final_score >= 80:
        return "B"
    else:
        return "C"
```

3. **Refactor High Complexity**: This function has complexity 12. Refactor it into smaller functions with lower complexity:

```python
def validate_user_registration(form_data):
    if not form_data.get("email"):
        return False, "Email required"
    if "@" not in form_data["email"]:
        return False, "Invalid email"
    if not form_data.get("password"):
        return False, "Password required"
    if len(form_data["password"]) < 8:
        return False, "Password too short"
    if not form_data.get("age"):
        return False, "Age required"
    if form_data["age"] < 13:
        return False, "Too young"
    if not form_data.get("country"):
        return False, "Country required"
    if form_data["country"] not in ALLOWED_COUNTRIES:
        return False, "Country not supported"
    if not form_data.get("agreed_to_terms"):
        return False, "Must agree to terms"
    if profanity_check(form_data.get("username", "")):
        return False, "Inappropriate username"
    return True, "Valid"
```

---

## Next Steps

- Read [05-coverage-tools.md](./05-coverage-tools.md) to learn about measuring coverage with tools
- Practice with [Exercise 4: Path Coverage](../exercises/04-path-coverage.md)
- Review cyclomatic complexity in your own code
