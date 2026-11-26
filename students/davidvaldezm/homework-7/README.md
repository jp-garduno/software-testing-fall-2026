# Homework 7 — Data-Driven Order Testing

The Python system calculates order totals, validates customer and billing details, and runs checkout from customer validation through confirmation. Integration tests inject a simulated payment function and verify each amount charged.

## Run the suite

Run these commands from this assignment directory with Python 3.11 or newer.

```sh
python -m venv .venv
# macOS / Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest
```

To measure statement and branch coverage and generate a fresh HTML report, run:

```sh
python -m pytest -q --cov=src --cov-branch --cov-report=term-missing --cov-report=html:htmlcov --cov-fail-under=80
```

Open `htmlcov/index.html` for the new report. The submitted run is recorded in [coverage_report.html](coverage_report.html) and [test_results.txt](test_results.txt).

## Test data

| File | Cases | Coverage |
| --- | ---: | --- |
| `order_calculations.csv` | 36 | 3 simple, 11 discount, 5 tax, 7 shipping, 10 complex |
| `generated_orders.csv` | 100 | Seeded combinations of baskets, customer types, coupon eligibility and shipping |
| `customer_validation.json` | 37 | 3 valid, 5 email, 4 phone, 7 address, 11 card, 6 multiple errors, 1 malformed customer |
| `order_workflows.json` | 5 | Three successful checkout paths, a rejected customer and a corrected order |
| `order_comparison.csv` | 10 | The same calculator scenarios as the traditional suite |

The two bonus features are seeded generation with Faker and schema validation before test execution. Run `python generate_orders.py` to regenerate the 100 regression rows. The generator computes the expected results in integer cents independently of `Order`. Fixture validation checks headers, required fields, types and duplicate case names, and reports the file and source line.

See the [fixture specification](TEST_DATA_SPEC.md) and the [comparison report](COMPARISON_REPORT.md).

## Rule decisions

- `SAVE10` and `SAVE20` require subtotals strictly greater than $50 and $100. The test data checks one cent below, at and one cent above each threshold.
- Standard shipping adds $0.50 per kilogram and $0.10 per kilometer. A 1 kg delivery over 10 km costs $1.50. Express multiplies that amount by 1.5, and `FREESHIP` waives the charge.
- Currency uses decimal arithmetic and half-up rounding to cents. The merchandise discount is rounded before tax. The total uses the rounded amounts displayed in the breakdown.
- Zero quantity contributes zero. Negative prices, weights, quantities and distances raise `ValueError`. Quantities must be integers.
- `NEWUSER` eligibility comes from the order's `customer_type`. The supported code table lists active codes. Expired codes have no entry and are rejected.
- The expiration month is inclusive. The validation fixtures set a fixed reference date so that the same cards pass or fail in future runs.
