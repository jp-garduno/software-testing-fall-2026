# Black Box Testing Analysis Report

## Executive Summary
This report analyzes the application of four distinct black-box testing techniques—Equivalence Partitioning (EP), Boundary Value Analysis (BVA), Decision Tables (DT), and State Transition Testing (STT)—applied to the SecureBank Online Banking System. The primary objective was to ensure that the core banking functionalities, such as money transfers, fee processing, and account management, behave reliably under both typical and edge-case conditions without knowing the internal implementation details of the system.

## Technique Effectiveness

### Equivalence Partitioning (EP)
Equivalence Partitioning was highly effective at drastically reducing the number of necessary test cases while maintaining broad coverage. By categorizing inputs into valid and invalid classes (e.g., negative transfer amounts vs. positive transfer amounts), I was able to test the system's baseline functionality quickly. I found that this technique is easiest to apply to simple numeric inputs. However, its main limitation is that it tends to miss edge cases located exactly at the boundaries of these partitions.

### Boundary Value Analysis (BVA)
Boundary Value Analysis proved to be the most critical technique for finding potential off-by-one errors. By focusing specifically on the edges of the equivalence classes—such as testing a transfer of exactly $0.01, or trying to transfer $5,000.01 against a $5,000.00 limit—BVA revealed exactly how the system behaves at its most vulnerable points. BVA gave me the most confidence in the numerical reliability of the banking system, as financial software is notorious for failing at exact boundary thresholds. 

### Decision Tables
Decision tables helped visualize and manage the complex business rules of the SecureBank system. When multiple conditions interacted (e.g., checking if an account has sufficient funds AND is within the daily limit AND is currently in an Active state), it became difficult to track all permutations mentally. The decision table matrix made it straightforward to map these conditions to specific actions. I discovered that this technique guarantees comprehensive coverage of complex logical requirements that other techniques might completely ignore.

### State Transition Testing
State testing was crucial for ensuring that the lifecycle of a bank account was secure. A banking system's security relies heavily on state management. Without this technique, I would have likely missed validating what happens when an account goes from "Active" to "Suspended" due to fees, or ensuring that a "Closed" account cannot be reopened. This technique was perhaps the hardest to model initially but provided the deepest systemic validation.

## Coverage Comparison

| Technique | Primary Focus | System Coverage | Identified Overlaps |
| :--- | :--- | :--- | :--- |
| **EP** | General Input Validation | ~60% | Overlaps with BVA on mid-range valid inputs. |
| **BVA** | Numerical Limits | ~85% (Math Logic) | Overlaps with EP at boundary edges. |
| **Decision Tables** | Business Logic Rules | ~90% (Conditionals) | Integrates EP inputs into complex scenarios. |
| **State Transitions** | Account Lifecycle | ~95% (State paths) | Unique coverage of sequential actions. |

While each technique covers different aspects, combining them provides a robust safety net. EP and BVA are excellent for single-input validation, while Decision Tables and State Transitions excel at multi-variable and sequential validations. There were very few gaps left, although performance or concurrent transaction testing would require different methodologies entirely.

## Real-World Application
In a professional setting, I would apply these techniques systematically during the test planning phase before any code is even written. The banking domain particularly benefits from Decision Tables and BVA, as financial regulations require strict adherence to limits, fees, and state-based permissions. I would prioritize Boundary Value Analysis to prevent critical financial calculation errors, combined with Decision Tables to ensure complex compliance rules are met.

## Recommendations
For future testing of similar systems, I would recommend integrating automated property-based testing alongside these static black-box techniques to generate thousands of random inputs automatically. Additionally, the test design could be improved by incorporating Negative State Transition testing (attempting invalid transitions explicitly). I would also recommend adding concurrency testing to ensure that race conditions do not allow a user to bypass transfer limits by making simultaneous requests.

## Lessons Learned
The most important insight was that no single black-box technique is sufficient on its own. While EP provides a good foundation, it must be paired with BVA to catch edge-case bugs, and complex enterprise software demands Decision Tables to prevent logical loopholes.