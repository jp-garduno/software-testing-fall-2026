# Performance Test Design

## Identifying Requirements

### Functional Requirements

- Which features/APIs to test
- Expected user workflows
- Business-critical paths

### Non-Functional Requirements

- **Response time**: < 2s for page load
- **Throughput**: 1000 requests/second
- **Concurrent users**: 5000 simultaneous
- **Availability**: 99.9% uptime
- **Error rate**: < 0.1%

## Test Scenarios

### 1. Normal Load

Typical business day traffic.

**Example**: E-commerce site

- 1000 users
- 70% browsing, 20% search, 10% checkout
- Duration: 1 hour

### 2. Peak Load

Maximum expected traffic.

**Example**: Black Friday

- 10,000 users
- Same ratios
- Duration: 4 hours

### 3. Stress Load

Beyond maximum capacity.

**Example**: Finding breaking point

- Start: 1000 users
- Increase: +500 every 5 minutes
- Stop: When error rate > 5%

## Load Patterns

### Constant Load

```
Users
1000 |████████████████
     |________________
     0     30    60 min
```

### Ramp-Up

```
Users
1000 |        /█████████
     |      /
  0  |____/___________
     0     30    60 min
```

### Step Load

```
Users
1000 |      ████
 500 |   ███
     |███
     0     30    60 min
```

### Spike

```
Users
5000 |    ██
     |   █  █
1000 |███    ███
     0     30    60 min
```

## User Think Time

Pauses between actions (realistic behavior).

- **Fast**: 1-3 seconds
- **Normal**: 3-10 seconds
- **Slow**: 10-30 seconds

## Test Data

- **Unique**: Each user different data
- **Realistic**: Production-like values
- **Sufficient**: Enough for all users
- **Clean**: Reset between runs

## Next: [03-jmeter-fundamentals.md](./03-jmeter-fundamentals.md)
