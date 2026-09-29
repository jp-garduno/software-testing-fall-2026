# Test Design Document — SecureBank Online Banking System

**Student:** Luis Cacho (`LuisCacho-py`)
**Module:** 4 — Black Box Testing
**System Under Test:** SecureBank Online Banking Platform

---

## Overview

This document presents the complete black box test design for the SecureBank
Online Banking System using four complementary techniques:

1. Equivalence Partitioning (EP)
2. Boundary Value Analysis (BVA)
3. Decision Tables (DT)
4. State Transition Testing (ST)

---

## 1.1 Equivalence Partitioning

Equivalence partitioning divides input domains into classes where members
are expected to behave identically. One representative value is chosen per class.

### Input: Transfer Amount

| Partition ID | Description                  | Type    | Representative Value | Expected Result                        |
|-------------|------------------------------|---------|----------------------|----------------------------------------|
| EP-01       | Valid amount within limits   | Valid   | $500.00              | Transfer succeeds                      |
| EP-02       | Zero amount                  | Invalid | $0.00                | Error: Amount must be positive         |
| EP-03       | Negative amount              | Invalid | -$100.00             | Error: Amount must be positive         |
| EP-04       | Amount exceeds daily limit   | Invalid | $100,000.00          | Error: Exceeds daily limit             |
| EP-05       | Amount exceeds balance       | Invalid | Balance + $1.00      | Error: Insufficient funds              |

### Input: Account Type

| Partition ID | Description              | Type    | Representative Value | Expected Result                    |
|-------------|--------------------------|---------|----------------------|------------------------------------|
| EP-06       | Savings account          | Valid   | "Savings"            | Account created, limit = $2,000    |
| EP-07       | Checking account         | Valid   | "Checking"           | Account created, limit = $5,000    |
| EP-08       | Premium account          | Valid   | "Premium"            | Account created, limit = $50,000   |
| EP-09       | Invalid / unknown type   | Invalid | "Gold"               | ValueError raised                  |

### Input: Account Balance (initial balance vs. minimum)

| Partition ID | Description                       | Type    | Representative Value | Expected Result             |
|-------------|-----------------------------------|---------|----------------------|-----------------------------|
| EP-10       | Balance well above minimum        | Valid   | $500.00 (Savings)    | State = Active              |
| EP-11       | Balance below minimum (Savings)   | Invalid | $50.00 (Savings)     | State = Suspended           |
| EP-12       | Zero balance (Checking, $0 min)   | Valid   | $0.00 (Checking)     | State = Active              |

### Input: Payee (bill payment)

| Partition ID | Description               | Type    | Representative Value | Expected Result                |
|-------------|---------------------------|---------|----------------------|--------------------------------|
| EP-13       | Valid payee name          | Valid   | "Electric Company"   | Bill payment succeeds          |
| EP-14       | Empty string payee        | Invalid | ""                   | Error: Payee name is required  |
| EP-15       | Whitespace-only payee     | Invalid | "   "                | Error: Payee name is required  |

### Input: Date Range (transaction history filter)

| Partition ID | Description                      | Type    | Representative Value         | Expected Result                              |
|-------------|----------------------------------|---------|------------------------------|----------------------------------------------|
| EP-16       | No date filter (all history)     | Valid   | None / None                  | All transactions returned                    |
| EP-17       | Valid range (start ≤ end ≤ today)| Valid   | today / today                | Filtered transactions returned               |
| EP-18       | Invalid range (start > end)      | Invalid | tomorrow / yesterday         | Error: Start date must be before end date    |

---

## 1.2 Boundary Value Analysis

BVA focuses on values at and just around boundaries where behavior changes.
For each boundary, we test: below min, at min, just below limit, at limit,
just above limit, and far above limit.

### Boundary Group 1: Transfer Amount — Checking Account ($5,000 daily limit)

| Test ID | Boundary          | Test Value   | Expected Result                        |
|---------|-------------------|--------------|----------------------------------------|
| BV-01   | Below minimum     | $0.00        | Error: Amount must be positive         |
| BV-02   | Minimum valid     | $0.01        | Transfer succeeds                      |
| BV-03   | Just below limit  | $4,999.99    | Transfer succeeds                      |
| BV-04   | At limit          | $5,000.00    | Transfer succeeds                      |
| BV-05   | Just above limit  | $5,000.01    | Error: Exceeds daily limit             |
| BV-06   | Far above limit   | $10,000.00   | Error: Exceeds daily limit             |

### Boundary Group 2: Transfer Amount — Savings Account ($2,000 daily limit)

| Test ID | Boundary          | Test Value   | Expected Result                        |
|---------|-------------------|--------------|----------------------------------------|
| BV-07   | At limit          | $2,000.00    | Transfer succeeds                      |
| BV-08   | Just above limit  | $2,000.01    | Error: Exceeds daily limit             |

### Boundary Group 3: Account Balance vs. Minimum (Savings — $100 minimum)

| Test ID | Boundary               | Test Value  | Expected Result   |
|---------|------------------------|-------------|-------------------|
| BV-09   | Just above minimum     | $100.01     | State = Active    |
| BV-10   | At minimum             | $100.00     | State = Active    |
| BV-11   | Just below minimum     | $99.99      | State = Suspended |
| BV-12   | Zero (far below min)   | $0.00       | State = Suspended |

### Boundary Group 4: Fee Waiver Threshold (Savings — $1,000 threshold)

| Test ID | Boundary                 | Test Value  | Expected Result     |
|---------|--------------------------|-------------|---------------------|
| BV-13   | Just above threshold     | $1,000.01   | Fee waived ($0)     |
| BV-14   | At threshold (not >)     | $1,000.00   | Fee charged ($5.00) |
| BV-15   | Just below threshold     | $999.99     | Fee charged ($5.00) |

### Boundary Group 5: Cumulative Daily Limit (Checking — $5,000)

| Test ID | Boundary                              | Test Values             | Expected Result             |
|---------|---------------------------------------|-------------------------|-----------------------------|
| BV-16   | Cumulative exactly at limit           | $3,000 + $2,000         | Both succeed                |
| BV-17   | Cumulative just above limit           | $4,999 + $2.00          | Second transfer rejected    |

---

## 1.3 Decision Tables

Decision tables capture combinations of conditions and their resulting actions.

### Decision Table 1: Transfer Validation

| Condition               | Rule 1 | Rule 2 | Rule 3 | Rule 4 | Rule 5 | Rule 6 | Rule 7 | Rule 8 |
|-------------------------|--------|--------|--------|--------|--------|--------|--------|--------|
| Sufficient funds?       | Y      | Y      | Y      | Y      | N      | N      | N      | N      |
| Within daily limit?     | Y      | Y      | N      | N      | Y      | Y      | N      | N      |
| Account Active?         | Y      | N      | Y      | N      | Y      | N      | Y      | N      |
| **Action**              |        |        |        |        |        |        |        |        |
| Transfer succeeds       | ✓      |        |        |        |        |        |        |        |
| Error: Account frozen   |        | ✓      |        | ✓      |        | ✓      |        | ✓      |
| Error: Exceeds limit    |        |        | ✓      |        |        |        |        |        |
| Error: Insufficient     |        |        |        |        | ✓      |        | ✓      |        |
| Error: Account closed   |        |        |        |        |        |        |        | ✓*     |

*Rule 8 triggers "Closed" error (Closed is a subset of "not Active").

### Decision Table 2: Monthly Fee Processing

| Condition                    | Rule 1  | Rule 2  | Rule 3   | Rule 4   | Rule 5  |
|------------------------------|---------|---------|----------|----------|---------|
| Account type                 | Savings | Savings | Checking | Checking | Premium |
| Balance > waiver threshold?  | Y       | N       | Y        | N        | —       |
| **Action**                   |         |         |          |          |         |
| Fee waived ($0)              | ✓       |         | ✓        |          | ✓       |
| Charge $5 fee                |         | ✓       |          |          |         |
| Charge $10 fee               |         |         |          | ✓        |         |

### Decision Table 3: Bill Payment Validation

| Condition             | Rule 1 | Rule 2 | Rule 3 | Rule 4 |
|-----------------------|--------|--------|--------|--------|
| Valid payee?          | Y      | Y      | Y      | N      |
| Amount > 0?           | Y      | Y      | N      | —      |
| Sufficient funds?     | Y      | N      | —      | —      |
| **Action**            |        |        |        |        |
| Payment succeeds      | ✓      |        |        |        |
| Error: Insufficient   |        | ✓      |        |        |
| Error: Amount invalid |        |        | ✓      |        |
| Error: Payee required |        |        |        | ✓      |

---

## 1.4 State Transition Testing

### State Transition Diagram

```
                     ┌─────────────────────────────────┐
                     │                                  │
          ┌──────────▼──────────┐   Balance < minimum   │
          │        ACTIVE        ├───────────────────────►──────────────┐
          └───┬────────┬────────┘                                       │
              │        │                                                 ▼
     Freeze   │        │ Close                              ┌─────────────────────┐
    request   │        │                                    │      SUSPENDED       │
              │        │                                    └──┬──────────────┬───┘
              ▼        ▼                                       │              │
          ┌────────┐ ┌────────┐     Deposit restores          │ Close        │
          │ FROZEN │ │ CLOSED │◄──────────────────────────────┘              │
          └───┬────┘ └────────┘                                              │
              │          ▲                                                   │
    Unfreeze  │          │ Close                                             │
              └──────────┘◄──────────────────────────────────────────────────┘
```

Textual representation:
```
[Active]    --(Balance < min)--> [Suspended]
[Active]    --(Freeze request)--> [Frozen]
[Active]    --(Close request)-->  [Closed]
[Suspended] --(Deposit restores balance)--> [Active]
[Suspended] --(Close request)-->  [Closed]
[Frozen]    --(Unfreeze approved)--> [Active]
[Frozen]    --(Close request)-->  [Closed]
[Closed]    --(Any event)-->      [Closed]  (terminal state — error returned)
```

### State Transition Table

| Current State | Event                          | Next State  | Action / Output                        |
|---------------|--------------------------------|-------------|----------------------------------------|
| Active        | Transfer causes balance < min  | Suspended   | Warning; transactions still logged     |
| Active        | Freeze request                 | Frozen      | All transactions blocked               |
| Active        | Close request                  | Closed      | Final statement generated              |
| Active        | Normal transfer (balance ≥ min)| Active      | No state change                        |
| Suspended     | Deposit restores balance ≥ min | Active      | Full access restored                   |
| Suspended     | Deposit still below min        | Suspended   | No state change                        |
| Suspended     | Close request                  | Closed      | Final statement generated              |
| Frozen        | Unfreeze approved              | Active      | Full access restored                   |
| Frozen        | Close request                  | Closed      | Final statement generated              |
| Closed        | Any event                      | Closed      | Error: Account is Closed (no action)   |

### State Transition Test Cases

| Test ID | Start State | Event                               | Expected End State | Validation                                   |
|---------|-------------|-------------------------------------|--------------------|----------------------------------------------|
| ST-01   | Active      | Transfer drops balance below $100   | Suspended          | state == Suspended, transfer still succeeds  |
| ST-02   | Active      | freeze() call                       | Frozen             | state == Frozen, transfers rejected          |
| ST-03   | Active      | close() call                        | Closed             | state == Closed, no further ops              |
| ST-04   | Active      | Transfer keeps balance above min    | Active             | state unchanged == Active                    |
| ST-05   | Suspended   | deposit() restores to ≥ $100        | Active             | state == Active, transfers enabled           |
| ST-06   | Suspended   | close() call                        | Closed             | state == Closed                              |
| ST-07   | Suspended   | transfer() attempt                  | Suspended          | Fails: insufficient funds (state not Frozen) |
| ST-08   | Suspended   | deposit() still below $100          | Suspended          | state unchanged == Suspended                 |
| ST-09   | Frozen      | unfreeze() call                     | Active             | state == Active, operations restored         |
| ST-10   | Frozen      | close() call                        | Closed             | state == Closed                              |
| ST-11   | Frozen      | transfer() attempt                  | Frozen             | Fails: Account is Frozen                     |
| ST-12   | Frozen      | pay_bill() attempt                  | Frozen             | Fails: Account is Frozen                     |
| ST-13   | Closed      | transfer() attempt                  | Closed             | Fails: Account is Closed                     |
| ST-14   | Closed      | deposit() attempt                   | Closed             | Fails: Account is Closed                     |
| ST-15   | Closed      | close() call again                  | Closed             | Fails: Already Closed                        |
| ST-16   | Closed      | freeze() call                       | Closed             | Fails: Cannot freeze Closed account          |
| ST-17   | Active→Frozen→Active | Full freeze/unfreeze cycle | Active            | Fully operational after unfreeze             |
| ST-18   | Active→Suspended→Active | Full low-balance cycle   | Active            | Fully operational after deposit              |
| ST-19   | Active      | Monthly fee with insufficient funds | Suspended          | Fee charged, account suspended               |
