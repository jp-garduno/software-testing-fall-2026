# Test Design Document — SecureBank Online Banking

**Student**: Isaac Vazquez (isaac-evs)
**Module**: 4 — Black Box Testing
**System Under Test**: `src/banking_system.py`

This document applies all four black box techniques to SecureBank's core
business rules: account transfers, account creation, bill payments,
transaction history filtering, monthly fees, and account state management.

---

## 1. Equivalence Partitioning

### Input: Transfer Amount

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | --------------------- | ---------------- |
| EP1 | Valid amount, within balance and daily limit | Valid | $500 (Checking, balance $1000) | Transfer succeeds |
| EP2 | Zero amount | Invalid | $0 | Error: Amount must be positive |
| EP3 | Negative amount | Invalid | -$100 | Error: Amount must be positive |
| EP4 | Amount exceeds daily limit | Invalid | $100,000 (Checking) | Error: Exceeds daily limit |
| EP5 | Amount exceeds current balance | Invalid | Balance + $1 | Error: Insufficient funds |

### Input: Account Type (account creation / validation)

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | --------------------- | ---------------- |
| EP6 | Recognized account type — Savings | Valid | `"Savings"` | Accepted |
| EP7 | Recognized account type — Checking | Valid | `"Checking"` | Accepted |
| EP8 | Recognized account type — Premium | Valid | `"Premium"` | Accepted |
| EP9 | Unrecognized account type | Invalid | `"Crypto"` | Error: Invalid account type |
| EP10 | Empty/blank account type | Invalid | `""` | Error: Invalid account type |

### Input: Account Balance (relative to minimum, drives Active/Suspended)

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | --------------------- | ---------------- |
| EP11 | Balance above the account type's minimum | Valid | Savings, $500 (min $100) | State = Active |
| EP12 | Balance below the account type's minimum | Invalid (business rule) | Savings, $50 | State = Suspended at creation |
| EP13 | Balance exactly at the minimum | Boundary-adjacent, valid | Savings, $100 | State = Active |

### Input: Payee (bill payment)

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | --------------------- | ---------------- |
| EP14 | Non-empty payee name | Valid | `"City Water Utility"` | Payee accepted |
| EP15 | Empty string payee | Invalid | `""` | Error: Invalid payee |
| EP16 | Whitespace-only payee | Invalid | `"   "` | Error: Invalid payee |
| EP17 | `None` payee | Invalid | `None` | Error: Invalid payee |

### Input: Date Range (transaction history filter)

| Partition ID | Description | Type | Representative Value | Expected Result |
| ------------ | ----------- | ---- | --------------------- | ---------------- |
| EP18 | Valid range, start before end | Valid | `2026-01-01` → `2026-01-31` | Returns matching transactions |
| EP19 | Valid range, start equals end (single day) | Valid | `2026-01-15` → `2026-01-15` | Returns only that day's transactions |
| EP20 | Invalid range, start after end | Invalid | `2026-02-01` → `2026-01-01` | Error: start_date must not be after end_date |
| EP21 | Valid range with no matching transactions | Valid (empty result, not an error) | Range outside all transaction dates | Returns an empty list, `success: True` |

**Required-coverage checklist**: transfer amount (EP1–EP5), account type
(EP6–EP10), account balance vs. minimum (EP11–EP13), payee (EP14–EP17), and
date range (EP18–EP21) — 5 distinct inputs, each with at least one valid and
one invalid class, as required.

---

## 2. Boundary Value Analysis

### Boundary: Transfer Amount — Checking Account ($5,000 daily limit)

| Test ID | Boundary | Test Value | Expected Result |
| ------- | -------- | ---------- | ---------------- |
| BV1 | Below minimum | $0.00 | Error: Amount must be positive |
| BV2 | Minimum valid | $0.01 | Transfer succeeds |
| BV3 | Just below limit | $4,999.99 | Transfer succeeds |
| BV4 | At limit | $5,000.00 | Transfer succeeds |
| BV5 | Just above limit | $5,000.01 | Error: Exceeds daily limit |
| BV6 | Far above limit | $10,000.00 | Error: Exceeds daily limit |

### Boundary: Transfer Amount — Savings Account ($2,000 daily limit)

| Test ID | Boundary | Test Value | Expected Result |
| ------- | -------- | ---------- | ---------------- |
| BV7 | Just below limit | $1,999.99 | Transfer succeeds |
| BV8 | At limit | $2,000.00 | Transfer succeeds |
| BV9 | Just above limit | $2,000.01 | Error: Exceeds daily limit |

### Boundary: Account Balance vs. Minimum — Savings ($100 minimum)

| Test ID | Boundary | Test Value (balance after transfer) | Expected Result |
| ------- | -------- | -------------------------------------- | ---------------- |
| BV10 | Just below minimum | $99.99 | State becomes Suspended |
| BV11 | At minimum | $100.00 | State remains Active |
| BV12 | Just above minimum | $100.01 | State remains Active |

### Boundary: Account Balance vs. Minimum — Premium ($10,000 minimum)

| Test ID | Boundary | Test Value | Expected Result |
| ------- | -------- | ---------- | ---------------- |
| BV13 | Just below minimum | $9,999.99 | State becomes Suspended |
| BV14 | At minimum | $10,000.00 | State remains Active |
| BV15 | Just above minimum | $10,000.01 | State remains Active |

### Boundary: Monthly Fee Waiver Threshold — Savings ($1,000 waiver threshold)

| Test ID | Boundary | Test Value (balance at fee time) | Expected Result |
| ------- | -------- | ------------------------------------ | ---------------- |
| BV16 | At threshold (not "above") | $1,000.00 | Fee charged ($5) — threshold is strictly "greater than" |
| BV17 | Just above threshold | $1,000.01 | Fee waived |
| BV18 | Just below threshold | $999.99 | Fee charged ($5) |

### Boundary: Insufficient Funds for Fee — Checking ($10 fee)

| Test ID | Boundary | Test Value (balance at fee time) | Expected Result |
| ------- | -------- | ------------------------------------ | ---------------- |
| BV19 | Just below fee amount | $9.99 | Fee fails, account Suspended |
| BV20 | Exactly at fee amount | $10.00 | Fee charged, balance becomes $0.00 |

**Required-coverage checklist**: 6 distinct boundaries (BV1–6, 7–9, 10–12,
13–15, 16–18, 19–20), each with 3–6 representative values straddling the
boundary — exceeds the required minimum of 5 boundaries.

---

## 3. Decision Tables

### Decision Table 1: Transfer Validation

| Condition | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 | Rule 9 |
| --------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Amount positive? | Y | Y | Y | Y | Y | Y | N | - | - |
| Sufficient funds? | Y | Y | Y | N | - | - | - | - | - |
| Within daily limit? | Y | N | - | - | - | - | - | - | - |
| Account is Active? | Y | - | - | - | Y | N | - | - | - |
| **Action** |
| Transfer succeeds | X | | | | | | | | |
| Error: Exceeds daily limit | | X | | | | | | | |
| Error: Insufficient funds | | | | X | | | | | |
| Error: Amount must be positive | | | | | | | X | | |
| Error: Account frozen/closed | | | | | | X | | | |

*Note on structure*: "Account is Active?" is only meaningful once amount and
funds checks pass, because the implementation checks account state **first**
(Rule 6 fires regardless of amount/funds, since a frozen account is rejected
before those checks run) — Rules 5 and 6 use "-" for amount/funds to reflect
that account-state rejection short-circuits the other validations. Rule 3
("Sufficient funds Y, daily limit not evaluated because Rule 2's N already
covers the limit failure") is folded into Rule 2 using don't-care on funds,
since a limit failure occurs independently of whether funds are sufficient
for the raw amount.

**Simplified table** (collapsing Rules 2–3 using "don't care", since exceeding
the limit produces the same action regardless of the funds check):

| Condition | R1: Success | R2: Exceeds limit | R3: Insufficient funds | R4: Not positive | R5: Frozen/Closed |
| --------- | ----------- | ------------------ | ------------------------ | ------------------ | -------------------- |
| Account Active? | Y | Y | Y | Y | N |
| Amount positive? | Y | Y | Y | N | - |
| Amount ≤ balance? | Y | - | N | - | - |
| Amount + daily total ≤ limit? | Y | N | - | - | - |
| **Action → Transfer succeeds / Error** | Succeeds | Exceeds limit | Insufficient funds | Must be positive | Account frozen/closed |

### Decision Table 2: Monthly Fee Processing

| Condition | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 |
| --------- | ------ | ------ | ------ | ------ | ------ | ------ |
| Account type | Savings | Savings | Checking | Checking | Premium | Any |
| Balance > waiver threshold? | Y | N | Y | N | - | - |
| Balance ≥ fee amount? | - | Y | - | Y | - | - |
| Balance < fee amount? | - | N | - | N | - | - |
| **Action** |
| No fee charged (fee is $0 for this type) | | | | | X | |
| Fee waived (balance above threshold) | X | | X | | | |
| Fee charged, balance reduced | | X | | X | | |
| Fee fails → account Suspended | | | | | | X (when balance < fee amount, any type with a nonzero fee) |

### Decision Table 3: Bill Payment Validation

| Condition | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 |
| --------- | ------ | ------ | ------ | ------ | ------ |
| Account Active? | Y | N | Y | Y | Y |
| Payee non-empty? | Y | - | N | Y | Y |
| Amount positive? | Y | - | - | N | Y |
| Amount ≤ balance? | Y | - | - | - | N |
| **Action** |
| Payment succeeds | X | | | | |
| Error: Account frozen/closed | | X | | | |
| Error: Invalid payee | | | X | | |
| Error: Amount must be positive | | | | X | |
| Error: Insufficient funds | | | | | X |

**Required-coverage checklist**: 3 decision tables (transfer validation, fee
processing, bill payment validation), all rules mapped to exactly one action,
condition precedence documented where checks short-circuit each other.

---

## 4. State Transition Testing

### State Transition Diagram

```
                    Balance restored >= minimum
        +------------------------------------------+
        |                                            |
        v                                            |
   [Suspended] <----(transfer drops balance < min)---[Active]
        |                                                |  |
        | close_account()                close_account() |  | freeze()
        v                                                v  v
   [Closed] <---------------------------------------[Frozen]
        ^                                                |
        |                    unfreeze() (balance >= min) |
        |                    +-----------------------------+ -> [Active]
        |                    | unfreeze() (balance < min)
        |                    +-----------------------------+ -> [Suspended]
        |
        +----------------------- close_account() (from any non-Closed state)

  [Closed] --(any event)--> [Closed]   (terminal: no transitions leave Closed)
```

### State Transition Table

| Current State | Event | Next State | Action/Output |
| -------------- | ----- | ---------- | --------------- |
| Active | Transfer drops balance below minimum | Suspended | Balance updated, state flips to Suspended |
| Active | `freeze()` | Frozen | All transactions blocked |
| Active | `close()` | Closed | Account terminated |
| Suspended | `deposit()` restores balance ≥ minimum | Active | Restrictions removed |
| Suspended | `freeze()` | Frozen | Transactions blocked (can still freeze a suspended account) |
| Suspended | `close()` | Closed | Account terminated |
| Frozen | `unfreeze()`, balance ≥ minimum | Active | Full access restored |
| Frozen | `unfreeze()`, balance < minimum | Suspended | Restrictions partially restored, still below minimum |
| Frozen | `close()` | Closed | Account terminated |
| Closed | Any event (`transfer`, `deposit`, `freeze`, `unfreeze`, `close`) | Closed | Error: account is closed / already closed; no state change |

### State Transition Test Cases

| Test ID | Start State | Event | Expected End State | Validation |
| ------- | ----------- | ----- | -------------------- | ----------- |
| ST1 | Active (Savings, $150) | Transfer $60 (balance → $90, below $100 min) | Suspended | `result["success"] is True`, `account.state == "Suspended"` |
| ST2 | Suspended (Savings, $50) | `deposit(100)` (balance → $150) | Active | `account.state == "Active"` |
| ST3 | Active | `freeze()` | Frozen | `account.state == "Frozen"`, subsequent transfer rejected |
| ST4 | Frozen (balance ≥ min) | `unfreeze()` | Active | `account.state == "Active"` |
| ST5 | Frozen (balance < min) | `unfreeze()` | Suspended | `account.state == "Suspended"` (not silently reset to Active) |
| ST6 | Active | `close()` | Closed | `account.state == "Closed"` |
| ST7 | Suspended | `close()` | Closed | `account.state == "Closed"` from a non-Active state |
| ST8 | Closed | `transfer()` | Closed (no change) | `result["success"] is False`, state unchanged, error mentions closed |
| ST9 | Closed | `close()` again | Closed (no change) | `result["success"] is False`, error "already closed" (idempotent, not a crash) |
| ST10 | Frozen | `freeze()` again | Frozen (no change) | `result["success"] is True`, state stays Frozen (re-freezing is a harmless no-op, not an error) |

**Required coverage**: complete diagram, transition table covering all valid
transitions plus the Closed sink state, and 10 test cases (exceeds the
required minimum of 8), including two "no-op on invalid trigger" cases (ST8,
ST9) and the ambiguous Frozen→unfreeze() case that depends on current balance
(ST4 vs. ST5), which is the transition most likely to be implemented
incorrectly (naively resetting straight to Active without re-checking the
balance).
