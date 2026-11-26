# Dual Implementation Notes (Python / JavaScript)

Both implementations encode the same rules and the same 116 test cases. These are the differences
that the port actually forced, and what they say about testing the same design twice.

## 1. Money representation

Both store balances as integer cents, which is the fix for the floating point drift that BV2 and
BV3 exposed. The conversion from dollars differs:

- **Python** uses `Decimal(str(amount))` and reads the exponent to detect sub-cent precision.
- **JavaScript** has no decimal type, so `toCents` matches `String(amount)` against
  `/^-?\d+(\.\d+)?$/` and counts the digits after the point.

Both reject `$0.001` and `1e-7` with the same error, but the JavaScript version needs a second
regular expression for scientific notation, because `String(1e-7)` is `"1e-7"` while
`str(1e-07)` in Python is `'1e-07'` and `Decimal` parses it directly.

## 2. Type checking of inputs

Python can ask `isinstance(amount, (int, float, str, Decimal))` and must additionally exclude
`bool`, which is a subclass of `int`. JavaScript checks `typeof` and must exclude `null`,
`undefined` and `boolean` explicitly. The partitions are identical (EP6, EP32, EP34); only the
guard differs.

## 3. Dates

Python compares `datetime.date` objects directly. JavaScript has no date-only type, so the port
normalises every `Date` through `Date.UTC(y, m, d)` before comparing, which keeps the inclusive
range boundaries (BV28–BV31) from drifting with the local timezone. The Python suite has no
equivalent risk.

## 4. Parametrized tests

`pytest.mark.parametrize` with `ids=[...]` puts the design ID straight into the test name, so
pytest output reads `BV18-one-cent-below`. Jest's `test.each` has no id list, so the design ID is
passed as the first column of the table and interpolated into the test name with `%s`. The pytest
form is more readable; the Jest form needs an extra unused parameter.

## 5. Coverage measurement

Python reports 100% line and 100% branch. JavaScript reports 100% line and 99.15% branch, and the
one missing branch is the `active = true` default parameter of the `Payee` constructor: Istanbul
counts a default parameter as a branch, `coverage.py` does not. The test suites are equivalent; the
tools disagree about what a branch is. That is worth knowing before comparing coverage percentages
between two languages in a report.

## 6. What the port proved about the design

Porting 116 cases produced zero behavioural surprises, which is the useful result: every case is
written against the documented rules rather than against Python semantics. The only tests that had
to change shape were the ones about *input types*, which is exactly where the two languages
genuinely differ.
