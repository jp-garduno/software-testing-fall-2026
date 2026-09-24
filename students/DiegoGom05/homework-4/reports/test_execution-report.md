## 3.1 Test Execution Summary

- **Date**: 2026-09-22
- **Test Framework**: Jest (Node.js)
- **Total Tests**: 25
- **Passed**: 25
- **Failed**: 0
- **Skipped**: 0
- **Duration**: 0.84s

### Coverage Summary

| Metric                 | Percentage | Covered / Total |
| :--------------------- | :--------- | :-------------- |
| **Line Coverage**      | 100%       | 52 / 52         |
| **Branch Coverage**    | 100%       | 34 / 34         |
| **Function Coverage**  | 100%       | 6 / 6           |
| **Statement Coverage** | 100%       | 52 / 52         |

---

## 3.2 Results by Technique

### Equivalence Partitioning (7 tests)

- ✅ `EP1_TA: Valid transfer amount within limits succeeds`
- ✅ `EP2_TA: Zero transfer amount fails`
- ✅ `EP3_TA: Negative transfer amount fails`
- ✅ `EP4_TA: Transfer exceeding daily limit fails`
- ✅ `EP5_TA: Transfer exceeding current balance fails`
- ✅ `EP4_AT: Unsupported account type fails during transfer`
- ✅ `EP2_PI: Unregistered payee ID fails bill payment`

**Defects Found**: During initial test execution, `EP5_TA` failed because the daily limit check was evaluated before the insufficient funds check. Adjusting the validation order in `bankingSystem.js` resolved the issue, ensuring funds verification takes precedence.

---

### Boundary Value Analysis (6 tests)

- ✅ `BV1: Transfer below minimum ($0.00) fails`
- ✅ `BV2: Transfer exactly at minimum ($0.01) succeeds`
- ✅ `BV3: Transfer just below daily limit ($4,999.99) succeeds`
- ✅ `BV4: Transfer exactly at daily limit ($5,000.00) succeeds`
- ✅ `BV5: Transfer just above daily limit ($5,000.01) fails`
- ✅ `BV4_P: Premium account transfer at $25,000.00 limit succeeds`

**Defects Found**: None. Floating-point comparisons ($0.01, $4,999.99, $5,000.01) were evaluated without precision drift issues using `parseFloat`.

---

### Decision Tables (6 tests)

- ✅ `DT1_Rule1: Transfer succeeds when funds available, within limit, and account active`
- ✅ `DT1_Rule2: Transfer fails when account is frozen despite having funds and being within limit`
- ✅ `DT1_Rule5: Transfer fails when funds are insufficient despite active account and within limit`
- ✅ `DT2_Rule2: Monthly fee charged when Savings balance <= $100 threshold`
- ✅ `DT2_Rule5: Monthly fee waived for Premium accounts regardless of balance`
- ✅ `DT3_Rule4: Bill payment fails when payee service is unavailable`

**Defects Found**: None. Multi-condition business logic (fee waiver logic across tiers and account status guards) executed properly according to specification.

---

### State Transitions (6 tests)

- ✅ `ST1: Active to Suspended transition when balance drops below $100`
- ✅ `ST2: Suspended to Active transition after deposit restores balance above $100`
- ✅ `ST3: Active to Frozen transition via freeze request`
- ✅ `ST4: Frozen to Active transition via unfreeze approval`
- ✅ `ST7: Outbound transfer attempt blocked while in Frozen state`
- ✅ `ST8: Any operation fails when account is in Closed state`

**Defects Found**: None. Terminal (`Closed`) and restricted (`Frozen`, `Suspended`) states correctly blocked unauthorized transaction operations.

---

## 3.4 Coverage Analysis

### Which code paths are covered?

- **Input Parameter & Type Validation**:
  - Processing of valid vs. invalid account types (`Savings`, `Checking`, `Premium`, and unsupported types).
  - Validation of transaction amounts (zero, negative numbers, standard valid floats, and high-value amounts).
  - Payee ID format and existence checks during bill payments.
- **Business Logic & Limit Checks**:
  - Account tier dynamic daily limit evaluation (`Savings`: $2,000, `Checking`: $5,000, `Premium`: $25,000).
  - Pre-transaction balance verification (`parsedAmount > balance`).
  - Fee calculation and dynamic fee waiver logic based on account balance thresholds (e.g., $100 balance threshold) and account tiers (`Premium` vs. `Savings`/`Checking`).
- **State Lifecycle & Operational Guards**:
  - Automatic balance-driven state updates (transitioning from `Active` to `Suspended` when balance falls below $100, and back to `Active` upon sufficient deposit).
  - Manual state updates (`Active` to `Frozen`, and `Frozen` to `Active`).
  - Early-return operational guards blocking transactions on `Frozen` or `Closed` accounts.

---

### Which code paths are not covered and why?

- **None (0% uncovered paths)**:
  - The executed test suite achieves **100% Line, Branch, Statement, and Function coverage** on `bankingSystem.js`.
  - Every logical branch (`if`/`else` condition), error handling return statement, state transition branch, and utility function was fully traversed during execution.

---

### How does coverage differ by technique?

| Technique                         | Primary Code Paths Covered                                                             | Analytical Focus & Impact                                                                                                                                                                                                   |
| :-------------------------------- | :------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Equivalence Partitioning (EP)** | Core method entry points, input parser lines, and primary error return branches.       | Exercises general valid and invalid data domains (e.g., valid positive floats vs. negative numbers or unsupported strings), confirming that broad classes of inputs route to their respective success/error handlers.       |
| **Boundary Value Analysis (BVA)** | Exact conditional branch comparison operations (`>`, `<`, `>=`, `<=`).                 | Targets boundary conditions specifically (e.g., $0.00, $0.01, $4,999.99, $5,000.00, $5,000.01). Guarantees that off-by-one comparison errors do not exist around daily limits and minimum transaction amounts.              |
| **Decision Tables (DT)**          | Compound conditional ladders and multi-variable business rules.                        | Covers lines where multiple logical flags interact simultaneously (e.g., verifying `accountType === 'Premium'` OR `balance > 100` before applying monthly fees, and blocking transactions when `payeeAvailable === false`). |
| **State Transitions (ST)**        | State assignment statements, implicit/explicit state setters, and status guard checks. | Covers lifecycle execution flows, ensuring operations verify account state (`Active`, `Suspended`, `Frozen`, `Closed`) before processing and trigger appropriate state changes post-transaction.                            |
