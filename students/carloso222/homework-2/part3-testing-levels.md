# Part 3: Testing Levels Strategy — Spotify

## Unit Testing

**Scope**: Individual functions, methods, and components in isolation (e.g., a single microservice function, a UI component, a utility class).

**What to Test**:

- Playback control functions (play, pause, seek, skip) — verify correct state transitions in isolation, with audio hardware mocked.
- Playlist logic (add/remove/reorder track) — verify data structure updates are correct without touching the database.
- Price/subscription calculation logic (e.g., prorated upgrades from Free to Premium, Family plan member limits).
- Search query parser — verify it correctly tokenizes and normalizes user input (e.g., handles typos, special characters).

**Tools**: JUnit / Mockito (Java backend services), pytest (Python services), Jest (React web player / JS components), XCTest (iOS), Espresso/JUnit (Android).

**Coverage Goal**: 80% line coverage on core business logic (playback state machine, playlist management, billing calculations); lower priority for purely presentational UI code.

**Example Test Cases**:

1. `addTrackToPlaylist()` correctly appends a track and does not allow duplicate entries if "no duplicates" mode is enabled.
2. `calculateProratedCharge()` returns the correct amount when a user upgrades from Free to Premium mid-billing-cycle.
3. `parseSearchQuery("beetles")` returns a normalized query that still matches "Beatles" via fuzzy matching.

**Estimated Number of Tests**: ~2,000+ unit tests across all microservices and client apps (given the size and modularity of the platform).

---

## Integration Testing

**Scope**: Interactions between two or more components or services — e.g., the playback service talking to the licensing/rights service, or the client app talking to the authentication API.

**What to Test**:

- Authentication service ↔ user profile service: confirm a successful login correctly retrieves the right user's playlists and preferences.
- Payment gateway ↔ subscription service: confirm a successful payment correctly and immediately upgrades account status.
- Recommendation engine ↔ playback history service: confirm listening history correctly feeds into "Discover Weekly" generation.
- Client app ↔ Content Delivery Network (CDN): confirm the app requests and receives the correct audio stream for a given track and region.

**Tools**: Postman/Newman or REST-assured (API integration tests), Testcontainers (spinning up dependent services/databases in isolation), WireMock (mocking third-party services like payment processors).

**Coverage Goal**: All critical service-to-service contracts covered (target: 100% of documented API contracts between core services — auth, billing, playback, recommendations).

**Example Test Cases**:

1. After a successful OAuth login, the client correctly receives a valid session token and the user's saved playlists in the same session.
2. A completed credit card charge event correctly triggers the subscription service to update the account to "Premium" within an acceptable time window.
3. When a track is region-restricted (licensing), the CDN correctly returns a "not available in your region" response instead of corrupted audio.

**Estimated Number of Tests**: ~500 integration test cases covering the major service boundaries.

---

## System Testing

**Scope**: The application as a complete, end-to-end system, tested against full business requirements, typically in a staging environment that mirrors production.

**What to Test**:

- Full user journey: sign up → search for an artist → create a playlist → play a song → go offline → download tracks → resume playback later.
- Cross-device continuity: start playback on mobile, transfer to a smart speaker via Spotify Connect, confirm seamless handoff.
- Full subscription lifecycle: free trial → conversion to paid → plan change → cancellation → downgrade to Free tier.
- Load and stress behavior of the full stack during a simulated "viral release" event.

**Tools**: Selenium/Playwright (web end-to-end flows), Appium (mobile end-to-end flows), JMeter/k6 (load and stress testing at the system level), manual exploratory testing for less predictable flows.

**Coverage Goal**: 100% of critical user journeys (the "happy paths" identified as mission-critical in Part 1) plus major edge cases (e.g., poor connectivity, expired payment methods).

**Example Test Cases**:

1. A brand-new user can complete registration, find a song, and successfully play it within the expected time and without errors.
2. Playback transferred via Spotify Connect from phone to smart speaker continues from the exact same timestamp with no audio glitch.
3. The system maintains acceptable response times when simulating 50,000 concurrent users triggered by a major artist's midnight album release.

**Estimated Number of Tests**: ~150–200 end-to-end scenarios covering critical and high-priority user journeys.

---

## Acceptance Testing

**Scope**: Validating that the system meets business and user requirements from the perspective of stakeholders (product owners, business team) and real end users, confirming it is ready for release.

**What to Test**:

- Business requirement: "Users must be able to cancel a subscription without contacting support" — verify the self-service cancellation flow fully satisfies this.
- User acceptance: real or representative users complete a beta test of a new feature (e.g., a redesigned "Discover" tab) and confirm it meets their expectations.
- Legal/compliance acceptance: confirm the app correctly enforces regional content licensing restrictions before a feature is released globally.
- Contractual acceptance: confirm royalty-reporting data delivered to record labels matches actual playback counts (a hard business requirement with legal implications).

**Tools**: Manual UAT scripts/checklists reviewed with product owners, beta-testing platforms (e.g., TestFlight for iOS beta groups), A/B testing frameworks to gather real user acceptance signals at scale.

**Coverage Goal**: 100% of the release's defined acceptance criteria signed off by product owners before general availability; beta feedback loop for major feature launches.

**Example Test Cases**:

1. A product owner confirms that the self-service subscription cancellation flow requires no more than 3 taps and no customer support contact.
2. A beta group of 500 users test the redesigned "Discover" tab and at least 80% report it as "easy to use" in a follow-up survey.
3. Royalty/playback-count reports generated for a sample artist match the actual number of completed streams recorded by the analytics pipeline.

**Estimated Number of Tests**: ~30–50 formal acceptance criteria/scenarios per major release, supplemented by ongoing beta and A/B testing programs.
