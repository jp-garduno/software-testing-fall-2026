# Homework 9: Performance Test Strategy & Execution

**Due**: Before Exam 3 (Week 16)  
**Points**: 110 (100 base + 10 bonus)

## Overview

Design and execute a comprehensive performance testing strategy for a web application. Create JMeter test plans, execute load/stress/spike tests, analyze results, and provide performance optimization recommendations.

## Application Under Test

Choose ONE of the following:

### Option A: Public API (Recommended)

**JSONPlaceholder** - https://jsonplaceholder.typicode.com/

Endpoints to test:

- GET /posts (list all posts)
- GET /posts/1 (get single post)
- GET /posts/1/comments (get post comments)
- POST /posts (create post)
- PUT /posts/1 (update post)

### Option B: Your Own Application

Use Team Project application or personal project with REST API.

**Requirements**:

- Must have at least 3 different endpoints
- Must be accessible for testing
- Document base URL and endpoints

## Part 1: Performance Test Strategy (20 points)

Create **PERFORMANCE_STRATEGY.md** document:

### 1.1 Performance Requirements (5 points)

Define:

- **Response Time Targets**: e.g., "95th percentile < 500ms"
- **Throughput Goals**: e.g., "500 requests/second"
- **Concurrent Users**: e.g., "Support 1000 concurrent users"
- **Error Rate**: e.g., "< 1% under load"
- **Resource Limits**: e.g., "CPU < 80%"

### 1.2 Test Scenarios (5 points)

Design 3 test scenarios:

1. **Load Test**

   - Purpose: Verify normal operation
   - Users: [specify]
   - Duration: [specify]
   - Load pattern: Ramp-up

2. **Stress Test**

   - Purpose: Find breaking point
   - Users: [start] to [max]
   - Increment: [step size]
   - Exit criteria: Error rate > 5%

3. **Spike Test**
   - Purpose: Handle sudden traffic
   - Base users: [specify]
   - Spike users: [specify]
   - Spike duration: [specify]

### 1.3 User Scenarios (5 points)

Define realistic user workflows:

**Example**:

```
User Workflow: Browse and Read
1. GET /posts (list)          - 30% of requests
2. Think time: 2-5 seconds
3. GET /posts/{id} (detail)   - 50% of requests
4. Think time: 3-8 seconds
5. GET /posts/{id}/comments   - 20% of requests
```

### 1.4 Success Criteria (5 points)

Define what "passing" means:

- Load test: All targets met
- Stress test: Graceful degradation
- Spike test: Recovery < 60s

## Part 2: JMeter Test Plans (40 points)

Create 3 JMeter test plans (.jmx files):

### 2.1 Load Test (15 points)

**load_test.jmx**

Requirements:

- Thread Group with realistic user count
- HTTP Request Samplers for each endpoint
- HTTP Request Defaults (base URL)
- CSV Data Set (if using parameters)
- Timers for think time
- Response Assertions (status code 200)
- Duration Assertion (< target)
- Aggregate Report Listener
- View Results Tree Listener

**Example Configuration**:

```
Thread Group:
- Threads: 100
- Ramp-up: 30 seconds
- Duration: 300 seconds (5 min)

HTTP Requests:
- GET /posts
- GET /posts/1
- POST /posts (with body)

Timers:
- Uniform Random Timer: 1000-3000ms
```

### 2.2 Stress Test (15 points)

**stress_test.jmx**

Requirements:

- Stepping Thread Group (or regular with long duration)
- Start: Low users
- Increment: Gradual increase
- Monitor: Error rate
- Same samplers as load test
- Additional: Throughput Controller

**Example Configuration**:

```
Stepping Thread Group:
- Initial threads: 50
- Add threads: 50
- Every: 60 seconds
- Hold for: 120 seconds
- Total duration: Until failure
```

### 2.3 Spike Test (10 points)

**spike_test.jmx**

Requirements:

- Multiple Thread Groups
  - Base load (continuous)
  - Spike load (sudden burst)
- Synchronized start for spike
- Monitor recovery time

**Example Configuration**:

```
Thread Group 1 (Base):
- Threads: 50
- Duration: Entire test

Thread Group 2 (Spike):
- Threads: 500
- Start time: 60 seconds
- Duration: 30 seconds
```

## Part 3: Test Execution & Results (20 points)

Execute all tests and collect results.

### 3.1 Load Test Results (7 points)

Run test and save:

- `load_test_results.jtl`
- Generate HTML report: `load_test_report/`

**Document in RESULTS.md**:

- Average response time per endpoint
- 95th percentile response time
- Throughput (requests/sec)
- Error rate
- Screenshots of Aggregate Report

### 3.2 Stress Test Results (7 points)

Run test and save:

- `stress_test_results.jtl`
- Generate HTML report: `stress_test_report/`

**Document in RESULTS.md**:

- Breaking point (max users before failure)
- Response time degradation graph
- At what load did errors start
- How system behaved at breaking point

### 3.3 Spike Test Results (6 points)

Run test and save:

- `spike_test_results.jtl`
- Generate HTML report: `spike_test_report/`

**Document in RESULTS.md**:

- Response time during spike
- Recovery time after spike
- Error rate during spike
- System stability assessment

## Part 4: Analysis & Recommendations (20 points)

Create **ANALYSIS_REPORT.md**:

### 4.1 Performance Analysis (10 points)

Analyze results:

**Response Times**:

- Which endpoints are slowest?
- Are times within targets?
- What's the variance?

**Throughput**:

- Requests handled per second
- Does it scale linearly?
- Where does it plateau?

**Errors**:

- When do errors start?
- What types of errors?
- Pattern in failures?

**Resource Utilization** (if monitored):

- CPU usage
- Memory usage
- Network bandwidth

### 4.2 Bottleneck Identification (5 points)

Identify performance bottlenecks:

- Application layer issues
- Database issues (if applicable)
- Network issues
- External dependencies

### 4.3 Recommendations (5 points)

Provide actionable recommendations:

**Quick Wins**:

1. Add caching for GET requests
2. Use connection pooling
3. Enable compression

**Long-term Improvements**:

1. Database indexing
2. Horizontal scaling
3. CDN for static assets

**Prioritization**:

- High impact, low effort first
- Estimated improvement per fix

## Part 5: Final Report (10 points)

Create comprehensive **PERFORMANCE_REPORT.md**:

### Executive Summary

- Key findings (2-3 sentences)
- Pass/fail against requirements
- Top 3 recommendations

### Test Environment

- Application URL
- JMeter version
- Test machine specs
- Network conditions

### Test Scenarios Executed

- Load test summary
- Stress test summary
- Spike test summary

### Results Summary

- Table with key metrics
- Graphs/charts (screenshots)
- Comparison to targets

### Detailed Analysis

- Performance characteristics
- Bottlenecks found
- Scalability assessment

### Recommendations

- Prioritized list
- Implementation difficulty
- Expected impact

### Conclusion

- Overall performance assessment
- Readiness for production
- Next steps

## Bonus: Advanced Features (+10 points)

Implement ANY TWO:

### Option A: Distributed Testing (+5 points)

- Set up JMeter master/slave
- Run test across multiple machines
- Document setup and results

### Option B: CI/CD Integration (+5 points)

- Create GitHub Actions workflow
- Run load test automatically
- Fail build if performance regresses
- Upload HTML report as artifact

### Option C: Custom Monitoring (+5 points)

- Monitor application metrics (CPU, memory, DB)
- Correlate with JMeter results
- Create combined dashboard

### Option D: Advanced Scenarios (+5 points)

- Implement realistic user journeys
- Use correlation (extract/reuse tokens)
- Parameterize with CSV data (100+ rows)
- Weighted distribution of requests

## Deliverables

```
homework-9/
├── PERFORMANCE_STRATEGY.md
├── RESULTS.md
├── ANALYSIS_REPORT.md
├── PERFORMANCE_REPORT.md
├── jmeter/
│   ├── load_test.jmx
│   ├── stress_test.jmx
│   └── spike_test.jmx
├── results/
│   ├── load_test_results.jtl
│   ├── stress_test_results.jtl
│   ├── spike_test_results.jtl
│   ├── load_test_report/ (HTML)
│   ├── stress_test_report/ (HTML)
│   └── spike_test_report/ (HTML)
├── screenshots/
│   └── (Aggregate reports, graphs)
└── README.md (Setup instructions)
```

## Grading Rubric

### Performance Strategy (20 points)

- Clear requirements: 5 pts
- Well-defined scenarios: 5 pts
- Realistic user workflows: 5 pts
- Measurable success criteria: 5 pts

### JMeter Test Plans (40 points)

- Load test completeness: 15 pts
- Stress test implementation: 15 pts
- Spike test design: 10 pts

### Test Execution (20 points)

- Load test results: 7 pts
- Stress test results: 7 pts
- Spike test results: 6 pts

### Analysis & Recommendations (20 points)

- Thorough analysis: 10 pts
- Bottleneck identification: 5 pts
- Actionable recommendations: 5 pts

### Final Report (10 points)

- Completeness: 4 pts
- Clarity: 3 pts
- Professionalism: 3 pts

### Bonus (10 points)

- Advanced features: up to 10 pts

## Tips

1. **Start early** - Performance tests take time to run
2. **Use CLI mode** - jmeter -n for actual tests (GUI for creation)
3. **Monitor both sides** - Client (JMeter) and server
4. **Realistic loads** - Don't start with 10,000 users
5. **Iterate** - Run multiple times, average results
6. **Document everything** - Screenshots, observations, logs
7. **Clean data** - Delete old .jtl files between runs
8. **Be careful** - Don't DDoS public APIs

## Common Issues

### Issue: "Connection Refused"

- Check application is running
- Verify URL is correct
- Check firewall rules

### Issue: "Out of Memory"

- Reduce thread count
- Increase JMeter heap size
- Use non-GUI mode

### Issue: "Test Results Inconsistent"

- Run multiple times
- Check network conditions
- Verify server isn't throttling

## Resources

- [JMeter User Manual](https://jmeter.apache.org/usermanual/index.html)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [Performance Testing Guide](https://www.guru99.com/performance-testing.html)

## Submission

1. Create branch: `homework-9-solution`
2. Commit all files with conventional commits
3. Create PR with summary
4. Include link to HTML reports (GitHub Pages or Screenshots)

**Due**: Before Exam 3 (Week 16)  
**Late penalty**: 10% per day

Good luck with the final homework! ⚡
