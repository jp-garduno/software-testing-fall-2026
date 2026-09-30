# Part 2: Testing Types Classification

## Test Type: Functional Testing
**Category**: Functional
**Purpose**: Validate core ordering behavior.
**Examples**: 1. Search returns open restaurants. 2. Cart total includes tax and tip. 3. Paid checkout creates one order.
**Priority**: Critical
**Justification**: Ordering and payment are FoodHub’s primary value.

## Test Type: Performance Testing
**Category**: Non-Functional
**Purpose**: Keep peak-hour service responsive.
**Examples**: 1. Search responds under two seconds. 2. Checkout handles concurrent users. 3. Event queues do not grow during dinner rush.
**Priority**: High
**Justification**: Slow flows cause abandonment and late orders.

## Test Type: Security Testing
**Category**: Non-Functional
**Purpose**: Protect accounts, addresses, and payment data.
**Examples**: 1. Users cannot access another order. 2. Login throttles repeated attempts. 3. Invalid payment callbacks are rejected.
**Priority**: Critical
**Justification**: Fraud or data exposure is unacceptable.

## Test Type: Usability Testing
**Category**: Non-Functional
**Purpose**: Ensure users understand price and delivery choices.
**Examples**: 1. New users complete checkout. 2. Fees and tips are understood. 3. Cancellation rules are findable.
**Priority**: High
**Justification**: Confusion creates accidental orders and support contacts.

## Test Type: Regression Testing
**Category**: Functional
**Purpose**: Detect release side effects.
**Examples**: 1. New promotions preserve totals. 2. Assignment changes preserve notifications. 3. Auth upgrades preserve recovery.
**Priority**: High
**Justification**: Shared services change frequently.

## Test Type: Accessibility Testing
**Category**: Non-Functional
**Purpose**: Make ordering usable with assistive technology.
**Examples**: 1. Keyboard checkout works. 2. Screen readers announce cart changes. 3. Zoom and contrast preserve controls.
**Priority**: High
**Justification**: Accessibility is essential and reduces exclusion.

## Test Type: Compatibility Testing
**Category**: Non-Functional
**Purpose**: Support approved devices and browsers.
**Examples**: 1. Checkout works on Chrome, Safari, Firefox, Edge. 2. Mobile deep links open the order. 3. Wallet totals match receipts.
**Priority**: Medium
**Justification**: Impact depends on the supported usage matrix.

## Test Type: Reliability Testing
**Category**: Non-Functional
**Purpose**: Preserve a correct order state during failure.
**Examples**: 1. Network loss cannot duplicate a charge. 2. Notification outages retry safely. 3. Restaurant restart preserves accepted orders.
**Priority**: Critical
**Justification**: Recovery failures cause lost orders and refunds.
