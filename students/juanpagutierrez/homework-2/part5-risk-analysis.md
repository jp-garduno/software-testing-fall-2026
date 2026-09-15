# Part 5: Risk Analysis & Test Prioritization

## 5.1 Risk Matrix

| **Risk**                                                     | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy**                                                                                     |
| -------------------------------------------------------------- | --------------- | ---------- | ------------- | -------------------------------------------------------------------------------------------------------------- |
| Incorrect balance/budget calculation shown to user              | Medium          | Critical   | P0            | Extensive unit tests on calculation logic; property-based tests for rounding and edge-case amounts             |
| Bank credentials or transaction data exposed in a breach         | Low             | Critical   | P0            | Security testing, encryption at rest/in transit, regular third-party penetration testing                       |
| Duplicate or missing transactions after a failed sync            | Medium          | High       | P1            | Integration tests simulating sync interruptions; idempotency checks on the sync service                        |
| User can access another user's financial data (authorization bug)| Low             | Critical   | P0            | Authorization/IDOR test cases on every endpoint that takes a resource ID; automated security scans in CI       |
| Bill reminder fails to send, causing a real late fee             | Medium          | High       | P1            | Integration tests on the scheduler/notification pipeline; monitoring and alerting on failed notification jobs  |
| Currency conversion uses the wrong or stale exchange rate        | Medium          | High       | P1            | Unit tests pinning conversion to the transaction-date rate; regression tests after any conversion logic change |
| App becomes slow or unresponsive during start-of-month traffic   | Medium          | Medium     | P2            | Load/performance testing simulating peak usage patterns before each release                                    |
| Poor onboarding UX causes new users to abandon before first budget| High            | Medium     | P2            | Usability testing with representative first-time users; track onboarding completion rate as a release gate     |

**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High / Critical
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

## 5.2 Testing Priority Order

Based on the risk matrix above, testing activities are prioritized as follows:

1. **Data integrity and calculation testing** - Verify budget totals, balances, and currency conversion are always mathematically correct, since this risk is both likely and catastrophic if wrong.
2. **Security and authorization testing** - Verify encryption of sensitive data and that no user can access another user's data, given the critical impact of any breach even at low likelihood.
3. **Bank sync reliability testing** - Verify transaction sync is idempotent and recovers cleanly from interruptions, to prevent duplicate or missing transactions.
4. **Notification pipeline testing** - Verify bill reminders are scheduled and delivered reliably, since a failure has a direct real-world financial consequence for the user.
5. **Performance/load testing** - Verify the system holds up under predictable peak-usage patterns (start of month, payday).
6. **Usability testing of onboarding** - Verify first-time users can successfully link an account and create a first budget, since this determines whether users ever reach the app's core value.
7. **Compatibility and accessibility testing** - Verify consistent behavior across devices/browsers and for users relying on assistive technology, as broader but lower-severity risks.
