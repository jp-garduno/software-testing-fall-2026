# Part 5: Risk Analysis & Test Prioritization

Exhaustive testing is impossible, so risk is what decides where the effort goes. Each risk below is scored, given a priority, and matched to a mitigation built from the types in Part 2 and the levels in Part 3.

**Scales used**:

- **Likelihood**: Low / Medium / High
- **Impact**: Low / Medium / High / Critical
- **Priority**: P0 (Critical) / P1 (High) / P2 (Medium) / P3 (Low)

## 5.1 Risk Matrix

| **Risk**                                                            | **Likelihood** | **Impact** | **Priority** | **Mitigation Strategy**                                                                           |
| ------------------------------------------------------------------- | -------------- | ---------- | ------------ | ------------------------------------------------------------------------------------------------- |
| Card or edit lost when two users act on the same card at once       | Medium         | Critical   | P0           | Two-client end-to-end scenarios, run with injected latency and packet loss                        |
| Private board readable by a non-member through the API or WebSocket | Low            | Critical   | P0           | Authorization tests on every endpoint and channel, plus penetration testing                       |
| Board state diverges after a dropped WebSocket connection           | High           | High       | P0           | Recovery testing with forced disconnects and reconnection resync scenarios                        |
| Offline mobile edits silently dropped on reconnect                  | Medium         | High       | P1           | Integration tests on the offline queue, and mobile end-to-end runs with airplane mode mid-edit    |
| Butler automation rule mass-modifies or loops over cards            | Low            | High       | P1           | Unit tests on rule triggers, including self-trigger prevention, and a staged rollout of changes   |
| Large boards load too slowly or freeze the browser tab              | Medium         | High       | P1           | Load and endurance testing on 5,000-card boards, with a 95th-percentile load budget as a gate     |
| Regression in the card detail view caused by an unrelated change    | High           | Medium     | P2           | Full regression suite on every PR touching shared components, smoke suite on every build          |
| Search results stale or missing after the Elasticsearch index lags  | Medium         | Medium     | P2           | Integration tests asserting the agreed index lag window, plus monitoring of index latency in prod |

## 5.2 Testing Priority Order

1. **Concurrency and sync-integrity testing** (P0) - two-client end-to-end scenarios under degraded network conditions. This protects the write path, and silent data loss is the failure users forgive least.
2. **Permission and authorization testing** (P0) - every endpoint and WebSocket channel, enforced server-side. A leak exposes confidential company data with no rollback.
3. **Reconnection and recovery testing** (P0) - forced disconnects and resync. Dropped connections are an everyday condition, so high likelihood meets high impact.
4. **Offline and mobile queue testing** (P1) - queued edits applied correctly on reconnect, since a failure here looks identical to data loss from the user's side.
5. **Automation rule testing** (P1) - Butler acts with nobody watching, so a faulty rule can damage hundreds of cards before anyone notices.
6. **Performance testing on large boards** (P1) - load and endurance profiles, because the biggest boards belong to the paying customers.
7. **Regression and smoke suites** (P2) - run continuously to catch collateral breakage cheaply.
8. **Search, compatibility and accessibility sweeps** (P2) - scheduled per release rather than per commit, since their failures are visible and recoverable.

If a release cycle is compressed, activities 1-3 are non-negotiable, 4-6 are cut down to their highest-value subset, and 7-8 fall back to production monitoring until the next cycle.
