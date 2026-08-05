# Introduction to Performance Testing

## What is Performance Testing?

**Performance Testing** evaluates how a system performs under various conditions - speed, responsiveness, stability, and resource usage under different workloads.

## Why Performance Matters

- **User Experience**: Slow apps lose users (53% abandon sites that take >3s to load)
- **Business Impact**: Amazon found every 100ms delay costs 1% in sales
- **Scalability**: Know your limits before you hit them
- **Cost**: Over-provisioned resources waste money

## Types of Performance Testing

### 1. Load Testing

Tests system behavior under **expected load**.

**Example**: 1000 concurrent users browsing an e-commerce site.

**Goal**: Verify response times and throughput meet requirements.

### 2. Stress Testing

Pushes system **beyond normal capacity** to find breaking point.

**Example**: Gradually increase from 1000 to 10,000 users until system fails.

**Goal**: Identify maximum capacity and how gracefully system degrades.

### 3. Spike Testing

Tests **sudden dramatic increase** in load.

**Example**: Black Friday sale - traffic jumps from 100 to 10,000 users instantly.

**Goal**: Validate system handles traffic spikes without crashing.

### 4. Endurance Testing (Soak Testing)

Tests system over **extended period** (8-24+ hours).

**Example**: Run with 500 users continuously for 24 hours.

**Goal**: Identify memory leaks, resource depletion, degradation over time.

### 5. Scalability Testing

Tests system's ability to **scale up/down**.

**Example**: Add more servers and verify throughput increases proportionally.

**Goal**: Validate horizontal/vertical scaling strategies.

### 6. Volume Testing

Tests system with **large amounts of data**.

**Example**: Database with 10 million records.

**Goal**: Verify performance with production-scale data.

## Key Performance Metrics

### Response Time

Time from request to response.

- **Average**: Mean response time
- **Median (50th percentile)**: Half faster, half slower
- **90th percentile**: 90% of requests faster
- **95th/99th percentile**: Catch outliers

**Targets**:

- Critical pages: < 1s
- API calls: < 200ms
- Database queries: < 100ms

### Throughput

Requests processed per unit time.

- **Requests/second**: How many requests handled
- **Transactions/second**: Completed business operations
- **Data transfer**: MB/s or GB/s

### Error Rate

Percentage of failed requests.

**Target**: < 0.1% under normal load, < 1% under stress

### Resource Utilization

- **CPU**: % utilization (target < 70-80%)
- **Memory**: RAM usage (watch for leaks)
- **Disk I/O**: Read/write operations
- **Network**: Bandwidth usage

### Concurrent Users

Number of simultaneous active users.

## Performance Testing Process

1. **Define Requirements**: Response time, throughput, capacity targets
2. **Identify Scenarios**: User journeys to test
3. **Design Tests**: Load patterns, ramp-up, duration
4. **Prepare Environment**: Production-like setup
5. **Execute Tests**: Run and monitor
6. **Analyze Results**: Identify bottlenecks
7. **Optimize**: Fix issues
8. **Retest**: Validate improvements
9. **Report**: Document findings

## Common Performance Issues

### Application Layer

- **N+1 queries**: Multiple database calls in loop
- **No caching**: Recalculating same data
- **Synchronous operations**: Blocking calls
- **Memory leaks**: Unreleased resources

### Database Layer

- **Missing indexes**: Full table scans
- **Slow queries**: Complex joins, subqueries
- **Lock contention**: Concurrent updates
- **Connection pool exhaustion**: Too few connections

### Network Layer

- **Latency**: Geographic distance
- **Bandwidth**: Insufficient capacity
- **DNS lookups**: Too many external calls
- **Large payloads**: Uncompressed responses

### Infrastructure Layer

- **Insufficient resources**: CPU, RAM, disk
- **No load balancing**: Single point of failure
- **Misconfiguration**: Poor tuning
- **Network bottlenecks**: Switch/router limits

## Best Practices

1. **Test early and often**: Don't wait until production
2. **Use production-like environment**: Realistic hardware/network
3. **Start small, scale up**: Baseline → normal → peak → stress
4. **Monitor everything**: App, DB, infra metrics
5. **Isolate bottlenecks**: Test components individually
6. **Test realistic scenarios**: Actual user behavior
7. **Automate**: CI/CD integration
8. **Set SLAs**: Define acceptable performance

## Tools Overview

- **JMeter**: Java-based, GUI and CLI, industry standard
- **Locust**: Python-based, code-as-config
- **k6**: JavaScript-based, modern, developer-friendly
- **Gatling**: Scala-based, great for CI/CD
- **Artillery**: Node.js-based, simple YAML config

## Next: [02-test-design.md](./02-test-design.md)
