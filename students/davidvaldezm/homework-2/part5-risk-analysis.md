# Part 5: Risk Analysis and Test Prioritization

## 5.1 Risk Matrix

Priority combines likelihood and impact, with security, privacy, and silent financial-integrity failures conservatively elevated. Each mitigation includes both prevention and detection because no control is perfect.

| **Risk** | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy** |
| --- | --- | --- | --- | --- |
| Cross-user access caused by broken object-level authorization | Medium | Critical | P0 | Centralize ownership checks; run negative API tests for every resource; perform threat modeling, SAST/DAST, and penetration testing; alert on anomalous access patterns. |
| Missing or duplicated transactions after provider retries | High | Critical | P0 | Use idempotency keys and database uniqueness constraints; inject timeouts at every sync stage; reconcile provider and local counts/balances; monitor duplicate rate. |
| Incorrect balance or budget total due to signs, rounding, time zones, or month boundaries | Medium | Critical | P0 | Use decimal arithmetic, boundary and property-based unit tests, versioned golden datasets, cross-report invariants, and production reconciliation metrics. |
| Sensitive data appears in logs, analytics, exports, or support tools | Medium | Critical | P0 | Enforce structured redaction and data minimization; scan all telemetry channels; test export authorization and expiration; audit support roles and retained artifacts. |
| Account takeover through recovery, session, or MFA weakness | Medium | Critical | P0 | Test rate limits, enumeration resistance, token expiry/revocation, device history, step-up authentication, secure recovery, and suspicious-login alerting. |
| Database migration corrupts ownership, precision, timestamps, or history | Low | Critical | P1 | Rehearse forward and rollback paths on production-shaped synthetic data; compare checksums/invariants; back up first; canary release and halt on reconciliation drift. |
| Bank provider outage or rate limiting leaves data stale without clear warning | High | High | P1 | Contract and fault-injection tests; bounded backoff with jitter; show last-success time and provider status; alert operations; test replay after recovery. |
| Account deletion or consent revocation fails in a downstream store | Medium | High | P1 | Maintain a data inventory; test orchestration across primary DB, cache, index, exports, analytics, and provider tokens; collect deletion evidence and monitor overdue jobs. |
| Dashboard becomes unavailable or misleading under peak load | Medium | High | P1 | Load/stress/soak test production-like environments; define latency/error objectives; capacity alerts, graceful degradation, and post-test integrity reconciliation. |
| Inaccessible charts, forms, or error recovery exclude users | Medium | High | P1 | Combine axe checks with keyboard, zoom, contrast, screen-reader, and moderated assistive-technology testing; require text alternatives for visual data. |
| Malicious CSV input or export formula compromises a user's computer | Medium | High | P1 | Validate file type/size/encoding; neutralize formula prefixes; isolate parsing; fuzz importers; malware-scan stored files; test safe export round trips. |
| Ambiguous labels cause users to misinterpret available money | Medium | High | P2 | Prototype wording; moderated comprehension tests; distinguish posted/pending values; avoid color-only meaning; monitor corrections and support contacts. |
| Notification is late, repeated, or sent to the wrong channel | Medium | Medium | P2 | Test preference and ownership rules, deduplication, retry windows, time zones, quiet hours, provider contracts, and delivery audit trails. |
| Unsupported browser or mobile version renders a noncritical view incorrectly | Low | Medium | P3 | Publish a support matrix; automate representative cross-browser/device checks; use analytics to update coverage; provide graceful fallback. |

## Risk Scoring Rationale

- **P0 (Critical)**: Could expose financial data, compromise an account, or silently change financial truth. These tests gate every release and relevant change.
- **P1 (High)**: Could make a critical capability unavailable, violate a data-lifecycle promise, or exclude a substantial user group. These tests gate release candidates.
- **P2 (Medium)**: Meaningfully harms comprehension or communication but has a contained workaround. These tests run before release and in focused regression.
- **P3 (Low)**: Limited impact, low likelihood, and a practical workaround. These tests are scheduled according to the compatibility matrix and change scope.

## 5.2 Testing Priority Order

1. **Authorization and account security**: verify tenant isolation, recovery, MFA, session expiry/revocation, export access, rate limits, and audit events before exposing any financial endpoint.
2. **Financial calculation and data invariants**: validate signs, decimal precision, dates, balances, budgets, splits, imports, and report agreement with unit/property tests and golden datasets.
3. **Synchronization idempotency and recovery**: exercise pagination, overlapping webhooks, retries, worker crashes, provider outages, and reconciliation under deterministic fault injection.
4. **Privacy lifecycle**: test minimization and redaction, consent revocation, token removal, portable export, retention, and deletion across every downstream store.
5. **Migration and backward compatibility**: rehearse schema/data migrations and rollback against production-shaped data before deployment.
6. **Critical end-to-end journeys**: automate sign-in, bank linking, import, budgeting, alerting, reauthorization, export, deletion, and sign-out across supported clients.
7. **Performance and resilience**: test expected peak, stress, soak, queue recovery, and graceful degradation, followed by integrity reconciliation.
8. **Accessibility and usability**: validate keyboard/screen-reader operation and measure whether representative users understand and recover from critical states.
9. **Compatibility and localization**: exercise the risk-based browser/device/locale/time-zone matrix with special attention to numeric and date presentation.
10. **Lower-risk notification and presentation regression**: cover preferences, delivery timing, responsive layouts, and noncritical visual variations.

## Entry, Exit, and Residual-Risk Rules

Testing starts when requirements have examples, the build is deployable, test data is approved, and dependencies can be controlled or simulated. A release is blocked by any open P0 defect, unexplained reconciliation difference, critical/high security finding, failed critical privacy or accessibility journey, or unmet performance objective. P1 exceptions require an owner, user impact, workaround, monitoring signal, target date, and explicit approval from product and the relevant security/privacy/operations stakeholder. P2/P3 defects may be scheduled when documented and observable.

## Bonus: Risk-to-Test Traceability

| **Risk Area** | **Primary Level** | **Primary Test Types** | **Release Evidence** |
| --- | --- | --- | --- |
| Authorization and takeover | Integration / System | Security, Functional, Regression | Negative tenant matrix, token suite, security report, zero unresolved high findings |
| Calculation integrity | Unit / Integration | Functional, Data Integrity, Regression | Property-test results, golden dataset checksum, invariant report |
| Provider synchronization | Integration / System | Reliability, Performance, Functional | Fault-injection results, duplicate/reconciliation metrics, replay evidence |
| Privacy lifecycle | System / Acceptance | Privacy, Security, Usability | Data-flow checklist, deletion evidence, stakeholder sign-off |
| Accessibility and comprehension | System / Acceptance | Accessibility, Usability, Compatibility | Automated scan, manual AT record, participant task/comprehension results |

This traceability prevents a high-priority risk from being represented only by a document or a single happy-path test. It also makes release decisions auditable: reviewers can see which evidence supports each claim and which residual risks remain.
