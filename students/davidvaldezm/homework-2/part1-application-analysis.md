# Part 1: Application Selection and Analysis

## Application: Nexo — Personal Finance Manager

### Purpose

Nexo is a hypothetical personal finance application available on the web and on iOS and Android. It gives people one place to understand cash flow, plan budgets, and make informed financial decisions. A user may connect bank and credit-card accounts through an open-banking provider or enter transactions manually. Nexo normalizes imported records, categorizes spending, calculates balances and budget progress, displays trends, and sends alerts when unusual activity or a budget threshold is detected. It does not move money or provide investment advice; it is a read-oriented planning tool whose value depends on accuracy, privacy, and clarity.

### Target Users

The main users are adults who manage one or more personal accounts, including students learning to budget, households monitoring shared expenses, freelancers separating variable income from expenses, and privacy-conscious users who prefer manual entry. A support team investigates synchronization problems, while operations and security teams monitor provider health, suspicious access, and data-protection controls. Users vary greatly in financial literacy, technical confidence, language, vision, and motor ability, so the interface must explain financial information without relying on expert terminology or color alone.

### Key Features

1. Registration, sign-in, multi-factor authentication, session management, and account recovery.
2. Secure connection and reauthorization of bank and credit-card accounts.
3. Automatic synchronization, deduplication, and reconciliation of transactions.
4. Manual creation, editing, splitting, categorization, and deletion of transactions.
5. Monthly and category-based budgets with threshold alerts.
6. Dashboard views for net cash flow, balances, trends, and upcoming recurring expenses.
7. Search, filters, custom categories, tags, and transaction notes.
8. CSV import and export, plus portable account-data export.
9. Notifications for unusual spending, synchronization failures, and budget limits.
10. Consent controls, device/session history, data-retention settings, and account deletion.

### Technology Stack

The assumed client stack is React and TypeScript for the responsive web application and React Native for mobile clients. A REST/JSON API implemented with Java and Spring Boot serves both clients. PostgreSQL stores transactional application data, Redis supports short-lived sessions and caching, and an encrypted object store holds generated exports. External integrations include an open-banking aggregator, email/push notification providers, and an identity provider supporting OAuth 2.0/OIDC. Services run in containers behind an API gateway, with centralized logs, metrics, traces, secret management, and continuous delivery. These are planning assumptions, not claims about a real product.

### Critical Functions

Financial data ingestion and calculation are mission-critical: a missing, duplicated, stale, or mis-signed transaction can produce a false balance and lead to a harmful decision. Authentication, authorization, encryption, consent, and deletion are equally critical because transaction histories reveal sensitive personal behavior. Bank synchronization must be idempotent and recover safely after provider timeouts. Budget totals and currency rounding must remain consistent across dashboards, exports, time zones, and month boundaries. Recovery and reauthorization flows also matter because security that locks out legitimate users destroys availability.

The main quality risks are therefore financial integrity, confidentiality, recoverability, and understandable presentation. Convenience features such as custom tags remain valuable but receive less testing effort than authorization boundaries, synchronization, calculations, deletion, and data export. Every critical action should be observable through privacy-safe audit events so failures can be detected without logging account numbers, tokens, or transaction descriptions.

### Quality Objectives and Constraints

- Correctness: balances and budget totals use deterministic decimal arithmetic and documented rounding rules.
- Security: least-privilege access, protected secrets, encrypted transport/storage, and auditable consent.
- Reliability: retries never duplicate records; interrupted synchronization can resume safely.
- Performance: the primary dashboard meets its service objective under expected peak load.
- Accessibility: critical journeys target WCAG 2.2 AA behavior.
- Compatibility: current major browsers and supported iOS/Android versions produce equivalent financial results.
