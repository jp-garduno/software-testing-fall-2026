# Milestone 4: White Box Testing

**Due**: End of Week 10  
**Points**: 20 (20% of project grade)  
**Focus**: Unit and integration testing with code coverage  
**Module Applied**: White Box Testing (Module 5)

---

## 🎯 Objectives

- Implement comprehensive unit tests
- Achieve 80%+ code coverage
- Write integration tests for API endpoints
- Use mocking for external dependencies
- Generate coverage reports
- Fix bugs discovered through testing

---

## 📋 Deliverables

### 1. Unit Tests (40 points)

#### 1.1 Test Coverage Requirements

**Minimum Coverage**:

- Overall: 80% line coverage
- Critical modules: 90%+ coverage
- Business logic: 95%+ coverage

**Coverage by Component**:
| Component | Target Coverage | Rationale |
| ----------------- | --------------- | ------------------------------ |
| Authentication | 95% | Critical security component |
| Business Logic | 95% | Core application functionality |
| API Routes | 85% | Integration tests cover some |
| Models/Schema | 80% | Simpler code, less complexity |
| Utilities | 90% | Reused across application |

#### 1.2 Unit Test Structure

**Python (pytest)**:

```python
# tests/unit/test_auth.py
import pytest
from src.api.services.auth import AuthService
from src.api.models.user import User

class TestAuthService:
    """Unit tests for authentication service"""

    @pytest.fixture
    def auth_service(self):
        """Create auth service instance for testing"""
        return AuthService()

    @pytest.fixture
    def valid_user_data(self):
        """Valid user registration data"""
        return {
            "email": "test@example.com",
            "password": "ValidPass123!",
            "username": "testuser"
        }

    def test_register_user_success(self, auth_service, valid_user_data):
        """Test successful user registration"""
        # Arrange
        email = valid_user_data["email"]
        password = valid_user_data["password"]

        # Act
        user = auth_service.register(email, password)

        # Assert
        assert user is not None
        assert user.email == email
        assert user.password != password  # Should be hashed
        assert auth_service.verify_password(user, password)

    def test_register_duplicate_email(self, auth_service, valid_user_data):
        """Test registration with duplicate email fails"""
        # Arrange
        auth_service.register(valid_user_data["email"], valid_user_data["password"])

        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            auth_service.register(valid_user_data["email"], "AnotherPass123!")

    @pytest.mark.parametrize("invalid_email", [
        "notanemail",
        "@example.com",
        "missing-domain@",
        ""
    ])
    def test_register_invalid_email(self, auth_service, invalid_email):
        """Test registration with invalid email formats"""
        with pytest.raises(ValueError, match="Invalid email"):
            auth_service.register(invalid_email, "ValidPass123!")
```

**JavaScript (Jest)**:

```javascript
// tests/unit/auth.test.js
const AuthService = require("../../src/api/services/auth");

describe("AuthService", () => {
  let authService;

  beforeEach(() => {
    authService = new AuthService();
  });

  describe("register", () => {
    const validUserData = {
      email: "test@example.com",
      password: "ValidPass123!",
      username: "testuser",
    };

    it("should successfully register a new user", async () => {
      // Arrange
      const { email, password } = validUserData;

      // Act
      const user = await authService.register(email, password);

      // Assert
      expect(user).toBeDefined();
      expect(user.email).toBe(email);
      expect(user.password).not.toBe(password); // Should be hashed
      expect(await authService.verifyPassword(user, password)).toBe(true);
    });

    it("should fail when registering duplicate email", async () => {
      // Arrange
      await authService.register(validUserData.email, validUserData.password);

      // Act & Assert
      await expect(
        authService.register(validUserData.email, "AnotherPass123!"),
      ).rejects.toThrow("Email already exists");
    });

    it.each(["notanemail", "@example.com", "missing-domain@", ""])(
      "should reject invalid email: %s",
      async (invalidEmail) => {
        await expect(
          authService.register(invalidEmail, "ValidPass123!"),
        ).rejects.toThrow("Invalid email");
      },
    );
  });
});
```

#### 1.3 Required Test Suites

Create unit tests for **all** modules:

- [ ] `tests/unit/test_auth.py` - Authentication logic
- [ ] `tests/unit/test_models.py` - Database models
- [ ] `tests/unit/test_validation.py` - Input validation
- [ ] `tests/unit/test_business_logic.py` - Core features
- [ ] `tests/unit/test_utils.py` - Utility functions

**Minimum**: 50+ unit test cases

---

### 2. Integration Tests (30 points)

#### 2.1 API Endpoint Tests

Test all API endpoints with real database (test DB):

```python
# tests/integration/test_api_auth.py
import pytest
from fastapi.testclient import TestClient
from src.api.app import app

@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)

@pytest.fixture
def test_db():
    """Set up test database"""
    # Create test database
    db = create_test_database()
    yield db
    # Teardown
    db.drop_all()

class TestAuthAPI:
    """Integration tests for authentication endpoints"""

    def test_register_endpoint(self, client, test_db):
        """Test POST /api/auth/register"""
        # Arrange
        payload = {
            "email": "newuser@example.com",
            "password": "ValidPass123!"
        }

        # Act
        response = client.post("/api/auth/register", json=payload)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == payload["email"]
        assert "password" not in data  # Should not return password
        assert "id" in data

    def test_login_endpoint_success(self, client, test_db):
        """Test POST /api/auth/login with valid credentials"""
        # Arrange - Register user first
        register_payload = {
            "email": "user@example.com",
            "password": "ValidPass123!"
        }
        client.post("/api/auth/register", json=register_payload)

        # Act - Login
        login_payload = {
            "email": "user@example.com",
            "password": "ValidPass123!"
        }
        response = client.post("/api/auth/login", json=login_payload)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_protected_endpoint_without_auth(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/users/profile")
        assert response.status_code == 401

    def test_protected_endpoint_with_auth(self, client, test_db):
        """Test accessing protected endpoint with valid token"""
        # Arrange - Register and login
        user_data = {"email": "user@example.com", "password": "ValidPass123!"}
        client.post("/api/auth/register", json=user_data)
        login_response = client.post("/api/auth/login", json=user_data)
        token = login_response.json()["access_token"]

        # Act
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/users/profile", headers=headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == user_data["email"]
```

#### 2.2 Database Integration Tests

```python
# tests/integration/test_database.py
def test_user_crud_operations(test_db):
    """Test Create, Read, Update, Delete for User model"""
    # Create
    user = User(email="test@example.com", password_hash="hashed")
    test_db.add(user)
    test_db.commit()
    assert user.id is not None

    # Read
    retrieved = test_db.query(User).filter_by(email="test@example.com").first()
    assert retrieved.id == user.id

    # Update
    retrieved.username = "newusername"
    test_db.commit()
    updated = test_db.query(User).get(user.id)
    assert updated.username == "newusername"

    # Delete
    test_db.delete(updated)
    test_db.commit()
    assert test_db.query(User).get(user.id) is None
```

#### 2.3 Required Integration Test Suites

- [ ] `tests/integration/test_api_auth.py` - Auth endpoints
- [ ] `tests/integration/test_api_users.py` - User endpoints
- [ ] `tests/integration/test_api_<feature>.py` - Core feature endpoints
- [ ] `tests/integration/test_database.py` - Database operations

**Minimum**: 20+ integration test cases

---

### 3. Mocking Strategy (15 points)

#### 3.1 Mock External Dependencies

```python
# tests/unit/test_email_service.py
from unittest.mock import Mock, patch
import pytest
from src.api.services.email import EmailService

class TestEmailService:
    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp):
        """Test email sending with mocked SMTP"""
        # Arrange
        mock_server = Mock()
        mock_smtp.return_value.__enter__.return_value = mock_server
        email_service = EmailService()

        # Act
        result = email_service.send_email(
            to="user@example.com",
            subject="Test",
            body="Test email"
        )

        # Assert
        assert result is True
        mock_server.send_message.assert_called_once()

    @patch('requests.post')
    def test_external_api_call(self, mock_post):
        """Test calling external API with mock"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Act
        result = call_external_api()

        # Assert
        assert result["status"] == "success"
        mock_post.assert_called_once()
```

#### 3.2 Mock Database

```python
@pytest.fixture
def mock_db_session():
    """Mock database session"""
    session = Mock()
    session.query.return_value.filter_by.return_value.first.return_value = User(
        id=1, email="test@example.com"
    )
    return session

def test_get_user_with_mock_db(mock_db_session):
    """Test getting user with mocked database"""
    service = UserService(mock_db_session)
    user = service.get_user_by_email("test@example.com")
    assert user.id == 1
```

---

### 4. Coverage Reports (10 points)

#### 4.1 Generate Coverage Reports

**Python**:

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

**JavaScript**:

```bash
# Run tests with coverage
npm test -- --coverage

# View HTML report
open coverage/lcov-report/index.html
```

#### 4.2 Coverage Report Analysis

Create `docs/milestones/M4/coverage-report.md`:

```markdown
# Coverage Report - Milestone 4

## Overall Coverage

- **Line Coverage**: 85%
- **Branch Coverage**: 82%
- **Function Coverage**: 90%

## Coverage by Module

| Module            | Line %  | Branch % | Functions % | Missing Lines |
| ----------------- | ------- | -------- | ----------- | ------------- |
| src/api/auth.py   | 95%     | 92%      | 100%        | 45-47         |
| src/api/users.py  | 88%     | 85%      | 95%         | 23, 67-70     |
| src/api/orders.py | 82%     | 78%      | 90%         | 102-115       |
| src/api/utils.py  | 92%     | 90%      | 100%        | 12            |
| **Total**         | **85%** | **82%**  | **90%**     |               |

## Uncovered Code Analysis

### Low-Priority Uncovered

| File              | Lines | Reason                    | Action          |
| ----------------- | ----- | ------------------------- | --------------- |
| src/api/errors.py | 45-50 | Error handling edge cases | Add tests in M5 |
| src/api/utils.py  | 12    | Deprecated function       | Remove or test  |

### High-Priority Coverage Gaps

| File              | Lines   | Impact | Plan                          |
| ----------------- | ------- | ------ | ----------------------------- |
| src/api/orders.py | 102-115 | High   | Add test for refund logic     |
| src/api/auth.py   | 45-47   | Medium | Test password reset edge case |

## Next Steps

1. Add tests for order refund logic (HIGH PRIORITY)
2. Improve branch coverage in users module
3. Test error handling paths
4. Target: 90% coverage by M5
```

Include screenshots of coverage reports.

---

### 5. Bug Fixes (10 points)

#### 5.1 Document Bugs Found

Create `docs/milestones/M4/bugs-found.md`:

| Bug ID | Description                           | Severity | Found By | Status | Fixed In Commit |
| ------ | ------------------------------------- | -------- | -------- | ------ | --------------- |
| BUG-01 | Login fails with SQL injection        | Critical | Tests    | Fixed  | abc1234         |
| BUG-02 | Cart total calculation wrong for bulk | High     | Tests    | Fixed  | def5678         |
| BUG-03 | Missing email validation              | Medium   | Tests    | Fixed  | ghi9012         |
| BUG-04 | Race condition in order creation      | High     | Tests    | Fixed  | jkl3456         |

#### 5.2 Show Test-Driven Bug Fixes

For each critical bug:

1. Write failing test demonstrating bug
2. Fix the code
3. Verify test now passes
4. Document in git history

---

## 📤 Submission Instructions

### 1. Required Files

```
tests/
├── unit/
│   ├── test_auth.py (50+ tests total)
│   ├── test_models.py
│   ├── test_validation.py
│   └── ...
├── integration/
│   ├── test_api_auth.py (20+ tests total)
│   ├── test_api_users.py
│   └── test_database.py
├── conftest.py (shared fixtures)
└── pytest.ini / jest.config.js

docs/milestones/M4/
├── coverage-report.md
├── bugs-found.md
├── testing-strategy.md
└── screenshots/
    ├── coverage-overall.png
    ├── coverage-auth.png
    └── ci-passing.png
```

### 2. CI/CD Must Pass

Update `.github/workflows/ci.yml` to enforce coverage:

```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-report=xml --cov-report=term --cov-fail-under=80
```

### 3. Create Pull Request

```bash
git checkout -b milestone-4-white-box
git add tests/ docs/milestones/M4/
git commit -m "test: complete M4 unit and integration tests (80%+ coverage)"
git push -u origin milestone-4-white-box
gh pr create --title "Milestone 4: White Box Testing"
```

### 4. Submit on Canvas

- Pull Request URL (CI must be green ✅)
- Coverage report link
- Bugs found document link

---

## 🎯 Grading Rubric

| Category              | Points | Criteria                                       |
| --------------------- | ------ | ---------------------------------------------- |
| **Unit Tests**        | 40     | 50+ tests, all components covered, AAA pattern |
| **Integration Tests** | 30     | 20+ tests, API endpoints, database tested      |
| **Mocking Strategy**  | 15     | External deps mocked, proper use of mocks      |
| **Coverage Reports**  | 10     | 80%+ coverage, detailed analysis, screenshots  |
| **Bug Fixes**         | 10     | Bugs documented, test-driven fixes             |
| **Code Quality**      | 10     | Clean tests, good naming, proper fixtures      |
| **CI/CD Integration** | 10     | Tests run in CI, coverage enforced             |

**Total**: 125 points (25% bonus available)

**Requirements**:

- Minimum 80% code coverage (REQUIRED)
- All tests must pass in CI (REQUIRED)
- 50+ unit tests, 20+ integration tests (REQUIRED)

**Deductions**:

- Coverage < 80%: -20 points (-5 per % below 80%)
- CI failing: -15 points
- < 50 unit tests: -2 points per missing test
- < 20 integration tests: -3 points per missing test
- No mocking: -15 points
- Tests don't follow AAA pattern: -5 points

---

## ✅ Checklist

- [ ] 50+ unit tests written
- [ ] 20+ integration tests written
- [ ] 80%+ line coverage achieved
- [ ] All critical modules have 90%+ coverage
- [ ] External dependencies mocked appropriately
- [ ] Coverage reports generated (HTML and terminal)
- [ ] Coverage analysis document written
- [ ] Bugs found during testing documented
- [ ] All bugs fixed with test-driven approach
- [ ] CI/CD enforces coverage threshold
- [ ] All tests passing in CI (green checkmark)
- [ ] Test code reviewed by team members
- [ ] PR created and submitted

---

## 💡 Tips for Success

### Writing Good Tests

1. **AAA Pattern**: Arrange, Act, Assert
2. **One assertion per test** (when possible)
3. **Clear test names**: `test_<what>_<condition>_<expected>`
4. **Use fixtures** for common setup
5. **Parameterize** similar tests
6. **Test edge cases** and error paths

### Increasing Coverage

1. **Start with critical code**: Auth, business logic first
2. **Use coverage reports**: Find untested lines
3. **Test error paths**: Don't just test happy path
4. **Branch coverage**: Test all if/else branches
5. **Mock wisely**: Don't over-mock, test real interactions

### Common Mistakes

- ❌ Only testing happy paths
- ❌ Tests depend on each other
- ❌ Not cleaning up test data
- ❌ Mocking too much (no integration testing)
- ❌ Ignoring low-coverage modules
- ❌ Tests are too slow (not using mocks)

---

## 📚 Resources

- [Module 5: White Box Testing](../../05-white-box-testing/)
- [pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Python unittest.mock](https://docs.python.org/3/library/unittest.mock.html)
- [Testing Guidelines](../guidelines/testing-guidelines.md)

---

**Testing is not a phase, it's a practice. Write tests as you code!** ✅🧪
