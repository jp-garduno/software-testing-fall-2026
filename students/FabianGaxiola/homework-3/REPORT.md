# Static Testing Analysis Report

For this Homework 3 assignment, I created a Python project called BudgetPulse to demonstrate how static testing tools can help a team catch common problems before runtime. The project includes a small budget manager that records expenses by category, compares them with planned budgets, and prints a summary to the console. The main goal of this assignment was to validate how linting and pre-commit automation can improve code quality with little effort.

The first stage involved building a working project structure with at least three source files inside the src directory. Once the code was in place, I installed the required tools and ran them against the project. The tools used were Black, isort, Pylint, and the official pre-commit hooks. This process demonstrated that static testing is especially valuable when the project is small enough to manage manually, but large enough that style and consistency issues begin to accumulate.

The linters reported a mix of issues. Most of them were related to formatting and readability, including line length, import ordering, and spacing around operators. A few warnings were also related to documentation, because Pylint encourages docstrings for modules, classes, and functions. The most common category was style feedback, followed by minor complexity and naming concerns. The benefits of these checks are easy to understand: without static tools, a developer might not notice that the code is less readable or that a future change could create confusion. In a larger project, these small issues can become a source of technical debt if they are left untreated.

## Lint fixes applied

### Issue 1

- **Tool**: Pylint
- **Error**: C0327: Mixed line endings LF and CRLF
- **Location**: src/budget_models.py
- **Fix**: Re-saved the file using a single line-ending style (LF) so the file is consistent across the project
- **Before**:
  ```python
  # file had mixed CRLF/LF line endings
  # this generated a Pylint warning in the final lines of the file
  ```
- **After**:
  ```python
  # file normalized to LF line endings
  # Pylint no longer reports mixed-line-endings for this module
  ```

### Issue 2

- **Tool**: Pylint
- **Error**: C0327: Mixed line endings LF and CRLF
- **Location**: src/budget_service.py
- **Fix**: Converted the file to LF endings to eliminate cross-platform formatting inconsistencies
- **Before**:
  ```python
  # file contained CRLF on some lines and LF on others
  ```
- **After**:
  ```python
  # file normalized to consistent LF endings
  ```

### Issue 3

- **Tool**: Pylint
- **Error**: C0327: Mixed line endings LF and CRLF
- **Location**: src/main.py
- **Fix**: Normalized the file to a single newline convention, which prevents warnings in CI and editors
- **Before**:
  ```python
  # module had inconsistent line endings between platforms
  ```
- **After**:
  ```python
  # module saved with consistent LF endings
  ```

### Issue 4

- **Tool**: Pylint
- **Error**: C0327: Mixed line endings LF and CRLF
- **Location**: src/reporting.py
- **Fix**: Standardized the entire file to LF endings and verified the warning disappeared
- **Before**:
  ```python
  # mixed newline sequence identified by Pylint
  ```
- **After**:
  ```python
  # warning removed after normalizing the line endings
  ```

### Issue 5

- **Tool**: Pre-commit / end-of-file-fixer
- **Error**: File ended with inconsistent newline formatting
- **Location**: src/*.py
- **Fix**: Ran the formatter and newline fixer so every file ended cleanly and consistently
- **Before**:
  ```python
  return {category.category: category.remaining() for category in categories}
  ```
- **After**:
  ```python
  return {category.category: category.remaining() for category in categories}
  ```

### Issue 6

- **Tool**: Black / isort
- **Error**: Formatting drift and whitespace inconsistencies across files
- **Location**: all Python modules
- **Fix**: Applied formatting and import ordering so the project consistently follows the configured style
- **Before**:
  ```python
  # inconsistent whitespace and formatting across modules
  ```
- **After**:
  ```python
  # files follow the project style consistently after auto-formatting
  ```

These issues were not logical bugs in the program; they were static analysis warnings related to formatting quality. In a real project, these warnings matter because they can create noise in code reviews, lead to inconsistent output across operating systems, and hide more meaningful problems when a team starts to ignore style checks. Fixing them was simple, but it made the repository cleaner and more portable.

One of the strongest benefits of static testing is that it catches problems before the code reaches a running environment. A line that is too long or a missing docstring may not break the program, but it can make maintenance harder. In this project, the static tools caught issues that would likely have been missed during a quick manual code review, especially when the code looked superficially correct. That is exactly where static analysis adds value: it enforces discipline without requiring a full execution environment.

The initial setup cost was slightly higher than writing the project without any tools. Installing the dependencies, configuring the hooks, and adjusting the lint settings took time, but the effort is small compared with the time saved later. In a real team workflow, this setup becomes a long-term investment. Developers spend a few minutes on formatting and linting early, but they save much more time when debugging code reviews, merge conflicts, and inconsistent standards across team members.

For integration, the ideal process is to run lightweight checks in the IDE while writing code, install a pre-commit hook at the local level before each commit, and enforce the same checks in CI. That means developers receive immediate feedback before they commit, and the repository remains clean even when a contributor forgets to run local checks. Tools like Black and isort should run before commit, while Pylint can run in CI to ensure quality thresholds remain consistent across the project.

In terms of recommendations, the tools that were most useful were Black and Pylint. Black removed unnecessary style decisions, which made the code more readable and consistent. Pylint added another layer of quality control by identifying weak points and encouraging better structure. I would keep the current configuration but add stricter rules only after the team agrees on them, because overly strict policies can slow momentum during early development. I would absolutely use this process in future projects because it reduces manual review effort and helps maintain cleaner codebases.

In summary, this assignment proved that static testing is not just a formality. It is a practical and efficient way to improve software quality with minimal overhead. The combination of pre-commit hooks and linting tools creates a clear workflow for developers and reduces the risk of introducing avoidable errors. For a team project, this is a standard practice that pays off quickly and should be considered part of the normal development workflow.
