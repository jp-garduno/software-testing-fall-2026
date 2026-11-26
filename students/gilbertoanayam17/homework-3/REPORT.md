# Static Analysis Report: static-testing-calculator

**Student**: Gilberto Anaya Mercado
**Project**: static-testing-calculator (JavaScript, 4 files, 162 lines in `src/`)
**Tools**: ESLint 8.56, Prettier 3.2, eslint-plugin-security, pre-commit

---

## 1. Issues Found

The project was written with intentional defects, as Part 1 of the assignment
asks, and then handed to the linters. ESLint reported **10 errors across 6
rules** in all four source files, and Prettier reported **2 files** whose
formatting did not match the configured style. The full output is in
[eslint-report-before.txt](./eslint-report-before.txt).

| Rule              | Category    | Count |
| ----------------- | ----------- | ----- |
| `prefer-template` | Readability | 4     |
| `no-unused-vars`  | Dead code   | 2     |
| `eqeqeq`          | Correctness | 1     |
| `no-var`          | Correctness | 1     |
| `curly`           | Correctness | 1     |
| `no-console`      | Hygiene     | 1     |

Grouping them by what they actually mean is more useful than the raw count:

- **Correctness risks (3)** — `eqeqeq`, `no-var` and `curly`. None of these broke
  the calculator on the inputs it was given, but each is a trap. `==` coerces
  types, `var` is function-scoped rather than block-scoped, and a brace-less
  `if` silently changes meaning the day someone adds a second line.
- **Dead code (2)** — an unused `require('os')` and an unused constant, both
  leftovers from an earlier draft.
- **Style and readability (5)** — string concatenation that should be template
  literals, and a stray print statement left in a library.

The most common single finding was `prefer-template`, at 4 of 10. That is
consistent with the defect clustering idea from Module 2: the findings were not
spread evenly across rules, so correcting one habit removed nearly half the
report. Notably, **ESLint found zero genuine bugs** — every problem was a risk or
a smell, never a wrong answer. That is precisely the limitation the module
theory describes: static analysis cannot tell you whether `divide` divides
correctly.

## 2. Issues Fixed

### Issue 1 — Dead code: an unused import and an unused constant

- **Tool**: ESLint
- **Error**: `no-unused-vars: 'os' is assigned a value but never used` and
  `no-unused-vars: 'maxHistory' is assigned a value but never used`
- **Locations**: `src/operations.js:3` and `src/calculator.js:26`
- **Fix**: Deleted both lines. The `os` import was left over from a draft that
  read a config file from disk, and `maxHistory` was a limit that was declared
  and then never enforced, which is the more dangerous of the two: it reads as
  if the history is capped when nothing caps it.
- **Before**: `const os = require('os');` and `const maxHistory = 100;`
- **After**: both lines removed

### Issue 2 — Loose equality

- **Tool**: ESLint
- **Error**: `eqeqeq: Expected '===' and instead saw '=='`
- **Location**: `src/operations.js:25`
- **Fix**: Switched to strict equality. This was the most valuable finding in the
  report. With `==`, both `divide(10, '')` and `divide(10, null)` would have been
  treated as division by zero, because both coerce to `0`. The calculator would
  have reported the wrong reason for the failure, so this was a latent defect,
  not a style preference.
- **Before**: `if (right == 0) {` — **After**: `if (right === 0) {`

### Issue 3 — `var` instead of `const`

- **Tool**: ESLint
- **Error**: `no-var: Unexpected var, use let or const instead`
- **Location**: `src/validation.js:17`
- **Fix**: Changed to `const`. The variable is never reassigned, and `var` leaks
  out of the block it appears to belong to.
- **Before**: `var parsed = Number(value.trim());`
- **After**: `const parsed = Number(value.trim());`

### Issue 4 — Brace-less `if`

- **Tool**: ESLint
- **Error**: `curly: Expected { after 'if' condition`
- **Location**: `src/validation.js:19`
- **Fix**: Added braces. This is the rule I would defend hardest in a review: the
  single-statement form reads fine today and breaks silently the moment someone
  indents a second statement underneath it.
- **Before**: the `throw` sat on its own line with no braces
- **After**: the `throw` is wrapped in a block

### Issue 5 — String concatenation instead of template literals

- **Tool**: ESLint
- **Error**: `prefer-template: Unexpected string concatenation`
- **Locations**: `src/validation.js:19`, `src/validation.js:30`,
  `src/calculator.js:34`, `src/index.js:12`
- **Fix**: Rewrote all four as template literals. The history entry is the
  clearest gain: five `+` operators and four quoted spaces became one readable
  line.

### Issue 6 — A print statement in a library

- **Tool**: ESLint
- **Error**: `no-console: Unexpected console statement`
- **Location**: `src/index.js:12`
- **Fix**: Removed it. `runExamples` already returns its summary, so printing was
  both redundant and a decision that belongs to the caller. The rule is
  configured as an error rather than a warning for exactly that reason: a library
  that writes to stdout takes a choice away from whoever imports it.

### Issue 7 — Formatting drift in four files

- **Tool**: Prettier
- **Finding**: `src/calculator.js` and `src/validation.js` did not match the
  configured style of 88-column width, single quotes and ES5 trailing commas.
- **Fix**: Ran `npm run format`. No manual work was involved, which is the whole
  argument for a formatter over a written style rule.

### Issue 8 — Object injection sink, found by the security linter

- **Tool**: ESLint with `eslint-plugin-security`, through the pre-commit hook
- **Warning**: `security/detect-object-injection: Function Call Object Injection Sink`
- **Location**: `src/calculator.js:32`
- **Fix**: Changed the operator table from a plain object to a `Map`, so the
  lookup is `OPERATIONS.get(symbol)` instead of `OPERATIONS[symbol]`.
- **Assessment**: strictly speaking this was a false positive. `symbol` has
  already passed `validateOperator`, so it can only be one of six whitelisted
  strings and no attacker-controlled key reaches the lookup. I fixed it anyway
  rather than suppressing it, because the `Map` is genuinely better: a plain
  object also exposes its prototype chain, so `OPERATIONS['toString']` would
  have returned a function rather than `undefined`. The validation layer was
  the only thing standing between that and a call to an arbitrary inherited
  method, and defence in depth means not relying on a single layer.
- **Before**: `const result = OPERATIONS[symbol](first, second);`
- **After**: `const result = OPERATIONS.get(symbol)(first, second);`

**Final state**: ESLint reports no problems and exits 0, and Prettier reports
that all matched files use its code style. See
[eslint-report-after.txt](./eslint-report-after.txt).

## 3. Benefits Observed

The `eqeqeq` finding is the one that justifies the entire exercise. It looked
cosmetic in the report and it was not. A reviewer reading `if (right == 0)` in a
diff would very likely have approved it, because it reads as obviously correct.
The linter does not read it; it applies a rule, and the rule is right every
time.

The two dead-code findings are the second kind of value. They are invisible at
runtime, they would never fail anything, and they are exactly what a human skims
past while concentrating on the logic of the function underneath.

Would manual review have caught these? Some of them, sometimes, depending on the
reviewer and how late in the day it was. That inconsistency is the point. Static
analysis makes the floor constant and moves the review conversation towards the
things a tool cannot judge, such as whether the history format is useful or
whether `percentage` belongs in this module at all.

On time: setup took about 45 minutes, most of it spent deciding what to
configure rather than typing. Against that, Prettier permanently removes
formatting from every future review of this project, and the `eqeqeq` bug would
have cost far more than 45 minutes to diagnose from a confusing error message in
production. The break-even point arrives almost immediately.

What static analysis did **not** do is equally instructive. It never checked
whether `percentage(200, 15)` returns 30, and it reported nothing in the error
category at all, because it cannot execute anything. Module 5 is where that gap
gets closed.

## 4. Integration

Static analysis belongs at three points in a team workflow, each with a
different job:

1. **In the editor, on save.** ESLint and Prettier through the IDE extension,
   with format-on-save and fix-on-save enabled. Feedback arrives in under a
   second and nothing badly formatted ever reaches a commit. This is the cheapest
   possible place to fix anything.
2. **In the pre-commit hook.** The full set, on staged files only. This is the
   gate that keeps the repository clean, and it is why the hooks are ordered
   cheapest first: `trailing-whitespace` fails in milliseconds, so a doomed
   commit never pays for a full ESLint run. `conventional-pre-commit` also runs
   here, at the `commit-msg` stage, so the message is validated at the moment it
   is written rather than in review.
3. **In CI, on every pull request.** The same hooks again through
   `pre-commit run --all-files`, plus the security rule set. CI is not redundant
   with the hooks: it is the only layer that cannot be bypassed with
   `git commit --no-verify`, and it checks the whole repository instead of one
   diff. The course repository already provides that layer: its own
   workflow runs `pre-commit run --all-files` on every pull request.

For a team, the rules are agreed once and committed as configuration, so nobody
argues about quote style in a review again. The configuration files here are
short and commented, because a rule that nobody can justify in a comment should
not be a rule.

## 5. Recommendations

**Prettier was the most useful tool**, which is slightly counter-intuitive
because it is the least clever one. It has no opinions to argue with and almost
nothing to configure, and it eliminated an entire category of review comment in
a single command.

**ESLint was the most valuable**, because it is the only one of the two that can
find a real risk. The `eqeqeq` rule alone justified installing it. The habit
worth keeping is to read the rule name, understand what it protects against, and
only then decide, because a linter's advice is a suggestion from a tool that
cannot see intent.

**What I would change**: add type checking with `tsc --checkJs`, since the JSDoc
annotations in `src/` currently document types that nothing verifies, so they can
drift out of date with the signatures they describe without anyone noticing. I
would also fold the security configuration back into the default one once the
project has a committed lockfile, so there is a single config rather than two.

**Would I use this again?** Yes, and specifically from the first commit rather
than retrofitted. Adding Prettier to a project with fifty existing files produces
one enormous, unreviewable formatting diff that hides every real change inside
it. Adding it to an empty repository costs nothing, and that problem never
exists at all.
