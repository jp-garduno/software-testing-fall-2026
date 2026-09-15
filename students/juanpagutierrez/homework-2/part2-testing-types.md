# Part 2: Testing Types Classification

Nine testing types are identified for BudgetWise (one more than the required minimum of 8, to cover accessibility as a bonus type given its relevance to a financial app used by a broad population).

## Test Type: Functional Testing

**Category**: Functional

**Purpose**: Verify that every feature behaves according to its requirements. For BudgetWise, this means users can reliably link accounts, categorize transactions, set budgets, and track goals exactly as specified.

**Examples**:

1. Linking a bank account successfully imports the last 90 days of transactions.
2. Creating a budget category and assigning a monthly limit correctly reduces the "remaining budget" as transactions are categorized into it.
3. Marking a goal as complete when the saved amount reaches the target amount.

**Priority**: Critical

**Justification**: These are the core features that define the product. If account linking or budget tracking doesn't work, BudgetWise has no value to users regardless of how polished anything else is.

---

## Test Type: Performance Testing

**Category**: Non-Functional

**Purpose**: Ensure the app remains responsive as transaction history grows and during predictable usage spikes (e.g., beginning of the month when budgets reset and many users check their dashboards).

**Examples**:

1. Dashboard with 5,000+ historical transactions loads and renders charts in under 2 seconds.
2. Transaction sync for a newly linked account with 12 months of history completes in under 10 seconds.
3. API sustains 5,000 concurrent active sessions during a simulated "start of month" traffic spike without response times exceeding 1 second.

**Priority**: High

**Justification**: Users check budgets at predictable, concentrated times (paydays, month start). Slow performance at these moments erodes trust and increases abandonment.

---

## Test Type: Security Testing

**Category**: Non-Functional

**Purpose**: Protect sensitive financial data (bank credentials via the aggregation API, transaction history, personal identifiers) from unauthorized access, leakage, or tampering.

**Examples**:

1. Bank access tokens are encrypted at rest and never returned in any API response body or client-side log.
2. A user cannot access another user's accounts, transactions, or goals by manipulating request IDs (authorization/IDOR check).
3. Two-factor authentication is enforced before a user can unlink a bank account or export transaction data.

**Priority**: Critical

**Justification**: BudgetWise handles real financial data. A security failure could mean stolen credentials, financial fraud, and severe reputational and legal consequences.

---

## Test Type: Usability Testing

**Category**: Non-Functional

**Purpose**: Confirm that budgeting workflows are intuitive for users who are not financial experts, since the target audience includes first-time budgeters.

**Examples**:

1. A new user can create their first budget within 3 minutes without external help, measured in a moderated usability session.
2. Category icons and colors are visually distinct enough that users correctly identify categories in under 2 seconds.
3. Error messages during account linking (e.g., wrong bank credentials) clearly explain what went wrong and what to do next.

**Priority**: High

**Justification**: If budgeting feels confusing or intimidating, the target audience of casual/first-time budgeters will abandon the app, even if it is technically correct.

---

## Test Type: Regression Testing

**Category**: Functional

**Purpose**: Ensure that new features or bug fixes do not break existing, previously working functionality, especially calculation logic that many features depend on.

**Examples**:

1. After adding multi-currency support, existing single-currency budgets still calculate totals correctly.
2. After a bill-reminder feature update, previously scheduled reminders still fire at the correct time.
3. After a UI redesign of the dashboard, all existing chart data still maps to the correct categories and amounts.

**Priority**: High

**Justification**: BudgetWise's features are deeply interconnected (transactions feed budgets, goals, and analytics). A change in one area can silently break another; regression testing is what protects against build-breaking-build errors.

---

## Test Type: Compatibility Testing

**Category**: Non-Functional

**Purpose**: Verify BudgetWise works correctly across the range of devices, OS versions, and browsers its users actually have, since it ships on iOS, Android, and web.

**Examples**:

1. Biometric login (Face ID / fingerprint) works correctly on the last 3 major iOS and Android versions.
2. The responsive web app renders budget charts correctly on Chrome, Safari, Firefox, and Edge.
3. Push notifications for bill reminders are delivered correctly on both Android and iOS notification systems.

**Priority**: Medium

**Justification**: Compatibility issues affect a subset of users rather than everyone, but with a broad user base across old and new devices, uncaught issues can still impact a meaningful share of the audience.

---

## Test Type: Reliability Testing

**Category**: Non-Functional

**Purpose**: Confirm the app behaves consistently over extended use and recovers gracefully from failures such as a dropped network connection or a failed bank sync.

**Examples**:

1. If a transaction sync fails midway (e.g., bank API timeout), no duplicate or partial transactions are recorded, and the sync retries automatically.
2. The app runs continuously for 72 hours under simulated background sync load without memory leaks or crashes.
3. If the app loses internet connectivity while a user is editing a budget, unsaved changes are preserved locally and synced once connectivity returns.

**Priority**: High

**Justification**: Users trust BudgetWise to hold an accurate financial record. Any inconsistency after a failure (missing data, duplicated transactions) directly undermines that trust.

---

## Test Type: Data Integrity Testing

**Category**: Functional

**Purpose**: Verify that financial data remains accurate and consistent across sync, storage, calculation, and currency conversion, since even small arithmetic errors compound into materially wrong balances.

**Examples**:

1. The sum of all categorized transactions in a budget period always equals the total spend shown on the dashboard, down to the cent.
2. Currency conversion for a multi-currency account uses the exchange rate at the time of the transaction, not the current rate, and is reproducible.
3. Deleting a duplicate transaction correctly recalculates all dependent budget totals and goal progress.

**Priority**: Critical

**Justification**: BudgetWise's entire value proposition depends on numbers being correct. Silent data-integrity bugs are worse than visible crashes because users may make financial decisions based on wrong information without knowing it.

---

## Test Type: Accessibility Testing

**Category**: Non-Functional

**Purpose**: Ensure BudgetWise is usable by people with visual, motor, or cognitive impairments, since financial independence tools should not exclude users who rely on assistive technology.

**Examples**:

1. All screens are navigable and operable using a screen reader (VoiceOver/TalkBack), with meaningful labels on charts and buttons.
2. Color is never the only way information is conveyed (e.g., "over budget" is marked with an icon and text, not just red color).
3. All interactive elements meet minimum touch-target size and color-contrast ratio (WCAG AA) requirements.

**Priority**: Medium

**Justification**: Accessibility is not exercised by every user, but it is a legal and ethical requirement in many markets, and excluding users with disabilities from managing their own finances is a meaningful harm.
