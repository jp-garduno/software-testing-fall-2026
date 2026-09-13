# Static Testing Analysis Report

## 1. Issues Found

For this homework, I created a simple Python task management application and used static analysis tools to find code quality and formatting problems before delivering the final version of the project.

The main static analysis tool used was Pylint. After configuring Pylint for the project, the first relevant analysis reported 9 issues and gave the source code a score of 8.95/10.

The problems found included unused imports, an unused variable, incorrect import order, a line that exceeded the configured maximum length, and files without a final newline. When the complete pre-commit configuration was executed, other formatting problems such as mixed line endings were also detected.

The tools used during the homework were Pylint, Black, isort, coverage, and several pre-commit hooks.

### Issue 1: Unused Import in task.py

Pylint reported an unused import with the following warning:

```text
W0611: Unused import math
```

The file `src/task.py` contained:

```python
import math
```

However, the `math` module was never used anywhere in the file.

The solution was simply to remove the import.

Removing unused imports makes the code cleaner and avoids unnecessary dependencies.

### Issue 2: Unused Import in app.py

Pylint also detected another unused import:

```text
W0611: Unused import sys
```

The file originally contained:

```python
import sys
```

The application did not use any functionality from the `sys` module, so the import was removed.

This type of problem does not normally cause the application to fail, but static analysis helps detect unnecessary code that could otherwise remain in the project.

### Issue 3: Unused Variable

Pylint detected the following warning in `src/app.py`:

```text
W0612: Unused variable 'temporary_message'
```

The original code contained:

```python
temporary_message = "this variable is intentionally unused"
```

The variable was created but never used by the application.

The solution was to remove the variable completely.

This improved the readability of the `main()` function because every remaining variable now has a clear purpose.

### Issue 4: Line Too Long

Pylint detected a line in `src/task_manager.py` that exceeded the configured maximum length of 88 characters.

The original code was:

```python
return f"Task summary -> total tasks: {total}, completed tasks: {completed}, pending tasks: {pending}, completion tracking enabled"
```

The line was changed to:

```python
return (
    f"Task summary -> total tasks: {total}, "
    f"completed tasks: {completed}, "
    f"pending tasks: {pending}, "
    "completion tracking enabled"
)
```

The behavior of the program remained exactly the same, but the code became easier to read and now follows the configured formatting rules.

A similar long-line problem was also corrected in the unit test file.

### Issue 5: Missing Final Newline

Pylint reported:

```text
C0304: Final newline missing
```

Several files did not contain a newline character at the end of the file.

The `end-of-file-fixer` pre-commit hook automatically corrected this problem.

This was a good example of the advantage of automated static testing tools because the problem did not need to be corrected manually. The hook detected the problem, modified the affected files, and prevented the commit until the corrected files were added again.

### Issue 6: Incorrect Import Order

Pylint detected an incorrect import order in `src/app.py`.

The original imports were similar to:

```python
from src.task_manager import TaskManager
import sys
```

Standard library imports should normally appear before imports from the project.

The isort pre-commit hook automatically reorganized the imports. In this specific case, the `sys` import was later removed because it was not actually being used.

This demonstrated how isort can automatically enforce a consistent import structure across a project.

## 2. Benefits Observed

One of the most important things I observed during this homework is that passing unit tests does not necessarily mean that the code has good quality.

Before fixing the static analysis issues, the original unit tests were already passing successfully. However, Pylint was still able to identify unused imports, unused variables, formatting problems, and excessively long lines.

These issues do not necessarily change the functionality of the program, so traditional functional testing may never detect them.

Static analysis provides an additional layer of validation focused on maintainability, readability, consistency, and code quality.

Another benefit was automation. Tools such as `end-of-file-fixer`, Black, and isort can automatically correct some problems instead of only reporting them.

This reduces the amount of manual work required from developers and also makes formatting more consistent between different team members.

The test suite was later expanded to 23 unit tests. Using the `coverage` tool, the initial source code coverage was approximately 64%. Additional tests were created for methods and branches that were not previously exercised.

After improving the test suite, the final coverage results were:

```text
src/__init__.py       100%
src/app.py             95%
src/task.py           100%
src/task_manager.py   100%
TOTAL                  99%
```

The final result was 92 statements with only one statement not covered, resulting in 99% total source code coverage.

After all corrections, all 23 unit tests passed successfully, all pre-commit hooks passed, and Pylint reported a score of 10.00/10 for the source code.

## 3. Integration Into a Development Workflow

In a real development team, I would use these tools throughout the complete development workflow.

Black and isort could be executed automatically through the IDE or before every commit because they can automatically correct formatting and import organization.

Pylint is useful while developing because it identifies possible code quality problems and provides the exact file, line number, error code, and description of each issue.

Pre-commit is especially useful because it connects all these tools directly to Git.

Before a commit is created, the configured hooks automatically inspect the files. If a problem is detected, the commit is stopped until the developer corrects the issue.

Coverage can also be used together with the unit tests to identify parts of the application that are not being exercised. In this project, the coverage report made it possible to identify missing test cases and increase total coverage from approximately 64% to 99%.

The same static analysis and testing tools could also be executed in a Continuous Integration pipeline after pushing the branch to the remote repository. This would ensure that the same quality rules are applied even if a developer accidentally skips the local hooks.

## 4. Recommendations

The two tools I found most useful were Pylint and pre-commit.

Pylint was useful because its messages clearly explained what the problem was and where it occurred. It was especially helpful for identifying unused imports, unused variables, long lines, and other code quality problems.

Pre-commit was useful because it automated the complete validation process and integrated it directly with Git.

Black and isort were also valuable because instead of only reporting formatting problems, they could automatically correct them.

Coverage was also useful because it showed which parts of the application were not being tested. Increasing the number of tests from 10 to 23 improved the total source code coverage from approximately 64% to 99%.

One important lesson from this homework was that the scope of the hooks must be configured correctly when working inside a large repository. Initially, running `pre-commit run --all-files` caused the hooks to inspect files outside my homework directory. The configuration was then updated so that the hooks only analyze files inside:

```text
students/Luis-045/homework-3/
```

This prevents the static analysis tools from modifying files that belong to other students or other sections of the repository.

For future projects, I would use a similar combination of Pylint, Black, isort, coverage, and pre-commit. I would also make sure that all developers use compatible versions of the tools and that the same checks are executed locally and in Continuous Integration.

Overall, static testing was useful because it detected problems that unit tests were not designed to find, automated repetitive code quality checks, and helped produce cleaner and more consistent code. The coverage report also demonstrated the importance of testing different paths and behaviors instead of only checking whether the existing tests pass.
