## Unit Testing

**Scope**: Individual functions, methods, UI components, and utility classes in isolation.

**What to Test**:
- **Authentication Validator**: Functions that check password strength and email formatting.
- **Feed Algorithm Utilities**: Methods that calculate engagement scores based on likes and comments.
- **UI Components**: The Like Button component (checking state changes when clicked).

**Tools**: Jest, React Testing Library (Frontend), Pytest, Unittest (Backend).

**Coverage Goal**: 85% code coverage for core services.

**Example Test Cases**:
1. `test_password_strength_rejects_weak_password`: Ensure the function returns false for passwords under 6 characters.
2. `test_like_button_toggles_state`: Verify the button changes color from white to red upon being clicked.
3. `test_image_compression_ratio`: Ensure the image compression utility reduces file size by at least 30% without throwing errors.

**Estimated Number of Tests**: ~5,000+ unit tests across all microservices.

---

## Integration Testing

**Scope**: Interactions and data flow between multiple integrated components, modules, or services.

**What to Test**:
- **Frontend-Backend API integration**: Ensuring the mobile app correctly parses JSON from the server.
- **Database connectivity**: Verifying the Python backend can correctly read/write to the PostgreSQL database.
- **Third-party Services**: Integration with AWS S3 for media storage or Stripe for Instagram Shopping payments.

**Tools**: Postman, REST Assured, Pytest, Cypress (Component Integration).

**Coverage Goal**: 70% API endpoint coverage.

**Example Test Cases**:
1. `test_upload_endpoint_saves_to_s3`: Send a POST request with an image and verify it is successfully stored in the AWS bucket.
2. `test_login_flow_generates_token`: Submit valid credentials to the auth API and verify a valid JWT is returned.
3. `test_feed_cache_sync`: Ensure that when a new post is saved to the database, the Redis cache is correctly invalidated and updated.

**Estimated Number of Tests**: ~800 integration tests.

---

## System Testing

**Scope**: The complete, fully integrated software system as a whole, tested against the system requirements.

**What to Test**:
- **End-to-End User Flows**: Registering a new account, setting up a profile, and making the first post.
- **Cross-platform consistency**: Ensuring data syncs between the mobile app and the web browser.
- **Security & Performance**: Testing the entire system's ability to handle load and block attacks.

**Tools**: Appium (Mobile), Selenium/Cypress (Web), JMeter (Performance).

**Coverage Goal**: 100% coverage of critical user journeys.

**Example Test Cases**:
1. Complete End-to-End flow: User logs in, takes a photo, applies a filter, writes a caption, posts it, and verifies it appears on a follower's feed.
2. Verify that deleting an account completely removes all associated photos and comments from the public platform.
3. Simulate 1,000 concurrent users logging in and posting a story simultaneously to verify system stability.

**Estimated Number of Tests**: ~250 system tests.

---

## Acceptance Testing

**Scope**: Validating that the software meets business requirements and is acceptable for delivery to end-users. Performed by QA, Product Managers, and sometimes beta users.

**What to Test**:
- **Business Logic**: Does the new Instagram Shopping feature actually drive conversions?
- **User Acceptance (UAT)**: Is the new UI for Reels intuitive for average users?
- **Alpha/Beta Testing**: Releasing a new feature (like Notes) to a small percentage of users to gather real-world feedback.

**Tools**: TestFlight (iOS), Google Play Console (Android Beta), Manual Testing, A/B Testing tools.

**Coverage Goal**: Approval on all new business requirements for a release candidate.

**Example Test Cases**:
1. Beta users report that the new Direct Message layout is easy to understand and use.
2. Verify that sponsored posts are correctly labeled with "Sponsored" to meet legal business requirements.
3. The marketing team verifies that the new ad analytics dashboard provides accurate and readable metrics.

**Estimated Number of Tests**: ~50 manual/exploratory UAT scenarios per major release.
