# Module 9: Performance and Stress Testing

## 🎯 Learning Objectives

By the end of this module, you will be able to:

- Understand different types of performance testing
- Design performance test scenarios
- Use JMeter for load and stress testing
- Analyze performance test results
- Identify performance bottlenecks
- Create performance testing strategies

## 📚 Theory Materials

### [1. Introduction to Performance Testing](./theory/01-introduction.md)

- What is performance testing
- Why performance matters
- Types: Load, Stress, Spike, Endurance, Scalability
- Performance metrics (response time, throughput, resource usage)

### [2. Performance Test Design](./theory/02-test-design.md)

- Identifying performance requirements
- Defining test scenarios
- User load patterns
- Performance test planning

### [3. JMeter Fundamentals](./theory/03-jmeter-fundamentals.md)

- JMeter architecture
- Thread groups and samplers
- Listeners and assertions
- Configuration elements

### [4. Advanced JMeter](./theory/04-jmeter-advanced.md)

- Parameterization and data files
- Timers and think times
- Distributed testing
- CI/CD integration

### [5. Performance Analysis](./theory/05-analysis.md)

- Reading performance reports
- Identifying bottlenecks
- Performance tuning strategies
- Common performance issues

## 🛠️ Setup Instructions

### Install JMeter

**Option 1: Download**

1. Download from: https://jmeter.apache.org/download_jmeter.cgi
2. Extract the archive
3. Run: `bin/jmeter` (Linux/Mac) or `bin/jmeter.bat` (Windows)

**Option 2: Package Manager (Mac)**

```bash
brew install jmeter
```

**Requirements**:

- Java 8 or higher

**Verify Installation**:

```bash
jmeter --version
```

### Alternative Tools (Optional)

```bash
# Locust (Python-based)
pip install locust

# k6 (JavaScript-based)
brew install k6  # Mac
```

## 💻 Practical Exercises

### [Exercise 1: Simple Load Test](./exercises/01-simple-load-test.md)

Create your first JMeter test plan for a web application.

### [Exercise 2: API Performance Testing](./exercises/02-api-testing.md)

Test REST API endpoints under load.

### [Exercise 3: Stress Testing](./exercises/03-stress-test.md)

Find the breaking point of an application.

### [Exercise 4: Spike Testing](./exercises/04-spike-test.md)

Test how system handles sudden traffic spikes.

### [Exercise 5: Endurance Testing](./exercises/05-endurance-test.md)

Test system stability over extended periods.

### [Exercise 6: Database Load Testing](./exercises/06-database-load.md)

Test database performance under concurrent queries.

## 📝 Homework Assignment

**[Homework 9: Performance Test Plan](./homework/homework-9.md)**

**Due**: Before Exam 3 (Week 16)

**Objectives**:

- Design complete performance test strategy
- Create JMeter test plans
- Execute load and stress tests
- Analyze results and provide recommendations
- Document findings

## 🎥 Video Resources

- **Performance Testing Overview** (20 min)
- **JMeter Basics** (30 min)
- **Creating Test Plans** (25 min)
- **Analyzing Results** (20 min)
- **Real-world Case Studies** (15 min)

## 📊 Types of Performance Testing

### Load Testing

- Tests system behavior under **expected load**
- Validates response times meet requirements
- Identifies resource usage patterns

### Stress Testing

- Tests system behavior **beyond normal capacity**
- Finds breaking point
- Validates system recovery

### Spike Testing

- Tests **sudden increases** in load
- Common in flash sales, viral events
- Validates auto-scaling

### Endurance Testing (Soak Testing)

- Tests system over **extended period**
- Identifies memory leaks
- Validates stability

### Scalability Testing

- Tests ability to **scale up/down**
- Vertical vs horizontal scaling
- Cost-performance analysis

## 📖 JMeter Test Plan Structure

```
Test Plan
├── Thread Group (Users)
│   ├── HTTP Request Sampler
│   ├── HTTP Request Sampler
│   └── ...
├── Listeners
│   ├── View Results Tree
│   ├── Aggregate Report
│   └── Graph Results
├── Configuration
│   ├── HTTP Request Defaults
│   ├── CSV Data Set Config
│   └── User Defined Variables
└── Assertions
    └── Response Assertion
```

## 🎯 Key Performance Metrics

| **Metric**           | **Description**           | **Target Example** |
| -------------------- | ------------------------- | ------------------ |
| **Response Time**    | Time to complete request  | < 200ms (avg)      |
| **Throughput**       | Requests per second       | > 1000 req/s       |
| **Error Rate**       | % of failed requests      | < 1%               |
| **Concurrent Users** | Simultaneous active users | 10,000 users       |
| **CPU Usage**        | Server CPU utilization    | < 70%              |
| **Memory Usage**     | Server memory utilization | < 80%              |
| **Network I/O**      | Data transfer rate        | < 100 Mbps         |

## 📈 Sample JMeter Configuration

### Basic HTTP Request Test

```
Thread Group Settings:
- Number of Threads: 100
- Ramp-up Period: 10 seconds
- Loop Count: 10

HTTP Request:
- Server: example.com
- Path: /api/users
- Method: GET

Assertions:
- Response Code: 200
- Response Time: < 500ms
```

## 🛠️ Performance Testing Workflow

```
1. Define Performance Requirements
   ↓
2. Design Test Scenarios
   ↓
3. Prepare Test Environment
   ↓
4. Create Test Scripts (JMeter)
   ↓
5. Execute Tests
   ↓
6. Monitor & Collect Metrics
   ↓
7. Analyze Results
   ↓
8. Identify Bottlenecks
   ↓
9. Optimize & Retest
   ↓
10. Generate Report
```

## ❓ Common Questions

**Q: How many virtual users should I simulate?**
A: Based on expected traffic. Start with realistic numbers, then increase for stress testing.

**Q: Can I run JMeter tests from CI/CD?**
A: Yes! JMeter can run in non-GUI mode and integrate with Jenkins, GitHub Actions, etc.

**Q: What's a good response time?**
A: Depends on context. Generally: < 100ms excellent, 100-300ms good, > 1s poor.

**Q: Should I test in production?**
A: Generally no. Use staging environment with production-like configuration.

**Q: How long should a performance test run?**
A: Load tests: 30-60 min. Endurance tests: 8-24 hours. Stress tests: until failure.

## 🎯 Self-Assessment Checklist

- [ ] Understand different types of performance testing
- [ ] Install and configure JMeter
- [ ] Create basic test plans
- [ ] Configure thread groups and samplers
- [ ] Add listeners and assertions
- [ ] Execute load tests
- [ ] Analyze performance reports
- [ ] Identify common bottlenecks
- [ ] Generate performance test reports

## 🚀 Next Steps

- Complete all JMeter exercises
- Complete [Homework 9](./homework/homework-9.md)
- Work on Team Project Milestone 7
- Prepare for **Exam 3** (Week 16, Session 2)
- Review all modules for comprehensive final exam

---

**Remember**: Performance testing finds issues that functional tests miss. A working application isn't enough - it needs to work under load! ⚡
