# Exercise 4: API Data-Driven Testing (Python)

## Objective

Apply data-driven testing to API testing scenarios with complex request/response validation.

## Scenario: RESTful API Testing

Test a complete REST API with various endpoints, methods, and data scenarios.

## Setup

**api_server.py** (Mock API for testing):

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory database
users = {}
posts = {}
user_id_counter = 1
post_id_counter = 1

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data.get('username') or not data.get('email'):
        return jsonify({"error": "Missing required fields"}), 400

    global user_id_counter
    user = {
        "id": user_id_counter,
        "username": data['username'],
        "email": data['email'],
        "bio": data.get('bio', '')
    }
    users[user_id_counter] = user
    user_id_counter += 1

    return jsonify(user), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify(users[user_id]), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    users[user_id].update(data)
    return jsonify(users[user_id]), 200

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

## Part 1: API Test Data

**test_data/api_tests.json**:

```json
{
  "user_creation_tests": [
    {
      "name": "create_user_success",
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "username": "alice",
        "email": "alice@example.com",
        "bio": "Test user"
      },
      "expected": {
        "status_code": 201,
        "response_contains": {
          "username": "alice",
          "email": "alice@example.com"
        },
        "response_has_keys": ["id", "username", "email", "bio"]
      }
    },
    {
      "name": "create_user_missing_username",
      "method": "POST",
      "endpoint": "/api/users",
      "body": {
        "email": "test@example.com"
      },
      "expected": {
        "status_code": 400,
        "response_contains": {
          "error": "Missing required fields"
        }
      }
    }
  ],
  "user_retrieval_tests": [
    {
      "name": "get_user_success",
      "setup": {
        "create_users": [{ "username": "bob", "email": "bob@example.com" }]
      },
      "method": "GET",
      "endpoint": "/api/users/1",
      "expected": {
        "status_code": 200,
        "response_contains": {
          "username": "bob"
        }
      }
    },
    {
      "name": "get_user_not_found",
      "method": "GET",
      "endpoint": "/api/users/999",
      "expected": {
        "status_code": 404,
        "response_contains": {
          "error": "User not found"
        }
      }
    }
  ]
}
```

**test_api.py**:

```python
import pytest
import json
import requests
from api_server import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def load_api_test_data():
    """Load API test data from JSON"""
    with open('test_data/api_tests.json', 'r') as f:
        return json.load(f)

test_data = load_api_test_data()

@pytest.mark.parametrize(
    "test_case",
    test_data['user_creation_tests'],
    ids=lambda tc: tc['name']
)
def test_user_creation(client, test_case):
    """Test user creation API with various inputs"""

    # Make request
    response = client.post(
        test_case['endpoint'],
        json=test_case['body'],
        content_type='application/json'
    )

    # Verify status code
    assert response.status_code == test_case['expected']['status_code']

    # Verify response content
    response_data = response.get_json()

    if 'response_contains' in test_case['expected']:
        for key, value in test_case['expected']['response_contains'].items():
            assert key in response_data
            assert response_data[key] == value

    if 'response_has_keys' in test_case['expected']:
        for key in test_case['expected']['response_has_keys']:
            assert key in response_data

# TODO: Implement test_user_retrieval similar to above
# TODO: Implement test_user_update
# TODO: Implement test_user_deletion
```

## Part 2: Authentication Tests

**test_data/auth_tests.json**:

```json
{
  "login_tests": [
    {
      "name": "login_success",
      "credentials": {
        "username": "admin",
        "password": "admin123"
      },
      "expected": {
        "status": 200,
        "response_has": ["token", "user_id"],
        "token_format": "^[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+\\.[A-Za-z0-9-_]+$"
      }
    },
    {
      "name": "login_invalid_credentials",
      "credentials": {
        "username": "admin",
        "password": "wrongpassword"
      },
      "expected": {
        "status": 401,
        "error": "Invalid credentials"
      }
    },
    {
      "name": "login_missing_password",
      "credentials": {
        "username": "admin"
      },
      "expected": {
        "status": 400,
        "error": "Missing password"
      }
    }
  ],
  "protected_endpoint_tests": [
    {
      "name": "access_with_valid_token",
      "endpoint": "/api/profile",
      "auth_token": "valid_token_here",
      "expected": {
        "status": 200
      }
    },
    {
      "name": "access_without_token",
      "endpoint": "/api/profile",
      "expected": {
        "status": 401,
        "error": "Authentication required"
      }
    },
    {
      "name": "access_with_expired_token",
      "endpoint": "/api/profile",
      "auth_token": "expired_token_here",
      "expected": {
        "status": 401,
        "error": "Token expired"
      }
    }
  ]
}
```

## Part 3: Complex Validation

Create tests that validate:

- Response schema
- Response time (performance)
- Header values
- Status codes for all HTTP methods

**test_data/validation_tests.json**:

```json
{
  "response_schema_tests": [
    {
      "name": "user_list_schema",
      "endpoint": "/api/users",
      "expected_schema": {
        "type": "array",
        "items": {
          "type": "object",
          "required": ["id", "username", "email"],
          "properties": {
            "id": { "type": "integer" },
            "username": { "type": "string" },
            "email": { "type": "string" },
            "bio": { "type": "string" }
          }
        }
      }
    }
  ],
  "performance_tests": [
    {
      "name": "get_user_performance",
      "endpoint": "/api/users/1",
      "max_response_time_ms": 100
    }
  ]
}
```

## Requirements

1. Implement all CRUD operations for users
2. Create comprehensive test data JSON (30+ test cases)
3. Test success and failure scenarios
4. Validate response structure
5. Test authentication/authorization
6. Include performance tests
7. Use pytest fixtures for setup/teardown

## Advanced: Testing Real APIs

**test_data/github_api_tests.json** (Example):

```json
{
  "github_api_tests": [
    {
      "name": "get_user_profile",
      "base_url": "https://api.github.com",
      "endpoint": "/users/octocat",
      "method": "GET",
      "headers": {
        "Accept": "application/vnd.github.v3+json"
      },
      "expected": {
        "status": 200,
        "response_has_keys": ["login", "id", "avatar_url"],
        "response_matches": {
          "login": "octocat"
        }
      }
    }
  ]
}
```

## Tips

1. Use `requests` library for API calls
2. Use Flask's `test_client()` for testing Flask apps
3. Validate JSON schemas with `jsonschema` library
4. Measure response times with `time.time()`
5. Clean up test data after each test

## Submission

Submit:

- `api_server.py` (API implementation)
- All test files
- All JSON test data files
- `requirements.txt` with dependencies
- README with API documentation
- Test coverage report

## Grading Criteria

- API implementation: 25%
- Test data quality: 30%
- Test coverage: 30%
- Code quality: 10%
- Documentation: 5%
