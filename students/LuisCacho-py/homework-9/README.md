# Homework 9: Performance Test Strategy & Execution (Apache JMeter + Python Telemetry Suite)

Complete performance testing strategy, Apache JMeter test plans (`.jmx`), execution telemetry logs (`.jtl`), HTML dashboard reports, visual charts, bottleneck analysis, and automated SLA verification tests for the **JSONPlaceholder REST API** (`https://jsonplaceholder.typicode.com/`).

## Directory Structure

```text
homework-9/
├── PERFORMANCE_STRATEGY.md       # Part 1: SLAs, Load/Stress/Spike scenarios, user workflows, success criteria
├── RESULTS.md                    # Part 3: Detailed execution metrics, breaking point, and spike recovery
├── ANALYSIS_REPORT.md            # Part 4: Response time/throughput/error analysis, bottlenecks, recommendations
├── PERFORMANCE_REPORT.md         # Part 5: Final executive performance report and production readiness
├── jmeter/
│   ├── load_test.jmx             # Part 2.1: 100-user Load Test plan with CSV Data Set, Timers & Assertions
│   ├── stress_test.jmx           # Part 2.2: 50-500 user Stress Test plan with Throughput Controllers
│   ├── spike_test.jmx            # Part 2.3: Dual Thread Group Spike Test plan (50 base + 500 burst users)
│   └── test_payloads.csv         # Bonus Option D: 120 parameterized request rows with correlation tokens
├── results/
│   ├── load_test_results.jtl     # 750 JMeter samples from Load Test execution
│   ├── stress_test_results.jtl   # 900 JMeter samples from Stress Test execution
│   ├── spike_test_results.jtl    # 700 JMeter samples from Spike Test execution
│   ├── custom_monitoring_metrics.csv # Bonus Option C: Correlated CPU, Memory, DB Pool & Network metrics
│   ├── load_test_report/
│   │   └── index.html            # HTML dashboard report for Load Test
│   ├── stress_test_report/
│   │   └── index.html            # HTML dashboard report for Stress Test
│   └── spike_test_report/
│       └── index.html            # HTML dashboard report for Spike Test
├── screenshots/
│   ├── 01-load-test-aggregate-report.png
│   ├── 02-stress-test-degradation-graph.png
│   ├── 03-spike-test-recovery-graph.png
│   └── 04-resource-monitoring-dashboard.png
├── src/
│   ├── __init__.py
│   └── performance_suite.py      # JMX validator, JTL statistical parser, SLA checker & report generator
├── tests/
│   ├── __init__.py
│   └── test_performance_suite.py # Automated pytest suite verifying JMX plans, JTL metrics & SLAs (100% cov)
├── requirements.txt
└── README.md
```

## Running JMeter Test Plans (CLI Mode)

```bash
# 1. Execute Load Test
jmeter -n -t jmeter/load_test.jmx -l results/load_test_results.jtl -e -o results/load_test_report

# 2. Execute Stress Test
jmeter -n -t jmeter/stress_test.jmx -l results/stress_test_results.jtl -e -o results/stress_test_report

# 3. Execute Spike Test
jmeter -n -t jmeter/spike_test.jmx -l results/spike_test_results.jtl -e -o results/spike_test_report
```

## Running Automated Verification & SLA Tests (`pytest`)

```bash
pip install -r requirements.txt
PYTHONPATH=src pytest -v --cov=src --cov-report=term-missing
```
