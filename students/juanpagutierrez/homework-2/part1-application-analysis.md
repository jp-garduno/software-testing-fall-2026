# Part 1: Application Selection & Analysis

## Application: BudgetWise - Personal Finance Manager

**Option Selected**: Option B - Hypothetical Application (Personal finance manager)

### Purpose

BudgetWise is a mobile and web application that helps individuals and households take control of their money. It connects to users' bank accounts and credit cards, automatically imports and categorizes transactions, and compares actual spending against user-defined budgets. Beyond tracking, BudgetWise helps users set savings goals (e.g., an emergency fund or a vacation), reminds them of upcoming bills so they avoid late fees, and gives them visual reports that turn raw transaction data into an understandable picture of their financial health. The core value proposition is reducing the mental overhead of manual budgeting by automating data collection while keeping the user in control of categorization and goals.

### Target Users

- **Individual users**: people who want to budget, save, and understand where their money goes without spreadsheets.
- **Couples and families**: users who share expenses and want a joint view of household spending, with support for multiple linked accounts under one budget.
- **Freelancers and gig workers**: users with irregular income who need to separate personal and business-like expenses and plan around variable cash flow.
- **Financially cautious/first-time budgeters**: users who need guardrails (alerts, reminders) more than advanced financial planning tools.

### Key Features

1. **Bank account linking and transaction sync** - Connects to banks and credit cards through a third-party aggregation API (e.g., Plaid-style) and automatically imports new transactions on a schedule.
2. **Budget creation and category-based expense tracking** - Users define monthly budgets per category (groceries, rent, entertainment, etc.) and the app tracks actual spend against each budget in real time.
3. **Bill reminders and recurring payment alerts** - Detects recurring charges (subscriptions, utilities, rent) and notifies users a configurable number of days before they are due.
4. **Financial goal setting and savings tracking** - Users create goals with a target amount and date; the app tracks progress and suggests monthly contributions.
5. **Spending analytics and visual dashboards** - Charts and summaries (by category, by month, by merchant) that let users see trends over time.
6. **Multi-currency support** - Users who hold accounts in more than one currency can view converted totals alongside native-currency transaction details.
7. **Secure authentication (biometric login / 2FA)** - Login via fingerprint/Face ID on mobile, with two-factor authentication as a fallback and a required step for sensitive actions like unlinking a bank account.

### Technology Stack

- **Client**: Mobile apps (iOS and Android) built with React Native, plus a companion responsive web app (React).
- **Backend**: Node.js/Express REST API, PostgreSQL as the primary data store, Redis for caching and session management.
- **Third-party integrations**: A bank-aggregation API (Plaid-style) for account linking and transaction retrieval, a push-notification service for bill reminders, and a currency-exchange-rate API for multi-currency conversion.
- **Infrastructure**: Hosted on AWS (ECS for the API, RDS for PostgreSQL), with CI/CD pipelines running automated test suites before deployment.

### Critical Functions

The following are mission-critical because a failure directly causes financial harm, loss of user trust, or regulatory exposure:

- **Bank account linking and transaction sync**: if sync fails silently or duplicates transactions, every downstream feature (budgets, analytics, goals) becomes inaccurate.
- **Balance and budget calculations**: incorrect arithmetic (e.g., wrong running totals, category sums, or currency conversion) can mislead users into overspending or missing bills.
- **Authentication and data security**: BudgetWise stores or brokers access to real bank credentials and transaction history, making it a high-value target; any breach has severe consequences for users.
- **Bill reminder notifications**: a missed or late reminder can cause a user to incur a real late fee or damage their credit, so reliability of the notification pipeline is essential.
