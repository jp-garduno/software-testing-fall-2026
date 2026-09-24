# SecureBank Black Box Testing Analysis

## Introduction

This assignment focused on applying black box testing techniques to the SecureBank banking system. The objective was to design and execute tests based on the expected behavior of the system rather than its internal implementation. Four techniques were used: Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing, and State Transition Testing.

Each technique was useful for identifying different types of test scenarios. Together, they provided broader coverage than relying only on normal input/output testing.

## Equivalence Partitioning

Equivalence Partitioning was useful for dividing input values into groups that should behave similarly. Instead of testing every possible value, representative values were selected from valid and invalid partitions.

For example, transfer amounts were divided into valid positive amounts, zero values, negative values, amounts above the daily transfer limit, and amounts greater than the available balance. Similar partitions were considered for account types, initial balances, deposits, and payees.

This technique reduced the number of tests required while still covering significantly different categories of behavior. It was especially useful for detecting validation errors because each partition represented a different business rule.

One limitation is that Equivalence Partitioning does not focus strongly on values located directly at the limits of a valid range. For this reason, Boundary Value Analysis was also necessary.

## Boundary Value Analysis

Boundary Value Analysis focused on values immediately below, at, and immediately above important limits. This was particularly relevant for SecureBank because many banking rules are based on numerical thresholds.

Examples include the minimum valid transfer amount, the $5,000 Checking daily transfer limit, the $2,000 Savings transfer limit, minimum account balances, and monthly fee waiver thresholds.

Testing these values was important because errors frequently occur around comparison operators such as `<`, `<=`, `>` and `>=`. A system may work correctly for ordinary values but behave incorrectly exactly at a limit.

For example, testing $4,999.99, $5,000.00, and $5,000.01 made it possible to verify the Checking daily transfer limit precisely.

## Decision Table Testing

Decision Table Testing was useful when the result of an operation depended on multiple conditions simultaneously.

Transfer validation depends on conditions such as sufficient funds, the daily transfer limit, and the account state. Monthly fee processing depends on the account type, account balance, and fee waiver threshold. Bill payments also require a valid payee, a positive amount, sufficient funds, and an active account.

Representing these combinations in decision tables made the business rules easier to understand and prevented important combinations from being overlooked.

This technique was particularly valuable because individual conditions may appear correct when tested independently while unexpected behavior can occur when several conditions interact.

## State Transition Testing

State Transition Testing was used to verify the lifecycle of a bank account. SecureBank accounts may be Active, Suspended, Frozen, or Closed.

The tests verified valid transitions such as Active to Frozen, Frozen to Active, Active to Suspended, and Suspended to Active. They also verified invalid or restricted operations, such as attempting transactions on a Closed or Frozen account.

This technique was important because the expected result of an operation may depend on the current state of the account. The same operation can therefore produce different results depending on the account state.

## Test Results and Coverage

The final automated test suite contained 40 tests, and all 40 tests passed successfully.

Initial execution showed that several branches were not covered. Additional cases were then added for invalid account creation, deposits to frozen accounts, invalid state transitions, monthly fee scenarios, and bill payment conditions.

After these additional tests were implemented, the final test suite achieved 100% statement and branch coverage according to pytest-cov.

Coverage alone does not guarantee that a system is completely correct, but it helped identify behaviors that had not yet been exercised by the test suite.

## Conclusion

The four black box techniques complemented each other. Equivalence Partitioning reduced large input spaces, Boundary Value Analysis examined critical numerical limits, Decision Tables tested combinations of business conditions, and State Transition Testing validated account behavior across different states.

The assignment demonstrated that systematic test design can identify scenarios that might easily be missed when tests are created only from intuition. Using several techniques together resulted in a more complete and structured test suite for SecureBank.