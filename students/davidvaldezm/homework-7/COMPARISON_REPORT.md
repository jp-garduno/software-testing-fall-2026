# Traditional vs. Data-Driven Order Tests

Both suites check the same ten orders, including cases at and just above the coupon thresholds, first-order eligibility, discounted tax, express delivery and free shipping. Each suite checks all five amounts and the coupon application result where applicable.

## Lines of code

Counts use physical lines including imports, comments and blank lines. The CSV count includes its header.

| Measurement | Traditional | Data-driven |
| --- | ---: | ---: |
| Test module | 166 lines | 19 lines |
| Suite-specific input file | Embedded in test module | 11 CSV lines |
| Test module plus suite-specific input | 166 lines | 30 lines |
| Distinct scenarios | 10 | 10 |
| Calculator statement and branch coverage | 83% | 83% |

Parameterization reduces the test module by **88.55%** using `(166 - 19) / 166 × 100`. Counting the dedicated CSV, the reduction is **81.93%**. The data-driven suite also uses the shared loader and schemas. Those modules serve the calculator, customer, integration and comparison suites, so the table excludes their one-time cost. Charging all shared infrastructure to the ten-case comparison would make its initial implementation larger.

## Maintenance and readability

A new traditional case requires a named function with setup, coupon handling and five expected amounts. Updating a rule across several cases can require changing repeated assertions. The complete inputs and behavior of each scenario are visible together in Python, which helps when an order needs several state changes or unusual assertions.

A new data-driven case needs one CSV row. Updating the breakdown assertion applies to the entire table, and each named row still appears independently in pytest. Comparing threshold values is easy across rows. A long quoted `items` cell takes more effort to read, and tracking a failure can require opening both the test and the CSV.

## Coverage and effort

Running each module by itself with `--cov=src.order_calculator --cov-branch` produced ten passing cases and 83% coverage. The missing paths include invalid numeric inputs and shipping branches beyond the ten selected scenarios. Additional calculator cases and checkout workflows cover those paths in the full suite.

With ten expected breakdowns already calculated, adding and reviewing ten similar cases would take an estimated 20–30 minutes with individual functions and 8–12 minutes with validated CSV rows. These estimates cover editing and rerunning tests. Designing inputs and calculating independent expected amounts takes time in both approaches.

## Conclusion

Use data-driven tests when scenarios share setup and assertions and differ in values. Coupon thresholds, payment validation and generated regression data fit that shape. Use a traditional test for behavior that needs distinct setup or assertions, such as verifying that a rejected replacement coupon leaves the previous coupon applied. External data adds a loading and validation step, so descriptive case names and precise source errors matter.
