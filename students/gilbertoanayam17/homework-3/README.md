# Homework 3: Static Testing Setup

**Student**: Gilberto Anaya Mercado
**Project**: static-testing-calculator
**Language**: JavaScript

## Description

A small calculator library that validates its operands, applies one of six
arithmetic operators and keeps a history of what it computed. It is deliberately
plain CommonJS with no runtime dependencies, so every tool in this homework is
analysing the code itself rather than a framework. The project was written with
a handful of intentional defects, which ESLint and Prettier then found and which
are documented in [REPORT.md](./REPORT.md).

## Project Structure

```
homework-3/
├── .eslintrc.js               # ESLint configuration (default, dependency free)
├── .eslintrc.security.js      # Security rules, used by pre-commit and npm run lint:security
├── .prettierrc                # Prettier configuration
├── .pre-commit-config.yaml    # 13 hooks across 5 repositories
├── .gitignore
├── package.json
├── README.md
├── REPORT.md                  # Analysis report
├── eslint-report-before.txt   # ESLint output before the fixes
├── eslint-report-after.txt    # ESLint output after the fixes
└── src/
    ├── operations.js          # Arithmetic and the CalculatorError type
    ├── validation.js          # Operand and operator validation
    ├── calculator.js          # Calculator class with history
    └── index.js               # Public entry point
```

## Setup Instructions

### 1. Install dependencies

```bash
cd students/gilbertoanayam17/homework-3
npm install
```

### 2. Install pre-commit hooks

```bash
pip install pre-commit
python -m pre_commit install --install-hooks
python -m pre_commit install --hook-type commit-msg
```

The second install is required because `conventional-pre-commit` runs at the
`commit-msg` stage, which the first one does not register.

`python -m pre_commit` is used rather than the bare `pre-commit` command
because it works whether or not the executable is on `PATH`. When the system
`site-packages` is not writeable, pip installs into a per-user directory that
is not on `PATH` by default, and the shorter command then fails with "not
recognised" even though the install succeeded. To check what is installed:

```bash
python -m pre_commit --version
```

> **On a recent Debian or Ubuntu, including WSL**, `pip install` into the system
> Python is refused with `error: externally-managed-environment`. That is
> PEP 668: the system interpreter belongs to `apt`, so installing into it with
> `pip` could break packaged tools. Use `sudo apt install pre-commit`,
> `pipx install pre-commit`, or a virtual environment instead.

### 3. Run the project

The package is a library, so it is used by requiring it:

```bash
node -e "const {Calculator} = require('./src'); const c = new Calculator(); console.log(c.calculate('7', '*', 6)); console.log(c.history);"
```

```
42
[ '7 * 6 = 42' ]
```

For anything longer than one expression, load the package into an interactive
session instead:

```bash
node -i -e "const {Calculator} = require('./src'); const c = new Calculator();"
```

```js
c.calculate(10, '+', 5); // 15
c.calculate('20', '/', 4); // 5
c.calculate(200, '%', 15); // 30, which is 15 per cent of 200
c.history; // [ '10 + 5 = 15', '20 / 4 = 5', '200 % 15 = 30' ]
c.last(); // '200 % 15 = 30'
c.clear();
```

Operands accept a number or a string, so `20` and `'20'` behave the same.
Anything the caller can get wrong throws `CalculatorError`:

```js
c.calculate(10, '/', 0); // CalculatorError: cannot divide by zero
c.calculate(1, '$', 2); // CalculatorError: unknown operator "$", expected one of: + - * / ^ %
c.calculate('abc', '+', 1); // CalculatorError: not a number: abc
```

## Pre-commit Hooks Configured

| Repository              | Hooks                                                                                                                                                                                       |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pre-commit-hooks        | `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-json`, `check-added-large-files`, `check-merge-conflict`, `check-case-conflict`, `detect-private-key`, `mixed-line-ending` |
| mirrors-prettier        | `prettier` (JavaScript, JSON, YAML, Markdown)                                                                                                                                               |
| mirrors-eslint          | `eslint --max-warnings=0`                                                                                                                                                                   |
| mirrors-eslint          | `eslint-security`, the same linter run against `.eslintrc.security.js`                                                                                                                      |
| conventional-pre-commit | `conventional-pre-commit` at the `commit-msg` stage                                                                                                                                         |

Hooks are ordered cheapest first: the file checks fail in milliseconds, Prettier
then rewrites files, and the slower linters run last on the already formatted
result.

## Linting

```bash
npm run lint            # ESLint with the default config
npm run lint:fix        # ESLint, applying every automatic fix
npm run lint:security   # ESLint with the eslint-plugin-security rule set
npm run format          # Prettier, rewriting files
npm run format:check    # Prettier, reporting without rewriting
python -m pre_commit run --all-files
```

Reports are committed next to this file:

- [`eslint-report-before.txt`](./eslint-report-before.txt) — 10 errors across 6
  rules, the state the project started in.
- [`eslint-report-after.txt`](./eslint-report-after.txt) — clean: ESLint reports
  no problems and Prettier reports no formatting differences.

There are two ESLint configurations on purpose. `.eslintrc.js` extends only
`eslint:recommended`, which ships inside ESLint, so `npm run lint` works on a
machine that has not run `npm install` for this sub-project. The security rules
need `eslint-plugin-security`, so they live in `.eslintrc.security.js` and run
through the pre-commit hook, which installs the plugin into its own environment.

## Results Summary

| Check           | Before                      | After               |
| --------------- | --------------------------- | ------------------- |
| ESLint problems | 10 errors                   | **0**               |
| Rules triggered | 6                           | **0**               |
| Prettier        | 2 files needed reformatting | **all files clean** |

See [REPORT.md](./REPORT.md) for the analysis of what the tools found, how each
issue was fixed, and how this fits into a team workflow.
