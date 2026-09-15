# Homework 3: Static Testing Setup

**Student**: Pablo Portillo
**Project**: Kadu Care NEWS2 Early-Warning Scorer
**Language**: Python 3.11

## Description

A small clinical-monitoring module taken from the Kadu Care domain I analysed in Homework 2. It
validates a set of patient vital signs, computes the NEWS2 (National Early Warning Score 2)
deterioration score with its per-parameter breakdown, and keeps a patient observation history that
reports risk level, trend, and whether clinical escalation is required.

The project was committed first in a deliberately unlinted state so the static analysis tooling had
real findings to report. The git history walks through that baseline (Pylint **6.71/10**, 46
findings) to the current state (**10.00/10**, 28 tests passing).

## Setup Instructions

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Install the pre-commit hooks

   The config is scoped to this directory, so install it with an explicit path from the repository
   root:

   ```bash
   pre-commit install -c students/pabloportillo1/homework-3/.pre-commit-config.yaml \
     --hook-type pre-commit --hook-type commit-msg
   ```

3. Run the hooks over every file

   ```bash
   pre-commit run --all-files -c students/pabloportillo1/homework-3/.pre-commit-config.yaml
   ```

## Pre-commit Hooks Configured

12 hooks across 6 repositories:

| Hook | Purpose |
| --- | --- |
| `trailing-whitespace` | Strips trailing spaces |
| `end-of-file-fixer` | Guarantees a single trailing newline |
| `check-yaml` | Parses every YAML file |
| `check-json` | Parses every JSON file |
| `check-added-large-files` | Blocks accidental blobs over 500 KB |
| `check-merge-conflict` | Blocks committed conflict markers |
| `debug-statements` | Blocks a forgotten `breakpoint()` / `pdb` |
| `black` | Formats Python, 120 character lines |
| `isort` | Orders imports, `black` profile |
| `pylint` | Static analysis against `.pylintrc` |
| `bandit` | Security linting (bonus) |
| `conventional-pre-commit` | Validates the commit message format |

## Project Structure

```
homework-3/
├── README.md
├── REPORT.md                   # Analysis report + documented fixes
├── STYLE_GUIDE.md              # Team style guide (bonus)
├── .pre-commit-config.yaml
├── .pylintrc
├── pyproject.toml              # black / isort / pytest settings
├── requirements.txt
├── pylint-report-before.txt    # Baseline: 6.71/10
├── pylint-report-after.txt     # Current: 10.00/10
├── src/
│   ├── vitals.py               # Reading validation and normalization
│   ├── news2.py                # NEWS2 scoring bands and risk levels
│   └── patient_record.py       # Observation history, trend, escalation
├── test_vitals.py
├── test_news2.py
└── test_patient_record.py
```

## Testing

```bash
pytest -v --cov=src --cov-report=term
```

28 tests cover range validation, every NEWS2 scoring band, risk thresholds, trend detection and
escalation. `test_records_do_not_share_history` is a regression test for the `W0102` mutable
default argument bug that Pylint found — it fails against the original code in commit `4cb5571`.

## Static Analysis

```bash
pylint --rcfile=.pylintrc src     # 10.00/10
black --check --line-length=120 src test_*.py
isort --check-only --profile=black --line-length=120 src test_*.py
```

CI runs the same checks on every pull request touching this directory — see
`.github/workflows/homework-3-static-analysis.yml`.
