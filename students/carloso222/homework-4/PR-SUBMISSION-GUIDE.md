# Pull Request Submission Guide

## Required path

Move this folder to:

```text
students/<your-github-username>/homework-4/
```

## Branch

```bash
git checkout -b feat/<your-github-username>/homework-4
```

## Five conventional commits

```bash
git add students/<your-github-username>/homework-4/design
git commit -m "docs: add black box test design document"

git add students/<your-github-username>/homework-4/src
git commit -m "feat: add banking system under test"

git add students/<your-github-username>/homework-4/tests/test_equivalence_partitioning.py students/<your-github-username>/homework-4/tests/test_boundary_values.py
git commit -m "test: add equivalence partitioning and boundary value tests"

git add students/<your-github-username>/homework-4/tests/test_decision_tables.py students/<your-github-username>/homework-4/tests/test_state_transitions.py students/<your-github-username>/homework-4/tests/conftest.py
git commit -m "test: add decision table and state transition tests"

git add students/<your-github-username>/homework-4/reports students/<your-github-username>/homework-4/README.md students/<your-github-username>/homework-4/requirements.txt students/<your-github-username>/homework-4/.gitignore
git commit -m "docs: add execution and analysis reports"
```

## Final validation

```bash
cd students/<your-github-username>/homework-4
pip install -r requirements.txt
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
```

Capture the real terminal output and coverage report and save them under `reports/screenshots/`.

## Push and PR

```bash
git push -u origin feat/<your-github-username>/homework-4
```

PR title:

```text
Homework 4: Black Box Testing Suite - Carlos Emiliano Olmedo Navarro
```

Base branch: `main`. Add the **`homework`** label so the automatic grader runs. Submit the PR URL in Canvas.
