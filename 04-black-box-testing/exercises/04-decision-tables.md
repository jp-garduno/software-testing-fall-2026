# Exercise 4: Decision Tables

**Module**: 4 - Black Box Testing  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice creating decision tables for complex business rules with multiple conditions.

By completing this exercise, you will:

- Identify conditions and actions from requirements
- Create complete decision tables
- Simplify tables using "don't care" entries
- Achieve 100% rule coverage
- Implement complex business logic based on decision tables

---

## Instructions

For each scenario:

1. **Identify all conditions** (inputs/factors)
2. **Identify all actions** (outputs/results)
3. **Create complete decision table** with all combinations
4. **Simplify table** by combining rules with "don't care" (-)
5. **Verify completeness** (no missing combinations)
6. **Implement code** based on the table
7. **Create tests** covering all rules

### Decision Table Template

| Rule #         | 1   | 2   | 3   | 4   | ... |
| -------------- | --- | --- | --- | --- | --- |
| **Conditions** |
| Condition 1    | T   | T   | F   | F   | ... |
| Condition 2    | T   | F   | T   | F   | ... |
| **Actions**    |
| Action 1       | X   | -   | X   | -   | ... |
| Action 2       | -   | X   | -   | X   | ... |

**Legend**:

- T = True, F = False
- X = Execute this action
- \- = Don't care / Don't execute

---

## Scenario 1: Weather Advisory System

### Requirements

A weather advisory system issues warnings based on:

**Conditions**:

- **Temperature**:
  - Very Cold: < 32°F
  - Cold: 32-50°F
  - Moderate: 51-85°F
  - Hot: 86-100°F
  - Very Hot: > 100°F
- **Humidity**:
  - Low: < 30%
  - Normal: 30-60%
  - High: > 60%
- **Wind Speed**:
  - Calm: < 10 mph
  - Breezy: 10-25 mph
  - Windy: 26-40 mph
  - Very Windy: > 40 mph

**Advisory Rules**:

1. **Frost Warning**: Temp < 32°F, any humidity, wind < 25 mph
2. **Freeze Warning**: Temp < 32°F, any humidity, wind >= 25 mph
3. **Heat Advisory**: Temp > 85°F, humidity > 60%, any wind
4. **Excessive Heat Warning**: Temp > 100°F, any humidity, any wind
5. **High Wind Warning**: Any temp, any humidity, wind > 40 mph
6. **Dry Conditions**: Temp 51-100°F, humidity < 30%, wind >= 10 mph
7. **Pleasant**: Temp 51-85°F, humidity 30-60%, wind < 25 mph
8. **No Advisory**: All other combinations

### Part A: Create Complete Decision Table

First, translate requirements into testable conditions:

**Simplified Conditions**:

1. Temperature Very Cold (< 32°F)?
2. Temperature Very Hot (> 100°F)?
3. Temperature Hot (86-100°F)?
4. Temperature Moderate (51-85°F)?
5. Humidity High (> 60%)?
6. Humidity Low (< 30%)?
7. Wind Very Windy (> 40 mph)?
8. Wind Windy (26-40 mph)?
9. Wind Breezy (10-25 mph)?

**Actions**:

- Issue Frost Warning
- Issue Freeze Warning
- Issue Heat Advisory
- Issue Excessive Heat Warning
- Issue High Wind Warning
- Issue Dry Conditions Alert
- Issue Pleasant Conditions
- No Advisory

**Your Task**: Create a decision table covering all rules. Start with this template:

| Rule #         | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | ... |
| -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Conditions** |
| Temp < 32°F    | T   | T   | F   | F   | F   | F   | F   | F   | ... |
| Temp > 100°F   | F   | F   | T   | T   | F   | F   | F   | F   | ... |
| Temp 86-100°F  | F   | F   | F   | F   | T   | T   | F   | F   | ... |
| Temp 51-85°F   | F   | F   | F   | F   | F   | F   | T   | T   | ... |
| Humidity > 60% | -   | -   | -   | -   | T   | F   | T   | F   | ... |
| Humidity < 30% | -   | -   | -   | -   | F   | T   | F   | T   | ... |
| Wind > 40 mph  | F   | T   | -   | -   | -   | -   | F   | F   | ... |
| Wind 26-40 mph | F   | F   | -   | -   | -   | -   | F   | F   | ... |
| Wind 10-25 mph | -   | F   | -   | -   | -   | T   | -   | F   | ... |
| **Actions**    |
| Frost Warning  | X   | -   | -   | -   | -   | -   | -   | -   | ... |
| Freeze Warning | -   | X   | -   | -   | -   | -   | -   | -   | ... |
| Heat Advisory  | -   | -   | -   | -   | X   | -   | -   | -   | ... |
| Excessive Heat | -   | -   | X   | X   | -   | -   | -   | -   | ... |
| High Wind      | -   | X   | X   | -   | -   | -   | -   | -   | ... |
| Dry Conditions | -   | -   | -   | -   | -   | X   | -   | -   | ... |
| Pleasant       | -   | -   | -   | -   | -   | -   | X   | -   | ... |
| No Advisory    | -   | -   | -   | -   | -   | -   | -   | X   | ... |

**Complete this table** with all necessary rules.

### Part B: Simplify Table

Look for rules that can be combined using "don't care":

Example:

- If Rules 3 and 4 both issue "Excessive Heat Warning" and only differ in humidity, combine them with humidity = "-"

### Part C: Implementation

**Python**:

```python
from enum import Enum
from typing import List

class Advisory(Enum):
    FROST = "Frost Warning"
    FREEZE = "Freeze Warning"
    HEAT = "Heat Advisory"
    EXCESSIVE_HEAT = "Excessive Heat Warning"
    HIGH_WIND = "High Wind Warning"
    DRY = "Dry Conditions"
    PLEASANT = "Pleasant Conditions"
    NONE = "No Advisory"

class WeatherAdvisory:
    def __init__(self, temperature, humidity, wind_speed):
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed

    def get_advisories(self) -> List[Advisory]:
        """
        Get all applicable weather advisories.
        Returns list of Advisory enums (can be multiple).
        """
        advisories = []

        # Rule 1: Frost Warning
        if self.temperature < 32 and self.wind_speed < 25:
            advisories.append(Advisory.FROST)

        # Rule 2: Freeze Warning
        if self.temperature < 32 and self.wind_speed >= 25:
            advisories.append(Advisory.FREEZE)

        # Rule 3: Excessive Heat Warning (takes precedence)
        if self.temperature > 100:
            advisories.append(Advisory.EXCESSIVE_HEAT)

        # Rule 4: Heat Advisory
        elif self.temperature > 85 and self.humidity > 60:
            advisories.append(Advisory.HEAT)

        # Rule 5: High Wind Warning
        if self.wind_speed > 40:
            advisories.append(Advisory.HIGH_WIND)

        # Rule 6: Dry Conditions
        if 51 <= self.temperature <= 100 and self.humidity < 30 and self.wind_speed >= 10:
            advisories.append(Advisory.DRY)

        # Rule 7: Pleasant
        if (51 <= self.temperature <= 85 and
            30 <= self.humidity <= 60 and
            self.wind_speed < 25):
            advisories.append(Advisory.PLEASANT)

        # Rule 8: No Advisory
        if len(advisories) == 0:
            advisories.append(Advisory.NONE)

        return advisories


# Test cases based on decision table
def test_rule_1_frost_warning():
    """Rule 1: Temp < 32, Wind < 25 → Frost Warning"""
    weather = WeatherAdvisory(temperature=30, humidity=50, wind_speed=15)
    advisories = weather.get_advisories()
    assert Advisory.FROST in advisories

def test_rule_2_freeze_warning():
    """Rule 2: Temp < 32, Wind >= 25 → Freeze Warning"""
    weather = WeatherAdvisory(temperature=28, humidity=40, wind_speed=30)
    advisories = weather.get_advisories()
    assert Advisory.FREEZE in advisories

def test_rule_3_excessive_heat():
    """Rule 3: Temp > 100 → Excessive Heat Warning"""
    weather = WeatherAdvisory(temperature=105, humidity=30, wind_speed=10)
    advisories = weather.get_advisories()
    assert Advisory.EXCESSIVE_HEAT in advisories

def test_rule_4_heat_advisory():
    """Rule 4: Temp 86-100, Humidity > 60% → Heat Advisory"""
    weather = WeatherAdvisory(temperature=90, humidity=70, wind_speed=10)
    advisories = weather.get_advisories()
    assert Advisory.HEAT in advisories

def test_rule_5_high_wind():
    """Rule 5: Wind > 40 mph → High Wind Warning"""
    weather = WeatherAdvisory(temperature=70, humidity=50, wind_speed=45)
    advisories = weather.get_advisories()
    assert Advisory.HIGH_WIND in advisories

def test_rule_6_dry_conditions():
    """Rule 6: Temp 51-100, Humidity < 30%, Wind >= 10 → Dry"""
    weather = WeatherAdvisory(temperature=75, humidity=25, wind_speed=15)
    advisories = weather.get_advisories()
    assert Advisory.DRY in advisories

def test_rule_7_pleasant():
    """Rule 7: Temp 51-85, Humidity 30-60%, Wind < 25 → Pleasant"""
    weather = WeatherAdvisory(temperature=72, humidity=45, wind_speed=8)
    advisories = weather.get_advisories()
    assert Advisory.PLEASANT in advisories

def test_rule_8_no_advisory():
    """Rule 8: No conditions met → No Advisory"""
    weather = WeatherAdvisory(temperature=50, humidity=70, wind_speed=8)
    advisories = weather.get_advisories()
    assert Advisory.NONE in advisories

def test_multiple_advisories():
    """Multiple rules triggered: High wind + Excessive heat"""
    weather = WeatherAdvisory(temperature=105, humidity=50, wind_speed=45)
    advisories = weather.get_advisories()
    assert Advisory.EXCESSIVE_HEAT in advisories
    assert Advisory.HIGH_WIND in advisories
    assert len(advisories) == 2

# TODO: Add tests for all decision table rules
```

**JavaScript**:

```javascript
const Advisory = {
  FROST: "Frost Warning",
  FREEZE: "Freeze Warning",
  HEAT: "Heat Advisory",
  EXCESSIVE_HEAT: "Excessive Heat Warning",
  HIGH_WIND: "High Wind Warning",
  DRY: "Dry Conditions",
  PLEASANT: "Pleasant Conditions",
  NONE: "No Advisory",
};

class WeatherAdvisory {
  constructor(temperature, humidity, windSpeed) {
    this.temperature = temperature;
    this.humidity = humidity;
    this.windSpeed = windSpeed;
  }

  getAdvisories() {
    const advisories = [];

    // Rule 1: Frost Warning
    if (this.temperature < 32 && this.windSpeed < 25) {
      advisories.push(Advisory.FROST);
    }

    // Rule 2: Freeze Warning
    if (this.temperature < 32 && this.windSpeed >= 25) {
      advisories.push(Advisory.FREEZE);
    }

    // Rule 3: Excessive Heat Warning
    if (this.temperature > 100) {
      advisories.push(Advisory.EXCESSIVE_HEAT);
    }
    // Rule 4: Heat Advisory
    else if (this.temperature > 85 && this.humidity > 60) {
      advisories.push(Advisory.HEAT);
    }

    // Rule 5: High Wind Warning
    if (this.windSpeed > 40) {
      advisories.push(Advisory.HIGH_WIND);
    }

    // Rule 6: Dry Conditions
    if (
      this.temperature >= 51 &&
      this.temperature <= 100 &&
      this.humidity < 30 &&
      this.windSpeed >= 10
    ) {
      advisories.push(Advisory.DRY);
    }

    // Rule 7: Pleasant
    if (
      this.temperature >= 51 &&
      this.temperature <= 85 &&
      this.humidity >= 30 &&
      this.humidity <= 60 &&
      this.windSpeed < 25
    ) {
      advisories.push(Advisory.PLEASANT);
    }

    // Rule 8: No Advisory
    if (advisories.length === 0) {
      advisories.push(Advisory.NONE);
    }

    return advisories;
  }
}

describe("Weather Advisory - Decision Table", () => {
  test("Rule 1: Frost Warning", () => {
    const weather = new WeatherAdvisory(30, 50, 15);
    expect(weather.getAdvisories()).toContain(Advisory.FROST);
  });

  test("Rule 2: Freeze Warning", () => {
    const weather = new WeatherAdvisory(28, 40, 30);
    expect(weather.getAdvisories()).toContain(Advisory.FREEZE);
  });

  test("Rule 3: Excessive Heat Warning", () => {
    const weather = new WeatherAdvisory(105, 30, 10);
    expect(weather.getAdvisories()).toContain(Advisory.EXCESSIVE_HEAT);
  });

  test("Rule 4: Heat Advisory", () => {
    const weather = new WeatherAdvisory(90, 70, 10);
    expect(weather.getAdvisories()).toContain(Advisory.HEAT);
  });

  test("Multiple advisories: High wind + Excessive heat", () => {
    const weather = new WeatherAdvisory(105, 50, 45);
    const advisories = weather.getAdvisories();
    expect(advisories).toContain(Advisory.EXCESSIVE_HEAT);
    expect(advisories).toContain(Advisory.HIGH_WIND);
    expect(advisories).toHaveLength(2);
  });

  // TODO: Add tests for all rules
});
```

---

## Scenario 2: User Authentication System

### Requirements

Multi-factor authentication system with account locking:

**Conditions**:

1. **Username exists** in database? (Yes/No)
2. **Password correct**? (Yes/No)
3. **Failed attempts** in last 30 minutes:
   - 0-2 attempts: Normal
   - 3-4 attempts: Warning
   - 5+ attempts: Locked
4. **Account status**:
   - Active
   - Suspended
   - Locked (by admin)
5. **Time-based lock** expired? (Yes/No)
6. **2FA enabled**? (Yes/No)
7. **2FA code correct**? (Yes/No if enabled)

**Actions**:

1. Grant access + create session
2. Deny access - user not found
3. Deny access - wrong password
4. Deny access - account suspended
5. Deny access - account locked
6. Deny access - too many attempts (auto-lock for 30 min)
7. Prompt for 2FA code
8. Deny access - wrong 2FA code
9. Increment failed attempt counter
10. Reset failed attempt counter
11. Send security alert email

### Part A: Create Decision Table

**Your Task**: Create a complete decision table with all rules.

Start by organizing conditions:

| Rule #             | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | ... |
| ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Conditions**     |
| Username exists?   | F   | T   | T   | T   | T   | T   | T   | T   | ... |
| Password correct?  | -   | F   | F   | F   | T   | T   | T   | T   | ... |
| Failed attempts    | -   | 0-2 | 3-4 | 5+  | -   | -   | -   | -   | ... |
| Account Active?    | -   | T   | T   | T   | F   | F   | T   | T   | ... |
| Account Suspended? | -   | F   | F   | F   | T   | F   | F   | F   | ... |
| Account Locked?    | -   | F   | F   | F   | F   | T   | F   | F   | ... |
| Time lock expired? | -   | -   | -   | F   | -   | -   | -   | -   | ... |
| 2FA enabled?       | -   | -   | -   | -   | -   | -   | F   | T   | ... |
| 2FA code correct?  | -   | -   | -   | -   | -   | -   | -   | T/F | ... |
| **Actions**        |
| Grant access       | -   | -   | -   | -   | -   | -   | X   | X   | ... |
| User not found     | X   | -   | -   | -   | -   | -   | -   | -   | ... |
| Wrong password     | -   | X   | X   | -   | -   | -   | -   | -   | ... |
| Account suspended  | -   | -   | -   | -   | X   | -   | -   | -   | ... |
| Account locked     | -   | -   | -   | -   | -   | X   | -   | -   | ... |
| Too many attempts  | -   | -   | -   | X   | -   | -   | -   | -   | ... |
| Prompt 2FA         | -   | -   | -   | -   | -   | -   | -   | X   | ... |
| Wrong 2FA          | -   | -   | -   | -   | -   | -   | -   | -   | ... |
| Increment fails    | -   | X   | X   | X   | -   | -   | -   | -   | ... |
| Reset fails        | -   | -   | -   | -   | -   | -   | X   | X   | ... |
| Send alert         | -   | -   | X   | X   | -   | -   | -   | -   | ... |

**Complete the table** with all necessary rules.

### Part B: Implementation

```python
from datetime import datetime, timedelta
from enum import Enum

class AuthResult(Enum):
    SUCCESS = "Access granted"
    USER_NOT_FOUND = "User not found"
    WRONG_PASSWORD = "Incorrect password"
    ACCOUNT_SUSPENDED = "Account suspended"
    ACCOUNT_LOCKED = "Account locked by administrator"
    TOO_MANY_ATTEMPTS = "Account locked due to too many failed attempts"
    REQUIRES_2FA = "2FA code required"
    WRONG_2FA = "Incorrect 2FA code"

class User:
    def __init__(self, username, password_hash, status="active", two_fa_enabled=False):
        self.username = username
        self.password_hash = password_hash
        self.status = status  # active, suspended, locked
        self.two_fa_enabled = two_fa_enabled
        self.failed_attempts = []
        self.locked_until = None

class AuthenticationSystem:
    def __init__(self):
        self.users = {}

    def authenticate(self, username, password, two_fa_code=None):
        """
        Authenticate user based on decision table.
        Returns: (AuthResult, should_increment_fails, should_send_alert)
        """
        # TODO: Implement based on decision table
        pass

    def get_recent_failed_attempts(self, user):
        """Get number of failed attempts in last 30 minutes."""
        thirty_mins_ago = datetime.now() - timedelta(minutes=30)
        return len([t for t in user.failed_attempts if t > thirty_mins_ago])

    def is_time_lock_expired(self, user):
        """Check if time-based lock has expired."""
        if user.locked_until is None:
            return True
        return datetime.now() > user.locked_until


# Test cases for each decision table rule
def test_rule_user_not_found():
    """Rule: Username doesn't exist → User not found"""
    auth = AuthenticationSystem()
    result, increment, alert = auth.authenticate("nonexistent", "password")
    assert result == AuthResult.USER_NOT_FOUND
    assert increment == False
    assert alert == False

def test_rule_wrong_password_first_attempt():
    """Rule: Password wrong, 0-2 attempts → Wrong password, increment"""
    auth = AuthenticationSystem()
    auth.users["user1"] = User("user1", "correct_hash", "active")
    result, increment, alert = auth.authenticate("user1", "wrong_password")
    assert result == AuthResult.WRONG_PASSWORD
    assert increment == True
    assert alert == False

def test_rule_wrong_password_warning():
    """Rule: Password wrong, 3-4 attempts → Wrong password, increment, send alert"""
    auth = AuthenticationSystem()
    user = User("user1", "correct_hash", "active")
    # Simulate 3 previous failed attempts
    user.failed_attempts = [datetime.now()] * 3
    auth.users["user1"] = user

    result, increment, alert = auth.authenticate("user1", "wrong_password")
    assert result == AuthResult.WRONG_PASSWORD
    assert increment == True
    assert alert == True

def test_rule_too_many_attempts():
    """Rule: 5+ failed attempts → Lock account"""
    auth = AuthenticationSystem()
    user = User("user1", "correct_hash", "active")
    user.failed_attempts = [datetime.now()] * 5
    auth.users["user1"] = user

    result, increment, alert = auth.authenticate("user1", "wrong_password")
    assert result == AuthResult.TOO_MANY_ATTEMPTS
    assert user.locked_until is not None

def test_rule_account_suspended():
    """Rule: Account suspended → Access denied"""
    auth = AuthenticationSystem()
    auth.users["user1"] = User("user1", "hash", "suspended")
    result, increment, alert = auth.authenticate("user1", "password")
    assert result == AuthResult.ACCOUNT_SUSPENDED

def test_rule_2fa_required():
    """Rule: Password correct, 2FA enabled, no code → Prompt for 2FA"""
    auth = AuthenticationSystem()
    auth.users["user1"] = User("user1", "correct", "active", two_fa_enabled=True)
    result, increment, alert = auth.authenticate("user1", "correct", two_fa_code=None)
    assert result == AuthResult.REQUIRES_2FA

def test_rule_2fa_success():
    """Rule: Password correct, 2FA enabled, code correct → Access granted"""
    auth = AuthenticationSystem()
    auth.users["user1"] = User("user1", "correct", "active", two_fa_enabled=True)
    result, increment, alert = auth.authenticate("user1", "correct", two_fa_code="123456")
    assert result == AuthResult.SUCCESS

# TODO: Complete all decision table rules
```

---

## Scenario 3: Insurance Premium Calculator

### Requirements

Auto insurance premium calculator based on multiple factors:

**Conditions**:

1. **Driver Age**:
   - Under 21: Young
   - 21-25: New adult
   - 26-65: Standard
   - 65+: Senior
2. **Driving History** (last 5 years):
   - No accidents, no violations: Clean
   - 1 minor violation: Minor
   - 2+ violations OR 1 accident: Moderate
   - 2+ accidents: High risk
3. **Coverage Type**:
   - Liability only
   - Collision + Comprehensive
   - Full coverage
4. **Location**:
   - Urban (high crime)
   - Suburban
   - Rural

**Premium Rules** (monthly base rate):

- Base rate: $100
- Age multipliers:
  - Under 21: ×2.5
  - 21-25: ×1.8
  - 26-65: ×1.0
  - 65+: ×1.2
- History multipliers:
  - Clean: ×1.0
  - Minor: ×1.2
  - Moderate: ×1.5
  - High risk: ×2.0 (or deny coverage)
- Coverage multipliers:
  - Liability only: ×1.0
  - Collision + Comprehensive: ×1.5
  - Full coverage: ×2.0
- Location multipliers:
  - Urban: ×1.3
  - Suburban: ×1.0
  - Rural: ×0.9

**Special Rules**:

1. Deny coverage if: Age < 21 AND history = High risk
2. Deny coverage if: Age < 21 AND more than 2 violations
3. Mandatory full coverage if: Age < 25 AND history = Moderate or worse
4. Discount 10% if: Age 26-65 AND history = Clean AND location = Rural
5. Discount 5% if: Age 65+ AND history = Clean

### Part A: Create Decision Table

Create a decision table showing at least 15 key rules, including:

- Normal premium calculations
- Denial cases
- Discount cases
- Mandatory coverage cases

### Part B: Implementation

```javascript
class InsurancePremium {
  constructor(age, drivingHistory, coverageType, location) {
    this.age = age;
    this.drivingHistory = drivingHistory; // 'clean', 'minor', 'moderate', 'high_risk'
    this.coverageType = coverageType; // 'liability', 'collision_comp', 'full'
    this.location = location; // 'urban', 'suburban', 'rural'
    this.baseRate = 100;
  }

  calculatePremium() {
    /**
     * Calculate premium based on decision table.
     * Returns: {
     *   approved: boolean,
     *   premium: number,
     *   reason: string,
     *   appliedDiscounts: string[]
     * }
     */
    // TODO: Implement based on decision table
  }

  getAgeMultiplier() {
    if (this.age < 21) return 2.5;
    if (this.age <= 25) return 1.8;
    if (this.age <= 65) return 1.0;
    return 1.2;
  }

  getHistoryMultiplier() {
    const multipliers = {
      clean: 1.0,
      minor: 1.2,
      moderate: 1.5,
      high_risk: 2.0,
    };
    return multipliers[this.drivingHistory];
  }

  // TODO: Add other helper methods
}

describe("Insurance Premium - Decision Table", () => {
  test("Rule: Young driver with high risk → Deny coverage", () => {
    const calc = new InsurancePremium(20, "high_risk", "liability", "suburban");
    const result = calc.calculatePremium();
    expect(result.approved).toBe(false);
    expect(result.reason).toContain("high risk");
  });

  test("Rule: Standard driver, clean history, rural → 10% discount", () => {
    const calc = new InsurancePremium(35, "clean", "liability", "rural");
    const result = calc.calculatePremium();
    expect(result.approved).toBe(true);
    expect(result.appliedDiscounts).toContain("10% rural clean driver");
    // Base: 100 × 1.0 (age) × 1.0 (history) × 1.0 (coverage) × 0.9 (location) × 0.9 (discount) = 81
    expect(result.premium).toBeCloseTo(81, 2);
  });

  test("Rule: Young driver moderate history → Mandatory full coverage", () => {
    const calc = new InsurancePremium(22, "moderate", "liability", "suburban");
    const result = calc.calculatePremium();
    expect(result.approved).toBe(false);
    expect(result.reason).toContain("full coverage required");
  });

  test("Rule: Senior with clean history → 5% discount", () => {
    const calc = new InsurancePremium(70, "clean", "liability", "suburban");
    const result = calc.calculatePremium();
    expect(result.approved).toBe(true);
    expect(result.appliedDiscounts).toContain("5% senior clean driver");
  });

  // TODO: Add tests for all decision table rules
});
```

---

## Scenario 4: Shipping Method Selector

### Requirements

E-commerce shipping method selector based on:

**Conditions**:

1. **Package Weight**:
   - Light: 0-5 lbs
   - Medium: 5.1-20 lbs
   - Heavy: 20.1-50 lbs
   - Very Heavy: 50.1+ lbs
2. **Destination**:
   - Local (same state)
   - Regional (adjacent states)
   - National
   - International
3. **Urgency**:
   - Standard (5-7 days)
   - Expedited (2-3 days)
   - Overnight
4. **Cost Preference**:
   - Lowest cost
   - Balanced
   - Fastest

**Available Methods**:

1. Ground (5-7 days, $5-$50)
2. Priority Mail (2-3 days, $10-$75)
3. Express (overnight, $25-$150)
4. Freight (5-10 days, $100-$500, for very heavy)
5. International Standard (10-14 days, $30-$200)
6. International Express (3-5 days, $75-$400)

**Selection Rules**:

1. Very Heavy + Local/Regional → Freight only
2. Very Heavy + National → Freight or Ground (if cost is priority)
3. Very Heavy + International → Not available
4. Overnight + International → Not available
5. Overnight + (any weight) + National/Local → Express
6. Lowest cost + Light + Local → Ground
7. Fastest + Light/Medium + Local/Regional → Express
8. International → Only International methods
9. Default: Priority Mail if available

### Part A: Create Decision Table

Create decision table with at least 20 rules covering all combinations.

### Part B: Implementation

```python
from typing import List, Optional
from dataclasses import dataclass

@dataclass
class ShippingOption:
    method: str
    days: str
    cost_range: str
    cost_min: float
    cost_max: float

class ShippingSelector:
    def __init__(self, weight, destination, urgency, cost_preference):
        self.weight = weight
        self.destination = destination  # 'local', 'regional', 'national', 'international'
        self.urgency = urgency  # 'standard', 'expedited', 'overnight'
        self.cost_preference = cost_preference  # 'lowest', 'balanced', 'fastest'

    def get_weight_category(self):
        if self.weight <= 5:
            return 'light'
        elif self.weight <= 20:
            return 'medium'
        elif self.weight <= 50:
            return 'heavy'
        else:
            return 'very_heavy'

    def select_shipping_method(self) -> List[ShippingOption]:
        """
        Select appropriate shipping methods based on decision table.
        Returns list of available options, sorted by preference.
        """
        # TODO: Implement decision table logic
        pass


# Test cases
def test_rule_very_heavy_local_freight():
    """Rule: Very heavy + Local → Freight only"""
    selector = ShippingSelector(weight=60, destination='local',
                                urgency='standard', cost_preference='lowest')
    options = selector.select_shipping_method()
    assert len(options) == 1
    assert options[0].method == 'Freight'

def test_rule_overnight_international_unavailable():
    """Rule: Overnight + International → Not available"""
    selector = ShippingSelector(weight=10, destination='international',
                                urgency='overnight', cost_preference='fastest')
    options = selector.select_shipping_method()
    assert len(options) == 0 or all(opt.method != 'Express' for opt in options)

def test_rule_overnight_national_express():
    """Rule: Overnight + National → Express"""
    selector = ShippingSelector(weight=10, destination='national',
                                urgency='overnight', cost_preference='fastest')
    options = selector.select_shipping_method()
    assert options[0].method == 'Express'

def test_rule_lowest_cost_light_local():
    """Rule: Lowest cost + Light + Local → Ground"""
    selector = ShippingSelector(weight=3, destination='local',
                                urgency='standard', cost_preference='lowest')
    options = selector.select_shipping_method()
    assert options[0].method == 'Ground'

# TODO: Add tests for all decision table rules
```

---

## Deliverables

Submit:

1. **Complete Decision Tables** for all 4 scenarios:

   - All conditions listed
   - All actions listed
   - All rules documented
   - Simplified using "don't care"

2. **Completeness Verification**:

   - Total possible combinations calculated
   - All combinations accounted for
   - No contradictory rules
   - No missing rules

3. **Implementation**:

   - Working code (Python or JavaScript)
   - Tests for ALL rules in decision table
   - 100% rule coverage

4. **Analysis Document**:
   - How you simplified the table
   - Rules that could be combined
   - Edge cases discovered

---

## Evaluation Criteria

| Criteria                        | Points | Description                               |
| ------------------------------- | ------ | ----------------------------------------- |
| **Decision Table Completeness** | 30     | All conditions, actions, rules identified |
| **Table Simplification**        | 15     | Effective use of "don't care"             |
| **Implementation**              | 35     | Code correctly implements all rules       |
| **Test Coverage**               | 15     | All rules have corresponding tests        |
| **Documentation**               | 5      | Clear analysis and explanation            |

**Total**: 100 points

---

## Tips for Success

1. **Start with conditions**: List ALL input factors first
2. **List all actions**: Document every possible outcome
3. **Calculate combinations**: 2^n conditions = possible rules (before simplification)
4. **Look for patterns**: Rules that differ in only one condition can be combined
5. **Verify completeness**: Every possible input combination should match exactly one rule
6. **Test systematically**: Create one test per rule

---

## Common Mistakes to Avoid

❌ Forgetting to handle all combinations  
✅ Calculate 2^n and verify all are covered

❌ Overlapping rules (same conditions → different actions)  
✅ Each combination should match exactly one rule

❌ Missing edge cases  
✅ Pay special attention to boundary conditions

❌ Overly complex tables  
✅ Use "don't care" to simplify

❌ Actions that aren't mutually exclusive  
✅ Clarify which actions can occur together

---

## Bonus Challenge

### Decision Table Optimization

For **Scenario 3 (Insurance Premium)**:

1. Create the **complete** decision table (all 4^4 = 256 possible combinations)
2. **Simplify** to minimum number of rules using "don't care"
3. Calculate **reduction percentage**
4. Document your **simplification strategy**

Example simplification:

**Before**:

- Rule 1: Age=Young, History=Clean, Coverage=Liability, Location=Urban → Premium=$325
- Rule 2: Age=Young, History=Clean, Coverage=Liability, Location=Suburban → Premium=$250
- Rule 3: Age=Young, History=Clean, Coverage=Liability, Location=Rural → Premium=$225

**After**:

- Rule 1: Age=Young, History=Clean, Coverage=Liability, Location=ANY → Calculate based on location

---

## Next Steps

After completing this exercise:

1. Review [Theory: Decision Tables](../theory/04-decision-tables.md)
2. Move to [Exercise 5: State Transition Testing](./05-state-transition.md)
3. Compare your tables with classmates
4. Practice identifying when decision tables are the best technique

---

**Remember: Decision tables ensure you test ALL combinations of business rules!** 🎯
