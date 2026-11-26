## Unit Testing

**Scope**: Individual functions/methods/components in isolation, with all external dependencies (network, database, other services) mocked or stubbed.

**What to Test**:

- Authentication logic — password hashing/validation, token generation and expiration, email format validation on registration.
- Playlist domain logic — functions that add/remove/reorder tracks, enforce max playlist length, prevent duplicate track entries, and compute playlist duration.
- Search query parsing — functions that tokenize and normalize a raw search string (e.g., trimming, lowercasing, handling special characters) before it is sent to the search index.
- Recommendation scoring helpers — pure functions that compute a similarity or ranking score from a set of listening-history features.
- React UI components — rendering of the player controls (play/pause/next/previous) and playlist list items in different states (loading, empty, error).

**Tools**: Jest (JavaScript/TypeScript, React components), XCTest (iOS/Swift), JUnit + Mockito (Android/Kotlin), ts-jest or Vitest for the TypeScript backend.

**Coverage Goal**: 80% code coverage on core business logic modules (auth, playlist, search parsing, recommendation scoring); 60%+ on UI components.

**Example Test Cases**:

1. Verify that the password hashing function produces a different hash for the same password on each call (salting works) but validates correctly against the original password.
2. Verify that adding a track already present in a playlist is rejected by the "add track" function without modifying the playlist state.
3. Verify that the search query parser correctly strips leading/trailing whitespace and lowercases a mixed-case artist name before tokenization.
4. Verify that the play/pause button component toggles its icon and calls the correct callback when clicked.

**Estimated Number of Tests**: ~400–500 unit tests across all platforms (backend logic, iOS, Android, and web components).

---

## Integration Testing

**Scope**: Interaction between two or more internal components or services, such as an API endpoint talking to a database, or the recommendation service consuming data from the listening-history service. External third-party systems may still be mocked, but internal service boundaries are exercised for real.

**What to Test**:

- Authentication service ↔ session/database layer — verify that a successful login writes a valid session record and that the session can be retrieved and validated by the API layer.
- Playlist API ↔ database — verify that creating, renaming, and deleting a playlist through the API correctly persists and removes records in the database, including cascading deletion of playlist-track associations.
- Search API ↔ search index/catalog service — verify that a new song published by an artist becomes searchable through the search API within an expected indexing window.
- Streaming service ↔ CDN/audio delivery layer — verify that a playback request correctly resolves to a valid, licensed audio stream URL for the requesting user's subscription tier (free vs. Premium).
- Recommendation engine ↔ listening-history store — verify that recently played tracks are correctly fed into the "Discover Weekly" generation job.

**Tools**: Supertest or Postman/Newman (API-level integration tests against the TypeScript backend), Testcontainers (spinning up real/ephemeral database instances for tests), Jest/Mocha as the test runner, WireMock for stubbing any external dependency not under test.

**Coverage Goal**: All critical service-to-service integration points (auth, playlist, search, streaming, recommendations) covered by at least one happy-path and one failure-path test; target ~70% of documented API contracts.

**Example Test Cases**:

1. Verify that a POST request to create a playlist results in a correctly linked row in the playlists and playlist_tracks tables, and that a subsequent GET returns the same data.
2. Verify that when the audio delivery layer returns an error (e.g., file not found), the streaming API returns a graceful error response instead of a raw exception.
3. Verify that a free-tier user's playback request is correctly resolved to an ad-supported stream, while a Premium user's request resolves to an ad-free, higher-quality stream.
4. Verify that deleting a user account cascades correctly to remove or anonymize their playlists and listening history per data-retention rules.

**Estimated Number of Tests**: ~150–200 integration tests.

---

## System Testing

**Scope**: The application as a whole, end-to-end, running in an environment that closely mirrors production (real backend, real databases, real third-party integrations where feasible), tested against the full set of functional and non-functional requirements identified in Part 2.

**What to Test**:

- Full functional workflows — registration through login, search, playback, and playlist management, validated together as a real user would experience them.
- Non-functional requirements — performance (playback start time, search latency), load/stress behavior under simulated concurrent users, security (session isolation, injection resistance), compatibility across iOS/Android/Web, and accessibility (screen reader/keyboard navigation) as defined in Part 2's test types.
- Cross-platform behavior — verifying that state (e.g., current playback position, queue) stays consistent when a user switches from the mobile app to the web player.
- Artist-side system flow — upload, processing, and publishing of a song through to its appearance in the catalog and search index.
- Failure and recovery scenarios — behavior when a dependent service (e.g., recommendation engine, CDN) is degraded or unavailable, verifying graceful degradation rather than full outage.

**Tools**: Cypress or Playwright (web end-to-end), Appium (cross-platform mobile automation for iOS/Android), k6 or JMeter (load/stress testing), OWASP ZAP or Burp Suite (security scanning), axe-core (accessibility audits), BrowserStack/Sauce Labs (device and browser compatibility matrix).

**Coverage Goal**: 100% of critical-priority requirements from Part 2 (functional, security) and high-priority requirements (performance, load, compatibility) exercised at least once in a production-like environment.

**Example Test Cases**:

1. Verify that a new user can complete the full journey of registering, searching for a song, playing it, and saving it to a new playlist, with all steps working together correctly.
2. Simulate 2 million concurrent playback sessions and confirm that playback start time stays under the defined threshold and error rates remain within acceptable limits.
3. Verify that a session token issued on the web player cannot be used to access another user's private playlists when replayed against the mobile API.
4. Verify that when the recommendation service is intentionally taken offline, the app still allows search, playback, and manual playlist management without crashing.

**Estimated Number of Tests**: ~100–150 system-level test scenarios (combining functional, performance, security, compatibility, and accessibility suites).

---

## Acceptance Testing

**Scope**: Validating that the finished product meets business requirements and real user expectations, typically performed from the perspective of stakeholders or actual end users (listeners and artists) rather than the engineering team, using acceptance criteria tied to the application's stated purpose.

**What to Test**:

- Listener-side acceptance criteria — a listener can discover, save, and enjoy personalized audio content as easily as the product's purpose statement promises.
- Artist-side acceptance criteria — an artist or label can publish a song and reach fans through the distribution and analytics tools described in the application's purpose.
- Business/monetization rules — the free vs. Premium distinction (ads, offline listening, audio quality) behaves exactly as marketed to users during a subscription upgrade or downgrade.
- Usability acceptance — new users (both listener and artist personas) can complete their primary workflow without external help, matching the usability goals from Part 2.
- Legal/compliance acceptance — accessibility (WCAG 2.1 AA) and data-handling behaviors meet the standard required for market launch.

**Tools**: Manual exploratory testing by QA/product stakeholders, structured UAT scripts (TestRail or Zephyr for tracking), Gherkin/Cucumber for behavior-driven acceptance scenarios written in collaboration with product owners, beta/limited-rollout programs with real user feedback (e.g., TestFlight for iOS, Play Console beta tracks for Android).

**Coverage Goal**: 100% of defined acceptance criteria (one per key feature/business rule) signed off by product stakeholders before release; typically expressed as a checklist rather than a raw test count.

**Example Test Cases**:

1. Verify that a first-time listener, given no prior instructions, can find a song they like and start playing it, confirming the product's "discover and enjoy" purpose is met.
2. Verify that upgrading from the free tier to Premium immediately removes ads and enables offline downloads, and that downgrading correctly restores ad-supported playback.
3. Verify that a new artist can complete the full publishing workflow (register, upload a song, publish it) and see basic engagement analytics, confirming the platform's promise as a "distribution channel."
4. Verify, with an actual screen-reader user, that the core listener workflow (search, play, save to playlist) can be completed without sighted assistance.

**Estimated Number of Tests**: ~40–60 acceptance criteria/scenarios, generally tracked as pass/fail checklist items rather than automated test counts.