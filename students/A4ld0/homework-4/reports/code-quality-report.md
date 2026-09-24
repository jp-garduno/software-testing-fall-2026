# Code-quality corrections after initial grading

The initial grading report awarded 96.68/100, with 8.34/10 from Pylint.
The same **8.34/10** was reproduced locally with Pylint 3.3.8 against all
submitted Python source, tests, and scripts. The run reported 45 messages,
including five import errors from the PDF exporter's undeclared dependency.
The saved baseline is [pylint-before.json](pylint-before.json).

## Corrections

- Documented public banking operations, test helpers, and reporting functions.
- Grouped immutable account rules, customer-facing profile data, and mutable
  ledger collections into small dataclasses. Each ledger uses independent
  default factories, preserving account isolation. BankAccount now coordinates
  six instance attributes instead of fourteen.
- Exposed the date-refresh hook used by the command decorator through the
  documented `refresh_day()` method, avoiding external protected-member access.
- Split PDF formatting, Markdown parsing, table construction, and export into
  focused functions without changing their layout settings.
- Shared UTF-8 command capture between the full-suite and per-technique scripts.
- Formatted all Python files with Black and declared `reportlab==4.4.9`, which
  the supplied PDF exporter imports. Development tools are reproducible through
  `requirements-dev.txt`.

No Pylint checks were disabled, score thresholds relaxed, or grading workflows
modified. JavaScript behavior and the shared design cases were unchanged.

## Verification

```sh
python -m pip install -r requirements-dev.txt
python -m pylint src tests scripts --persistent=n --output-format=json2
python -m black --check src tests scripts
python scripts/verify.py
python scripts/technique_coverage.py
python scripts/export_pdfs.py
```

| Check | Observed result |
| --- | --- |
| Pylint 3.3.8 | 10.00/10, zero messages |
| Black 26.3.1 | All submitted Python files formatted |
| Python | 172 passed; 200/200 statements and 56/56 branches covered |
| JavaScript | 172 passed in four suites; 98.60% lines and 95.50% branches |
| Case parity | The same 172 unique design IDs in both implementations |

The result is recorded in [pylint-after.json](pylint-after.json). Execution logs,
coverage summaries, screenshots, and the analysis PDF were refreshed after the
refactor. Added dataclass declarations change the per-technique line-coverage
denominator; the actual scenario count and full-suite coverage remain unchanged.

The grade report's JavaScript count of four matches the suite count. The raw Jest
output records 172 passing cases. The new automated grade must be confirmed by
the grading workflow; a local lint score alone is not a new official grade.

The published `hw4-final` tag is preserved as the original graded submission.
The follow-up correction is committed on `feat/A4ld0/homework-4`.
