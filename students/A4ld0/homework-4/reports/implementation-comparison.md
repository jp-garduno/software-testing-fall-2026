# Dual-language implementation comparison

## Equivalence evidence

Both independent source files implement the public contract in the design
document. Python/pytest and JavaScript/Jest load the same `design/cases.json`.
Each framework creates a fresh account and clock for each case, executes public
commands, compares exact results and checks balance/state/history checkpoints.
Neither implementation imports or executes the other.

The final runs contain exactly the same **172 unique IDs**, verified by
`scripts/verify.py` against pytest XML and Jest JSON. All pass. Python reaches
100% line and branch coverage. JavaScript reaches 98.60% line, 95.50% branch,
97.63% statement, and 96.77% function coverage. Both exceed the bonus's 80%
requirement. See `verification-summary.json` and the raw logs for evidence.

## Implementation differences

| Concern | Python | JavaScript |
| --- | --- | --- |
| Money validation | Decimal conversion from the numeric string representation | Decimal digits and exponent parsed with BigInt |
| Storage | Integer cents | Safe integer cents, capped identically |
| Domain failures | ValueError converted by a command decorator | BankingError converted by a private command wrapper |
| Constructor errors | ValueError | BankingError, an Error subclass |
| Account fields | Underscore convention | Native private fields |
| Date validation | Strict pattern plus date.fromisoformat | Strict pattern plus UTC parsing and round-trip comparison |
| Test parametrization | pytest.mark.parametrize and fixture | Jest test.each and a fresh runner invocation |
| Coverage | coverage.py through pytest-cov | Jest instrumentation |

Names intentionally match across languages, including `pay_bill` and
`get_daily_limit`, so the shared case catalog does not need an API translation
layer. JSON cannot represent non-finite numbers; explicit `$number` markers
decode to each runtime's NaN/Infinity values. These are invalid input cases.

Python booleans are int subclasses, so the validator checks exact numeric types.
JavaScript distinguishes booleans using typeof. Neither accepts numeric strings
or rounds sub-cent input into a valid transaction. Expected decimal balances
come from the catalog; they are not calculated by calling production helpers.

Coverage percentages are not directly comparable across instrumentation tools.
Python's line count includes definitions and the decorator; Jest also counts
anonymous functions and expression branches. Python's 100% does not establish
that the real default clock ran: all scenarios inject a deterministic clock.
JavaScript's uncovered default-clock function makes that limitation visible.

## Limits of parity

Shared cases prevent accidental behavioral drift but can share an incorrect
oracle. The design's assumptions still require human review. The suite does not
prove equivalent behavior for every possible input, clock failure, or concurrent
execution. Real settlement, persistence, identity verification and production
security remain outside scope. Only the dual-language bonus is claimed.
