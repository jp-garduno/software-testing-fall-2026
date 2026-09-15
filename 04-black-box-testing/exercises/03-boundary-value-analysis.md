# Exercise 3: Boundary Value Analysis

**Module**: 4 - Black Box Testing  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice identifying and testing boundary values to find edge case defects.

By completing this exercise, you will:

- Identify boundaries for numeric, string, and date inputs
- Apply BVA systematically (min, min+1, nominal, max-1, max)
- Combine BVA with Equivalence Partitioning
- Calculate boundary coverage

---

## Instructions

For each scenario:

1. **Identify all boundaries** for each input
2. **Document boundary values** in a table
3. **Create test cases** for boundary values
4. **Implement tests** in Python or JavaScript
5. **Combine with EP** for comprehensive coverage

### Boundary Value Template

For a range [min, max], test:

- **Below min**: min - 1
- **At min**: min
- **Just above min**: min + 1
- **Nominal**: middle value
- **Just below max**: max - 1
- **At max**: max
- **Above max**: max + 1

---

## Scenario 1: Loan Eligibility Calculator

### Requirements

A loan eligibility system checks:

- **Annual Income**: $20,000 - $500,000
  - < $30,000: Not eligible
  - $30,000 - $75,000: Standard rate (6.5%)
  - $75,001 - $150,000: Reduced rate (5.5%)
  - $150,001+: Premium rate (4.5%)
- **Credit Score**: 300 - 850
  - < 580: Rejected
  - 580 - 669: High risk (8% rate)
  - 670 - 739: Good (6% rate)
  - 740+: Excellent (4% rate)
- **Loan Amount**: $5,000 - $1,000,000
- **Loan Term**: 1 - 30 years

**Business Rules**:

- Loan amount cannot exceed 5x annual income
- Credit score < 580: Automatic rejection
- Debt-to-income ratio calculated based on term

### Part A: Identify Boundaries

Complete this table for **Annual Income**:

| Boundary Type                | Value    | Expected Category | Expected Rate |
| ---------------------------- | -------- | ----------------- | ------------- |
| Below minimum                | $19,999  | Invalid           | Error         |
| At minimum                   | $20,000  | Not eligible      | -             |
| Just above minimum           | $20,001  | Not eligible      | -             |
| Below first threshold        | $29,999  | Not eligible      | -             |
| At first threshold           | $30,000  | Standard          | 6.5%          |
| Just above first threshold   | $30,001  | Standard          | 6.5%          |
| Below second threshold       | $75,000  | Standard          | 6.5%          |
| At second threshold boundary | $75,001  | Reduced           | 5.5%          |
| Just above second threshold  | $75,002  | Reduced           | 5.5%          |
| Below third threshold        | $150,000 | Reduced           | 5.5%          |
| At third threshold boundary  | $150,001 | Premium           | 4.5%          |
| Just above third threshold   | $150,002 | Premium           | 4.5%          |
| Just below maximum           | $499,999 | Premium           | 4.5%          |
| At maximum                   | $500,000 | Premium           | 4.5%          |
| Above maximum                | $500,001 | Invalid           | Error         |

**Your turn**: Create similar tables for:

1. **Credit Score** boundaries
2. **Loan Amount** boundaries
3. **Loan Term** boundaries

### Part B: Combine BVA + EP

| Test Case ID | Income (BVA)             | Credit Score (BVA) | Loan Amount | Expected Result           |
| ------------ | ------------------------ | ------------------ | ----------- | ------------------------- |
| TC_LOAN_001  | $30,000 (boundary)       | 580 (boundary)     | $50,000     | Approved - High risk, 8%  |
| TC_LOAN_002  | $29,999 (below boundary) | 700                | $50,000     | Rejected - Income too low |
| TC_LOAN_003  | $75,001 (boundary)       | 740 (boundary)     | $100,000    | Approved - Excellent, 4%  |
| ...          | ...                      | ...                | ...         | ...                       |

**Create at least 15 test cases** combining boundary values from different inputs.

### Part C: Implementation

**Python**:

```python
class LoanEligibility:
    def __init__(self, income, credit_score, loan_amount, loan_term):
        self.income = income
        self.credit_score = credit_score
        self.loan_amount = loan_amount
        self.loan_term = loan_term

    def validate_inputs(self):
        """Validate all inputs are within acceptable ranges."""
        errors = []

        if not (20000 <= self.income <= 500000):
            errors.append("Income must be between $20,000 and $500,000")

        if not (300 <= self.credit_score <= 850):
            errors.append("Credit score must be between 300 and 850")

        if not (5000 <= self.loan_amount <= 1000000):
            errors.append("Loan amount must be between $5,000 and $1,000,000")

        if not (1 <= self.loan_term <= 30):
            errors.append("Loan term must be between 1 and 30 years")

        return len(errors) == 0, errors

    def calculate_eligibility(self):
        """
        Calculate loan eligibility and rate.
        Returns: (eligible: bool, rate: float, category: str, message: str)
        """
        # TODO: Implement eligibility logic
        pass


def test_income_at_minimum():
    """BVA: Income at minimum boundary ($20,000)"""
    loan = LoanEligibility(income=20000, credit_score=650, loan_amount=50000, loan_term=15)
    valid, errors = loan.validate_inputs()
    assert valid == True
    eligible, rate, category, msg = loan.calculate_eligibility()
    assert eligible == False  # Below $30,000 threshold

def test_income_below_minimum():
    """BVA: Income below minimum boundary ($19,999)"""
    loan = LoanEligibility(income=19999, credit_score=650, loan_amount=50000, loan_term=15)
    valid, errors = loan.validate_inputs()
    assert valid == False
    assert "Income must be between" in errors[0]

def test_income_at_first_threshold():
    """BVA: Income at first threshold ($30,000)"""
    loan = LoanEligibility(income=30000, credit_score=650, loan_amount=50000, loan_term=15)
    valid, errors = loan.validate_inputs()
    assert valid == True
    eligible, rate, category, msg = loan.calculate_eligibility()
    assert eligible == True
    assert rate == 6.5
    assert category == "Standard"

def test_credit_score_at_rejection_boundary():
    """BVA: Credit score at rejection boundary (580)"""
    loan = LoanEligibility(income=50000, credit_score=580, loan_amount=50000, loan_term=15)
    valid, errors = loan.validate_inputs()
    assert valid == True
    eligible, rate, category, msg = loan.calculate_eligibility()
    assert eligible == True  # 580 is accepted
    assert rate == 8.0

def test_credit_score_below_rejection():
    """BVA: Credit score below rejection (579)"""
    loan = LoanEligibility(income=50000, credit_score=579, loan_amount=50000, loan_term=15)
    eligible, rate, category, msg = loan.calculate_eligibility()
    assert eligible == False
    assert "credit score" in msg.lower()

def test_loan_amount_exceeds_5x_income():
    """Business rule: Loan amount > 5x income"""
    loan = LoanEligibility(income=50000, credit_score=700, loan_amount=250001, loan_term=15)
    eligible, rate, category, msg = loan.calculate_eligibility()
    assert eligible == False
    assert "5 times" in msg or "income" in msg.lower()

# TODO: Add tests for all boundary values identified in Part A
```

**JavaScript**:

```javascript
class LoanEligibility {
  constructor(income, creditScore, loanAmount, loanTerm) {
    this.income = income;
    this.creditScore = creditScore;
    this.loanAmount = loanAmount;
    this.loanTerm = loanTerm;
  }

  validateInputs() {
    const errors = [];

    if (this.income < 20000 || this.income > 500000) {
      errors.push("Income must be between $20,000 and $500,000");
    }

    if (this.creditScore < 300 || this.creditScore > 850) {
      errors.push("Credit score must be between 300 and 850");
    }

    if (this.loanAmount < 5000 || this.loanAmount > 1000000) {
      errors.push("Loan amount must be between $5,000 and $1,000,000");
    }

    if (this.loanTerm < 1 || this.loanTerm > 30) {
      errors.push("Loan term must be between 1 and 30 years");
    }

    return { valid: errors.length === 0, errors };
  }

  calculateEligibility() {
    // TODO: Implement eligibility logic
    // Returns: { eligible: boolean, rate: number, category: string, message: string }
  }
}

describe("Loan Eligibility - Boundary Value Analysis", () => {
  test("BVA: Income at minimum boundary ($20,000)", () => {
    const loan = new LoanEligibility(20000, 650, 50000, 15);
    const { valid } = loan.validateInputs();
    expect(valid).toBe(true);

    const result = loan.calculateEligibility();
    expect(result.eligible).toBe(false); // Below $30,000 threshold
  });

  test("BVA: Income below minimum boundary ($19,999)", () => {
    const loan = new LoanEligibility(19999, 650, 50000, 15);
    const { valid, errors } = loan.validateInputs();
    expect(valid).toBe(false);
    expect(errors[0]).toContain("Income must be between");
  });

  test("BVA: Income at first threshold ($30,000)", () => {
    const loan = new LoanEligibility(30000, 650, 50000, 15);
    const result = loan.calculateEligibility();
    expect(result.eligible).toBe(true);
    expect(result.rate).toBe(6.5);
    expect(result.category).toBe("Standard");
  });

  test("BVA: Credit score at rejection boundary (580)", () => {
    const loan = new LoanEligibility(50000, 580, 50000, 15);
    const result = loan.calculateEligibility();
    expect(result.eligible).toBe(true);
    expect(result.rate).toBe(8.0);
  });

  test("BVA: Credit score below rejection (579)", () => {
    const loan = new LoanEligibility(50000, 579, 50000, 15);
    const result = loan.calculateEligibility();
    expect(result.eligible).toBe(false);
    expect(result.message.toLowerCase()).toContain("credit score");
  });

  // TODO: Add tests for all boundary values
});
```

---

## Scenario 2: E-commerce Product Categorization

### Requirements

An e-commerce system categorizes products and applies discounts:

**Price Ranges**:

- $0.01 - $10.00: Budget
- $10.01 - $50.00: Standard
- $50.01 - $200.00: Premium
- $200.01+: Luxury

**Discounts by Category**:

- Budget: 5% if quantity >= 10
- Standard: 10% if quantity >= 5
- Premium: 15% if quantity >= 3
- Luxury: 20% if quantity >= 2

**Quantity Limits**:

- Budget items: 1-100 per order
- Standard items: 1-50 per order
- Premium items: 1-20 per order
- Luxury items: 1-10 per order

**String Length Boundaries**:

- Product name: 3-100 characters
- Product description: 10-500 characters
- SKU: Exactly 8 characters (alphanumeric)

### Part A: Create Boundary Tables

Create boundary tables for:

1. **Price ranges** (for each category boundary)
2. **Quantity** (for each category limit)
3. **String lengths** (name, description, SKU)

Example for Price:

| Boundary                  | Value  | Expected Category |
| ------------------------- | ------ | ----------------- |
| Below minimum             | $0.00  | Invalid           |
| At minimum                | $0.01  | Budget            |
| Just below first boundary | $10.00 | Budget            |
| At first boundary         | $10.01 | Standard          |
| Just above first boundary | $10.02 | Standard          |
| ...                       | ...    | ...               |

### Part B: Implementation

```python
class Product:
    def __init__(self, name, description, sku, price, quantity):
        self.name = name
        self.description = description
        self.sku = sku
        self.price = price
        self.quantity = quantity

    def validate(self):
        """Validate product data."""
        # TODO: Implement validation
        pass

    def get_category(self):
        """Determine product category based on price."""
        # TODO: Implement
        pass

    def calculate_discount(self):
        """Calculate discount based on category and quantity."""
        # TODO: Implement
        pass

    def calculate_total(self):
        """Calculate total price after discount."""
        # TODO: Implement
        pass


def test_price_at_budget_boundary():
    """BVA: Price at budget upper boundary ($10.00)"""
    product = Product("Widget", "A nice widget", "WDG12345", 10.00, 1)
    assert product.get_category() == "Budget"

def test_price_at_standard_boundary():
    """BVA: Price at standard lower boundary ($10.01)"""
    product = Product("Widget", "A nice widget", "WDG12345", 10.01, 1)
    assert product.get_category() == "Standard"

def test_quantity_for_bulk_discount_budget():
    """BVA: Budget item at discount threshold (10 items)"""
    product = Product("Widget", "A nice widget", "WDG12345", 5.00, 10)
    discount = product.calculate_discount()
    assert discount == 0.05  # 5%

def test_quantity_below_bulk_discount_budget():
    """BVA: Budget item below discount threshold (9 items)"""
    product = Product("Widget", "A nice widget", "WDG12345", 5.00, 9)
    discount = product.calculate_discount()
    assert discount == 0.0  # No discount

def test_name_at_minimum_length():
    """BVA: Product name at minimum length (3 characters)"""
    product = Product("ABC", "A nice widget", "WDG12345", 5.00, 1)
    valid, errors = product.validate()
    assert valid == True

def test_name_below_minimum_length():
    """BVA: Product name below minimum (2 characters)"""
    product = Product("AB", "A nice widget", "WDG12345", 5.00, 1)
    valid, errors = product.validate()
    assert valid == False
    assert any("name" in e.lower() for e in errors)

# TODO: Complete all boundary tests
```

---

## Scenario 3: Shipping Cost Calculator

### Requirements

Shipping cost calculator based on:

**Weight Ranges** (in pounds):

- 0.1 - 1.0 lbs: $5.00
- 1.1 - 5.0 lbs: $10.00
- 5.1 - 20.0 lbs: $20.00
- 20.1 - 50.0 lbs: $40.00
- 50.1 - 100.0 lbs: $75.00
- Over 100 lbs: $75.00 + $1.00 per lb over 100

**Dimensions** (L x W x H in inches):

- Sum of dimensions <= 62: Standard
- Sum 63-108: Oversized (+$20)
- Sum > 108: Not shippable

**Shipping Zones**:

- Zone 1 (local): Base rate
- Zone 2 (regional): Base rate × 1.5
- Zone 3 (national): Base rate × 2.0
- Zone 4 (remote): Base rate × 3.0

**Precision Requirements**:

- Weight: 1 decimal place (e.g., 5.1, 5.2)
- Dimensions: Whole numbers only

### Part A: Identify Boundaries

Create tables for:

1. Weight boundaries (including precision)
2. Dimension sum boundaries
3. Combination tests (weight + dimensions + zone)

### Part B: Implementation

```python
def calculate_shipping(weight, length, width, height, zone):
    """
    Calculate shipping cost.
    Returns: (cost: float, category: str, errors: list)
    """
    # TODO: Implement
    pass


def test_weight_at_first_boundary():
    """BVA: Weight at 1.0 lb boundary"""
    cost, category, errors = calculate_shipping(1.0, 10, 10, 10, 1)
    assert cost == 5.00
    assert len(errors) == 0

def test_weight_just_above_first_boundary():
    """BVA: Weight at 1.1 lb boundary"""
    cost, category, errors = calculate_shipping(1.1, 10, 10, 10, 1)
    assert cost == 10.00

def test_dimensions_at_standard_limit():
    """BVA: Dimensions sum exactly 62"""
    cost, category, errors = calculate_shipping(5.0, 20, 20, 22, 1)
    # 20 + 20 + 22 = 62
    assert "Oversized" not in category
    assert cost == 10.00  # 5 lbs in zone 1

def test_dimensions_at_oversized_boundary():
    """BVA: Dimensions sum exactly 63"""
    cost, category, errors = calculate_shipping(5.0, 21, 21, 21, 1)
    # 21 + 21 + 21 = 63
    assert "Oversized" in category
    assert cost == 30.00  # 10 + 20 oversized fee

def test_weight_over_100_lbs():
    """BVA: Weight at 101 lbs (over 100 boundary)"""
    cost, category, errors = calculate_shipping(101.0, 20, 20, 20, 1)
    assert cost == 76.00  # 75 + 1

def test_weight_precision():
    """BVA: Weight with 2 decimal places (should round)"""
    cost, category, errors = calculate_shipping(1.15, 10, 10, 10, 1)
    # Should round to 1.2 or handle precision
    assert len(errors) == 0

# TODO: Complete all boundary tests
```

---

## Scenario 4: Temperature Control System

### Requirements

Smart thermostat with precise temperature control:

**Temperature Ranges** (Fahrenheit):

- Minimum settable: 50.0°F
- Maximum settable: 90.0°F
- Precision: 0.5°F increments only (50.0, 50.5, 51.0, etc.)
- Danger zones:
  - < 40°F: Freeze warning
  - > 95°F: Overheat warning

**Operating Modes**:

- Heat: Activates when temp < (setpoint - 2.0°F)
- Cool: Activates when temp > (setpoint + 2.0°F)
- Off: When within ± 2.0°F of setpoint

**Time Ranges**:

- Schedule slots: 0-1440 minutes (24 hours)
- Duration: Must be 15-minute increments

### Part A: Boundary Analysis

Create tables for:

1. Temperature setpoints (with precision requirements)
2. Hysteresis boundaries (setpoint ± 2.0)
3. Time slot boundaries

### Part B: Implementation

```javascript
class Thermostat {
  constructor(currentTemp, setpoint) {
    this.currentTemp = currentTemp;
    this.setpoint = setpoint;
  }

  validateSetpoint() {
    // TODO: Validate setpoint is in range and correct precision
  }

  determineMode() {
    // TODO: Return 'heat', 'cool', or 'off' based on hysteresis
  }

  checkWarnings() {
    // TODO: Check for freeze/overheat warnings
  }
}

describe("Thermostat - Boundary Value Analysis", () => {
  test("BVA: Setpoint at minimum (50.0°F)", () => {
    const thermostat = new Thermostat(55.0, 50.0);
    const { valid } = thermostat.validateSetpoint();
    expect(valid).toBe(true);
  });

  test("BVA: Setpoint below minimum (49.5°F)", () => {
    const thermostat = new Thermostat(55.0, 49.5);
    const { valid, error } = thermostat.validateSetpoint();
    expect(valid).toBe(false);
    expect(error).toContain("minimum");
  });

  test("BVA: Invalid precision (50.3°F)", () => {
    const thermostat = new Thermostat(55.0, 50.3);
    const { valid, error } = thermostat.validateSetpoint();
    expect(valid).toBe(false);
    expect(error).toContain("0.5");
  });

  test("BVA: Heat activation boundary (setpoint - 2.0)", () => {
    const thermostat = new Thermostat(68.0, 70.0);
    const mode = thermostat.determineMode();
    expect(mode).toBe("heat");
  });

  test("BVA: Within hysteresis range (setpoint - 1.9)", () => {
    const thermostat = new Thermostat(68.1, 70.0);
    const mode = thermostat.determineMode();
    expect(mode).toBe("off");
  });

  test("BVA: Freeze warning at boundary (40.0°F)", () => {
    const thermostat = new Thermostat(40.0, 70.0);
    const warnings = thermostat.checkWarnings();
    expect(warnings).toContain("freeze");
  });

  // TODO: Complete all boundary tests
});
```

---

## Scenario 5: Game Level System

### Requirements

RPG game level progression system:

**XP Requirements per Level**:

- Level 1: 0 XP
- Level 2: 100 XP
- Level 3: 250 XP
- Level 4: 500 XP
- Level 5: 1000 XP
- Level 6: 2000 XP
- Level 7: 4000 XP
- Level 8: 8000 XP
- Level 9: 15000 XP
- Level 10: 30000 XP (max level)

**Feature Unlocks**:

- Level 3: Special attack
- Level 5: Mount
- Level 7: Guild access
- Level 10: Legendary items

**XP Constraints**:

- Single XP gain: 1 - 10,000 XP
- Total XP: 0 - 30,000 (max)
- Cannot lose XP (negative gains invalid)

### Part A: Boundary Analysis

Identify boundaries for:

1. Each level threshold (XP needed to level up)
2. Feature unlock thresholds
3. Single XP gain limits

Example:

| Level Transition | XP Below | XP At Boundary | XP Above | Expected Level |
| ---------------- | -------- | -------------- | -------- | -------------- |
| 1 → 2            | 99       | 100            | 101      | 1, 2, 2        |
| 2 → 3            | 249      | 250            | 251      | 2, 3, 3        |
| ...              | ...      | ...            | ...      | ...            |

### Part B: Implementation

```python
class Player:
    def __init__(self, name):
        self.name = name
        self.xp = 0
        self.level = 1
        self.unlocked_features = []

    XP_THRESHOLDS = [0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000]
    FEATURE_UNLOCKS = {
        3: "Special Attack",
        5: "Mount",
        7: "Guild Access",
        10: "Legendary Items"
    }

    def add_xp(self, amount):
        """
        Add XP and check for level up.
        Returns: (success: bool, new_level: int, unlocked: list, message: str)
        """
        # TODO: Implement
        pass

    def get_level_from_xp(self, xp):
        """Determine level based on total XP."""
        # TODO: Implement
        pass


def test_xp_at_level_2_boundary():
    """BVA: Exactly 100 XP (Level 2 threshold)"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(100)
    assert success == True
    assert new_level == 2
    assert player.level == 2

def test_xp_below_level_2_boundary():
    """BVA: 99 XP (just below Level 2)"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(99)
    assert success == True
    assert player.level == 1  # Should not level up

def test_xp_above_level_2_boundary():
    """BVA: 101 XP (just above Level 2)"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(101)
    assert success == True
    assert player.level == 2

def test_feature_unlock_at_level_3():
    """BVA: Exactly 250 XP (Level 3 + Special Attack unlock)"""
    player = Player("Hero")
    player.add_xp(250)
    assert player.level == 3
    assert "Special Attack" in player.unlocked_features

def test_multiple_levels_single_gain():
    """BVA: Large XP gain causing multiple level-ups"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(1000)
    assert player.level == 5
    assert "Special Attack" in player.unlocked_features
    assert "Mount" in player.unlocked_features

def test_xp_at_max_level():
    """BVA: At max level (30,000 XP)"""
    player = Player("Hero")
    player.add_xp(30000)
    assert player.level == 10

    # Try to add more XP
    success, new_level, unlocked, msg = player.add_xp(100)
    assert player.xp == 30000  # Should not exceed max
    assert "maximum" in msg.lower()

def test_single_xp_gain_at_maximum():
    """BVA: Single gain at maximum (10,000 XP)"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(10000)
    assert success == True

def test_single_xp_gain_above_maximum():
    """BVA: Single gain above maximum (10,001 XP)"""
    player = Player("Hero")
    success, new_level, unlocked, msg = player.add_xp(10001)
    assert success == False
    assert "maximum" in msg.lower() or "10000" in msg

# TODO: Complete all boundary tests
```

---

## Deliverables

Submit:

1. **Boundary Tables** for all 5 scenarios showing:

   - Boundary values identified
   - Expected results for each boundary
   - Rationale for boundary selection

2. **Test Case Documentation**:

   - Test case ID
   - Boundary being tested
   - Input values
   - Expected outputs
   - Actual results (after execution)

3. **Implementation**:

   - Working code (Python or JavaScript)
   - All test cases implemented and passing
   - Code coverage report

4. **Analysis Report**:
   - Defects found during testing
   - Boundaries that revealed bugs
   - Comparison of BVA vs EP effectiveness

---

## Evaluation Criteria

| Criteria                    | Points | Description                             |
| --------------------------- | ------ | --------------------------------------- |
| **Boundary Identification** | 25     | All boundaries correctly identified     |
| **Test Case Design**        | 25     | Systematic testing of boundaries        |
| **Implementation**          | 30     | Code works correctly for all boundaries |
| **BVA + EP Integration**    | 10     | Effectively combines both techniques    |
| **Documentation**           | 10     | Clear tables and analysis               |

**Total**: 100 points

---

## Tips for Success

1. **Systematic approach**: Use the template (min-1, min, min+1, nominal, max-1, max, max+1)
2. **Don't skip "just above/below"**: These often reveal off-by-one errors
3. **Test both sides**: Test values on both sides of each boundary
4. **Precision matters**: For floating-point numbers, consider precision boundaries
5. **Combine with EP**: Use EP for partition selection, BVA for boundary values
6. **Document rationale**: Explain why each boundary is significant

---

## Common Mistakes to Avoid

❌ Only testing min and max (skip min+1, max-1)  
✅ Test all 7 values: min-1, min, min+1, nominal, max-1, max, max+1

❌ Assuming boundaries are inclusive on both sides  
✅ Check requirements: is it [min, max] or (min, max) or [min, max)?

❌ Missing internal boundaries (thresholds within valid range)  
✅ Identify all thresholds where behavior changes

❌ Ignoring precision requirements  
✅ Test precision boundaries for floating-point values

❌ Testing boundaries in isolation  
✅ Combine multiple boundary values in single tests

---

## Bonus Challenge

### Multi-dimensional Boundary Testing

For **Scenario 1 (Loan Eligibility)**, create a **boundary coverage matrix**:

| Income | Credit Score | Loan Amount | Expected Result              | Test Priority |
| ------ | ------------ | ----------- | ---------------------------- | ------------- |
| 29,999 | 579          | 5,000       | Rejected (both boundaries)   | High          |
| 30,000 | 580          | 5,001       | Approved (all at boundaries) | Critical      |
| 75,001 | 740          | 200,000     | Rate change boundaries       | High          |
| ...    | ...          | ...         | ...                          | ...           |

Calculate:

1. **Total possible boundary combinations**
2. **Minimum tests for full boundary coverage**
3. **Risk-based prioritization** of boundary tests

---

## Next Steps

After completing this exercise:

1. Review [Theory: Boundary Value Analysis](../theory/03-boundary-value-analysis.md)
2. Compare your boundary tables with peers
3. Move to [Exercise 4: Decision Tables](./04-decision-tables.md)
4. Practice combining BVA + EP for complete coverage

---

**Remember: Most defects lurk at boundaries. Test the edges, not just the middle!** 🎯
