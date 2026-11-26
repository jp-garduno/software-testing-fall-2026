# Traditional versus data-driven

The two files in Part 3 cover **the same ten scenarios** with the same
assertions: subtotal, discount, tax, shipping and total for each one. The only
thing that changes is where the data lives.

- `tests/test_order_traditional.py` — ten functions, data written inline
- `tests/test_order_data_driven.py` — one parameterized function, data in `test_data/order_calculations.csv`

Every number in this report is measured, not estimated. The commands to
reproduce them are at the end.

## 1. Lines of code

| | Traditional | Data-driven | Reduction |
| --- | --- | --- | --- |
| Total lines | 144 | 41 | **71.5 %** |
| Excluding blanks and comments | 120 | 30 | **75.0 %** |
| Test functions | 10 | 2 | 80 % |
| Cases executed | 10 | 11 | — |

The data-driven file runs one case more because, besides the ten scenarios, it
includes a test that checks the ten names still exist in the CSV. Without that
guard, renaming a CSV row would make a scenario disappear silently and the
suite would stay green with nine cases instead of ten.

The real reduction is larger than the 75 % suggests: the 30 lines of the
data-driven file are **constant** with respect to the number of scenarios. The
120 lines of the traditional one grow by roughly 12 per scenario.

## 2. Maintainability

**Adding a new case.** In the traditional file it is about 12 lines: a
function, the order setup and five assertions. In the data-driven one it is a
line in the CSV plus a name in the `SCENARIOS` list. For the other files in
this submission, which do not filter by name, it is a single line in the CSV
and nothing else.

**Changing a rule.** If the tax rate went from 8 % to 9 %, the traditional file
needs ten `tax` values and ten `total` values recomputed by hand, spread over
144 lines. It is tedious and it is exactly where a typo slips in. In the
data-driven one the CSV column is regenerated with the same script that
produced it.

**Where data-driven hurts.** The context switch. Seeing a failure and
understanding what was being tested means opening the CSV and finding the row.
That is why every data file in this submission carries a `reason` or `category`
column that is not used to decide anything: it only travels into the failure
message.

## 3. Readability

The traditional file wins when you read **one** test. Everything is in sight:
inputs, steps and expected result, without opening anything else. For someone
new to the code, `test_save10_exactly_at_the_minimum` makes sense with no
context at all.

The data-driven file wins when you read **all** of them. The 35 CSV rows fit on
one screen and read like a decision table: you can see at a glance which
combinations are covered and which are missing. In the traditional file that
same view means reading 144 lines and keeping count in your head.

There is one effect I did not expect: the tabular format **makes the gaps
visible**. Laying the cases out in columns made it obvious that no row had a
quantity of zero, and that is where
`complex_zero_quantity_contributes_nothing` came from. Writing separate
functions, that gap goes unnoticed.

## 4. Coverage and the cost of growing

| | Traditional | Data-driven |
| --- | --- | --- |
| Scenarios covered | 10 | 10 |
| Run time (average of 3 runs) | 0.030 s | 0.010 s |
| Lines for 10 more scenarios | ~110 | ~10 (one per CSV row) |
| Files to touch | 1 | 1 (the CSV) |

Time favours the data-driven version, but the difference is milliseconds and it
is not the argument. With 10 cases it does not matter; the point is that the
cost of adding case 50 is the same as the cost of case 11, and in the
traditional file it is not.

In the full submission this shows: the 257 tests in the suite come out of 35
CSV rows, 39 JSON cases, 5 workflows and a handful of functions. Written one by
one they would be more than two thousand lines.

## 5. Conclusion

**Data-driven when** the same code path is walked with many combinations of
input: price tables, discount rules, format validation, decision matrices. The
more the cases resemble each other, the more it wins.

**Traditional when** each test does something different: setting up a
particular state, checking a sequence of calls, confirming something raises at
a precise moment. Forcing that into a table means inventing columns that apply
to a single row, and the table becomes harder to read than the code it
replaces.

**What works best is mixing them**, and that is what this submission does: the
amounts and the validations go through CSV and JSON, while the rules that are
not expressible as a number — that a rejected code does not replace the
previous one, that `FREESHIP` does not discount the price — live as separate
functions in `test_order_calculator.py`.

**What needs care.** Data is code and it needs the same rigour. A CSV with a
shifted column does not make a test fail: it makes it pass with the wrong
values. That is why this submission includes `src/data_validator.py`, which
checks the files before they are used and reports every problem with file, line
and column.

And a subtler risk: if the expected values are generated by calling the code
under test, the test stops testing anything and only confirms the code agrees
with itself. The values in `order_calculations.csv` were computed with a
formula written separately, from the text of the brief, and then cross-checked
against the implementation. `test_data/generated_orders.csv` does come from the
code, and that is exactly why it is labelled as regression data: it detects
that something changed, it does not prove that something is right.

## Reproducing the numbers

```bash
# Lines
wc -l tests/test_order_traditional.py tests/test_order_data_driven.py
grep -vcE '^\s*$|^\s*#' tests/test_order_traditional.py

# Cases executed
pytest tests/test_order_traditional.py --collect-only -q
pytest tests/test_order_data_driven.py --collect-only -q

# Time
pytest tests/test_order_traditional.py -q
pytest tests/test_order_data_driven.py -q
```
