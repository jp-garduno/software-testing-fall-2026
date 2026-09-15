# JMeter Fundamentals

## Architecture

JMeter is a Java-based load testing tool with GUI for test creation and CLI for execution.

## Key Components

### 1. Test Plan

Root element containing all test elements.

### 2. Thread Group

Simulates users.

**Settings**:

- **Number of Threads**: Virtual users
- **Ramp-up Period**: Time to start all users
- **Loop Count**: How many times to repeat

**Example**: 100 users, 10s ramp-up, 5 loops

- Starts 10 users/second
- Each user executes test 5 times

### 3. Samplers

Make requests.

**Types**:

- **HTTP Request**: Web/API calls
- **JDBC Request**: Database queries
- **FTP Request**: File transfers

### 4. Listeners

View/save results.

**Types**:

- **View Results Tree**: Individual requests
- **Aggregate Report**: Statistics summary
- **Graph Results**: Visual charts

### 5. Configuration Elements

Set defaults and variables.

**Types**:

- **HTTP Request Defaults**: Base URL
- **CSV Data Set Config**: Load test data
- **User Defined Variables**: Constants

### 6. Assertions

Validate responses.

**Types**:

- **Response Assertion**: Check text/code
- **Duration Assertion**: Max response time
- **Size Assertion**: Response size

### 7. Timers

Add delays.

**Types**:

- **Constant Timer**: Fixed delay
- **Uniform Random Timer**: Random range
- **Gaussian Random Timer**: Bell curve

## Creating First Test

1. Add Thread Group
2. Add HTTP Request Sampler
3. Add Listener (View Results Tree)
4. Configure and Run
5. Analyze Results

## CLI Execution

```bash
# Run test
jmeter -n -t test.jmx -l results.jtl

# Generate HTML report
jmeter -g results.jtl -o report/
```

## Next: [04-jmeter-advanced.md](./04-jmeter-advanced.md)
