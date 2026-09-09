# Part 3: Testing Levels Strategy

## Unit Testing

**Scope**: Individual functions, methods, and components in isolation, with all external dependencies (database, bank API, notification service) mocked or stubbed.

**What to Test**:

- Budget calculation functions (category totals, remaining budget, percentage used)
- Currency conversion utility (applies the correct historical exchange rate, handles rounding)
- Transaction categorization rules engine (assigns a category based on merchant name patterns)
- Individual React components (e.g., a budget progress bar renders the correct fill percentage for given props)
- Input validation functions (e.g., rejecting a negative budget limit or an invalid goal date)

**Tools**: Jest (JavaScript/React Native components and utility functions), React Testing Library (component behavior), pytest-style equivalent is not needed here since the backend is Node.js - Jest is also used for backend unit tests.

**Coverage Goal**: 85% line coverage on core business logic (budget calculations, currency conversion, categorization rules); UI components targeted at 70% given the added cost of testing purely presentational code.

**Example Test Cases**:

1. `calculateRemainingBudget()` returns the correct value when spend is under, exactly at, and over the limit.
2. `convertCurrency()` uses the exchange rate stored on the transaction date, not today's rate, and rounds to 2 decimal places using standard rounding rules.
3. `categorizeTransaction()` assigns "Groceries" to a transaction from a known supermarket merchant and falls back to "Uncategorized" for an unrecognized merchant.

**Estimated Number of Tests**: ~220 unit tests

---

## Integration Testing

**Scope**: Interaction between two or more internal components, and between the backend and its direct external dependencies (database, bank aggregation API, notification service), without going through the full UI.

**What to Test**:

- API endpoint + database interaction (e.g., `POST /budgets` correctly persists a new budget and returns it)
- Transaction sync service + bank aggregation API client (correctly parses and stores transactions from a mocked bank API response)
- Bill reminder scheduler + push notification service (a due reminder correctly triggers a notification send call)
- Goal progress service + transaction/budget data (goal progress recalculates correctly when a new transaction affects the linked budget)

**Tools**: Jest with Supertest (API endpoint testing against a test database), a mocked/sandboxed bank aggregation API (e.g., Plaid's sandbox environment), Testcontainers or a Dockerized PostgreSQL instance for realistic database integration tests.

**Coverage Goal**: All API endpoints covered by at least one success-path and one failure-path integration test (target ~90% endpoint coverage).

**Example Test Cases**:

1. `POST /transactions/sync` for a linked account correctly stores new transactions and skips ones already recorded (no duplicates) using the sandboxed bank API.
2. `PUT /budgets/:id` correctly updates a budget and the change is immediately reflected when `GET /budgets/:id` is called.
3. When a bill reminder's due date arrives, the scheduler calls the notification service exactly once with the correct user and bill details.

**Estimated Number of Tests**: ~90 integration tests

---

## System Testing

**Scope**: The complete, deployed application (mobile app + web app + backend + real or sandboxed third-party integrations) tested end-to-end against full business workflows, verifying both functional and non-functional requirements.

**What to Test**:

- Full user workflows spanning multiple features (e.g., link account -> categorize transactions -> see updated budget -> receive a bill reminder)
- Non-functional characteristics at the system level: performance under load, security scans, cross-device compatibility
- Data consistency across the mobile app, web app, and backend when the same account is used on multiple devices

**Tools**: Playwright (web end-to-end flows), Detox or Appium (mobile end-to-end flows), k6 or JMeter (load/performance testing at the system level), OWASP ZAP (automated security scanning).

**Coverage Goal**: All critical user journeys (account linking, budgeting, goal tracking, bill reminders) covered by at least one end-to-end scenario; target 100% of "critical" priority features from Part 2 covered by a system test.

**Example Test Cases**:

1. A user links a bank account on mobile, and the imported transactions and resulting budget totals appear correctly and consistently when they log in on the web app.
2. Under a simulated load of 5,000 concurrent users at "start of month," dashboard response times stay under 1 second and no transactions are lost or duplicated.
3. An automated security scan of the deployed staging environment finds no critical or high-severity vulnerabilities (e.g., exposed tokens, missing auth checks).

**Estimated Number of Tests**: ~45 end-to-end system test scenarios

---

## Acceptance Testing

**Scope**: Validating that the system meets business and user requirements from the perspective of stakeholders and real (or representative) end users, typically the last gate before release.

**What to Test**:

- Business requirements defined by product stakeholders (e.g., "users must be able to set up their first budget in under 3 minutes")
- User acceptance criteria for key features, validated through beta testing with a representative group of real users
- Regulatory/compliance requirements relevant to a financial app (e.g., data privacy disclosures shown before linking a bank account)

**Tools**: Manual UAT scripts executed by QA and a beta user group, TestRail (test case management and sign-off tracking), feature flags to run acceptance testing against a limited beta audience in production-like conditions.

**Coverage Goal**: 100% of documented acceptance criteria for a release must be explicitly signed off (pass/fail) before that release ships; no numeric "test count" target since this is criteria-driven rather than exhaustive.

**Example Test Cases**:

1. A group of 20 beta users can each successfully link at least one bank account and create a first budget without contacting support, confirming the onboarding acceptance criterion.
2. Product stakeholders confirm that the privacy disclosure and consent screen is shown and must be explicitly accepted before any bank linking begins, satisfying the compliance acceptance criterion.
3. Beta users confirm that bill reminders arrive at the configured lead time (e.g., 3 days before due) with no missed or duplicate notifications over a 2-week trial period.

**Estimated Number of Tests**: ~25 acceptance criteria validated per release cycle
