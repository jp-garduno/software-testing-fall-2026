# Homework 3 - Static Testing Report

## Introduction

For this homework, I made a simple Python calculator with three source files in `src`: `calculator.py`, `operations.py` and `utils.py`.

The goal was to practice finding problems before execution. I used Pylint, Black, isort and pre-commit, with pytest as a separate behavior check.

## Issues Found

The original code produced several findings.

The first issue was missing module documentation (`C0114`).

The second was missing function documentation (`C0116`) in the calculator, operations and utility files.

Another issue was multiple statements on one line (`C0321`). I expanded those operations to improve readability.

Pylint also found a problem with the name `porcentaje` (`W0621`). The function was called `porcentaje`, but one of its parameters also had the name `porcentaje`. I changed the parameter name to `valor_porcentaje` to avoid using the same name.

The `calcular` function also had too many return statements (`R0911`). I replaced its repeated conditions with a dictionary that maps each option to a function.

Black corrected spacing and layout, while isort organized the imports in `calculator.py`.

## Fixes Made

I fixed more than five issues found by the static testing tools:

1. Added a module docstring.
2. Added documentation to functions that were missing it.
3. Changed one-line functions into multiple lines.
4. Renamed the `porcentaje` parameter to `valor_porcentaje`.
5. Reduced the number of return statements in `calcular`.
6. Formatted the Python files using Black.
7. Organized the imports using isort.

After the changes, all 10 calculator tests passed and the pre-commit checks passed for the Python files.

## Benefits of Static Testing

Static testing finds problems without running the program. Here, Pylint identified documentation, structure and naming issues.

Black and isort made the code consistent, which reduces formatting disagreements in team reviews.

Pre-commit makes these checks easier to use because the tools can run automatically when making commits. This helps prevent simple problems from being added to the project.

## Git and Integration

I made five conventional commits covering setup, source code, testing configuration and documentation. This makes the work easier to review because each commit has a clear purpose.

## Integration and Recommendations

In a team workflow, I would run Black and isort while developing in the IDE or before opening a pull request. These tools give quick feedback and keep formatting consistent. I would run the complete pre-commit configuration before every commit so that whitespace, file validity, imports and Pylint rules are checked locally. The CI pipeline should run `pre-commit run --all-files` and the test suite again on every pull request. This protects the repository when a contributor has not installed the local hooks or uses a different editor.

The most useful tools were Pylint and pre-commit. Pylint explained each problem, while pre-commit combined the checks into one repeatable command. I would review disabled Pylint messages periodically and add Bandit plus CI in a larger project.

The setup took approximately one hour. That is less time than a team might spend finding inconsistent formatting or confusing names during review. Static testing does not replace runtime tests, but it catches a different class of defects early. I would use this workflow in future Python projects because it creates a consistent quality gate with little ongoing effort.
