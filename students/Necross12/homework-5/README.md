# Homework 5: White Box Testing - TaskFlow System

## Description

Comprehensive white box test suite for a task management system demonstrating unit testing, integration testing, code coverage analysis, and mocking techniques.

## Objectives

- Achieve >80% statement coverage and >80% branch coverage
- Implement isolated unit tests for all model methods
- Create integration tests with proper mocking
- Analyze and document coverage gaps

## Prerequisites

- Node.js 22+
- Jest

## Installation

```bash
npm install
```

## Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Watch mode
npm test -- --watch
```

## Coverage Reports

After running tests with coverage, open the HTML report:

```bash
# Windows (PowerShell)
Start-Process coverage/lcov-report/index.html

# macOS
open coverage/lcov-report/index.html
```

## Current Coverage

- **Statement Coverage**: 100%
- **Branch Coverage**: 100%
- **Function Coverage**: 100%
- **Line Coverage**: 100%

## Project Structure

```
homework-5/
├── src/                 # Production code
│   ├── task.js
│   ├── taskService.js
│   ├── taskRepository.js         # Interface, replaced by mocks in tests
│   └── notificationService.js    # Interface, replaced by mocks in tests
├── tests/               # Test suite
│   ├── helpers/mockTask.js              # Mock factories and in-memory fake repository
│   ├── task.test.js                     # Unit tests (Task model)
│   ├── taskService.test.js              # Integration tests (TaskService)
│   ├── mocking.test.js                  # Mocks, stubs, fakes, spies and fake timers
│   └── coverageEdgeCases.test.js        # Branch fallback and interface contracts
├── reports/             # Coverage analysis, reports and screenshots
├── jest.config.js
└── package.json
```

## Features Implemented

- ✅ Task model with validation and state management
- ✅ TaskService with business logic
- ✅ Complete unit test suite (15+ tests)
- ✅ Integration tests with mocking (10+ tests)
- ✅ Mocks, stubs, fakes, spies and fake timers
- ✅ Comprehensive coverage analysis
- ✅ Error scenario testing

## Test Summary

- **Total Tests**: 71
- **Unit Tests**: 45
- **Integration Tests**: 26
- **All Tests Passing**: ✅

## Author

Diego Orozco Mólgora - Software Testing Fall 2026
