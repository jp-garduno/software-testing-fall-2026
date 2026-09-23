## State Transition Testing

### State Transition Diagram

                     ┌────────────────────────────────────────────┐
                     │                                            │
                     ▼                                            │
        (Balance restored above minimum)                          │
                     │                                            │
    ┌───────────►[Suspended]                                      │
    │                │    │                                       │
    │  (Balance <    │    │ (Close request)                       │
    │   minimum)     │    │                                       │
    │                │    ▼                                       │
[Active] ──────────► │  [Closed] ◄─────────────────────┐          │
    │  │             │    ▲                            │          │
    │  │             │    │ (Close request)            │          │
    │  │             │    │                            │          │
    │  │ (Freeze     │    │                            │          │
    │  │  request /  │    │                            │          │
    │  │  fraud)     │    │                            │          │
    │  ▼             │    │                            │          │
    │[Frozen]────────┘    │                            │          │
    │  │                  │                            │          │
    │  └─────────(Unfreeze approved)───────────────────┘          │
    │                                                             │
    └──(Close request)────────────────────────────────────────────┘

[Closed] --(Any event)--> [Closed]   (terminal state, no exit)

### State Transition Text

'Active' → 'Suspended': When balance under minimum
'Active' → 'Frozen': Client request or fraud
'Active' → 'Closed': Closing request
'Suspended' → 'Active': When deposit restores balance over minimum
'Suspended' → 'Closed': Closing request
'Frozen' → 'Active': Unfreeze approval
'Frozen' → 'Closed': Closing request
'Closed' → 'Closed': Any event in a closed account is invalid

### State Transition Table

| Current State  | Event                              | Next State   | Action/Output             |
| -------------- | ---------------------------------- | ------------ | ------------------------- |
| Active         | Balance drops below minimum        | Suspended    | Send warning notification |
| Active         | Freeze request (customer/fraud)    | Frozen       | Block all transactions    |
| Active         | Close request                      | Closed       | Final statement generated |
| Suspended      | Deposit restores balance           | Active       | Remove restrictions       |
| Suspended      | Close request                      | Closed       | Final statement generated |
| Frozen         | Unfreeze approved                  | Active       | Restore full access       |
| Frozen         | Close request                      | Closed       | Final statement generated |
| Closed         | Any event (transfer, freeze, etc.) | Closed       | Error: Account closed     |

### State Transition Test Cases

| Test ID | Start State | Event                                  | Expected End State | Validation                                   |
| ------- | ----------- | -------------------------------------- | ------------------ | -------------------------------------------- |
| ST1     | Active      | Transfer causes balance < minimum      | Suspended          | Warning shown, status = Suspended            |
| ST2     | Suspended   | Deposit restores balance above minimum | Active             | Status = Active, restrictions removed        |
| ST3     | Active      | Customer requests freeze               | Frozen             | All transactions blocked                     |
| ST4     | Frozen      | Customer requests unfreeze (approved)  | Active             | Full access restored                         |
| ST5     | Active      | Customer requests close                | Closed             | Final statement generated                    |
| ST6     | Suspended   | Customer requests close                | Closed             | Final statement generated                    |
| ST7     | Frozen      | Customer requests close                | Closed             | Final statement generated                    |
| ST8     | Closed      | Attempt to transfer funds              | Closed (no change) | Error: Account closed                        |
| ST9     | Closed      | Attempt to reopen account              | Closed (no change) | Error: Account closed, cannot be reopened    |
| ST10    | Frozen      | Attempt to transfer while frozen       | Frozen (no change) | Error: Account is frozen, transaction denied |



#### Coverage Summary

| Element                                          | Coverage                              |
| ------------------------------------------------ | ------------------------------------- |
| Status                                           | 4 (Active, Suspended, Frozen, Closed) |
| Valid Transition                                 | 7                                     |
| Invalid Transitions                              | 3 (ST8, ST9, ST10)                    |
| Testing cases                                    | 10                                    |