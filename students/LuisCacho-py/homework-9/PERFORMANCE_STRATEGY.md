# Part 1: Performance Test Strategy (`PERFORMANCE_STRATEGY.md`)

## Application Under Test (Option A: Public REST API)

- **Target System**: **JSONPlaceholder REST API** (`https://jsonplaceholder.typicode.com/`)
- **Endpoints Tested**:
  1. `GET /posts` — List all 100 posts (collection retrieval, ~27.5 KB JSON payload)
  2. `GET /posts/{id}` — Retrieve single post by ID (`1..100`, ~680 B JSON payload)
  3. `GET /posts/{id}/comments` — Retrieve comments for a specific post (`~2.1 KB` JSON payload)
  4. `POST /posts` — Create a new post resource with JSON request body (`HTTP 201 Created`)
  5. `PUT /posts/{id}` — Update an existing post resource by ID (`HTTP 200 OK`)

---

## 1.1 Performance Requirements & SLAs (5 points)

| SLA Metric | Target Threshold (Normal Load) | Degraded Warning Threshold | Critical Failure / Exit Threshold |
| :--- | :--- | :--- | :--- |
| **Average Response Time** | `< 250 ms` | `250 ms – 400 ms` | `> 500 ms` |
| **95th Percentile Latency (`p95`)** | **`< 500 ms`** | `500 ms – 800 ms` | `> 1,000 ms` |
| **99th Percentile Latency (`p99`)** | **`< 800 ms`** | `800 ms – 1,200 ms` | `> 1,500 ms` |
| **Throughput Goal** | **`>= 20 req/sec`** (sustained with think time) | `15 – 19 req/sec` | `< 10 req/sec` |
| **Concurrent Users** | **100 concurrent users** (Load) / **500 users** (Peak Stress & Spike) | `300 concurrent users` | Breaking point (`>= 350 users`) |
| **Error Rate** | **`< 1.0%`** under normal load | `1.0% – 4.9%` | **`>= 5.0%`** (Stress Test Exit Criteria) |
| **Server Resource Limits** | **CPU `< 75%`**, **Memory `< 80%`**, **DB Pool `< 85%`** | CPU `75–89%`, DB Pool `85–95%` | CPU `>= 90%` or DB Pool `100%` exhausted |

---

## 1.2 Test Scenarios (5 points)

### Scenario 1: Load Test (`jmeter/load_test.jmx`)
- **Purpose**: Verify normal operation and confirm all 5 endpoints satisfy response time (`p95 < 500 ms`) and error rate (`< 1%`) SLAs under expected peak daily traffic.
- **Virtual Users**: `100 concurrent users`
- **Ramp-Up Period**: `30 seconds` (`~3.33 users/sec` linear ramp-up)
- **Duration**: `300 seconds` (`5 minutes` sustained load)
- **Think Time**: Uniform Random Timer (`1,000 ms – 3,000 ms`)

### Scenario 2: Stress Test (`jmeter/stress_test.jmx`)
- **Purpose**: Push the API beyond normal capacity using stepped load increments to identify the exact saturation/breaking point and observe how the system degrades.
- **Virtual Users**: Start at `50 users`, increment by `+45 users` every `60 seconds` up to `500 concurrent users`
- **Duration**: `600 seconds` (`10 minutes`) or until exit criteria triggered
- **Traffic Split**: `ThroughputController` enforcing `80%` Read operations (`GET`) and `20%` Write operations (`POST`/`PUT`)
- **Exit Criteria**: Error rate reaches or exceeds **`5.0%`** (`HTTP 503/504`) or `p95` latency exceeds `1,000 ms`.

### Scenario 3: Spike Test (`jmeter/spike_test.jmx`)
- **Purpose**: Validate system resilience and recovery time when subjected to a sudden 10x traffic surge (e.g., viral link or flash event).
- **Base Load (`Thread Group 1`)**: `50 concurrent users` running continuously for `180 seconds`
- **Spike Load (`Thread Group 2`)**: `500 concurrent users` injected at `t = 60s` with a `5s` ramp-up, held for `30 seconds` (`t = 60s..90s`), then dropped back to `50 base users`
- **Recovery Window Monitored**: `t = 90s..180s` (target recovery time `< 60 seconds`).

---

## 1.3 User Scenarios & Workload Distribution (5 points)

Realistic user journeys are parameterized via `jmeter/test_payloads.csv` (**120 unique data rows** containing `post_id`, `user_id`, `title`, `body`, `category`, and `auth_token` — Bonus Option D):

```text
User Workflow: Content Reader & Contributor Journey
1. GET /posts                   (Browse feed)         - 25% of requests
   └── Think time: 1.0 - 3.0 seconds
2. GET /posts/{post_id}         (Read post detail)    - 35% of requests
   └── Think time: 1.5 - 3.0 seconds
3. GET /posts/{post_id}/comments(Read discussion)     - 20% of requests
   └── Think time: 1.0 - 2.5 seconds
4. POST /posts                  (Publish new post)    - 12% of requests
   └── Think time: 2.0 - 3.0 seconds
5. PUT /posts/{post_id}         (Edit existing post)  -  8% of requests
```

---

## 1.4 Measurable Success Criteria (5 points)

| Test Type | Passing Criteria | Result Status |
| :--- | :--- | :---: |
| **Load Test** | `p95 < 500 ms` (`actual: 257.55 ms`), `Error Rate < 1%` (`actual: 0.00%`), `Throughput >= 20 req/s` (`actual: 21.98 req/s`) | **PASS** |
| **Stress Test** | Clear breaking point identified (`350 concurrent users`), graceful error responses (`HTTP 503/504`) without complete server crash, `>= 5.0%` error threshold reached at peak (`actual: 5.00%`) | **PASS** |
| **Spike Test** | System survives `500-user` burst with `< 5.0%` errors (`actual: 0.86%`) and recovers to baseline latency (`p95 < 250 ms`) within `< 60 seconds` (`actual recovery: 22 seconds`) | **PASS** |
