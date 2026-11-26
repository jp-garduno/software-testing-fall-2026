# Homework 5: White Box Testing - TaskFlow System

Comprehensive white-box test suite and implementation for **TaskFlow**, a modular task management system, demonstrating unit testing, integration testing, code coverage analysis, mocking, and test doubles.

---

## 🎯 Objectives

- Achieve >80% statement coverage and >80% branch coverage (achieved **100% statement** and **100% branch** coverage).
- Implement fully isolated unit tests for all `Task` model methods, boundary validations, and status transitions.
- Build integration tests combining `TaskService` and `TaskRepository` with proper mocking of external dependencies (`NotificationService`).
- Demonstrate test doubles (Mocks, Stubs, and Fakes) and simulate error handling scenarios.
- Analyze coverage reports, document boundary conditions, and deliver an analytical report.

---

## 📋 Prerequisites

- **Python**: 3.11+ (Tested on Python 3.14)
- **pytest**: 8.0+
- **pytest-cov**: 5.0+

---

## 🚀 Installation

```bash
# Navigate to the homework directory
cd students/Frijol75/homework-5

# Create and activate virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required dependencies
pip install -r requirements.txt
```

---

## 🧪 Running Tests

```bash
# Run all tests with standard verbose output
pytest -v

# Run unit tests only
pytest tests/test_task_unit.py -v

# Run integration tests only
pytest tests/test_task_service_integration.py -v

# Run mocking tests only
pytest tests/test_mocking.py -v

# Run edge cases tests only
pytest tests/test_coverage_edge_cases.py -v
```

---

## 📊 Generating Coverage Reports

```bash
# Run tests with terminal and HTML coverage reporting
pytest --cov=src --cov-branch --cov-report=term-missing --cov-report=html

# View the interactive HTML report (macOS)
open htmlcov/index.html
```

---

## 📈 Coverage Summary

| Metric | Threshold | Achieved | Status |
| :--- | :---: | :---: | :---: |
| **Statement Coverage** | 80% | **100%** | ✅ Pass |
| **Branch Coverage** | 80% | **100%** | ✅ Pass |
| **Function Coverage** | 80% | **100%** | ✅ Pass |
| **Line Coverage** | 80% | **100%** | ✅ Pass |

### Coverage by File

| Module | Statements | Missing | Branches | Partial | Coverage |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `src/__init__.py` | 5 | 0 | 0 | 0 | **100%** |
| `src/notification_service.py` | 5 | 0 | 0 | 0 | **100%** |
| `src/task.py` | 78 | 0 | 34 | 0 | **100%** |
| `src/task_repository.py` | 21 | 0 | 0 | 0 | **100%** |
| `src/task_service.py` | 92 | 0 | 30 | 0 | **100%** |
| **TOTAL** | **201** | **0** | **64** | **0** | **100%** |

---

## 🗂 Project Structure

```
students/Frijol75/homework-5/
├── .gitignore                    # Excludes bytecode, coverage, and caches
├── pytest.ini                    # Pytest configuration with pythonpath = . src
├── requirements.txt              # Project testing dependencies
├── README.md                     # Documentation and instructions
├── src/
│   ├── __init__.py               # Exports package modules
│   ├── task.py                   # Task model, enums, validation, transitions
│   ├── task_repository.py        # Persistence layer interface (for mocking)
│   ├── notification_service.py   # External notification interface
│   └── task_service.py           # Core business logic and orchestration
├── tests/
│   ├── conftest.py               # Shared fixtures and FakeTaskRepository
│   ├── test_task_unit.py         # Unit tests for Task model (Part 1)
│   ├── test_task_service_integration.py # Integration test suite (Part 2)
│   ├── test_mocking.py           # Mocking, stubs, fakes, errors (Part 4)
│   └── test_coverage_edge_cases.py # Boundary and coverage edge cases (Part 3)
└── reports/
    ├── coverage-analysis.md      # Detailed coverage tables, analysis, strategy
    ├── analysis-report.md        # Comprehensive 400-600 word reflection report
    ├── reflection.md             # Personal testing reflection
    └── screenshots/
        ├── coverage-summary.png     # Terminal coverage output screenshot
        ├── coverage-html-report.png # HTML report screenshot
        └── test-execution.png       # Test suite execution screenshot
```

---

## 🌟 Key Features Implemented

- **Task Model with Validation**: Enforces title length boundaries (3-100 chars), future due dates, and auto-timestamps.
- **Strict State Machine**: Validates transitions (`TODO -> IN_PROGRESS -> DONE -> ARCHIVED`), prevents invalid backward or skip transitions, and treats `ARCHIVED` as terminal.
- **Overdue Detection**: Accurately flags overdue tasks while ignoring completed and archived tasks.
- **Priority Comparison**: Comparable priorities (`URGENT > HIGH > MEDIUM > LOW`).
- **Service Orchestration**: Decoupled architecture using dependency injection for `TaskRepository` and `NotificationService`.
- **Fault-Tolerant Workflows**: Gracefully handles external notification downtime without blocking core task operations.
- **Advanced Search & Filtering**: Multi-parameter search by title, status, priority, and date range.
- **Diverse Test Doubles**: Implements Mocks (interaction verification), Stubs (canned return values), and Fakes (`FakeTaskRepository`).

---

## 📋 Test Summary

- **Total Tests**: 67
- **Unit Tests**: 30
- **Integration Tests**: 17
- **Mocking & Isolation Tests**: 9
- **Edge Case Tests**: 11
- **Execution Time**: ~0.08 seconds
- **All Tests Passing**: ✅ 100%

---

## 👤 Author

- **Student**: Frijol75
- **Course**: Software Testing - Fall 2026
