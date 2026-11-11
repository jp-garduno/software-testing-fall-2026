# Traditional versus data-driven order tests

Both versions run the same ten named order scenarios and check the same five amounts. They use the same assertion helper and calculator.

## Lines of code

| Test file | Nonblank lines | Scenarios |
|---|---:|---:|
| `tests/orderTraditional.test.js` | 59 | 10 |
| `tests/orderDataDriven.test.js` | 12 | 10 |

The parameterized test file has **79.7% fewer lines**, calculated as `(59 - 12) / 59 × 100`. This measures the two runner files. The shared CSV loader, test data and assertion helper sit outside that comparison. The CSV loader is also used by the 29-case calculation suite.

## Maintainability and readability

Adding a traditional case means writing a function with its inputs, coupon application when applicable, shipping setup, and expected amounts. Adding a data-driven case means writing one CSV row. An update to the common test procedure goes into one parameterized function. An update to one scenario goes into its row.

The traditional file keeps setup and expectations together, which makes an individual case easy to read. The data-driven file makes the shared procedure visible once, while the CSV makes it easier to compare thresholds and expected values across cases. The nested item JSON requires CSV quoting and becomes harder to read for orders with many items.

## Scenario coverage and extension effort

Both versions cover ten scenarios, including empty orders, quantities, coupon eligibility, and tax after a discount. The data-driven version reports each row by its scenario name.

For ten additional scenarios of similar complexity, budget roughly **10–15 minutes** for the traditional suite and **6–10 minutes** for the data-driven suite. These are estimates for writing and checking cases. Calculating and reviewing expected values is required in both versions. The shared data-driven procedure assumes every new case uses the same inputs and assertions.

## Runtime benchmark

| Cases | Traditional median | Data-driven median |
|---:|---:|---:|
| 10 | 140.7 ms | 141.5 ms |
| 50 | 147.2 ms | 153.1 ms |
| 100 | 181.5 ms | 167.3 ms |
| 500 | 262.3 ms | 262.1 ms |

The benchmark alternated the execution order and used five fresh Node.js processes per variant and size. It repeated the same ten seed scenarios in both variants. The traditional variant embeds its cases in test calls. The data-driven variant loads the same cases from JSON. The timings include process startup and test execution, with coverage instrumentation disabled. See [benchmark_results.html](benchmark_results.html) for the graph.

At 500 cases the two medians were within 1 ms. At 100 cases the data-driven version was about 14 ms faster, while at 50 the traditional version was about 6 ms faster. This run shows no consistent speed advantage across sizes. It measures the JSON benchmark runner and does not isolate CSV parsing or startup costs.

## Conclusion

Use traditional tests when scenarios have distinct setup or assertions that benefit from being read together. Use data-driven tests for large groups that share a procedure and differ mainly in inputs and expected results. For the order calculator, this keeps the test procedure in one place and makes boundary cases easy to add. The trade-offs are fixture parsing, input validation, and looking in a separate file to diagnose individual cases.
