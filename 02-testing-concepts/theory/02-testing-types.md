# Software Testing Types

## Overview

Testing types describe **WHAT** you're testing - functionality, performance, security, etc.

## Functional vs Non-Functional

### Functional Testing
Tests **what the system does** - its features and functions.

**Question**: Does it do what it's supposed to do?

### Non-Functional Testing
Tests **how well the system performs** - quality attributes.

**Question**: How well does it do it?

---

## Key Functional Testing Types

### 1. Smoke Testing
**Quick check that basics work**
- After each build
- Broad but shallow
- Example: Can login? Homepage loads?

### 2. Sanity Testing
**Quick check of specific functionality**
- After bug fix
- Narrow but deeper
- Example: Did the fix work?

### 3. Regression Testing
**Verify existing features still work**
- After any change
- Catch unintended side effects
- Essential for maintenance

### 4. Integration Testing
**Test components working together**
- After unit testing
- Find interface defects

### 5. System Testing
**Test complete integrated system**
- After integration
- Verify end-to-end functionality

### 6. Acceptance Testing
**Verify business requirements met**
- Before deployment
- User/stakeholder approval

---

## Key Non-Functional Testing Types

### 1. Performance Testing
- Response time
- Throughput
- Resource usage
- Includes: Load, Stress, Spike, Endurance

### 2. Security Testing
- Find vulnerabilities
- Prevent attacks
- Protect data

### 3. Usability Testing
- User-friendliness
- Learning curve
- Satisfaction

### 4. Compatibility Testing
- Different browsers
- Operating systems
- Devices
- Screen sizes

---

## Quick Reference

| **Type** | **Tests** | **Priority** |
|----------|-----------|--------------|
| Functional | Features work | High |
| Regression | No breaks | High |
| Performance | Speed/load | Medium-High |
| Security | Vulnerabilities | High |
| Usability | User experience | Medium |

Next: [Testing Levels](./03-testing-levels.md)
