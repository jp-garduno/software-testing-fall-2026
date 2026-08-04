# State Transition Testing

**Module**: 4 - Black Box Testing  
**Topic**: Testing Stateful Systems  
**Reading Time**: 30 minutes

---

## 🎯 Learning Objectives

After reading this document, you will be able to:

- Understand state machines and state-dependent behavior
- Create state transition diagrams
- Design state transition tables
- Identify valid and invalid transitions
- Apply coverage criteria to state testing
- Test real-world stateful systems

---

## What is State Transition Testing?

**State Transition Testing** is a black-box testing technique for systems where outputs depend not just on current inputs, but also on the system's **current state** (history of previous inputs).

### When to Use State Transition Testing

Use this technique when:

- System behavior changes based on **previous actions**
- System has distinct **states** or **modes**
- Different inputs produce different outputs **depending on state**
- Requirements include **state diagrams** or **workflows**

### Examples of Stateful Systems

- **E-commerce order**: New → Paid → Shipped → Delivered
- **User account**: Active → Suspended → Locked → Deleted
- **ATM session**: Idle → Card Inserted → PIN Entered → Transaction
- **Traffic light**: Red → Yellow → Green → Yellow → Red
- **TCP connection**: Closed → Listen → Established → Close-Wait → Closed

---

## Core Concepts

### State

A **state** represents a condition or situation during the system's lifetime.

**Example: User Account States**

- Active
- Suspended (temporary)
- Locked (security issue)
- Deleted (permanently removed)

### Transition

A **transition** is a change from one state to another, triggered by an **event** or **action**.

**Example: Account State Transitions**

- Active → Suspended (event: admin suspends account)
- Suspended → Active (event: admin reactivates)
- Active → Locked (event: 3 failed login attempts)

### Event/Action

An **event** or **action** triggers a transition.

**Example: Order Events**

- Place Order → New state
- Confirm Payment → Paid state
- Ship Order → Shipped state

---

## State Transition Diagram

A visual representation of states and transitions.

### Example 1: Simple Order Flow

```
     place_order
   ┌─────────────┐
   │             ↓
[Start]        [NEW]
                 │
                 │ confirm_payment
                 ↓
              [PAID]
                 │
                 │ ship_order
                 ↓
            [SHIPPED]
                 │
                 │ deliver_order
                 ↓
           [DELIVERED]
                 │
                 │ (final state)
                 ↓
              [End]
```

### Example 2: ATM Session

```
         insert_card
   ┌──────────────────┐
   │                  ↓
[IDLE]           [CARD_INSERTED]
   ↑                  │
   │                  │ enter_pin
   │                  ↓
   │            [PIN_ENTERED]
   │                  │
   │                  │ select_transaction
   │                  ↓
   │            [TRANSACTION]
   │                  │
   │                  │ complete / cancel
   │                  ↓
   └────────────[EJECT_CARD]
         eject_complete
```

### Example 3: Traffic Light

```
      timer_expires           timer_expires
        (30 sec)                (3 sec)
   ┌─────────────┐         ┌─────────────┐
   │             ↓         │             ↓
[GREEN] ────→ [YELLOW] ────→ [RED]
   ↑                              │
   │          timer_expires       │
   │            (30 sec)          │
   └──────────────────────────────┘
```

---

## State Transition Table

A table showing all possible state transitions.

### Format

| Current State | Event/Action | Next State | Output/Action |
| ------------- | ------------ | ---------- | ------------- |

### Example: User Login States

| Current State | Event            | Next State | Output                      |
| ------------- | ---------------- | ---------- | --------------------------- |
| Logged Out    | Valid Login      | Logged In  | Show dashboard              |
| Logged Out    | Invalid Login    | Logged Out | Show error, increment count |
| Logged Out    | 3rd Failed Login | Locked     | Lock account, send email    |
| Logged In     | Logout           | Logged Out | Clear session               |
| Logged In     | Timeout          | Logged Out | Clear session, show message |
| Locked        | Admin Unlock     | Logged Out | Send unlock email           |

---

## Example 1: E-Commerce Order States

### Requirements

An order goes through these states:

1. **NEW**: Order placed, awaiting payment
2. **PAID**: Payment confirmed
3. **SHIPPED**: Order shipped to customer
4. **DELIVERED**: Customer received order
5. **CANCELLED**: Order cancelled (only from NEW or PAID)

### State Transition Diagram

```
              place_order
         ┌─────────────────┐
         │                 ↓
     [Start]            [NEW]
                          │ │
          confirm_payment │ │ cancel_order
                          │ │
                          ↓ ↓
                       [PAID] ─────→ [CANCELLED]
                          │
                  ship    │
                          ↓
                    [SHIPPED]
                          │
                  deliver │
                          ↓
                   [DELIVERED]
```

### State Transition Table

| Current State | Event           | Next State | Valid?      |
| ------------- | --------------- | ---------- | ----------- |
| NEW           | confirm_payment | PAID       | ✓           |
| NEW           | cancel_order    | CANCELLED  | ✓           |
| PAID          | ship            | SHIPPED    | ✓           |
| PAID          | cancel_order    | CANCELLED  | ✓           |
| SHIPPED       | deliver         | DELIVERED  | ✓           |
| SHIPPED       | cancel_order    | SHIPPED    | ✗ (invalid) |
| DELIVERED     | any event       | DELIVERED  | ✗ (final)   |
| CANCELLED     | any event       | CANCELLED  | ✗ (final)   |

### Python Implementation

```python
class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.state = "NEW"

    def confirm_payment(self):
        if self.state == "NEW":
            self.state = "PAID"
            return True, "Payment confirmed"
        return False, f"Cannot confirm payment from {self.state} state"

    def ship(self):
        if self.state == "PAID":
            self.state = "SHIPPED"
            return True, "Order shipped"
        return False, f"Cannot ship from {self.state} state"

    def deliver(self):
        if self.state == "SHIPPED":
            self.state = "DELIVERED"
            return True, "Order delivered"
        return False, f"Cannot deliver from {self.state} state"

    def cancel(self):
        if self.state in ["NEW", "PAID"]:
            self.state = "CANCELLED"
            return True, "Order cancelled"
        return False, f"Cannot cancel from {self.state} state"

# Test cases for state transitions
def test_valid_order_flow():
    """Test complete valid order flow"""
    order = Order("ORD-001")

    # NEW → PAID
    assert order.state == "NEW"
    success, msg = order.confirm_payment()
    assert success == True
    assert order.state == "PAID"

    # PAID → SHIPPED
    success, msg = order.ship()
    assert success == True
    assert order.state == "SHIPPED"

    # SHIPPED → DELIVERED
    success, msg = order.deliver()
    assert success == True
    assert order.state == "DELIVERED"

def test_cancel_from_new():
    """Test cancellation from NEW state"""
    order = Order("ORD-002")
    success, msg = order.cancel()
    assert success == True
    assert order.state == "CANCELLED"

def test_cancel_from_paid():
    """Test cancellation from PAID state"""
    order = Order("ORD-003")
    order.confirm_payment()
    success, msg = order.cancel()
    assert success == True
    assert order.state == "CANCELLED"

def test_invalid_cancel_from_shipped():
    """Test invalid cancellation from SHIPPED state"""
    order = Order("ORD-004")
    order.confirm_payment()
    order.ship()
    success, msg = order.cancel()
    assert success == False
    assert order.state == "SHIPPED"  # State unchanged

def test_invalid_ship_from_new():
    """Test invalid transition: skip payment"""
    order = Order("ORD-005")
    success, msg = order.ship()
    assert success == False
    assert order.state == "NEW"  # State unchanged
```

---

## Example 2: User Account States

### Requirements

User accounts have these states:

- **ACTIVE**: Normal account usage
- **SUSPENDED**: Temporarily disabled by admin
- **LOCKED**: Locked due to security (3 failed logins)
- **DELETED**: Permanently removed

### State Transition Diagram

```
              create_account
         ┌────────────────────┐
         │                    ↓
     [Start]              [ACTIVE]
                            │ ╱ ╲ │
          ┌─────────────────┘   └─────────────┐
          │                                    │
    admin_suspend                      3_failed_logins
          │                                    │
          ↓                                    ↓
    [SUSPENDED]                            [LOCKED]
          │                                    │
          │ admin_reactivate    admin_unlock  │
          └──────────────┬────────────────────┘
                         ↓
                     [ACTIVE]
                         │
                         │ admin_delete
                         ↓
                    [DELETED]
                     (final)
```

### JavaScript/TypeScript Implementation

```javascript
class UserAccount {
  constructor(username) {
    this.username = username;
    this.state = "ACTIVE";
    this.failedLoginAttempts = 0;
  }

  suspend() {
    if (this.state === "ACTIVE") {
      this.state = "SUSPENDED";
      return { success: true, message: "Account suspended" };
    }
    return { success: false, message: `Cannot suspend from ${this.state}` };
  }

  reactivate() {
    if (this.state === "SUSPENDED") {
      this.state = "ACTIVE";
      this.failedLoginAttempts = 0;
      return { success: true, message: "Account reactivated" };
    }
    return { success: false, message: `Cannot reactivate from ${this.state}` };
  }

  unlock() {
    if (this.state === "LOCKED") {
      this.state = "ACTIVE";
      this.failedLoginAttempts = 0;
      return { success: true, message: "Account unlocked" };
    }
    return { success: false, message: `Cannot unlock from ${this.state}` };
  }

  recordFailedLogin() {
    if (this.state === "ACTIVE") {
      this.failedLoginAttempts++;
      if (this.failedLoginAttempts >= 3) {
        this.state = "LOCKED";
        return {
          success: true,
          message: "Account locked due to failed attempts",
        };
      }
      return {
        success: true,
        message: `Failed attempt ${this.failedLoginAttempts}/3`,
      };
    }
    return {
      success: false,
      message: "Cannot record failed login in current state",
    };
  }

  deleteAccount() {
    if (["ACTIVE", "SUSPENDED", "LOCKED"].includes(this.state)) {
      this.state = "DELETED";
      return { success: true, message: "Account deleted" };
    }
    return { success: false, message: "Account already deleted" };
  }
}

// Jest tests
describe("User Account State Transitions", () => {
  test("Active → Suspended → Active", () => {
    const user = new UserAccount("testuser");
    expect(user.state).toBe("ACTIVE");

    // Suspend
    let result = user.suspend();
    expect(result.success).toBe(true);
    expect(user.state).toBe("SUSPENDED");

    // Reactivate
    result = user.reactivate();
    expect(result.success).toBe(true);
    expect(user.state).toBe("ACTIVE");
  });

  test("Active → Locked after 3 failed logins", () => {
    const user = new UserAccount("testuser");

    user.recordFailedLogin();
    expect(user.state).toBe("ACTIVE");

    user.recordFailedLogin();
    expect(user.state).toBe("ACTIVE");

    user.recordFailedLogin();
    expect(user.state).toBe("LOCKED");
  });

  test("Locked → Active via unlock", () => {
    const user = new UserAccount("testuser");

    // Lock the account
    user.recordFailedLogin();
    user.recordFailedLogin();
    user.recordFailedLogin();
    expect(user.state).toBe("LOCKED");

    // Unlock
    const result = user.unlock();
    expect(result.success).toBe(true);
    expect(user.state).toBe("ACTIVE");
    expect(user.failedLoginAttempts).toBe(0);
  });

  test("Invalid transition: Reactivate from ACTIVE", () => {
    const user = new UserAccount("testuser");
    const result = user.reactivate();
    expect(result.success).toBe(false);
    expect(user.state).toBe("ACTIVE");
  });

  test("Delete from any state", () => {
    const user = new UserAccount("testuser");
    user.suspend();

    const result = user.deleteAccount();
    expect(result.success).toBe(true);
    expect(user.state).toBe("DELETED");
  });

  test("Cannot transition from DELETED", () => {
    const user = new UserAccount("testuser");
    user.deleteAccount();

    const result = user.reactivate();
    expect(result.success).toBe(false);
    expect(user.state).toBe("DELETED");
  });
});
```

---

## Coverage Criteria

### 1. State Coverage

Visit **every state** at least once.

**Example**: Order states (NEW, PAID, SHIPPED, DELIVERED, CANCELLED)

**Minimum test cases**: 2

- Test 1: NEW → PAID → SHIPPED → DELIVERED
- Test 2: NEW → CANCELLED

### 2. Transition Coverage (0-Switch Coverage)

Execute **every valid transition** at least once.

**Example**: Order transitions

| Transition          | Test Case |
| ------------------- | --------- |
| NEW → PAID          | TC1       |
| PAID → SHIPPED      | TC1       |
| SHIPPED → DELIVERED | TC1       |
| NEW → CANCELLED     | TC2       |
| PAID → CANCELLED    | TC3       |

**Minimum test cases**: 3

### 3. Path Coverage (All Paths)

Test **all possible paths** through the state machine.

**Warning**: Can explode exponentially with loops!

**Example**: User account with loop (ACTIVE ↔ SUSPENDED)

Possible paths with 3 transitions:

- ACTIVE → SUSPENDED → ACTIVE → SUSPENDED
- ACTIVE → SUSPENDED → ACTIVE → LOCKED
- ACTIVE → LOCKED → ACTIVE → SUSPENDED
- ... (many more)

**Practical approach**: Test key paths and boundary cases (max loops).

---

## Testing Invalid Transitions

Always test that **invalid transitions are rejected**.

### Example: Order System

```python
def test_invalid_transitions():
    """Test that invalid transitions are properly rejected"""

    # Cannot ship before payment
    order = Order("ORD-001")
    assert order.state == "NEW"
    success, msg = order.ship()
    assert success == False
    assert order.state == "NEW"  # State unchanged

    # Cannot deliver before shipping
    order = Order("ORD-002")
    order.confirm_payment()
    assert order.state == "PAID"
    success, msg = order.deliver()
    assert success == False
    assert order.state == "PAID"  # State unchanged

    # Cannot cancel after shipping
    order = Order("ORD-003")
    order.confirm_payment()
    order.ship()
    assert order.state == "SHIPPED"
    success, msg = order.cancel()
    assert success == False
    assert order.state == "SHIPPED"  # State unchanged

    # Cannot perform any action on delivered order
    order = Order("ORD-004")
    order.confirm_payment()
    order.ship()
    order.deliver()
    assert order.state == "DELIVERED"

    # Try all invalid transitions
    assert order.confirm_payment()[0] == False
    assert order.ship()[0] == False
    assert order.cancel()[0] == False
    assert order.state == "DELIVERED"  # Still delivered
```

---

## Example 3: Traffic Light Controller

### Requirements

Traffic light cycles:

- GREEN (30 seconds) → YELLOW (3 seconds) → RED (30 seconds) → GREEN

Emergency override: Any state → RED (emergency vehicle)

### State Transition Table with Timing

| Current State | Event     | Next State | Duration |
| ------------- | --------- | ---------- | -------- |
| GREEN         | timer_30s | YELLOW     | -        |
| GREEN         | emergency | RED        | -        |
| YELLOW        | timer_3s  | RED        | -        |
| YELLOW        | emergency | RED        | -        |
| RED           | timer_30s | GREEN      | -        |
| RED           | emergency | RED        | -        |

### Python Implementation with Timing

```python
import time

class TrafficLight:
    def __init__(self):
        self.state = "RED"
        self.state_start_time = time.time()

    def get_elapsed_time(self):
        return time.time() - self.state_start_time

    def update(self, emergency=False):
        """Update state based on timer or emergency"""
        if emergency:
            if self.state != "RED":
                self.state = "RED"
                self.state_start_time = time.time()
                return "Emergency: Changed to RED"
            return "Already RED"

        elapsed = self.get_elapsed_time()

        if self.state == "GREEN" and elapsed >= 30:
            self.state = "YELLOW"
            self.state_start_time = time.time()
            return "GREEN → YELLOW"

        elif self.state == "YELLOW" and elapsed >= 3:
            self.state = "RED"
            self.state_start_time = time.time()
            return "YELLOW → RED"

        elif self.state == "RED" and elapsed >= 30:
            self.state = "GREEN"
            self.state_start_time = time.time()
            return "RED → GREEN"

        return f"No change, {self.state} for {elapsed:.1f}s"

# Tests with timing simulation
def test_traffic_light_cycle():
    """Test complete cycle"""
    light = TrafficLight()

    # Start at RED
    assert light.state == "RED"

    # Simulate 30 seconds → GREEN
    light.state_start_time = time.time() - 30
    light.update()
    assert light.state == "GREEN"

    # Simulate 30 seconds → YELLOW
    light.state_start_time = time.time() - 30
    light.update()
    assert light.state == "YELLOW"

    # Simulate 3 seconds → RED
    light.state_start_time = time.time() - 3
    light.update()
    assert light.state == "RED"

def test_emergency_override():
    """Test emergency vehicle override"""
    light = TrafficLight()
    light.state = "GREEN"

    # Emergency override
    result = light.update(emergency=True)
    assert light.state == "RED"
    assert "Emergency" in result
```

---

## Combining State Transitions with Other Techniques

### State Transitions + BVA

Test boundary values **within state transitions**.

**Example**: Order with quantity limits

```python
def test_order_with_quantity_boundaries():
    """Test state transitions with BVA on quantity"""

    # Boundary: Minimum quantity (1)
    order = Order("ORD-001", quantity=1)
    order.confirm_payment()
    assert order.state == "PAID"

    # Boundary: Maximum quantity (100)
    order = Order("ORD-002", quantity=100)
    order.confirm_payment()
    assert order.state == "PAID"

    # Invalid: Below minimum (0)
    order = Order("ORD-003", quantity=0)
    success = order.confirm_payment()
    assert success == False  # Cannot confirm invalid quantity
    assert order.state == "NEW"  # State unchanged
```

### State Transitions + Decision Tables

Combine when state transitions have **complex conditional logic**.

**Example**: Discount eligibility changes by account state

| Account State | Order Total | Member Years | Discount |
| ------------- | ----------- | ------------ | -------- |
| ACTIVE        | > $100      | > 1          | 20%      |
| ACTIVE        | > $100      | ≤ 1          | 10%      |
| ACTIVE        | ≤ $100      | any          | 5%       |
| SUSPENDED     | any         | any          | 0%       |
| LOCKED        | any         | any          | 0%       |

---

## Common Mistakes

### 1. Missing Invalid Transitions

❌ **Wrong**: Only test happy path  
✅ **Right**: Test both valid AND invalid transitions

### 2. Not Testing Final States

❌ **Wrong**: Stop testing after reaching final state  
✅ **Right**: Verify no transitions possible from final states

### 3. Ignoring Initial State

❌ **Wrong**: Start tests from arbitrary state  
✅ **Right**: Always start from initial state or document preconditions

### 4. Insufficient Coverage

❌ **Wrong**: Test only state coverage  
✅ **Right**: Aim for transition coverage at minimum

### 5. Not Testing State Persistence

❌ **Wrong**: Only test transitions  
✅ **Right**: Verify state persists across operations

```python
def test_state_persistence():
    """Verify state persists when no transition occurs"""
    order = Order("ORD-001")
    order.confirm_payment()

    initial_state = order.state
    # Try invalid transition
    order.deliver()  # Cannot deliver from PAID

    # State should be unchanged
    assert order.state == initial_state
```

---

## State Transition Testing Checklist

Before finalizing state transition tests:

- [ ] All states identified and documented
- [ ] All valid transitions identified
- [ ] All invalid transitions identified
- [ ] State transition diagram or table created
- [ ] Every state covered by at least one test
- [ ] Every valid transition covered by at least one test
- [ ] Invalid transitions tested and rejected
- [ ] Initial state tests included
- [ ] Final state tests included
- [ ] State persistence verified

---

## Summary

**State Transition Testing** helps you:

1. **Test state-dependent behavior** systematically
2. **Verify valid transitions** work correctly
3. **Ensure invalid transitions** are rejected
4. **Achieve coverage** of states and transitions

**Key Concepts**:

- **State**: Condition of the system
- **Transition**: Change between states
- **Event**: Trigger for transition
- **Coverage**: State → Transition → Path

**Remember**: Always test both valid and invalid transitions!

---

## Practice Exercises

Design state machines and test cases for:

1. **ATM withdrawal**: Card inserted → PIN → Select amount → Dispense cash → Eject card
2. **Login system**: Logged out → Enter credentials → Verify → Logged in / Locked
3. **Thermostat**: Off → Heating → Target reached → Off / Cooling
4. **E-learning quiz**: Not started → In progress → Submitted → Graded

Include state diagrams, transition tables, and test cases!

---

## Next Steps

- Review all 5 Black Box Testing techniques
- Practice with [Exercise 5: State Transition](../exercises/05-state-transition.md)
- Start [Homework 4](../homework/homework-4.md)
- Combine techniques for comprehensive test coverage
