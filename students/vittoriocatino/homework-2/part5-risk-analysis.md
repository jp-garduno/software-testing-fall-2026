# Part 5: Risk Analysis & Test Prioritization

## 5.1 Risk Matrix

| Risk | Likelihood | Impact | Priority | Mitigation Strategy |
| --- | --- | --- | --- | --- |
| Payment succeeds but no order is created, or a retry duplicates a charge. | Medium | Critical | P0 | Idempotency keys, webhook tests, reconciliation, recovery scenarios. |
| Incorrect total from tax, fees, tip, or promotions. | Medium | High | P1 | Calculation boundaries, pricing contracts, receipt comparison. |
| Unauthorized access to addresses, orders, or support tools. | Medium | Critical | P0 | Authorization checks, security scans, audit logs, penetration tests. |
| Peak demand slows checkout or grows queues. | High | High | P1 | Load, stress, soak, capacity, and queue tests. |
| Stale inventory accepts an order the restaurant cannot prepare. | High | High | P1 | Sync tests, timestamp validation, substitutions, monitoring. |
| Inaccurate courier status or location causes missed handoff. | Medium | High | P1 | Network-loss, event-ordering, GPS permission, fallback tests. |
| Inaccessible or unclear checkout reduces completion. | Medium | Medium | P2 | Usability sessions, keyboard/screen-reader, contrast, funnel tests. |
| Notifications fail or arrive late. | Medium | Medium | P2 | Provider sandbox, retry/DLQ, in-app fallback, alerts. |

## 5.2 Testing Priority Order
1. P0 payment integrity and security: authorization, idempotency, webhooks, refunds, authentication, object-level access.
2. P1 order creation and pricing: inventory, calculations, receipts, cart validation.
3. P1 fulfillment synchronization: restaurant acceptance, courier assignment, status and cancellations.
4. P1 performance and resilience: peak load, timeouts, retries, queues, recovery.
5. P2 usability and accessibility: fee clarity, errors, keyboard/screen reader, first-order comprehension.
6. P2 compatibility and notification polish: supported browsers/devices and delivery fallback.

## Review Cadence
Review the matrix at planning, after incidents, and whenever payment, identity, pricing, or fulfillment dependencies change.
