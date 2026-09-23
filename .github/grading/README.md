# Grading linter configurations

These files are used by `.github/workflows/grading-automation.yml` to lint student
submissions. They are **not** the repository's own linter configuration and are
not picked up by pre-commit; the workflow passes them explicitly.

| File            | Used for   | Applied when                                                                       |
| --------------- | ---------- | ---------------------------------------------------------------------------------- |
| `pylintrc`      | Python     | the submission does not commit its own pylint config                               |
| `eslintrc.json` | JavaScript | the submission does not commit its own ESLint config, or ESLint cannot run with it |

## Why a default at all

A submission with source files but no linter configuration used to be left out of
the quality grade entirely, which meant a whole language went ungraded and the
20% category was decided by the other one - or, for a single-language submission,
awarded in full by the "no linter could run" fallback. Supplying a default grades
everyone on the same rules instead.

## Why the submission's own config wins when it has one

Homework 3 is the static-testing assignment: writing the configuration _is_ the
work being graded. Exam 1 likewise lets students set the line length themselves.
Overriding a config a student was asked to produce would grade something other
than what was assigned, so these files are only a fallback.

For homework 3 specifically, the fallback lints the code and reports its findings
but JavaScript still scores 0/100 in the quality category, because the missing
configuration is the missing deliverable. Every other assignment is graded on the
findings alone.

A submission that _did_ commit an ESLint configuration ESLint then fails to load -
no `package.json` to install the toolchain from, an undeclared plugin, a flat
config on the repository's ESLint 8 - is also linted with `eslintrc.json`, but the
workflow records that case as `submission_unusable` rather than `course`, so it
never draws the homework-3 penalty and the comment says the configuration was
found and could not be run.

## What the rules are

Both files encode the standards the course actually teaches, not the tools'
defaults:

- **120-column lines** - stated in `.claude/CLAUDE.md`, module 3 and exam 1.
  Pylint defaults to 100 and ESLint enforces no limit at all.
- **`eslint:recommended`** plus `eqeqeq`, `no-var`, `prefer-const`,
  `no-param-reassign` and `max-len` - the exact set exercise 2 of exam 1 asks
  students to configure, so a submission graded with this file is held to the
  same rules as one graded with its own.
- **No module docstring required** in Python, because documentation is a rubric
  item scored by reading the submission rather than by counting linter findings.

`pylintrc` carries the reasoning for each of its `disable` entries in comments.
`eslintrc.json` cannot, so the short version: nothing is disabled there - the
rules listed are additions on top of `eslint:recommended`.

## Changing them

Editing these files changes every grade computed afterwards, including re-grades
of submissions that were already reported. Re-run the grading workflow on any PR
whose published grade should reflect the change.
