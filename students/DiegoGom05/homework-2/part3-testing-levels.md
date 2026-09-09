# Part 3: Testing Levels Strategy

## Unit Testing

**Scope**: Isolated individual functions, methods, algorithmic classes, and utility components without external dependencies like databases or network calls.

**What to Test**:

- Track duration and playlist total runtime calculation algorithms
- Input validation functions (e.g., email syntax, password strength)
- Audio player utility functions (e.g., converting seconds to `MM:SS` display format)

**Tools**: Jest (React/JS), JUnit (Java), PyTest (Python)

**Coverage Goal**: 85% code coverage for core business logic

**Example Test Cases**:

1. Test that `calculatePlaylistDuration()` returns correct total seconds when given an array of track durations.
2. Test that `validateEmailFormat()` returns `false` when passed an email string without an `@` symbol.
3. Test that `formatTime()` correctly formats `215` seconds into the string `"03:35"`.

**Estimated Number of Tests**: ~2,500 unit tests

---

## Integration Testing

**Scope**: Interactions between integrated modules, API endpoints, microservices, and database systems.

**What to Test**:

- REST API endpoints connecting the mobile/web client with backend microservices
- Payment processing module integrating with external gateway APIs (e.g., Stripe, PayPal)
- Search service queries interacting with the database index and caching layer

**Tools**: Postman, REST Assured, Supertest, Testcontainers

**Coverage Goal**: 80% coverage of all API endpoints and integration workflows

**Example Test Cases**:

1. Verify that a `POST /api/v1/playlists` request successfully writes a new playlist entry to the database and returns a `201 Created` status code.
2. Verify that sending valid payment credentials to the payment gateway service receives a success token and updates user status in the database.
3. Validate that the recommendation service correctly receives user history events from the messaging queue (Kafka) and updates user recommendations.

**Estimated Number of Tests**: ~500 integration tests

---

## System Testing

**Scope**: Complete end-to-end testing of the fully integrated Spotify application in a staging environment that mirrors production.

**What to Test**:

- Full user onboarding, subscription, and playback journeys across platforms
- Cross-device playback synchronization via Spotify Connect
- Offline media downloading and playback behavior in air-plane mode

**Tools**: Selenium, Cypress, Appium, Playwright

**Coverage Goal**: 100% execution of critical user journeys and core feature flows

**Example Test Cases**:

1. Execute full flow: New user registers -> Searches for an artist -> Upgrades to Premium -> Downloads album -> Switches to offline mode -> Plays downloaded track.
2. Test that pressing "Play" on the Spotify Mobile app transfers active audio stream seamlessly to a connected Smart TV using Spotify Connect.
3. Verify that removing a download locally purges cached files from disk storage without deleting user playlist metadata.

**Estimated Number of Tests**: ~150 end-to-end system tests

---

## Acceptance Testing

**Scope**: Validation of the entire application against business requirements, user needs, and deployment readiness before public release.

**What to Test**:

- User Acceptance Testing (UAT) for newly designed UI features or experimental tools
- Beta testing releases with selected external user groups
- Compliance with global standards (e.g., WCAG accessibility, GDPR data export)

**Tools**: TestFlight (iOS), Google Play Beta Console, Firebase App Distribution

**Coverage Goal**: 100% sign-off on release acceptance criteria by Product Owners and QA Leads

**Example Test Cases**:

1. Beta testing group evaluates usability and engagement of a new AI-generated playlist feature over a 2-week testing window.
2. Verify that clicking "Download My Data" under privacy settings correctly generates a downloadable file with all stored user playback history (GDPR compliance).
3. Validate that screen readers (VoiceOver/TalkBack) can successfully read and navigate through all main media controls for visually impaired users.

**Estimated Number of Tests**: ~40 acceptance test scenarios