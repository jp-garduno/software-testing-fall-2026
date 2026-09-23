# Homework 4: SecureBank black box testing

**Author:** Aldo Ramon Velazquez Fonseca (A4ld0)
**Branch:** `feat/A4ld0/homework-4`

An in-memory banking simulation with independent Python and JavaScript
implementations. Both run the same **172 scenarios**: 66 equivalence partitions,
58 boundary cases, 33 decision-table cases, and 15 state-transition scenarios.
The only bonus attempted is **dual implementation (+5)**.

## Prerequisites and installation

Python 3.11+ and Node.js 22+ with npm. Run from this directory:

```sh
cd students/A4ld0/homework-4
python -m venv .venv
```

Activate the environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```sh
# macOS / Linux
source .venv/bin/activate
```

Install both test frameworks:

```sh
python -m pip install -r requirements.txt
npm ci
```

## Run tests and coverage

```sh
# Individual suites
python -m pytest -v
npm test

# Individual coverage reports
python -m pytest -v --cov=src.banking_system --cov-branch --cov-report=term-missing --cov-report=html
npm run test:coverage

# Both suites, saved evidence, exact ID parity, and >80% line/branch checks
python scripts/verify.py

# Optional: measure each technique independently for the comparison report
python scripts/technique_coverage.py
```

Open `htmlcov/index.html` for Python or `coverage/index.html` for JavaScript in
a browser. Generated HTML and dependency directories are ignored by Git.
The verification script preserves raw logs, coverage JSON, pytest XML and Jest
JSON under `reports/`. It fails if either suite fails, an ID is missing or
duplicated, or either implementation has line/branch coverage at or below 80%.

Measured on 2026-09-22 using Python 3.12.14, pytest 8.4.2, pytest-cov 6.3.0,
Node 24.13.1, and Jest 30.1.3:

| Implementation | Passing tests | Lines | Branches |
| --- | --- | --- | --- |
| Python | 172/172 | 100% | 100% |
| JavaScript | 172/172 | 98.60% | 95.50% |

## What is tested

Savings, Checking, and Premium accounts; exact-cent validation; source-side
transfers; cumulative daily limits; deposits; fee waivers; once-monthly fees;
registered payees; scheduled payments; freeze, suspension, and closure; owner
updates; date-filtered history; and CSV escaping. Every scenario has a design ID
in its test name. Rejected operations assert unchanged public state, except the
documented suspension after an unaffordable monthly fee.

The [design document](design/test-design-document.md) defines assumptions where
the assignment is ambiguous. Transfer settlement, persistence, authentication,
concurrency, and a user interface are outside this classroom simulation.

## Project structure and deliverables

| Path | Contents |
| --- | --- |
| `design/test-design-document.md` | Part 1: partitions, boundaries, decision tables, state diagram description |
| `design/case-catalog.md` | All 172 case IDs and scenario descriptions |
| `design/cases.json` | Shared concrete inputs and expected results |
| `src/banking_system.py`, `src/bankingSystem.js` | Independent implementations |
| `tests/` | Four suites per language and fresh-account helpers |
| `reports/test-execution-report.md` | Part 3: observed results, evidence, coverage analysis |
| `reports/analysis-report.md` | Part 4: 500-700-word analysis |
| `reports/reflection.md` | 200-300-word reflection draft for personal review |
| `reports/implementation-comparison.md` | Dual-language bonus explanation |
| `reports/screenshots/` | Captured test output and HTML coverage screenshots |
| `output/pdf/` | Required design and analysis PDF exports |
| `scripts/` | Repeatable test execution, coverage comparison and PDF export |

## Public API

Both versions expose `BankAccount(type, initial_balance, clock)` where the optional
clock returns a UTC ISO date. Python accepts it as `clock=...`; JavaScript accepts
it as the third positional argument. Tests always inject a clock.

```python
from src.banking_system import BankAccount

account = BankAccount("Savings", 500, clock=lambda: "2026-09-22")
assert account.transfer(25) == {"success": True, "amount": 25}
assert account.snapshot()["balance"] == 475
```

```javascript
const BankAccount = require('./src/bankingSystem');
const account = new BankAccount('Savings', 500, () => '2026-09-22');
console.log(account.transfer(25)); // { success: true, amount: 25 }
console.log(account.snapshot().balance); // 475
```

Commands: `transfer(amount, destination?)`, `deposit(amount)`,
`pay_bill(payee, amount, date?)`, `process_scheduled()`, `process_fee()`,
`freeze()`, `unfreeze()`, `close()`, `update_info(owner)`, `history(start, end)`,
and `export_csv(start, end)`. Reads: `snapshot()` and `get_daily_limit()`.
Domain errors return `{success: false, error: message}`; invalid constructor
arguments raise an exception. Monetary input values use dollars, with integer
cents internally.

## Submission

This follows the course repository's `students/<username>/homework-4` layout.
The branch and commits are local; the student will publish and open the PR.
The final submission is tagged `hw4-final`. Review the reflection, then submit
the required repository/PR link, design PDF, analysis PDF, and reflection through
Canvas. No CI bonus or visual-diagram bonus is included.

PDF export uses the optional `reportlab` package:

```sh
python -m pip install reportlab
python scripts/export_pdfs.py
```
