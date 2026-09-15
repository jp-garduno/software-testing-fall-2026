# Exercise 5: State Transition Testing

**Module**: 4 - Black Box Testing  
**Difficulty**: Intermediate  
**Time**: 60 minutes

---

## 🎯 Objectives

Practice identifying states, transitions, and events to test stateful systems.

By completing this exercise, you will:

- Identify states and transitions in a system
- Create state transition diagrams
- Build state transition tables
- Test valid and invalid transitions
- Calculate state and transition coverage
- Find defects in state machine implementations

---

## Instructions

For each scenario:

1. **Identify all states** the system can be in
2. **Identify events** that trigger transitions
3. **Map transitions** between states
4. **Create state diagram** (ASCII art or drawing)
5. **Create state transition table**
6. **Identify invalid transitions** (should be rejected)
7. **Implement state machine**
8. **Create tests** for all valid and invalid transitions
9. **Calculate coverage**

### State Transition Table Template

| Current State | Event   | Next State | Action/Output    |
| ------------- | ------- | ---------- | ---------------- |
| State A       | Event 1 | State B    | Action performed |
| State B       | Event 2 | State C    | Another action   |
| State B       | Event 3 | State A    | Return action    |

---

## Scenario 1: Order Processing System

### Requirements

An e-commerce order processing system with the following lifecycle:

**States**:

1. **New** - Order just created
2. **Confirmed** - Payment received and verified
3. **Shipped** - Package sent to customer
4. **Delivered** - Customer received package
5. **Returned** - Customer returned the order
6. **Refunded** - Money returned to customer
7. **Cancelled** - Order cancelled before shipping

**Events** (triggers):

- `confirm_payment()` - Payment processed successfully
- `cancel_order()` - Customer cancels order
- `ship_order()` - Warehouse ships package
- `mark_delivered()` - Delivery confirmed
- `initiate_return()` - Customer starts return process
- `approve_return()` - Return approved and received
- `issue_refund()` - Refund processed

**Business Rules**:

- Cannot cancel after shipping
- Cannot return without delivery
- Cannot ship without payment confirmation
- Return window: 30 days after delivery
- Refund only after return approval

### Part A: Create State Diagram

Create a state diagram showing all states and transitions:

```
ASCII Diagram Example:

                     cancel_order()
        [New] --------------------------> [Cancelled]
          |
          | confirm_payment()
          v
      [Confirmed]
          |
          | ship_order()              cancel_order()
          +------------------------> [Cancelled]
          |
          v
      [Shipped]
          |
          | mark_delivered()
          v
      [Delivered]
          |
          | initiate_return()
          v
      [Returned]
          |
          | approve_return()
          v
      [Refunded]
```

**Your task**: Complete the diagram with ALL transitions, including error paths.

### Part B: Create State Transition Table

Complete this table:

| Test ID | Current State | Event             | Expected Next State   | Action/Validation                         | Valid? |
| ------- | ------------- | ----------------- | --------------------- | ----------------------------------------- | ------ |
| ST_01   | New           | confirm_payment() | Confirmed             | Verify payment, send confirmation email   | Yes    |
| ST_02   | New           | cancel_order()    | Cancelled             | Release inventory, notify customer        | Yes    |
| ST_03   | New           | ship_order()      | New (no change)       | Error: Cannot ship unconfirmed order      | No     |
| ST_04   | Confirmed     | ship_order()      | Shipped               | Generate tracking number, notify customer | Yes    |
| ST_05   | Confirmed     | cancel_order()    | Cancelled             | Initiate refund, release inventory        | Yes    |
| ST_06   | Shipped       | cancel_order()    | Shipped (no change)   | Error: Cannot cancel shipped order        | No     |
| ST_07   | Shipped       | mark_delivered()  | Delivered             | Update delivery date, request review      | Yes    |
| ST_08   | Delivered     | initiate_return() | Returned              | Generate RMA number, send return label    | Yes    |
| ST_09   | Delivered     | confirm_payment() | Delivered (no change) | Error: Already paid                       | No     |
| ST_10   | Returned      | approve_return()  | Refunded              | Process refund, update inventory          | Yes    |
| ST_11   | New           | mark_delivered()  | New (no change)       | Error: Invalid state transition           | No     |
| ...     | ...           | ...               | ...                   | ...                                       | ...    |

**Your task**: Complete the table with ALL possible transitions (valid and invalid).

### Part C: Implementation

**Python**:

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Optional, Tuple

class OrderState(Enum):
    NEW = "New"
    CONFIRMED = "Confirmed"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    RETURNED = "Returned"
    REFUNDED = "Refunded"
    CANCELLED = "Cancelled"

class OrderStateMachine:
    def __init__(self, order_id):
        self.order_id = order_id
        self.state = OrderState.NEW
        self.payment_confirmed = False
        self.tracking_number = None
        self.delivered_date = None
        self.rma_number = None
        self.history = [(OrderState.NEW, datetime.now())]

    def _transition(self, new_state: OrderState, message: str) -> Tuple[bool, str]:
        """Helper to record state transition."""
        self.history.append((new_state, datetime.now()))
        old_state = self.state
        self.state = new_state
        return True, f"Transitioned from {old_state.value} to {new_state.value}: {message}"

    def _reject(self, message: str) -> Tuple[bool, str]:
        """Helper to reject invalid transition."""
        return False, f"Invalid transition from {self.state.value}: {message}"

    def confirm_payment(self) -> Tuple[bool, str]:
        """Event: Payment confirmed."""
        if self.state == OrderState.NEW:
            self.payment_confirmed = True
            return self._transition(OrderState.CONFIRMED, "Payment confirmed")
        else:
            return self._reject("Cannot confirm payment in current state")

    def cancel_order(self) -> Tuple[bool, str]:
        """Event: Cancel order."""
        if self.state == OrderState.NEW:
            return self._transition(OrderState.CANCELLED, "Order cancelled before payment")
        elif self.state == OrderState.CONFIRMED:
            return self._transition(OrderState.CANCELLED, "Order cancelled, refund initiated")
        elif self.state == OrderState.SHIPPED:
            return self._reject("Cannot cancel order after shipping")
        elif self.state == OrderState.DELIVERED:
            return self._reject("Cannot cancel order after delivery. Use return process.")
        else:
            return self._reject("Cannot cancel order in current state")

    def ship_order(self) -> Tuple[bool, str]:
        """Event: Ship order."""
        if self.state == OrderState.CONFIRMED:
            self.tracking_number = f"TRK{self.order_id}123"
            return self._transition(OrderState.SHIPPED, f"Order shipped, tracking: {self.tracking_number}")
        elif self.state == OrderState.NEW:
            return self._reject("Cannot ship order without payment confirmation")
        else:
            return self._reject("Cannot ship order in current state")

    def mark_delivered(self) -> Tuple[bool, str]:
        """Event: Mark as delivered."""
        if self.state == OrderState.SHIPPED:
            self.delivered_date = datetime.now()
            return self._transition(OrderState.DELIVERED, "Order delivered successfully")
        else:
            return self._reject("Cannot mark as delivered in current state")

    def initiate_return(self) -> Tuple[bool, str]:
        """Event: Customer initiates return."""
        if self.state == OrderState.DELIVERED:
            # Check 30-day return window
            if datetime.now() - self.delivered_date > timedelta(days=30):
                return self._reject("Return window (30 days) has expired")
            self.rma_number = f"RMA{self.order_id}456"
            return self._transition(OrderState.RETURNED, f"Return initiated, RMA: {self.rma_number}")
        else:
            return self._reject("Can only return delivered orders")

    def approve_return(self) -> Tuple[bool, str]:
        """Event: Return approved and received."""
        if self.state == OrderState.RETURNED:
            return self._transition(OrderState.REFUNDED, "Return approved, refund processed")
        else:
            return self._reject("No return to approve")

    def get_state(self) -> OrderState:
        """Get current state."""
        return self.state

    def get_history(self) -> list:
        """Get state transition history."""
        return self.history


# Test cases - Valid transitions
def test_valid_new_to_confirmed():
    """ST_01: New → Confirmed via confirm_payment()"""
    order = OrderStateMachine("ORD001")
    success, msg = order.confirm_payment()
    assert success == True
    assert order.get_state() == OrderState.CONFIRMED
    assert "Payment confirmed" in msg

def test_valid_new_to_cancelled():
    """ST_02: New → Cancelled via cancel_order()"""
    order = OrderStateMachine("ORD002")
    success, msg = order.cancel_order()
    assert success == True
    assert order.get_state() == OrderState.CANCELLED

def test_valid_confirmed_to_shipped():
    """ST_04: Confirmed → Shipped via ship_order()"""
    order = OrderStateMachine("ORD003")
    order.confirm_payment()
    success, msg = order.ship_order()
    assert success == True
    assert order.get_state() == OrderState.SHIPPED
    assert order.tracking_number is not None

def test_valid_shipped_to_delivered():
    """ST_07: Shipped → Delivered via mark_delivered()"""
    order = OrderStateMachine("ORD004")
    order.confirm_payment()
    order.ship_order()
    success, msg = order.mark_delivered()
    assert success == True
    assert order.get_state() == OrderState.DELIVERED

def test_valid_delivered_to_returned():
    """ST_08: Delivered → Returned via initiate_return()"""
    order = OrderStateMachine("ORD005")
    order.confirm_payment()
    order.ship_order()
    order.mark_delivered()
    success, msg = order.initiate_return()
    assert success == True
    assert order.get_state() == OrderState.RETURNED
    assert order.rma_number is not None

def test_valid_returned_to_refunded():
    """ST_10: Returned → Refunded via approve_return()"""
    order = OrderStateMachine("ORD006")
    order.confirm_payment()
    order.ship_order()
    order.mark_delivered()
    order.initiate_return()
    success, msg = order.approve_return()
    assert success == True
    assert order.get_state() == OrderState.REFUNDED

# Test cases - Invalid transitions
def test_invalid_new_to_shipped():
    """ST_03: New → Shipped (should fail - no payment)"""
    order = OrderStateMachine("ORD007")
    success, msg = order.ship_order()
    assert success == False
    assert order.get_state() == OrderState.NEW
    assert "Cannot ship" in msg

def test_invalid_shipped_to_cancelled():
    """ST_06: Shipped → Cancelled (should fail - already shipped)"""
    order = OrderStateMachine("ORD008")
    order.confirm_payment()
    order.ship_order()
    success, msg = order.cancel_order()
    assert success == False
    assert order.get_state() == OrderState.SHIPPED
    assert "Cannot cancel" in msg

def test_invalid_new_to_delivered():
    """ST_11: New → Delivered (should fail - invalid transition)"""
    order = OrderStateMachine("ORD009")
    success, msg = order.mark_delivered()
    assert success == False
    assert order.get_state() == OrderState.NEW

def test_invalid_delivered_confirm_payment():
    """ST_09: Delivered → confirm_payment (should fail - already paid)"""
    order = OrderStateMachine("ORD010")
    order.confirm_payment()
    order.ship_order()
    order.mark_delivered()
    success, msg = order.confirm_payment()
    assert success == False
    assert order.get_state() == OrderState.DELIVERED

# Test state history
def test_state_history_tracking():
    """Verify state history is tracked correctly"""
    order = OrderStateMachine("ORD011")
    order.confirm_payment()
    order.ship_order()
    order.mark_delivered()

    history = order.get_history()
    assert len(history) == 4  # NEW, CONFIRMED, SHIPPED, DELIVERED
    assert history[0][0] == OrderState.NEW
    assert history[1][0] == OrderState.CONFIRMED
    assert history[2][0] == OrderState.SHIPPED
    assert history[3][0] == OrderState.DELIVERED

# TODO: Add tests for ALL transitions in state table
```

### Part D: Calculate Coverage

Calculate:

1. **State Coverage**: (States visited / Total states) × 100%
2. **Transition Coverage**: (Transitions tested / Total valid transitions) × 100%
3. **Invalid Transition Coverage**: (Invalid transitions tested / Total invalid transitions) × 100%

---

## Scenario 2: User Account Lifecycle

### Requirements

User account management system with states:

**States**:

1. **Pending** - Account created, email verification needed
2. **Active** - Verified and active
3. **Suspended** - Temporarily suspended (policy violation)
4. **Locked** - Locked due to security reasons
5. **Dormant** - Inactive for 180+ days
6. **Deleted** - Soft deleted (can be restored)
7. **Permanently Deleted** - Hard deleted (cannot be restored)

**Events**:

- `verify_email()` - User clicks verification link
- `suspend_account(reason)` - Admin suspends account
- `lock_account(reason)` - System locks account (security)
- `reactivate_account()` - Admin/user reactivates
- `mark_dormant()` - System marks as dormant after 180 days
- `soft_delete()` - User/admin deletes account
- `restore_account()` - Restore soft-deleted account
- `hard_delete()` - Permanently delete after 30 days

**Business Rules**:

- Email must be verified within 7 days, or account deleted
- Suspended accounts can be reactivated by admin
- Locked accounts require security review before reactivation
- Dormant accounts can be reactivated by user login
- Soft-deleted accounts can be restored within 30 days
- After 30 days, soft-deleted → permanently deleted

### Part A: Create State Diagram

```
Your task: Create complete state diagram with all transitions
```

### Part B: Create State Transition Table

Create comprehensive table with:

- All valid transitions
- All invalid transitions
- Expected actions for each transition
- Time-based transitions (e.g., Pending → Deleted after 7 days)

### Part C: Implementation

**JavaScript**:

```javascript
class AccountState {
  static PENDING = "Pending";
  static ACTIVE = "Active";
  static SUSPENDED = "Suspended";
  static LOCKED = "Locked";
  static DORMANT = "Dormant";
  static DELETED = "Deleted";
  static PERMANENTLY_DELETED = "Permanently Deleted";
}

class UserAccount {
  constructor(userId, email) {
    this.userId = userId;
    this.email = email;
    this.state = AccountState.PENDING;
    this.createdAt = new Date();
    this.lastActivityAt = new Date();
    this.deletedAt = null;
    this.suspensionReason = null;
    this.lockReason = null;
    this.history = [{ state: AccountState.PENDING, timestamp: new Date() }];
  }

  _transition(newState, message) {
    this.history.push({ state: newState, timestamp: new Date() });
    const oldState = this.state;
    this.state = newState;
    return { success: true, message: `${oldState} → ${newState}: ${message}` };
  }

  _reject(message) {
    return {
      success: false,
      message: `Invalid transition from ${this.state}: ${message}`,
    };
  }

  verifyEmail() {
    if (this.state === AccountState.PENDING) {
      return this._transition(AccountState.ACTIVE, "Email verified");
    }
    return this._reject("Can only verify pending accounts");
  }

  suspendAccount(reason) {
    if (this.state === AccountState.ACTIVE) {
      this.suspensionReason = reason;
      return this._transition(AccountState.SUSPENDED, `Suspended: ${reason}`);
    }
    return this._reject("Can only suspend active accounts");
  }

  lockAccount(reason) {
    if (
      this.state === AccountState.ACTIVE ||
      this.state === AccountState.SUSPENDED
    ) {
      this.lockReason = reason;
      return this._transition(AccountState.LOCKED, `Locked: ${reason}`);
    }
    return this._reject("Cannot lock account in current state");
  }

  reactivateAccount() {
    if (this.state === AccountState.SUSPENDED) {
      this.suspensionReason = null;
      this.lastActivityAt = new Date();
      return this._transition(
        AccountState.ACTIVE,
        "Account reactivated from suspension",
      );
    } else if (this.state === AccountState.DORMANT) {
      this.lastActivityAt = new Date();
      return this._transition(
        AccountState.ACTIVE,
        "Account reactivated from dormant",
      );
    } else if (this.state === AccountState.LOCKED) {
      return this._reject("Locked accounts require security review");
    }
    return this._reject("Cannot reactivate in current state");
  }

  markDormant() {
    if (this.state === AccountState.ACTIVE) {
      const daysSinceActivity =
        (new Date() - this.lastActivityAt) / (1000 * 60 * 60 * 24);
      if (daysSinceActivity >= 180) {
        return this._transition(
          AccountState.DORMANT,
          "Marked as dormant due to inactivity",
        );
      }
      return this._reject("Account still active (< 180 days)");
    }
    return this._reject("Only active accounts can become dormant");
  }

  softDelete() {
    if (
      this.state === AccountState.ACTIVE ||
      this.state === AccountState.SUSPENDED ||
      this.state === AccountState.DORMANT ||
      this.state === AccountState.PENDING
    ) {
      this.deletedAt = new Date();
      return this._transition(AccountState.DELETED, "Account soft deleted");
    }
    return this._reject("Cannot delete in current state");
  }

  restoreAccount() {
    if (this.state === AccountState.DELETED) {
      const daysSinceDeletion =
        (new Date() - this.deletedAt) / (1000 * 60 * 60 * 24);
      if (daysSinceDeletion > 30) {
        return this._reject("Cannot restore after 30 days");
      }
      this.deletedAt = null;
      return this._transition(
        AccountState.ACTIVE,
        "Account restored from deletion",
      );
    }
    return this._reject("Can only restore deleted accounts");
  }

  hardDelete() {
    if (this.state === AccountState.DELETED) {
      const daysSinceDeletion =
        (new Date() - this.deletedAt) / (1000 * 60 * 60 * 24);
      if (daysSinceDeletion >= 30) {
        return this._transition(
          AccountState.PERMANENTLY_DELETED,
          "Account permanently deleted",
        );
      }
      return this._reject("Can only hard delete after 30 days");
    }
    return this._reject("Can only permanently delete soft-deleted accounts");
  }

  getState() {
    return this.state;
  }

  getHistory() {
    return this.history;
  }
}

describe("User Account Lifecycle - State Transitions", () => {
  test("Valid: Pending → Active via verify_email()", () => {
    const account = new UserAccount("user1", "test@example.com");
    const result = account.verifyEmail();
    expect(result.success).toBe(true);
    expect(account.getState()).toBe(AccountState.ACTIVE);
  });

  test("Valid: Active → Suspended via suspend_account()", () => {
    const account = new UserAccount("user2", "test@example.com");
    account.verifyEmail();
    const result = account.suspendAccount("Policy violation");
    expect(result.success).toBe(true);
    expect(account.getState()).toBe(AccountState.SUSPENDED);
  });

  test("Valid: Suspended → Active via reactivate_account()", () => {
    const account = new UserAccount("user3", "test@example.com");
    account.verifyEmail();
    account.suspendAccount("Test");
    const result = account.reactivateAccount();
    expect(result.success).toBe(true);
    expect(account.getState()).toBe(AccountState.ACTIVE);
  });

  test("Valid: Active → Deleted → Active via restore()", () => {
    const account = new UserAccount("user4", "test@example.com");
    account.verifyEmail();
    account.softDelete();
    expect(account.getState()).toBe(AccountState.DELETED);

    const result = account.restoreAccount();
    expect(result.success).toBe(true);
    expect(account.getState()).toBe(AccountState.ACTIVE);
  });

  test("Invalid: Pending → Suspended (should fail)", () => {
    const account = new UserAccount("user5", "test@example.com");
    const result = account.suspendAccount("Test");
    expect(result.success).toBe(false);
    expect(account.getState()).toBe(AccountState.PENDING);
  });

  test("Invalid: Locked → Active without security review", () => {
    const account = new UserAccount("user6", "test@example.com");
    account.verifyEmail();
    account.lockAccount("Security issue");
    const result = account.reactivateAccount();
    expect(result.success).toBe(false);
    expect(account.getState()).toBe(AccountState.LOCKED);
  });

  test("Time-based: Cannot restore after 30 days", () => {
    const account = new UserAccount("user7", "test@example.com");
    account.verifyEmail();
    account.softDelete();

    // Simulate 31 days passing
    account.deletedAt = new Date(Date.now() - 31 * 24 * 60 * 60 * 1000);

    const result = account.restoreAccount();
    expect(result.success).toBe(false);
    expect(account.getState()).toBe(AccountState.DELETED);
  });

  // TODO: Add tests for all transitions
});
```

---

## Scenario 3: Traffic Light Controller

### Requirements

Traffic light system with pedestrian crossing button:

**States**:

1. **Green** - Cars can go
2. **Yellow** - Prepare to stop
3. **Red** - Cars must stop
4. **Pedestrian Walk** - Pedestrians can cross
5. **Pedestrian Flash** - Finish crossing
6. **Maintenance** - System in maintenance mode

**Events**:

- `timer_green_expired()` - Green light timer expires (30 seconds)
- `timer_yellow_expired()` - Yellow light timer expires (5 seconds)
- `timer_red_expired()` - Red light timer expires (30 seconds)
- `pedestrian_button_pressed()` - Pedestrian requests crossing
- `timer_walk_expired()` - Walk signal expires (15 seconds)
- `timer_flash_expired()` - Flash signal expires (10 seconds)
- `enter_maintenance()` - Maintenance mode activated
- `exit_maintenance()` - Return to normal operation

**Business Rules**:

- Green → Yellow → Red → Green (normal cycle)
- Pedestrian button during Green: Queue request for next Red
- Pedestrian button during Red: Activate Walk signal
- Walk → Flash → Red (with shorter duration)
- Maintenance mode: All lights flash yellow

### Part A: Create State Diagram

### Part B: Create State Transition Table

### Part C: Implementation

```python
from enum import Enum
import time
from threading import Timer

class LightState(Enum):
    GREEN = "Green"
    YELLOW = "Yellow"
    RED = "Red"
    PED_WALK = "Pedestrian Walk"
    PED_FLASH = "Pedestrian Flash"
    MAINTENANCE = "Maintenance"

class TrafficLight:
    def __init__(self):
        self.state = LightState.GREEN
        self.pedestrian_requested = False
        self.timer = None
        self.history = []

    # TODO: Implement state machine

    def timer_green_expired(self):
        """Event: Green light timer expires."""
        pass

    def timer_yellow_expired(self):
        """Event: Yellow light timer expires."""
        pass

    def timer_red_expired(self):
        """Event: Red light timer expires."""
        pass

    def pedestrian_button_pressed(self):
        """Event: Pedestrian button pressed."""
        pass

    def timer_walk_expired(self):
        """Event: Walk signal timer expires."""
        pass

    def timer_flash_expired(self):
        """Event: Flash signal timer expires."""
        pass

    def enter_maintenance(self):
        """Event: Enter maintenance mode."""
        pass

    def exit_maintenance(self):
        """Event: Exit maintenance mode."""
        pass


# Test cases
def test_normal_cycle():
    """Test normal traffic light cycle: Green → Yellow → Red → Green"""
    light = TrafficLight()
    assert light.state == LightState.GREEN

    light.timer_green_expired()
    assert light.state == LightState.YELLOW

    light.timer_yellow_expired()
    assert light.state == LightState.RED

    light.timer_red_expired()
    assert light.state == LightState.GREEN

def test_pedestrian_during_red():
    """Test pedestrian button during red: Activate walk signal"""
    light = TrafficLight()
    light.timer_green_expired()  # → Yellow
    light.timer_yellow_expired()  # → Red

    result = light.pedestrian_button_pressed()
    assert result.success == True
    assert light.state == LightState.PED_WALK

def test_pedestrian_walk_cycle():
    """Test pedestrian cycle: Walk → Flash → Red"""
    light = TrafficLight()
    light.timer_green_expired()
    light.timer_yellow_expired()
    light.pedestrian_button_pressed()
    assert light.state == LightState.PED_WALK

    light.timer_walk_expired()
    assert light.state == LightState.PED_FLASH

    light.timer_flash_expired()
    assert light.state == LightState.RED

# TODO: Implement all test cases
```

---

## Scenario 4: Vending Machine

### Requirements

Vending machine with coin/bill acceptance:

**States**:

1. **Idle** - Waiting for money
2. **HasCredit** - Money inserted
3. **ProductSelected** - User selected product
4. **Dispensing** - Dispensing product
5. **ChangeReturn** - Returning change
6. **OutOfOrder** - Machine malfunction

**Events**:

- `insert_coin(amount)` - User inserts coin
- `select_product(product_id)` - User selects product
- `cancel_transaction()` - User presses cancel
- `dispense_complete()` - Product dispensed
- `change_returned()` - Change dispensing complete
- `insufficient_funds()` - Not enough money
- `product_out_of_stock()` - Selected product unavailable
- `system_error()` - Machine error

**Business Rules**:

- Accept coins: $0.25, $0.50, $1.00, $2.00
- Products: $1.50 - $3.00
- Must have sufficient funds before selection
- Return change if amount > product price
- Return all money on cancel

### Part A: Create State Diagram

### Part B: Create State Transition Table

### Part C: Implementation

**JavaScript**:

```javascript
class VendingMachine {
  constructor() {
    this.state = "Idle";
    this.credit = 0.0;
    this.selectedProduct = null;
    this.products = {
      A1: { name: "Chips", price: 1.5, stock: 10 },
      A2: { name: "Candy", price: 1.0, stock: 5 },
      B1: { name: "Soda", price: 2.0, stock: 8 },
      B2: { name: "Water", price: 1.5, stock: 12 },
    };
  }

  insertCoin(amount) {
    // TODO: Implement state transitions
  }

  selectProduct(productId) {
    // TODO: Implement state transitions
  }

  cancelTransaction() {
    // TODO: Implement state transitions
  }

  dispenseComplete() {
    // TODO: Implement state transitions
  }

  changeReturned() {
    // TODO: Implement state transitions
  }

  getState() {
    return this.state;
  }

  getCredit() {
    return this.credit;
  }
}

describe("Vending Machine - State Transitions", () => {
  test("Valid: Idle → HasCredit via insert_coin()", () => {
    const vm = new VendingMachine();
    const result = vm.insertCoin(1.0);
    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("HasCredit");
    expect(vm.getCredit()).toBe(1.0);
  });

  test("Valid: HasCredit → ProductSelected → Dispensing", () => {
    const vm = new VendingMachine();
    vm.insertCoin(2.0);

    const result = vm.selectProduct("A2"); // $1.00 candy
    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("ProductSelected");

    vm.dispenseComplete();
    expect(vm.getState()).toBe("ChangeReturn"); // $1.00 change
  });

  test("Invalid: Idle → ProductSelected (no money)", () => {
    const vm = new VendingMachine();
    const result = vm.selectProduct("A1");
    expect(result.success).toBe(false);
    expect(vm.getState()).toBe("Idle");
  });

  test("Valid: Cancel transaction returns to Idle with refund", () => {
    const vm = new VendingMachine();
    vm.insertCoin(1.5);
    expect(vm.getCredit()).toBe(1.5);

    const result = vm.cancelTransaction();
    expect(result.success).toBe(true);
    expect(vm.getState()).toBe("Idle");
    expect(vm.getCredit()).toBe(0);
    expect(result.refund).toBe(1.5);
  });

  // TODO: Add tests for all transitions
});
```

---

## Deliverables

Submit:

1. **State Diagrams** for all 4 scenarios (ASCII or drawn)
2. **State Transition Tables** showing:
   - All states
   - All events
   - All valid transitions
   - All invalid transitions
   - Expected actions
3. **Implementation**:
   - Working state machines
   - All transitions implemented
   - History tracking
4. **Test Suite**:
   - Tests for all valid transitions
   - Tests for all invalid transitions
   - Coverage report
5. **Coverage Analysis**:
   - State coverage percentage
   - Transition coverage percentage
   - Invalid transition coverage

---

## Evaluation Criteria

| Criteria                 | Points | Description                              |
| ------------------------ | ------ | ---------------------------------------- |
| **State Identification** | 20     | All states correctly identified          |
| **Transition Mapping**   | 25     | Complete and accurate transition table   |
| **Implementation**       | 30     | State machine works correctly            |
| **Test Coverage**        | 20     | All valid and invalid transitions tested |
| **Documentation**        | 5      | Clear diagrams and tables                |

**Total**: 100 points

---

## Tips for Success

1. **Start with states**: List all possible states first
2. **Identify events**: What triggers each transition?
3. **Draw it out**: Visual diagrams help see the big picture
4. **Test invalid transitions**: As important as valid ones
5. **Track history**: Helps with debugging and verification
6. **Consider edge cases**: Timeouts, errors, concurrent events

---

## Common Mistakes to Avoid

❌ Missing "return to previous state" transitions  
✅ Map all possible transitions, including loops

❌ Forgetting invalid transitions  
✅ Test that invalid transitions are properly rejected

❌ Not considering error states  
✅ Include maintenance, error, and recovery states

❌ Ignoring time-based transitions  
✅ Consider timers and automatic state changes

❌ Complex conditions in transitions  
✅ Keep transitions simple; use guards for conditions

---

## Coverage Metrics

Calculate these metrics:

### State Coverage

```
State Coverage = (States Visited) / (Total States) × 100%
```

### Transition Coverage (0-switch)

```
0-Switch = (Transitions Tested) / (Total Valid Transitions) × 100%
```

### Round-Trip Coverage (1-switch)

```
1-Switch = Test each transition AND return path
Example: A → B → A
```

### Example Calculation

For Order Processing System:

- **Total States**: 7 (New, Confirmed, Shipped, Delivered, Returned, Refunded, Cancelled)
- **Valid Transitions**: 10
- **Invalid Transitions**: ~30

**Target Coverage**:

- State Coverage: 100% (visit all states)
- Transition Coverage: 100% (test all valid transitions)
- Invalid Transition Coverage: 80%+ (test key invalid transitions)

---

## Bonus Challenge

### Multi-System State Coordination

Implement **Order Processing + Inventory System** where:

**Order States**: New, Confirmed, Shipped, Delivered
**Inventory States**: Available, Reserved, Committed, Shipped

**Coordinated Transitions**:

- Order: New → Confirmed requires Inventory: Available → Reserved
- Order: Confirmed → Shipped requires Inventory: Reserved → Committed
- If Inventory: Out of Stock, Order: Confirmed → Cancelled

Create:

1. Combined state diagram
2. Coordinated state table
3. Implementation managing both state machines
4. Tests for coordination scenarios

---

## Next Steps

After completing this exercise:

1. Review [Theory: State Transition Testing](../theory/05-state-transition.md)
2. Move to [Exercise 6: Comprehensive Black Box Testing](./06-comprehensive.md)
3. Practice identifying state machines in real systems
4. Compare state diagrams with classmates

---

**Remember: If it has states and transitions, it needs state transition testing!** 🎯
