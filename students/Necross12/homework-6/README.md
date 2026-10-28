# Homework 6: TDD Feature Development

Library Management System built with strict Test Driven Development (JavaScript + Jest).

## Prerequisites

- Node.js 22+

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

# Generate the HTML coverage report
npm run test:docs
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
homework-6/
├── src/
│   ├── book.js
│   ├── library.js
│   └── member.js
├── test/
│   ├── book.test.js
│   ├── library.test.js
│   └── member.test.js
├── docs/
│   ├── reflection.md
│   └── tdd-process.md
├── coverage/
├── package.json
└── README.md
```

## Test Summary

- **Total Tests**: 85
- **Unit Tests** (Book, Member): 39
- **Integration Tests** (Library): 46
- **Time**: under 2 s
- **All Tests Passing**: ✅

## Author

Diego Orozco Mólgora - Software Testing Fall 2026
