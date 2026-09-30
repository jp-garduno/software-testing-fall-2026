# Task Tracker Style Guide

## Python conventions

- Use four spaces for indentation and keep lines at or below 88 characters.
- Format code with Black and sort imports with isort using Black's profile.
- Use `snake_case` for functions and variables, `PascalCase` for classes, and
  `UPPER_CASE` for enum values and constants.
- Add concise module, class, and public-function docstrings that explain the
  contract rather than repeating the implementation.
- Prefer explicit type hints for public inputs and return values.

## Design and safety

- Validate input at the service boundary and raise a clear domain exception.
- Keep each method focused on one behavior; reuse validation helpers instead
  of duplicating rules.
- Avoid dynamically executing input, writing secrets, or silencing security
  findings. Run Bandit before requesting review.

## Tests and commits

- Name tests after observable behavior and cover happy paths, invalid input,
  and error conditions.
- Run `pytest`, Black, isort, Pylint, Bandit, and pre-commit before a commit.
- Use conventional commits such as `feat(homework-3): add task creation`.
