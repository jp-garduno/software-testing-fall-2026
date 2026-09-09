# Part 5: Risk Analysis and Test Prioritization

## 5.1 Risk Matrix

Ten risks, classified by likelihood and impact. Priority mixes the two: something unlikely still gets P0 if you cannot undo the damage once it happens.

| **Risk**                                                                 | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy**                                                                                                                                                         |
| ------------------------------------------------------------------------ | -------------- | ---------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A student can read another student's grades through a direct API request | Medium         | Critical   | P0           | Authorization tests per role on every endpoint; automated scan for insecure direct object references; mandatory review of any change touching access control                    |
| Incorrect final grade due to a defect in weighting or rounding           | Medium         | Critical   | P0           | 100% branch coverage plus mutation testing on the calculation module; recomputation of historical records against stored values; audit trail on every grade change              |
| Two students enrolled in the same last available seat                    | High           | High       | P0           | Concurrency integration tests against a real database; explicit locking strategy; enforcement at the database constraint level, not only in application code                    |
| Payment charged without the payment record being stored                  | Low            | Critical   | P0           | Transactional integration tests with induced failures; idempotent webhook handling; nightly reconciliation against the gateway                                                  |
| System unavailable during the registration window                        | Medium         | Critical   | P0           | Load testing at three times expected peak before each term; queueing with graceful degradation; rehearsed incident runbook                                                      |
| Regression in tuition calculation after adding a scholarship type        | High           | High       | P1           | Full regression suite on the finance module in CI; golden-file tests comparing calculated amounts against approved reference cases                                              |
| Registration flow unusable with a screen reader or keyboard only         | Medium         | High       | P1           | axe-core in the pipeline; manual keyboard and screen-reader testing of critical flows; accessibility as a release blocker                                                       |
| Data loss or corruption during term-opening migration                    | Low            | Critical   | P1           | Migration rehearsal against a production copy; verified backups with a tested restore procedure; row counts and checksums before and after                                      |
| Notifications not delivered for payment or submission deadlines          | Medium         | Medium     | P2           | Integration tests on the job queue including retries and dead-letter handling; delivery-rate monitoring; deadlines always visible in the interface and not only by notification |
| Interface unusable on low-end mobile devices                             | Medium         | Medium     | P2           | Device matrix testing on real hardware; performance budget for the mobile bundle; responsive layout verified down to 360px                                                      |

**Likelihood**: Low / Medium / High
**Impact**: Low / Medium / High / Critical
**Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

## 5.2 Testing Priority Order

The order follows two rules: irreversible damage before recoverable damage, and defects that affect everyone at once before defects that affect one person at a time.

1. **Authorization and access control testing.** First because it is the only risk whose damage cannot be undone by a fix — once data has been read, it has been read.
2. **Grade and tuition calculation testing.** Wrong numbers propagate into legal documents and are usually discovered late, by the person harmed.
3. **Concurrency and data integrity testing on registration.** Enforced at the database level and verified against a real instance, because capacity is finite and a duplicate enrollment must be resolved manually.
4. **Payment integration testing, including failure paths.** Money in dispute is expensive in staff time and in institutional trust, and the failure paths are where the defects live.
5. **Load testing of the registration window.** Scheduled before each term. Cannot be deferred, because the event has a fixed date and no second chance.
6. **Regression testing of academic and financial rules.** Runs continuously in CI; the protection against breaking what already worked.
7. **Accessibility testing of critical flows.** A release blocker: an inaccessible enrollment screen blocks a student from an obligatory process.
8. **End-to-end testing of complete flows.** Confirms the parts work together as a coherent whole rather than only in isolation.
9. **Usability testing with real students.** Measures whether the system is usable, which no functional suite can answer.
10. **Compatibility, localization and exploratory testing.** Lower priority not because they are unimportant, but because their defects are visible, reported quickly and worked around while a fix ships.
