# Static Testing Report

**Student:** DiegoGom05
**Project:** Calculator
**Language:** JavaScript

---

## 1. Issues Found

During the static testing process, ESLint initially found **18 errors** in the JavaScript project. The errors were mainly related to undefined and unused variables and functions.

The most common category was **`no-undef`**, with **12 errors**. These errors occurred because functions such as `appendDecimal`, `updateDisplay`, `appendNumber`, `getDisplayValue`, `calculate`, `displayResult`, `showError`, and `clearDisplay` were being used in `app.js` without being properly imported or defined in that file. This revealed an important problem with the organization of the JavaScript modules.

The second category was **`no-unused-vars`**, with **6 errors**. These errors appeared in `display.js` and `operations.js`, where functions were defined but ESLint could not detect that they were being used by other files. The main issue was that the functions were not exported, so the connection between the different modules was not explicit.

Prettier and the pre-commit hooks also identified formatting issues such as trailing whitespace and missing newlines at the end of files. These issues were automatically fixed by the configured hooks. The combination of ESLint and Prettier therefore identified both functional code-quality problems and formatting inconsistencies.

---

## 2. Benefits Observed

Static testing was useful because it detected problems before running or manually testing the calculator. The most important issue found by ESLint was the incorrect use of functions across JavaScript files. Without static analysis, these problems could have resulted in runtime errors when users interacted with the calculator.

The tools also helped identify formatting problems that are easy to overlook during manual review. For example, trailing whitespace, inconsistent formatting, and missing end-of-file newlines do not normally affect the functionality of the application, but they make the codebase less consistent and harder to maintain.

Some of these problems could have been found through manual code review, especially the missing imports and exports. However, manually checking every function and every file is slower and more error-prone. ESLint can identify these problems immediately and consistently.

The setup required some initial time to install the dependencies, configure ESLint and Prettier, create the pre-commit configuration, and fix the detected issues. However, this initial investment can save time later by preventing simple problems from reaching other developers or the CI pipeline. Automatic formatting also reduces the amount of time developers need to spend reviewing style-related changes.

---

## 3. Integration

These tools could be integrated into the team's development workflow at several levels.

### IDE

ESLint and Prettier can be integrated into the developer's IDE. This provides immediate feedback while writing code and allows developers to fix problems before committing their changes.

### Pre-commit

The configured pre-commit hooks should run whenever a developer creates a Git commit. The hooks can automatically check formatting, validate configuration files, and perform other static checks. This prevents common problems from entering the repository.

### CI Pipeline

ESLint and the other static analysis tools should also run in the CI pipeline whenever a pull request is created. This provides an additional layer of protection because the CI environment can verify that the code meets the project's quality standards before it is merged.

Using all three levels provides fast feedback in the IDE, local protection through pre-commit hooks, and centralized verification through CI.

---

## 4. Recommendations

The most useful tools in this exercise were **ESLint and Prettier**. ESLint was particularly valuable because it detected actual problems in the JavaScript code, while Prettier provided automatic and consistent formatting.

One possible improvement would be to configure ESLint with additional rules for code complexity, naming conventions, and potential bugs. The project could also configure Prettier and ESLint to work together more closely so that formatting and code-quality rules do not conflict.

I would use these tools in future projects because they require relatively little maintenance after the initial configuration and provide continuous feedback during development. Automated static testing is especially useful in team projects because it establishes consistent standards and reduces the number of simple errors that reach code review or production.
