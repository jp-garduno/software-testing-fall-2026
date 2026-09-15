# Part 2: Testing Types Classification

Testing types are complementary perspectives. Each type below targets a distinct product risk and is exercised at the appropriate testing levels.

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verify that Nexo implements the stated business rules and user workflows, especially those that transform financial data.

**Examples**:

1. Importing a debit of MXN 250.50 decreases the correct account balance exactly once.
2. Splitting a MXN 900 transaction into MXN 500, MXN 250, and MXN 150 preserves the original total.
3. A budget alert is generated when spending crosses its configured 80% threshold, but not before.

**Priority**: Critical

**Justification**: Incorrect behavior can misrepresent a user's finances and invalidate the application's central purpose.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Confirm responsive behavior and stable throughput during morning synchronization peaks and month-end reporting.

**Examples**:

1. The dashboard API has a p95 response time below 1.5 seconds with 5,000 concurrent sessions.

2. A 10,000-row CSV import completes within 60 seconds without blocking interactive requests.
3. A 30-minute stress test at 150% expected peak load produces no data loss and returns to normal latency within five minutes.

**Priority**: High

**Justification**: Slow or unstable access prevents timely decisions, while overloaded retry workers can also amplify duplicate-import risk.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Protect credentials, tokens, financial records, exports, and account-management operations against unauthorized access or disclosure.

**Examples**:

1. Changing the transaction identifier in an authenticated request never exposes another user's record.
2. Expired, revoked, malformed, or wrong-audience access tokens are rejected by every protected endpoint.
3. CSV cells beginning with `=`, `+`, `-`, or `@` are neutralized so exported files cannot trigger spreadsheet-formula injection.

**Priority**: Critical

**Justification**: A breach creates severe privacy, legal, and reputational harm; authorization failures can expose an entire account history.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Determine whether people with different levels of financial literacy can understand balances, resolve sync errors, and control their data.

**Examples**:

1. At least 90% of representative participants create a first monthly budget without assistance in under three minutes.
2. Participants correctly explain whether a displayed amount is income, spending, or available budget.
3. A user can identify the affected bank and recover from an expired connection without contacting support.

**Priority**: High

**Justification**: A mathematically correct result still fails if users misinterpret it or cannot complete essential tasks.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Ensure changes to providers, calculation rules, and clients do not break previously working behavior.

**Examples**:

1. Re-run the golden dataset of balances and budgets after changing transaction categorization.
2. Re-run authentication, reauthorization, export, and deletion smoke suites after an identity-provider upgrade.
3. Verify historical transactions keep their value and category after a schema migration.

**Priority**: Critical

**Justification**: Financial rules are highly interconnected; a localized change can silently alter totals throughout the product.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Make critical financial tasks perceivable and operable for users with visual, motor, auditory, or cognitive disabilities.

**Examples**:

1. Complete sign-in, budget creation, transaction editing, and account deletion using only a keyboard.

2. Verify screen-reader names, roles, states, heading order, error summaries, and live announcements.
3. Confirm charts provide text equivalents and that gains, losses, and alerts are not communicated by color alone.

**Priority**: High

**Justification**: Accessibility is part of usable access to an essential service and must be designed into the primary journeys.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Verify consistent behavior across supported browsers, screen sizes, operating systems, locales, time zones, and interrupted mobile networks.

**Examples**:

1. Compare balance and budget results on the latest two versions of Chrome, Edge, Firefox, and Safari.
2. Verify MXN and USD formatting in Spanish and English without changing stored decimal values.
3. Interrupt and restore connectivity while editing a transaction; the UI must show the final server state without duplication.

**Priority**: High

**Justification**: Client-specific formatting or synchronization defects can present different financial truth to different users.

---

## Test Type: Reliability and Recovery Testing

**Category**: Non-Functional

**Purpose**: Demonstrate that Nexo preserves integrity during timeouts, retries, service restarts, partial failures, and restoration from backup.

**Examples**:

1. Retry the same provider page after a timeout and verify idempotency keys prevent duplicate transactions.
2. Restart the sync worker between persistence and acknowledgment and confirm processing resumes exactly once.
3. Restore a recent backup into an isolated environment and reconcile record counts, balances, and audit events against the recovery point.

**Priority**: Critical

**Justification**: External providers and networks inevitably fail; recovery must not corrupt or silently lose financial history.

---

## Test Type: Data Integrity Testing

**Category**: Functional

**Purpose**: Validate invariants across storage, API responses, derived reports, migrations, imports, and exports.

**Examples**:

1. The sum of category totals equals the month's total spending for the same account and date range.
2. Decimal values remain unchanged through CSV import, database storage, API serialization, and export.
3. A migration preserves transaction count, immutable external identifiers, ownership, timestamps, and calculated balances.

**Priority**: Critical

**Justification**: Silent inconsistency undermines every report even when individual screens appear to work.

---

## Test Type: Privacy Testing

**Category**: Non-Functional

**Purpose**: Verify data minimization, consent, retention, deletion, and safe observability across the complete data lifecycle.

**Examples**:

1. Revoking a bank connection stops future collection and removes the provider token while retaining only data covered by the displayed policy.
2. An account-deletion request makes user data unavailable within the promised window and propagates to search indexes, exports, and backups according to policy.
3. Logs, traces, analytics events, crash reports, and support views contain no raw tokens, full account numbers, or transaction descriptions.

**Priority**: Critical

**Justification**: Privacy defects can persist outside the main database and are difficult to remediate after sensitive data spreads.

## Cross-Type Exit Criteria

A release candidate may proceed only when all P0 scenarios pass, no unresolved critical or high-severity security finding exists, financial invariants pass against the golden dataset, performance objectives are met twice in a production-like environment, and product owners accept documented residual P1/P2 risks. A failed accessibility or privacy criterion in a critical journey blocks release just as a functional failure would.
