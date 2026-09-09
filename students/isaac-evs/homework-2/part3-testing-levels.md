# Part 3: Testing Levels Strategy — Spotify

## Unit Testing

**Scope**: Individual functions, methods, and components in isolation, with all external dependencies (network, database, other services) mocked.

**What to Test**:

- Playlist logic (adding/removing tracks, reordering, duplicate detection)
- Price/subscription calculation functions (prorating a plan upgrade, applying a student discount)
- Audio queue management (next/previous/shuffle/repeat logic)
- Search query parsing and filter construction

**Tools**: pytest (Python backend services), Jest (JavaScript/TypeScript web player and Node services), JUnit (any Java/Scala backend services)

**Coverage Goal**: 80% code coverage on core business logic modules (queue management, playlist operations, billing calculations)

**Example Test Cases**:

1. `test_add_track_to_playlist_appends_to_end` — adding a track appends it to the end of the playlist array without disturbing existing order
2. `test_shuffle_queue_includes_all_tracks_exactly_once` — shuffling the queue produces a permutation containing every track exactly once
3. `test_prorate_upgrade_from_free_to_premium_mid_cycle` — upgrading mid-billing-cycle charges the correct prorated amount

**Estimated Number of Tests**: ~2,000+ unit tests across all backend services and client business logic (a platform of this scale has many independently testable modules)

---

## Integration Testing

**Scope**: Interactions between two or more components or services, such as the playback service talking to the CDN, or the billing service talking to a third-party payment processor.

**What to Test**:

- Playback service correctly requests and receives audio streams from the CDN/content service
- Billing service correctly communicates with external payment gateways (Stripe, Apple Pay, Google Pay)
- Recommendation service correctly reads listening history from the user data service to generate Discover Weekly
- Authentication service correctly issues and validates tokens consumed by other microservices

**Tools**: pytest with `requests-mock`/`responses` for Python service integration, Postman/Newman or REST-assured for API contract testing, Testcontainers for spinning up real dependent services (databases, message queues) in CI

**Coverage Goal**: All critical service-to-service contracts covered (payment, playback, auth, recommendations) — targeting 100% of documented API contracts between critical services

**Example Test Cases**:

1. Playback service returns a valid streaming URL when queried with a valid track ID and active session token
2. Billing service correctly handles a failed payment response from the payment gateway and marks the subscription as "past due" instead of "active"
3. Recommendation service gracefully degrades (returns a default popular-tracks playlist) when the user-history service is unavailable

**Estimated Number of Tests**: ~500 integration tests covering the main service boundaries

---

## System Testing

**Scope**: The complete, integrated Spotify application (client + backend) tested end-to-end as a whole, verifying it meets functional and non-functional requirements from a user's perspective.

**What to Test**:

- Full user journeys: sign up → search → build playlist → play a song → go offline → resume online
- Cross-device behavior: starting playback on mobile and transferring via Spotify Connect to a desktop
- Non-functional behavior at the system level: load testing the full stack during a simulated release-day traffic spike
- Failure/recovery behavior: app behavior when the network drops mid-stream and reconnects

**Tools**: Selenium/Playwright for web player end-to-end flows, Appium for mobile app end-to-end flows, JMeter/k6 for system-level load and performance testing

**Coverage Goal**: All major user journeys (onboarding, search, playback, playlist management, subscription upgrade/downgrade, offline mode) covered end-to-end on each supported platform (iOS, Android, Web, Desktop)

**Example Test Cases**:

1. A new free-tier user can sign up, search for an artist, and play a 30-second preview without errors
2. A Premium user downloads a playlist for offline listening, disables network access, and successfully plays the downloaded tracks
3. Starting playback on a phone and selecting a smart speaker via Spotify Connect transfers playback within 3 seconds without audio glitches

**Estimated Number of Tests**: ~150 end-to-end scenarios per supported platform (mobile, web, desktop)

---

## Acceptance Testing

**Scope**: Validating that the system meets business and user requirements well enough to be released — typically performed from the perspective of stakeholders or a representative sample of real users, using real-world-like scenarios.

**What to Test**:

- Business requirement: "A user must be able to upgrade from Free to Premium and immediately lose ads and gain offline access"
- Business requirement: "Artists must see royalty-accurate stream counts on Spotify for Artists within 24 hours"
- User acceptance: beta users can complete their normal daily listening habits (commute playlist, workout playlist) without friction
- Legal/compliance acceptance: content takedown requests are honored and the track becomes unavailable within the agreed SLA

**Tools**: Manual exploratory testing by QA and product stakeholders, beta testing programs (TestFlight for iOS, Google Play internal testing track), behave/Cucumber for expressing acceptance criteria as executable Gherkin scenarios

**Coverage Goal**: 100% of defined business acceptance criteria for the release must pass sign-off before shipping to production

**Example Test Cases**:

1. Given a Free user upgrades to Premium, when the payment completes, then ads stop appearing and the download icon becomes available within the same session
2. Given an artist's track is streamed 1,000 times, when the artist checks Spotify for Artists the next day, then the stream count reflects the correct total within an acceptable margin
3. Given a licensing agreement expires for a region, when a user in that region opens the track, then it is marked unavailable instead of playable

**Estimated Number of Tests**: ~50-80 acceptance scenarios tied directly to the release's documented business requirements
