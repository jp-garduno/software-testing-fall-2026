# Black Box Testing — Scenario 5 Conceptual Solutions

**Module**: 4 — Black Box Testing
**Type**: Class activity (not graded homework)
**Covers**:

- `04-black-box-testing/exercises/02-equivalence-partitioning.md` → Scenario 5: Password Strength Checker
- `04-black-box-testing/exercises/03-boundary-value-analysis.md` → Scenario 5: Game Level System
- `04-black-box-testing/exercises/04-decision-tables.md` → Scenario 4: Shipping Method Selector
- `04-black-box-testing/exercises/05-state-transition.md` → Scenario 4: Vending Machine

**Scope note**: this is a *test design* document. It explains how the solution
should be reasoned about — partitions, boundaries, test cases, inputs, expected outputs and
the ambiguities that must be resolved before writing a single assertion. It deliberately
contains **no implementation code**.

---

## Part 1 — Password Strength Checker (Equivalence Partitioning)

### 1.1 The specification under test

| Result | Rule as written |
| ------ | --------------- |
| Weak | `< 8 characters` **OR** only lowercase letters **OR** only numbers |
| Medium | (`8–12 characters` **AND** mix of letters and numbers) **OR** (`12+ characters` with only letters) |
| Strong | `12+ characters` **AND** uppercase + lowercase + digits **AND** at least one special char (`@#$%^&*`) |

The function takes one input (the password string) and returns one of three labels:
`"weak"`, `"medium"`, `"strong"`.

### 1.2 Step 0 — resolve the specification before designing tests

This is the part that matters most, and the part most students skip. Equivalence
partitioning only works if every input value maps to **exactly one** expected output. The
spec as written does not satisfy that, so the partitions cannot be drawn until these four
issues are decided and written down as documented assumptions.

**Ambiguity A — overlapping rules (a value that matches two categories).**
`"abcdefghijklm"` is 13 characters, only lowercase. It matches Weak (*only lowercase
letters* — note there is no length qualifier on that rule) and it also matches Medium
(*12+ characters with only letters*). The rules are not mutually exclusive, so the
specification alone does not tell us what to expect.

*Resolution to document*: evaluate in the order **length-floor → Strong → Medium → Weak**.
Concretely: anything under 8 characters is Weak regardless of composition; for everything
else, the first matching rule from Strong downward wins, with Weak as the fallback. Under
this rule `"password"` (8 chars, all lowercase) is Weak — which agrees with the starter
test the exercise gives us — and `"abcdefghijklm"` is Medium.

**Ambiguity B — the length bands overlap at exactly 12.**
`8–12` and `12+` both claim the value 12. Because the precedence order above puts Strong
first, a 12-character password with uppercase + lowercase + digit + special is Strong, and
the overlap stops being harmful. This must still be stated explicitly, because "overlapping
partitions" is exactly the defect EP is supposed to eliminate.

**Ambiguity C — the special-character set contradicts the exercise's own example.**
The spec lists specials as `@#$%^&*`. The provided starter test asserts that
`"SecurePass123!"` is Strong — but `!` is not in that list. Both statements cannot be true.

*Resolution to document*: treat the listed set as illustrative and define **special = any
character that is neither a letter nor a digit**. This keeps the supplied test green and is
the more defensible security rule. The alternative (a strict literal set) is also valid, but
then the exercise's own example is a bug and must be reported as such. Either way, the test
suite must contain a case that pins down the decision: a 12+ password whose only special is
`!` — expected Strong under the broad reading, Medium under the strict one.

**Ambiguity D — gaps: passwords that match no rule at all.**
Several perfectly ordinary inputs fall through every branch of the spec:

| Example input | Why it matches nothing |
| ------------- | ---------------------- |
| `"password12345"` (13) | Not `<8`; not *only* lowercase (has digits); not only numbers → not Weak. Not in the 8–12 band; not *only* letters → not Medium. No uppercase, no special → not Strong. |
| `"SecurePassword123"` (17) | Same trap, plus uppercase: still no special character, so not Strong; still outside every Medium clause. |
| `"ABCDEFGH"` (8) | Only uppercase — the Weak rule says only *lowercase*; no digits so no Medium clause applies. |
| `"@#$%^&*@"` (8) | No letters, no digits at all. |

*Resolution to document*: the fall-through default is **Weak** for anything that fails every
positive rule, **except** that a password of 12+ characters containing at least two
character classes is Medium. Whatever default is chosen, it must be written into the spec
and each gap must get its own test case — an undefined-behaviour input that nobody tested is
where production defects live.

### 1.3 Step 1 — choose the partitioning dimensions

The single string input is not one variable; it is two independent ones, and they must be
partitioned separately and then combined:

- **Dimension 1 — length**: `0`, `1–7`, `8–11`, `12`, `13+`
- **Dimension 2 — character composition** (which classes are present: lowercase, uppercase,
  digit, special)

Composition classes worth distinguishing:

| ID | Composition | Example shape |
| -- | ----------- | ------------- |
| C1 | lowercase only | `abcdefgh` |
| C2 | digits only | `12345678` |
| C3 | uppercase only | `ABCDEFGH` |
| C4 | letters only, mixed case | `AbcdEfghIjkl` |
| C5 | lowercase + digits | `abcdef1234` |
| C6 | upper + lower + digits, no special | `Abcdef1234xy` |
| C7 | upper + lower + digits + special | `Abcdef123!xy` |
| C8 | specials only | `@#$%^&*@` |
| C9 | non-ASCII / whitespace | `contraseña 1` |

Not every length × composition pair is a distinct partition — many collapse onto the same
expected output. The goal of EP is to keep one representative per *distinct expected
behaviour*, not one per combination.

### 1.4 Step 2 — the partition table

Representative values are chosen mid-partition on purpose. A value sitting on a boundary
(7, 8, 12, 13 characters) belongs to a BVA suite, not here; using boundary values as EP
representatives hides which technique actually caught a given defect.

| ID | Partition | Representative input | Length | Expected output |
| -- | --------- | -------------------- | ------ | --------------- |
| P01 | Empty string | `""` | 0 | `weak` |
| P02 | Below minimum length, mixed composition | `"Pa1!"` | 4 | `weak` |
| P03 | Below minimum length, strong-looking | `"Ab1!"` | 4 | `weak` (length floor beats everything) |
| P04 | 8–12, lowercase only | `"password"` | 8 | `weak` |
| P05 | 8–12, digits only | `"12345678"` | 8 | `weak` |
| P06 | 8–12, uppercase only *(gap D)* | `"ABCDEFGH"` | 8 | `weak` (documented default) |
| P07 | 8–12, specials only *(gap D)* | `"@#$%^&*@"` | 8 | `weak` (documented default) |
| P08 | 8–12, letters + digits | `"password123"` | 11 | `medium` |
| P09 | 8–12, letters + digits + special | `"passwd12!"` | 9 | `medium` (fails the 12-char Strong gate) |
| P10 | 8–12, mixed-case letters only | `"AbcdEfghIj"` | 10 | `weak` (not 12+, so no Medium clause) |
| P11 | 12+, letters only | `"abcdefghijklmn"` | 14 | `medium` (resolves ambiguity A) |
| P12 | 12+, lower + digits, no upper, no special *(gap D)* | `"password12345"` | 13 | `medium` (documented default) |
| P13 | 12+, upper + lower + digits, no special | `"SecurePassword123"` | 17 | `medium` — the single most valuable negative case for Strong |
| P14 | 12+, upper + lower + special, **no digit** | `"SecurePassword!"` | 15 | `medium` — isolates the digit requirement |
| P15 | 12+, lower + digits + special, **no uppercase** | `"securepass123!"` | 14 | `medium` — isolates the uppercase requirement |
| P16 | 12+, all four classes, special from the listed set | `"SecurePass12@"` | 13 | `strong` |
| P17 | 12+, all four classes, special *outside* the listed set | `"SecurePass123!"` | 14 | `strong` under the broad reading — the case that pins ambiguity C |
| P18 | Non-ASCII / whitespace | `"contraseña 12A!"` | 15 | `strong` (decide and document how accents and spaces are classified) |
| P19 | Invalid type (`None` / non-string) | `None` | — | raises a documented error, or returns `weak` — pick one and test it |

**Why P13–P15 carry the most weight.** The Strong rule is a conjunction of four conditions.
The classic implementation bug is writing `or` where `and` belongs, or forgetting one
condition entirely. P13, P14 and P15 each remove exactly one condition while leaving the
others satisfied, so each one fails if and only if that specific condition is missing from
the implementation. That is the difference between a suite that reports a failure and a
suite that tells you *which line is wrong*.

### 1.5 Step 3 — how the tests should be structured

- **One partition per test, one assertion per test.** The test name states the partition and
  the expected label, e.g. *"a 17-character password with no special character is medium"*.
- **Arrange–Act–Assert.** Arrange is the literal password string; Act is the single call;
  Assert is the returned label. No setup or teardown is needed — the function is pure, which
  is precisely why it is a good EP exercise.
- **Group the tests by expected output** (`weak`, `medium`, `strong`, `invalid input`) so
  that a failure report reads as "Strong detection is broken", not "test_17 failed".
- **Every documented assumption gets a test.** Ambiguities A, C and D above are not
  commentary — each resolution becomes a test case (P11, P17, P06/P07/P12) whose job is to
  fail loudly if someone later "fixes" the implementation to the other interpretation.

### 1.6 Step 4 — coverage report

| Metric | Value |
| ------ | ----- |
| Partitions identified | 19 |
| Partitions covered by a test case | 19 |
| Partition coverage | 100% |
| Partitions defined by the spec | 10 |
| Partitions existing only because of spec gaps/ambiguities | 9 |

That last row is the real finding of the exercise: roughly half of the partitions exist
because the requirement is incomplete. A test-design document that reports this back to the
requirements author has done more good than the test code itself will.

---

## Part 2 — Game Level System (Boundary Value Analysis)

### 2.1 The specification under test

XP thresholds by level: `0, 100, 250, 500, 1000, 2000, 4000, 8000, 15000, 30000`
(levels 1 through 10; level 10 is the maximum).

Feature unlocks: level 3 → Special Attack, level 5 → Mount, level 7 → Guild Access,
level 10 → Legendary Items.

Constraints: a single XP gain is `1–10,000`; total XP is capped at `30,000`; XP can never
be lost.

The operation under test adds XP and returns four things: whether the gain succeeded, the
resulting level, the features unlocked **by this call**, and a message.

### 2.2 Step 0 — the structural insight that drives the whole design

Two constraints interact, and noticing the interaction is the point of this scenario:

> A single gain is capped at **10,000**, but the top threshold is **30,000**.

Therefore **no single call can reach level 9 or 10 from zero**. Reaching 15,000 requires at
least 2 calls; reaching 30,000 requires at least 3. This has three consequences for the
design:

1. **Most boundary tests need a multi-step Arrange.** To test the 14,999 / 15,000 / 15,001
   boundary you must first *legally* bring the player to a known starting XP, then apply the
   gain under test. The Arrange must go through the public operation (not by poking the XP
   field directly), otherwise the test is exercising a state the real system can never
   produce — and a bug that only occurs on the legal path would be missed.
2. **A reusable "seed the player to N XP" fixture is required**, and it must itself respect
   the 10,000-per-call cap. This is setup, not a test.
3. **The current XP and the gain amount are two separate variables**, each with its own
   boundaries. They must be analysed separately.

### 2.3 Step 1 — enumerate the boundaries

**Variable A — resulting total XP, at each level threshold.** For each of the 9 transitions,
the standard triple applies: `threshold − 1`, `threshold`, `threshold + 1`. The critical
question the tests answer is whether the comparison is `>=` or `>` — an off-by-one here is
the single most likely defect in the whole scenario.

| Transition | Below | At | Above | Expected level (below / at / above) |
| ---------- | ----- | -- | ----- | ----------------------------------- |
| 1 → 2 | 99 | 100 | 101 | 1 / 2 / 2 |
| 2 → 3 | 249 | 250 | 251 | 2 / 3 / 3 |
| 3 → 4 | 499 | 500 | 501 | 3 / 4 / 4 |
| 4 → 5 | 999 | 1000 | 1001 | 4 / 5 / 5 |
| 5 → 6 | 1999 | 2000 | 2001 | 5 / 6 / 6 |
| 6 → 7 | 3999 | 4000 | 4001 | 6 / 7 / 7 |
| 7 → 8 | 7999 | 8000 | 8001 | 7 / 8 / 8 |
| 8 → 9 | 14999 | 15000 | 15001 | 8 / 9 / 9 |
| 9 → 10 | 29999 | 30000 | *unreachable* | 9 / 10 / — |

The "above" cell for the last row is deliberately empty: 30,001 total XP cannot exist,
because the total cap clamps it. That is itself a test case (see 2.5), not a gap.

**Variable B — the single XP gain amount.** Range `1–10,000`, so the robust BVA set is:

| Value | Classification | Expected outcome |
| ----- | -------------- | ---------------- |
| −1 | below min, invalid | rejected; XP unchanged; message names the constraint |
| 0 | below min, invalid | rejected; XP unchanged (0 is *not* a valid no-op) |
| 1 | minimum valid | accepted |
| 2 | min + 1 | accepted |
| 5000 | nominal | accepted |
| 9999 | max − 1 | accepted |
| 10000 | maximum valid | accepted |
| 10001 | above max, invalid | rejected; XP unchanged |

**Variable C — the total XP cap (30,000).** Boundaries arise from the *sum* of current XP
and the gain, which is where the two variables interact:

| Current XP | Gain | Resulting total | Expected |
| ---------- | ---- | --------------- | -------- |
| 29,998 | 1 | 29,999 | accepted, level 9 |
| 29,999 | 1 | 30,000 | accepted, level 10, Legendary Items unlocked |
| 30,000 | 1 | would be 30,001 | at cap: no change, message mentions the maximum |
| 29,500 | 1,000 | would be 30,500 | **partial overflow — see 2.4** |

**Variable D — feature-unlock thresholds.** These sit at the level thresholds for 3, 5, 7
and 10 (XP 250, 1000, 4000, 30000). They need their own assertions because "the level
changed" and "the feature was granted" are two different behaviours that can fail
independently.

### 2.4 Step 0 (continued) — the one design decision that must be made explicitly

**Partial overflow**: a player at 29,500 XP gains 1,000, which would exceed the 30,000 cap.
Two defensible designs:

- **(a) Clamp** — accept the gain, set total XP to 30,000, report success.
- **(b) Reject** — refuse the whole gain, leave XP at 29,500.

*Recommendation*: **clamp**. Option (b) silently discards XP the player legitimately earned,
which is a worse product behaviour than capping. Note that this is a genuine either/or:
whichever is chosen, it must be written into the spec and pinned by a test, because the two
options produce different expected outputs for the same input.

Note also that the starter test for a player already *at* 30,000 expects no change and a
message containing "maximum" — that is the already-full case and is compatible with either
design, so it does not settle the question.

### 2.5 Step 2 — the test case table

Each row states the precondition (starting XP, reached through legal calls), the input, and
the full expected output tuple.

**Group 1 — level threshold boundaries.** Nine transitions × three values = 27 cases. Two
rows shown as the pattern; the remaining transitions follow it identically.

| ID | Start XP | Gain | Expected success | Expected level | Expected unlocked (this call) | Rationale |
| -- | -------- | ---- | ---------------- | -------------- | ----------------------------- | --------- |
| B01 | 0 | 99 | true | 1 | none | just below the level-2 threshold |
| B02 | 0 | 100 | true | 2 | none | exactly at the threshold — proves `>=`, not `>` |
| B03 | 0 | 101 | true | 2 | none | just above the threshold |
| B22 | 10,000 | 4,999 | true | 8 | none | total 14,999, just below level 9 |
| B23 | 10,000 | 5,000 | true | 9 | none | total exactly 15,000; note the two-call Arrange |
| B24 | 10,000 | 5,001 | true | 9 | none | total 15,001 |

**Group 2 — feature unlocks.** For each of the four unlock levels, three cases:

| ID | Scenario | Input | Expected |
| -- | -------- | ----- | -------- |
| F01 | One XP below the unlock | start 0, gain 249 | level 2, Special Attack **absent** from the player's feature list |
| F02 | Exactly at the unlock | start 0, gain 250 | level 3, Special Attack present, and returned in this call's `unlocked` list |
| F03 | Above the unlock, no re-grant | start 250, gain 1 | level 3, Special Attack still present **exactly once**, this call's `unlocked` list **empty** |

F03 is the case most likely to be skipped and most likely to fail: appending to the feature
list on every call produces duplicates, and returning the cumulative list instead of the
newly-unlocked one is a distinct bug. The same triple repeats for levels 5, 7 and 10.

**Group 3 — single-gain limits.** One case per row of the Variable B table (8 cases). For
the invalid values (−1, 0, 10001) the expected output is: success `false`, XP **unchanged**,
level unchanged, `unlocked` empty, and a message naming the violated limit. Asserting that
XP is unchanged matters as much as asserting the failure flag — a function can correctly
report failure and still have mutated state.

**Group 4 — total cap.** One case per row of the Variable C table (4 cases), including the
partial-overflow case whose expected value follows the decision recorded in 2.4.

**Group 5 — multi-threshold jumps (interaction cases).** A single gain can cross several
thresholds at once, and every crossed unlock must fire:

| ID | Start XP | Gain | Expected level | Expected unlocked (this call) |
| -- | -------- | ---- | -------------- | ----------------------------- |
| M01 | 0 | 1,000 | 5 | Special Attack **and** Mount |
| M02 | 0 | 4,000 | 7 | Special Attack, Mount, Guild Access |
| M03 | 999 (reached legally) | 1 | 5 | Mount only — Special Attack was already owned |

M01 and M02 test a loop that must keep levelling while the threshold is met; an
implementation that levels up only once per call passes every Group 1 test and fails here.

**Group 6 — max-level behaviour.**

| ID | Scenario | Expected |
| -- | -------- | -------- |
| X01 | At 30,000 XP, gain 100 | XP stays 30,000, level stays 10, success `false`, message mentions the maximum |
| X02 | At 30,000 XP, gain 10,000 | same as X01 — a valid-sized gain is still refused when the total is full |
| X03 | At level 10, level never exceeds 10 | level stays 10 under any further input |

### 2.6 Step 3 — test strategy notes

- **Do not attempt worst-case BVA across both variables.** Current XP has ~29 interesting
  values and gain has 8; the full cross product is roughly 230 cases with very little added
  value. Apply **robust BVA to each variable independently** under the single-fault
  assumption (vary one variable, hold the other at a nominal value), then add the handful of
  deliberate interaction cases in Groups 4 and 5 where the two constraints genuinely meet.
  This is the reasoning that takes the suite from ~230 cases to ~55 without losing coverage
  of any boundary.
- **Every test starts from a fresh player.** State leaking between tests turns one real
  defect into a cascade of misleading failures, and makes the results depend on execution
  order.
- **Seed XP through the public operation**, using a parameterised fixture that respects the
  10,000-per-call cap. Writing directly to the XP field would let a test set up a state the
  system itself cannot produce.
- **Assert on the whole contract, not just the level.** Each test checks the returned
  success flag, the returned level, this call's unlocked list, the player's stored XP, and —
  for rejections — that the message names the violated constraint. Checking the level alone
  lets state-corruption bugs pass.
- **Parameterise the threshold triples.** The 27 cases in Group 1 are the same test shape
  driven by a table of `(start XP, gain, expected level)`. Expressing them as a data table
  rather than 27 hand-written tests is what Module 7 (Data-Driven Testing) formalises, and
  it means adding level 11 later costs one row, not three tests.

### 2.7 Step 4 — boundary coverage report

| Metric | Value |
| ------ | ----- |
| Level-transition boundaries identified | 9 transitions × 3 values = 27 |
| Feature-unlock boundaries identified | 4 unlocks × 3 values = 12 |
| Single-gain boundaries identified | 8 |
| Total-cap boundaries identified | 4 |
| Interaction / multi-level cases | 3 |
| Max-level cases | 3 |
| **Total boundary cases** | **57** |
| Cases covered by the designed suite | 57 |
| Boundary coverage | 100% |
| Cases unreachable by a single call (need a multi-step Arrange) | 15 |

---

## Part 3 — Shipping Method Selector (Decision Tables)

### 3.1 The specification under test

Four independent input dimensions, each with a fixed set of values:

| Dimension | Values |
| --------- | ------ |
| Weight class | Light (0–5 lb), Medium (5.1–20 lb), Heavy (20.1–50 lb), Very Heavy (50.1+ lb) |
| Destination | Local, Regional, National, International |
| Urgency | Standard, Expedited, Overnight |
| Cost preference | Lowest, Balanced, Fastest |

Raw combination count: **4 × 4 × 3 × 3 = 144**. A decision table is the right technique
precisely because 144 combinations cannot be reasoned about rule-by-rule; they must be
partitioned into the small number of *distinct expected outcomes* and simplified with
"don't care" (`-`).

### 3.2 Step 0 — resolve the specification before building the table

As with Part 1, the nine numbered "Selection Rules" in the exercise are not a complete,
non-overlapping function from input → output. Four conflicts must be resolved and documented
before a single row can be trusted.

**Ambiguity A — Rule 2 ("Freight or Ground if cost is priority") is not a decision.**
"If cost is priority" is not one of the three defined `cost_preference` values (`lowest`,
`balanced`, `fastest`). *Resolution to document*: read "cost is priority" as
`cost_preference == lowest`. Under this reading, Very Heavy + National collapses to two
outcomes: `lowest` → Ground, anything else → Freight. This must be pinned by a test on both
sides of the reading, because the alternative interpretation (Ground is never offered for
Very Heavy, i.e. always Freight) produces a different action for the same input.

**Ambiguity B — Rule 5 covers "National/Local" but not Regional, leaving Overnight + Regional
undefined.** No rule assigns an outcome to `urgency=overnight, destination=regional`. This is
a gap in the same sense as Ambiguities D in Part 1: an ordinary-looking input that matches no
rule. *Resolution to document*: Express is not offered between adjacent states overnight in
this catalog (only Local and National routes are guaranteed next-day), so
Overnight + Regional resolves to **Not available**, not to a silent fallback such as Priority
Mail — offering a 2–3 day method when the customer explicitly asked for overnight would
violate the urgency they selected. This is a genuine either/or design decision and the
alternative (extend Express to Regional) is equally defensible; whichever is chosen must be
written into the spec, because it changes the expected output for this input.

**Ambiguity C — physical/eligibility constraints vs. stated preferences.** Rule 7 says
"Fastest + Light/Medium + Local/Regional → Express", but Rule 1 already locks Very Heavy
packages to Freight regardless of urgency or cost. The rules never state which one wins when
a customer's *stated preference* (fastest, lowest) conflicts with a *hard eligibility
constraint* (weight class, international reachability). *Resolution to document*: eligibility
constraints (weight class, international/domestic reachability) are evaluated first and can
narrow or lock the available method set; urgency is applied second within whatever remains
eligible; cost preference is applied last, to choose among options that already satisfy
urgency. A customer cannot request their way out of a weight limit.

**Ambiguity D — Rule 8 ("International → only International methods") does not say which one.**
*Resolution to document*: within International, `expedited` maps to International Express
(3–5 days) and `standard`/`balanced`/`lowest` all map to International Standard (10–14 days),
since the catalog offers exactly two international speeds and Expedited is the only urgency
level that clearly matches the faster one.

### 3.3 Step 1 — conditions and actions

**Conditions** (as identified by the exercise's simplified dimensions):

1. Weight = Very Heavy?
2. Destination = International?
3. Destination ∈ {Local, National}?
4. Destination = Regional?
5. Urgency = Overnight?
6. Urgency = Expedited?
7. Cost preference = Lowest?
8. Cost preference = Fastest?

**Actions**: Offer Ground / Offer Priority Mail / Offer Express / Offer Freight / Offer
International Standard / Offer International Express / Not available.

### 3.4 Step 2 — the simplified decision table

Built directly from the resolved precedence (eligibility → urgency → cost → default), using
"don't care" to collapse the 144 raw combinations down to 13 rules:

| Rule # | Weight | Destination | Urgency | Cost | Action | Resolves |
| ------ | ------ | ----------- | ------- | ---- | ------ | -------- |
| R1 | Very Heavy | International | – | – | Not available | Rule 3 |
| R2 | – | International | Overnight | – | Not available | Rule 4 |
| R3 | ≠ Very Heavy | International | Expedited | – | International Express | Rule 8 + Ambiguity D |
| R4 | ≠ Very Heavy | International | Standard | – | International Standard | Rule 8 + Ambiguity D |
| R5 | Very Heavy | Local / Regional | – | – | Freight only | Rule 1 |
| R6 | Very Heavy | National | – | Lowest | Ground | Rule 2 + Ambiguity A |
| R7 | Very Heavy | National | – | Balanced / Fastest | Freight | Rule 2 + Ambiguity A |
| R8 | ≠ Very Heavy | Local / National | Overnight | – | Express | Rule 5 |
| R9 | ≠ Very Heavy | Regional | Overnight | – | Not available | Ambiguity B |
| R10 | Light / Medium | Local / Regional | ≠ Overnight | Fastest | Express | Rule 7 |
| R11 | ≠ Very Heavy | Local / Regional / National | ≠ Overnight | Lowest | Ground | Rule 6, generalised |
| R12 | Heavy | Local / Regional / National | ≠ Overnight | Balanced / (Fastest, not covered by R10) | Priority Mail | Rule 9 (default) |
| R13 | Light / Medium | Local / Regional / National | ≠ Overnight | Balanced | Priority Mail | Rule 9 (default) |

**Completeness check**: every one of the 144 raw combinations lands in exactly one rule —
international routes are fully handled by R1–R4 (weight × overnight × expedited/standard is
exhaustive for that branch); domestic Very Heavy is fully handled by R5–R7; domestic
non-Very-Heavy is handled by R8 (overnight), R9 (the Regional-overnight gap), and R10–R13
(the remaining urgency × cost combinations for Standard/Expedited, in every weight/destination
combination not already claimed by a more specific rule). No two rules share the same
condition combination, so there are no contradictions.

### 3.5 Step 3 — simplification strategy

Rules 1–9 above are *eligibility-first* rules: they fire on weight and destination alone
(urgency/cost mostly "don't care") because a hard constraint overrides preference. Rules
10–13 are *preference-first* rules that only apply once eligibility has already passed. This
two-tier structure is the simplification: instead of writing out cost × urgency separately
for every weight/destination pair (which is where the 144 raw combinations come from), the
table asks "is there a hard constraint?" once, and only branches on preference for the
combinations that survive. That collapses the table from 144 to 13 rules — a **91% reduction**
— without losing any distinct expected behaviour.

### 3.6 Step 4 — test case design notes and coverage

- One test per rule (13), plus one test per resolved ambiguity that isn't already a rule
  boundary in its own right (Ambiguity A's Ground/Freight split at R6/R7 is already covered by
  having both rows; Ambiguity D's Expedited/Standard split is covered by R3/R4).
- **Highest-value tests**: R6 vs. R7 (isolates whether "cost is priority" was implemented as
  intended) and R9 (isolates whether Overnight + Regional was implemented as "not available"
  rather than silently falling through to Priority Mail — a bug that would ship a customer a
  slower method than they explicitly rejected).
- **Coverage report**:

| Metric | Value |
| ------ | ----- |
| Raw combinations (4 × 4 × 3 × 3) | 144 |
| Simplified rules | 13 |
| Reduction | 91% |
| Rules covered by a test case | 13/13 (100%) |
| Documented ambiguities resolved by a dedicated test | 4/4 |

---

## Part 4 — Vending Machine (State Transition Testing)

### 4.1 The specification under test

**States** (6): Idle, HasCredit, ProductSelected, Dispensing, ChangeReturn, OutOfOrder.

**Events as given** (8): `insert_coin(amount)`, `select_product(product_id)`,
`cancel_transaction()`, `dispense_complete()`, `change_returned()`, `insufficient_funds()`,
`product_out_of_stock()`, `system_error()`.

**Business rules**: accepted coins are $0.25 / $0.50 / $1.00 / $2.00; products cost
$1.50–$3.00; a product cannot be selected without sufficient credit; change is returned
whenever inserted credit exceeds the product price; cancelling refunds everything inserted.

### 4.2 Step 0 — resolve the specification before drawing the diagram

**Ambiguity A — three of the eight "events" are not externally triggered events.**
`insufficient_funds()`, `product_out_of_stock()`, and `system_error()`'s domestic-error
cousins read like consequences, not triggers: nothing in the machine's physical interface
lets a *user* invoke "insufficient funds". The scenario's own illustrative test calls
`selectProduct()` directly and asserts `result.success === false` — it never calls a separate
`insufficientFunds()` method. *Resolution to document*: `insufficient_funds` and
`product_out_of_stock` are **outcomes** of attempting `select_product()`, not independent
transitions with their own trigger. Only `system_error()` remains a genuine externally-fired
event (the hardware itself reports a fault), and it is treated as available from every
non-terminal state. This distinction matters for coverage counting: a state-transition suite
that tries to write a standalone test calling `.insufficientFunds()` is testing a method that
the real interface doesn't expose.

**Ambiguity B — the "Dispensing" state has no defined entry event.**
The exercise's own sample test contradicts the state list: it calls `selectProduct()` and
then asserts the state is `"ProductSelected"` — not `"Dispensing"` — and the *next* call,
`dispenseComplete()`, is what moves the machine on to `"ChangeReturn"`. Under the event set as
given, `Dispensing` is a declared state with no incoming transition; it is unreachable.
*Resolution to document*: treat the executable test as the authoritative spec (tests are
harder to misread than prose) and collapse the model to the five *reachable* states — Idle,
HasCredit, ProductSelected, ChangeReturn, OutOfOrder — while flagging `Dispensing` back to
the requirements author as a likely missing transition (either `select_product()` should
target `Dispensing` and a new event such as `start_dispense()` is missing, or `Dispensing` is
a duplicate of `ProductSelected` under a different name and should be deleted from the state
list). Reporting an unreachable declared state is exactly the kind of defect state-transition
design is meant to catch before the diagram is finalised.

**Ambiguity C — `OutOfOrder` has no documented recovery event.**
Unlike the Traffic Light scenario, which pairs `enter_maintenance()` with
`exit_maintenance()`, the vending machine's event list has no equivalent "reset" or
"technician clears fault" trigger. *Resolution to document*: `OutOfOrder` is modelled as a
terminal sink state reachable from anywhere but leaving only through an out-of-band
operation (a physical technician reset) that is outside the scope of the software's public
event interface — so, within this state machine, every event received while `OutOfOrder`
must be rejected, including `system_error()` itself (already-faulted stays faulted).

**Ambiguity D — does credit carry over into `OutOfOrder`, and is it refunded?**
The spec never says what happens to money already inserted when `system_error()` fires
mid-transaction. *Resolution to document*: the safer product decision — and the one a test
should pin — is that credit is preserved (not silently forfeited) when entering
`OutOfOrder`, so it can be refunded once the machine is serviced, rather than the customer
losing money to a hardware fault that is not their doing.

### 4.3 Step 1 — state diagram

```
                          insert_coin(amount)
                 +-------------------------------+
                 |                                v
   [Idle] ----insert_coin(amount)----------> [HasCredit] ---insert_coin(amount)--+
      ^                                          |  ^                            |
      |                                          |  |----------------------------+
      |                       cancel_transaction()  |  select_product(id) [insufficient
      |                       (full refund)          |  funds / out of stock: no transition,
      |                                          |    |  reject with reason]
      |                                          v    |
      |                                  [ProductSelected] ---cancel_transaction()---> [Idle]
      |                                          |                                (full refund)
      |                                          | dispense_complete()
      |                                          v
      |                          +---------------+----------------+
      |                          |                                |
      |                   change owed > 0                   change owed == 0
      |                          v                                v
      |                   [ChangeReturn]                       [Idle]
      |                          |
      |                 change_returned()
      +--------------------------+

   system_error() from Idle / HasCredit / ProductSelected / ChangeReturn --> [OutOfOrder]
   [OutOfOrder] rejects every event (insert_coin, select_product, cancel_transaction,
                dispense_complete, change_returned, system_error) — no transition, no state change
```

### 4.4 Step 2 — state transition table

| Test ID | Current State | Event | Next State | Action / Validation | Valid? |
| ------- | -------------- | ----- | ---------- | -------------------- | ------ |
| VM_01 | Idle | `insert_coin(1.00)` | HasCredit | Accept coin, credit = 1.00 | Yes |
| VM_02 | HasCredit | `insert_coin(0.50)` | HasCredit | Accumulate credit (self-loop) | Yes |
| VM_03 | HasCredit | `select_product(id)` — credit ≥ price, in stock | ProductSelected | Lock product, no deduction yet | Yes |
| VM_04 | HasCredit | `select_product(id)` — credit < price | HasCredit (no change) | Reject: insufficient funds (Ambiguity A) | No |
| VM_05 | HasCredit | `select_product(id)` — price OK, product out of stock | HasCredit (no change) | Reject: out of stock (Ambiguity A) | No |
| VM_06 | HasCredit | `cancel_transaction()` | Idle | Refund full credit | Yes |
| VM_07 | ProductSelected | `dispense_complete()` — credit > price | ChangeReturn | Dispense product, compute change owed | Yes |
| VM_08 | ProductSelected | `dispense_complete()` — credit == price | Idle | Dispense product, credit reset to 0, no change owed | Yes |
| VM_09 | ProductSelected | `cancel_transaction()` | Idle | Refund full credit, release locked product | Yes |
| VM_10 | ChangeReturn | `change_returned()` | Idle | Reset credit to 0, clear selection | Yes |
| VM_11 | Idle | `select_product(id)` | Idle (no change) | Reject: no credit inserted | No |
| VM_12 | Idle | `cancel_transaction()` | Idle (no change) | Reject: nothing to cancel | No |
| VM_13 | Idle | `dispense_complete()` | Idle (no change) | Reject: nothing selected | No |
| VM_14 | ChangeReturn | `select_product(id)` | ChangeReturn (no change) | Reject: change must be collected first | No |
| VM_15 | Idle / HasCredit / ProductSelected / ChangeReturn | `system_error()` | OutOfOrder | Halt machine, preserve credit for later refund (Ambiguity D) | Yes |
| VM_16 | OutOfOrder | any event | OutOfOrder (no change) | Reject: machine out of service (Ambiguity C — no recovery event in scope) | No |

### 4.5 Step 3 — test case design notes

- **Group by outcome**, exactly as in Part 1: one block of "valid transition" tests, one block
  of "invalid transition — state unchanged" tests, one block of "`system_error()` from every
  reachable state" tests, since VM_15 must be independently verified from all four non-terminal
  states, not just Idle — a state machine that only guards against errors from the state it was
  developed against is a common source of production incidents.
- **VM_04/VM_05 are the highest-value pair.** Both look identical from the outside (`select_product`
  called, `success: false` returned) but must be reachable through genuinely different
  preconditions (low credit vs. depleted stock) and should carry different rejection messages —
  conflating them into one code path is the most likely implementation bug.
- **Assert on the whole contract, not just the state name.** For VM_06/VM_09, the test must
  check both that the state becomes `Idle` *and* that the refunded amount equals the credit
  that was actually inserted — a transition test that only checks `getState()` would miss a bug
  where the machine resets to `Idle` but silently keeps the customer's money.
- **VM_02 (the HasCredit self-loop) is easy to skip** because it doesn't change the state name,
  but it is exactly the kind of transition the pesticide-paradox thinking in Part 1 warns
  against dropping from a regression suite: without it, a defect where a second coin
  overwrites rather than accumulates credit would never be caught.

### 4.6 Step 4 — coverage report

| Metric | Value |
| ------ | ----- |
| States identified (as declared) | 6 |
| States reachable under the resolved event model (Ambiguity B) | 5 |
| State coverage (reachable states visited by the suite) | 5/5 = 100% |
| Valid transitions identified | 8 (VM_01–VM_03, VM_06–VM_10) |
| Valid transition coverage | 8/8 = 100% |
| Invalid transitions identified | 6 (VM_04, VM_05, VM_11–VM_14) + 1 sink-state class (VM_16) |
| Invalid transition coverage | 7/7 = 100% |
| `system_error()` source states tested | 4/4 (Idle, HasCredit, ProductSelected, ChangeReturn) |

---

## Summary — what each scenario is really teaching

| | Password Strength Checker (EP) | Game Level System (BVA) | Shipping Method Selector (Decision Table) | Vending Machine (State Transition) |
| - | ------------------------------ | ----------------------- | ------------------------------------------ | ------------------------------------ |
| Core skill | Splitting one input into dimensions, then collapsing combinations into distinct expected behaviours | Finding the exact values where behaviour changes, and testing on both sides of each | Mapping every combination of independent conditions to exactly one action, then simplifying with "don't care" | Mapping every (state, event) pair to exactly one outcome, including the pairs that must be rejected |
| Main trap | Overlapping and incomplete rules — the spec does not map every input to one output | Constraints that interact: the per-call cap makes most boundaries unreachable in one step | Preference rules (cost, urgency) that silently conflict with hard eligibility constraints (weight, geography) | Declared states/events that the actual interface never reaches or exposes |
| Highest-value tests | P13–P15: remove one Strong condition at a time to isolate which requirement is missing | M01–M02 and F03: multi-threshold jumps and no-duplicate unlocks — passed over by naive implementations | R6 vs. R7 and R9: pin the "cost is priority" reading and the Overnight+Regional gap | VM_04 vs. VM_05: two rejections that look identical externally but must come from different preconditions |
| Deliverable beyond the tests | A list of specification defects (4 ambiguities, 9 gap partitions) | An explicit design decision on partial overflow, plus the reachability analysis | A 144 → 13 rule reduction (91%) with every collapse traced back to a documented precedence decision | A corrected 6 → 5 state model, with the unreachable state reported back to the requirements author |

In all four scenarios the test design surfaced requirement defects **before** any code was
written. That is the argument for doing black box design on the specification rather than on
the implementation: tests derived from the code can only ever confirm what the code already
does.
