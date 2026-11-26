# Part 3: Testing Levels Strategy

## Unit Testing
**Scope**: Pricing, validation, state transitions, and UI components in isolation.
**What to Test**: cart calculations; modifier validation; order-state rules.
**Tools**: Jest/Vitest, React Testing Library, pytest/JUnit, factory data.
**Coverage Goal**: 85% line and 80% branch coverage in payment, pricing, and order modules.
**Example Test Cases**:
1. A promotion, fee, and tip produce a correctly rounded total.
2. An item with a required modifier cannot enter the cart without it.
3. A delivered order cannot transition back to picked_up.
**Estimated Number of Tests**: ~320.

## Integration Testing
**Scope**: APIs, database, payment callbacks, queues, identity, and third-party adapters.
**What to Test**: order persistence with inventory; payment webhooks; courier events.
**Tools**: Supertest/Postman, Testcontainers, WireMock, Pact.
**Coverage Goal**: Every API contract plus positive, invalid, timeout, and duplicate-event paths.
**Example Test Cases**:
1. A duplicate valid payment webhook updates only one order.
2. Unavailable inventory blocks persistence with a cart error.
3. Courier assignment stores an event and sends one notification.
**Estimated Number of Tests**: ~110.

## System Testing
**Scope**: Deployed web/mobile clients, services, configuration, and sandbox integrations.
**What to Test**: end-to-end purchase; cross-role status changes; resilience and performance.
**Tools**: Playwright/Cypress, Appium/Maestro, k6, OWASP ZAP.
**Coverage Goal**: Every critical path and all P0/P1 risks in a production-like environment.
**Example Test Cases**:
1. Customer orders, pays, receives status, and rates delivery.
2. Restaurant substitution updates total and communicates options.
3. Payment timeout shows recovery without duplicate order.
**Estimated Number of Tests**: ~75 automated scenarios plus exploratory charters.

## Acceptance Testing
**Scope**: Product-owner and representative-user validation of agreed business outcomes.
**What to Test**: acceptance criteria, price clarity, operations workflows, accessibility and policy.
**Tools**: Gherkin/Cucumber, shared staging, usability sessions, analytics.
**Coverage Goal**: 100% of release criteria and all P0/P1 stories accepted; five representative users for changed primary flows.
**Example Test Cases**:
1. Checkout total matches receipt and restaurant payout.
2. New customer explains fees, delivery estimate, and cancellation choice.
3. Restaurant operator handles a timed order simulation.
**Estimated Number of Tests**: ~40 acceptance scenarios per major release.
