# Advanced JMeter

## Parameterization

### CSV Data Set Config

Load data from CSV files.

**users.csv**:

```csv
username,password
user1,pass1
user2,pass2
```

**JMeter Config**:

- Filename: users.csv
- Variable Names: username,password
- Recycle: true
- Sharing mode: All threads

**Usage**: `${username}`, `${password}`

## Correlation

Extract dynamic values from responses.

**Use Case**: Session tokens, CSRF tokens

**Regular Expression Extractor**:

- Apply to: Main sample
- Field to check: Body
- Regular Expression: `"token":"(.+?)"`
- Template: `$1$`
- Match No.: 1
- Variable Name: token

**Usage**: `${token}`

## Distributed Testing

Run tests across multiple machines.

**Master**: Controls test
**Slaves**: Generate load

**Setup**:

1. Configure jmeter.properties
2. Add slave IPs to master
3. Run jmeter-server on slaves
4. Start remote from master

## CI/CD Integration

### GitHub Actions

```yaml
- name: Run JMeter Test
  run: |
    jmeter -n -t test.jmx -l results.jtl
    jmeter -g results.jtl -o report/

- name: Upload Report
  uses: actions/upload-artifact@v3
  with:
    name: jmeter-report
    path: report/
```

## Performance Goals

Set in assertions or check in CI.

## Next: [05-analysis.md](./05-analysis.md)
