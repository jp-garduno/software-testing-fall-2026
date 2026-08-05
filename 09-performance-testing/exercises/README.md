# Module 9: Performance Testing - Exercises

## Overview

Performance testing is best learned through hands-on JMeter practice. This module provides guided exercises and a comprehensive homework assignment.

## Learning Path

### 1. Study Theory (Week 16 - Session 1)

Read all 5 theory files:

- [01-introduction.md](../theory/01-introduction.md) - Types of performance testing
- [02-test-design.md](../theory/02-test-design.md) - Designing test scenarios
- [03-jmeter-fundamentals.md](../theory/03-jmeter-fundamentals.md) - JMeter basics
- [04-jmeter-advanced.md](../theory/04-jmeter-advanced.md) - Advanced features
- [05-analysis.md](../theory/05-analysis.md) - Analyzing results

### 2. Install JMeter

```bash
# Download from https://jmeter.apache.org/
# Or use package manager
brew install jmeter  # Mac
```

Verify:

```bash
jmeter --version
```

### 3. Hands-On Practice

Complete [Homework 9](../homework/homework-9.md) which covers:

- ✅ Load testing (normal traffic)
- ✅ Stress testing (find limits)
- ✅ Spike testing (sudden traffic)
- ✅ Analysis and recommendations
- ✅ Full performance report

## Practice Sites for JMeter

### 1. Public APIs (Free)

- **JSONPlaceholder**: https://jsonplaceholder.typicode.com/
- **ReqRes**: https://reqres.in/
- **HTTPBin**: https://httpbin.org/

### 2. Local Test Apps

- **Apache HTTP Server**: Install locally
- **Sample Spring Boot App**: Create simple REST API
- **Docker Containers**: Spin up test services

## Quick JMeter Tutorial

### Create Your First Test Plan

1. **Launch JMeter**

   ```bash
   jmeter
   ```

2. **Add Thread Group**

   - Right-click Test Plan → Add → Threads → Thread Group
   - Set: 10 users, 5s ramp-up, 1 loop

3. **Add HTTP Request**

   - Right-click Thread Group → Add → Sampler → HTTP Request
   - Server: jsonplaceholder.typicode.com
   - Path: /posts
   - Method: GET

4. **Add Listener**

   - Right-click Thread Group → Add → Listener → View Results Tree
   - Right-click Thread Group → Add → Listener → Aggregate Report

5. **Run Test**

   - Click green Start button
   - View results in listeners

6. **Save Test Plan**
   - File → Save Test Plan As → my_first_test.jmx

### CLI Execution (for CI/CD)

```bash
# Run without GUI
jmeter -n -t my_first_test.jmx -l results.jtl

# Generate HTML report
jmeter -g results.jtl -o html-report/

# View report
open html-report/index.html
```

## Exercise Topics Covered in Homework

The homework assignment covers all essential exercises:

1. **Simple Load Test** - Basic HTTP requests
2. **API Performance Testing** - REST endpoints
3. **Stress Testing** - Find breaking point
4. **Spike Testing** - Handle sudden traffic
5. **Results Analysis** - Interpret metrics
6. **Reporting** - Document findings

## Performance Testing Checklist

Before starting homework:

- [ ] JMeter installed and working
- [ ] Understand load vs stress vs spike testing
- [ ] Can create basic test plans
- [ ] Know how to read aggregate reports
- [ ] Understand key metrics (response time, throughput, error rate)

## Common JMeter Issues

### Issue: Java Not Found

**Solution**: Install Java 8+ and set JAVA_HOME

### Issue: Port Already in Use

**Solution**: Change JMeter port in jmeter.properties

### Issue: Out of Memory

**Solution**: Increase heap size:

```bash
export HEAP="-Xms512m -Xmx2048m"
```

### Issue: Too Many Open Files

**Solution**: Increase file limits (Linux/Mac):

```bash
ulimit -n 10000
```

## JMeter Best Practices

1. **Use Non-GUI mode** for actual tests (GUI is for creating tests)
2. **Start small** - 10 users, then scale up
3. **Monitor resources** - CPU, memory on both client and server
4. **Use realistic data** - CSV files with test data
5. **Add think time** - Simulate real user behavior
6. **Clean up** - Remove old result files
7. **Version control** - Save .jmx files in git

## Additional Resources

- [JMeter Documentation](https://jmeter.apache.org/usermanual/index.html)
- [JMeter Best Practices](https://jmeter.apache.org/usermanual/best-practices.html)
- [BlazeMeter JMeter Academy](https://www.blazemeter.com/jmeter-tutorial)

## Next Steps

1. Install JMeter
2. Try the quick tutorial above
3. Complete [Homework 9](../homework/homework-9.md)
4. Apply performance tests to Team Project (Milestone 7)
5. Prepare for **Exam 3** (Week 16)

---

**Remember**: Start with simple tests and gradually increase complexity. Performance testing is iterative! ⚡
