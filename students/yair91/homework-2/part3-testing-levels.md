# Part 3: Testing Levels Strategy

The four levels are complementary, not alternatives. Each one catches bugs the others simply cannot see: a unit test will never catch a wrong database constraint, and a system test will not tell you which of forty functions produced the wrong number.

---

## Unit Testing

**Scope**: Individual functions, methods and React components, in isolation, with every external dependency replaced by a test double.

**What to Test**:

- **Grade calculation**: weighted averages, rounding rules, handling of missing or exempted assessments, minimum passing thresholds.
- **Prerequisite engine**: the rules that decide whether a course is available to a student, including chained prerequisites and validated external credits.
- **Tuition calculation**: base charges, scholarship percentages, discounts, late fees, and the order in which they compose.
- **Schedule-conflict detection**: interval overlap, including sessions that touch at the boundary without overlapping.
- **Validators and formatters**: enrollment identifiers, date ranges, currency formatting per locale.
- **UI components**: rendering states of the grade table, the course card and the payment form, including empty and error states.

**Tools**: Jest with React Testing Library for the frontend, Jest for the NestJS backend, `@faker-js/faker` for test data generation.

**Coverage Goal**: 85% line coverage overall, and 100% branch coverage in the grade, prerequisite and tuition calculation modules. The global number is a hygiene check; the targeted number is the one that matters.

**Example Test Cases**:

1. `calculateFinalGrade` with weights 30/30/40 and scores 8.0/7.5/9.0 returns 8.25.
2. `calculateFinalGrade` with an assessment marked exempt redistributes its weight proportionally instead of scoring it as zero.
3. `hasMetPrerequisites` returns false when the student passed the prerequisite in a term that was later annulled.
4. `detectScheduleConflict` returns false for a class ending at 10:00 and another starting at 10:00.
5. `applyScholarship` with a 50% scholarship and a 10% early-payment discount applies them in the documented order and never produces a negative balance.

**Estimated Number of Tests**: ~450 unit tests, roughly 60% backend and 40% frontend.

---

## Integration Testing

**Scope**: Collaboration between modules and with real infrastructure — API endpoints against a real database, and adapters against external services.

**What to Test**:

- **API and database**: registration endpoints against a real PostgreSQL instance, verifying transactions, unique constraints and rollback on failure.
- **Concurrency**: simultaneous requests for the last seat in a course, exercising the actual locking strategy rather than a mocked one.
- **Payment gateway adapter**: successful charge, declined card, timeout, and duplicate webhook delivery.
- **Identity provider**: SAML login, role mapping, expired assertion, and account deprovisioning.
- **Job queue**: notification and PDF generation jobs, including retry behavior and dead-letter handling.
- **Nightly warehouse export**: shape and completeness of exported data.

**Tools**: Jest with Supertest for HTTP, Testcontainers to run PostgreSQL and Redis in Docker, WireMock to stub the payment gateway and identity provider.

**Coverage Goal**: 100% of API endpoints exercised, and every external integration covered for its success path plus at least three failure modes.

**Example Test Cases**:

1. `POST /enrollments` on a course with one seat left, issued by twenty concurrent clients, produces exactly one 201 and nineteen 409 responses.
2. `POST /payments` returns 502 and leaves no partial charge when the gateway times out after the request was sent.
3. A duplicate payment webhook for an already-processed transaction is acknowledged without creating a second payment record.
4. A SAML assertion carrying the `professor` role grants access to grade capture and denies access to the finance module.
5. Deleting a course with active enrollments is rejected by the database constraint and returns 409 rather than a 500.

**Estimated Number of Tests**: ~180 integration tests.

---

## System Testing

**Scope**: The complete deployed system, exercised end to end through the real interfaces, in an environment that mirrors production.

**What to Test**:

- **Complete academic flows**: login, course search, registration, schedule consultation, assignment submission, grade consultation.
- **Complete administrative flows**: catalog creation, opening a registration window, grade publication, transcript issuance.
- **Complete financial flows**: charge generation, payment, receipt, and reflection of the balance in the student view.
- **Cross-cutting non-functional behavior**: load during the registration window, keyboard-only navigation, screen-reader output, both locales, and the supported browser and device matrix.

**Tools**: Playwright for end-to-end browser flows, Detox for the React Native application, k6 for load testing, axe-core for automated accessibility checks, BrowserStack for the device matrix.

**Coverage Goal**: 100% of critical flows automated; roughly 70% of secondary flows automated, with the rest covered by exploratory sessions.

**Example Test Cases**:

1. A student logs in through SSO, searches for a course by name, registers, and sees it reflected in the schedule within the same session.
2. A professor captures grades for a full group of forty students, the registrar publishes them, and each student sees only their own grade.
3. A student pays tuition with a test card, receives the receipt by email, and observes the balance return to zero.
4. Five thousand virtual users open the registration window simultaneously and the 95th percentile response stays under two seconds with no enrollment lost.
5. The entire registration flow is completed using only the keyboard, with focus visible at every step.

**Estimated Number of Tests**: ~90 automated end-to-end scenarios, plus around 12 exploratory sessions per release.

---

## Acceptance Testing

**Scope**: Confirmation that the system solves the institution's actual problem, validated by the people who will live with it. The question stops being "does it work like we said" and becomes "did we say the right thing".

**What to Test**:

- **User acceptance**: registrar staff, professors and a group of student volunteers execute real term-opening scenarios in a staging environment loaded with anonymized data.
- **Business rules**: verification against institutional regulations for credit limits, minimum passing grades, absence thresholds and refund policy.
- **Regulatory**: personal data handling, retention periods, and the audit trail for grade modifications.
- **Operational readiness**: backup and restore, rollback of a failed deployment, and the runbook for a registration-window incident.

**Tools**: Cucumber with Gherkin scenarios written jointly with the registrar's office, a structured UAT checklist per role, and a beta pilot with one faculty for a full term.

**Coverage Goal**: 100% of documented institutional rules validated by their owner, with explicit written sign-off per role before go-live.

**Example Test Cases**:

1. The registrar confirms that the credit limit per term matches current regulations, including the documented exception for students in their final semester.
2. A professor confirms that the grade-correction flow produces an audit record naming who changed what, when, and why.
3. The finance office confirms that a refund for a dropped course is calculated according to the published calendar of refund percentages.
4. A student volunteer completes registration on their own phone, over mobile data, without instructions.
5. The operations team restores the database from the previous night's backup within the agreed recovery time objective.

**Estimated Number of Tests**: ~60 acceptance scenarios, of which roughly 35 are automated as Gherkin specifications and the rest are executed manually with sign-off.
