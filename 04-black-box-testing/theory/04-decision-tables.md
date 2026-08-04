# Decision Tables

**Module**: 4 - Black Box Testing  
**Topic**: Testing Complex Business Logic  
**Reading Time**: 28 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand when to use decision tables
- Create decision tables for complex business rules
- Identify conditions, actions, and rules
- Simplify redundant rules
- Combine decision tables with EP and BVA
- Test multi-condition scenarios systematically

---

## What is a Decision Table?

A **decision table** is a tabular method for representing complex business logic where the output depends on multiple conditions.

### The Problem

Some business rules have **multiple conditions** that combine in complex ways:

```
If user is Premium AND age >= 18 AND country is US:
    Allow feature A, B, C
If user is Premium AND age >= 18 AND country is not US:
    Allow feature A, B (not C)
If user is Premium AND age < 18:
    Allow feature A only
...
```

Testing all these combinations is error-prone without a systematic approach.

### The Solution

Decision tables organize conditions, combinations, and expected actions in a clear, testable format.

---

## Why Use Decision Tables?

### 1. Handle Multiple Conditions

When you have 2+ conditions that interact:

- User type AND subscription status
- Age AND location AND time
- Input validation with multiple rules

### 2. Ensure Complete Coverage

Decision tables help you identify:

- All possible combinations
- Missing test cases
- Impossible combinations
- Redundant rules

### 3. Document Complex Logic

Decision tables serve as:

- Test specifications
- Living documentation
- Requirements validation
- Communication tool for stakeholders

---

## Decision Table Structure

### Components

```
┌─────────────────────────────────────────┐
│ Conditions                              │ ← Input factors
├──────────┬──────────┬──────────┬────────┤
│ Rule 1   │ Rule 2   │ Rule 3   │ ...    │ ← Combination of conditions
├──────────┼──────────┼──────────┼────────┤
│ Actions                                 │ ← Expected outcomes
└─────────────────────────────────────────┘
```

### Notation

- **Y** (Yes/True): Condition is true
- **N** (No/False): Condition is false
- **-** (Don't care): Condition doesn't matter
- **X**: Action is executed
- **-**: Action is not executed

---

## Example 1: Simple Login Logic

### Requirement

Login validation with three conditions:

1. Valid username
2. Valid password
3. Account is active

### Decision Table

| Condition                  | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  |
| -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Valid username             | Y   | Y   | Y   | Y   | N   | N   | N   | N   |
| Valid password             | Y   | Y   | N   | N   | Y   | Y   | N   | N   |
| Account active             | Y   | N   | Y   | N   | Y   | N   | Y   | N   |
| **Actions**                |     |     |     |     |     |     |     |     |
| Grant access               | X   | -   | -   | -   | -   | -   | -   | -   |
| Show "Account locked"      | -   | X   | -   | X   | -   | -   | -   | -   |
| Show "Invalid credentials" | -   | -   | X   | -   | X   | X   | X   | X   |

### Analysis

- **8 rules** for 3 binary conditions (2³ = 8)
- Only **Rule 1** grants access (all conditions true)
- Rules 2, 4 show "Account locked" message
- Rules 3, 5, 6, 7, 8 show "Invalid credentials"

### Python Implementation

```python
def login(username, password, account_status):
    """
    Login validation based on decision table.

    Returns: (success: bool, message: str)
    """
    valid_username = username in ["user@example.com", "admin@example.com"]
    valid_password = password == "ValidPass123!"
    account_active = account_status == "active"

    # Rule 1: All conditions true
    if valid_username and valid_password and account_active:
        return True, "Login successful"

    # Rules 2, 4: Valid username but account not active
    if valid_username and not account_active:
        return False, "Account locked"

    # All other rules: Invalid credentials
    return False, "Invalid credentials"


# Test cases based on decision table
def test_login_decision_table():
    """Test all 8 rules from decision table"""

    # Rule 1: Y-Y-Y → Grant access
    success, msg = login("user@example.com", "ValidPass123!", "active")
    assert success == True
    assert msg == "Login successful"

    # Rule 2: Y-Y-N → Account locked
    success, msg = login("user@example.com", "ValidPass123!", "locked")
    assert success == False
    assert msg == "Account locked"

    # Rule 3: Y-N-Y → Invalid credentials
    success, msg = login("user@example.com", "WrongPass", "active")
    assert success == False
    assert msg == "Invalid credentials"

    # Rule 4: Y-N-N → Account locked
    success, msg = login("user@example.com", "WrongPass", "locked")
    assert success == False
    assert msg == "Account locked"

    # Rule 5: N-Y-Y → Invalid credentials
    success, msg = login("hacker@evil.com", "ValidPass123!", "active")
    assert success == False
    assert msg == "Invalid credentials"

    # Rule 6: N-Y-N → Invalid credentials
    success, msg = login("hacker@evil.com", "ValidPass123!", "locked")
    assert success == False
    assert msg == "Invalid credentials"

    # Rule 7: N-N-Y → Invalid credentials
    success, msg = login("hacker@evil.com", "WrongPass", "active")
    assert success == False
    assert msg == "Invalid credentials"

    # Rule 8: N-N-N → Invalid credentials
    success, msg = login("hacker@evil.com", "WrongPass", "locked")
    assert success == False
    assert msg == "Invalid credentials"
```

---

## Example 2: Shipping Cost Calculator

### Requirement

Shipping cost depends on:

1. **Weight**: Light (< 5 kg) or Heavy (>= 5 kg)
2. **Destination**: Domestic or International
3. **Priority**: Standard or Express

### Decision Table

| Condition    | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| Light weight | Y   | Y   | Y   | Y   | N   | N   | N   | N   |
| Domestic     | Y   | Y   | N   | N   | Y   | Y   | N   | N   |
| Express      | Y   | N   | Y   | N   | Y   | N   | Y   | N   |
| **Actions**  |     |     |     |     |     |     |     |     |
| Cost: $10    | X   | -   | -   | -   | -   | -   | -   | -   |
| Cost: $5     | -   | X   | -   | -   | -   | -   | -   | -   |
| Cost: $40    | -   | -   | X   | -   | -   | -   | -   | -   |
| Cost: $25    | -   | -   | -   | X   | -   | -   | -   | -   |
| Cost: $20    | -   | -   | -   | -   | X   | -   | -   | -   |
| Cost: $15    | -   | -   | -   | -   | -   | X   | -   | -   |
| Cost: $60    | -   | -   | -   | -   | -   | -   | X   | -   |
| Cost: $35    | -   | -   | -   | -   | -   | -   | -   | X   |

### JavaScript Implementation

```javascript
/**
 * Calculate shipping cost based on weight, destination, and priority.
 *
 * @param {number} weight - Weight in kg
 * @param {string} destination - "domestic" or "international"
 * @param {string} priority - "standard" or "express"
 * @returns {number} - Shipping cost in dollars
 */
function calculateShipping(weight, destination, priority) {
  const isLight = weight < 5;
  const isDomestic = destination === "domestic";
  const isExpress = priority === "express";

  // Decision table mapping
  if (isLight && isDomestic && isExpress) return 10; // R1
  if (isLight && isDomestic && !isExpress) return 5; // R2
  if (isLight && !isDomestic && isExpress) return 40; // R3
  if (isLight && !isDomestic && !isExpress) return 25; // R4
  if (!isLight && isDomestic && isExpress) return 20; // R5
  if (!isLight && isDomestic && !isExpress) return 15; // R6
  if (!isLight && !isDomestic && isExpress) return 60; // R7
  if (!isLight && !isDomestic && !isExpress) return 35; // R8

  throw new Error("Invalid input combination");
}

// Test cases based on decision table
describe("Shipping Cost Decision Table", () => {
  test("R1: Light, Domestic, Express → $10", () => {
    expect(calculateShipping(3, "domestic", "express")).toBe(10);
  });

  test("R2: Light, Domestic, Standard → $5", () => {
    expect(calculateShipping(3, "domestic", "standard")).toBe(5);
  });

  test("R3: Light, International, Express → $40", () => {
    expect(calculateShipping(3, "international", "express")).toBe(40);
  });

  test("R4: Light, International, Standard → $25", () => {
    expect(calculateShipping(3, "international", "standard")).toBe(25);
  });

  test("R5: Heavy, Domestic, Express → $20", () => {
    expect(calculateShipping(8, "domestic", "express")).toBe(20);
  });

  test("R6: Heavy, Domestic, Standard → $15", () => {
    expect(calculateShipping(8, "domestic", "standard")).toBe(15);
  });

  test("R7: Heavy, International, Express → $60", () => {
    expect(calculateShipping(8, "international", "express")).toBe(60);
  });

  test("R8: Heavy, International, Standard → $35", () => {
    expect(calculateShipping(8, "international", "standard")).toBe(35);
  });
});
```

---

## Creating a Decision Table: Step-by-Step

### Step 1: Identify Conditions

List all conditions that affect the outcome.

**Example**: Insurance premium calculation

- Age category: Young (< 25), Adult (25-60), Senior (> 60)
- Driving record: Clean, Minor violations, Major violations
- Coverage type: Basic, Premium

### Step 2: Determine Possible Values

For each condition, list possible values:

- Age: 3 values (Young, Adult, Senior)
- Record: 3 values (Clean, Minor, Major)
- Coverage: 2 values (Basic, Premium)

Total combinations: 3 × 3 × 2 = **18 rules**

### Step 3: Create Initial Table

List all combinations systematically:

| Condition        | R1  | R2  | R3  | R4  | R5  | ... | R18 |
| ---------------- | --- | --- | --- | --- | --- | --- | --- |
| Young            | Y   | Y   | Y   | Y   | Y   | Y   | N   |
| Adult            | N   | N   | N   | N   | N   | N   | Y   |
| Senior           | N   | N   | N   | N   | N   | N   | N   |
| Clean record     | Y   | Y   | N   | N   | N   | N   | Y   |
| Minor violations | N   | N   | Y   | Y   | N   | N   | N   |
| Major violations | N   | N   | N   | N   | Y   | Y   | N   |
| Basic coverage   | Y   | N   | Y   | N   | Y   | N   | Y   |
| Premium coverage | N   | Y   | N   | Y   | N   | Y   | N   |

### Step 4: Define Actions

Specify what happens for each rule:

- Calculate premium amount
- Reject application
- Require additional review

### Step 5: Simplify (Optional)

Look for opportunities to combine rules (covered in next section).

---

## Simplified Decision Tables

### The Problem with Complete Tables

For **n conditions** with **2 values each**: 2ⁿ rules

- 3 conditions: 8 rules
- 4 conditions: 16 rules
- 5 conditions: 32 rules
- 10 conditions: 1,024 rules!

### Using "Don't Care" Values

If a condition doesn't affect the outcome, mark it with **"-"** (don't care).

### Example: Discount Eligibility

**Requirement**:

- Student discount applies if user is a student (other conditions don't matter)
- Senior discount applies if user is senior (other conditions don't matter)
- No discount otherwise

**Complete Table** (unnecessary):

| Condition        | R1  | R2  | R3  | R4  |
| ---------------- | --- | --- | --- | --- |
| Is student       | Y   | Y   | N   | N   |
| Is senior        | Y   | N   | Y   | N   |
| **Action**       |     |     |     |     |
| Student discount | X   | X   | -   | -   |
| Senior discount  | -   | -   | X   | -   |
| No discount      | -   | -   | -   | X   |

**Simplified Table** (better):

| Condition        | R1  | R2  | R3  |
| ---------------- | --- | --- | --- |
| Is student       | Y   | N   | N   |
| Is senior        | -   | Y   | N   |
| **Action**       |     |     |     |
| Student discount | X   | -   | -   |
| Senior discount  | -   | X   | -   |
| No discount      | -   | -   | X   |

**Note**: R1 doesn't check "Is senior" because student status alone determines the discount.

```python
def calculate_discount(is_student, is_senior):
    """
    Apply discount based on simplified decision table.
    Student discount has priority.
    """
    # R1: Student (senior status doesn't matter)
    if is_student:
        return "Student discount: 20%"

    # R2: Senior (not student)
    if is_senior:
        return "Senior discount: 15%"

    # R3: No discount
    return "No discount"

def test_discount_simplified():
    # R1: Student + Senior → Student discount (senior ignored)
    assert calculate_discount(True, True) == "Student discount: 20%"

    # R1: Student only → Student discount
    assert calculate_discount(True, False) == "Student discount: 20%"

    # R2: Senior only → Senior discount
    assert calculate_discount(False, True) == "Senior discount: 15%"

    # R3: Neither → No discount
    assert calculate_discount(False, False) == "No discount"
```

---

## Example 3: ATM Withdrawal Logic

### Requirement

ATM withdrawal depends on:

1. **Card valid**: Yes/No
2. **PIN correct**: Yes/No
3. **Sufficient balance**: Yes/No
4. **Daily limit not exceeded**: Yes/No

### Complete Decision Table

| Condition            | R1  | R2  | R3  | R4  | R5  | R6  | R7  | R8  | R9  | R10 | R11 | R12 | R13 | R14 | R15 | R16 |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Valid card           | Y   | Y   | Y   | Y   | Y   | Y   | Y   | Y   | N   | N   | N   | N   | N   | N   | N   | N   |
| Correct PIN          | Y   | Y   | Y   | Y   | N   | N   | N   | N   | Y   | Y   | Y   | Y   | N   | N   | N   | N   |
| Sufficient balance   | Y   | Y   | N   | N   | Y   | Y   | N   | N   | Y   | Y   | N   | N   | Y   | Y   | N   | N   |
| Under limit          | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   | Y   | N   |
| **Actions**          |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| Dispense cash        | X   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   |
| "Limit exceeded"     | -   | X   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   |
| "Insufficient funds" | -   | -   | X   | X   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   | -   |
| "Invalid PIN"        | -   | -   | -   | -   | X   | X   | X   | X   | -   | -   | -   | -   | -   | -   | -   | -   |
| "Invalid card"       | -   | -   | -   | -   | -   | -   | -   | -   | X   | X   | X   | X   | X   | X   | X   | X   |

**16 rules** for 4 binary conditions!

### Simplified Table

| Condition            | R1  | R2  | R3  | R4  | R5  |
| -------------------- | --- | --- | --- | --- | --- |
| Valid card           | Y   | Y   | Y   | Y   | N   |
| Correct PIN          | Y   | Y   | Y   | N   | -   |
| Sufficient balance   | Y   | Y   | N   | -   | -   |
| Under limit          | Y   | N   | -   | -   | -   |
| **Actions**          |     |     |     |     |     |
| Dispense cash        | X   | -   | -   | -   | -   |
| "Limit exceeded"     | -   | X   | -   | -   | -   |
| "Insufficient funds" | -   | -   | X   | -   | -   |
| "Invalid PIN"        | -   | -   | -   | X   | -   |
| "Invalid card"       | -   | -   | -   | -   | X   |

**Simplified from 16 to 5 rules** by using logical priorities:

- Invalid card is checked first (other conditions don't matter)
- Invalid PIN is checked second (balance/limit don't matter)
- Then check balance and limit

```python
class ATM:
    def __init__(self, valid_cards, pin_database, account_balances, daily_limits):
        self.valid_cards = valid_cards
        self.pins = pin_database
        self.balances = account_balances
        self.daily_limits = daily_limits
        self.daily_withdrawn = {}

    def withdraw(self, card_number, pin, amount):
        """Process withdrawal using simplified decision table logic."""

        # R5: Check card validity first
        if card_number not in self.valid_cards:
            return False, "Invalid card"

        # R4: Check PIN second
        if self.pins.get(card_number) != pin:
            return False, "Invalid PIN"

        # R3: Check sufficient balance
        if self.balances.get(card_number, 0) < amount:
            return False, "Insufficient funds"

        # R2: Check daily limit
        withdrawn_today = self.daily_withdrawn.get(card_number, 0)
        if withdrawn_today + amount > self.daily_limits.get(card_number, 500):
            return False, "Daily limit exceeded"

        # R1: All checks passed - dispense cash
        self.balances[card_number] -= amount
        self.daily_withdrawn[card_number] = withdrawn_today + amount
        return True, f"Cash dispensed: ${amount}"


def test_atm_decision_table():
    atm = ATM(
        valid_cards=["1234"],
        pin_database={"1234": "5678"},
        account_balances={"1234": 1000},
        daily_limits={"1234": 500}
    )

    # R1: All conditions met → Dispense cash
    success, msg = atm.withdraw("1234", "5678", 100)
    assert success == True
    assert "Cash dispensed: $100" in msg

    # R2: Daily limit exceeded
    success, msg = atm.withdraw("1234", "5678", 500)  # Already withdrew 100
    assert success == False
    assert "Daily limit exceeded" in msg

    # Reset for next tests
    atm = ATM(
        valid_cards=["1234"],
        pin_database={"1234": "5678"},
        account_balances={"1234": 50},
        daily_limits={"1234": 500}
    )

    # R3: Insufficient balance
    success, msg = atm.withdraw("1234", "5678", 100)
    assert success == False
    assert "Insufficient funds" in msg

    # R4: Invalid PIN
    success, msg = atm.withdraw("1234", "0000", 20)
    assert success == False
    assert "Invalid PIN" in msg

    # R5: Invalid card
    success, msg = atm.withdraw("9999", "5678", 20)
    assert success == False
    assert "Invalid card" in msg
```

---

## Combining Decision Tables with EP and BVA

Decision tables work best when combined with other techniques.

### Example: Course Registration

**Conditions**:

- Student type: Freshman, Sophomore, Junior, Senior
- Credits attempted: 0-18 (boundary: 12 for full-time)
- GPA: 0.0-4.0 (boundary: 2.0 for good standing)

### Step 1: Use EP for Student Type

Partitions:

- Freshman (1 value)
- Sophomore (1 value)
- Junior (1 value)
- Senior (1 value)

### Step 2: Use BVA for Credits

Test values: 0, 11, 12, 13, 18, 19

### Step 3: Use BVA for GPA

Test values: 0.0, 1.9, 2.0, 2.1, 4.0, 4.1

### Step 4: Create Decision Table for Business Logic

| Condition            | R1  | R2  | R3  | R4  |
| -------------------- | --- | --- | --- | --- |
| Senior               | Y   | N   | -   | -   |
| GPA >= 2.0           | -   | Y   | Y   | N   |
| Credits >= 12        | -   | Y   | N   | -   |
| **Actions**          |     |     |     |     |
| Early registration   | X   | -   | -   | -   |
| Normal registration  | -   | X   | -   | -   |
| Limited registration | -   | -   | X   | -   |
| Registration hold    | -   | -   | -   | X   |

```typescript
interface Student {
  type: "Freshman" | "Sophomore" | "Junior" | "Senior";
  gpa: number;
  credits: number;
}

function determineRegistration(student: Student): string {
  const isSenior = student.type === "Senior";
  const goodStanding = student.gpa >= 2.0;
  const fullTime = student.credits >= 12;

  // R1: Seniors get early registration
  if (isSenior) {
    return "Early registration";
  }

  // R2: Good standing + full-time
  if (goodStanding && fullTime) {
    return "Normal registration";
  }

  // R3: Good standing but not full-time
  if (goodStanding && !fullTime) {
    return "Limited registration (part-time)";
  }

  // R4: Not in good standing
  return "Registration hold - see advisor";
}

describe("Course Registration Decision Table + BVA", () => {
  // R1: Senior (boundary: Senior vs Junior)
  test("Senior with any GPA/credits gets early registration", () => {
    expect(
      determineRegistration({ type: "Senior", gpa: 1.5, credits: 6 }),
    ).toBe("Early registration");
  });

  // R2: Good standing + full-time (test boundaries)
  test("Junior with GPA 2.0 (boundary) and 12 credits (boundary)", () => {
    expect(
      determineRegistration({ type: "Junior", gpa: 2.0, credits: 12 }),
    ).toBe("Normal registration");
  });

  test("Sophomore with GPA 2.1 and 13 credits", () => {
    expect(
      determineRegistration({ type: "Sophomore", gpa: 2.1, credits: 13 }),
    ).toBe("Normal registration");
  });

  // R3: Good standing but part-time (test boundary)
  test("Freshman with GPA 2.5 and 11 credits (below full-time)", () => {
    expect(
      determineRegistration({ type: "Freshman", gpa: 2.5, credits: 11 }),
    ).toBe("Limited registration (part-time)");
  });

  // R4: Not in good standing (test boundary)
  test("Junior with GPA 1.9 (below threshold)", () => {
    expect(
      determineRegistration({ type: "Junior", gpa: 1.9, credits: 15 }),
    ).toBe("Registration hold - see advisor");
  });

  test("Sophomore with GPA 0.0 (minimum boundary)", () => {
    expect(
      determineRegistration({ type: "Sophomore", gpa: 0.0, credits: 12 }),
    ).toBe("Registration hold - see advisor");
  });
});
```

---

## Example 4: Insurance Premium Calculator

### Requirement

Calculate car insurance premium based on:

- **Age**: < 25, 25-60, > 60
- **Driving record**: Clean (0 violations), Minor (1-2 violations), Major (3+ violations)
- **Coverage**: Basic, Premium

### Decision Table (Simplified)

| Condition           | R1   | R2   | R3  | R4   | R5   | R6  | R7   | R8   | R9  |
| ------------------- | ---- | ---- | --- | ---- | ---- | --- | ---- | ---- | --- |
| Age < 25            | Y    | Y    | Y   | N    | N    | N   | N    | N    | N   |
| Age 25-60           | N    | N    | N   | Y    | Y    | Y   | N    | N    | N   |
| Age > 60            | N    | N    | N   | N    | N    | N   | Y    | Y    | Y   |
| Clean record        | Y    | N    | N   | Y    | N    | N   | Y    | N    | N   |
| Minor violations    | N    | Y    | N   | N    | Y    | N   | N    | Y    | N   |
| Major violations    | N    | N    | Y   | N    | N    | Y   | N    | N    | Y   |
| Premium coverage    | -    | -    | -   | -    | -    | -   | -    | -    | -   |
| **Actions**         |      |      |     |      |      |     |      |      |     |
| Base rate           | $200 | $300 | -   | $150 | $200 | -   | $180 | $250 | -   |
| Reject              | -    | -    | X   | -    | -    | X   | -    | -    | X   |
| Add 50% for Premium | X    | X    | -   | X    | X    | -   | X    | X    | -   |

**Note**: Major violations result in rejection for young and senior drivers.

```python
def calculate_insurance_premium(age, violations, coverage_type):
    """
    Calculate insurance premium using decision table.

    Returns: (approved: bool, premium: float, reason: str)
    """
    # Determine age category
    if age < 25:
        age_category = 'young'
    elif 25 <= age <= 60:
        age_category = 'adult'
    else:
        age_category = 'senior'

    # Determine violation category
    if violations == 0:
        record = 'clean'
    elif violations <= 2:
        record = 'minor'
    else:
        record = 'major'

    # Decision table mapping
    premiums = {
        ('young', 'clean'): 200,
        ('young', 'minor'): 300,
        ('young', 'major'): None,  # Rejected
        ('adult', 'clean'): 150,
        ('adult', 'minor'): 200,
        ('adult', 'major'): None,  # Rejected
        ('senior', 'clean'): 180,
        ('senior', 'minor'): 250,
        ('senior', 'major'): None,  # Rejected
    }

    key = (age_category, record)
    base_premium = premiums.get(key)

    if base_premium is None:
        return False, 0, f"Application rejected: {record} record with {age_category} driver"

    # Apply coverage multiplier
    final_premium = base_premium * 1.5 if coverage_type == 'premium' else base_premium

    return True, final_premium, f"Approved: {age_category} driver, {record} record"


def test_insurance_premium_decision_table():
    # R1: Young + Clean + Basic → $200
    approved, premium, msg = calculate_insurance_premium(22, 0, 'basic')
    assert approved == True
    assert premium == 200

    # R1 with Premium coverage: Young + Clean + Premium → $300
    approved, premium, msg = calculate_insurance_premium(22, 0, 'premium')
    assert approved == True
    assert premium == 300  # 200 * 1.5

    # R2: Young + Minor → $300 (basic)
    approved, premium, msg = calculate_insurance_premium(23, 1, 'basic')
    assert approved == True
    assert premium == 300

    # R3: Young + Major → Rejected
    approved, premium, msg = calculate_insurance_premium(24, 3, 'basic')
    assert approved == False
    assert "rejected" in msg.lower()

    # R4: Adult + Clean → $150
    approved, premium, msg = calculate_insurance_premium(35, 0, 'basic')
    assert approved == True
    assert premium == 150

    # R5: Adult + Minor → $200
    approved, premium, msg = calculate_insurance_premium(40, 2, 'basic')
    assert approved == True
    assert premium == 200

    # R6: Adult + Major → Rejected
    approved, premium, msg = calculate_insurance_premium(50, 4, 'basic')
    assert approved == False

    # R7: Senior + Clean → $180
    approved, premium, msg = calculate_insurance_premium(65, 0, 'basic')
    assert approved == True
    assert premium == 180

    # R8: Senior + Minor → $250
    approved, premium, msg = calculate_insurance_premium(70, 1, 'basic')
    assert approved == True
    assert premium == 250

    # R9: Senior + Major → Rejected
    approved, premium, msg = calculate_insurance_premium(75, 3, 'basic')
    assert approved == False
```

---

## Testing Multiple Actions

Some rules trigger **multiple actions** simultaneously.

### Example: User Permissions

| Condition          | R1  | R2  | R3  | R4  |
| ------------------ | --- | --- | --- | --- |
| Admin user         | Y   | Y   | N   | N   |
| Premium member     | -   | -   | Y   | N   |
| **Actions**        |     |     |     |     |
| View content       | X   | X   | X   | X   |
| Edit content       | X   | X   | X   | -   |
| Delete content     | X   | X   | -   | -   |
| Access admin panel | X   | X   | -   | -   |
| Download reports   | X   | X   | X   | -   |
| Upload files       | X   | -   | X   | -   |

```javascript
class UserPermissions {
  constructor(isAdmin, isPremium) {
    this.isAdmin = isAdmin;
    this.isPremium = isPremium;
  }

  getPermissions() {
    const permissions = {
      viewContent: false,
      editContent: false,
      deleteContent: false,
      accessAdminPanel: false,
      downloadReports: false,
      uploadFiles: false,
    };

    // R1 & R2: Admin users (premium status doesn't affect admin permissions)
    if (this.isAdmin) {
      permissions.viewContent = true;
      permissions.editContent = true;
      permissions.deleteContent = true;
      permissions.accessAdminPanel = true;
      permissions.downloadReports = true;
      permissions.uploadFiles = true;
      return permissions;
    }

    // R3: Premium members (not admin)
    if (this.isPremium) {
      permissions.viewContent = true;
      permissions.editContent = true;
      permissions.downloadReports = true;
      permissions.uploadFiles = true;
      return permissions;
    }

    // R4: Free users (default)
    permissions.viewContent = true;
    return permissions;
  }
}

describe("User Permissions Decision Table", () => {
  test("R1/R2: Admin gets all permissions", () => {
    const admin = new UserPermissions(true, false);
    const perms = admin.getPermissions();

    expect(perms.viewContent).toBe(true);
    expect(perms.editContent).toBe(true);
    expect(perms.deleteContent).toBe(true);
    expect(perms.accessAdminPanel).toBe(true);
    expect(perms.downloadReports).toBe(true);
    expect(perms.uploadFiles).toBe(true);
  });

  test("R3: Premium member gets limited permissions", () => {
    const premium = new UserPermissions(false, true);
    const perms = premium.getPermissions();

    expect(perms.viewContent).toBe(true);
    expect(perms.editContent).toBe(true);
    expect(perms.deleteContent).toBe(false); // No delete
    expect(perms.accessAdminPanel).toBe(false); // No admin panel
    expect(perms.downloadReports).toBe(true);
    expect(perms.uploadFiles).toBe(true);
  });

  test("R4: Free user can only view", () => {
    const free = new UserPermissions(false, false);
    const perms = free.getPermissions();

    expect(perms.viewContent).toBe(true);
    expect(perms.editContent).toBe(false);
    expect(perms.deleteContent).toBe(false);
    expect(perms.accessAdminPanel).toBe(false);
    expect(perms.downloadReports).toBe(false);
    expect(perms.uploadFiles).toBe(false);
  });
});
```

---

## Common Mistakes

### 1. Missing Rule Combinations

❌ **Wrong**: Only test the "happy path" rules  
✅ **Right**: Test all combinations, especially error cases

### 2. Inconsistent Actions

❌ **Wrong**: Same conditions lead to different actions in different rules  
✅ **Right**: Each unique combination should have exactly one outcome

### 3. Overlapping Rules

❌ **Wrong**: Multiple rules match the same input  
✅ **Right**: Rules should be mutually exclusive (or have clear priority)

### 4. Not Simplifying

❌ **Wrong**: Create 32 rules when 6 would suffice  
✅ **Right**: Use "don't care" values and logical grouping

### 5. Ignoring Impossible Combinations

❌ **Wrong**: Test rules that can never occur  
✅ **Right**: Mark impossible combinations and document why

Example: "User is both admin AND banned" (if admins can't be banned)

### 6. No Traceability

❌ **Wrong**: Test cases with no link to decision table rules  
✅ **Right**: Name tests after rules (test_R1_admin_access, etc.)

---

## Decision Table Checklist

Before finalizing your decision table:

- [ ] All conditions clearly identified
- [ ] All possible values for each condition listed
- [ ] All valid combinations included as rules
- [ ] Impossible combinations identified and excluded
- [ ] Actions defined for each rule
- [ ] Redundant rules combined using "don't care"
- [ ] Rule priorities documented (if rules overlap)
- [ ] Each rule has at least one test case
- [ ] Test cases traceable to rules
- [ ] Combined with EP/BVA where appropriate

---

## When NOT to Use Decision Tables

Decision tables are powerful but not always the best choice:

### Use Decision Tables When:

- Multiple conditions interact
- Complex business rules
- Combinations matter
- Need complete coverage

### Don't Use Decision Tables When:

- Single condition (use EP/BVA)
- Sequential workflow (use state transition)
- Simple if-else logic
- Continuous values with no clear partitions

---

## Summary

**Decision Tables** help you:

1. **Systematically test complex logic** with multiple conditions
2. **Ensure complete coverage** of all combinations
3. **Document business rules** in testable format
4. **Simplify testing** by identifying redundant rules

**Key Steps**:

1. Identify conditions and their possible values
2. Create rules for all valid combinations
3. Define actions for each rule
4. Simplify using "don't care" where appropriate
5. Create test cases for each rule

**Remember**: Decision tables work best when combined with EP (for partitioning values) and BVA (for testing boundaries within conditions).

---

## Practice Exercises

Create decision tables for these scenarios:

1. **Pizza Delivery Charge**

   - Distance: < 5 km, 5-10 km, > 10 km
   - Order value: < $20, $20-$50, > $50
   - Time: Peak hours, Off-peak
   - Determine: Delivery fee

2. **Library Book Checkout**

   - Member type: Student, Faculty, Public
   - Book type: Regular, Reference, New Release
   - Outstanding fines: Yes/No
   - Determine: Can checkout? How many days?

3. **Exam Grade Calculation**

   - Attendance: < 75%, 75-90%, > 90%
   - Midterm: < 60, 60-80, > 80
   - Final: < 60, 60-80, > 80
   - Project: Submitted/Not submitted
   - Determine: Pass/Fail and final grade

4. **Flight Upgrade Eligibility**
   - Ticket class: Economy, Business
   - Loyalty tier: None, Silver, Gold, Platinum
   - Flight occupancy: < 80%, 80-95%, > 95%
   - Determine: Upgrade offered? At what cost?

Document conditions, create decision tables (complete and simplified), and write test cases!

---

## Next Steps

- Practice with [Exercise 4: Decision Tables](../exercises/04-decision-tables.md)
- Review [05-state-transition-testing.md](./05-state-transition-testing.md) for sequential logic
- Combine decision tables with EP and BVA in your test designs
