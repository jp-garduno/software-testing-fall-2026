# Part 3: Testing Levels Strategy

The levels form a layered strategy: fast unit tests protect rules, integration tests protect contracts, system tests protect end-to-end behavior, and acceptance tests establish business fitness. Repeating a risk at several levels is intentional when the failure impact is high.

## Unit Testing

**Scope**: Individual functions, classes, hooks, reducers, validators, and UI components isolated from networks, databases, clocks, and external providers.

**What to Test**:

- Decimal arithmetic, debit/credit signs, currency rules, and monthly aggregation.
- Transaction normalization, duplicate fingerprints, categories, splits, and budget thresholds.
- Authorization policies, token-claim validation, redaction, input validation, and date/time boundaries.
- Client state transitions and accessible behavior of critical form components.

**Tools**: JUnit 5, AssertJ, Mockito, jqwik for property-based tests, Jest, and React Testing Library.

**Coverage Goal**: At least 85% line coverage and 80% branch coverage overall; 95% branch coverage for calculation, authorization, and deduplication modules. Coverage is a signal, not an exit criterion by itself.

**Example Test Cases**:

1. Given debits and credits with fractional cents, the money aggregator applies the documented rounding rule only at the output boundary.
2. For any valid split list whose parts equal the original amount, saving and recombining the parts preserves the total (property-based test).
3. A duplicate fingerprint composed of user, provider account, external ID, amount, and posting date is stable and tenant-specific.
4. A budget at 79.99% does not alert, crossing 80% alerts once, and recalculation does not resend the same alert.

**Estimated Number of Tests**: Approximately 550 unit and component tests, with mutation testing sampled on the critical calculation package.

---

## Integration Testing

**Scope**: Contracts and data flow between services, PostgreSQL, Redis, the identity provider, the bank-provider adapter, background jobs, and notification/export infrastructure.

**What to Test**:

- API-to-database transactions, ownership constraints, migrations, and rollback behavior.
- Provider pagination, webhooks, rate limits, retries, reauthorization, and idempotency.
- OIDC token validation, session revocation, cache invalidation, and tenant boundaries.
- Notification delivery and secure generation, expiration, and cleanup of exports.

**Tools**: Spring Boot Test, Testcontainers, WireMock, REST Assured, Pact contract tests, Toxiproxy, and Flyway migration verification.

**Coverage Goal**: 100% of critical service contracts and persistence paths, every supported provider error class, and all forward database migrations. About 85% of documented API endpoints receive integration coverage.

**Example Test Cases**:

1. A provider returns page one, times out on page two, and later succeeds; the resumed job stores each transaction exactly once.
2. A transaction insert and its balance update fail atomically when an ownership constraint is violated.
3. Revoking a session invalidates its Redis entry and causes the next protected API request to return 401.
4. Migrating a seeded database forward preserves ownership, counts, decimal precision, and the golden balance checksum.

**Estimated Number of Tests**: Approximately 180 integration and contract tests.

---

## System Testing

**Scope**: The deployable Nexo system in a production-like environment, including web/mobile clients, APIs, workers, storage, observability, and controlled substitutes for external providers.

**What to Test**:

- Complete user journeys and business rules across clients and services.
- Security, privacy, accessibility, compatibility, performance, recovery, and data integrity.
- Concurrent operations, degraded dependencies, deployment migrations, and rollback.
- Privacy-safe logs, metrics, traces, alerts, and operational runbooks.

**Tools**: Playwright, Appium, k6, OWASP ZAP, axe-core, screen readers, BrowserStack, and reconciliation scripts over a versioned golden dataset.

**Coverage Goal**: Automate 100% of P0 journeys and 90% of P1 journeys; meet WCAG 2.2 AA checks for critical flows; exercise the supported browser/device matrix; satisfy p95 dashboard latency under target load; complete one recovery drill per release train.

**Example Test Cases**:

1. A new user enables MFA, connects a bank, imports transactions, creates a budget, receives one threshold alert, exports data, and signs out.
2. Two simultaneous sync workers receive an overlapping provider page; final counts, balances, and audit records remain correct.
3. Under 5,000 concurrent sessions, dashboard p95 stays below 1.5 seconds and the error rate below 1% with no integrity violations.
4. A user completes account deletion; data disappears from user-facing systems and downstream stores according to the declared retention schedule.

**Estimated Number of Tests**: Approximately 120 automated end-to-end scenarios, 35 exploratory charters, and 15 performance/security/recovery suites.

---

## Acceptance Testing

**Scope**: Business validation by product, security, compliance, support, and representative users in a release-candidate environment using realistic but synthetic financial data.

**What to Test**:

- Fitness for the goals of understanding cash flow, controlling spending, and maintaining user trust.
- Acceptance criteria for onboarding, synchronization, budgeting, reporting, consent, export, and deletion.
- Clarity for users with different financial literacy and accessibility needs.
- Operational readiness: support diagnostics, alerts, incident runbooks, recovery objectives, and known-risk approval.

**Tools**: Gherkin/Cucumber for executable acceptance examples, Jira or GitHub Issues for evidence, moderated usability sessions, accessibility assistive technology, and release checklists.

**Coverage Goal**: 100% sign-off on P0 business scenarios; at least 90% task success in usability studies; no open critical/high security issue; product, security, compliance, and operations approve release evidence.

**Example Test Cases**:

1. Given a synthetic month of income and expenses, a participant can identify available budget and the largest spending category without assistance.
2. Given an expired bank authorization, the user reconnects safely and sees no missing or duplicate historical transaction.
3. Given a privacy request, support can explain and verify consent revocation, export, and deletion without viewing unnecessary financial details.
4. During a simulated provider outage, operations detects the failure, follows the runbook, communicates status, and reconciles queued transactions after recovery.

**Estimated Number of Tests**: Approximately 30 formal acceptance scenarios, 12 moderated participant sessions across key personas, and one operational game day per release.

## Traceability and Release Evidence

Each P0/P1 risk is linked to at least one requirement, automated test identifier, execution result, and owner. CI runs unit and integration tests on every change; nightly builds run the stable system suite; weekly and pre-release pipelines run extended compatibility, performance, security, and recovery suites. Failed P0 tests block merging. The release record includes the tested build, environment, data version, unresolved defects, approved exceptions, and monitoring plan.
