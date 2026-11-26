# Part 3: Testing Levels Strategy

Testing **levels** describe where in the system we test, from a single function to the product in the hands of real teams. The distribution below follows the test pyramid from the course theory: many cheap tests at the bottom, few expensive ones at the top.

---

## Unit Testing

**Scope**: Individual functions, methods and components in isolation, with the database, Redis, Elasticsearch and the network replaced by test doubles. Written by developers, run on every commit.

**What to Test**:

- Card position and ordering logic - the calculation that decides where a card lands when dropped between two others.
- Permission-checking functions - given a user, a board and a role, is this action allowed?
- Butler rule evaluation - does a rule's trigger condition match a given card event?
- Due-date and reminder calculation, including time zones.
- React component rendering for the card, list and board-header components.

**Tools**: **Jest** for the Node.js services and the React frontend, JUnit and Espresso helpers on Android, XCTest on iOS. Mocking with Jest mocks and Sinon. Coverage measured with **Istanbul**.

**Coverage Goal**: 80% line coverage overall, raised to 95% branch coverage on the permission checks and the card-ordering logic, the two modules where defects cluster.

**Example Test Cases**:

1. `test_card_dropped_between_two_cards_gets_intermediate_position` - the new position value sits strictly between its neighbours.
2. `test_non_member_cannot_edit_private_board_card` - the permission function returns false for a user with no membership.
3. `test_butler_rule_does_not_trigger_on_its_own_action` - prevents a rule from re-triggering itself in a loop.
4. `test_due_date_reminder_uses_board_member_timezone` - a reminder fires at the right local time.

**Estimated Number of Tests**: ~1,500 unit tests, running in under 5 minutes in CI.

---

## Integration Testing

**Scope**: Components working together across a real boundary - service to MongoDB, service to Redis, service to Elasticsearch, client to REST API, client to WebSocket channel. Run on every pull request. The approach is **incremental** rather than big bang, so an interface defect is attributed to the module just added.

**What to Test**:

- API endpoints against a real MongoDB instance, including the write path for cards and boards.
- Search: a card created through the API becomes findable once the Elasticsearch index catches up.
- WebSocket publication: a change written through the API is pushed to a subscribed client.
- Session and cache behaviour in Redis, including expiry.
- Power-Up and public-API contracts consumed by third-party integrations.

**Tools**: **Supertest** and Jest for API-level tests, Testcontainers to spin up disposable MongoDB, Redis and Elasticsearch instances, WireMock to stub third-party services, and Postman/Newman for the API smoke collection in CI.

**Coverage Goal**: every public API endpoint exercised with at least one success and one failure path; every external integration point covered by a contract test.

**Example Test Cases**:

1. Creating a card through the API stores it in MongoDB with the correct board, list and position.
2. A card created through the API is returned by search within the index's agreed lag window.
3. Moving a card emits exactly one WebSocket event to subscribers of that board and none to other boards.
4. A request with an expired session token is rejected with 401 and does not read from the database.
5. Removing a member from a board immediately closes their WebSocket subscription to it.

**Estimated Number of Tests**: ~300 integration tests, running in roughly 15-20 minutes.

---

## System Testing

**Scope**: The complete, integrated product tested end to end in a production-like environment, covering both functional journeys and the non-functional behaviour described in Part 2. Owned by QA, run nightly and as a release gate.

**What to Test**:

- Complete team workflows: create a board, invite a member, create cards, move them through lists, comment and archive.
- Multi-client real-time scenarios with two browsers driven simultaneously.
- Degraded conditions: dropped WebSocket, offline mobile edits, reconnection.
- Non-functional suites: load and stress profiles, penetration testing of the API, usability sessions.
- Cross-surface journeys: a board edited on the web and continued in the mobile app.

**Tools**: **Playwright** and **Selenium** for web end-to-end flows (Playwright's multi-context support drives two users in one test), Appium for mobile, **JMeter** and **Locust** for load and stress, BrowserStack for the compatibility matrix, and OWASP ZAP for automated security scanning.

**Coverage Goal**: 100% of critical user journeys automated, and every P0 and P1 risk from Part 5 mapped to a named system test.

**Example Test Cases**:

1. **Full workflow**: create a board, add three lists and ten cards, move cards between lists, and verify the board state after reload.
2. **Real-time sync**: two browser contexts open the same board; a card moved in one appears in the correct position in the other within 1 second.
3. **Concurrent edit**: both contexts drag the same card to different lists at the same time; both converge on the same final state.
4. **Reconnect**: kill the WebSocket in one context for 60 seconds, make changes in the other, and verify the first resynchronises correctly.
5. **Permission**: a logged-in non-member navigating directly to a private board URL is denied, and the same request through the API returns 401.
6. **Peak load**: sustain the Monday-morning request profile for 30 minutes with 95th-percentile board load under 3 seconds.

**Estimated Number of Tests**: ~50 automated end-to-end scenarios plus the non-functional suites; a full run takes 2-3 hours, which is why it is nightly rather than per-commit.

---

## Acceptance Testing

**Scope**: Validation that the release meets business requirements and real user needs, performed by users and stakeholders rather than engineers. The last gate before deployment.

**What to Test**:

- **User Acceptance Testing (UAT)**: real teams running their actual boards against written acceptance criteria.
- **Business Acceptance Testing (BAT)**: product and business stakeholders confirming the release meets its goals, including anything affecting paid-tier features.
- **Alpha Testing**: internal Atlassian teams using the build in a controlled environment.
- **Beta Testing**: external customers on an opt-in channel, using real boards under real conditions.

**Tools**: Cucumber for acceptance criteria written in Gherkin with the product owner, TestFlight and Google Play testing tracks for mobile betas, in-app feedback and error monitoring for beta telemetry, and feature flags for a staged rollout that can be halted at a small percentage of users.

**Coverage Goal**: 100% of the release's acceptance criteria signed off. Beta exit criteria: zero open Critical defects, no more than 5 open High defects, no reported data-loss incident, and a satisfaction rating of at least 4 out of 5.

**Example Test Cases**:

1. **UAT**: 20 teams run their real boards for two weeks with no reported instance of a card being lost or reverting.
2. **UAT**: a new team creates their first board and reaches a working workflow without contacting support.
3. **BAT**: a stakeholder confirms that paid-tier views and limits are correctly gated, since this is the revenue path.
4. **Beta**: the crash-free session rate on mobile stays above 99.5% for the last 7 days of the cycle.

**Estimated Number of Tests**: ~12 formal acceptance scenarios plus a 2-week beta programme.

---

## Test Pyramid Summary

| Level       | Scope             | Speed   | Estimated Tests | Cost    | Who             | Frequency    |
| ----------- | ----------------- | ------- | --------------- | ------- | --------------- | ------------ |
| Unit        | Function / class  | Fast    | ~1,500          | Low     | Developers      | Every commit |
| Integration | Modules / APIs    | Medium  | ~300            | Medium  | Developers, QA  | Every PR     |
| System      | Complete product  | Slow    | ~50             | High    | QA team         | Nightly      |
| Acceptance  | Business and user | Slowest | ~12 + beta      | Highest | Users, business | Per release  |

In conclusión, it is not an **ice cream cone**: the expensive two-browser sync scenarios are kept to a few dozen because each one costs minutes of machine time. It is not an **hourglass** either: the ~300 integration tests exist precisely to cover the seams between Node.js, MongoDB, Redis, Elasticsearch and the WebSocket layer, where this product's most expensive defects live and which unit tests cannot reach by construction.
