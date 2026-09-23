# SecureBank test execution report

## Test summary

Execution date: **2026-09-22**, local timezone America/Mexico_City.
Environment: Windows, Python 3.12.14, pytest 8.4.2, pytest-cov 6.3.0,
coverage.py 7.16.1, Node.js 24.13.1, Jest 30.1.3.
Command: `python scripts/verify.py` (runs both suites and validates case parity).

| Result | Python | JavaScript |
| --- | --- | --- |
| Total | 172 | 172 |
| Passed | 172 | 172 |
| Failed | 0 | 0 |
| Skipped | 0 | 0 |
| Framework-reported duration | 0.73 s | 0.899 s |
| Test modules | 4 | 4 |

These are 172 distinct shared scenarios executed twice, not 344 distinct
design cases. Every case ID appears exactly once in each runner's result file.
Each scenario creates its own account and deterministic date clock.

## Results by technique

| Technique | IDs | Passed per language | Representative checks |
| --- | --- | --- | --- |
| Equivalence partitioning | EP01-EP66 | 66 | Invalid amounts/types/payees/dates, CSV escaping, independent history copies |
| Boundary values | BV01-BV58 | 58 | Exact transfer limits, minimum balances, fee thresholds, cumulative allowance, midnight |
| Decision tables | DT01-DT33 | 33 | All three tables, error precedence, fee idempotence, scheduling failures |
| State transitions | ST01-ST15 | 15 | All valid transitions, invalid transitions, closure, recovery and restrictions |

Every named result is available in [Python output](python-results.txt) and
[JavaScript output](javascript-results.txt). The [case catalog](../design/case-catalog.md)
maps each ID to a description; [cases.json](../design/cases.json) supplies the
exact arguments, expected results and snapshots.

**Defects and fixes:** no banking assertion failures occurred in the recorded
full runs. Design review identified ambiguity in minimum-balance equality,
waiver equality and outgoing permissions while Suspended; the contract records
the selected interpretations. Implementation review added the Closed-state
guard to scheduled processing, protected by ST15. The first verification wrapper
attempt encountered a Windows cp1252 encoding error while printing Jest check
marks after the tests passed. The wrapper now sets UTF-8 output; this was a
reporting-tool issue, not a failed banking test. No fabricated failure screenshot
is included.

## Coverage summary

Coverage includes only the banking implementation, excluding test helpers and
reporting scripts. No banking lines are excluded with ignore directives.

| Metric | Python | JavaScript |
| --- | --- | --- |
| Lines / executable statements in Python | 187/187 (100%) | 141/143 (98.60%) |
| Branches | 56/56 (100%) | 85/89 (95.50%) |
| Statements | 187/187 (100%) | 165/169 (97.63%) |
| Functions | Not a separate pytest-cov summary metric | 30/31 (96.77%) |

Both implementations exceed 80% line and branch coverage. The verification
script explicitly enforces the strict threshold and rejects missing/duplicate
case IDs. [verification-summary.json](verification-summary.json),
[python-coverage.json](python-coverage.json), and
[javascript-coverage-summary.json](javascript-coverage-summary.json) preserve
the measured totals. Python's function details are present in its coverage JSON,
but their instrumentation is not equivalent to Jest's function percentage.

### Covered and uncovered behavior

Covered paths include successful and rejected monetary commands; each supported
account type; cumulative allowance and reset; fee waivers, insufficient funds,
and repeated processing; due/pending/failed scheduled payments; state changes;
and history/CSV validation. Failed transactions check unchanged public state.

Python reports no missing executable lines or branches. Nevertheless, all cases
inject a clock, so the real default UTC clock is not independently exercised.
JavaScript's missing line 52 is that default clock; line 28 is a decimal
divisibility fallback not reached by the canonical numeric inputs. Unexpected
non-domain error rethrows on lines 59 and 83 are also unexercised expression
paths. These limitations do not imply additional tested business behavior.

### Separate technique measurements

Run `python scripts/technique_coverage.py` to reproduce the independent coverage
runs. Their temporary files do not overwrite full-suite coverage evidence.

| Technique | Python lines | Python branches | JS lines | JS branches |
| --- | --- | --- | --- | --- |
| EP | 75.40% | 60.71% | 68.53% | 68.53% |
| BV | 78.61% | 60.71% | 76.22% | 67.41% |
| DT | 78.61% | 60.71% | 75.52% | 65.16% |
| ST | 81.82% | 58.93% | 83.21% | 67.41% |

These measurements overlap. State scenarios execute multiple operations, while
partition tests emphasize rejection branches. No single technique reaches the
combined suite's branch coverage. Counts across different tools are not directly
comparable. Source data: [technique-coverage.json](technique-coverage.json).

## Screenshots and reproducible evidence

- [Test results](screenshots/test-results.png): browser screenshot of real captured
  stdout/stderr excerpts, labeled as captured output. Full transcripts are linked
  above; this is not presented as a photograph of a native terminal.
- [Python coverage](screenshots/coverage-python.png): screenshot of generated pytest-cov HTML.
- [JavaScript coverage](screenshots/coverage-javascript.png): screenshot of generated Jest HTML.
- [pytest XML](python-results.xml) and [Jest JSON](javascript-results.json): machine-readable results.

## Limits

The source models one account and source-side debits. It does not settle real
transfers, authenticate users, persist transactions, or implement concurrency.
The shared oracle can contain shared mistakes. These results support the
specified simulation and the dual-language bonus, not production certification.
