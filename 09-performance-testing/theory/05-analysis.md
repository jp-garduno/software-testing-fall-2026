# Performance Analysis

## Key Metrics to Analyze

### 1. Response Time

- **Average**: Overall performance
- **Median**: Typical user experience
- **90th/95th/99th percentile**: Worst-case scenarios
- **Max**: Outliers

**Good**: Low and consistent
**Bad**: High and variable

### 2. Throughput

Requests handled per second.

**Good**: Meets requirements, stable under load
**Bad**: Drops as load increases

### 3. Error Rate

% of failed requests.

**Good**: < 0.1%
**Bad**: Increases with load

### 4. Resource Utilization

CPU, memory, disk, network.

**Good**: < 70-80% at peak
**Bad**: Maxed out, causing throttling

## Reading JMeter Reports

### Aggregate Report Columns

- **Label**: Request name
- **# Samples**: Total requests
- **Average**: Mean response time
- **Min/Max**: Range
- **Std. Dev.**: Variability
- **Error %**: Failure rate
- **Throughput**: Requests/sec
- **KB/sec**: Data transfer rate

## Identifying Bottlenecks

### Application

- High response times
- Many errors
- Check application logs

### Database

- Slow queries
- Lock waits
- Connection pool exhausted

### Network

- High latency
- Packet loss
- Bandwidth saturation

### Infrastructure

- High CPU/memory
- Disk I/O wait
- Out of resources

## Performance Tuning

### Quick Wins

1. **Add caching**: Redis, memcached
2. **Add indexes**: Speed up queries
3. **Enable compression**: Reduce payload
4. **Use CDN**: Static assets
5. **Connection pooling**: Reuse connections

### Optimization Strategy

1. Measure baseline
2. Change ONE thing
3. Retest
4. Compare results
5. Repeat

## Report Structure

1. **Executive Summary**: Key findings
2. **Test Environment**: Hardware, config
3. **Test Scenarios**: What was tested
4. **Results**: Metrics, graphs
5. **Bottlenecks**: Issues found
6. **Recommendations**: How to fix
7. **Appendix**: Raw data

## Next: Complete [homework-9.md](../homework/homework-9.md)
