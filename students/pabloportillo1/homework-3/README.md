# Homework 3: Static Testing Setup

**Student**: Pablo Portillo
**Project**: Kadu Care NEWS2 Early-Warning Scorer
**Language**: Python

## Description

A small clinical-monitoring module extracted from the Kadu Care domain I analysed in Homework 2. It
validates a set of patient vital signs, computes the NEWS2 (National Early Warning Score 2)
deterioration score with its per-parameter breakdown, and keeps a patient observation history that
reports risk level, trend, and whether clinical escalation is required.

## Setup Instructions

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks

   ```bash
   pre-commit install
   ```

3. Run the tests

   ```bash
   pytest -v
   ```

## Pre-commit Hooks Configured

To be added in the next commits.

## Testing

```bash
pytest -v --cov=src --cov-report=term
```
